# Independent review request: LLVM regular-LTO fallback for non-PIC modules linked into shared objects / PIEs

## Your role

You are an independent reviewer with LLVM LTO and ELF linking expertise. Form your own view from the patch before reading the design doc. Review the attached patch for **correctness and safety**, not style. Assume it will be applied to the production compiler for a whole Linux TV distribution, and that a mistake shows up as wrong symbol binding or a runtime crash, not as a build failure. Be concrete: cite file, line and condition, and give a failing input wherever you claim a defect.

## Where the patch is (shared workspace, repo `lhmax2010/analysis`)

- **Full patch:** `artifacts/patches/lto-nonpic-in-pic-output-fallback.patch` (944 lines, SHA-256 `7d89083453e1d75707a4a6b3a6d9510a4c31e09d8e99865de2a18e07945bf76f`). Confirm the hash before you start.
- **The same content, split in three:** `artifacts/patches/lto-nonpic-in-pic-output-fallback.patch-part-01.txt` … `-part-03.txt`. `cat` of the three parts equals the full patch.
- **Related context, for reference only:**
  - `artifacts/patches/active-llvm.spec-part-0*.txt`: the LLVM spec that applies it as Source1005;
  - `artifacts/patches/driver-pass-llvmgold-to-gnu-ld-by-default.patch.txt`: the driver change that routes `-flto` through LLVMgold with GNU ld;
  - `reports/weekly/2026-11-20/03_PIC_FatLTO_Native_Path_Design.md`: the design doc, which you may read after forming your own view.
- **Where to write your review:** `reviews/lto-nonpic-fallback/REVIEW-<your-name>-<date>.md`.

The patch changes:
- `llvm/include/llvm/LTO/LTO.h`
- `llvm/lib/LTO/LTO.cpp`

It adds tests:
- `llvm/test/LTO/X86/pic-dsolocal-{declaration,declaration-pie,definition,definition-kinds,definition-wins,nonprevailing-pic,warning,tls-models}.ll`
- `llvm/test/LTO/ARM/pic-dsolocal-declaration.ll`
- `llvm/test/LTO/ARM/pic-stack-guard.ll`
- `llvm/test/tools/gold/X86/relocation-model-pic-declaration.ll`
- `lld/test/ELF/lto/arm-nonpic-in-pic-output.ll`

It also adds `lld/test/ELF/lto/wrap-unreferenced-before-codegen.test`. Tell us whether that test belongs to this change.

## Environment

- **LLVM:** 22.1.8 (Tizen package `llvm-22.1.8`), target `armv7l-tizen-linux-gnueabi` (ARMv7-A / ARMv8-A AArch32, Thumb-2 default intended, soft-float ABI with NEON).
- **Linkers:**
  - GNU ld 2.43 with the LLVMgold plugin. A separate local driver patch makes clang pass LLVMgold to GNU ld by default for `-flto`.
  - lld is used for some packages.
- **LTO:** full LTO (`-flto`), often with `-ffat-lto-objects`; ThinLTO is not used in production.
- **Mixed inputs:** about 2,300 packages build with clang. Some static archives and objects reaching a shared-object or PIE link were compiled **without** `-fPIC`/`-fPIE`, for example `*-devel-static` archives or packages that drop the platform CFLAGS.

## The problem the patch addresses

Under `-fno-pic`, clang marks many globals `dso_local`, and the module has `PICLevel::NotPIC`. When such bitcode is merged by **regular LTO** into an output linked as a shared object (`-shared`) or PIE, the code generator honors those per-module `dso_local` flags. It then emits direct, non-GOT references to symbols that are preemptible in the final DSO. The result is:
- link errors (`R_ARM_REL32` / MOVW-MOVT "recompile with -fPIC"), or
- silent `DT_TEXTREL` (absolute relocations in `.text`) on GNU ld, which writes code pages at load time.

The stack-protector guard (`__stack_chk_guard`) is accessed directly in the same way.

The patch makes regular LTO, for shared/PIE outputs, do these things for **non-PIC** modules only:
1. Clear `dso_local` on **declarations** when the output is shared/PIE and the module is not PIE (`ClearDSOLocalOnDeclarations`). This is modelled on the existing ThinLTO `ClearDSOLocalOnDeclarations` logic.
2. Clear `dso_local` on **preemptible definitions** when the module is `PICLevel::NotPIC` (`ClearDSOLocalOnPreemptibleDefinitions`). Exception: a prevailing `Function` that can benefit from a local alias keeps `dso_local` ("only the Function itself keeps a `.L$local` alias, as in clang").
3. Set `RegularLTO.DisableDirectAccessExternalData`. After all inputs are merged, `runRegularLTO` sets the combined module flag `direct-access-external-data` to 0 with `Module::Max`. The intent is that an explicit 1 cannot win the merge, so the stack guard and external data go through the GOT.
4. Add an opt-in, hidden, off-by-default diagnostic `-lto-warn-nonpic-in-pic-link` that prints `[tizen-nonpic-fallback] module '<id>' was compiled without -fPIC/-fPIE …`.

**Intended scope:** regular LTO only, for shared or PIE output, for modules compiled without PIC/PIE. PIC modules, static (non-PIE) executables and ThinLTO must be unaffected.

## Questions to answer

### A. Scope and gating
1. Read the exact conditions (`isOSBinFormatELF()`, `Conf.RelocModel`, `!= Reloc::Static`, `getPIELevel() == PIELevel::Default`, `getPICLevel() == PICLevel::NotPIC`). Does the fallback activate **only** for non-PIC modules in shared/PIE regular-LTO links?
   - Can it activate for a static non-PIE executable?
   - Can it activate for a PIE link of modules compiled with `-fPIE`?
   - Can it activate for a shared link of modules compiled with `-fPIC`?
