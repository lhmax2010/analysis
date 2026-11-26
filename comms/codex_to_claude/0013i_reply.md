**K1 vs K0 and K3 vs K2: no measured outliner delta in the returned evidence.** Both Clang builds reached a later GCC compilation of `scripts/mod/empty.o`. GCC rejected `-moutline` at 1,156 s in K1 and 1,125 s in K3. The follower preserved both failed roots. The transcript contains neither a perf ELF measurement nor the enclosing spec recipe. Calling that recipe SERET-UL would be premature. Command 1 reads the preserved trees first and prints a receipt before starting the image work. [Error transcript](../../artifacts/evidence/native-run-r0013f-kernel-errors-and-review-20261126.txt) · [Matrix and follower](../../artifacts/evidence/native-run-r0013d-kernel-dkyJ0S-follower-20261126.txt)

| Raw GBS comparison | K0, MLGO release | K2, MLGO off | K0 − K2 |
|---|---:|---:|---:|
| Linked `.text`, B | 8,564,600 | 9,859,176 | −1,294,576 (−13.13%) |
| uImage, B | 11,348,968 | 12,689,580 | −1,340,612 |

Both scheduler advisor checks agree with their lane. K2's two-advisor compile-command delta passed. These are raw GBS measurements. K0's build ID differs from the shipped kernel. The comparison measures the release-advisor switch on the Official Base.

### 1. Retained kernels, assembler, images, pilot, CU coverage and 0013g

Native host after PM review. One low-priority scan at a time, no sudo, GBS or build lock. Reads can overlap locked builds. Plan for minutes for the kernel measurements and roughly 1–3 hours for extraction and table generation, depending on I/O. Keep free space for the expanded image, working partitions and the retained Official sysroot; the partition admission checks run before extraction. The public stable-source archive is streamed for file provenance. Full logs stay under `workspace/temp`.

```bash
(
set -eu -o pipefail
p=30eb2a3fc30450a6eb1eefe4973bc1c46182e484
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013i-launch.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 150 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0013i/read.sh.txt" -o "$d/read"
printf '%s  %s\n' 90c6fbf8a3400de575fa08686326e9a76fcf50478ca895ac85e280a052a870a1 "$d/read" | sha256sum -c -
bash "$d/read" "$p" | tee "$d/combined.txt"
)
```

### 2. Conditional K1/K3 rerun

Use a foreground native terminal after receipt review. At the prompt paste the complete `LANE_RECEIPT path sha256` line from command 1. Validate the receipt before requesting the kernel lock. Each admitted lane uses the existing P4, attended sudo and capacity checks, six cores, at least 105 GiB free disk and 32 GiB available RAM. Budget about 30 minutes of build time per lane plus setup and analysis.

```bash
(
set -eu -o pipefail
t=/home1/chengkai/vd-tree/workspace/temp
p=52688091b40d1f4ade857d51b90ac970c994bc5c
read -r -p 'Paste LANE_RECEIPT line: ' tag receipt digest
[[ $tag == LANE_RECEIPT && $receipt =~ ^/home1/chengkai/vd-tree/workspace/temp/pm0013i-read\.[A-Za-z0-9]{6}/lanes\.json$ && $digest =~ ^[a-f0-9]{64}$ ]]
printf '%s  %s\n' "$digest" "$receipt" | sha256sum -c -
python3 -B - "$receipt" <<'PY'
import json,sys
r=json.load(open(sys.argv[1]))["lanes"]
if set(r)!={"K1","K3"} or any(v["status"] not in ("FINISHED","NO_MATCHING_PERF_ELF") for v in r.values()):
    sys.exit("HOLD: insufficient retained-tree evidence")
if all(v["status"]=="FINISHED" for v in r.values()):sys.exit("Both kernels present; no rerun required")
PY
export PM13I_RECEIPT="$receipt" PM12_REUSE_KERNEL_JOB="$t/pm0012-kernel.OwlD9Q/jobs/kernel-thumb"
d=$(mktemp -d "$t/pm0013i-retry.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 150 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0012r/reviewed-run.sh.txt" -o "$d/run"
printf '%s  %s\n' 2afd47e386fa3d4f95f0271bb5136c6eb874c84963570acba1dae95af63e1d38 "$d/run" | sha256sum -c -
rc=0
bash "$d/run" "$p" 2fbc08cad00ccbdceb1762981406292f18cc8aeb500412b4e2dae203d7916464 a984c67ad51ee218c32a0e138ee45d1dfc09ad31e1996a510bf89ebb16aca2a7 kernel | tee "$d/launch.log" || rc=$?
job=$(awk '$1=="PM12_BATCH_DIR"{print $2;exit}' "$d/launch.log")
if [[ $job == "$t"/pm0012-kernel.* && -f "$job/jobs/kernel-thumb/job.log" ]]; then
    awk '/^(OUTLINER_RETRY|KERNEL_LANE_REUSED|GBS_EXIT|ARGV_PROOF|LANE_METRICS|KERNEL_THUMB_LANE|KERNEL_THUMB_BLOCKED)/{if(++n<=40)print substr($0,1,1600)}' "$job/jobs/kernel-thumb/job.log"
fi
exit "$rc"
)
```

