# 0013b • Optimization tracks: restart them tonight in parallel with the kernel run (addendum to 0013a)

The 20 Nov plan (`reports/weekly/2026-11-20/01_Optimization_Plan_and_New_Observations.md` §3) scheduled the following for this week:

- N2 `-z text`;
- N4 LTO enablement;
- N5 `-O` level;
- GCC replacement (Doc 06);
- R1–R7.

None of them produced new data this week, because the kernel table, board visits, EROFS and the Thumb pilot took the native slots. The user wants them back on track, with whatever finishes by **Fri 27 Nov 10:00 CST** going into the weekly report.

The native server can run 4–8 jobs in parallel. Tonight the K0–K5 kernel run holds the shared build lock and has priority. Rules for this prompt:

- Use a **second lock domain (`pkg`)** with its own GBS root(s). The `pkg` lock must never take or wait on the kernel lock.
- At most 2 concurrent GBS package builds, all under `nice -n 19` and `ionice -c3`.
- A disk floor of 60 GB free, checked before each build. Stop cleanly below it.
- Inputs: the new Official QB **37777148** (Base 20261113.1, GBS config `config/gbs_vd_llvm_11.16_qb37777148.conf`, read-only) and its published RPMs.
- Product sources are unchanged. Every treatment goes through build.conf or macros in our own workspace copy only.

## Tier 1 — static scans of the 37777148 RPMs (no GBS, no lock)

Fold these into the 0013a no-lock command as **section E**, independent of B and C. They read RPM payloads, not the image, so they do not wait for the EROFS reader.

- **E1 GCC replacement census (Doc 06).**
  - Classify every loadable ELF by producer (`.comment`; DWARF `DW_AT_producer` where debuginfo exists) per source package: Clang only, GCC only, mixed, Rust, Go, none.
  - Compare with the 20 Nov figures: 101 packages with GCC ELFs, 27 with hard-coded `gcc`/`g++` fixed.
  - For each of the 27, state whether the fix CL is in this QB and whether the package is now all Clang.
  - List every package still GCC-built with its reason class: hard-coded and unfixed; GNU-only by evidence; prebuilt or vendor; not compiled. Give `.text` bytes for each.
- **E2 `-O` level baseline (Doc 04).** For the 34 packages, give the current `.text` and allocated bytes per ELF in 37777148. This is the "before" column. Give the effective level per CU wherever the producer string records it. Otherwise say "not recorded"; do not guess.
- **E3 LTO baseline (Doc 05).** For the 76 candidates not yet enabled: LTO ELF/all and `.text` in 37777148. Confirm that the four enabled by build.conf@14452507 are LTO-linked in this QB.
- **E4 TEXTREL (N2).** For every ELF with `DT_TEXTREL`/`DF_TEXTREL`: owner package, relocation count, and the text pages affected (as an upper bound on dirty pages).
- **E5 R2 export audit (prerequisite for `-fvisibility-inlines-hidden`).** For every DSO, the exported C++ inline/weak symbols that other ELFs in the image actually import, per provider → consumer. The output is the list of packages where R2 is safe without exclusions.
- **E6 R7 RELR.**
  - Count the `R_ARM_RELATIVE` relocations per ELF and estimate the file and dirty-page saving.
  - Check whether the Base glibc loader supports `DT_RELR` (version, and the symbol or tag in `ld.so`), and whether GNU ld 2.43 and lld 22 accept `-z pack-relative-relocs`.

Output: one line per summary result, with the full tables as a hash plus a zlib/base64 block, as in 0013a. Archive the full tables when the user relays them.

## Tier 2 — package A/B builds (GBS, `pkg` lock, max 2 parallel, niced)

Give a separate pinned command. Run the work in this order, largest `.text` first within each step. Stop at the disk floor or at Fri 09:30 CST, then print what finished. Unfinished items continue over the weekend.

1. **N5:** the remaining 30 of the 34 packages, lane A (published policy) vs lane B (+`-Os` only). Reuse the Step 8 lane definitions and fail closed if flag delivery is unproved, with CU and driver evidence as in Step 8. Leave libgcrypt's intentional low-level files unchanged.
2. **N4:** the top 10 LTO candidates by `.text`, LTO off vs on, with the ABI check against the GCC build (the 0013a T4 fallback: dynsym, SONAME, versions, `DT_NEEDED`). Removal from the exclusion list still needs the runtime and stability gate later. Here we report size and ABI only.
3. **R4-50 and R5** on the four R1 sample packages, using the staged recipes (`artifacts/ledger/r0012-experiment-recipes.json`), with the actual plugin argv.

R2, R3, R6 and the `-z text` strict-link trial stay gated, as recorded in the decisions.

## Weekly report

In `reports/weekly/2026-11-27/draft-data.md`, add an **Optimization tracks** table: N1 Thumb-2, N2, N3 kernel MLGO/-moutline, N4, N5, GCC replacement, R1–R7. For each give:

- what was measured this week, with the QB and evidence link;
- what was not measured this week;
- the next gate.

Fill it from the tier 1 and tier 2 outputs as they return.

Reply with the tier 1 command (merged into the 0013a command) and the tier 2 command in `comms/codex_to_claude/0013a_reply.md`. One reply covers both prompts. Commands first. Data only.
