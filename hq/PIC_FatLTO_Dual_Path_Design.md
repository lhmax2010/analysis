# Proposed PIC policy for ARMv7l FatLTO and native links

A FatLTO object contains LLVM IR and native machine code. The protection depends on which the linker consumes. We propose keeping the LLVM IR fallback and qualifying native inputs through producer flags, strict linking and an image release check.

## IR consumed by the matching LLVM LTO plugin

For a regular LLVM LTO link that requests a PIC relocation model, the existing fallback regenerates code from eligible non-PIC IR. Enable `-lto-warn-nonpic-in-pic-link` in qualification builds and retain the tagged `tizen-nonpic-fallback` diagnostic with the input, final output kind and plugin evidence. This policy covers the existing regular-LTO rules for shared libraries and PIE. ThinLTO follows its own import, symbol-resolution and code-generation rules. GCC LTO follows GCC's own plugin and IR rules. Validate both separately where used. Mixed toolchains can consume a compatible native member, subject to the policy below.

The Tizen ARM synthetic matrix had 56 cases. Under its tested linker settings, 38 linked and passed runtime checks, and 18 failed on native relocations. Those results include strict `-z text`. A linker may also reject some instruction and TLS relocations independently of that option. [Tizen ARM validation](../artifacts/evidence/arm-pic-matrix.txt)

## Native code consumed by GNU ld, GCC or a no-LTO link

