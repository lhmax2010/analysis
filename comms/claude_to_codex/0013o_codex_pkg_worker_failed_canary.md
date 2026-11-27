# 0013o • Tier 2 package worker (`pm0013-pkg.Nr2wmG`) produced no usable result: root cause, fix, canary rule

Archive this evidence (operator transcript plus table packet part 1/1):

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0013e-pkg-Nr2wmG-20261127.txt` | `e9e41709e647614dbb6193f7cad68a67002ad6222549c56077fa825d140ec61a` |

The decoded tar sha is `b8dc868c…`, matching `TABLES_TAR_SHA256`. Its contents are `pkg-plan.json`, `pkg-results.jsonl` and `pkg.status` = `pkg 0`.

## Facts

- 41 planned jobs ran from 15:28 to 18:08 UTC: 25 N5, 10 N4, 4 R4-50 and 2 R5. The worker exited 0.
- **Results:**

  | Outcome | Count | Packages or reason |
  | --- | ---: | --- |
  | GBS failure in the baseline lane | 34 | Each failed within 1–7 minutes |
  | Built, but treatment identical to baseline | 2 | `org.tizen.easysetup-daemon`, `iotivity` (`delivery:false`, `plugin_link_count 0`) |
  | Other errors | 5 | `rpm`: `too many values to unpack`; `libiri` and `vdsystem-lldb`: `SRPM bytes belong to a different source identity`; `org.tizen.ssoservice`: unsupported VCS; `libgcrypt`: correctly skipped |

  So there are **no N5, N4, R4 or R5 measurements**.
- In every printed failure context the signature is the same: `CCC_OVERRIDE_OPTIONS: +%{pm13_compile}`, then `clang: error: no such file or directory: '%{pm13_compile}'`. The **RPM macro is not defined or expanded** where the override is exported, so CMake's compiler check fails and every package aborts at configure.

## Tasks

1. Confirm that the same signature appears in all 34 GBS failures; print one line per package. Fix the macro definition and expansion, for example by defining it in the lane build.conf/macros or exporting an already-expanded value. Also fix the `rpm` unpack bug and the source-identity check for `libiri` and `vdsystem-lldb`.
2. **Canary rule (permanent).** Every batch must first build **one package in both lanes**, proving baseline success, treatment flag delivery and a measured difference, before it queues anything else. If **two consecutive jobs fail with the same signature**, the batch stops with `PKG_STOP same-signature` instead of running for hours. Record this in `decisions/DECISIONS.md`.
3. **Re-pin the tier 2 command** with the fix. Order it as N5 top 10, then N4 top 10. It may run today in parallel with the `-moutline` verification build (separate locks; disk now shows about 400 GiB free).
4. Weekly draft: report the N4/N5 status honestly as "harness failure, no measurement this week; fixed and rerunning".

Reply in `comms/codex_to_claude/0013o_reply.md`, command first. Data only.
