# PIC / FatLTO Native Path Design

Nov 20, 2026 · @Hao

We keep the regular-LTO IR fallback and protect the native path with producer `-fPIC`, strict `-z text` linking and an image release scan. On the Tizen GNU linker, a non-PIC absolute data reference in code links silently today.

## 1. The two consumption paths

- **IR path.** The LLVM LTO plugin consumes the bitcode and links it into a shared object or PIE. The existing fallback (`lto-nonpic-in-pic-output-fallback.patch` in OBS llvm) regenerates code from eligible non-PIC IR with the PIC relocation model. `-lto-warn-nonpic-in-pic-link` reports each affected module, tagged `[tizen-nonpic-fallback]`. Scope: regular LTO. ThinLTO and GCC LTO are validated separately.
- **Native path.** GNU ld, GCC or a no-LTO link consumes the FatLTO object's native code, or any non-LTO object. The relocation model was fixed at compile time, so the IR fallback cannot help here.

## 2. Tizen linker test

Run inside the Tizen armv7l GBS root with GNU ld 2.43 (`binutils-2.43-3.49.armv7l`):

| Non-PIC input | Shared object, default | PIE, default | With `-z text` |
| --- | --- | --- | --- |
| `R_ARM_ABS32` in `.text` | Links, exit 0, `DT_TEXTREL` + dynamic `R_ARM_ABS32` | Links, exit 0, `TEXTREL` | Rejected: “read-only segment has dynamic relocations” |
| `R_ARM_ABS32` in `.data` (control) | Links, no TEXTREL | Links, no TEXTREL | Links, no TEXTREL |
| External `R_ARM_REL32` | Rejected (“recompile with -fPIC”) | Rejected | — |
| Absolute `MOVW` / `MOVT` | Rejected (“recompile with -fPIC”) | Rejected | — |
| `R_ARM_TLS_LE32` | Rejected (“not permitted in shared object”) | Links (valid for PIE) | — |

The production Product build.conf and both Base configs contain no `-z text`. TEXTREL pages are written by the loader and become private dirty memory. Unsupported runtime relocations can also stop a library from loading, as happened with the historical non-PIC `libgstomx.so` (relocation type 0x03). The earlier 56-case matrix (38 linked and passed, 18 rejected) used strict `-z text`, so its rejections do not describe the default production link.

## 3. Protections on the native path

1. **Produce compatible objects.** Build `-fPIC` for native objects shipped as reusable shared/PIE inputs, including members of `*-devel` and `*-devel-static` RPMs. Fixes go through LLVM migration shelves.
2. **Reject text relocations at the final link.** Trial `-Wl,-z,text` in the armv7l LLVM build.conf, and `-z text` for direct linker calls. Exemptions need a named package, output, owner, reason and review date.
3. **Scan every shipped image.** Check every ARM32 DSO and PIE, prebuilt and TPK content included, for `DT_TEXTREL` / `DF_TEXTREL`, dynamic relocations into read-only or executable segments, and local-exec TLS in DSOs.
4. **Qualify external inputs.** Require a PIC/TLS-compatible variant from the supplier, or reject the consumer. Rewriting already emitted machine code is out of scope: the addressing and TLS semantics cannot be recovered without source or IR.

## 4. Coverage boundary

| Case | Policy |
| --- | --- |
| Absolute data reference into read-only or executable storage | Producer PIC and `-z text` cover the consuming link; the image scan catches what ships |
| Absolute MOVW/MOVT, external REL32 | Rejected by the linker; producer PIC required |
| Local-exec TLS in a DSO or plugin | Producer TLS model plus consumer test; valid in a main executable |
| Startup objects, fixed-address non-PIE outputs, firmware, kernel | Own link and loader rules; reuse in a shared/PIE output brings them into this policy |
| ABI incompatibilities (for example the Bluetooth calling-convention case) | Separate compatibility review |

## 5. Verification plan

| Step | Check | Pass criterion |
| --- | --- | --- |
| Done | Tizen GNU ld 2.43 fixture: ABS32, writable control, REL32, MOVW/MOVT, TLS | Default accepts ABS32 in code; `-z text` rejects it; other cases recorded |
| 1 | Image relocation scan on the current PERF image, repeated on the matched rebuild | Every shipped ARM32 DSO/PIE scanned; each hit assigned before enforcement |
| 2 | FatLTO routes with the same hashed inputs, default and strict links | Every permissive TEXTREL output detected; strict link rejects it; PIC controls pass runtime tests |
| 3 | build.conf `-z text` trial on the 8 inventory RPMs, gst-ffmpeg and the CAPI FatLTO member | Enforcement visible in effective argv; repaired outputs clean; startup and playback controls pass |
| 4 | GBS native and plugin links for `libcapi-base-common.a:tizen_error.c.o` and the TLS local-exec members of libdw, libasm, libelf, libunwind-arm | Link maps show the members are selected; shared variants use a supported TLS model; loader and thread-local tests pass |

