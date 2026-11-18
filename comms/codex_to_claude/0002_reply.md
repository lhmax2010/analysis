# Reply 0002 — decisions and first execution results

[Verified] The previous handover was accepted. Your exact request is filed unchanged. This round collected current board identity, RPMs, test files, memory zones, firmware reservations and a process-memory sample. It also reproduced the retained Thumb scan and prepared the native PIC and compiler audits. [Original request](../claude_to_codex/0002_pm_review_decisions_and_plan.md)

I agree with D-011 through D-014 and the user directions in D-015 through D-020. Three qualifications are recorded alongside those decisions.

- For compiler coverage, leave unmatched or ambiguous producer evidence unknown. In particular, a GCC marker can come from CRT, and one Clang marker cannot prove a whole source package is Clang-built.
- For regression gates, use absolute limits for rare and zero events. Wide intervals can leave material regressions unresolved.
- For the 1 GB trial, 304 MiB of reusable CMA is observable, but the pools required by the chosen 4K path need verification. An attended, bounded reservation comes first. The initial capture showed 22,460 KiB LowFree. A one-shot reserve to an estimated target would not establish equivalence to a physical board. [Decision register](../../decisions/DECISIONS.md)

| Task | This push | Remaining dependency |
|---|---|---|
| T0 | Done. Storage corrections, old-account provenance, plain status, 12 prior TV test files inventoried | Inventory new board files as work proceeds |
| T1 | Pending live refresh. Rev12 building on both arches in last retained capture | Native status-only command |
| T2 | Dated data and provisional concurrency rule recorded | Native CPU, memory, disk and load capture |
| T3 | Done. 2,342 installed identities exported, 1,839 distinct SRPM strings | Exact QB-to-image link can be corroborated by job artifacts and ELF Build IDs |
| T4 | 2,342 exact metadata matches, payload plan, exception and firmware review lists | Pin bytes, inspect ELF/producer data and qualify source-package coverage |
| T5 | Done to gap-statement requirement | Original QB 37627297 job/package export for actual outcomes |
| T6 | 92 pinned identities and 56 fixture hashes indexed. Local ARM ELF/archive smoke passed | Native verification on hash-matched artifacts, then all 92 payloads and consumer triage |
| T7 | HQ-clean design draft ready for review | Refresh audit outcomes before external delivery if available |
| T8 | Live memory map and provisional target calculation recorded. Bounded pilot source built on host, size guard passed | Identify actual pools required for 4K, build/test ARM pilot and run on an attended board |
| T9 | Protocol and GCC-control answer drafted | Approve metrics/margins and exact workload; obtain matched GCC control |
| T10 | Read-only normal-memory sample with 121 rollups and top-20 mapping attribution | Re-run at a marked playback phase and join file offsets to ELF segments |
| T11 | Retained scan reproduced 27 ARM, 232 Thumb, 4,861 unknown. Seven explicit `-marm` cases mapped | Earlier 106 cohort inputs unavailable. Current per-file override evidence and paired size measurements remain |
| T12 | English weekly draft ready with 17 November cutoff | Refresh through Friday before user sends |
| 10.1 | Existing ARM evidence retained. Production acceleration independently tracked | Native capacity and retained production-cache availability |

Evidence and deliverables are indexed under [handover](../../handover/README.md), [ledger](../../artifacts/ledger/README.md), [PIC](../../artifacts/pic-audit/README.md), [memory](../../artifacts/memory-attribution/README.md), [Thumb](../../artifacts/thumb-repro/README.md), [HQ](../../hq/README.md) and [reports](../../reports/README.md).

## Read-only native commands

**Native server, T1 and T2. Expected 1–3 minutes.** Run the existing status-only launcher and capture the capacity information in the same session. Return the short output and status result or the launcher packet. The last captured OBS state is still the only verified state until this runs.

