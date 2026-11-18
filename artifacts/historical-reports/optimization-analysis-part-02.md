
Local measurements (.text, KB; change relative to the unchanged configuration in parentheses):

| Package | GCC image | Unchanged | Threshold 50 | Threshold 25 | ML inliner (release) | `-fno-inline-functions` | `-finline-hint-functions` | MachineOutliner |
|---|---|---|---|---|---|---|---|---|
| openusd (`-O3`) | 8,135 | 8,971 | 6,223 (−30.6%) | **5,561 (−38.0%)** | 8,371 (−6.7%) | 5,950 (−33.7%) | 8,308 (−7.4%) | 7,430 (−17.2%) |
| app-installers (`-Os`) | 727 | 1,295 | no change | 1,023 (−21.0%) | 1,499 (+15.7%) | 646 (−50.1%) | 1,231 (−5.0%) | not measured |
| dali2-adaptor (`-Os`) | 1,379 | 1,819 | no change | 1,475 (−18.9%) | 1,836 (+0.9%) | 1,556 (−14.5%) | 1,765 (−3.0%) | 1,585 (−12.9%) |
| avoc-daemon (`-O2`) | 647 | 1,247 | build failed | build failed | build failed | 803 (−35.6%) | 847 (−32.0%) | build failed |

- With ML inlining turned off, every sample package produced output byte-identical to the unchanged configuration: the gap is unrelated to MLGO, which is currently used for the Linux kernel only.
- **A lower inlining threshold comes closest to the effect of GCC's `-fno-inline-functions`:** small functions are still inlined, and only the inlining of larger functions is reduced.
  - threshold 50 affects only code not built at `-Os`, because the threshold under `-Os` is already 50;
  - threshold 25 amounts to using the `-Oz` inlining threshold on `-Os` code;
  - affected samples in total: threshold 50 reduces the part loaded at run time by 14.3%, threshold 25 by 23.3% (−6.5 MB).
- **clang's `-fno-inline-functions` cannot be used.** It marks every function not marked always_inline as "do not inline". The mark is stored in the LTO intermediate code, so cross-file inlining at the LTO stage is switched off as well. Added through the global optimization options, it raised libgrpc's exports from 46,117 to 164,783 and its part loaded at run time by 180%.
- **Other candidates:**
  - `-finline-hint-functions` gains little: −0.9% of the part loaded at run time over the samples;
  - the release mode of the ML inliner is inconsistent (webappservice −42.5%, app-installers +13.9%).
- **Implementation:** avoc-daemon's build tool rejects `-mllvm` arguments, and `-Wl,-plugin-opt` fails on links that do not perform LTO (these are the build failures in the table). The inlining threshold and MachineOutliner therefore have to be implemented as defaults in the llvm package: through clang's default configuration at compile time and through LLVMgold's default options at the LTO stage.
- org.tizen.webappservice is still 86% larger than GCC after the gap to the forced options is closed. It is built at `-Os`, so it falls under threshold 25.

#### Conclusion

1. **Close the gap to the options forced by the GCC lane** in batch 1, changing only the product build.conf. This also removes the differences in `char` signedness and hardening.
2. **Inlining policy of the exempt packages** in batch 2: implement a lower inlining threshold (25 or 50) and MachineOutliner as defaults in the llvm package, compare performance with TPMS on an experimental image, then choose. For performance-sensitive processes such as avocd and tv-viewer, no performance loss is the precondition.
3. **Package-defined optimization levels**: unchanged for the exempt packages, consistent with the GCC lane; the non-exempt packages are handled by point 1 the same way the GCC lane handles them.

### 6.4 `-ffunction-sections -fdata-sections` + `--gc-sections` (not recommended)

#### Data

- openusd rebuilt in a local build environment: with this group of options, `libusd_usd.so + libusd_sdf.so` went from 8,910 KB to 8,978 KB, **no gain, 0.8% larger**.
- In the new image, executables hold 125.99 MB of .text (1304 files, 19%), shared libraries 519.59 MB (3393 files, 79%).
- The current build.conf does not contain this group of options.

#### Analysis

