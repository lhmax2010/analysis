# VD LLVM LTO Image (20261111.1): Full Analysis Report (Revised)

Date: 2026-11-12

Revision note: corrects the conclusion of Section 6.3 of the previous version about the optimization levels of individual packages; adds new data on the options forced by the GCC lane, inlining thresholds, lld and RELR; updates the exclusion list of the visibility option and the rollout order in Section 6.10.

## Summary

- The new VD LLVM image includes three changes: full LTO, MLGO (currently used for the Linux kernel only), and non-PIE by default for clang. The whole image is 8.6 MB smaller than the GCC image and 54.7 MB smaller than the previous LLVM image.
- The run-time symbol metadata, the number of dynamic relocations and the number of non-PIE executables are all back to the level of the GCC image. The code (.text) is 39.9 MB smaller than with GCC.
- The larger symbol metadata of the LLVM image reported by HQ was caused by LTO not actually being enabled in the LLVM image, not by `-O2` versus `-Os`. With LTO in place and the optimization level still `-Os`, the issue is largely resolved.
- LTO coverage is now essentially the same as with GCC. Only 21 files (6 MB) are behind GCC. The root cause is known: clang performs LTO only when the link command itself contains `-flto`. The fix has been decided.
- After LTO was introduced, 30 coredumps were observed. The 22 SIGSEGV cases were traced to an uninitialized variable in the code and fixed, pending verification on a new image; the remaining 8 SIGABRT cases are considered consequential failures.
- **Correction to the previous version: the GCC lane appends a set of compile options to the VD-owned packages, and the clang lane lacks this mechanism.**
  - The build environment of the GCC image replaces gcc/g++ with wrapper scripts that append a fixed set of options after the package's own options, including `-O2`, `-fsigned-char`, `-fstack-protector-strong`, `-mcpu=cortex-a53` and a set of VD warning options.
  - Only packages on the exemption lists in build.conf (open source, SR, third party, etc.) are not forced. Of the 2245 source packages of the GCC image, 1269 are forced.
  - The previous statement that "package-defined optimization levels are also used by the GCC lane" therefore does not hold for these 1269 packages: in the GCC lane, their own `-O0`/`-O1` is overridden by `-O2`.
  - clang is not wrapped, so in the LLVM image these packages are built at their own level (org.tizen.AVControl at `-O0`, for example) and without `-fsigned-char`. The latter makes the signedness of `char` differ from the GCC image, which is a difference in program behavior.
  - The way to close the gap has been decided and verified locally (Section 6.3): through a hook that already exists in the product rpm macros, the clang form of the same option set is appended to every clang call of the same packages. In the sample packages, the part loaded at run time shrinks by 25.9% and the code by 36.2%.
- The option candidates were measured by local rebuilds under conditions identical to Quickbuild: 22 sample packages, 151 builds. The .text of the unchanged local rebuild matches the same files in the image, so the measurement conditions are reliable. Conclusions (Section 6):
  - **Batch 1, product build.conf only, verified locally in its final form:**
    - close the gap to the options forced by the GCC lane (6.3);
    - `-fvisibility-inlines-hidden`, on by default, with openusd, tvs-si and aurum excluded (6.2). libgrpc's dynamic symbol tables shrink by 49% and its part loaded at run time by 20%.
  - **ThinLTO as the default LTO mode**: size essentially the same as full LTO, much shorter build time; can go in at the same time as batch 1.
  - **Batch 2, performance assessment needed: inlining policy and MachineOutliner.** For the exempt packages, the GCC lane uses `-fno-inline-functions` and the clang lane has no equivalent limit.
    - A lower inlining threshold: threshold 25 reduces the part loaded at run time of the affected samples by 23.3%, threshold 50 by 14.3%;
    - MachineOutliner: by 8.1%.

    Both are to be implemented as defaults in the llvm package and confirmed with TPMS.
  - **Batch 3, with the switch to lld:** lld + ICF is 2.3% smaller than GNU ld. RELR saves 18.8 MB of file size; the earlier concern about a conflict with prelink is gone with the decision to keep PIE and drop prelink.
  - **Assessed separately:**
    - whether to add the VD warning options and `-Werror` to the clang lane (a build quality gate that does not change the output);
    - `-fstack-protector-strong` for the exempt packages (aligning with the global options of the GCC lane, about +2%).
  - **Not recommended**: the gc-sections group; clang's `-fno-inline-functions`.
