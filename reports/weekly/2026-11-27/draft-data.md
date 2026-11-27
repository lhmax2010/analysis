# KantSU2E PERF · Friday 27 November 2026

Evidence cutoff 27 November (jFI9ye). One board. All kernel size and Thumb ELF size figures are bytes.

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
| R7 RELR | 18,016,828 B estimated installed relocation-table saving. | Official glibc 2.40-1.111 libc defines GLIBC_ABI_DT_RELR. | Ready for three-package lld 22 trial after 0013o canary; actual size, dirty-page and board load results open. |

[Pilot, reader and pair transcript](../../../artifacts/evidence/native-run-r0012z-pilot-pair-reader-20261126.txt) · [20 November reference figures](../2026-11-20/01_Optimization_Plan_and_New_Observations.md) · [Native measurements and gates](../../../comms/codex_to_claude/0013a_reply.md)

## Thumb-2 acceptance plan · Official QB 37777148

Baseline for rollout is Official 37777148. A candidate QB ID has yet to be assigned. Use the same Product source revisions, LLVM Base, kernel, packaging, LTO, optimization level and MLGO settings. Record all manifest, compiler argv and installed ELF differences. A packaging lane that newly enables LTO or changes optimization needs separate attribution. The AVControl pilot used the earlier Official configuration. Its reference/default .text was 736,944/441,362 B (−40.1%) and its mapped A32 code was 693,820/88 B. Its package lane measured 179,660 B. These are file measurements. [Pilot evidence](../../../artifacts/evidence/native-run-r0013a-bce-qp4O4m-20261126.txt)

Owners below are proposed responsibilities for review. Each gate requires an evidence file for its stated baseline and candidate.

| Gate | Owner | Method | Acceptance | Status |
|---|---|---|---|---|
| C1 ARM-only source | Package maintainers + VD toolchain | Map 609 historical paths to current source packages. Review inline asm and assembly directives, encodings, instruction width assumptions, jump tables and returns. Check actual flags for the affected TU. | Give every hit a file/line disposition and prove the authored mode, verify a fix, or register an exclusion. Account for missing source or renamed files. | Official source screen prepared; owner dispositions open |
| C2 interworking | Toolchain + vendor library owners | Disassemble shipped prebuilts and ELFs lacking CU provenance. Match candidate returns to symbols, NEEDED providers and importing ELFs. Review callers, indirect/dynamic lookup and actual ISA at calls. | Identify Thumb ALU-to-PC paths reachable from ARM callers; check instruction state and control flow at each edge. Resolve each uncertain path by instruction semantics, integration test, fix or exclusion. | Prior count included interworking A32 and load-to-PC returns; 0013l reclassification pending |
| C3 binary interface | ABI owner + package maintainers | Compare the same installed ELF path, SONAME, NEEDED and defined dynsym name/type/binding/version/size on both images. Retain complete diffs; check symbol versions and object/TLS sizes. | Required fields identical. Any difference, including an STT_FUNC size change, goes to review; record any approved change to the criterion separately. | Requires candidate RPMs |
| C4 frame pointers and unwind | Crash reporting + profiling + runtime owners | Find frame-pointer walkers and r11 assumptions; inspect EHABI tables, coverage and CANTUNWIND entries. Validate symbolized Thumb crash and sampled stacks against known call chains on board. | Crash reporter, profiler and applicable sanitizer/backtrace users resolve expected frames across ISA boundaries. Document compact exidx entries that do not require an extab. | Official static screen prepared; board proof open |
| C5 generated code | Web, managed-runtime and FFI owners | Inventory V8/Chromium, .NET, JS/Lua JITs, FFI trampolines. Compare emitter options and boundaries in both builds, exercise JIT→native→JIT and callback paths. | Prove ISA settings unchanged or register explicit package exclusion. New code-generation modes require independent qualification. | Official inventory prepared; candidate comparison open |
| C6 exclusions | Kernel, boot, TEE, firmware and package owners | Retain actual argv for kernel, modules, bootloader, firmware and explicit ARM overrides. Check final cc1 triple and mapping symbols, including authored NEON/asm. | Every excluded unit retains its intended mode. Explicit package -marm wins over the distribution default. | Candidate argv and outputs required |
| C7 ARMv8 AArch32 IT | Toolchain + kernel | On each image count mapped T32 IT blocks with >1 slot or a 32-bit instruction; retain stripped/unknown coverage. Establish active ITD at the relevant exception level from validated board evidence or CPU setup. | ITD=0 confirmed and site count reviewed. If ITD=1, every deprecated site requires repair. | Accepted by PM on shipped Official; signed-binary board smoke confirms compatibility. Recheck candidate paths. |
| C8 alignment | Kernel + package owners | Inventory mapped T32 LDRD/STRD/LDM/STM sites. Record /proc/cpu/alignment settings, counters and SIGBUS across matched soak intervals. | Zero new alignment fixups or SIGBUS; instruction counts alone do not establish address alignment. | Static launcher ready; board open |
| C9 mixed control transfers | C++ runtime + QA | Signed fixtures for cross-ISA throw/catch, setjmp/longjmp and a Thumb signal handler with ucontext verification. Exercise both directions where applicable. | Expected handler, register state, exception and return in each case. | Signed fixtures and candidate needed |
| C10 core analysis | Crash reporting + QA | Symbolize a known QA core against the actual build IDs; verify CPSR.T, mapping symbols and expected mixed frames. | Correct mode and frame order. Record missing/stripped symbols separately. | Board/core evidence required |

