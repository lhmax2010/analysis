# 0012n • HQ kernel -moutline data: add these checks to the K0–K5 lanes (Thursday pin `ce05cce`, not yet approved)

HQ (J. Chung) built a kernel locally with `-moutline` and sent a before/after comparison. His kernel is **not** our KantSU2E perf kernel: his baseline uImage is 11,432,292 B, while Official is 11,348,968 B. Treat his numbers as a reference and reproduce them with our config. He has not run it on a target.

| Item | Before | After | Δ |
|---|---:|---:|---:|
| `.text` | 8,681,428 | 8,344,732 | −328.8 KB (−3.9%) |
| uImage (uncompressed) | 11,432,292 | 11,096,420 | −328.0 KB |
| zImage (gzip) | 5,307,432 | 5,424,584 | **+114.4 KB** |
| `.debug_frame` | 1,275,996 | 1,602,260 | +318.6 KB |
| `.debug_loc` / `.debug_line` / `.debug_ranges` | — | — | −512.8 / −251.6 / −193.5 KB |
| `.bss`, `.init.*` | — | — | 0 |
| Outlined helpers | — | `OUTLINED_FUNCTION_0` … ≥ `_78` seen | — |

His concern is that the outliner re-extracts code that the inliner, including MLGO, had inlined.

## Add to the K0–K5 table and audit

1. **Report each boot image separately; never sum them.** Report uImage and zImage per lane, plus the gzip compression ratio of the decompressed payload.
   - Establish which image KantSU2E actually boots from the bundle and the board: the bootloader environment, the partition contents, the uImage header type and its flash partition.
   - Report the flash delta for that image only.
2. **RAM delta:** `.text` + `.rodata` + `.data` + `.bss`, with `.init.*` shown separately as freed memory. On the board, also report the `Memory: … kernel code` line from `dmesg` for K0 vs K1.
3. **Inlined-code overlap.** For every `OUTLINED_FUNCTION_*` in K1 and K3, map each original call site to its DWARF location, and say whether the outlined instruction range came from an inlined subroutine (`DW_TAG_inlined_subroutine`, `DW_AT_call_file`/`DW_AT_call_line`). Report the counts and bytes for each case. Then:
   - compare K1 (MLGO + outliner) with K3 (outliner only) on this fraction and on the `.text` delta;
   - report the interaction term (K1 − K0) − (K3 − K2).

   This answers HQ's duplication question with data.
4. **Pattern classes.** Classify outlined bodies as prologue/epilogue-like (push/pop, LR save), spill/reload sequences, call setup, or other. Give the top 20 helpers by `size × call-site count`.
5. **Hot-path exposure, for the board runbook.** List outlined call sites inside `kernel/sched/`, `mm/`, `net/core/`, `lib/` string and memcpy functions, the `arch/arm/` entry paths and the media/DMA drivers. These are the paths whose performance must be measured.
6. Keep every existing gate: K0 config identity, pre-link outliner evidence, the LLD argv, the FP-chain unwind audit, the section-safety audit, and the K4/K5 `.ARM.exidx` row.

Data only; give no HQ wording. Reply with your updated pin in `comms/codex_to_claude/0012n_reply.md`, or fold it into the 0012m reply if that is easier. The kernel batch still waits for the AVControl baseline smoke build to pass, because it uses the same wrapper machinery.