A native consumer receives the relocation assumptions made at compilation. A linker that allows text relocations can accept a non-PIC absolute reference and emit `DT_TEXTREL` or `DF_TEXTREL` in the final shared object or PIE. Loader writes to formerly read-only file-backed pages can make those pages private and dirty. Unsupported runtime relocation types can prevent the library from loading. This has occurred on Tizen. The historical non-PIC `libgstomx.so` failed to load with relocation type `0x03` (`R_ARM_REL32`). That incident establishes the loader failure mode. [GNU ld options](https://sourceware.org/binutils/docs/ld/Options.html) [Arm ELF relocation types](https://github.com/ARM-software/abi-aa/blob/main/aaelf32/aaelf32.rst) [Tizen stability evidence](../artifacts/historical-reports/stability-report.md#L44)

The native-link fixture ran inside Tizen armv7l GBS with GNU ld 2.43 from `binutils-2.43-3.49.armv7l` (ld SHA-256 `2b5cb60876bd4da4711fe9e7cd6bd92f0ec1c6335695b0a53665b2d936c80f3d`). A reference in `.text` requiring a dynamic absolute relocation linked successfully as a DSO and as PIE under the tested default and explicit `-z notext`. Both outputs had `DT_TEXTREL`, `DF_TEXTREL` and a dynamic `R_ARM_ABS32`. Enforcing `-z text` rejected both links with “read-only segment has dynamic relocations.” [GBS linker evidence](../artifacts/evidence/native-run-r0008-ldprobe-forensics-usbmethod-20261120.txt#L87)

| Fixture input | Default shared link | Default PIE link | With `-z text` |
|---|---|---|---|
| `R_ARM_ABS32` in `.text` | Success with TEXTREL | Success with TEXTREL | Both rejected |
| `R_ARM_ABS32` in writable `.data` | Success without TEXTREL | Success without TEXTREL | Both pass without TEXTREL |
| External `R_ARM_REL32` | Rejected | Rejected | Not required for rejection |
| External absolute MOVW/MOVT | Rejected | Rejected | Not required for rejection |
| Local definition with `R_ARM_TLS_LE32` | Rejected | Success without TEXTREL | Not exercised for this fixture |

The retained production Product build.conf `98690f23…` and both Base configs `b5e6d8e1…` contain no literal `-z text`, `-z notext` or `-z textoff` setting. Establish final linker argv separately for package overrides, direct linker calls, and any other linker used in production. The fixture establishes that a successful link exit is insufficient as a gate. The baseline image scan will measure the shipped incidence. [Configuration and fixture evidence](../artifacts/evidence/native-run-r0008-ldprobe-forensics-usbmethod-20261120.txt#L80)

1. **Produce compatible objects.** Use `-fPIC` for native objects exposed as reusable shared/PIE inputs, including such members shipped in `*-devel` and `*-devel-static` RPMs. Apply fixes through LLVM migration shelves. Capture the actual C/C++/assembly flags, archive-member identity and consuming link command. Explicit assembly addressing and TLS model overrides require their own review. Validate native and LTO variants, including clean no-LTO builds and reused prebuilts.
2. **Reject text relocations at the final link.** Trial `-Wl,-z,text` in the armv7l LLVM build.conf link flags and the equivalent `-z text` for direct linker calls. This rejects the demonstrated successful TEXTREL output. Verify the effective linker argv for shared/PIE links, including packages that set their own link flags or pass a later permissive option. Production adoption follows the baseline image scan and package trial. Each exemption requires an identified package, output, consumer, owner, reason and review date. A shipped finding enters the repair list and requires explicit approval for any temporary exception.
3. **Check the shipped image.** Inspect every ARM32 DSO/PIE in the release scope, including prebuilt and packaged application ELFs. Flag `DT_TEXTREL`, `DF_TEXTREL`, and dynamic relocation writes into read-only or executable segments. Record the target segment and relocation type, including `R_ARM_ABS32`, `R_ARM_REL32` and `R_ARM_RELATIVE`. For DSOs, flag observable local-exec TLS relocations. Reconcile unreadable inputs and covered partitions before accepting a clean scan. Compare findings by image, path, owning package and file hash.
4. **Qualify external inputs.** Require a compatible PIC/TLS variant from the supplier, or reject the affected shared/PIE consumer. Recovering the correct addressing and TLS semantics from already emitted instructions would require source or IR and consumer information that a generic linker rewrite does not have.

## Coverage boundary

| Input or output | Policy |
|---|---|
| Absolute data reference that requires a dynamic write in read-only storage, or a code relocation in an executable segment | Producer PIC and final-link checks cover the consuming shared/PIE link. The image check identifies emitted tags and segment targets. Ordinary relocations into writable data are valid. |
| Absolute ARM/Thumb MOVW/MOVT against a symbol requiring dynamic resolution | Use a compatible producer. Some final links reject the instruction relocation directly. The image check examines runtime relocations that survive emission. |
| Local-exec TLS in a DSO or plugin | Qualify the producer TLS model and actual consumer. Scan retained ELF relocations where present. Resolved relocations erased from stripped output require compile/link evidence and a runtime test. A main executable can legitimately use local-exec TLS for its own definitions. |
| Native startup objects and fixed-address non-PIE outputs, firmware and kernel | Validate with their own link and loader rules. Shared/PIE reuse brings that consumer into this policy. |
| Source-level or runtime ABI incompatibilities | Separate compatibility review, including the Bluetooth shared-library calling convention issue. |

## Verification and acceptance

| Order and owner | Check | Pass criterion |
|---|---|---|
| Done · Toolchain validation | Tizen GNU ld 2.43 native ABS32 test and writable-data, REL32, MOVW/MOVT, TLS controls. | Default and notext accept ABS32 in code. Strict link rejects it. Writable control passes, and the other relocation cases have recorded outcomes. |
| 1 · Release integration | Scan the retained flat Customized PERF partitions and repeat on the matched rebuild. Reconcile partitions, including any separately delivered /prd payload, before release acceptance. | Every shipped ARM32 DSO/PIE is scanned or has reconciled coverage evidence. Record and assign each existing hit before enforcement. Final gate permits only explicit, reviewed exceptions. |
| 2 · Toolchain validation | Extend the completed native linker fixture to the actual FatLTO routes using the same hashed inputs, with default and strict links. Include ABS32, REL32, MOVW/MOVT and TLS_LE controls. | Linker and route are proven. Each permissive output with a text relocation is detected and the strict link rejects it. PIC controls link and pass runtime tests. Report unconditional rejections separately. |
| 3 · Build integration and package owners | Trial the armv7l build.conf flag on the eight RPM inventory entries, the gst-ffmpeg build-input case and the CAPI FatLTO case. | Effective argv shows enforcement in each applicable consumer. Repaired inputs produce clean outputs and intended startup, executable, loader and playback controls still pass. |
| 4 · Consumer owners | Repeat the GBS native and plugin links for `libcapi-base-common.a:tizen_error.c.o` and the TLS-local-exec members in libdw, libasm, libelf and libunwind-arm. | Link maps prove that the relevant members were selected and identify the final output type. Shared variants use a supported TLS model. Accepted consumers pass loader and thread-local behavior tests on the intended path. |

The design can be reviewed before the baseline completes. Enabling enforcement in release builds needs the baseline and package trial. Retain the linker identity, compile and link traces, input and output hashes, exceptions and runtime results with each image. Compare paired board builds for affected startup, playback, code size and memory before adopting a wider policy.
