# 0013l • Full image census is in: follow-ups for the report, the Thumb-2 gates and the pilot

Archive this evidence (0013i command 1, which includes 0013f run `HgSjf0` and 0013g run `nkPaPY`):

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0013i-read-a0Pmc0-0013f-HgSjf0-0013g-nkPaPY-20261126.txt` | `7e5c2d72b638136c47ed5b0bef1e27fc2a152ab921bb8db4658d4dce0078c108` |

Comes after 0013jk part 1. Read-only: no build lock, no GBS, idle I/O.

## Facts (PM reading)

- **Kernel K1/K3 FINISHED, ARGV PASS:** K1 `.text` −350,288 vs K0; K3 −489,252 vs K2. Helpers: 20,324 (316,380 B) and 26,020 (411,200 B). zImage +2.31% / +2.56%. No rebuild was needed.
- **The Thumb-2 kernel is blocked by assembly:**
  - `arch/arm/lib/backtrace-clang.S:19` `stmia r0, {r0 - r15}` (VDLinux-modified file);
  - `arch/arm/kernel/entry-armv.S:375` in the `check_overflow` macro: `mov r8, sp, lsr #12` (ARM-only).
  - The replay covered only 1 of 84 commands (`ASM_SCOPE 1 84 1`), so the list is partial.
- **Platform extraction now passes on all three images** (81,314 + 7 verified special files = 81,321). Image totals:

  | Image | ELFs | Exec bytes | A32 estimate |
  | --- | ---: | ---: | ---: |
  | GCC 37564293 | 4,796 | 735,633,578 | 276,117,548 |
  | Official 37736448 | 4,793 | 701,762,092 | 300,990,787 |
  | Official 37777148 | 4,793 | 701,762,092 | 300,990,787 |

  So LLVM is **−33.9 MB (−4.60%)** of executable bytes vs GCC, and **+24.9 MB of A32** (the Thumb-2 opportunity).
- **E6 RELR (full coverage):** REL 2,201,840 → RELR 65,396, so **2,136,444 B** of metadata saved. The top contributor is `lightweight-web-engine-profile_tv` at 1,194,020. `ARM_LOADER` is `/usr/lib/ld-linux.so.3`, sha `aec21fb5…`; its glibc join is UNPROVED.
- **E1:** only 5.26% of ELFs carry producer information (781 of 14,852), so no conclusion can be drawn about GCC-built packages.
- **0013g static:**
  - cohort 609 → 219 source packages;
  - C2: 74,405 return sites, 2,931 caller rows;
  - C4: 395 ELFs (384 EHABI, 317 unwind imports);
  - C5: chromium-efl only;
  - **GAP 4,510 rows, 4,398 with owner "?"**;
  - verdict OWNER_REVIEW.
- **Pilot still REVIEW:** T4 "empty dynsym" in all lanes; T6 cannot resolve `/usr/lib/pulseaudio/libpulsecommon-15.0.so`; the T2 spans match no CRT and are not in the PLT.

## Tasks

1. **37777148 = 37736448?** The platform census is byte-identical (entries, compressed count, exec bytes, A32 estimate), but the Product versions differ (20261125.1 vs 20261123.2).
   - Prove it either way: platform.img sha, partition sha, and the count of per-file sha differences between the two extracted trees.
   - If they are identical, say why: no rebuilt payload, or the same image published twice.
2. **A32 census comparison for the report and the Thumb-2 QB.** Per package: GCC vs Official A32 estimate and exec bytes, top 30 by A32 increase, and the new Thumb-2 target roster from the image, replacing the historical 609. Separate the explicit `-marm`, vendor/prebuilt, kernel-module and JIT rows.
3. **C2 re-classification with ARMv7 interworking semantics.**
   - On ArchVersion ≥ 7, ARM-state `mov pc, rX` and ALU-to-PC writes use ALUWritePC, which interworks. `ldm`/`pop {…, pc}`/`ldr pc` use LoadWritePC, which interworks. Only **Thumb-state** ALU writes to PC (BranchWritePC) do not.
   - Confirm the CPU architecture from the archived board `/proc/cpuinfo` (O1/C1/G1 evidence).
   - Then reduce C2 to the sites that really do not interwork (Thumb-state `mov pc`/`add pc` reachable from ARM callers), and print the remaining count.
4. **GAP ownership.** Fix the join that leaves 4,398 rows with owner "?". Use the extracted platform tree's RPM database (`installed.tsv`) and the file lists of the published RPMs. Then re-run the C1/C2/C4/C5 summary.
5. **ARM loader and DT_RELR.** Identify the glibc RPM and version that ships `/usr/lib/ld-linux.so.3`, and check whether `ld.so` carries the `GLIBC_ABI_DT_RELR` version and handles `DT_RELR` (glibc ≥ 2.36). Give a YES/NO with evidence.
6. **E1 replacement method.** Per ELF, classify `.comment`:
   - contains a Clang/LLVM string;
   - only `GCC:` strings (CRT included);
   - none.

   Report the source packages whose ELFs have **no Clang string at all**, as the GCC-built or prebuilt candidates. Report the fixed-27 status with this method.
7. **Close or rescope the AVControl pilot.**
   - T4: if the Official executable's dynsym is also empty, T4 = N/A (an executable with no exports) with evidence.
   - T6: resolve libraries with the ELF's `DT_RUNPATH`/`RPATH` and the platform ld config.
   - T2: map the 88 B spans through the lane's linker map (`-Wl,-Map`) or the object symbol tables in the build root.
   - T1/T7: is Official AVControl LTO-linked? Decide this from the Official ELF now available (LTO markers, single-CU signature).
   - Then emit the final verdict per gate.

   If T1/T7 cannot be proved without the Official build log, say so, and treat the pilot as **size-qualified, with production acceptance deferred to the Thumb-2 QB board gates**.
8. **USB export.** Give the copy commands for both archives, `pm0013f-review.HgSjf0/tables.tar.gz` (`09d2b2dd…`) and `pm0013g-static.nkPaPY/static-tables.tar.gz` (`0915605b…`), and pull them from the TV over SDB once the user plugs in the stick.

Give one pinned read-only command for 1–7, printing at most 40 lines. Add these to `reports/weekly/2026-11-27/draft-data.md`:

- the image census table (GCC vs Official) and the RELR result;
- the kernel K0–K3 table;
- the Thumb-2 kernel blocker.

Reply in `comms/codex_to_claude/0013l_reply.md`, command first. Data only.
