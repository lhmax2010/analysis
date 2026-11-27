# 0013q • The 0013m static follow-up crashed: `NameError: route` in effects.py

Archive this evidence:

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0013m-static-NzBk1N-20261127.txt` | `54dc08637bd8ccc7694647b2e210c3b55a710db5aaeccd98bf00b7b8d36ee0b1` |

The `9e8886d` static run (`pm0013jk-static.NzBk1N`) reported every S1–S15 check for K1 and K3 as `REVIEW "name 'route' is not defined"`. `r0013jk/effects.py.txt` line 358 calls `route(a)` inside the S2 detail loop, but `route` is never defined. The resulting exception poisons every check. C7/C8 still say "no supported RPM DB". The receipt is `2282b69c…` (HOLD), and BOARD_FLASH is HOLD on S1, S4, S9, S11, S12 and S2.

## Fix

1. Define `route()` (the critical-root path for a caller) or remove the call. Also add a **NameError/syntax smoke test** that runs every S-function on a tiny fixture ELF before release, so one bad helper cannot mask all 15 checks. Isolate each S-check in its own try block so that one failure leaves the other results intact.
2. Re-pin the static command and keep the same inputs (mo1VRK lanes, f7f1148e lane receipt).
3. Do not touch `kernel.py` or the build/shelve path (`d428782`), which is about to run.

Reply in `comms/codex_to_claude/0013q_reply.md`, command first. Data only.
