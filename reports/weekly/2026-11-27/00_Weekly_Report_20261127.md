# Tizen LLVM Adaptation — Weekly Report (27 Nov 2026)

Nov 27, 2026 · @Hao

## Summary

LLVM already makes the KantSU2E image smaller than GCC: executable code −33.9 MB (−4.6%), PERF kernel `.text` −0.80 MB (Official) / −1.05 MB (Custom). This week added kernel `-moutline` (−4.1% `.text`, TEST-ONLY QBs building) and Thumb-2 analysis (−40% `.text` on AVControl). The Thumb-2 kernel is blocked by Samsung VDLinux assembly; the fix is in progress.

| Method | Result this week | Verification level | Next step |
| --- | --- | --- | --- |
| GCC → LLVM replacement | Executable bytes −33,871,486 B (−4.60%); 23 of 27 hard-coded GCC packages now Clang-built | Full image census (4,793 ELFs); board MemAvailable and gzip/xz on GCC vs LLVM | Close 3 absent + 1 coverage gap; matched-board rerun |
| Kernel MLGO | Release advisors cut PERF `.text` 9,859,176 → 8,564,600 B (−13.1%); Custom model −248,768 B more than Official | Local GBS builds + shipped QB kernels | Board performance on the 4 new QBs |
| Kernel `-moutline` (HQ) | `.text` −350,288 B (−4.09%) on top of MLGO; zImage +2.31% | Build-level + 11 static side-effect checks; source proven equal to the QB CL | S12 module check, then board test of 4 images |
| Thumb-2 (user space) | AVControl `.text` 736,944 → 441,362 B (−40.1%) | File measurement + static compatibility gates C1/C2/C4/C7 | Thumb-2 image QB; board P1–P5 |
| Thumb-2 (kernel) | Not built: ARM-only instructions in VDLinux assembly | Assembler errors confirmed; full inventory build running | Patch with ARM()/THUMB() variants, then QB |
| RELR (R7) | Estimated relocation-table saving 18,016,828 B across 4,793 ELFs; glibc 2.40 supports it | Static estimate; loader support confirmed | 3-package trial after package-worker fix |
| LTO non-PIC fallback (HQ PIC design) | IR path: patch in both LLVM toolchains, under review. Native path (GNU ld / no-LTO consumers): design and GNU ld 2.43 fixture done 20 Nov; implementation not started | Fixture: default link accepts an absolute reference in code and emits TEXTREL; -z text rejects it | Start native path: image TEXTREL scan, FatLTO-route fixture, -z text trial |
| −O level (N5), LTO (N4), R1–R6 | No new measurement this week | — | Fix the package-build worker, then fill the HQ tables (section 5) |

## 1. GCC → LLVM replacement

The LLVM image is smaller in both kernel and user space; board memory and speed are within noise except xz, which runs 0.10 s slower. Images compared: GCC 37564293, Official MLGO 37736448 (LLVM Base 20261113.1), Custom MLGO 37736427 (LLVM Base 20261118.1). All use kernel source CL 14293732.

**Shipped PERF kernel (bytes)**

| Item | GCC | Official MLGO | Custom MLGO | Official − GCC | Custom − GCC |
| --- | --: | --: | --: | --: | --: |
| Text | 9,364,188 | 8,564,632 | 8,315,864 | −799,556 | −1,048,324 |
| Total (uImage − header) | 12,218,544 | 11,348,904 | 11,085,176 | −869,640 | −1,133,368 |
| zImage | 5,664,248 | 5,326,504 | 5,222,032 | −337,744 | −442,216 |
| tztv-kernel-perf RPM | 20,018,029 | 19,345,448 | 19,160,700 | −672,581 | −857,329 |

**Installed image (platform + prd)**

| Image | ARM ELFs | Executable bytes | Estimated A32 bytes |
| --- | --: | --: | --: |
| GCC 37564293 | 4,796 | 735,633,578 | 276,117,548 |
| Official 37777148 | 4,793 | 701,762,092 (−4.60%) | 300,990,787 |

- **Hard-coded GCC packages (27 fixed):** 23 now Clang-built, 3 have no ELF or are absent, 1 coverage gap.
- **Board, GCC vs Custom (one board, warm reboot, Home in focus):** MemAvailable median 1,088,000 vs 1,086,360 KiB (+1,640 KiB GCC, inside sample spread). gzip 0.42 vs 0.41 s; xz 0.83 vs 0.93 s. Product and OS libraries also differ between these images, so this is a whole-image comparison, not a compiler-only one.
- **A32 growth:** Official carries +24.9 MB more ARM-mode code than GCC. The largest named cause is tv-viewer (+4.47 MB): its spec resets CFLAGS and drops `-mthumb`. This is the first Thumb-2 target (section 3).

## 2. Kernel: MLGO and `-moutline` (HQ request)

`-moutline` cuts PERF kernel `.text` by a further 4.09% on top of MLGO, and no static side-effect check found a blocking issue. The trade-off is a 2.3% larger compressed zImage. Board verification of runtime effects starts next week on four new QBs.

**Size, local GBS builds (Official base, bytes)**