## 6. Reference code

| Component | Location | What it does |
| --- | --- | --- |
| IR fallback | `lto-nonpic-in-pic-output-fallback.patch` (OBS llvm, Source1005): `llvm/include/llvm/LTO/LTO.h`, `llvm/lib/LTO/LTO.cpp` | In regular LTO for a shared/PIE output, clears `dso_local` on declarations and on preemptible definitions of non-PIC modules, and forces the stack-protector guard through the GOT |
| Fallback tests | `llvm/test/LTO/X86/pic-dsolocal-*.ll`, `llvm/test/LTO/ARM/pic-dsolocal-declaration.ll`, `llvm/test/LTO/ARM/pic-stack-guard.ll`, `llvm/test/tools/gold/X86/relocation-model-pic-declaration.ll`, `lld/test/ELF/lto/arm-nonpic-in-pic-output.ll` | Declarations, definitions, TLS models, warning output, ARM stack guard, gold and lld routes |
| Native linker fixture | `gbs-native-textrel.sh` | Assembles one-instruction ARM fixtures inside the GBS root and links each as `-shared` and `-pie` with default, `-z notext` and `-z text` |
| Image relocation scan | `perf-relocations.py` | Reads every ARM32 DSO/PIE of a PERF image and reports TEXTREL, text-targeting dynamic relocations and local-exec TLS in DSOs |

### IR fallback, core logic (`LTO.cpp`, `LTO::addRegularLTO`)

```cpp
bool ClearDSOLocalOnDeclarations =
    M.getTargetTriple().isOSBinFormatELF() && Conf.RelocModel &&
    *Conf.RelocModel != Reloc::Static &&
    M.getPIELevel() == PIELevel::Default;
bool ClearDSOLocalOnPreemptibleDefinitions =
    ClearDSOLocalOnDeclarations && M.getPICLevel() == PICLevel::NotPIC;
RegularLTO.DisableDirectAccessExternalData |=
    ClearDSOLocalOnPreemptibleDefinitions;
if (WarnNonPICInPICLink && ClearDSOLocalOnPreemptibleDefinitions)
  M.getContext().diagnose(DiagnosticInfoGeneric(
      "[tizen-nonpic-fallback] module '" + M.getModuleIdentifier() +
          "' was compiled without -fPIC/-fPIE but is linked into a shared "
          "object or PIE; direct access to its preemptible symbols is "
          "disabled",
      DS_Warning));

// Per global value:
} else if (!GV->isImplicitDSOLocal()) {
  // Only the Function itself keeps a .L$local alias, as in clang.
  bool KeepLocalAlias = R.Prevailing && isa<Function>(GV) &&
                        GV->canBenefitFromLocalAlias();
  if ((GV->isDeclarationForLinker() || !R.Prevailing)
          ? ClearDSOLocalOnDeclarations
          : ClearDSOLocalOnPreemptibleDefinitions && !KeepLocalAlias)
    GV->setDSOLocal(false);
}
```

### IR fallback, stack-protector guard (`LTO.cpp`, `LTO::runRegularLTO`)

```cpp
// Set after every input has been merged, so that an explicit 1
// cannot win the Max merge.
if (RegularLTO.DisableDirectAccessExternalData)
  RegularLTO.CombinedModule->setModuleFlag(
      Module::Max, "direct-access-external-data", 0u);
```

### Opt-in diagnostic (`LTO.cpp`)

```cpp
static cl::opt<bool> WarnNonPICInPICLink(
    "lto-warn-nonpic-in-pic-link", cl::init(false), cl::Hidden,
    cl::desc("Report each module compiled without -fPIC/-fPIE that regular "
             "LTO links into a shared object or PIE"));
```

### Native linker fixture, the decisive case

```asm
.syntax unified
.arm
.text
.global pm_entry
.type pm_entry,%function
pm_entry: bx lr
.p2align 2
.word pm_data      @ R_ARM_ABS32 in .text: default link gives TEXTREL, -z text rejects
```
