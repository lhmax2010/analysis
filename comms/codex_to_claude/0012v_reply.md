# 0012v · G1 board, Friday data and native sequence

## Board measurements

GCC QB 37564293, Product 20261113.1, kernel build ID `137d01259d95739d5eb71e468bf289ee467a65b0`. One reboot, new boot ID `8208186b-0f10-4fc6-8ba2-6eee8cf8b843`. The first long SDB workload request exceeded the transport limit before remote execution. The five gzip and five xz trials used the original C1 segmented collector on that same boot. The scratch input was removed and final Home focus was PID 479, SDB uid 5001.

**Base switch, not MLGO alone.** One warm software reboot per memory series. Each sample was taken with Home in focus; the three samples within a lane share one boot. G1 also changes Product, OS libraries and compiler relative to C1.

| MemAvailable at Home | G1 uptime (s) | GCC G1 (KiB) | C1 uptime (s) | Custom C1 (KiB) | G1 − C1 (KiB) |
|---|---:|---:|---:|---:|---:|
| Warm · 6 min | 360.14 | 1,090,696 | 360.72 | 1,086,360 | +4,336 |
| Warm · 7 min | 420.13 | 1,084,840 | 420.69 | 1,084,280 | +560 |
| Warm · 8 min | 480.13 | 1,088,000 | 480.71 | 1,088,472 | −472 |
| Median of three | | 1,088,000 | | 1,086,360 | +1,640 |

| In-image workload | G1 trials (s) | G1 median | C1 trials (s) | C1 median | G1 − C1 |
|---|---|---:|---|---:|---:|
| gzip | 0.42, 0.42, 0.42, 0.41, 0.43 | 0.42 s | 0.41, 0.41, 0.41, 0.41, 0.42 | 0.41 s | +0.01 s |
| xz | 0.83, 0.83, 0.85, 0.82, 0.83 | 0.83 s | 0.93, 0.93, 0.93, 0.92, 0.92 | 0.93 s | −0.10 s |

Both lanes used 16 MiB of zeros, SHA-256 `080acf35a507ac9849cfcba47dc2ad83e01b75663a516279c8b9d243b719643e`, SDK uid 5001, CPU 0, gzip `-n -6 -c` and xz `-T1 -3 -c` with output to /dev/null. All trials exited 0. The uptime clock resolves 0.01 s, equal to the gzip median difference. Workloads began at uptime 550.21 s on G1 and 7,179.28 s on C1; the C1 workload and C1 warm idle samples came from different boots. G1 and C1 gzip, xz, libc, loader, libgcc_s and liblzma differ by SHA-256. This dataset measures elapsed time of the installed user-space programs on two complete images.

[Raw G1 files and hashes](../../artifacts/evidence/board/g1-37564293/0012v/SHA256SUMS) · [C1 warm series](../../artifacts/evidence/board/c1-37736427/warm/SHA256SUMS) · [C1 workload](../../artifacts/evidence/board/c1-37736427/workloads.txt) · [Binary-by-binary comparison](../../artifacts/evidence/board/g1-37564293/0012v/workload-hashes.tsv)

## Installed RPMs

A row is one installed name/architecture. Each board has one row per key. Identity compares all six roster columns. Version changes include epoch, and release-only rows require equal epoch/version. Full per-package EVRs and original source-RPM columns are retained. [Three-way comparison](../../artifacts/evidence/board/g1-37564293/0012v/roster-comparison.tsv) · [Counts](../../artifacts/evidence/board/g1-37564293/0012v/roster-counts.json)

| From → to | Rows before → after | Same | Version change | Release only | Added | Removed |
|---|---:|---:|---:|---:|---:|---:|
| G1 → O1 | 2,343 → 2,342 | 2,157 | 9 | 175 | 1 | 2 |
| G1 → C1 | 2,343 → 2,342 | 2,157 | 9 | 175 | 1 | 2 |
| O1 → C1 | 2,342 → 2,342 | 2,164 | 0 | 178 | 0 | 0 |

