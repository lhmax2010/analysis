# MLGO Kernel Comparison — Official vs Customized Models

Nov 20, 2026 · @Hao

The LLVM build with the customized MLGO models reduces Linux kernel code by 2.90% (vmlinux `.text`) and the kernel images by about 2%. A fully matched image pair, identical except for the LLVM Base, is being built. The board performance and memory comparison on it will be delivered on Nov 23, 2026.

## 1. Setup and kernel size

| Lane | LLVM package | Base snapshot |
| --- | --- | --- |
| Official | clang/llvm 22.1.8-9.1, VD reference MLGO models | tizen-10.0-base-dev-llvm 20261113.1 |
| Customized | clang/llvm 22.1.8-11.1, customized MLGO models | tizen-10.0-base-dev-llvm 20261118.1 |

Both kernels were rebuilt in GBS from the same source (P4 14293732 + 14427407, 24 overlays), the same config and the same build.conf. All 7,100 compile commands per lane carry `-mllvm -enable-ml-inliner=release` and `-regalloc-enable-advisor=release`. So the kernel difference comes from the LLVM Base swap alone: clang/llvm 22.1.8-9.1 → 22.1.8-11.1, which carries the official vs customized MLGO models, and clang-accel-x86_64-armv7l 0.4-2.4 → 0.4-2.5. The local uImage size matches the QuickBuild uImage exactly in both lanes.

| Item | Official | Customized | Change |
| --- | --: | --: | --: |
| uImage | 11,348,968 B | 11,085,240 B | −2.32% |
| zImage | 5,326,464 B | 5,222,304 B | −1.96% |
| 115 kernel modules | 6,507,334 B | 6,487,666 B | −0.30% |
| vmlinux `.text` | 8,564,600 B | 8,315,832 B | −2.90% |
| Loaded code + data (`.text`, `.init.text`, `.exit.text`, `.rodata`, `.data`) | 10,801,094 B | 10,545,094 B | −2.37% |

[Chart in the doc: Native GBS replay of tztv-kernel, official (llvm 22.1.8-9.1) vs customized (22.1.8-11.1), 18 Nov 2026 — per-section change]

The customized models keep 2,421 more functions out of line (BTF FUNC 37,987 → 40,408; FUNC\_PROTO +1,497). That explains the larger symbol and unwind tables and the +3.37% detached BTF file `/lib/modules/perf/6.12.60/kernel/vmlinux`. None of these is loaded into kernel memory. External kernel modules from 45 driver packages also changed: 60 module `.text` sections differ and 2 are identical.

## 2. User space and board results

- **User space:** `.text` is identical in 4,784 of 4,834 comparable ELF files (98.97%). User-space builds do not use the MLGO advisors, so the compiler change does not alter user-space code.
- **The 50 differing files** are in 9 packages, all with identical NEVRA, source RPM and P4 changelist. Four of them (org.tizen.tv.swu, liballshare-core, nagsam-mw, ug-hbbtv-efl) grew because the earlier customized image was built with build.conf@14431365, which excluded them from LTO. This is a build-configuration difference, not an MLGO effect.
- **Board memory and performance:** the two earlier published images differ in build.conf as well as in Base, so they are not a valid A/B pair.

### Source-matched QuickBuild pair for the board comparison

| Lane | QuickBuild | Product publication | LLVM Base |
| --- | --: | --- | --- |
| Official | 37736448 | 20261123.2 | 20261113.1 |
| Customized | 37736427 | 20261123.1 | 20261118.1 |

Both QuickBuilds use the same published build.conf@14452507 and the same shelf and Base lists. All 5,880 Product RPMs have the same source version and pinned VCS in both lanes, and no source-related field of the published build.xml differs. The LLVM Base is the only build input that differs. The board comparison on KantSU2E runs on this pair with performance and memory results:

| Metric | Runs per lane | Measured |
| --- | --: | --- |
| Cold boot to Home | 5 | Boot time |
| Kernel microbenchmarks (syscall, context switch, memory) | 5 | Latency and throughput |
| 4K stream playback | 3 | Dropped / late frames, stalls, CPU load |
| Memory | During each run | PSS, private dirty, kernel memory |
