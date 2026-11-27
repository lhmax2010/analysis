# 0013ad — Fix the package worker (0013o, never delivered) and fill the HQ tables

The 0013o prompt never reached you. Its evidence is not in `artifacts/evidence/` and there is no reply. This prompt includes its content and adds the HQ table work it was blocking.

**Evidence (archive under `artifacts/evidence/`):** `native-run-r0013e-pkg-Nr2wmG-20261127.txt`, sha256 `e9e41709e647614dbb6193f7cad68a67002ad6222549c56077fa825d140ec61a`. Inside it, the decoded table tar sha is `b8dc868c…`, with `pkg-plan.json`, `pkg-results.jsonl` and `pkg.status` = `pkg 0`.

## Part A — package worker failure (from 0013o)

**What happened.** Run `pm0013-pkg.Nr2wmG` ran 41 jobs: 25 N5, 10 N4, 4 R4-50 and 2 R5. The worker exited 0, but nothing was measured.

| Outcome | Count | Detail |
|---|---:|---|
| GBS failure in the baseline lane | 34 | Each failed within 1–7 minutes |
| Built, but treatment identical to baseline | 2 | `org.tizen.easysetup-daemon` and `iotivity`: `delivery:false`, `plugin_link_count 0` |
| Other errors | 5 | `rpm`: `too many values to unpack`; `libiri` and `vdsystem-lldb`: `SRPM bytes belong to a different source identity`; `org.tizen.ssoservice`: unsupported VCS; `libgcrypt`: correctly skipped |

**Failure signature:** `CCC_OVERRIDE_OPTIONS: +%{pm13_compile}`, then `clang: error: no such file or directory: '%{pm13_compile}'`. The RPM macro is not expanded where the override is exported, so CMake's compiler check fails at configure.

**Tasks:**
1. Confirm the same signature in all 34 failures, one line per package.
2. Fix the macro: define it in the lane build.conf or macros, or export an already-expanded value.
3. Fix the `rpm` unpack bug and the source-identity check for `libiri` and `vdsystem-lldb`.
4. Find out why the treatment flags never reached the link for easysetup-daemon and iotivity.
5. **Permanent canary rule.** Each batch first builds one package in both lanes and proves three things: the baseline succeeds, the treatment flag is delivered (argv), and the measured result differs. Only then does it queue the rest. If two consecutive jobs fail with the same signature, stop with `PKG_STOP same-signature`. Record this in `DECISIONS.md`.

## Part B — fill the HQ tables (20 Nov report, `reports/weekly/2026-11-20/`)

### B1 — refresh now from the existing image census (no build)

- **06 GCC / G++** (27 fixed packages). For each row, give the 37777148 status from PQnb3T: `CLANG_OBSERVED`, `NO_ELF_OR_ABSENT` or `COVERAGE_GAP`.
  - Where a matched `.text` exists, give the size: GCC image 37564293 vs Official 37777148, per package. Use the same ELF set and label any ELF-set difference.
  - Name the 3 absent packages and the 1 gap.
- **07 A32 files.** Re-rank the per-file list on Official **37777148**: 480 ARM-predominant entries plus 177 modules counted separately.
  - Give the estimated A32 bytes, owner RPM and cause class, reusing the 20 Nov classes.
  - Mark the files that are new or gone versus the 20 Nov list of 609.
  - Put tv-viewer, pkgmgr-extension and soc-ir-interface at the top of the Clang-without-`-mthumb` class.
  - Keep the unknown-owner bucket separate.

Output a rev3 markdown for each table in the 20 Nov format, with the changed cells only, plus a short changelog per table. The PM will update the live docs from it.

### B2 — after the worker canary passes

Run in this order. Same source, same dependencies; vary only the treatment; paired isolated armv7l GBS on Official 37777148; one change per pair.

1. **04, packages below `-O2`:** the 30 "to measure" rows, current level vs `-Os`. Do the top 10 by `.text` first. Keep libgcrypt's intended low-level files.
2. **05, LTO enablement:** the 76 "LTO on/off to be measured" rows. Do the top 10 by `.text` first. esg-api (+71.5% in LLVM) gets its analysis first.
3. **R7 RELR 3-package trial,** as already planned in 0013t.

For every pair, record:
- `.text` and file size;
- the effective argv, proving the treatment was delivered;
- build pass/fail;
- the ABI diff (SONAME, NEEDED, dynsym);
- the table row update.

Mark a runtime result "pending board" until the board tests run.

## Deliverable

1. The worker fix, and a re-pinned tier-2 command with the canary first, for PM review. It may run alongside the stooH5 enumeration and S12; keep the existing locks.
2. A hash-pinned, read-only B1 command, or the B1 tables themselves if your retained census data suffices.
3. Update `STATUS.md`: "HQ tables 04/05: no rows this week (harness failure); 06/07 refresh in progress".

No GitHub submission from the Native Server.