The matrix rechecks the original dkyJ0S receipt, Official config and saved symbols. A measurement requires a matching K0/K2 config, a unique linked ELF, and matching addresses for three symbols in System.map. Effective argv has its own verdict. Image-plus-64 is labelled as an estimate where the uImage is missing. The retry selects only K1/K3 with a conclusive missing-ELF verdict. Make expands the outliner option against the actual target CC. The prior GCC failure came from an unconditional KCFLAGS assignment shared by the Clang and GCC submakes.

**Thumb kernel.** K4/K5 both reject the register list at `arch/arm/lib/backtrace-clang.S:19:13`. Two further diagnostics name macro expansion lines 12 and 37. Command 1 gathers source text and expansion notes, replays discoverable K4 assembly argv inside the read-only GBS-root view and reports make-plan status, command coverage, failing files and MAINTAINERS matches. It compares source files with stable v6.12.60, commit `318a47068f7b88de838518897500d7509e3fe205`. A failed plan/sandbox or ungenerated prerequisite leaves the site list partial. Owners must review changed files before assigning the origin of individual instructions.

**Platform and pilot.** zHbk5J counted prd only. Extraction now accepts an individual skip only with a zero fsck exit, its exact skipped path absent, and a special-file type read independently from the matching image. Walked entries plus verified skips must equal the dump count. Command 1 runs 0013g on the exact new extraction after all three platform gates pass. T4 now takes the board-hash-matched ELF directly from Official 37736448 as well as probing the RPM ledger and member digests. T6 uses the extracted 37777148 loader and its platform/product library paths under qemu-arm-static. T2 requires input ownership for both 60 B and 28 B residues before granting a runtime exemption. A byte-pattern candidate alone leaves REVIEW. T1/T7 retain the observed baseline/default 0 of 26 vs package 26 of 26 LTO inputs, and the package's CU/IR gaps. A proved Official LTO link would require repeating the default lane with the Official link policy.

**Producer coverage.** The earlier zero counted identifiable package-owned GNU C/C++ CUs. Three fixed-roster packages were absent and 24 were unresolved; four sources had separate object-only evidence. Use `E1_COVERAGE` and `e1-rpm-coverage.tsv` for ELF count, build IDs, matching debug rows, producer strings and source ownership per RPM. The zero cannot establish the size of the GCC population. The earlier RELR estimate of 376,196 B likewise covers only matched prd rows.

**Validation and return.** Both evidence hashes matched the PM pins. Local checks passed with Python 3.10.12, real Bash 3.2.57 RPM stage fixtures, five GNU make CC selections, and a rootless EROFS extraction with a dump-confirmed character device. Native measurements and PM review remain open. Return command 1's terminal text, including the receipt and the 0013g verdict. To return the detailed kernel measurement without transferring a file, paste the receipt line at the prompt:

```bash
read -r -p 'Paste LANE_RECEIPT line: ' tag file sum
[[ $tag == LANE_RECEIPT && $sum =~ ^[0-9a-f]{64}$ ]] && printf '%s  %s\n' "$sum" "$file" | sha256sum -c - && python3 -B -c 'import base64,pathlib,sys,zlib;print(base64.b64encode(zlib.compress(pathlib.Path(sys.argv[1]).read_bytes(),9)).decode())' "$file"
```
