# Tizen LLVM weekly progress, 16–20 November

Draft for Friday. This revision reflects verified data through the 17 November workstation and target captures. Refresh Wednesday through Friday status before transmission.

The compiler migration covers packages that can be built with Clang. Exceptions require package evidence that a component needs GNU GCC or that its shipped content is outside our GCC/Clang build, such as Rust, Go, data or vendor prebuilts. Kernel, bootloader, TEE and driver components are evaluated individually. Optimization continues after each measured gain. Smooth 4K on KantSU2E under a physical 1 GB budget is a key stress benchmark.

| Area | Planned this week | Verified through this draft | Next validation |
|---|---|---|---|
| Product compiler coverage | Identify installed code and establish scope | 2,342 installed RPM identities matched the pinned repository metadata | Inspect exact ELF payloads and valid producer evidence, then calculate eligible source-package coverage |
| PIC and FatLTO | Verify native and LTO consumption and propose producer policy | Tizen ARM synthetic matrix had 38 runtime passes and 18 expected native link rejections. Local ARM relocation screen smoke passed | Verify all retained matrix inputs, then screen 92 repository RPM identities and qualify actual consumers |
| Stability / media | Retain a reproducible regression control | Scoped gst-ffmpeg target playback, seek and reopen passed in earlier target testing | Broader current-image and endurance acceptance |
| Compiler/flag optimization | Check impact and dependencies before target rollout | AVControl candidate reduced allocated ELF size from 1,055,033 to 364,120 bytes and direct NEEDED entries from 108 to 34 | Validate dynamic consumers, target performance and stability |
| Thumb | Reproduce the baseline with evidence | Retained measurement reproduced 27 ARM-predominant ELF paths. Seven have explicit non-CRT `-marm` producer evidence | Match more debuginfo, trace build overrides and measure paired object sizes and target workload |
| 1 GB and memory | Confirm board memory map and start attribution | Captured ARM32 memory banks, low/highmem, reusable CMA ranges and normal-board process memory | Identify pools required for 4K, test reversible pressure, then run controlled playback |
| MLGO Official/Customized | Compare frozen 1113.1 and 1118.1 Base images, then isolate model effects | Current image retained as 1113.1 control. Rev12 source embeds both custom models by default. Repository and effective advisor preflight staged | Verify both architectures, full RPM delta and actual advisor use before QuickBuild. Measure target and static changes on the pair |
| Tizen 10.1 | Continue parallel migration | Scoped ARM bootstrap, linker/runtime checks and RPM layout evidence available | Confirm production acceleration and downstream package/image acceptance |

Stability and performance conclusions remain scoped to completed measurements. A full GCC/LLVM runtime comparison needs a matched-source GCC control. The current week’s work establishes the evidence and validation gates for that comparison.

A weighted dynamic-symbol pass on the 5,120 retained paths added 185 ARM and 1,658 Thumb lower-bound decisions. 3,018 entries still require additional evidence. Matched debug and paired Thumb size work continue through the November 25 follow-up.
