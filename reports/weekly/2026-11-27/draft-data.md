# KantSU2E PERF · Friday 27 November 2026

Evidence cutoff 26 November. One board. All kernel size and Thumb ELF size figures are bytes.

## Shipped kernel sizes

| VDLinux PERF (bytes) | GCC 37564293 | Official MLGO 37736448 | Custom MLGO 37736427 | Official − GCC | Custom − GCC | Custom − Official |
|---|---:|---:|---:|---:|---:|---:|
| Text | 9,364,188 | 8,564,632 | 8,315,864 | −799,556 | −1,048,324 | −248,768 |
| Data¹ | 683,008 | 681,984 | 680,960 | −1,024 | −2,048 | −1,024 |
| BSS¹ | 4,117,504 | 4,120,576 | 4,121,600 | +3,072 | +4,096 | +1,024 |
| Total | 12,218,544 | 11,348,904 | 11,085,176 | −869,640 | −1,133,368 | −263,728 |
| uImage | 12,218,608 | 11,348,968 | 11,085,240 | −869,640 | −1,133,368 | −263,728 |
| zImage | 5,664,248 | 5,326,504 | 5,222,032 | −337,744 | −442,216 | −104,472 |
| rodata | 1,740,800 | 1,679,360 | 1,675,264 | −61,440 | −65,536 | −4,096 |
| init¹ | 421,888 | 413,696 | 405,504 | −8,192 | −16,384 | −8,192 |
| tztv-kernel-perf RPM | 20,018,029 | 19,345,448 | 19,160,700 | −672,581 | −857,329 | −184,748 |

Text and rodata use inclusive physical ranges from each running kernel. Data, BSS and init use boot accounting at whole-KiB resolution, converted to bytes. ¹GCC values are derived from its verified kernel image using the mem_init print formula. The same calculation reproduced Official 666/4,024/404 KiB and Custom 665/4,025/396 KiB exactly. Total is uImage file length minus the 64-byte header, including the 260-byte trailer. HQ's RPI Total definition remains unverified. [Raw byte table, formulas and identity](../../../comms/codex_to_claude/0012u_reply.md)

All three use kernel source CL 14293732. Official and Custom have matching published Product source/VCS for all 5,880 rows and differ in LLVM Base, 20261113.1 versus 20261118.1. GCC uses Product 20261113.1 and Base 10.1/20260919.1. GCC versus LLVM also changes Product sources, installed releases and compiler-dependent config. Of 34 differing config symbols, only MLGO and its two children differ as enabled optimization selections. [QB pair gate](../../../artifacts/evidence/native-run-r0011-step2-pair-gate-20261124.txt)

## AVControl and the Thumb-2 census

| Delivered AVControl ELF | Baseline | Scoped Clang default | Default − baseline |
|---|---:|---:|---:|
| .text | 736,944 | 441,362 | −295,582 (−40.11%) |
| Allocated section bytes | 1,055,461 | 758,644 | −296,817 |
| Estimated A32 / executable bytes | 740,645 / 740,764 | 4,245 / 445,170 | 99.984% → 0.954% |

Provisional file measurements. Both retained lanes reported `NOT_DELIVERED` for acceptance. The earlier package-fix lane failed in %install. The corrected four-stage wrapper subsequently passed the baseline smoke. T3 (scope) passed for the scoped default. T1 requires the executed final link, LTO options and CU evidence. T2 requires attribution of the residual A32 and coverage of unmapped .text. T4 showed matching SONAME, NEEDED and exports, with type-level abidiff outstanding. T5/T6 need accepted test, interworking and load/run receipts. T7 needs the real target objects resolved among 28 reported gaps, including two CMake probes. T8 is inapplicable. The native three-lane pilot supplies the next acceptance data. A deployed RAM or PSS saving has not been measured. [Native counts](../../../artifacts/evidence/native-run-r0012m-pilot-and-r0012p-size-20261125.txt) · [Gate evidence](../../../comms/codex_to_claude/0012t_reply.md)

Historical QB 37627297 had 609 ARM-predominant files among 5,166 loadable ELFs from 2,342 installed RPMs. The scan counted 179 relocatable kernel-module files separately. It returned exact A32 bytes and the measurement basis for ranks 1–211. Retained build logs identified source flag replacement and 26 AVControl / 549 tv-viewer Clang invocations lacking -mthumb. For matched Official 37736448, the reviewed range ledger currently contains zero evidence rows. Its denominator and per-file causes require the installed-image scan and compile evidence. [Historical measurements](../../../artifacts/thumb-repro/a32-exact-top211-20261124.tsv) · [Build flag origins](../../../artifacts/ledger/thumb-flag-origins-20261124.tsv) · [Matched reviewed ranges](../../../artifacts/ledger/official-37736448-thumb-reviewed.tsv)