- In shared libraries, all functions with default visibility are exported. Exported functions count as referenced, so the linker cannot remove them; the options are largely ineffective for shared libraries, which matches the openusd measurement.
- In executables, unreferenced functions can be removed. For files built with LTO, unreferenced code has already been removed during LTO, so the remaining room is only in executables built without LTO, which is a small share.
- Risk: code that relies on sections that are not referenced (custom linker scripts, `__start_`/`__stop_` sections) may be removed by mistake, which requires per-package verification.

#### Conclusion

The gain is very small and per-package verification is required. **Not recommended.**

### 6.5 RELR relocation packing (adopted with lld)

#### Data (all 4780 ELF files of the new image)

| Relocation type | Count | Share | Size |
|---|---|---|---|
| R_ARM_RELATIVE (relative) | 2,561,353 | 64.8% | 19.54 MB |
| R_ARM_JUMP_SLOT | 734,695 | 18.6% | 5.61 MB |
| R_ARM_ABS32 | 517,998 | 13.1% | 3.95 MB |
| R_ARM_GLOB_DAT | 135,129 | 3.4% | 1.03 MB |

- Computed file by file with the actual RELR encoding rules: all 2.56 million relative relocations are aligned; with RELR they need only 186,679 words (0.71 MB), **saving 18.83 MB of file size**.
- Packages with the largest saving: vd_memps 3.68 MB, chromium-efl 3.57 MB, org.tizen.tts-engine-vd 1.51 MB, lightweight-web-engine-profile_tv 1.14 MB, org.tizen.tv.swu 0.53 MB. The first three are not built by the clang lane; changing them requires adding options to their own builds.
- glibc in the new image is 2.40; the loader supports DT_RELR (since glibc 2.36).

#### Difference from RELRO

RELR and RELRO are two different mechanisms:

- **RELRO** (`-Wl,-z,relro`) makes regions such as the GOT and .data.rel.ro read-only after relocation; it is a security hardening measure. Both the GCC lane and the LLVM lane already use it: `__optflags` on line 459 of the product build.conf contains `-Wl,-z,relro,--as-needed`, and `%build_ldflags` of the Base also contains `-Wl,-z,relro`. No change is needed here.
- **RELR** (`-z pack-relative-relocs`) is a compact format for the relative relocation table. The GCC image does not use it either: .rel.dyn is 24.52 MB in the GCC image and 24.51 MB in the LLVM image. RELR would therefore be a new optimization for both sides.

#### Risks and prerequisites

- **The main earlier concern is gone.** The concern was that prelink might not understand RELR. On 2026-11-12 it was decided to keep PIE and drop prelink (also in the GCC image), so this concern no longer applies.
- **Only with lld.** GNU ld does not support `-z pack-relative-relocs` on 32-bit ARM; lld does. The option will be restored in the lld default-linker configuration.
- **Gain.** Without prelink, relative relocations are processed at run time, and RELR does not change the number of data pages that get modified. The gain is mainly file size (18.8 MB) and a smaller relocation table to read at load time.
- vd_memps, chromium-efl and org.tizen.tts-engine-vd are not built by the clang lane; the option has to be added in their own builds.

#### Conclusion

**Adopt together with the switch to lld (batch 3).** After the image is built, check the loader's handling and the boot time.

### 6.6 Relative vtables (not adopted for now; long-term item)

#### Data

- .data.rel.ro totals 19.10 MB with 2,685,117 dynamic relocations, 67.9% of all dynamic relocations.
- Of these, 86,245 C++ vtables (4.50 MB) carry 989,350 relocations, 25.0% of all dynamic relocations.
- Packages with the most vtable relocations: chromium-efl 316,046, vd_memps 145,593, org.tizen.tv.swu 39,655, lib-lcc-player-tv 25,493, opencv 20,734.

#### Analysis

- Relative vtables (`-fexperimental-relative-c++-abi-vtables`) replace the absolute addresses in vtables with relative offsets, so no relocations are needed and the vtables can live in read-only, shareable pages. Based on the data, up to 25% of dynamic relocations could be removed.
- Without prelink, every library processes its relocations at run time, so the gain of this item will be larger than earlier estimated.
- This changes the C++ ABI: all modules that pass C++ objects to each other (including the C++ standard library) must switch at the same time, and modules built by GCC do not support it.

