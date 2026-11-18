# Status — 2026-11-17, round 0002

- The TV boots the LLVM-configured image. Installed RPM identities and the live memory map are recorded.
- The compiler coverage count needs RPM payload and producer checks. The board matched 2,342 package identities to repository metadata.
- The PIC design draft is ready for review. Local ARM screening passed a smoke check, and the full validation needs the retained native-server fixtures.
- Next, refresh OBS MLGO status and server capacity, screen the pinned inputs and use controlled playback for memory attribution. The 10.1 track continues in parallel.
- Before a full 1 GB trial, confirm the 4K memory carveouts and an attended test window. A later boot limit needs the exact recovery procedure.

Round 0001 was accepted as the baseline. Round 0002 results and proposal updates await review. [Reply and commands](../comms/codex_to_claude/0002_reply.md)

| Workstream | Evidence-backed state | Next gate |
|---|---|---|
| 10.0 image/compiler ledger | T-KSU2EJAKUC-0101-PERF-202611171009, 2,342 installed RPMs, 1,839 source strings | Payload, DWARF/source attribution, in-scope coverage and exact QB job export |
| gst-ffmpeg and AVControl | Scoped TV seek regression and AVControl static closure still valid | Repeated current-image and dynamic consumer acceptance |
| Customized MLGO | Latest retained OBS evidence shows rev12, armv7l/x86_64 building | T1 status-only refresh on native server |
| 10.1 parallel | Scoped bootstrap, smoke and RPM layout passed | Production accelerator compatibility, bounded by D-018 |
| HQ PIC/ABI | Producer policy drafted, 56 synthetic outcomes retained, basic ARM classifier exercised | Native 56-case validation then 92 pinned RPM identities and consumer attribution |
| Thumb | 27 ARM and 232 Thumb retained cohort reproduced. 4,861 unknown lack usable mapping spans | Expand Build-ID debug coverage, classify causes and measure paired Thumb size |
| 1 GB / memory | Memory ranges and normal-board top-20 VMA evidence recorded | 4K pool mapping, attended Method A pilot, paired measurements |
| Capacity | Last available /home1 239.68 GiB, older vd-tree size 348.73 GiB | Live native capture and confirmed concurrency bounds |

[Tracker](../artifacts/progress_tracker.csv) records scoped completions and current dependencies. Overall adaptation coverage and performance/memory acceptance remain unknown.
