```bash
# 1. Native host, attended. Save this terminal's PM13E_TOOLS line. Dry-run only.
cd /home1/chengkai/vd-tree/workspace/temp && (
  set -eu -o pipefail
  d=$(mktemp -d "$PWD/pm0013e-tools.XXXXXX")
  p=4bce9028331343ca64254fe6b2227715359ae86f
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0013e/ops.sh.txt" -o "$d/run"
  printf '%s  %s\n' 4d7e641e17b087ff896009c73b845b464696f1df54a947bd22a5e0e15e150bc2 "$d/run" | sha256sum -c -
  printf 'PM13E_TOOLS %s\n' "$d"
  APPLY=0 bash "$d/run" "$p" historical
)
```

```bash
# 2. Native host. After reviewing ALLOW and KEPT_OR_PARTIAL, paste the PM13E_TOOLS line at the prompt.
pm13e_init() {
  local tag d
  read -r -p 'Paste PM13E_TOOLS line: ' tag d
  [[ $tag == PM13E_TOOLS && ${d%/*} == /home1/chengkai/vd-tree/workspace/temp && ${d##*/} =~ ^pm0013e-tools\.[0-9A-Za-z]{6}$ && $(realpath -e "$d") == "$d" ]] || return 2
  PM13E_TOOLS=$d
}
pm13e() {
  printf '%s  %s\n' 4d7e641e17b087ff896009c73b845b464696f1df54a947bd22a5e0e15e150bc2 "$PM13E_TOOLS/run" | sha256sum -c - &&
    bash "$PM13E_TOOLS/run" 4bce9028331343ca64254fe6b2227715359ae86f "$@"
}
pm13e_init && APPLY=1 pm13e historical
```

**Measured on /home1:** 27 exact build-root/cache paths total **30,901,366,784 B (28.779 GiB)** in the operator's census. The full 40-row census was 32.314 GiB. The 27-path figure includes saved scratch contents and hard links. The dry-run prints eligible exclusive blocks per path. The apply prints the accepted estimate and the filesystem-wide change in free space. Concurrent builds affect that last figure. Recovered GiB awaits the native apply readback. The two original RPM directories were measured separately at **9,115,103,232 B (8.489 GiB)**. Their published-match count is still unknown. [Exact allowlist, bytes, archive locations and three-pin reference audit](../../artifacts/ledger/0013e-native-prune.tsv) · [Root census](../../artifacts/evidence/native-input-r0013e-roots-20261126.txt) · [Parent census](../../artifacts/evidence/native-input-r0013e-parents-20261126.txt) · [Operator scope](../../artifacts/evidence/native-input-r0013e-scope-20261126.txt)

**Historical cleanup scope.** The ledger contains 12 pairs of `local/BUILD-ROOTS` and `local/cache`, plus three cache-only paths. For each populated build root the helper requires retained RPMs and a package build log under `local/repos`. Each scratch home, `var/log` and `var/tmp` moves by rename to the sibling `pm0013e-retained` directory on /home1. Source trees, result files, RPM outputs and GBS logs outside those leaves stay available. At all three requested revisions the sole literal candidate reference reads the board-bench parent's external `gbs.log`. The active kernel uses its own run plus OwlD9Q, RhOLRN, smoke and source proofs. B+C+E and the pkg worker use their captures and private workdirs. Mount, open-handle and path checks run again at deletion. A permission or evidence failure prints the retained path. The operator's other large directories and the two RPM-original directories are outside command 1/2.

### Kernel lane reclaim for the running 4d30cbc batch

```bash
# Native, separate attended terminal. Define pm13e_init and pm13e from block 2, then run pm13e_init in that terminal.
APPLY=1 pm13e kernel-follow auto
```

The follower acquires its own directory lock and checks for completed lanes every 30 seconds. It can run alongside the current kernel and B+C+E. Each K1–K5 lane needs its close marker in `job.log`, measured receipt in `kernel-matrix.json`, saved uImage/zImage, built perf RPM, GBS log, and hash-verified vmlinux, System.map and .config. The helper also verifies the saved scheduler object/command and command files from mm, arch/arm and net/core. It moves the complete perf evidence tree to `Kx/pm0013e-build-evidence/<zImage-sha256>/` and then removes only that lane's `GBS-ROOT/local/BUILD-ROOTS`. Use that new prefix for paths recorded in the old receipts. `KERNEL_KEEP` identifies a lane requiring review. K0, its original roots and the retained RPM repositories are excluded.

**Post-run sweep tomorrow**, before any recovery build. These commands also work if no follower ran tonight.

```bash
APPLY=0 pm13e kernel auto
APPLY=1 pm13e kernel auto
```

