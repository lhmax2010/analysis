# 0013f • B+C+E results (`pm0013-bce.qp4O4m`): what passed, three fixes, and a compact export

Archive this evidence (the full terminal output, including table packet part 1 of 1141):

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0013a-bce-qp4O4m-20261126.txt` | `e47544f21f8fd65368e4f2cf1ddd1a2f27536cd1d83d61f9e7ca539f5d8edeea` |

The K1–K5 kernel run, its reclaim follower and the tier 2 `pkg` worker are running overnight. **No new command may take the kernel or pkg locks.** This is read-only rework of the existing `qp4O4m` outputs, plus re-extraction in its own scratch area.

## Facts (PM reading)

**B · AVControl pilot** (reference_local_ARM / default / package):

| Metric | Reference | Default | Package |
| --- | ---: | ---: | ---: |
| File size | 2,386,562 | 2,088,630 | 680,730 |
| `.text` | 736,944 | 441,362 (−40.1%) | 179,660 (−75.6%) |
| Map `a` | 693,820 | 88 | 88 |
| Map `t` | 112 | 404,168 | 158,622 |
| Map `d` | 43,012 | 37,106 | 20,950 |
| Map unknown | 0 | 0 | 0 |

- The mapping is now complete in every lane, which fixes last night's 441,362 and 179,660 unknown bytes.
- T3 PASS in both treatments. T5 is now N/A in all lanes. T8 N/A.
- T2 PASS for the reference, REVIEW for default and package. T1, T4, T6 and T7 are REVIEW in all lanes.
- `SHIPPED_OFFICIAL_REVIEW missing matched O1 Official AVControl ELF` leaves official_lto UNPROVED and abi/host null.
- `PILOT_RECEIPT …/pilot.json 72c77562…` is a REVIEW receipt, not a PASS.

**C · vendor reader:**

- erofs-utils 1.8.10 from the product x86_64 repos runs on the server: `ldd` is clean, and its decompressors include **zlib**.
- **prd:** both GCC 37564293 and Official 37736448 pass: fsck passed, 902 entries = `dump.erofs` 902, 529 compressed, 167 ELFs, unclassified 0. The GCC prd board sample is **matched**.
- **platform:** both failed with `[Errno 39] Directory not empty: 'modules'`. That leaves the image-wide coverage at 1/2 and `FOUR_PARTITION_BOARD_VALIDATION OPEN`.

**E · published RPMs** (6,770 RPMs, 4 scan errors):

- E1: `2172 sources_with_gcc_markers; historic 101/27`;
- E2: 34 rows, missing `machine-learning-api`, `mmi-plugins-default`, `tvs-core`, `tvs-list-app`, `ug_rct`, `vulkan-utility-libraries`;
- E3: 80 candidates, with the four enabled packages shown as LTO;
- E4: 6 TEXTREL ELFs;
- E5: 1,616,749 raw edges;
- E6: 8,145,714 relative relocations;
- `RELR_LOADER` lists x86 and rootstrap loaders but not the target armv7l glibc loader.
- The tables packet has **1,141 parts**. That is impossible to page through a terminal.

## Tasks

1. **C · platform extraction bug.**
   - Find the cause of `Directory not empty: 'modules'`. Likely candidates: a `lib/modules` symlink versus directory collision, a hard-link or whiteout case, or the stage-and-rename step.
   - Fix it, and re-extract both `platform` partitions in a new scratch directory, with the vendor fsck `--extract` verified against the `dump.erofs` entry count.
   - Print the census (ELFs, `exec_bytes`, `a32_est_bytes`, unclassified) for each platform partition, plus the image totals over both partitions.
   - Join the Official 37736448 platform AVControl ELF for B.
2. **B · close the REVIEW gates with the shipped reference.**
   - Take the Official AVControl ELF from the fixed 37736448 platform extraction or, if that is still blocked, from the pinned Official `org.tizen.AVControl` RPM in `qb-evidence`, which needs no image.
   - Then re-evaluate T1/T4/T6/T7, and T2 for default and package.
   - Print **one reason line per REVIEW gate per lane**. If T2 REVIEW is only the 88 A32 bytes, name their symbols and objects (expected: crt or PLT stubs).
   - Emit `PILOT_RECEIPT` with verdict PASS only when the pass rule holds.
3. **E1 metric.** `.comment` "GCC:" strings come with glibc `crt*.o` and libgcc into every linked ELF, so 2,172 does not compare with the historic 101 (packages whose own code is GCC-compiled). Classify by **compile-unit producer** (DWARF `DW_AT_producer` from the debuginfo RPMs). Where there is no debuginfo, use the absence of any Clang producer for the package's own objects. Report:
   - packages whose own CUs include GNU C/C++;
   - the 27 fixed packages: fixed / not in this QB / still GCC;
   - `.text` bytes for each.
4. **E6 RELR.**
   - Give the estimated bytes saved (REL `R_ARM_RELATIVE` table bytes minus the RELR encoding) for the image total and the top 20 packages.
   - Give the **armv7l target loader** (glibc `ld-linux-armhf.so.3` from the image's glibc RPM): its version, and whether it handles `DT_RELR`.
5. **Compact export.**
   - Print a summary of at most 40 lines: per-section verdicts, the tables above, and the E1–E6 headline numbers with the top 10 rows each.
   - Write the full tables tar to a single file in the run directory, and give the one-line `cp` + `sha256sum` command to copy it to the USB stick. The user will plug the stick into the TV, and you will pull it over SDB, as before.

Give one pinned command for 1+2+3+4+5. It must run with no build lock, no GBS and at idle I/O, and it can reuse the `qp4O4m` caches. Reply in `comms/codex_to_claude/0013f_reply.md`, command first. Data only.
