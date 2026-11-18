# Provenance of the earlier 106 ARM-predominant files

| Evidence | Date and scope | What it establishes |
|---|---|---|
| Operator correction retained in claude_mem/LOG.md lines 333 and 335 | 2026-11-17, handover recollection | The previous analysis used a full-code comparison before Thumb was proposed. Original file roster and underlying artifacts were already missing at handover. |
| [PM handover 0002](../../comms/claude_to_codex/0002_pm_review_decisions_and_plan.md) | 2026-11-17, D-019 | Earlier account records are unavailable. This is a secondary reference to the count. |
| Round 0004 HQ question supplied verbatim by the user | Current round | Earliest exact wording recovered in the current interaction. The question repeats 106 and the argot PSS, but contains no original report title, date, image ID, scan threshold or roster. |
| [November 11-image optimization report](../historical-reports/optimization-analysis-part-01.md) | Report dated 2026-11-12, QB 37518055, Base 20261105.1, 4,778 shared ELF paths | Identifies its image and sample. It documents mapping-symbol size effects and kernel-only MLGO. No verified link from this report to the 106 ARM roster or the exact HQ sentence was found. |
| HQ Clang decision tables, 2026-11-13 edition, row 46 | EFL compiler classification | Its “2 of 106 ELF built by GCC” describes EFL compiler markers, a different measure from ARM mode. |

Checked the retained weekly reports for November 6, November 9–14 and the November 14–16 handover, compiler/option/LTO reports, the saved HQ tables and handover records. The original report name, send date, image and classification method remain **unverified**. The preceding user clarification establishes that an analysis took place. Its exact method cannot be inferred from the current reproduction.

The user’s forthcoming full-image scan covers 2,342 installed RPMs. Keep mapping-symbol and condition-field heuristic results labelled with image, method and confidence. Record validation against mapped examples, CPU/endian assumptions, thresholds, handling of mixed/executable-data regions and ambiguous cases. Use the flagged paths to queue source and build-log attribution. The earlier mapping and dynsym tables remain historical diagnostics.