## Whole-board measurements

**Base switch, not MLGO alone.** One warm software reboot per memory series. Each sample was taken with Home in focus; the three samples within a lane share one boot. G1 also changes Product, OS libraries and compiler relative to C1.

| MemAvailable at Home | G1 uptime (s) | GCC G1 (KiB) | C1 uptime (s) | Custom C1 (KiB) | G1 − C1 (KiB) |
|---|---:|---:|---:|---:|---:|
| Warm · 6 min | 360.14 | 1,090,696 | 360.72 | 1,086,360 | +4,336 |
| Warm · 7 min | 420.13 | 1,084,840 | 420.69 | 1,084,280 | +560 |
| Warm · 8 min | 480.13 | 1,088,000 | 480.71 | 1,088,472 | −472 |
| Median of three | | 1,088,000 | | 1,086,360 | +1,640 |

| In-image workload | G1 trials (s) | G1 median | C1 trials (s) | C1 median | G1 − C1 |
|---|---|---:|---|---:|---:|
| gzip | 0.42, 0.42, 0.42, 0.41, 0.43 | 0.42 s | 0.41, 0.41, 0.41, 0.41, 0.42 | 0.41 s | +0.01 s |
| xz | 0.83, 0.83, 0.85, 0.82, 0.83 | 0.83 s | 0.93, 0.93, 0.93, 0.92, 0.92 | 0.93 s | −0.10 s |

Both lanes used 16 MiB of zeros, SHA-256 `080acf35a507ac9849cfcba47dc2ad83e01b75663a516279c8b9d243b719643e`, SDK uid 5001, CPU 0, gzip `-n -6 -c` and xz `-T1 -3 -c` with output to /dev/null. All trials exited 0. The uptime clock resolves 0.01 s, equal to the gzip median difference. Workloads began at uptime 550.21 s on G1 and 7,179.28 s on C1; the C1 workload and C1 warm idle samples came from different boots. G1 and C1 gzip, xz, libc, loader, libgcc_s and liblzma differ by SHA-256. This dataset measures elapsed time of the installed user-space programs on two complete images.

[Raw G1 files and hashes](../../../artifacts/evidence/board/g1-37564293/0012v/SHA256SUMS) · [C1 warm series](../../../artifacts/evidence/board/c1-37736427/warm/SHA256SUMS) · [C1 workload](../../../artifacts/evidence/board/c1-37736427/workloads.txt) · [Binary-by-binary comparison](../../../artifacts/evidence/board/g1-37564293/0012v/workload-hashes.tsv)

Installed name/architecture keys: G1 2,343, O1 and C1 2,342 each. G1 → either LLVM lane has 175 release-only changes, nine version changes, one addition and two removals. O1 → C1 has 178 release-only changes. [Full roster comparison](../../../artifacts/evidence/board/g1-37564293/0012v/roster-comparison.tsv)

## Remaining measurements and blockers

| Item | Evidence available | Blocking input |
|---|---|---|
| Image scan and installed-owner census | pm0012-image.mKv04z platform rc=1, unsupported EROFS features 0x180. New upstream host tool passed 48-bit/metabox LZ4 and Zstd extraction with exact byte comparison. | All four raw headers show incompat 0x1a3 and algorithm mask 0x10. GCC BTF and both shipped kernel dispatch tables identify ID 4 as vendor ZLIB. Vendor reader fsck, full extraction, entry counts and image RPM DB comparisons are outstanding. [Four-partition evidence](../../../comms/codex_to_claude/0012z_reply.md) |
| Kernel K0–K5 and GCC perf config | OwlD9Q stopped before compilation at GBS spec selection. GCC USB verified. Perf config digests GCC bb8208f4 and Official 2a316525. | Relaunch receipt with HEAD spec selection and parent CONFIG_MLGO=n in K2/K3; external-module owners from image census. |
| Whole-board MLGO comparison | C1 and G1 have signed workload data. GCC and Custom differ in OS libraries and Product. | O2 signed workloads on the Official board with the same protocol, replicated independent boots, and control of user-space/other Base deltas. |
| AVControl production acceptance | Scoped ELF sizes above. | The baseline/default/package pilot can run from the qualified smoke. Installed-image matches remain open. |
| LTO non-PIC fallback | Source1005 in both Official and Custom SRPMs is byte-equal to the independent review copy (SHA-256 7d89083453e1d75707a4a6b3a6d9510a4c31e09d8e99865de2a18e07945bf76f). | Independent reviewer findings and disposition. No REVIEW-*.md is archived in the review directory. The regular-LTO IR patch leaves native consumption of fat objects as a separate consumer/link qualification. |