- Packages whose build scripts hard-code gcc/g++ (e.g. org.tizen.remote-management) are being changed to use the global toolchain.

## 1. Scope

| Item | Image / repository | Notes |
|---|---|---|
| New LLVM image | TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261111.1 (Quickbuild 37518055, b341) | LTO + MLGO (Linux kernel only) + non-PIE by default for clang |
| New LLVM Base | tizen-10.0-base-dev-llvm-standard_20261105.1 | tizen_macros calls `%lto_build` again from `%__spec_build_pre` |
| Previous LLVM image | TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261103.1 (Base 20261029.1) | LTO not enabled |
| GCC image | TIZEN-ONEMAIN-KantSU2e-RELEASE_20261001.3 | Full LTO, `-O2` |

- Comparison scope: the 4778 ELF files of the HQ file list that exist in all three images.
- Data sources: RPMs downloaded directly from each image repository and parsed file by file; the Quickbuild build logs and the original build.conf were also checked.
- build.conf: the build.conf of the new image's product project is identical to TIZEN_KantSU2E_Clang_build.conf #11 in P4. The clang lane uses `-Os -fstack-protector ...`; the GCC lane uses `-O2 -fno-inline-functions -fstack-protector-strong ...`.

## 2. Changes Already Merged

| Change | Location | Effect |
|---|---|---|
| Full LTO | tizen_macros of the LLVM Base: `%__spec_build_pre` calls `%lto_build`, using the three LTO package lists of build.conf | Same LTO scope as the GCC image (Section 4) |
| MLGO | LLVM toolchain | Currently enabled for the Linux kernel only; user-space packages do not use it. In a local control experiment, turning off ML inlining left the output of every sample package byte-identical to the unchanged configuration, consistent with this |
| Non-PIE by default for clang | llvm package of the LLVM Base | Non-PIE executables back from 14 to 155 (GCC: 153). Note: on 2026-11-12 it was decided, for security, to keep PIE and drop prelink, also in the GCC image; later images will be adjusted accordingly |
| build-id | LLVM toolchain | 4776 files carry a build-id, same as GCC |

## 3. Size and Memory-Related Data

### 3.1 Overall comparison (4778 files)

| Metric | GCC | Previous LLVM | New LLVM | New LLVM − GCC |
|---|---|---|---|---|
| Total file size | 1647.38 MB | 1693.41 MB | **1638.76 MB** | **−8.62 MB** |
| .text | 689.84 MB | 649.28 MB | 649.91 MB | −39.93 MB |
| .rodata | 203.61 MB | 201.99 MB | 201.90 MB | −1.71 MB |
| Run-time symbol metadata (.dynsym/.dynstr/.gnu.hash/.hash/.gnu.version) | 115.18 MB | 152.22 MB | 119.86 MB | +4.68 MB |
| Dynamic relocations (.rel.dyn + .rel.plt) | 3,948,470 | 4,223,663 | **3,946,190** | −2,280 |
| .got | 3.74 MB | 4.16 MB | 3.62 MB | −0.13 MB |
| .data.rel.ro | 18.63 MB | 19.69 MB | 19.07 MB | +0.44 MB |
| Weak exports (defined WEAK in .dynsym) | 179,255 | 525,206 | 281,743 | +102,488 |
| Non-PIE executables | 153 | 14 | 155 | +2 |
| .symtab + .strtab (not loaded; stripped in release images) | 424.43 MB | 462.65 MB | 446.86 MB | +22.42 MB |

Key points:

1. **Metrics related to run-time memory are on par with GCC.** Dynamic relocations determine the private pages written at process start-up; they, together with .got and the number of non-PIE executables, are back to the GCC level. Run-time symbol metadata is still 4.68 MB larger than with GCC, mostly in files that are not built with LTO on either side (Section 3.2).
2. **Code is about 40 MB smaller than with GCC.** This is the main reason the new image is smaller than the GCC image.
3. **The 22.4 MB increase in .symtab/.strtab is mainly ARM mapping symbols (`$a`/`$t`/`$d`).** These are not loaded into memory and are stripped from release images, so they do not affect release image size or memory.
4. **Unwind tables are larger than with GCC**: .ARM.exidx +1.44 MB, .ARM.extab +3.66 MB. This is listed for follow-up analysis.

### 3.2 Breakdown by LTO state of the files in the new image (new LLVM − GCC)

