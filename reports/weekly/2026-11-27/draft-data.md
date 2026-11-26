# KantSU2E PERF · Friday 27 November 2026

Evidence cutoff 25 November. One board. All kernel size and Thumb ELF size figures are bytes.

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
