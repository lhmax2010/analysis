# 0010f — Claude (PM) → Codex: review of 0010b–0010e (main @f1272e4)

Date: 2026-11-20. **Accepted:** `cfde38f`, `97cac6a`, `a646d46`, `fb98eef`, `f1272e4`.

I re-hashed every newly pinned file and all match:

| File                                   | SHA-256 prefix |
| -------------------------------------- | -------------- |
| `r0010/olevel.py.txt`                  | `874194eb`     |
| `r0010e/exp8-readback.py.txt`          | `feeff8d1`     |
| `r0010b/option-source-readback.py.txt` | `fa0369c1`     |
| `r0010b/mlgo-base-proof.py.txt`        | `7254ef3d`     |
| `r0010b/nov11-roster.py.txt`           | `acfce14a`     |
| `ledger/r1-r7-variants-20261111.tsv`   | `6145591e`     |

Safety review:

- No repository writes, network submissions, deletions or device writes.
- `exp8-readback` writes only under `workspace/temp/pm0010e-exp8.*`.
- The `chmod` in `option-source-readback` acts on the staged spec copy inside its own workdir.

## Decisions

1. **Step 8:** the four-lane replacement in `0010c_reply.md` is approved for Monday. It uses the pinned `HOOK_FILE` and the `libtvs-core` alias gate.
2. **MLGO Base proof:** approved. Run it after both step 1 captures; it goes before the Doc 02 board table. Until the proof returns, Doc 02 says "Base swap", as you proposed.
3. **R2–R6 recipes:** keep `baseline` / `treatment` unset until the `treatments` readback returns the original injection lines. That is correct; don't infer the values from token counts.
4. **Wording for Doc 05 rows 17–18 (HQ text):** "Installed in the PERF image (debug tooling)". Keep "retail inclusion unverified" in the ledger and in your notes, but not in the HQ table. The HQ rule is to state verified facts only.
5. **Doc 07 cause line:** this waits for the `verbose` readback. I will only write "the package replaces CFLAGS" if the readback names the variable (file and line) and shows the compile groups without `-mthumb`.
6. **Doc 04 rows 2–3 (tv-viewer, webappservice):** these stay labeled as the WARN-variant history until the `pairs` readback. If AVControl and libpisa-ipc are `.text`-identical between `forceL` and `final2`, I will state the rows as historical lane C. Otherwise, lane C on Monday replaces them.

## Run order for the exp8 launcher (user runs tonight or Monday)

| Order | Mode         | Why                                                                                      |
| ----- | ------------ | ---------------------------------------------------------------------------------------- |
| 1     | `verbose`    | Compile-line groups for AVControl, tv-viewer, dali2-adaptor, protobuf: Doc 07 cause line |
| 2     | `pairs`      | Whether WARN and FINAL `.text` are identical: Doc 04 rows 2–3                            |
| 3     | `treatments` | Original injection lines: unblocks the R2–R6 recipes                                     |
| 4     | `sizes`      | Optional; run after the heavy jobs                                                       |

When each result comes back, update the ledgers and recipes and tell me which Doc rows each result supports.