[Image and Source1005 readback](../../../artifacts/evidence/native-run-r0012r-image-mKv04z-erofs-20261125.txt) · [Upstream tool fixture](../../../artifacts/evidence/erofs-upstream-0012v.txt) · [Independent review request](../../../reviews/lto-nonpic-fallback/README.md)

## Current Thumb-2 board reference · 26 November capture

| Artifact (bytes) | Official 37777148 | Custom 37777264 | Custom − Official |
|---|---:|---:|---:|
| uImage | 11,348,968 | 11,085,240 | −263,728 |
| zImage | 5,326,496 | 5,222,024 | −104,472 |
| tztv-kernel-perf RPM | 19,345,800 | 19,160,803 | −184,997 |

Build IDs are `de1c600eee82b0fdebd9f2d1161d2271b2c9b4cc` and `8f9c7262bfae0f13de8b1b13710cc4669398ba37`. Relative to each earlier lane, uImage length is unchanged, zImage is eight bytes smaller, and the RPM grew by 352 or 103 bytes respectively. All artifact hashes changed. Published VCS matched 5,880/5,880. Submitted shelf and Base-list copies remain unproved. PM accepted this pair for the board comparison. The earlier kernel and board measurements retain their original QB labels. [Pair and USB evidence](../../../artifacts/evidence/native-run-r0012z-pilot-pair-reader-20261126.txt)

## Optimization tracks · status at 26 November, before the overnight readback

| Track | Evidence measured this week | Open measurement | Next gate |
|---|---|---|---|
| N1 Thumb-2 | Official 37736448 policy, AVControl local reference/scoped/packaging lanes. Smoke and T3 passed. Earlier scoped .text was 441,362 B. | Final byte coverage and acceptance; signed application and board PSS. | Re-evaluate retained outputs, then gated installed roster on 37777148/37777264. |
| N2 strict text relocations | No new strict-link trial on 37777148. | Ownership, affected pages, actual link rejection. | E4 static census; strict-link trial stays gated. |
| N3 kernel MLGO/outliner | Shipped byte table above, prior-board boot accounting, and GCC perf config comparison. | K0–K5 effective argv, section/call-site deltas and controlled hot-path timing. | Kernel batch running independently. |
| N4 LTO enablement | No new size/ABI pair on 37777148. Prior inventory has 76 candidates plus four policy-enabled packages. | Final-link signature in published ELFs, A/B size, ABI and stability. | E3, then top ten in pkg; runtime gate before policy change. |
| N5 optimization level | Prior four-package evidence; no new acceptance rows for the remaining 30. | Current 34-package per-ELF baseline and CU-qualified -Os pairs. | E2, then ranked pkg builds; preserve libgcrypt's low-level choices. |
| GCC replacement | 20 Nov reference: 101 packages with GCC-marker ELFs, 27 reported hard-coded fixes. | New 37777148 census, fix inclusion and all-Clang status by source. | E1 byte/provenance evidence and submission manifest where needed. |
| R1 forced options | November reference recipes and four-package cohort. No new matched R1 run this week. | New pair and signed-char board checks. | Prove treatment and source match before combining changes. |
| R2 inline visibility | No new measured treatment. | Installed consumers of weak C++ exports and dynamic lookup. | E5 then installed hash join and package-specific ABI review. |
| R3 ThinLTO | No new matched build timing. | Separate controlled timing/size comparison. | Retain full-LTO baseline and matching build resources. |
| R4 inline threshold | No new measurement on 37777148. | Threshold-50 .text and codegen per package. | pkg paired runs, actual plugin argv, later hot-path timing. |
| R5 machine outliner | New package and kernel outliner results outstanding. | .text, unwind and performance. | pkg four-package R5 plus separate K0–K5 experiment. |
| R6 lld / ICF | No new matched result. | Linker-only A/B and subsequent safe ICF. | Resolve linker dependencies; qualify each change separately. |
| R7 RELR | Earlier projection is historical. No new installed savings measured. | Packed-file estimate, loader evidence, acceptance by both linkers. | E6 and a future load/compatibility test. |

[Pilot, reader and pair transcript](../../../artifacts/evidence/native-run-r0012z-pilot-pair-reader-20261126.txt) · [20 November reference figures](../2026-11-20/01_Optimization_Plan_and_New_Observations.md) · [Native measurements and gates](../../../comms/codex_to_claude/0013a_reply.md)

## Thumb-2 acceptance plan · Official QB 37777148