2. Rule 1 (declarations) is gated on `PIELevel::Default`, not `NotPIC`. So it also applies to `-fPIC` modules in a shared link. Is that correct and harmless? Compare it with what upstream ThinLTO already does for declarations, and with what clang itself emits for `-fPIC` (declarations are not `dso_local` under `-fPIC` anyway, except for visibility attributes).
3. How does `Conf.RelocModel` get set on each linker path: GNU ld + LLVMgold, lld, and the legacy `llvm-lto` / `LTOCodeGenerator`?
   - Is `-shared` vs `-pie` vs a static executable reliably reflected in `RelocModel` on each path?
   - Is there a path where `RelocModel` is unset (`std::nullopt`), so that the fallback silently does nothing?
4. ThinLTO: confirm the change cannot alter ThinLTO behavior, both for the thin backend and for mixed regular + thin LTO in one link.

### B. Semantics and safety
5. **Preemption and visibility.** Can clearing `dso_local` on a definition ever be **wrong**, as opposed to merely slower? Consider:
   - hidden/protected visibility definitions;
   - `-Bsymbolic` / `-Bsymbolic-functions` links;
   - version scripts that make symbols local;
   - `local_unnamed_addr` / `unnamed_addr`;
   - definitions with `internal`/`private` linkage after LTO internalization.

   Does the patch clear `dso_local` before or after the LTO internalization decision? Can that order cause a symbol that is internalized later to be accessed through the GOT unnecessarily, or, worse, a symbol that stays exported to be accessed directly?
6. **`KeepLocalAlias`** (prevailing `Function` that `canBenefitFromLocalAlias()`): does keeping `dso_local` on such a function preserve correct interposition semantics in a shared object? Clang `-fPIC -fno-semantic-interposition` uses `.L$local` aliases. Is this case equivalent, or does it **change** interposition semantics for code that was compiled `-fno-pic` and expected default (interposable) semantics in the DSO?
7. **Aliases, ifuncs, TLS, comdats and weak symbols:**
   - Check GlobalAlias and GlobalIFunc handling.
   - Check `thread_local` variables of each TLS model, including local-exec in a shared object. Is TLS correctly excluded or handled, and does `pic-dsolocal-tls-models.ll` prove it?
   - Check weak/linkonce/comdat definitions where the non-prevailing copy came from a non-PIC module and the prevailing copy from a PIC module, and the reverse.
8. **`direct-access-external-data` with `Module::Max` set after the merge:**
   - Is `Max` the right merge behavior?
   - Does setting the flag on the **combined** module affect codegen for **PIC** modules merged into the same LTO unit? That would be a pessimization, not a correctness problem. Quantify it if you can.
   - Does ARM codegen in LLVM 22 actually read this flag for the stack guard (`__stack_chk_guard`) and for other external data? Point to the code path.
   - Is there any other target-specific direct access, for example a TLS base, `__dso_handle` or the ARM EHABI personality, that is still emitted directly?
9. Can this patch produce a **link-time or load-time failure** that did not exist before? Examples: a new GOT relocation type GNU ld 2.43 cannot handle for ARM, `R_ARM_GOT_PREL` vs `R_ARM_GOT_BREL`, or copy relocations in a PIE.
10. **Concurrency and order:** `RegularLTO.DisableDirectAccessExternalData` is a member that `addRegularLTO` sets, possibly while modules are added in parallel. Is it a data race in any LTO configuration with parallel module loading?

### C. Diagnostics
11. The diagnostic is off by default because "some configure probes treat any linker output as failure". Confirm it is hidden, off by default, and has no effect on codegen when on. Is `DS_Warning` safe with `-Werror`-style linker configurations (`--fatal-warnings` in GNU ld, `--fatal-warnings` in lld)?

### D. Tests
12. Do the tests check the right things?
    - **Checks:** each test should check the IR `dso_local` result and the final relocations or codegen, and each should have a negative control (PIC module, static executable, ThinLTO).
    - **ARM coverage:** a non-PIC module referencing a preemptible definition, a declaration, the stack guard and TLS, each in both a shared and a PIE link, through both lld and gold/LLVMgold.
    
    Name each missing test case precisely, and write the RUN lines and CHECK lines you would add.
13. Do any tests depend on host details (X86 only, a specific `ld.gold` path) such that they would be silently skipped in the Tizen build (`UNSUPPORTED`)?

### E. Alternatives and upstream
14. Is there an upstream LLVM mechanism or a discussion (Phabricator / GitHub PR / Discourse) for the same problem? For example: LTO honoring the output relocation model over per-module `dso_local`, `-fno-direct-access-external-data`, or lld's handling of non-PIC bitcode in `-shared`. If an upstream approach exists, compare it with this patch and say which to prefer.
15. Would a simpler or more conservative design be safer? For example:
    - reject the link with a clear error instead of rewriting;
    - re-run the module through a "make PIC" IR pass;
    - force `-fPIC` at the producer only.

    Give the trade-offs for a distribution where some producers cannot be rebuilt.

## Output format

1. **Verdict:** one of `SAFE TO SHIP`, `SHIP WITH CHANGES` or `DO NOT SHIP`, with one paragraph of reasoning.
2. **Findings table:**

   | # | Severity (Critical / Major / Minor / Note) | File:line | Finding | Concrete failing input or scenario | Suggested fix |
   | --- | --- | --- | --- | --- | --- |

3. **Missing tests:** ready-to-add RUN/CHECK snippets.
4. **Answers to questions 1–15:** one short paragraph each, saying what you verified by reading code and what you infer. Mark inference clearly.
5. **Anything outside these questions** that you believe is a risk.

Do not rewrite the patch wholesale. If you propose code changes, keep them minimal and show them as a unified diff against the patched files.
