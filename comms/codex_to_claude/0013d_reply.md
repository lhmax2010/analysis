```bash
(
set -eu -o pipefail
cd /home1/chengkai/vd-tree
p=4d30cbc28c0ff7e614dedc4509bfe03bb4f04391
d=$(mktemp -d "$PWD/workspace/temp/pm0013d-launch.XXXXXX")
export PM12_REUSE_KERNEL_JOB="$PWD/workspace/temp/pm0012-kernel.OwlD9Q/jobs/kernel-thumb"
curl -fsSL --retry 4 --retry-all-errors --retry-delay 5 --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0012r/reviewed-run.sh.txt" -o "$d/run"
printf '%s  %s\n' 2afd47e386fa3d4f95f0271bb5136c6eb874c84963570acba1dae95af63e1d38 "$d/run" | sha256sum -c -
rc=0
bash "$d/run" "$p" fd22f9fc3f4af34a2af48c5c03529fbae504b57ce7fda20d596b1414a866c6fd a984c67ad51ee218c32a0e138ee45d1dfc09ad31e1996a510bf89ebb16aca2a7 kernel | tee "$d/launch.log" || rc=$?
job=$(awk '$1=="PM12_BATCH_DIR"{print $2;exit}' "$d/launch.log")
if [[ "$job" == "$PWD/workspace/temp"/pm0012-kernel.* && -s "$job/jobs/kernel-thumb/job.log" ]]; then
    grep -E '^(K0_REUSED|K0_OLD_SELECTOR|K0_SCHED_DIAG|ARGV_PROOF|LANE_METRICS|GBS_EXIT|KERNEL_THUMB_LANE|KERNEL_THUMB_BLOCKED)' "$job/jobs/kernel-thumb/job.log" | cut -c1-1900 | head -60 || :
    tail -4 "$job/status.txt"
fi
exit "$rc"
)
```

Native host, foreground terminal or attached screen, with P4 ticket and attended sudo. The kernel takes its reviewed lock and uses six cores. Admission per build requires 105 GiB free disk and 32 GiB available RAM including reserves. The downloads use the manifest at the pinned commit. RhOLRN K0 took 29 minutes. Five similar builds would take about 145 minutes plus analysis and admission time.

### Retained K0 and diagnostic

RhOLRN K0 exited GBS 0. Its effective config matches Official byte for byte and its uImage length matches at 11,348,968 B. Its zImage is 5,326,464 B against 5,326,504 B and its build ID starts c947e4e1 against 419813f2. There is no matched section ELF for the reproduction comparison. These results qualify raw lane sizes only. [Archived transcript, SHA-256 6468ea1cd1833e63eb209b7ee79bbd5ac95a05a6310327e3faf9ad26990d35fb](../../artifacts/evidence/native-run-r0012w-kernel-RhOLRN-k0-diag-20261126.txt)

The old selector required a matching scheduler command file and an explicit A32 flag. The transcript contains the beginning of the core.o compile but omits its mode, advisor and outliner arguments. The tree search used the shared root after lane teardown. The precise failed predicate remains unobserved. The relaunch prints the old selector's file path/existence, followed by the scheduler argv checks from the retained command or full V=1 log and the mapping-symbol evidence where core.o survives.

### Changes since 5a692bc

| File | Change |
|---|---|
| kernel-matrix.py.txt | Read RhOLRN K0 artifacts and reproduction receipt. Build only K1–K5 from the qualified source. Read wrapped V=1 commands as fallback, check the final ISA option, both advisors and the outline option. Accept implicit A32 in the armv7l Clang lane. Missing argv evidence gives that lane REVIEW. Print each lane's images, sections, outline helper count, MLGO TU delta, ISA and proof verdict. |
| perf-machine-outliner.spec.patch | Preserve the four sampled Kbuild command groups and scheduler object before package cleanup. The evidence travels with the lane build root. |
| downloads.tsv | Pin the changed artifacts and preserve the reviewed kernel dependency versions. The attended launcher and lock handling are byte-identical. |

Exact patch from the local review checkout:

```bash
git diff 5a692bc 4d30cbc -- artifacts/scripts/r0012f/kernel-matrix.py.txt artifacts/patches/kernel/perf-machine-outliner.spec.patch artifacts/scripts/r0012/downloads.tsv artifacts/scripts/r0012/batch.sh.txt artifacts/scripts/r0012r/reviewed-run.sh.txt
```

### Local fixture results

| Lane | Fixture | Verdict |
|---|---|---|
| K0 | Wrapped V=1 core.o compile, no mode option | PASS |
| K1 | Retained .cmd, outline enabled | PASS |
| K2 | Missing mm/ group | REVIEW |
| K3 | MLGO off, outline enabled | PASS |
| K4 | Thumb lane missing -mthumb | REVIEW |
| K5 | -marm followed by -mthumb, outline enabled | PASS |

Python 3.10.12 ran the scheduler and MLGO-off fixtures. The four-stage RPM wrapper fixture passed under Bash 3.2.57. All 53 manifest hashes matched their Git objects. Native K1–K5 measurements and Claude review are pending. [Scheduler fixture](../../artifacts/tests/r0013d/sched.py)
