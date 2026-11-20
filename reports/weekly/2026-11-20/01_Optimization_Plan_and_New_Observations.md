# Optimization Plan and New Observations — Size, Memory, Performance

Nov 20, 2026 · @Hao

This week found two new optimization levers in the LLVM image: a Clang Thumb-2 default (609 ARM-predominant files) and strict text-relocation linking. The earlier option-optimization research (forced options, inline visibility, ThinLTO, inlining threshold, MachineOutliner, lld/ICF, RELR) is scheduled next to them, one change per experiment.

## 1. New observations this week

| Observation | Data | What it means for optimization |
| --- | --- | --- |
| Clang default ISA on armv7l is A32 | `armv7l-tizen-linux-gnueabi-clang -c` without `-mthumb` gives triple `armv7-tizen-linux-gnueabi` and `$a` code. With platform optflags it gives `thumbv8a` and `$t`. `clang.cfg` contains only `-target`, `-resource-dir`, `-D_FILE_OFFSET_BITS=64`. | Any package whose build drops `$CFLAGS` ships A32 code under Clang. A32 is larger than Thumb-2 for the same code. |
| GCC Product builds were always Thumb-2 and `-O2` | Product build.conf preinstalls `gcc-warning-build-env-14.2.0-4.1`. Its wrapper appends `-mthumb -O2 -g2 -fstack-protector-strong -fsigned-char -Wshadow -Werror …` after the package flags, except for `__KERNEL__` / `-nostdlib` compiles and exempt packages. Base (OBS) builds have no wrapper. | Explains why A32 code appears only in the LLVM image. GCC baselines were effectively `-O2` with Thumb-2 forced; the LLVM optflags are `-Os`. |
| 609 ARM-predominant loadable ELF files | Scan of all 2,342 RPMs of the LTO and PIE image: 445 files carry GCC + Clang markers, 157 GCC only, 4 GCC + Rust, 3 none. Estimated A32 code: 359.7 MB. | The largest code-size lever found so far. A ready fix vehicle exists in Base: `clang-force-options`. |
| LTO pays off on previously excluded packages | Same source revision, LTO excluded vs LTO on: org.tizen.tv.swu −11.3%, liballshare-core −9.9%, nagsam-mw −1.6%, ug-hbbtv-efl −0.3% `.text` (−1,379,302 B, −7.2% together). | build.conf@14452507 removes them from `%lto_uncompatible_pkgs`. The 80 other no-LTO packages are the next candidates. |
| Silent TEXTREL on the native link path | Tizen GNU ld 2.43 links a non-PIC `R_ARM_ABS32` in `.text` into a DSO and a PIE with `DT_TEXTREL`, exit 0. `-z text` rejects it. Production configs set no `-z text`. | TEXTREL pages become private dirty memory at load time, which costs RAM on a 1 GB target. |
| Kernel MLGO models trade inlining for size | Customized models keep 2,421 more functions out of line, yet vmlinux `.text` is −2.90%. | A size-oriented kernel model is a memory lever; matched board A/B decides adoption. |

## 2. Optimization methods

Each method is one experiment on the same control image. It is measured for static size, PSS / private-dirty memory, boot time and 4K playback on KantSU2E. The 1 GB 4K check runs on KantSU2E limited to 1 GB of RAM, and that is a checkpoint, not the end point. Accepted candidates are then combined and re-checked together.

### 2.1 New levers from this week

| # | Method | Target | Evidence | Gate |
| --- | --- | --- | --- | --- |
| N1 | **EXP-T1, Clang Thumb-2 default.** build.conf preinstalls `clang-force-options` with `%clang_force_options -mthumb`. Kernel and external-module packages are exempt; an explicit package `-marm` still wins. | Size, memory | Mechanism verified in GBS; 609-file target list | ARM-predominant count, `.text`, build failures, boot, playback, PSS of top media processes |
| N2 | **Strict text relocations:** `-Wl,-z,text` in the armv7l LLVM build.conf, plus producer `-fPIC` for shared and PIE inputs | Memory, stability | Linker fixture proven | Baseline TEXTREL scan, then package trial |
| N3 | **MLGO kernel models** (customized vs official) | Size, performance | Kernel `.text` −2.90% | Matched board A/B: boot ×5, kernel microbenchmarks ×5, 4K playback ×3 |
| N4 | **LTO coverage:** enable LTO for the 80 packages that GCC also built without LTO | Size | 4 packages: −0.3% to −11.3% `.text` | Per-package rebuild with LTO; exported API and ABI identical to the GCC build (.dynsym, SONAME, symbol versions, abidiff); consumers load; smoke test and 24 h soak with no new cores; then remove from the exclusion list |
| N5 | **Optimization level:** move the 34 packages below `-O2` (`-O0`, `-O1`, `-Og`) to `-Os` | Size, performance | 4 packages: `.text` −20% to −76% | Owner check for `-Og` / `-O0`, then rebuild and measure |