#### Conclusion

The gain can be quantified, but an image-wide ABI switch is required. **Listed as a long-term item**; not adopted at this stage.

### 6.7 Unwind tables (find the cause first)

#### Data

- .ARM.exidx: GCC 8.61 MB, new LLVM 10.05 MB (+1.44 MB); .ARM.extab: GCC 22.05 MB, new LLVM 25.71 MB (+3.66 MB).
- The whole +5.10 MB comes from files built by clang; files not built by clang show no increase.
- The packages with the largest increase are all C++ packages: tee_test_suite +0.49 MB, native-home +0.31 MB, lightweight-web-engine-profile_tv +0.30 MB, org.tizen.tv.swu +0.29 MB, openusd +0.21 MB, libgrpc +0.17 MB.

#### Analysis and conclusion

- Unwind tables are read only for exception handling and crash backtraces, and are normally not resident in memory, so the memory impact is small.
- Turning off unwind tables is not a solution, because it would affect coredump backtraces.
- Next, for the packages with the largest increase, compare the number of functions and the unwind records per function on both sides to find why clang produces more, and then decide whether any action is needed.

### 6.8 Local rebuild measurements: ThinLTO, MachineOutliner, lld ICF, `-fstack-protector-strong`

#### Method and conditions

- **Build conditions**: the original build.conf of the new image's product project, with the product repository 20261111.1 and Base 20261105.1, identical to Quickbuild 37518055. Each option is built separately.
- **How the options were added**: in the first round, the option was appended to the compile options that build.conf exports for every package (environment variables). Some packages (e.g. libgrpc, protobuf) use the optflags of build.conf directly and do not read the environment, so in the second round the option was added to optflags, the same way it would be rolled out.
- **Consistency of conditions**: the 136 image files produced by rebuilding 19 sample packages with the unchanged configuration differ from the same files in the image by 0.1% in total file size; total .text is 57,528 KB versus 57,533 KB, and except for pkgmgr-info (1.1% difference) the .text of every package is identical. The local conditions match Quickbuild, so the differences below can be cited directly.
- **Scale**: 22 sample packages, 151 builds up to this report (including the forced-option and inlining experiments of Section 6.3), 126 successful, 25 failed.
- **Metrics**: only ELF files on the image file list are counted. For each configuration, only packages where the option actually took effect are counted, i.e. packages whose output differs from the unchanged configuration; byte-identical output is not counted. In addition, the build logs were checked command by command for whether the option was present and which optimization level was in effect (results in 6.3).
- **Build time**: this round ran 4 jobs in parallel, and the timing includes build environment setup, so it fluctuates and is indicative only.

#### Results (relative to the unchanged configuration)

| Option | Packages where it took effect | Part loaded at run time | .text | Unwind tables | Dynamic symbol tables | Conclusion |
|---|---|---|---|---|---|---|
| ThinLTO (`-flto=thin`) | openusd, avoc-daemon, dali2-adaptor, libfreetype | +0.5% | −0.1% | +8.7% | 0 | Size essentially the same as full LTO |
| MachineOutliner | openusd, dali2-adaptor | **−8.1%** (−1.5 MB) | **−16.5%** | +21.6% | 0 | Clear gain; performance to be assessed |
| `-fstack-protector-strong` | openusd, avoc-daemon, dali2-adaptor, libgrpc | +2.1% | +4.2% | +1.2% | 0 | Cost of security hardening |
| lld (vs. GNU ld) | openusd, libgrpc, avoc-daemon, libfreetype | +0.6% | +0.2% | +1.2% | +0.3% | About the same |
| lld + `--icf=safe` (vs. GNU ld) | Same as above | **−2.3%** | **−3.5%** | −19.5% | +0.3% | Clear gain |

Notes:

