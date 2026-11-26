# 0012y · native EROFS retry

**Native Bash, after Claude review.** GCC finished. This definition replaces the previous terminal function. Allow 56 GiB free, up to two build jobs, intranet-local retained images and outbound source downloads. Allow 10–45 minutes, depending on download and storage throughput. The command builds the private tools, runs the byte fixture and reads both partitions of the retained Official 37736448 and GCC 37564293 images. Full compressor output stays inside the launcher directory.

```bash
pm12t() (
  set -eu
  cd /home1/chengkai/vd-tree
  p=5a692bca11e88830955df5c174bd0675bc2da5cb
  d=$(mktemp -d "$PWD/workspace/temp/pm0012y-launch.XXXXXX")
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0012t/next.sh.txt" -o "$d/run"
  printf '%s  %s\n' 7e6fa49eb63c1915f11d98c683f01ff61496e5e8c287e98900c9792ce913f968 "$d/run" | sha256sum -c -
  exec bash "$d/run" "$p" 34007ce035d5d89b9f21ab7baed085f6e68a6949fc97286ca6f48906abd66707 a984c67ad51ee218c32a0e138ee45d1dfc09ad31e1996a510bf89ebb16aca2a7 "$1"
)
pm12t erofs
```

A successful run prints four partition headers, two SOURCE_COMPRESSORS summaries and the verified tool receipt export. Paste that export into the same terminal and run `pm12t image` (80 GiB planning minimum). After its exact `PM12_BATCH_DIR/status.txt` ends in `DONE image rc=0`, export that directory as `PM12_IMAGE_RUN` and run `pm12t pilot` (62 GiB). Both still use the prior image pair.

**Diagnostic distinction.** The failing parser at 0db8f90 already guarded its unknown-mask error with `incompat & 2`. A complete incompat value of 0x180 cannot produce the observed exception in that revision. The previous fsck diagnostic reports *unrecognized bits* 0x180, which need not equal the complete field. The transcript does not identify the failing partition or show its raw bytes. The new reader reports the partition offset and superblock bytes and interprets 0x10 as distance 16 only when COMPR_CFGS is clear. With COMPR_CFGS set, an unsupported algorithm remains an error. The readback distinguishes those cases before publishing the receipt. [Original transcript](../../artifacts/evidence/native-run-r0012t-gcc-erofs-20261126.txt)

**Local tests.** Python 3.10.12 decoded (incompat, union) = (0x180, 0x10) at a nonzero partition offset; (0x182, 0x10) failed closed and (0x182, 9) decoded the LZ4 and Zstd records. On three real mkfs images the pinned upstream dump reported respectively 0, 1 and 1 compressed files. The plain partition reported file compression “none”; the legacy LZ4 partition reported distance 65535; the Zstd partition reported algorithm bitmap 8. This census describes reachable files. Native production results require the four actual partition headers and tool output. [Fixture](../../artifacts/tests/r0012y/compression.py)

## GCC config and tonight’s kernel relaunch

GCC USB verified with build ID `137d01259d95739d5eb71e468bf289ee467a65b0`, uImage 12,218,608 B, zImage 5,664,248 B, RPM 20,018,029 B. The same two kernel hashes were measured on G1’s operator-prepared USB. The new USB folder has its own manifest. [G1 measurements](0012u_reply.md)

I independently decoded the Official → GCC packet and verified SHA-256 `0694a479f529e795de2b503ae6058012b6a17989e03b866f957b2d282c9bff77`. There are 34 differing symbols. Three are MLGO, six are disabled on the one side where they occur, and 25 describe the compiler, assembler, linker, warning syntax or capabilities (including HAVE_CFI_ICALL_NORMALIZE_INTEGERS_CLANG). The enabled user-selected settings for optimization level, Thumb, unwinding, LTO, CMA, HIGHMEM and preemption match. MLGO is the intentional functional exception. The different toolchains, Product/Base snapshots and compiler capabilities still matter for the GCC comparison.

| vdlinux base CL 14293732, shelf 14427407 | Effective setting |
| --- | --- |
| linux-6.12/arch/arm/configs/KANTSU2E_perf_defconfig:33 | CONFIG_MLGO=y in Official |
| linux-6.12/init/Kconfig:193, 202, 207 | MLGO parent, MLGO_INLINER and MLGO_REGALLOC children. Both children depend on MLGO. |
| linux-6.12/Makefile:1066–1070 | Each child selects a KBUILD_CFLAGS pair, respectively `-mllvm -enable-ml-inliner=release` and `-mllvm -regalloc-enable-advisor=release`. |

These flags reach kernel C translation units and in-tree modules through Kbuild. K2/K3 change only the parent in the perf defconfig, using the canonical `# CONFIG_MLGO is not set` spelling. Generated config must have the parent off, children off/absent and zero other changes against Official. K0→K2 and K1→K3 print MLGO_TU_DELTA from actual kernel/sched/core.c command files. Both release pairs must disappear; both effective LLVM option diagnostics must read default. Actual lane results remain pending. [Shelved source readback](../../artifacts/evidence/native-run-r0005-20261118.txt) · [Spec and argv fixture](../../artifacts/tests/r0012y/mlgo-off.py)

**Tonight, native foreground** after gcc/erofs/image/pilot releases the shared lock. The retained OwlD9Q source and the 0012w GBS HEAD spec preflight are in this pin. Allow six cores, 55 GiB free before each lane, 16 GiB available RAM and interactive sudo; reserve the overnight window. The local rpmbuild fixture exercised all four RPM stages with Bash 3.2.57, and a separate fixture executed both off-lane defconfig edits and checked the paired TU flags and config-drift rejection.

```bash
(
set -eu -o pipefail
cd /home1/chengkai/vd-tree
p=5a692bca11e88830955df5c174bd0675bc2da5cb
d=$(mktemp -d "$PWD/workspace/temp/pm0012w-launch.XXXXXX")
export PM12_REUSE_KERNEL_JOB="$PWD/workspace/temp/pm0012-kernel.OwlD9Q/jobs/kernel-thumb"
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0012r/reviewed-run.sh.txt" -o "$d/run"
printf '%s  %s\n' 2afd47e386fa3d4f95f0271bb5136c6eb874c84963570acba1dae95af63e1d38 "$d/run" | sha256sum -c -
rc=0
bash "$d/run" "$p" 34007ce035d5d89b9f21ab7baed085f6e68a6949fc97286ca6f48906abd66707 a984c67ad51ee218c32a0e138ee45d1dfc09ad31e1996a510bf89ebb16aca2a7 kernel | tee "$d/launch.log" || rc=$?
job=$(awk '$1=="PM12_BATCH_DIR"{print $2;exit}' "$d/launch.log")
if [[ "$job" == "$PWD/workspace/temp"/pm0012-kernel.* ]]; then
  tail -n 6 "$job/status.txt" || :
  grep -E '^(RETAINED_|GBS_GUESS_SPEC|GBS_SOURCE_REUSED|GBS_SPEC_PREFLIGHT|GBS_START|GBS_EXIT|MLGO_TU_DELTA|KERNEL_THUMB_LANE|KERNEL_THUMB_BLOCKED)' "$job/jobs/kernel-thumb/job.log" | cut -c1-800 | head -80 || :
fi
exit "$rc"
)
```
