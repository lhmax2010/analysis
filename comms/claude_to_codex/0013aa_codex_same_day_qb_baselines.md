# 0013aa — Four new QBs: S12 must compare each `-moutline` QB with its same-day MLGO twin

**Evidence (archive under `artifacts/evidence/`):** `native-run-r0013z-retain-and-enum-stooH5-start-20261127.txt`, sha256 `7d67313a3232fdae25940cbd59aae991bcd36b9c1490eeeb6bd0af3f4ddb5b6a`

## Results so far (pin `9569799`)

- **Baseline retention:** `S12_RETAINED 37777148 … rpms 130 local 4 fetched 126 manifest 24efe905…` and `S12_RETAINED 37777264 … rpms 130 local 4 fetched 126 manifest b6780cf0…`. The run ended with `S12_BASELINE_RETENTION COMPLETE`.
- **r0013x enumeration `stooH5`:** admitted, and now running.
  - `PRODUCT_SUBSTITUTED …20261123.2/ -> …b567/19437567/…20261125.1/`
  - both `ENUM_PROVIDER` lines came from 20261125.1
  - build.conf `98690f23…` was found in `qb-evidence/37777148-*`
  - sudo has been accepted

  The result will follow.

## New QBs (operator, all running now)

The operator submitted **four** QBs at the same time:

| Shelve | Official (Base 20261113.1) | Custom (Base 20261118.1) |
|---|---|---|
| 14427407: MLGO only (no `-moutline`) | **37836579** | **37836654** |
| 14507546: MLGO + clang-only `-moutline` | **37836693** | **37836727** |

These are the 4 images for the board test plan.

## PM decision: S12 pairs

The primary S12 comparison is **same-day twins**: each pair shares the same submission time, base, base CL and product snapshot, so `-moutline` is the only difference.

| Lane | Reference | Candidate |
|---|---|---|
| Official | **37836579** | **37836693** |
| Custom | **37836654** | **37836727** |

37777148 and 37777264 stay as **secondary references only**, for a reproducibility check (step 3).

Changes to `s12.py`:

1. **Replace the fixed `BASES` with operator-supplied pairs.** Accept `REF=CAND` per lane, in the form `Official:37836579=37836693 Custom:37836654=37836727`. Each QB may be given as `QB=Product-URL` if it is not yet in the local config or a capture.
   - Validate each publication: product ID, Clang build.conf, and base 20261113.1 for Official or 20261118.1 for Custom.
   - The reference must be built **without** `-moutline`, so its helper count is the K-lane non-outline level, far below 20,324. The candidate must be built **with** it, so its count is in the 20,324 range.
   - Keep the rejection of the retired pair (37736448, 37736427).
   - Keep the rule that a candidate cannot be its own reference.
2. **On first read, retain all four new QBs** into `qb-evidence/<QB>-<release>/`, the same way as `--retain-baselines`: 130 RPMs and the manifest. Add a mode `--retain QB[=URL] …` so the operator can retain each QB **as soon as it finishes**, before S12 and before the artifacts expire.
3. **Reproducibility check (INFO, not a gate):**
   - Compare the 14427407 reference **37836579** with **37777148**, and **37836654** with **37777264**.
   - Same shelf, same base CL: `tztv-kernel-perf` vmlinux `.text`, the helper count and the module set should all match.
   - Report `S12_REPRO <lane> IDENTICAL|DIFFERENT <reasons>`. A difference is information for the report, not a FAIL.
4. **Expected `S12_PAIR` content:**
   - reference helpers vs candidate helpers;
   - candidate `.text` vs reference `.text` (the PERF kernel), so we can check against K1 8,214,312 and the K0 reference;
   - module set, vermagic, signature and CRC comparison as before.

   `S12 PASS` only if both pairs pass.
5. **Keep everything else:** read-only against the repos, idle priority, no locks, no sudo, workspace-only writes, the packet format, and checksum verification of every RPM.

## Deliverable

A new pin, plus two hash-pinned commands for PM review:

- (a) `--retain` for any finished QB, to run as each one completes;
- (b) the paired S12, `Official:37836579=37836693 Custom:37836654=37836727`.

Update `STATUS.md` with the four QB numbers and the board-test plan: 4 images, a 2×2 of MLGO × `-moutline`.

Do not touch the running `stooH5` enumeration. No GitHub submission from the Native Server.