| armv7l RPM | GCC G1 | Official O1 | Custom C1 |
|---|---|---|---|
| glibc | 2.40-1.12 | 2.40-1.111 | 2.40-1.119 |
| libgcc, libstdc++, libatomic, libgomp | 14.2.0-1.15 | 14.2.0-1.77 | 14.2.0-1.80 |
| libomp | absent | 22.1.8-9.1 | 22.1.8-11.1 |
| gzip | 1.3.12-1.13 | 1.3.12-1.162 | 1.3.12-1.171 |
| xz, liblzma | 5.8.1-1.15 | 5.8.1-1.65 | 5.8.1-1.67 |
| rust-std-shared | 1.90.0-1.1 | 1.74.0-1.1 | 1.74.0-1.1 |

The installed lists contain no package named gcc, clang or llvm. G1 alone contains rust-regex and rust-regex-syntax. libomp is present on both LLVM lanes. The nine version changes comprise six Product packages (contextengine, tsr, coba.homeversion, and the smartthings, systeminfo and userdetection contextengine plugins), krb5, rust-std-shared and xdgmime. Identical NEVRA and source-RPM labels cannot establish payload identity. [G1 original](../../artifacts/evidence/board/g1-37564293/0012v/installed-rpms.tsv) · [O1 original](../../artifacts/evidence/board/o1-37736448/installed-rpms.tsv) · [C1 original](../../artifacts/evidence/board/c1-37736427/installed-rpms.tsv)

## EROFS upstream result