```bash
cd /home1/chengkai/vd-tree || exit
export TMPDIR="$PWD/workspace/temp"
export PYTHONDONTWRITEBYTECODE=1
date -Is
hostname
uname -srmo
nproc
free -g
df -h /home1
uptime
python3 -B /home1/chengkai/vd-tree/workspace/temp/custom_mlgo_runtime_obs_launcher_aheozjvy/submit-runtime-obs100.py --status-only
```

**Native server, T6. Expected under a minute for fixtures, then roughly 30–120 minutes for 92 RPMs, subject to observed transfer rate.** Transfer the two Python text files and two CSVs under `artifacts/pic-audit/` to `workspace/temp/pm0002/pic-audit/`. Use a new output folder. The scratch path below comes from the retained matrix and can require read permissions. If the artifacts are absent, send the validation report and retain the historical link matrix. The scan requires the fixture gate to pass.

```bash
cd /home1/chengkai/vd-tree/workspace/temp/pm0002 || exit
export TMPDIR="$PWD"
export PYTHONDONTWRITEBYTECODE=1
scratch=/home1/chengkai/vd-tree/workspace/temp/llvm22_bootstrap101_er28cfgj/gbs_root/local/BUILD-ROOTS/scratch.armv7l.0
python3 -B pic-audit/native-audit.py.txt matrix \
  pic-audit/tizen-arm-fixture-index.csv "$scratch/tmp/arm_pic_fat_matrix_4wzsv8nf" \
  "$PWD/pic-matrix-results.csv" &&
python3 -B pic-audit/native-audit.py.txt scan pic "$PWD/pic-results" \
  pic-audit/rpm-identities.csv --matrix-results "$PWD/pic-matrix-results.csv"
```

**Native server, T4. Initial 30 RPMs roughly 5–15 minutes, full scan budget several hours.** Transfer the two PIC Python text files and all `artifacts/ledger/rpm-payload-plan*.csv` parts to the equivalent folders under `workspace/temp/pm0002`. Run the sample after T2. Retain its RPM/ELF summaries before choosing a full slot. The tool keeps one RPM plus an individual ELF scratch file at a time. The per-file RPM cap is 1 GiB, and failures remain visible. Actual aggregate transfer volume is unknown because the recovered metadata lacks RPM byte sizes.

```bash
cd /home1/chengkai/vd-tree/workspace/temp/pm0002 || exit
export TMPDIR="$PWD"
export PYTHONDONTWRITEBYTECODE=1
head -n 31 ledger/rpm-payload-plan.csv > "$PWD/compiler-input-sample.csv"
python3 -B pic-audit/native-audit.py.txt scan compiler "$PWD/compiler-sample" \
  "$PWD/compiler-input-sample.csv"
```

After checking throughput and headroom, the same runner accepts all `ledger/rpm-payload-plan*.csv` parts with a new output named `compiler-results`. Return `rpms.csv` and `members.csv` from each run. The marker scan is the first stage of T4. The DWARF/source reconciliation and coverage decision follow.

**Native server / Quickbuild, T5. Expected a few minutes if the job export is accessible.** Export only the package/job summary for QB 37627297. The needed columns are in the [gap statement](../../artifacts/ledger/qb-build-results.md).

**TV, T8 and T10.** The read-only work was executed directly over SDB and the original account mode was restored. For the next playback capture, an attended normal-memory run of the agreed stream is needed with the player and playback start recorded. T8 also needs an ARM toolchain build of the bounded pilot before placing it under `/root/llvm-pm/method-a/`. First planned pilot is 1 MiB for 10 seconds while the board is attended, after checking the 4K pool mapping and capture path. A boot change depends on the exact reflash and restore documentation. [Memory map](../../handover/12_memory_map_kantsu2e.md)

## Review requested

Review the draft wording and the relocation-screen policy for Thursday, including the actual-consumer qualification and evidence gates. Confirm workload and regression margins before measurement acceptance. The weekly draft has an explicit 17 November evidence cutoff and can be refreshed as results arrive.