`auto` requires one original batch with the exact 4d30cbc manifest. If several match, pass its full `PM12_BATCH_DIR` path instead. For a later recovery-run cleanup pass its explicit batch path. Logs remain in `PM13E_TOOLS`. The sweep/follower performs local metadata and hash reads, one lane at a time, at idle I/O priority. It saves evidence by same-filesystem rename. It takes no kernel or pkg build lock. Historical dry-run/apply likewise need no GBS or network after the pinned scripts download. Allow minutes for each scan.

### Command 2 for the package worker

```bash
pm13e pkg
```

Native, attended terminal or attached screen, with a valid P4 ticket. Use this pin when starting tier 2. An already-running worker continues on its original pin. The new worker writes its package result and both lane receipts, completes N4 ABI checks when applicable, and then reclaims the baseline and treatment roots separately. It verifies the ELF hashes, RPM owners, driver/link traces and GBS logs before each deletion. `PKG_RECLAIMED <package> <GiB> GiB <lane>` identifies the measured leaf. Errors retain the relevant root and evidence. The existing pkg lock, Friday cutoff, six eligible cores, single build thread, 74 GiB disk/28 GiB RAM admission and 60 GiB disk floor are unchanged. Build time and dependency traffic follow the existing package plan. The 0013a B+C+E and roster commands keep their approved pins.

### Disk-refusal fallback for K4/K5

```bash
pm13e disk-retry auto
```

Run in an attended native terminal after the original batch and the post-run sweep, when the existing heavy-job guard admits a kernel build. The kernel command retains its 105 GiB free-disk and 32 GiB available-RAM gates and P4/sudo checks. If the package worker is building, let its active build finish before starting this fallback. The current pin's source/smoke gates and spec are reused. Allow approximately 30 minutes per admitted lane plus analysis and dependency downloads; each new lane can consume approximately 10 GiB.

Selection requires the original script and manifest, completed batch, all six lane close records, K0 receipt, and verified retained symbols and effective config wherever present. For K4/K5 a retry requires the D-018 admission diagnostic, a unique matching capacity measurement with free disk <105 GiB and available RAM ≥32 GiB, and absence of both a GBS log and build root. The script prints `DISK_RETRY … lanes K4`, `K5`, `K4,K5` or `none`. Only selected lanes enter GBS. Successful, mixed-cause and compile-failed lanes retain their old verdicts. `KERNEL_NO_DISK_RETRY` ends the job without a build. Insufficient headroom or a review verdict can still leave the overall matrix incomplete.

### Optional RPM originals, outside the overnight critical path

```bash
pm13e rpm-plan
```

The plan hashes individual RPMs under exactly `o997/gcc_rpms` and `o984d/rpms`. It checks published repomd → primary checksums, indexes SHA-256 package entries from the retained GCC Product snapshot, its Base, both LLVM Bases and the two current Product snapshots, and writes a TSV of exact local path, size, RPM SHA-256, URL, primary URL and primary SHA-256. Unmatched rows have empty URL fields. A missing or expired repository is reported and may reduce coverage. The plan reads up to 8.489 GiB locally and downloads metadata. No sudo or build lock. Review the matching count before deciding whether to apply.

```bash
# Paste the RPM_MANIFEST line from the plan at the prompt.
read -r -p 'Paste RPM_MANIFEST line: ' tag run sha
[[ $tag == RPM_MANIFEST ]] && APPLY=1 pm13e rpm-apply "$run" "$sha"
```

Apply checks the reviewed TSV digest, fetches current metadata, streams each candidate RPM from its recorded URL, and recomputes the full remote and local SHA-256 and size before unlinking that exact regular file. Changed metadata, failed downloads, changed/shared files and unmatched entries stay. `rpm-restore.tsv` and `apply-results.tsv` stay under the workspace. Up to one serial RPM download per matched file, approximately 8.49 GiB maximum payload on this census. Schedule off the critical path if repo/network I/O is busy.

**Review state.** Python 3.10.12 fixtures passed for protected/symlink paths, historical evidence preservation, package and kernel receipt failures, per-lane cleanup, all four retry selections, mixed RAM+disk and 105 GiB boundary cases, and published/unmatched/corrupt RPM payloads. The scheduler proof and package PTY/admission fixtures also passed. All 54 kernel and 26 package manifest entries were verified. PM review and native recovery measurements are pending. [Reclamation fixture](../../artifacts/tests/r0013e/reclaim.py) · [Pinned script commit](https://github.com/lhmax2010/analysis/commit/4bce9028331343ca64254fe6b2227715359ae86f)