| Gate | Owner | Same-board comparison | Acceptance | Status |
|---|---|---|---|---|
| P1 hot code | Media/UI + profiling | 3 matched playback/navigation profiles per image. Join sampled functions and owning RPMs to build IDs and A32/T32 mappings. | Identify packages whose sampled hot functions changed ISA; quantify unresolved sample weight. | Await Thumb QB |
| P2 microbenchmarks | Performance team | 5 paired runs per workload: signed gzip, xz, zstd, OpenSSL SHA-256/AES-CBC, JPEG/PNG decode, memcpy/memset. | Per workload median regression ≤3%. Send each excess to its package owner. | Await Thumb QB and signed-tool inventory |
| P3 system latency/media | KantSU2E board + media QA | Cold boot ×5, top five app launches ×5 each, identical 4K playback and seek/reopen ×3 per image. Measure CPU, drops and A/V sync. | Paired intervals within predeclared repeatability bands; zero new dropped-frame events. | Await Thumb QB, fixture and telemetry qualification |
| P4 memory | Memory + application owners | 3 matched Home-idle and 4K samples per image. Join MemAvailable and PSS for a fixed set of top media/UI processes, including children. | Report bytes saved. No increase in matched PSS or reduction in available memory beyond agreed measurement precision. | Await Thumb QB |
| P5 stability | System QA | 24 h playback and app cycling on each image, collect crash/dump and reboot evidence. | Zero new crashes, including SIGILL/SIGBUS/SIGSEGV. | Await Thumb QB |

For a measured regression, the owner reviews a per-package `-marm` opt-out and repeats the failed gate on a matched image. The affected package, measured hot function, decision and retest remain in the ledger. Hand-written NEON and assembly retain their authored mode. [Static launcher and board procedure](../../../comms/codex_to_claude/0013g_reply.md)

## Retained perf kernels · 26 November

| GBS lane | Release advisors | Outline | .text (B) | Δ .text within advisor setting | zImage (B) | Δ zImage | Helpers | Helper bytes |
|---|---|---|---:|---:|---:|---:|---:|---:|
| K0 | On | Off | 8,564,600 | baseline | 5,326,464 | baseline | 0 | 0 |
| K1 | On | On | 8,214,312 | −350,288 (−4.09%) | 5,449,312 | +2.31% | 20,324 | 316,380 |
| K2 | Off | Off | 9,859,176 | baseline | 5,916,376 | baseline | 0 | 0 |
| K3 | Off | On | 9,369,924 | −489,252 (−4.96%) | 6,068,112 | +2.56% | 26,020 | 411,200 |

Outlining reduced linked .text in both comparisons while increasing compressed zImage. The .text interaction (K1−K0)−(K3−K2) is +138,964 B. The K1/K3 perf ELFs and compiler argv were recovered with build IDs `63a81d71…` and `853412bc…`. Their whole RPM builds failed later in the GCC SERET-UL step. These are local perf measurements. Both signed outline QB IDs and their board measurements remain open. [K0/K2 receipt](../../../artifacts/evidence/native-run-r0013d-kernel-dkyJ0S-follower-20261126.txt) · [K1/K3 receipt](../../../artifacts/evidence/native-run-r0013i-read-a0Pmc0-0013f-HgSjf0-0013g-nkPaPY-20261126.txt)

**Thumb-2 kernel blocker.** K4/K5 hit `stmia r0, {r0 - r15}` in VDLinux-modified `arch/arm/lib/backtrace-clang.S:19`. The K4 diagnostic also identifies `mov r8, sp, lsr #12` in `check_overflow` at `arch/arm/kernel/entry-armv.S:375`. Replay coverage was 1/84 assembler commands. The two confirmed sites are a partial inventory. Keep the peripheral and userspace Thumb experiments separately identified. [Assembly diagnostics](../../../artifacts/evidence/native-run-r0013i-read-a0Pmc0-0013f-HgSjf0-0013g-nkPaPY-20261126.txt)