Baseline for rollout is Official 37777148. A candidate QB ID has yet to be assigned. Use the same Product source revisions, LLVM Base, kernel, packaging, LTO, optimization level and MLGO settings. Record all manifest, compiler argv and installed ELF differences. A packaging lane that newly enables LTO or changes optimization needs separate attribution. The AVControl pilot used the earlier Official configuration. Its reference/default .text was 736,944/441,362 B (−40.1%) and its mapped A32 code was 693,820/88 B. Its package lane measured 179,660 B. These are file measurements. [Pilot evidence](../../../artifacts/evidence/native-run-r0013a-bce-qp4O4m-20261126.txt)

Owners below are proposed responsibilities for review. Each gate requires an evidence file for its stated baseline and candidate.

| Gate | Owner | Method | Acceptance | Status |
|---|---|---|---|---|
| C1 ARM-only source | Package maintainers + VD toolchain | Map 609 historical paths to current source packages. Review inline asm and assembly directives, encodings, instruction width assumptions, jump tables and returns. Check actual flags for the affected TU. | Give every hit a file/line disposition and prove the authored mode, verify a fix, or register an exclusion. Account for missing source or renamed files. | Official source screen prepared; owner dispositions open |
| C2 interworking | Toolchain + vendor library owners | Disassemble shipped prebuilts and ELFs lacking CU provenance. Match candidate returns to symbols, NEEDED providers and importing ELFs. Review callers, indirect/dynamic lookup and actual ISA at calls. | Establish that no incompatible return is reachable from Thumb callers. Resolve each uncertain path by instruction semantics, integration test, fix or exclusion. | Official screen prepared; reachability open |
| C3 binary interface | ABI owner + package maintainers | Compare the same installed ELF path, SONAME, NEEDED and defined dynsym name/type/binding/version/size on both images. Retain complete diffs; check symbol versions and object/TLS sizes. | Required fields identical. Any difference, including an STT_FUNC size change, goes to review; record any approved change to the criterion separately. | Requires candidate RPMs |
| C4 frame pointers and unwind | Crash reporting + profiling + runtime owners | Find frame-pointer walkers and r11 assumptions; inspect EHABI tables, coverage and CANTUNWIND entries. Validate symbolized Thumb crash and sampled stacks against known call chains on board. | Crash reporter, profiler and applicable sanitizer/backtrace users resolve expected frames across ISA boundaries. Document compact exidx entries that do not require an extab. | Official static screen prepared; board proof open |
| C5 generated code | Web, managed-runtime and FFI owners | Inventory V8/Chromium, .NET, JS/Lua JITs, FFI trampolines. Compare emitter options and boundaries in both builds, exercise JIT→native→JIT and callback paths. | Prove ISA settings unchanged or register explicit package exclusion. New code-generation modes require independent qualification. | Official inventory prepared; candidate comparison open |
| C6 exclusions | Kernel, boot, TEE, firmware and package owners | Retain actual argv for kernel, modules, bootloader, firmware and explicit ARM overrides. Check final cc1 triple and mapping symbols, including authored NEON/asm. | Every excluded unit retains its intended mode. Explicit package -marm wins over the distribution default. | Candidate argv and outputs required |

| Gate | Owner | Same-board comparison | Acceptance | Status |
|---|---|---|---|---|
| P1 hot code | Media/UI + profiling | 3 matched playback/navigation profiles per image. Join sampled functions and owning RPMs to build IDs and A32/T32 mappings. | Identify packages whose sampled hot functions changed ISA; quantify unresolved sample weight. | Await Thumb QB |
| P2 microbenchmarks | Performance team | 5 paired runs per workload: signed gzip, xz, zstd, OpenSSL SHA-256/AES-CBC, JPEG/PNG decode, memcpy/memset. | Per workload median regression ≤3%. Send each excess to its package owner. | Await Thumb QB and signed-tool inventory |
| P3 system latency/media | KantSU2E board + media QA | Cold boot ×5, top five app launches ×5 each, identical 4K playback and seek/reopen ×3 per image. Measure CPU, drops and A/V sync. | Paired intervals within predeclared repeatability bands; zero new dropped-frame events. | Await Thumb QB, fixture and telemetry qualification |
| P4 memory | Memory + application owners | 3 matched Home-idle and 4K samples per image. Join MemAvailable and PSS for a fixed set of top media/UI processes, including children. | Report bytes saved. No increase in matched PSS or reduction in available memory beyond agreed measurement precision. | Await Thumb QB |
| P5 stability | System QA | 24 h playback and app cycling on each image, collect crash/dump and reboot evidence. | Zero new crashes, including SIGILL/SIGBUS/SIGSEGV. | Await Thumb QB |

For a measured regression, the owner reviews a per-package `-marm` opt-out and repeats the failed gate on a matched image. The affected package, measured hot function, decision and retest remain in the ledger. Hand-written NEON and assembly retain their authored mode. [Static launcher and board procedure](../../../comms/codex_to_claude/0013g_reply.md)