| Section | LTO (2621 files) | No LTO (1475 files) | No .symtab (185 files) | Not built by clang (497 files) |
|---|---|---|---|---|
| .text | −14.60 MB | −22.30 MB | −2.97 MB | −0.05 MB |
| .dynstr | +0.80 MB | +3.26 MB | +0.70 MB | +0.06 MB |
| .dynsym | +0.10 MB | +0.20 MB | +0.04 MB | +0.01 MB |
| .symtab | +15.15 MB | +1.98 MB | 0.00 MB | +0.06 MB |
| File size | −0.34 MB | −8.61 MB | −2.35 MB | +2.68 MB |

For files built with LTO, file size and .dynstr are essentially the same as with GCC. The remaining symbol metadata gap comes mostly from files that are not built with LTO on either side; these are the main target of `-fvisibility-inlines-hidden` in Section 6.

## 4. LTO Coverage

Method: a file built with LTO no longer keeps project source file names in .symtab (only toolchain files such as crti.o and crtstuff.c remain); a file built without LTO still keeps them. The method was checked against four known samples and gives correct results on both the LLVM and the GCC side.

| New LLVM \ GCC | GCC with LTO | GCC without LTO |
|---|---|---|
| New LLVM with LTO | 2619 files, 470.32 MB | 2 files, 0.61 MB |
| New LLVM without LTO | **21 files, 5.96 MB** | 1454 files, 402.98 MB |

1. **LTO coverage is essentially the same as with GCC.** The 1454 files without LTO on both sides belong to packages excluded by the same rules, such as the LTO exclusion lists of build.conf; they are not an LLVM gap.
2. **The 21 files (13 packages) where LLVM is behind GCC** have a known root cause: these packages are compiled with `-flto`, but the final link command does not contain `-flto`.
   - The GCC driver always loads the LTO plugin at link time, so these packages still get LTO.
   - clang loads LLVMgold only when the link command contains `-flto`. Because `-ffat-lto-objects` is used globally, the object files also contain regular machine code, so the link does not fail; it silently falls back to a regular link.

   Affected packages: wpasupplicant, gst-ffmpeg-atsc3, libfreetype, libdbuspolicy, libdbuspolicy-serializer, sys-tools, klay, libtbb, ext4-utils, soc-cpu-heavyload-ewtest, libai-classifier-impl, soc-ai-classifier, nsjail. klay is a different case: `-DCMAKE_CXX_FLAGS` in its spec overrides the global compile options, so `-flto` is already missing at compile time.
3. **Fix**: make the LLVM driver behave like GCC, i.e. load LLVMgold at link time unless `-fno-lto` is given. Reasons:
   - several of the packages above use link commands that carry neither CFLAGS nor LDFLAGS, so a macro change alone cannot cover them;
   - a driver change makes the clang lane behave exactly like GCC for LTO, without per-package changes.

   klay needs a separate spec change so that options are appended to the existing CXXFLAGS.
4. **497 files (about 708 MB) are not built by clang**, so LLVM-side optimizations cannot apply to them. They mainly include:
   - chromium-efl (217 MB, built by GCC and linked by LLD), vd_memps (210 MB), tts-engine-vd (83 MB, prebuilt), bluetooth-impl-sec-oal (39 MB), GPU drivers, and Rust runtime libraries;
   - components kept on GCC by rule (glibc, libstdc++, binutils);
   - packages whose build scripts hard-code gcc/g++, such as org.tizen.remote-management. These are being fixed one by one: the hard-coded compiler is removed and the global toolchain (the system compiler specified by build.conf) is used instead, so that these packages also benefit from LTO and the other global optimizations of the clang lane.
5. **Note**: clang's LTO output leaves no source file names in .symtab. A package that strips its local symbols also shows no source file names, so the 2619 "LTO" files are an upper bound. The 21 files where LLVM is behind GCC were identified from the source file names that remain, so that conclusion is not affected.

## 5. Response to the HQ Analysis

The HQ analysis states that the increase in weak exports is the main reason for the larger .dynstr/.dynsym of the LLVM image. This matches our data. We see the cause differently, however.

1. **The root cause was that LTO was not enabled, not `-O2` versus `-Os`.** The clang optimization level of the new image is still `-Os`; only LTO was added. Results:
   - weak exports dropped from 525,206 to 281,743 (GCC: 179,255);
   - run-time symbol metadata went from 37.0 MB larger than GCC to only 4.7 MB larger;
   - the space taken by std:: symbol names dropped from 40.59 MB to 21.82 MB (GCC: 19.17 MB).
