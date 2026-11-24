# MLGO Kernel Comparison — Official vs Customized Models

Nov 20, 2026 · @Hao · Rev3 updated Nov 24, 2026

In the historical GBS comparison, the Customized LLVM Base reduced Linux kernel `vmlinux .text` by 2.90% and the kernel images by about 2%. The new QuickBuild pair passed the source and configuration gate. Its only verified build-input change is the LLVM Base. Attribution within the Base and KantSU2E measurements are pending.

## 1. Setup and kernel size

| Lane | LLVM package | Base snapshot |
| --- | --- | --- |
| Official | clang/llvm 22.1.8-9.1, VD reference MLGO models | tizen-10.0-base-dev-llvm 20261113.1 |
| Customized | clang/llvm 22.1.8-11.1, customized MLGO models | tizen-10.0-base-dev-llvm 20261118.1 |

Both kernels were rebuilt in GBS from the same source (P4 14293732 + 14427407, 24 overlays), the same config and the same build.conf. All 7,100 compile commands per lane carry `-mllvm -enable-ml-inliner=release` and `-regalloc-enable-advisor=release`. The controlled input change in this GBS replay was the LLVM Base, which changed clang/llvm 22.1.8-9.1 → 22.1.8-11.1 and clang-accel-x86_64-armv7l 0.4-2.4 → 0.4-2.5. The Clang packages carry the respective MLGO models. The local uImage sizes match the earlier QuickBuild pair. The results below are historical.

| Item | Official | Customized | Change |
| --- | --: | --: | --: |
| uImage | 11,348,968 B | 11,085,240 B | −2.32% |
| zImage | 5,326,464 B | 5,222,304 B | −1.96% |
| 115 kernel modules | 6,507,334 B | 6,487,666 B | −0.30% |
| vmlinux `.text` | 8,564,600 B | 8,315,832 B | −2.90% |
| Loaded code + data (`.text`, `.init.text`, `.exit.text`, `.rodata`, `.data`) | 10,801,094 B | 10,545,094 B | −2.37% |

[Chart in the doc: Native GBS replay of tztv-kernel, official (llvm 22.1.8-9.1) vs customized (22.1.8-11.1), 18 Nov 2026 — per-section change]

The Customized GBS variant has 2,421 more BTF FUNC records (37,987 → 40,408) and 1,497 more FUNC_PROTO records, consistent with more out-of-line functions. The packaged detached BTF file `/lib/modules/perf/6.12.60/kernel/vmlinux` grew 3.37%. In the earlier image pair, 60 of 62 comparable external-module `.text` sections across 45 RPM owners differed.

## 2. User space and board results

- **Earlier user-space comparison:** `.text` is identical in 4,784 of 4,834 comparable ELF files (98.97%). The new matched QuickBuild pair needs its own comparison.
- **The 50 differing files** are in 9 packages, all with identical NEVRA, source RPM and P4 changelist. Four of them (org.tizen.tv.swu, liballshare-core, nagsam-mw, ug-hbbtv-efl) grew because the earlier customized image was built with build.conf@14431365, which excluded them from LTO. This is a build-configuration difference, not an MLGO effect.
- **Board memory and performance:** the two earlier published images differ in build.conf as well as in Base, so they are not a valid A/B pair.

### Source-matched QuickBuild pair

| Lane | QuickBuild | Product publication | Published LLVM Base |
| --- | ---: | --- | --- |
| Official | 37736448 | 20261123.2 | 20261113.1 |
| Customized | 37736427 | 20261123.1 | 20261118.1 |

Step 2 verified the same published `TIZEN_KantSU2E_Clang_build.conf@14452507`, the pinned shelf and Base-list copies, matching published source-related XML fields, and matching source versions and pinned VCS for all 5,880 Product RPM identities. The published Base selector changed from 20261113.1 to 20261118.1. The Base proof will check the LLVM source payload, accelerator and other installed Base dependencies before narrowing attribution. Board measurements are planned as follows. [Step 2 evidence](../../../artifacts/evidence/native-run-r0011-step2-pair-gate-20261124.txt)

| Metric | Runs per lane | Measured |
| --- | --: | --- |
| Cold boot to Home | 5 | Boot time |
| Kernel microbenchmarks (syscall, context switch, memory) | 5 | Latency and throughput |
| 4K stream playback | 3 | Dropped / late frames, stalls, CPU load |
| Memory | During each run | PSS, private dirty, kernel memory |
