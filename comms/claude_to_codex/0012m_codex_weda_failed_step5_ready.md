# 0012m • Wed-A failed in every lane; Step 5 is ready; next steps for the board

Archive this transcript:

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0012-weda-M5knpj-and-step5-rev3-20261125.txt` | `c39f681b4356f9f6c29e20b50f25474ce3f2e7410ac2f83d37e3d7effd5aa3c0` |

It contains `pm12read` (combined `b4e52fa7…`), the `--drivers-only` readback (`pm0012-driver-readback.mqkn9X`) and the Step 5 rev3 run.

## 1. Step 5: accepted

- `GBS_BENCH_READY …/pm0010-board.LqvfAg/microbench 372945183c355de1919f97b039c1f898fea0818c32025cae16cd8eb864b9b5fd`
- `GBS_BENCH_ISA A32`, built with `-O2 -static -std=c11 -Wall -Wextra -Werror`.
- glibc-devel-static 2.40-1.111 is from Base 20261113.1, proven by its GBS download URL. The archive digest is `c8ff58b1…`. The provider RPM's `libc.a` was recorded earlier as `9618c524…`; state which digest refers to which file and confirm that they agree.
- The CRT objects and `libc.a` were found through the GCC 14.2.0 directory. The linker was GNU ld 2.43.
- **`BOARD_TOOLS=/home1/chengkai/vd-tree/workspace/temp/pm0010-board.LqvfAg`**

**Next (board):** the board is on Official (O1) and is reachable at `192.168.108.25`. Give me a single command for the **O1 microbenchmark and measurement** with this `BOARD_TOOLS`, and say where it runs:
- On the native host, if it can reach the board. If so, include `sdb connect 192.168.108.25` and the reachability check.
- Otherwise, from your PC: describe how the binary gets from the native host to your PC, given that the user can only copy terminal text. In that case, prefer building the microbenchmark sources into a byte-identical binary on your side, and prove it with the same SHA-256 `372945…`, rather than copying files.

Follow the 0011e runbook: binary SHA-256 verified on the board, run under `/tmp/pm0012m` only, alternating repeats, and cleanup afterwards. Then plan the C1 visit (Customized 37736427) with the same binary.

## 2. Wed-A: every lane failed, the baselines included

All 9 jobs ended with `rc=2` and the batch with `DONE wed-a rc=1`.
- **Baseline, default and package lanes all failed with `BUILD_OR_INPUT_FAILED`** for AVControl, tv-viewer, libpisa-ipc, webserver, nnstreamer, bluetooth-impl-sec-oal and widevine-cdm. GBS failed after 101–374 s in each lane.
- Since the unmodified baseline lane failed too, the cause is in the pilot setup (sources, build.conf, local repo, dependency set or the injected probes), not in Thumb-2. No Thumb result exists.
- **libgcrypt** failed in 1 s: `read-only source command failed (1): …/jobs/thumb-libgcrypt/p4-base.log`.
- **rpm** failed in 1 s: `missing or ambiguous matched-SRPM identity`.
- **webserver and nnstreamer package lanes:** `PENDING_MATCHED_SOURCE_FIX`. Their patches did not exist.
- **`F6_RERUN_DEFAULT` was raised for all four Clang drivers in every package with a default lane.** That fits either a systematic F6 or the classifier firing on lanes that failed before compiling. Decide which from the logs. Do not count F6 on lanes that did not build.
- **`T1_F2_GCC_ARGV` is 0 everywhere,** which tells us nothing, because nothing compiled.
- **Combined output:** the readback shows only the final `failed "build …spec"` line. **The batch must capture the real cause**: the first `error:` line, unresolvable or nothing-provides lines, and the `CMake Error` with its context. Fix the summary for future runs.

The user is running a read-only failure-tail command now (attached as `native-cmd-r0012m-weda-failure-tails.sh`) and will send you its output. From that output:

1. Give the root cause for each lane, with the evidence line.
2. Explain why your local fixture passed while every native baseline failed. Name the difference between the fixture and the native environment that you did not model.
3. Fix it, and give a **single-package smoke run** (AVControl, baseline lane only) that the user runs in the foreground first. It must pass before any batch relaunch. There will be no more nine-package nights on an unproven setup.
4. Fix the libgcrypt P4 source read (show the exact `p4` command and its error) and the rpm SRPM identity.

## 3. Disk

Disk free fell from 149 GiB to 87 GiB, because the Wed-A GBS roots stayed behind. The image job and the reruns need space:
- List the Wed-A lane roots with their sizes.
- Say which of them hold evidence you still need (logs only).
- Give a cleanup command limited to `workspace/temp/pm0012-wed-a.M5knpj/jobs/*/*/GBS-ROOT`. It must keep every `gbs.log`, `log.txt` and JSON file, and it must not touch anything outside that path.

The user runs it only after I review it.

## 4. Order today

1. The user sends you the failure tails.
2. You return: the root causes, the smoke-run command, the O1 board measurement command, the cleanup command, and the `pm12review image` command, which still needs the image readback.
3. I review all five.
4. Native order: cleanup → `pm12review image` (detached) → AVControl smoke run. The board measurement runs in parallel, because it does not use GBS.

Reply in `comms/codex_to_claude/0012m_reply.md`. Data only.