2. **rmdemon, the first sample in the HQ report (MaintModeApp likewise), is built by GCC in the LLVM image.** The CMakeLists.txt of its package hard-codes `SET(CMAKE_C_COMPILER gcc)` / `SET(CMAKE_CXX_COMPILER g++)`. For this sample, weak exports went from 17,798 to 1 (same as the GCC image): the compiler is GCC in both cases and the optimization options did not change; the only difference is that LTO now takes effect. This shows the difference is unrelated to both clang and `-Os`.
3. **For samples built by clang, .dynstr is now close to GCC once LTO is applied:**

   | File | GCC | Previous LLVM (no LTO) | New LLVM (LTO, `-Os`) |
   |---|---|---|---|
   | liblcc-player-tv.so | 0 / 1.01 MB | 11,996 / 2.03 MB | 2,454 / 1.06 MB |
   | libusd_usd.so | 0 / 0.93 MB | 9,231 / 1.67 MB | 4,725 / 0.97 MB |
   | libusd_sdf.so | 0 / 0.77 MB | 7,293 / 1.32 MB | 3,901 / 0.78 MB |

   Each cell shows the number of weak exports and the .dynstr size.
4. **Therefore, the clang lane does not need to switch to `-O2` to solve this issue.** The remaining weak exports can be further reduced with `-fvisibility-inlines-hidden` (Section 6).
5. **The increase in .symtab/.strtab is unrelated to the mechanism above.** In the new image it is mainly ARM mapping symbols, and it is stripped from release images.

## 6. Option-Level Optimization

Options are evaluated under one constraint: memory must not increase and performance must not drop noticeably. Each candidate below comes with data from three sources:

- static statistics of all 4780 ELF files of the new image;
- file-by-file comparison of the new image with the GCC image;
- local rebuild measurements: 22 sample packages rebuilt in a number of configurations, in a local environment identical to Quickbuild 37518055 (method and conditions in 6.8).

"Part loaded at run time" means the sum of the sections loaded into memory when the program runs, an approximation of memory use; sections that are not loaded, such as .symtab, are not counted.

### 6.1 Overview

| Option | Key data | Conclusion |
|---|---|---|
| Closing the gap to the options forced by the GCC lane (for the 1269 non-exempt packages, the clang form of the same option set appended to every clang call) | 4 sample packages: part loaded at run time −25.9%, .text −36.2%; org.tizen.AVControl .text from 720 KB to 173 KB (GCC: 245 KB); also adds `-fsigned-char` and the stack protection hardening | **Batch 1**: product build.conf only, verified locally in its final form; `-fsigned-char` changes the behavior of the current LLVM image, so functional testing is required |
| `-fvisibility-inlines-hidden` (C++) | Static upper bound 145,220 exports, about 21.5 MB; measured in packages where it took effect and no exclusion is needed: dynamic symbol tables −44%, part loaded at run time −11% | **Batch 1**: on by default, 3 packages excluded, verified locally in its final form |
| ThinLTO as the default LTO mode | Compared with full LTO: part loaded at run time +0.5%, .text −0.1%; earlier separate measurement: build time only 2% above no LTO (full LTO: +64%) | **Recommended**; can go in with batch 1 (llvm package change) |
| Lower inlining threshold (the counterpart of the global `-fno-inline-functions` of the GCC lane) | Threshold 25: part loaded at run time −23.3%, .text −36.1% in the affected samples; threshold 50: −14.3%, .text −22.2% | **Batch 2**: implemented as a default in the llvm package; chosen after TPMS confirms performance |
| MachineOutliner | In the 2 packages where it took effect: .text −16.5%, part loaded at run time −8.1% | **Batch 2**, as above |
| lld + `--icf=safe` | Compared with GNU ld: part loaded at run time −2.3%, .text −3.5% | **Batch 3**: with the switch to lld; an accelerated lld and a fix for the dali2-adaptor link error are needed first |
| RELR relocation packing | 2.56 million relative relocations (19.54 MB) would need only 0.71 MB with RELR; 18.8 MB of file size saved | **Batch 3**: GNU ld does not support RELR on 32-bit ARM, so only with lld; prelink is being dropped, so the earlier conflict concern is gone |
| VD warning options and `-Werror` | Forced on the non-exempt packages by the GCC lane; do not change the output | **Assessed separately**: first count the new errors under clang |
| `-fstack-protector-strong` for the exempt packages | Cost: part loaded at run time +2.1%, .text +4.2% | **Assessed separately**: aligns with the global options of the GCC lane; decision depends on security requirements |
| `-ffunction-sections -fdata-sections` + `--gc-sections` | No gain on openusd (8,910 KB → 8,978 KB); executables that could benefit hold only 19% of .text | **Not recommended** |
| Relative vtables | 989,000 relocations come from vtables, 25% of all dynamic relocations | **Not adopted for now**: image-wide ABI switch required; long-term item |
| Unwind tables | 5.10 MB larger than with GCC, all in files built by clang | Find the cause first; no option change |