- **ThinLTO**: size is essentially the same as full LTO. In this round, the build time of these 4 packages dropped by about 20% in total. The earlier separate measurement showed that, relative to no LTO, ThinLTO adds only 2% while full LTO adds 64% (table below). ThinLTO is suitable as the default LTO mode. It will be implemented as planned: the llvm package makes clang treat `-flto` as ThinLTO by default; the global macros stay unchanged, so packages built by GCC are not affected.
- **MachineOutliner**: extracts repeated instruction sequences into shared functions; openusd .text −17.2%, dali2-adaptor −12.9%.
  - The cost is an extra call and return for the extracted code, which may slow down hot paths; this must be measured with TPMS. Unwind tables grow by 21.6% because many small functions are added.
  - On 32-bit ARM it is enabled through a back-end option, which under LTO must also be passed at link time. Passed through the global options, it fails on links without LTO, and avoc-daemon's build tool rejects the argument. Like the inlining threshold, it is therefore to be implemented as a default in the llvm package (Section 6.3).
- **`-fstack-protector-strong`**: the global options of the GCC lane use `-strong`, while the clang lane uses the narrower `-fstack-protector`. Aligning costs +2.1% of the part loaded at run time (+2.7% for libgrpc, +1.4% to +1.7% for the other 3 packages).
  - For the non-exempt packages it is aligned as part of closing the gap to the forced options (6.3);
  - whether to align the exempt packages depends on security requirements.
  - libfreetype's output did not change (no additional functions needed protection).
- **lld and lld + ICF**:
  - lld alone is about the same as GNU ld. With `--icf=safe` (merging functions with identical contents) it is 2.3% smaller than GNU ld and 2.9% smaller than lld alone; openusd −5.0%, avoc-daemon −3.4%.
  - **The cause of the slow local lld builds is known**: the ld.lld in the build root is a 32-bit ARM program that runs under qemu emulation (the compiler and LLVMgold are accelerated native x86 versions). An accelerated native x86 lld must be provided in the build root before switching to lld.
  - **dali2-adaptor fails to link with lld**: libdali2-adaptor.so uses `tizen_policy_interface` and `tizen_display_policy_interface` without linking the library that provides them. GNU ld lets this pass, lld rejects it by default (`--no-allow-shlib-undefined`). The missing library must be added in the package; a global `--allow-shlib-undefined` is not adopted.
- **Failed builds (25)** do not affect the conclusions above:
  - the Base packages (boost, abseil-cpp, icu) must be rebuilt in the Base build environment (6 jobs);
  - aurum, org.tizen.mbr-daemon and native-home already fail locally with the unchanged configuration, due to local source or dependency issues (6 jobs);
  - the rest are caused by the test method: link-time options rejected on links without LTO, build tools of individual packages rejecting certain arguments, the lld link error above, and the tvs-si compile error of 6.3 when the warning options were appended along with the forced options.

Earlier ThinLTO measurement (11-03 conditions, openusd, libusd_usd.so + libusd_sdf.so):

| Configuration | Both libraries | vs. no LTO | Package build time |
|---|---|---|---|
| No LTO | 15,700,824 B | — | 240 s |
| Full LTO | 13,588,464 B | −13.5% | 393 s (+64%) |
| ThinLTO | 13,651,248 B | −13.1% | 245 s (+2%) |

### 6.9 Options explicitly not recommended

| Option | Reason |
|---|---|
| Global `-fvisibility=hidden`, `-Bsymbolic-functions` | Breaks C interface exports or symbol interposition (e.g. LD_PRELOAD replacing malloc); too broad an impact |
| Disabling unwind tables | Affects coredumps and crash backtraces |
| Global `-Oz` | Measured gains are concentrated in a few packages; highest performance risk; most exempt packages set their own optimization level, which a global `-Oz` does not reach |
| Copying `-fno-inline-functions` directly | clang's option of the same name is much stricter than GCC's and also switches off inlining at the LTO stage; libgrpc's part loaded at run time +180%; use a lower inlining threshold instead (6.3) |
| Disabling LTO | .text changes little, while exports increase by more than 20% |
| Switching the whole clang lane to `-O2` | The symbol metadata issue is solved by LTO (Section 5); clang code is smaller than GCC's in 1388 packages, and a global `-O2` would increase size and memory. The `-O2` of the GCC lane corresponds to `-Os` in the clang lane; this mapping is already used for the VD flag macros and for the forced options |
| Global `--allow-shlib-undefined` | Hides missing library dependencies; these are fixed in the packages concerned |
| The gc-sections group | See 6.4 |