| Lane | MLGO | `-moutline` | `.text` | Δ `.text` | zImage | Δ zImage | Outlined helpers |
| --- | --- | --- | --: | --: | --: | --: | --: |
| K2 | Off | Off | 9,859,176 | baseline | 5,916,376 | baseline | 0 |
| K3 | Off | On | 9,369,924 | −489,252 (−4.96%) | 6,068,112 | +2.56% | 26,020 |
| K0 | On | Off | 8,564,600 | baseline | 5,326,464 | baseline | 0 |
| K1 | On | On | 8,214,312 | −350,288 (−4.09%) | 5,449,312 | +2.31% | 20,324 |

MLGO is still worth keeping with `-moutline`: K1 (both) is 1,155,612 B smaller than K3 (outline only).

**Side effects, static verification (K1 vs K0)**

| Check | Result | Verdict |
| --- | --- | --- |
| S1 boot-critical sections (entry, vectors, idmap, MMU-off) | 0 helpers placed or called there | Pass |
| S2 stack / LR | 5 LR-save sites on critical paths; at least 8 B extra stack vs 8 KiB | Pass, worst-case nesting checked on board |
| S4 fault / bug tables | 0 table entries point into helpers | Pass |
| S5 atomics / barriers | 0 exclusive or barrier sequences split into helpers | Pass |
| S9 linker veneers | 0 range-extension thunks | Pass |
| S10 PC-relative literals | 0 helpers reach a literal outside themselves | Pass |
| S11 privileged instructions | 119 system-register instructions in helpers; residual cases are current-task TPIDRURO reads | Pass after review |
| S13 crash diagnosis | Helper entries have no source line (0/20,324) | Known cost: an oops inside a helper needs the caller address |
| S12 modules (115) | Built from the QBs below | Pending, gate before flash |

**Build and QBs**

- GCC (used for the SERET-UL step) rejects `-moutline`, so the flag is passed to Clang only.
- A TEST-ONLY CL, 14507546 (MLGO shelf 14427407 plus the clang-only flag; never submitted), was built locally and matched K1 exactly: `.text` 8,214,312 B, 20,324 helpers, Image 10,996,388 B.
- All 7 kernel files outside the user's workspace were proven byte-identical between the measured build and the CL (`SOURCE_EQUIV PASS`).
- Four QBs, building now:

|  | Official (Base 20261113.1) | Custom (Base 20261118.1) |
| --- | --- | --- |
| MLGO only (14427407) | 37836579 | 37836654 |
| MLGO + `-moutline` (14507546) | 37836693 | 37836727 |

## 3. Thumb-2

In user space, Thumb-2 cuts AVControl code by 40% and the static compatibility checks found no blocker. Performance and memory are not measured yet; they need a Thumb-2 image on the board. The kernel cannot build in Thumb-2 yet because of ARM-only assembly in Samsung VDLinux code.

**Thumb-2 vs ARM32, AVControl (bytes, file measurement)**

| Item | ARM32 baseline | Thumb-2 | Change |
| --- | --: | --: | --: |
| `.text` | 736,944 | 441,362 | −295,582 (−40.1%) |
| Allocated sections | 1,055,461 | 758,644 | −296,817 |
| Share of code in ARM mode | 99.98% | 0.95% | — |

**Compatibility, static checks on Official 37777148 (4,793 ELFs)**

| Check | Result | Status |
| --- | --- | --- |
| C1 ARM-only source | 0 hits in scanned source | Pass |
| C2 ARM↔Thumb interworking | 0 unsafe Thumb ALU-to-PC returns | Pass for decoded code |
| C3 ABI (AVControl) | 0 undefined imports across 4,793 ELFs after the change | Pass |
| C4 unwind tables | 4,688 / 4,793 ELFs have EHABI tables | Crash backtrace to check on board |
| C5 JIT / FFI | 55 candidates (web engine, .NET, FFI) | Owner review |
| C7 ARMv8 IT blocks | 17,236 sites; kernel keeps IT enabled (ITD=0) | Accepted |
| C8 alignment | 212,289 candidate instructions | Runtime check on board |

**Performance and memory (board, pending the Thumb-2 QB):** playback and navigation profiles, microbenchmarks (gzip, xz, zstd, OpenSSL, JPEG/PNG, memcpy; accept ≤ 3% median regression), cold boot and app launch ×5, 4K playback, Home-idle MemAvailable and PSS, 24 h stability. A regressing package can opt out with `-marm`.

**Largest opportunity:** tv-viewer is 4.69 MB of ARM-mode code in the LLVM image (GCC: 0.23 MB), because its spec resets CFLAGS and loses `-mthumb`. It is the first matched-size trial.

**Kernel Thumb-2: issues found, fix in progress.** Samsung VDLinux additions use instruction forms that exist only in ARM mode: a full-register store in `backtrace-clang.S`, an SP shift and an exception-return load in the stack-overflow handlers of `entry-armv.S`. The build that lists every such error is running now. The fix adds Thumb variants, as mainline Linux does, and must keep the ARM kernel byte-identical. Results will be reported with the Thumb-2 kernel image.