## Kernel -moutline side effects

| Check | Evidence for each outlined kernel relative to its own control | Status on 26 November |
|---|---|---|
| S1 boot-critical sections | Input and final sections, callers, direct reachability from entry/vector/idmap/MMU-off and cross-section list | Release gate awaiting both native verdicts |
| S2 stack/LR | Tail/thunk/register/stack/no-local-save/unknown sites; nested extra-save estimate and IRQ/entry checks against 8 KiB | Static return pending; indirect/recursive worst case open |
| S3 unwind | FP/r11 operands, caller frame setup, helper bodies by variant and a symbolized QA backtrace | Static and board |
| S4 fault handling | Counts and decoded fault, fixup and bug addresses versus helper intervals | Release gate awaiting both native verdicts |
| S5 atomics/barriers | Per-helper exclusive operations and barriers; inspect loop and caller context | Static return pending |
| S6 instrumentation | Effective FTRACE/KPROBES/KALLSYMS/stack-protector config; mcount, blacklist, symbol and canary implications for other configs | Config-specific review |
| S7 module ABI | Export names, Module.symvers CRCs; separate SERET-UL GCC compile and external module check | Clean package and module proof open |
| S8 code layout | Helper size distribution, distinct callers, source joins and hot-path site counts | Counts pending; board profiles required for latency |
| S9 veneers | LLD range-extension thunk count/bytes, section and linker-boundary placement | Release gate awaiting both native verdicts |
| S10 literals | PC-relative load targets against each helper's address extent; ADR and ambiguous ownership need review | Static return pending |
| S11 privileged/idle instructions | Decode all helper bodies; list sensitive opcodes and join caller PCs | Release gate awaiting both native verdicts |
| S12 modules | Compare per-module sizes, helpers, allocated relocations, PLT and ARM loader cases | Release gate awaiting both native verdicts |
| S13 debug coverage | DWARF file/line resolution at each helper entry and gap list | Static return pending |
| S14 profile bias | Attribute sampled helper PCs via matching build ID and recorded caller stack | Runtime time-share open |
| S15 timed vendor paths | Samsung/NVT/I²C/GPIO/SPI/CEC/tuner/display source joins, adjacent named delay/MMIO ops; inline register accesses require owner inspection | Static and device smoke |
| B runtime | Signed four-image rotation, boot, suspend, fast-boot, peripherals, signed scheduler/memory benchmarks, 4K, Home memory, oops symbolization, 24 h per treatment | Two signed treatment QBs required |

## Installed executable census and RELR

| PERF image | ARM loadable ELFs across platform + prd | Executable bytes | A32 bytes (estimate) | Unclassified ELFs | Platform entries + verified special nodes |
|---|---:|---:|---:|---:|---:|
| GCC 37564293 | 4,796 | 735,633,578 | 276,117,548 | 159 | 81,327 + 7 |
| Official 37736448 | 4,793 | 701,762,092 | 300,990,787 | 162 | 81,314 + 7 |
| Official 37777148 | 4,793 | 701,762,092 | 300,990,787 | 162 | 81,314 + 7 |

Official versus GCC changes executable bytes by −33,871,486 (−4.60%) and estimated A32 bytes by +24,873,239. The GCC image has a different Product/Base. Equal totals for the two Official images do not establish file identity. The platform extraction passed on all three; 37777148 lacks an independent board hash readback in this return. [Census](../../../artifacts/evidence/native-run-r0013i-read-a0Pmc0-0013f-HgSjf0-0013g-nkPaPY-20261126.txt)

**RELR estimate.** The two installed inventories cover 4,793 ELFs. The prior metadata join covered 374, leaving 4,419 unmatched. In the joined population, REL 2,201,840 B → estimated RELR 65,396 B, a saving of **2,136,444 B**. The largest RPM contribution was lightweight-web-engine-profile_tv at 1,194,020 B. The 0013r recount below covers all 4,793 platform/prd ELFs. The target-loader execution check remains open. This is relocation metadata size; per-page RAM and boot-time effects require measurement. [Coverage calculation](../../../artifacts/scripts/r0013f/review.py.txt)

### Retained perf kernel outlining side effects, 0013m

Both lane columns are observations from mo1VRK. The test-build override applies only to GBS and a pending test shelf. Board flash is HOLD.