### 2.2 Earlier option-optimization research (11 Nov analysis)

The 11 Nov analysis tested seven option changes on 22 sample packages (151 builds, 126 succeeded). These results are sample results, not projected savings for the current image. Each is re-run on the current control image as its own experiment.

| # | Option change | Sample result | Risk / condition | Re-run plan |
| --- | --- | --- | --- | --- |
| R1 | **Close the gap to the GCC forced options:** the `%clang_force_incompatible` hook appends the Clang form of the GCC option set (`-Os`, hardening, `-fsigned-char`, target options; no warnings or `-Werror`) to the 1,269 non-exempt packages | 4 packages: loaded sections 17,540 → 12,992 KB (−25.9%), `.text` −36.2%. org.tizen.AVControl 720 → 173 KB | `-fsigned-char` changes `char` signedness back to the GCC behavior: needs functional testing | Rebuild with `clang-force-options` carrying the option set; combine with EXP-T1 only after both pass alone |
| R2 | **`-fvisibility-inlines-hidden`** (inline visibility) | 6 packages: dynamic metadata −43.9%, loaded sections −11.4%; libgrpc metadata −49.2% | Exported inline symbols; exclusions openusd, tvs-si, aurum | Image-wide export / consumer audit, then rebuild |
| R3 | **ThinLTO** instead of full LTO | 4 packages: loaded sections +0.5%, `.text` −0.1%; build time 393 s → 245 s on two libraries | Mainly a build-time gain | Dedicated build-time measurement; size must not regress |
| R4 | **Inlining threshold** | Threshold 50: loaded sections −14.3%; threshold 25: −23.3% | Hot paths can slow down | Per-threshold experiment with performance check |
| R5 | **MachineOutliner** | 2 packages: `.text` −16.5%, loaded sections −8.1%, unwind tables +21.6% | Call overhead on hot paths; unwind growth | Size plus hot-path performance and stack-trace check |
| R6 | **lld + safe ICF** | lld alone about equal; lld + ICF loaded sections −2.3% | Host lld acceleration and dali2-adaptor link dependency | Linker change and ICF measured separately |
| R7 | **RELR** relocation packing | Estimated 18.83 MB file saving | Loader support; largest providers are GCC-built or prebuilt | Loader and packaging compatibility test first |

### 2.3 Memory focus for the 1 GB goal

Static size is ranked against measured memory. During 4K playback on KantSU2E limited to 1 GB, PSS and private-dirty memory are recorded per process. The next candidates are then picked by which processes and mappings hold the most memory.

## 3. Next week: 23–27 November

1. **Mon:** capture both matched QuickBuilds (Base 20261113.1 and 20261118.1, both build.conf@14452507). Prepare `updateSU2E` for each and run the image relocation baseline scan.
2. **Mon–Tue:** MLGO board A/B on KantSU2E with performance and memory (N3).
3. **Tue:** confirm the perf kernel ISA from the linked vmlinux, so the kernel exemption for EXP-T1 is set correctly.
4. **Tue–Wed:** EXP-T1 GBS pilot on deviced, gst-plugins-dash and inference-engine-tflite (N1).
5. **Tue–Wed:** re-run the option research on the current control image, one experiment each:
   1. R1 forced-option gap (the 4 packages from 11 Nov plus the 34 packages below `-O2`, N5);
   2. R2 inline visibility, after the export audit;
   3. R4 inlining threshold 50 and 25, and R5 MachineOutliner, on the same sample packages;
   4. R3 ThinLTO build time;
   5. R6 lld + ICF and R7 RELR, after the loader check.
6. **Wed–Thu:** `-z text` package trial and the GBS consumer links for the CAPI FatLTO and TLS archives (N2).
7. **Wed–Fri:** LTO enablement on the 80 candidate packages, starting with the four already enabled and then the largest `.text`. Each package passes the API / ABI comparison with the GCC build and the stability run before it leaves the exclusion list (N4).
8. **Thu–Fri:** EXP-T1 QuickBuild if the pilot passes; 1 GB memory attribution during 4K playback.
9. **Fri:** weekly report with measured size, memory and performance for every experiment that finished.