## 4. Other optimisation methods

RELR is the largest new opportunity found this week (an estimated 18.0 MB of relocation tables). The package-level trials for the other methods produced no measurement: the package-build worker failed (section 5). The fix goes to Codex today.

| Method | Status | Result / evidence so far | Next gate |
| --- | --- | --- | --- |
| R7 RELR packed relocations | Ready for trial | 18,672,840 B REL → 656,012 B estimated RELR: 18,016,828 B saving across 4,793 ELFs. glibc 2.40 in the image supports RELR. | Build tv-viewer, lightweight-web-engine-profile\_tv and sys-tools with lld; measure size, load and dirty pages |
| N5 optimisation level (`-Os` / `-Oz`) | Planned | 4-package evidence from earlier weeks; 30 packages remain | Per-ELF baseline, then ranked package builds |
| N4 LTO enablement | Planned | 76 candidate packages + 4 already enabled | Top 10 by size: A/B size, ABI, stability |
| LTO non-PIC fallback, IR path (Source1005) | In independent review | Patch source identical in Official and Custom SRPMs | Reviewer findings |
| LTO non-PIC fallback, native path | Not started (design only) | Design 20 Nov: PIC producers, -z text at final shared/PIE link, shipped-image TEXTREL audit, external-input rule. Tizen GNU ld 2.43 fixture: ABS32 in .text links with TEXTREL by default, rejected under -z text; current build.conf sets no -z text | 1) TEXTREL / read-only relocation scan of 37777148 (4,793 ELFs); 2) fixture on real FatLTO routes; 3) -z text trial on 8 RPMs + gst-ffmpeg + CAPI; 4) TLS consumer checks |
| R1 forced options | No new run | November recipes on 4 packages | Matched pair + signed-char board check |
| R2 inline visibility | No new run | — | Find installed consumers of weak C++ exports |
| R3 ThinLTO | No new run | — | Timing / size vs full LTO |
| R4 inline threshold | No new run | — | Threshold-50 `.text` per package |
| R5 machine outliner (user space) | No new run | Kernel result in section 2 | 4-package trial |
| R6 lld / ICF | No new run | — | Linker-only A/B, then safe ICF |
| N2 strict text relocations | No new run | — | Static census, then strict-link trial |

## 5. HQ tables (from the 20 Nov report)

The two package tables (−O level and LTO) got no new rows this week: the package trial ran 41 jobs, but 34 failed at configure because a build macro was not expanded, so nothing was measured. The GCC and A32 tables can be refreshed now from this week's image census, without any build.

| HQ table | Filled so far | Still open | This week |
| --- | --- | --- | --- |
| MLGO kernel comparison | Kernel size, Official vs Custom; matched QB pair defined | Board performance and memory on a matched pair | Extended with `-moutline` (section 2); 4 same-day QBs building |
| Packages below `-O2` (34) | 4 measured: `.text` −20% to −76% at `-Os` | 30 rows "to measure" | Trial failed (macro not expanded); no new rows |
| LTO enablement (80) | 4 enabled: −0.3% to −11.3% `.text` | 76 rows "LTO on/off to be measured" | Same failure; no new rows |
| GCC / G++ packages (27 fixed) | 15 matched size pairs | Runtime tests; sizes for the rest | 37777148 census: 23 now Clang-built, 3 absent, 1 coverage gap; table update pending |
| A32 files (609, top 211) | Cause classes and fixes | Effect of the `-mthumb` fix | 37777148: 480 ARM-predominant files; tv-viewer +4.47 MB A32 vs GCC; table update pending |

## 6. Next week

The priority is board results for kernel `-moutline` on the four new QBs, followed by the Thumb-2 kernel fix.

1. **Kernel `-moutline`:** module check (S12) on the 4 QBs, then flash. Board tests on all 4 images: boot time, Home-idle memory, benchmarks, 4K playback, suspend/resume, crash backtrace, and 24 h stability.
2. **Thumb-2 kernel:** complete the error list, patch the VDLinux assembly, prove the ARM kernel is unchanged, then build a Thumb-2 kernel QB.
3. **Thumb-2 user space:** tv-viewer trial, Thumb-2 image QB, then the P1–P5 performance, memory and stability checks on the board.
4. **Package trials:** once the build-worker fix lands, run the RELR 3-package trial, then the `-O` level and LTO rankings.
5. **LTO native path:** start implementation of the HQ PIC design, beginning with the shipped-image TEXTREL scan (no build needed), then the FatLTO-route fixture and the -z text package trial.
6. **HQ tables:** refresh the GCC / G++ and A32 tables from the 37777148 census now; after the worker fix, fill the 30 −O level rows and the 76 LTO on/off rows, top 10 of each first.

**Risks**

- QB build artifacts expire after 2–4 days. Each new QB's RPMs are saved as soon as it finishes; the S12 baselines are already saved (130 RPMs each).
- There is one board, so the 4-image `-moutline` test and the Thumb-2 test run one after another.
- xz ran 0.10 s (12%) slower on the LLVM image than on GCC. Product and library differences may explain it; it will be rechecked on matched images.