### 6.10 Rollout order

| Batch | Content | Basis | Approach and prerequisites |
|---|---|---|---|
| Batch 1 | Close the gap to the options forced by the GCC lane | 6.3: part loaded at run time −25.9% in the samples; removes the differences in `char` signedness and hardening | Product build.conf only (10 lines added, comments included), verified locally in its final form; with functional testing |
| Batch 1 | `-fvisibility-inlines-hidden`, excluding openusd, tvs-si, aurum | 6.2: in packages where it took effect and no exclusion is needed, dynamic symbol tables −44%, part loaded at run time −11% | Product build.conf only (2 lines added, 1 changed), verified locally in its final form; image-wide export check after the image is built |
| Same time | ThinLTO as the default LTO mode | 6.8: same size as full LTO, much shorter build time | llvm package change |
| Batch 2 | Lower inlining threshold, MachineOutliner | 6.3, 6.8: part loaded at run time −8% to −23% in the affected samples | Implemented as defaults in the llvm package; chosen after TPMS confirms performance |
| Batch 3 | lld + `--icf=safe`, RELR | 6.5, 6.8: part loaded at run time −2.3%; files −18.8 MB | With the switch to lld as default linker; accelerated lld and the dali2-adaptor fix first |
| Separate | VD warning options and `-Werror`; `-fstack-protector-strong` for the exempt packages | The former is a build quality gate that does not change the output; the latter costs about +2% | For the former, count new errors in a Quickbuild first; the latter depends on security requirements |

- Each batch gets its own image. After each image is built, four checks are always run:
  1. the image-wide export check;
  2. the LTO coverage check;
  3. boot time and memory measured on the board;
  4. TPMS performance comparison.
- Both items of batch 1 touch only the product build.conf; rolling back means deleting the added lines.

### 6.11 Other optimization directions being explored

This section covers the compile options that can already be evaluated with data; it is not the whole of the optimization work. The following directions are being pursued in parallel:

- **New or improved LLVM passes**:
  - new MLGO policies, including model-based hot/cold code splitting and basic block placement;
  - custom optimization passes for hot modules, e.g. media codec modules;
  - improvements to inlining decisions addressing the "clang code larger than GCC" issue of the exempt packages in 6.3.
- **Link-time optimizations that become possible with lld**:
  - identical code folding (ICF);
  - RELR relocation packing;
  - global function merging based on ThinLTO (available since LLVM 20);
  - link-time code layout optimization.
- **Image-level optimizations**:
  - the .symtab retention policy, e.g. MiniDebugInfo instead of full symbol tables;
  - switching packages whose build scripts hard-code gcc/g++ to the global toolchain, so that they also benefit from the optimizations above.

These directions will be added to the evaluation as data becomes available.

## 7. Stability: Coredumps After Introducing LTO

The 20261111.1 image produced 30 cores:

| Category | Processes | Count | Root cause | Status |
|---|---|---|---|---|
| SIGSEGV | avocd, deviced, wrt-loader, fw-update-service, issue_report_agent, boot_splashscreen | 22 | `PrdUtil::GetKeyData()` in prd-factory-api reads the uninitialized `keyData.value` when fopen/fread fails (undefined behavior). With LTO, the compiler infers across modules that this path is unreachable and generates abnormal code; with GCC the read only returned a random stack value, so the problem stayed hidden | Fixed (CL 14445927), pending verification on a new image |
| SIGABRT | tvs-daemon, avocd main process, tizen-watcherd | 8 | Considered consequences of the crashes above: assertion failures due to uninitialized AVOC, processes killed while waiting for a lock, aborted synchronous D-Bus calls | Verified together with CL 14445927 |

- Verification plan: put the image of Quickbuild 37531423 (which includes CL 14445927) on the board and confirm that all 30 cores are gone.
- Similar issue: an uninitialized variable (`textList`) was also found in voice-client and fixed (CL 14447603). LTO exposes undefined behavior that was previously latent in the code. We suggest a systematic review of uninitialized-variable warnings (`-Wsometimes-uninitialized`, `-Wuninitialized`) in the Quickbuild logs of the whole image, to remove similar issues in advance.