| Gate | K1, versus K0 | K3, versus K2 |
|---|---|---|
| S1 critical paths | 0 direct critical section hits; 3,466 reachable helpers; 616 reachable functions with an indirect site | 0; 4,602; 664 |
| S2 critical LR stack saves | 5 sites; 8 B lower bound / 8,192 B | 8 sites; 8 B / 8,192 B |
| S3 unwind | FP; 120 sampled; 3,016 bodies with FP operand | FP; 120 sampled; 3,174 |
| S4 fault/bug tables | 219/1,387 entries, 0 helper hits, 210 references outside sized functions | 224/1,830; 0; 215 |
| S5 exclusive/barrier | 0 groups, 14 partial decodes | 0, 14 |
| S6 kernel config | FRAME_POINTER unwinder; function tracer, kprobes and kallsyms unset | Same |
| S7 exports | 10,348 equal names; CRC unverified | Same |
| S8 sites | 82,778; 77,115 input origins joined | 107,900; 94,685 joined |
| S9 thunks | PASS, 0 | PASS, 0 |
| S10 PC-relative literals | 0 observed; 14 partial decodes | 0; 14 |
| S11 system-state instructions | 119; 14 partial helper decodes | 165; 14 |
| S12 modules | 0/115 compared | 0/115 compared |
| S13 source-level oops diagnosis | 0/20,324 helper entries resolved to function and line | 0/26,020 |
| S14 profile weight | Board data required | Board data required |
| S15 driver timing | 3,732 NVT sites; timing unmeasured | 4,469 NVT sites; timing unmeasured |

S13 is a known debugging cost. Preserve the build ID and caller return address to recover the call site. Frame-walk behaviour needs target verification.

Official 37736448 → 37777148: rebuilt, same aggregate executable and A32 sizes. Whole platform.img and both partition digests differ. File comparison gives 447 changed platform records and 2 changed prd records; neither partition added or removed a path. AVControl T4 passed on the baseline and default lanes; the package lane remains REVIEW. The package worker was absent at capture. [Native output](../../../artifacts/evidence/native-run-r0013jk-static-mo1VRK-r0013l-gBXGor-20261126.txt)

### Official 37777148 platform/prd census, 27 November

| Check | PQnb3T result | Coverage or gate |
|---|---:|---|
| GCC replacement, fixed 27 | 23 CLANG_OBSERVED, 3 NO_ELF_OR_ABSENT, 1 COVERAGE_GAP | Published RPM payloads, 16,396 ELFs, 49 RPMs unavailable. A compiler marker establishes presence in the ELF. |
| C1 source scan | 0 hits | Inspected source scope |
| C2 ARMv7 interworking | 0 mapped Thumb ALU-to-PC candidates | 0 proven direct A32-to-candidate paths. Closed for this instruction class in decoded spans. 671,504,468 executable bytes have unknown mode. |
| C4 EHABI | 4,688 / 4,793 ELFs with nonempty `.ARM.exidx` | 105 without that section. Target unwind behaviour remains a runtime check. |
| C5 JIT/FFI | 55 candidates | Candidate count |
| C7 deprecated IT forms | 17,236 sites in 6,983,954 mapped Thumb bytes | Accepted by PM on shipped Official. Setup preserves incoming SCTLR.ITD. Board smoke with signed binaries supports ITD=0 in practice; the direct bit value and execution of each counted site were not measured. |
| C8 alignment | 212,289 candidates | Runtime check |
| RELR | 18,672,840 B REL → 656,012 B estimated packed RELR | **18,016,828 B** potential relocation-table saving across 4,793 ELFs |
| R7 loader | glibc 2.40-1.111.armv7l; both loader and libc identify as 2.40. libc-2.40.so defines GLIBC_ABI_DT_RELR. | **Ready for trial** with the shipped pair; the ABI version definition resides in libc. Verify actual packed ELF loads and dirty pages in R7. |
| AVControl T4 | 782 removed names; 4,793 ELFs checked, 0 errors, 0 undefined imports. 34 literal-only hits. | No shipped dynamic-symbol importer found. SCSClient template-name strings do not establish imports. Pure Thumb is the baseline. The LTO/visibility lane remains optional; runtime name construction and out-of-image consumers are outside the scan. |
| A32 roster and ownership | 480 ARM-predominant Official entries, 177 separate modules; 4,404 ambiguous/missing Official owners and 140 GCC. | /var/lib/rpm resolves under /opt. data.img is Samsung VDFS (VDFS2007 followed by mkfs.vdfs); partition 21 is 3,986,176 K. Query the installed RPM DB on the next matched Official visit. |