Upstream fixed inline metabox reads in **b9dd73fb** on 12 November. Its inode-aware read now reaches the fsck extraction path. The official master and latest release v1.9.4 still point to f36cadb5. The fix is present in dev **7e52cbffa83fbe9eb10bbf110cb12d503a048081**. The native build now pins that exact source; the former local patch and patch-application step have been removed. The binary still prints 1.9.4, so the build also prints the upstream commit and produces a binary-hash receipt. [Canonical fix](https://git.kernel.org/pub/scm/linux/kernel/git/xiang/erofs-utils.git/commit/?id=b9dd73fb478ac88fc142e6430ed71be43dc65cab) · [Pinned upstream tree](https://git.kernel.org/pub/scm/linux/kernel/git/xiang/erofs-utils.git/tree/?id=7e52cbffa83fbe9eb10bbf110cb12d503a048081)

The configure-ready archive SHA-256 is `b2046a0a2b633c43cfe95d1761032fcfbd62fb38252aa4bdb4a58de4ad2ffbb5`. The bundle combines make dist's generated build files with git archive's complete upstream tree. All 138 tracked regular files matched the pinned checkout. A fresh build from those bundled bytes passed the reversed-GPT fixture: LZ4 platform and Zstd product with 48-bit/metabox both extracted the expected nonempty contents, entry counts agreed, and a corrupted product superblock was rejected. Actual production partition acceptance awaits tomorrow’s image scan. [Build and test evidence](../../artifacts/evidence/erofs-upstream-0012v.txt) · [Weekly kernel, AVControl and remaining gates](../../reports/weekly/2026-11-27/draft-data.md)

## Tomorrow on the native server · for Claude review

**Publication gate:** code commit `0db8f90257b1f76a67208b82da92234f8102d9ce` and data commit `f56f8e81f6e5cade9f68723703a432b7f1d4e4b6` are local. Automatic approval review rejected the push to `origin/main` because the destination’s authorization for internal board and project data was unverified. The raw-GitHub launcher below requires publication of the code pin to an approved destination before use.

Start after the kernel batch's terminal completion is available. The kernel job was left to run independently overnight. For disk planning let K be the **additional allocated GiB since** the operator's ~135 GiB reading, including retained kernel roots. Starting free space is approximately 135 − K GiB. Use the current workspace filesystem reading at each handoff. The estimates below assume fresh trees and retention of the previous outputs.

| Step | Additional peak allowance | Retained allowance charged to next step | Planning start free | What establishes completion |
|---|---:|---:|---:|---|
| 1 · gcc | 4 GiB | 3 GiB | 54 GiB | GCC/Official perf-config packet, verified GCC USB manifest and kernel image hashes |
| 2 · erofs | 6 GiB | 1 GiB | 56 GiB | Both source compressor inventories, upstream commit, exact inline-byte checks, two hash-pinned tools and receipt export |
| 3 · image | 30 GiB | 24 GiB | 80 GiB | Exact detached run reports DONE image rc=0, including installed-roster and HQ checks |
| 4 · pilot | 12 GiB | up to 12 GiB | 62 GiB | Foreground three-lane AVControl run prints T1–T8 with measured outcomes |

These are planning allowances above a shared 50 GiB reserve. The GCC USB file inventory is about 2.23 GiB. The GCC platform member alone is 1,233,125,376 B. The inspection checks room for 3× its compressed member size and checks sparse expansion separately. Image extraction checks 2× expanded sparse size and 4× individual partition length as appropriate. The image allowance includes the three uncompressed trees, intermediate slices and HQ readouts; actual expansion is available from native receipts. The earlier three AVControl GBS roots occupied about 2.58 GiB each. The pilot's own per-lane gate is 24 GiB free disk and 12 GiB available RAM. The launchers retain their actual size checks. A larger-than-budget extraction can still stop the run. [USB inventory](../../artifacts/evidence/board/g1-37564293/usb-inventory-and-hashes.txt) · [GBS root sizes](../../artifacts/evidence/native-run-r0012m-inventory-cleanup-smoke-20261125.txt) · [Extraction limits](../../artifacts/scripts/r0012c/image-tree.py.txt)

With these allowances the four start checks require 54, 59, 84 and **90 GiB** respectively when expressed against initial free space. Thus 135 GiB covers all four if K ≤45 GiB. A smaller actual retained footprint changes that bound; use df after each stage. If a gate fails, keep the kernel roots and receipts for review and report the measured shortfall. None of the commands below prunes a root.

In the same native Bash session, define the pinned launcher and free-space gate. The archived run commands use the existing captures under vd-tree. The only network traffic to GitHub is downloads. Steps 1–2 take minutes to tens of minutes; image can take hours; pilot uses one attended GBS job at a time, roughly 30–90 minutes.

```bash
pm12t() (
  set -eu
  cd /home1/chengkai/vd-tree
  p=0db8f90257b1f76a67208b82da92234f8102d9ce
  d=$(mktemp -d "$PWD/workspace/temp/pm0012t-launch.XXXXXX")
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0012t/next.sh.txt" -o "$d/run"
  printf '%s  %s\n' 9556607c280158caf57a6a568fc8454bfc1d958ff3ba2ffc2bf2a70b04a93049 "$d/run" | sha256sum -c -
  exec bash "$d/run" "$p" bceab9fc2dfdcadadc1186dcd5012e5c6007238d605e395d76a9075b690bb700 a984c67ad51ee218c32a0e138ee45d1dfc09ad31e1996a510bf89ebb16aca2a7 "$1"
)
space() (
  set -eu -o pipefail
  df -Pk /home1/chengkai/vd-tree/workspace/temp |
    awk -v required="$1" 'NR==2 {free=$4/1048576; printf "AVAILABLE %.2f GiB; planning minimum %d GiB\n",free,required; ok=(free>=required)} END {exit !ok}'
)
space 54 && pm12t gcc && space 56 && pm12t erofs
```

After erofs succeeds, paste its printed `export PM12_EROFS_RECEIPT=… PM12_EROFS_SHA=…` in that shell. Then run:

```bash
space 80 && pm12t image
```

At the completion handoff, use the exact path printed at image launch. The pilot validates the completion line again and checks the P4 ticket.

```bash
read -r -p 'Exact PM12_BATCH_DIR printed by this image launch: ' PM12_IMAGE_RUN
export PM12_IMAGE_RUN
grep ' DONE image rc=0$' "$PM12_IMAGE_RUN/status.txt" && space 62 && pm12t pilot
```
