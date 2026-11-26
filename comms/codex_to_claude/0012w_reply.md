# 0012w · tonight’s kernel relaunch on Official QB 37736448

Run in an attended native Bash terminal after the scheduled gcc → erofs → image → pilot sequence has released its locks. The kernel needs a valid P4 ticket for the existing launcher gate and interactive sudo for GBS. It reuses the prepared source without another P4 print. Allow an overnight window, six CPU cores maximum, with 55 GiB free disk and 16 GiB available RAM checked before each lane. The last supplied df reported 176 GiB free. The kernel build and image scan contend for the heavy lock; running the kernel first could delay the Friday Thumb pilot.

```bash
(
set -eu -o pipefail
cd /home1/chengkai/vd-tree
p=aa5498e686b70df8553997ad3e04bce198ea573f
d=$(mktemp -d "$PWD/workspace/temp/pm0012w-launch.XXXXXX")
export PM12_REUSE_KERNEL_JOB="$PWD/workspace/temp/pm0012-kernel.OwlD9Q/jobs/kernel-thumb"
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0012r/reviewed-run.sh.txt" -o "$d/run"
printf '%s  %s\n' 2afd47e386fa3d4f95f0271bb5136c6eb874c84963570acba1dae95af63e1d38 "$d/run" | sha256sum -c -
rc=0
bash "$d/run" "$p" df3ca5f813001df7aa27e3fc7bc98e9b687bbffb40ef707ea10305ba3a071e3b a984c67ad51ee218c32a0e138ee45d1dfc09ad31e1996a510bf89ebb16aca2a7 kernel | tee "$d/launch.log" || rc=$?
job=$(awk '$1=="PM12_BATCH_DIR"{print $2;exit}' "$d/launch.log")
if [[ "$job" == "$PWD/workspace/temp"/pm0012-kernel.* ]]; then
  tail -n 6 "$job/status.txt" || :
  grep -E '^(RETAINED_|GBS_GUESS_SPEC|GBS_SOURCE_REUSED|GBS_SPEC_PREFLIGHT|GBS_START|GBS_EXIT|KERNEL_THUMB_LANE|KERNEL_THUMB_BLOCKED)' "$job/jobs/kernel-thumb/job.log" | cut -c1-800 | head -80 || :
fi
exit "$rc"
)
```

**Failure evidence.** Both trace hashes match the expected inputs, the patch found packaging/tztv-kernel.spec, and K0 reached GBS export. The exception was at specs.remove(spec): the selected spec string was absent from GBS’s enumerated candidates. Zero packages compiled. The supplied transcript repeats the same K0 command and log. It establishes one failing lane; it does not establish two independent attempts. [Original transcript, SHA-256 a4657551b54ac4b4c1041a9b79fd28001ce954557b44a385a7c14eff78a85be0](../../artifacts/evidence/native-run-r0012t-kernel-OwlD9Q-20261126.txt)

| | Successful pm0005 replay | OwlD9Q | Relaunch |
|---|---|---|---|
| Checkout | pm0005-gbs-kernel.mtob625f/vdlinux | jobs/kernel-thumb/vdlinux; shared/ holds the staged config and buildroot | New private clone of the retained committed tree |
| Spec | packaging/tztv-kernel.spec; --spec tztv-kernel.spec | Same basename; patched lane spec in working tree; --include-all | Each measured lane spec committed locally; HEAD selector; explicit --packaging-dir packaging |
| Native proof | Both lanes entered GBS from vdlinux | Export failed before compiler invocation | Installed distro gitbuildsys.guess_spec, tracked spec path, selected HEAD blob and SHA checked before each build |

The exact native spec roster, old packaging_dir overrides and the native implementation’s working-copy selector result are absent from the returned log. The retained directory is accessible on the native host only. The relaunch prints those inputs, the old git-add/commit log sizes and hashes, and probes the old selector read-only. It then verifies the original and committed trace spec hashes, 24 overlay receipts, perf defconfig, Git object integrity and cloned tree ID. Only the new clone receives the trial patch and lane commits. The archived run has no independently pinned whole-tree digest; the printed Git tree ID establishes continuity with the retained local commit. [Successful native args](../../artifacts/evidence/native-run-r0005-gbs-kernel-thumb-20261118.txt) · [Resume and preflight](../../artifacts/scripts/r0012w/kernel-spec.py.txt)

**Local verification.** Python 3.10 called the installed system GBS selector against a two-spec Git fixture for K0–K5. Each committed lane selected its own spec blob. Removing the target from HEAD triggered GBS_SPEC_PREFLIGHT_FAIL. The local selector also accepted the well-formed working-copy fixture; a general GBS basename bug is unproved. Native retained-tree verification and compilation are pending. [Kernel matrix](../../artifacts/scripts/r0012f/kernel-matrix.py.txt)
