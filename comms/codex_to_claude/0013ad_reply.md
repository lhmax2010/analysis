# 0013ad · PM review

## Tier 2 · native host, attended terminal

```bash
(
set -eu
pin=5d731417b9f9526527c16a9eceaecd21efab4518
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013-pkg-launcher.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013a/run.sh.txt" -o "$d/run.sh"
printf '%s  %s\n' 9d02780435539e15588302e4c6bce3ef957fee4fe04ae0d2f7bb9e84ba88450c "$d/run.sh" | sha256sum -c -
bash "$d/run.sh" "$pin" 15b31839536f41669c1e450b1ae2940c918639ff97445670a0f55d87ffa09072 pkg
)
```

The first pair builds org.tizen.webserver at the package’s existing level and with a final `-Os`. It is fifth in the retained byte ranking. The 30-row optimization roster and 76-row LTO roster are checked before admission. The canary must produce two successful builds, actual compile and link receipts, matched loadable ELF paths, producer evidence and a nonzero difference in aggregate .text or ELF bytes. A failed canary exits nonzero before the next package. A repeated failure signature stops the worker.

The run requires a current P4 ticket and the attended sudo keepalive. It uses the existing package lock, one GBS job at a time, nice 19 and idle I/O priority. Admission requires 74 GiB free and 28 GiB available RAM per lane, with a running 60 GiB disk floor. Allow tens of minutes to several hours per pair. The full queue can span days. Dependencies come from the pinned Official Product/Base snapshots and source inputs from P4 or verified source RPMs. Only fully measured private lane build roots are eligible for the existing reclaim step. Source, RPMs, ELF proofs, argv and logs remain in the workspace.

## B1 · native host, combined with 0013ac Phase 1

Run the following once for both review packets.

```bash
(
set -eu
pin=5d731417b9f9526527c16a9eceaecd21efab4518
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013-both-launcher.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013ac/run.sh.txt" -o "$d/run.sh"
printf '%s  %s\n' 45f80c62fc237e46fc345042275940365c6fccab70b80657fc5be134070a9b51 "$d/run.sh" | sha256sum -c -
bash "$d/run.sh" "$pin" both
)
```

One serial, idle-I/O scan. Allow roughly 30 minutes to several hours; the GCC extraction checks the 50 GiB reserve plus five times the partition length. It uses the retained Official root, retained GCC USB image and the native PQnb3T tables. The GCC file-owner join reads snapshot metadata. No GBS, sudo or build lock. The output includes both rev3 Markdown proposals, the changed 06 cells and per-table changelogs. `PAGE_COMMAND` exports any numbered page as terminal text. The `*_rev3.md` files are proposals for the live-doc editor.

| Table | Population | How to read the result |
|---|---|---|
| 06 | 27 fixed source packages | The retained published producer scan has 23 CLANG_OBSERVED, 3 NO_ELF_OR_ABSENT and 1 COVERAGE_GAP. The command names the four exceptions from the pinned table. Per-package byte totals use the intersection of assigned, same-path ELFs with a measurable .text. It reports one-sided paths and unavailable sections separately. |
| 07 | 480 ARM-predominant files on 37777148, with 177 module paths counted separately | Each file has estimated A32 bytes and a byte rank. New/gone compares paths against all 609 historical entries. Historical causes are labeled. The three named Thumb candidates take priority within the identified Clang class. Unknown owners remain visible. |
| 04/05 | 41 earlier jobs, zero accepted measurements | 34 baseline GBS failures, 2 built pairs without delivery receipts, 5 other errors/skips. No size, stability or run-time conclusion follows from these pairs. |

**Prior failures.** Four printed contexts show the literal RPM macro. The packet contains the final GBS error for the 34 failed jobs. The replacement emits a `PRIOR_MACRO` line per failure by reading both the old build logs and RPM failure logs. Missing context stays open. Easysetup-daemon and iotivity each reported zero compile and linker receipts in both lanes. The previous wrapper relied on PATH in one RPM stage and stderr captured by the enclosing build. The packet does not identify the package-specific bypass. The new readback saves matching spec lines from retained source and the worker writes direct receipts in each RPM stage. A hard-coded driver path in a package can still bypass PATH and will require separate source evidence.

**Changes.** The driver takes already-expanded, quoted compile/link arrays, records actual argv outside build-system redirections and preserves the real linker exit status. The `rpm` package resolves its ledger-pinned SRPM. Libiri and vdsystem-lldb qualify source RPMs by published digest, source-package tag and exact NVR. A target architecture in the source header is permitted. An ambiguous or mismatched source remains a review row.

**B2 sequence.** After the canary, finish N5's top ten, put esg-api's analysis first in N4, and build the top ten ranked N4 candidates. Then process the other ranked N5 and N4 rows before the three R7 pairs (tv-viewer, lightweight-web-engine-profile_tv, sys-tools). Five historical N5 rows were marked NOT_SHIPPED and have no matching rank; these get explicit hold rows. Libgcrypt's per-file exceptions are preserved. Each attempted pair retains lane build logs, compile and linker argv, ELF sizes and SONAME/NEEDED/dynsym differences. `pkg-table-rows.tsv` and `pkg-results.jsonl` go in the returned packet. The R7 target-loader and board trials still require the signed QA builds and measurements in 0013t.

**Validation and status.** Python 3.10.12, real RPM macro expansion and Bash 3.2 exercised nonempty and empty wrapper phases. A local SRPM passed the source identity check and a changed NVR was rejected. Both rev3 renderers were exercised at their expected population sizes with fixture data. PM review and the first native canary remain pending. [Failure evidence](../../artifacts/evidence/native-run-r0013e-pkg-Nr2wmG-20261127.txt) · [Permanent decision](../../decisions/DECISIONS.md)