## 8. Other Findings

| Finding | Impact | Action |
|---|---|---|
| The GCC lane appends compile options (including `-O2`, `-fsigned-char`, `-fstack-protector-strong`) to non-exempt packages; the clang lane lacks this mechanism | In the LLVM image, 1269 packages differ from the GCC image in optimization level, `char` signedness and hardening options | Close the gap in the clang lane (6.3), batch 1 |
| securityscanner's scand/scandtest are non-PIE in the LLVM image. The package's CMakeLists.txt adds `-fPIE -pie` only under GCC | Security hardening regression compared with the GCC image | Extend the condition to clang (CL 14448070) |
| Build scripts of packages such as org.tizen.remote-management hard-code gcc/g++ | The whole package is built by GCC in the LLVM image and does not benefit from the global optimizations of the clang lane | Being changed to use the global toolchain instead of naming gcc/g++ (under verification) |
| klay's spec overrides the global options with `-DCMAKE_CXX_FLAGS` | Loses global options such as `-Os`, `-flto`, `-march` and stack protection | Change to append to the existing options (under verification) |
| dali2-adaptor does not link the library that provides `tizen_policy_interface` and related symbols it uses | No error with GNU ld; the link fails after switching to lld | Add the library in the package |
| The ld.lld in the build root is a 32-bit ARM program running under qemu | lld builds are noticeably slower | Provide an accelerated lld in the build root before switching to lld |
| binutils built with GCC again | None | Intentional, per the rule that the GCC toolchain's own components are built with GCC |
| .ARM.exidx/.ARM.extab about 5 MB larger than with GCC | Image size | To be analyzed |

## 9. Next Steps

1. **Verify the coredump fix**: run the image of Quickbuild 37531423 on the board and confirm that the 30 cores are gone.
2. **Fix clang links that skip LTO**: change the LLVM driver so that link behavior matches GCC; also change klay's spec. Afterwards recount LTO coverage, with the goal of zero files where LLVM is behind GCC. This change is also the precondition for the LTO-stage defaults of batch 2 to apply to every link.
3. **Batch 1 (once the LTO image is stable)**: merge the two product build.conf changes, closing the gap to the forced options and `-fvisibility-inlines-hidden`. After the image is built, run the image-wide export check and the LTO coverage check, measure memory, boot time and performance on the board, and run functional tests with attention to issues the change in `char` signedness may cause.
4. **Baseline for the export check**: build the symbol index of the 20261111.1 image as the baseline for all later batches (Quickbuild artifacts are kept for three days only, so this must be done soon).
5. **ThinLTO by default**: make clang treat `-flto` as ThinLTO by default in the llvm package, and measure the image-wide build time on Quickbuild.
6. **Batch 2**: implement defaults for the inlining threshold and MachineOutliner in the llvm package, compare performance with TPMS on an experimental image, and choose.
7. **Batch 3**: provide an accelerated lld in the build root and fix the dali2-adaptor link error; merge ICF and RELR with the switch to lld.
8. **Separate assessments**: enable the VD warning options for the clang lane in one Quickbuild, count the new errors, then decide on `-Werror`; decide on `-fstack-protector-strong` for the exempt packages according to security requirements.
9. **Follow-up measurements**: rebuild boost, abseil-cpp and icu in the Base build environment to decide on the visibility option for Base; remeasure aurum, org.tizen.mbr-daemon and native-home.
10. **Evaluate MLGO for user-space packages**: compare size and performance with the inlining options of batch 2.
11. **Packages that hard-code gcc/g++**: change them one by one to use the global toolchain, then recount the files not built by clang.
12. **Review uninitialized-variable warnings** to remove in advance issues of the kind LTO can expose.
13. **Unwind tables**: for the packages with the largest increase, compare function counts and unwind entries to find why clang adds 5.1 MB.
14. **Long-term item**: relative vtables (requires an image-wide ABI switch).