### 6.2 `-fvisibility-inlines-hidden`

#### Data (all 4780 ELF files of the new image)

| Item | Result |
|---|---|
| Exports that can become hidden (upper bound) | 145,220 entries in 858 ELF files built by clang, about 21.5 MB (.dynsym + .dynstr of the whole image: about 106 MB) |
| References that would lose their exporter (worst case) | 673 symbol names referenced by 72 ELF files, provided by 13 packages |
| Gain kept after excluding these 13 packages | about 16.8 MB (78% of the upper bound) |

Packages with the largest gain: libgrpc (3.62 MB), openusd (2.18 MB), soc-ai-acl (1.57 MB), org.tizen.mbr-daemon (1.55 MB), native-home (0.96 MB).

The 13 provider packages that may be affected: openusd, soc-ai-acl, boost-serialization, abseil-cpp, libicu, pkgmgr-info, tee_test_suite, trustzone-nwd, protobuf, libwebauthn-common, aurum, security-manager, tvs-si.

#### Risks

- **Static local variables (singleton pattern)**: on Linux, this clang option does not change the visibility of static local variables in inline functions, which matches GCC. There is no risk of each library getting its own copy of a singleton.
- **Explicit instantiation**: a local armv7 sample confirms that when a template has an explicit instantiation definition, its inline members are still exported with this option. Most of the 673 symbol names above are of this template kind (boost::archive, abseil, protobuf, openusd's VtArray/TfSingleton, etc.), and in the measurements most packages indeed still export them. openusd's VtArray is an exception (see the measurements below), so the code pattern alone is not enough; each package must be measured.
- **The real risk**: non-template member functions that are referenced by other libraries but implemented inline in the provider, e.g. `TCPSIManager::t_IsFilteringSectionSupported` in tvs-si.
- **Comparing addresses of inline functions across libraries**: not visible in symbol tables; on-board testing is needed as a safeguard.

#### Local rebuild measurements

The 13 provider packages that may be affected, as well as packages with a large expected gain such as libgrpc, were rebuilt with the unchanged configuration and with the option. For libgrpc and protobuf, the option was added to the global clang compile options of build.conf (optflags), the same way it would be rolled out; these two packages use optflags directly and do not read the compile options from the environment. For every symbol referenced by another file, we checked whether the provider still exports it with the option enabled:

| Provider package | Symbol names referenced by other files | Still exported with the option | Gone with the option | Conclusion |
|---|---|---|---|---|
| openusd | 373 | 325 | **48** | **Exclude** |
| tvs-si | 1 | 0 | **1** | **Exclude** |
| libgrpc | 0 | — | 0 | No exclusion needed (no other package relies on its exports alone) |
| pkgmgr-info | 13 | 13 | 0 | No exclusion needed |
| tee_test_suite | 18 | 18 | 0 | No exclusion needed |
| trustzone-nwd | 8 | 8 | 0 | No exclusion needed |
| libwebauthn-common | 3 | 3 | 0 | No exclusion needed |
| security-manager | 1 | 1 | 0 | No exclusion needed |
| protobuf | 3 | 3 | 0 | No exclusion needed: the option reached all 436 compile commands and the output is byte-identical to the unchanged build, so the option has no effect on it |
| soc-ai-acl | — | — | — | No exclusion needed: the package uses its own build system and its own compile options, so the global options of build.conf never reach its compilation |
| boost-serialization, abseil-cpp, libicu, aurum | — | — | — | Local build failed; not decidable in this round (the first three are Base packages and must be rebuilt in the Base build environment) |

- **openusd**: the 48 symbols that disappear are all members of `VtArray<T>` (`_AllocateNew`, `_DetachIfNotUnique`, the destructor, `operator==`), referenced by other openusd libraries and by dali2-usd-loader. openusd declares the common VtArray instances as external instances (extern template) in its headers, so users do not generate these functions themselves and rely on the provider's exports. With the option, the provider no longer exports them, and the symbols cannot be found at run time. Shared library links allow undefined symbols, so the successful openusd rebuild does not prove it is safe; it must be excluded.
- **tvs-si**: the symbol that disappears is exactly `TCPSIManager::t_IsFilteringSectionSupported`, flagged earlier by the static analysis and referenced by tvs-dvbbase-si and tvs-isdb-si. It must be excluded.
- **The other decided packages**: all symbols flagged as possibly affected by the static analysis are still exported with the option, consistent with the finding that members of explicitly instantiated templates remain exported. No exclusion is needed.
- **The static estimate is conservative**: for the 9 decided packages, the static analysis listed 420 possibly affected symbol names; only 49 actually disappear, in 2 packages.
- **Existing use**: dali2-adaptor already uses `-fvisibility-inlines-hidden` in its own spec.

Measured gain per package (unchanged → with the option):

| Package | Exported symbols | Dynamic symbol tables | Part loaded at run time | File size |
|---|---|---|---|---|
| libgrpc | 46,117 → 28,628 (−37.9%) | 6,277 → 3,190 KB (−49.2%) | −20.3% | −12.9% |
| openusd (to be excluded) | 25,910 → 18,007 (−30.5%) | 4,232 → 2,517 KB (−40.5%) | −10.8% | −7.1% |
| trustzone-nwd | 3,043 → 1,903 (−37.5%) | 389 → 237 KB (−39.2%) | −13.0% | −8.3% |
| tvs-si (to be excluded) | 1,741 → 1,129 (−35.2%) | 193 → 132 KB (−31.9%) | −13.1% | −9.4% |
| security-manager | 2,236 → 1,531 (−31.5%) | 333 → 252 KB (−24.4%) | −6.0% | −4.0% |
| tee_test_suite | 3,168 → 2,533 (−20.0%) | 459 → 392 KB (−14.8%) | −0.6% | −0.4% |
| pkgmgr-info | 1,830 → 1,824 (−0.3%) | 205 → 204 KB | −0.1% | −0.1% |
| libwebauthn-common | 402 → 400 (−0.5%) | 48 → 48 KB | −0.1% | 0.0% |

- .text is essentially unchanged in every package: the option changes exports only, not code.
- The 6 packages where the option took effect and no exclusion is needed, in total: dynamic symbol tables 7,711 → 4,323 KB (−43.9%), part loaded at run time 32,683 → 28,964 KB (−11.4%, about 3.6 MB).
- Measured versus static estimate: libgrpc's dynamic symbol tables shrank by 3.01 MB against an estimate of 3.62 MB; openusd by 1.67 MB against 2.18 MB. The measured gain is about 80% of the estimate, which supports the order of magnitude of the 21.5 MB static upper bound.
- org.tizen.mbr-daemon and native-home failed to build locally; their real gain remains to be measured.

#### Conclusion and approach

- **Feasible; part of batch 1.** Enable it by default with an exclusion list:
  - the option is appended to the global clang optimization options of build.conf (`%__optflags_toolchain_clang`);
  - a Lua macro decides from the package name whether it is on the exclusion list. The list has the same form as the existing LTO lists and is matched against the Name of the spec.
- **Exclusion list (3 packages):**
  - confirmed by measurement: openusd, tvs-si;
  - cannot be built locally, not decidable, excluded as a precaution: aurum.

  boost-serialization, abseil-cpp and libicu, listed in the previous version, are Base packages built in the Base project; changes to the product build.conf do not apply to them, so they are not on the product exclusion list. Whether to enable the option on the Base side will be decided after verification in the Base build environment.
- **Local verification of the final form:**
  - openusd and tvs-si, which are on the list, produce output byte-identical to the unchanged configuration;
  - libgrpc gets the option, with results identical to the measurement with the option added directly to optflags;
  - the pure C package libfreetype builds normally with unchanged output.
- **Verification after the image is built:**
  1. image-wide export check: every symbol referenced by another file is still exported by some file of the new image (the check script is ready, with the 20261111.1 image as the baseline);
  2. measure boot time and memory on the board and compare performance;
  3. cases such as comparing addresses of inline functions across libraries are not visible in symbol tables; on-board testing is the safeguard.
- This option goes beyond the GCC configuration (the GCC image does not use it). It will go into the image after the LTO-related coredumps have converged.

An earlier measurement (11-03 conditions, openusd rebuilt in a local build environment):

| File | Without the option | With the option | Change |
|---|---|---|---|
| libusd_usd.so (no LTO) | 8,908,820 B | 7,720,268 B | −13.3% |
| libusd_usd.so (ThinLTO) | 7,629,144 B | 7,035,884 B | −7.8% |
| libusd_sdf.so (ThinLTO) | 6,022,104 B | 5,529,348 B | −8.2% |

On top of ThinLTO, weak exports of libusd_usd.so went from 4,725 to 2,226, and .dynstr was halved (1,021,964 B → 504,607 B).

### 6.3 Per-package handling of packages whose clang code is larger than with GCC

#### Data (1654 packages built by clang and present on both sides, compared by .text)

- 1388 packages have smaller .text than with GCC, 55.95 MB less in total; 266 packages are larger, 16.08 MB more in total.
- The top 10 packages larger than with GCC account for 10.8 MB:

| Package | GCC .text | New LLVM .text | Difference | Ratio | Options forced by the GCC lane |
|---|---|---|---|---|---|
| org.tizen.webappservice | 2.74 MB | 6.38 MB | +3.64 MB | 2.33 | Yes |
| qte-bm | 6.20 MB | 8.90 MB | +2.70 MB | 1.43 | No (open-source exemption) |
| openusd | 7.94 MB | 8.76 MB | +0.82 MB | 1.10 | No (SR exemption) |
| soc-ai-acl | 2.83 MB | 3.51 MB | +0.67 MB | 1.24 | No (open-source exemption) |
| avoc-daemon | 0.63 MB | 1.22 MB | +0.59 MB | 1.93 | No (open-source exemption) |
| app-installers | 0.71 MB | 1.26 MB | +0.56 MB | 1.78 | No (SR exemption) |
| org.tizen.tv-viewer | 3.98 MB | 4.52 MB | +0.54 MB | 1.13 | Yes |
| org.tizen.AVControl | 0.24 MB | 0.70 MB | +0.46 MB | 2.94 | Yes |
| dali2-adaptor | 1.35 MB | 1.78 MB | +0.43 MB | 1.32 | No (SR exemption) |
| libpisa-ipc | 0.47 MB | 0.86 MB | +0.39 MB | 1.84 | Yes |

- This matches HQ's memory data: in the HQ research summary, clang `-Os` code is 2.5% larger overall by per-process PSS, and avocd nearly doubles; in the table above, avoc-daemon's .text is exactly 1.93 times GCC's.

#### Correction: the GCC lane appends compile options to non-exempt packages

The previous version stated that the optimization levels these packages set for themselves are also used by the GCC lane, so the two lanes are consistent. A check of the GCC build environment shows that this does not hold for the VD-owned packages.

- **The GCC lane mechanism:**
  - The build environment of the GCC image preinstalls gcc-warning-build-env, which replaces gcc, g++, cc and c++ with wrapper scripts that append a fixed set of options (macro `%gcc_warning_force_options`, 37 options) after all of the package's own options.
  - Before each package is built, the rpm macro `%gcc_warning_incompatible` checks the exemption lists (the open-source, SR, third-party and kernel lists in build.conf). Packages on the lists get the original compiler back and are not forced.
- **What is appended:**
  - optimization and debug: `-O2 -g2`;
  - hardening: `-fstack-protector-strong --param=ssp-buffer-size=4 -Wp,-D_FORTIFY_SOURCE=2`;
  - target: `-mcpu=cortex-a53` and other target options;
  - `-fno-common -fsigned-char`;
  - link: `-Wl,-z,relro,--as-needed -Wl,-O1 -Wl,--hash-style=gnu`;
  - a set of VD warning options, and `-Werror`.
- **Evidence:**
  - In the compile options recorded in the debug information of the GCC image, org.tizen.tv-viewer shows `-O1 -O2` and org.tizen.webappservice shows `-O2 -O2 -O -O0 -O -O2`. GCC records them in command-line order and the last one takes effect, so the packages' own `-O1` and `-O` are overridden by the `-O2` appended at the end.
  - The spec of org.tizen.AVControl provides no optimization level at all, yet the options recorded by GCC include `-O2 ... -fno-common -fsigned-char`.
  - org.tizen.AVControl and org.tizen.tv-viewer were rebuilt locally with the build.conf and repositories of the GCC image. The compile commands printed by make contain neither `-O2` nor `-fsigned-char`, but the options GCC actually recorded contain both. The g++ in the build environment is the wrapper script described above.
  - openusd is on an exemption list; GCC records `-O2 -O3`, and the package's own `-O3` takes effect.
- **Scale:** of the 2245 source packages of the GCC image, 976 are on an exemption list and 1269 are forced.
- **The gap in the clang lane:**
  - The LLVM product uses the same exemption lists and the same rpm macros, but clang is not wrapped, so these 1269 packages do not get the option set.
  - Optimization level: the package's own level takes effect. org.tizen.AVControl is built at `-O0`, org.tizen.tv-viewer at `-O1`, org.tizen.webappservice at `-O`.
  - Signedness of `char`: unsigned by default on ARM. In packages that do not use the VD flag macros themselves, `char` has a different signedness than in the GCC image, and code that depends on whether a `char` is negative behaves differently.
  - Hardening: packages that replace the global CFLAGS also lose stack protection and FORTIFY.

#### Closing the gap, and verification

- **Approach.** In `%__spec_build_pre`, right after the GCC exemption check, the rpm macros of the LLVM product expand `%{?clang_force_incompatible}`; this hook was never defined. It is now defined in build.conf:
  - exempt packages get nothing;
  - all other packages export clang's own `CCC_OVERRIDE_OPTIONS`, which appends the options at the end of every clang call.

  The exemption lists are the GCC ones.
- **Clang form of the option set:**
  - the options of the GCC set that affect the generated code, the ABI or the link are kept;
  - warning options and `-Werror` are left out, since they do not change the output;
  - the set ends with the existing clang adaptation of build.conf (`%__vd_flags_toolchain_clang`), which turns `-O2` into `-Os` exactly as for the VD flag macros.
- **Why the GCC wrapper script is not reused:** it renames the compiler and calls it through the resolved real path, while clang decides the C++ mode and the target from the name it is invoked with, so wrapping it that way breaks it.
- **Local measurements** (.text, KB):

| Package | Unchanged | Gap closed | GCC image |
|---|---|---|---|
| org.tizen.AVControl | 720 | 173 | 245 |
| org.tizen.tv-viewer | 4,630 | 2,362 | 4,080 |
| libpisa-ipc | 877 | 399 | 478 |
| org.tizen.webappservice | 6,534 | 5,210 | 2,808 |

  - The four packages together: part loaded at run time 17,540 → 12,992 KB (−25.9%), .text −36.2%.
  - Checked in the debug information: every clang compile unit of these packages ends at `-Os` and carries `-fsigned-char`.
  - Rebuilt with the final build.conf as is:
    - the forced packages are identical to the trial results;
    - the exempt openusd and grpc are unaffected;
    - the build logs of the forced packages contain the export, those of the exempt packages do not;
    - tvs-si, which uses `-Werror` itself, builds normally. tvs-si is already built at `-Os`; with the gap closed, its part loaded at run time grows from 531 to 540 KB (+1.6%), in line with the cost of the hardening options.
  - In one trial the warning options were appended as well, and tvs-si failed to compile because of its own `-Werror`: clang's `-Wcast-function-type` judges differently from GCC. This also shows that the warning options must be assessed separately and not be carried along with this item.
- **Risks:**
  - **`-fsigned-char` changes the behavior of the current LLVM image.** It returns to the behavior of the GCC image, the one the product has long been validated with, but for the current LLVM image it is a change, so it must go into an image together with functional testing.
  - **Cases this approach does not cover** (the GCC wrapper covers them):
    - code compiled only in the `%install` stage;
    - build systems that clear the environment;
    - `-nostdlib` links. The GCC wrapper skips such links; the kernel-related packages are on the exemption list anyway.

    The first two are found by the checks after the image is built and fixed package by package.

#### Exempt packages: inlining policy

Exempt packages use their own or the global options in both lanes. The remaining difference is in the global options: the GCC lane has `-fno-inline-functions`, and the clang lane has no equivalent inlining limit.
