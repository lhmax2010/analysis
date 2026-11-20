# Tizen LLVM weekly progress, 16–20 November

Draft for Friday. This revision includes the retained QuickBuild, ELF section and compiler-probe evidence through 20 November. Board acceptance remains pending.

The compiler migration covers packages that can be built with Clang. Exceptions require package evidence that a component needs GNU GCC or that its shipped content is outside our GCC/Clang build, such as Rust, Go, data or vendor prebuilts. Kernel, bootloader, TEE and driver components are evaluated individually. Optimization continues after each measured gain. Smooth 4K on KantSU2E under a physical 1 GB budget is a key stress benchmark.

| Area | Planned this week | Verified through this draft | Next validation |
|---|---|---|---|
| Product compiler coverage | Identify installed code and establish scope | 2,342 installed RPM identities matched the pinned repository metadata | Inspect exact ELF payloads and valid producer evidence, then calculate eligible source-package coverage |
| PIC and FatLTO | Verify native and LTO consumption and propose producer policy | Tizen ARM matrix had 38 runtime passes and 18 native link rejections. A subsequent GNU ld 2.43 GBS fixture links ABS32 in .text under the default, emits TEXTREL, and rejects it under `-z text` | Run the PERF baseline, qualify actual consumers and trial strict links on affected packages |
| Stability / media | Retain a reproducible regression control | Scoped gst-ffmpeg target playback, seek and reopen passed in earlier target testing | Broader current-image and endurance acceptance |
| Compiler/flag optimization | Check impact and dependencies before target rollout | AVControl candidate reduced allocated ELF size from 1,055,033 to 364,120 bytes and direct NEEDED entries from 108 to 34 | Validate dynamic consumers, target performance and stability |
| Thumb | Reproduce the baseline with evidence | Full installed-image scan identifies 609 ARM-predominant ELFs. In the GBS probe, the GCC wrapper appended Thumb while the unflagged Clang driver emitted A32 | Join actual per-package compile commands and measure paired package sizes and KantSU2E workloads |
| 1 GB and memory | Confirm board memory map and start attribution | Captured ARM32 memory banks, low/highmem, reusable CMA ranges and normal-board process memory | Identify pools required for 4K, test reversible pressure, then run controlled playback |
| MLGO Official/Customized | Compare the kernel on frozen 1113.1 and 1118.1 Base images | Published uImage −2.32%, zImage −1.96%. User-space .text matches in 4,784 of 4,834 comparable ELFs. Both advisor flags appear in the local GBS replay. Four packages newly excluded from LTO in the Customized build.conf account for all positive user-space .text growth | Rebuild with build.conf 14452507 in both lanes, confirm package parity and then measure on KantSU2E |
| Tizen 10.1 | Continue parallel migration | Scoped ARM bootstrap, linker/runtime checks and RPM layout evidence available | Confirm production acceleration and downstream package/image acceptance |

Stability and performance conclusions remain scoped to completed measurements. A full GCC/LLVM runtime comparison needs a matched-source GCC control. Historical GCC/LLVM comparisons also include different optimization, hardening, ISA and LTO policies. Where the GCC force wrapper applies it appends `-O2 -fstack-protector-strong`, while the tested Clang optflags are `-Os -fstack-protector`. [Compiler options evidence](../artifacts/historical-reports/hq-compiler-options-lto.md#L100)

The working Thumb cohort will use the new full installed-RPM scan and exact build evidence. Historical symbol-only results remain archived. The argot target/ABI checks and paired size measurements continue through the November 25 follow-up.