The original ROSTER sorts by **Official minus GCC estimated A32 bytes**. The unowned aggregate has 36,182,416 B of GCC executable sections, 631,491,596 B of Official executable sections, 18,596,572 B of GCC A32 and 261,056,385 B of Official A32. Its +242,459,813 B delta is sensitive to the different ownership coverage. The top-30 follow-up ranks named RPMs by **Official A32 bytes**. [PQnb3T evidence](../../../artifacts/evidence/native-run-r0013m-census-PQnb3T-20261127.txt)

The retained 37736448 Official uImage contains a v7 setup path that preserves SCTLR bit 7. The clear and set masks are `0x2120c302` and `0x10c03c7d`. Neither mask writes that bit. This result leaves its incoming value open. [Decoded masks and uImage hash](../../../artifacts/evidence/local-r0013r-o1-v7-setup.json)

### Package-level GCC and Official Thumb evidence, 0013t

| Named RPM | GCC estimated A32 B | Official estimated A32 B | Official − GCC A32 B | Interpretation |
|---|---:|---:|---:|---|
| org.tizen.tv-viewer | 228,084 | 4,693,514 | +4,465,430 | Executable sections 4,195,060 → 4,817,952 B (+622,892 B, +14.8%). GCC predominantly Thumb; LLVM predominantly A32. Historical spec resets CFLAGS, and all 549 sampled argv omit -mthumb. First matched-size trial target. |
| pkgmgr-extension | 7,105 | 204,554 | +197,449 | Thumb retest candidate; confirm current compile argv. |
| soc-ir-interface | 1,808 | 63,576 | +61,768 | Thumb retest candidate; confirm current compile argv. |
| bluetooth-impl-sec-oal | 25,007,569 | 25,006,506 | −1,063 | Mixed vendor package. The retained spec runs CMake/make and copies vendor DSOs, including libdualaudio.so and libbt-vendor_mtk.so. Explicit -marm is documented for a subset. Keep vendor/copied and source-linked paths separate. |
| vdfs | 5,073,113 | 4,622,699 | −450,414 | Vendor filesystem tools, source RPM vdfs-0004-3.src.rpm. Historical mkfs/tune/fsck/unpack.vdfs have GCC+Clang markers. Exact current source-link vs copied input is open until a matching spec install rule or compile/link record is available. |

The unknown-owner bucket holds 261,056,385 Official and 18,596,572 GCC A32 bytes. Exclude it from per-package deltas. The named-package deltas are observations across two Product/Base configurations. Quantify recoverable Thumb bytes using same-source, one-change builds. [jFI9ye roster and scans](../../../artifacts/evidence/native-run-r0013r-read-jFI9ye-20261127.txt) · [tv-viewer actual argv](../../../comms/codex_to_claude/0011b_reply.md) · [Historical vdfs path scan](../../../artifacts/evidence/native-run-r0005-argot-scan-gbs-20261118.txt)

For Official 37777148 the uImage digest is `f38df43d…`. Its clear/set masks are `0x2120c302` and `0x10c03c7d`. Upstream Clang 22.1.8 on thumbv8a defaults to unrestricted IT generation; an explicit `-mrestrict-it` enables the restriction. R7 will first measure tv-viewer (PIE canary), lightweight-web-engine-profile_tv (large DSO) and sys-tools (high relocation count); the 18,016,828 B estimate covers the relocation tables across the whole inventory. [Trial plan and board owner procedure](../../../comms/codex_to_claude/0013t_reply.md) · [LLVM ARM default](https://github.com/llvm/llvm-project/blob/llvmorg-22.1.8/llvm/lib/Target/ARM/ARMSubtarget.cpp#L256-L262)

### 27 November · Official perf kernel with clang-only outlining

| Retained GBS build | .text (B) | Outlined helper addresses | Image payload (B) | zImage (B) |
|---|---:|---:|---:|---:|
| K1 | 8,214,312 | 20,324 | 10,996,388 | 5,449,312 |
| jEMVH7 measured by dMztOS | 8,214,312 | 20,324 | 10,996,388 | 5,449,312 |

PM accepted the measured effect and the successful SERET-UL GCC step. The verifier recorded zero retained PERF compile lines. TEST-ONLY shelf 14507546 contains all 24 vdlinux inputs for the new Official and Custom clones. Their published module comparisons and helper counts await QB artifacts. [Evidence and S12 procedure](../../../comms/codex_to_claude/0013y_reply.md)

The DsfXAe Thumb-2 attempt failed to resolve two build requirements and compiled zero translation units. Its run adds no assembler sites to the earlier K4 evidence. [Dependency and provenance check](../../../comms/codex_to_claude/0013x_reply.md)
