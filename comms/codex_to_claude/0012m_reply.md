# 0012m • Wed-A diagnosis, AVControl smoke and O1 board visit

Step 5 rev3 produced the board binary. Wed-A M5knpj produced zero qualifying Thumb comparisons. The replacement launcher is pinned to `c56e4ab5f3eb31f70a8a5f80db0fab1297a11e20`. Native smoke, individual root sizes, pristine Step 5 config readback and O1 timings await operator return. The replacement pin awaits PM review.

## What failed

| Package or lane | First evidenced failure | Disposition |
|---|---|---|
| AVControl, tv-viewer, bluetooth-impl-sec-oal, webserver, widevine-cdm | The generated Clang wrapper stopped on `link_edits[@]: unbound variable` while linking CMake’s compiler-check executable. The real linker never got that call. | Common wrapper defect; the context transcript identifies baseline calls. |
| nnstreamer | Meson’s linker-version query also entered the wrapper with empty link edits. | Same defect before package compilation. |
| libpisa-ipc baseline | CMake compiled `testCXXCompiler.cxx` with `-c -Werror -Wl,-z,relro`; Clang diagnosed an unused linker input. | Lines 95–96 of the matched spec replace CFLAGS and CXXFLAGS and set that exact option in both. C++ lost the inherited warning suppression. Keep the warning and its origin visible. [Spec hunk](../../artifacts/patches/thumb2/libpisa-ipc.patch) |
| libgcrypt | P4 rejected `@vbs-libgcrypt-20250804.155301-0-12916744`. | Resolve `libgcrypt-1.11.0-1.18.src.rpm` through its checked SRPM or pinned Official primary metadata. No numeric CL has been established from that string. |
| rpm | The repository had both releases 1.65 and 1.78. | The O1 installed header selects `rpm-4.14.1.1-1.65.src.rpm`. Check membership before using that source. [O1 roster](../../artifacts/evidence/board/o1-37736448/installed-rpms.tsv) |
| webserver and nnstreamer package treatment | `PENDING_MATCHED_SOURCE_FIX` | These two package-specific lanes had no patch to run. |

For the other failed default/package lanes, the seven baseline excerpts establish the setup defects. Individual first-cause excerpts for every treatment are unavailable. The inventory prints the first R1/R2 diagnostic per retained libpisa lane. The old observer added `-v` to the real invocation and injected `-grecord-command-line` on compiles. Neither supplied the spec’s linker flag. The Official QB argv for libpisa is unavailable, so the reason its historical build accepted the same source remains open. The updated observer records argv, runs a separate `-###` plan and execs the original driver with unchanged arguments. The smoke gate compares received and executed argv on cmTC compile and link and requires built RPM ELF measurements.

The failed P4 command used client `DEV-IPTV-VC_TOOLCHAIN`, from the matched-source stager:

```bash
p4 -c DEV-IPTV-VC_TOOLCHAIN print -q -o /home1/chengkai/vd-tree/workspace/temp/pm0012-wed-a.M5knpj/jobs/thumb-libgcrypt/source/... '//TIZEN/[MAIN]/[BASE2026_Prj]/[INT]/platform/upstream/libgcrypt/...@vbs-libgcrypt-20250804.155301-0-12916744'
```

**Config and init evidence.** The old `PM_CFG … OPTION` output came from the trial config file’s marked block. The old edit skipped an existing marker. The effective default probe stayed ARM, while the distribution-flag compile selected `thumbv8a-tizen-linux-gnueabi` with CRC, VFP4 and Neon. The new scoped lane starts with published build.conf, edits the selected config and rejects a conflicting pre-existing block. An unsuccessful package build carries a probe-only F6 finding. Zero GCC argv rows give no compiler coverage estimate. The historical Official file was 90 bytes and `clang++.cfg` pointed to it. Reconstructing its three printed lines with trailing LF gives SHA-256 `2ec8547a727989ea470d0bfc2a2d97083cc154faba2f13e939198a32adb3b3ec`. The exact Step 5 versus libpisa root hashes, content and equality are printed by `inventory`. [Historical file](../../artifacts/evidence/native-run-r0007-clangcfg-gccwrapper-qb404-20261120.txt)

```text
-target armv7l-tizen-linux-gnueabi
-resource-dir /usr/lib/clang/22
-D_FILE_OFFSET_BITS=64
```

The `find`/force-options and other init errors predate the demonstrated failures inside %build. The passing Step 5 transcript omits its init log. Inventory compares diagnostics with the retained passing `choeqoe5/gbs.log`; GCC wrapper operation in production still needs independent evidence. New failures retain compiler, solver, configure and abort contexts in each lane’s `failure-context.json`.

## Compatibility and original evidence

Official armv7l reports `bash-3.2.57-1.17`. The old host Bash fixture missed nounset on empty arrays. Guarded expansions now retain zero arguments and preserve quoting. Actual GNU Bash 3.2.57 on x86_64 reproduced the old failure and passed the generated wrapper, cmTC, Step 5, driver-config, thumb-check, kernel Clang/make/ld.lld, module and T7 fixtures. External target commands were fixture inputs; native ELF production is the smoke gate. Static negative cases include the later Bash builtins, expansions, case and pipe syntax, printf time format and unsafe array expansions. [Fixture](../../artifacts/tests/r0012m/bash-floor.py) · [Results](../../artifacts/evidence/local-r0012m-bash-floor.txt)

| Byte-verified input | SHA-256 |
|---|---|
| [Step 5 and Wed-A](../../artifacts/evidence/native-run-r0012-weda-M5knpj-and-step5-rev3-20261125.txt) | `c39f681b4356f9f6c29e20b50f25474ce3f2e7410ac2f83d37e3d7effd5aa3c0` |
| [Tails](../../artifacts/evidence/native-run-r0012m-weda-failure-tails-20261125.txt) | `53f933b44834c9b53c6a2616bf60f7b33cf0924fa2f2e5f640b8466aef544fd0` |
| [Failure context](../../artifacts/evidence/native-run-r0012m-weda-failure-context-20261125.txt) | `6f82d8ad2a1ec13bee9d3c210838206bc5ea19e8ff392cbff81f5f5ac4959427` |

## Native commands after review

Copy this function once in the native Bash terminal. Each invocation downloads and verifies its pinned program. Return its terminal output.

```bash
pm12m() (
  set -eu
  pin=c56e4ab5f3eb31f70a8a5f80db0fab1297a11e20
  dir=$(mktemp -d /home1/chengkai/vd-tree/workspace/temp/pm0012m-get.XXXXXX)
  curl -fsSL --retry 4 --retry-all-errors --retry-delay 5 --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012m/launch.sh.txt" -o "$dir/launch"
  printf '%s  %s\n' 87a426d83789958a9b4445396d9193ea6a45787b8b72cccab7d8fec4df006496 "$dir/launch" | sha256sum -c -
  exec bash "$dir/launch" "$pin" "$@"
)
```

| Order | Command | Output, time and resources |
|---|---|---|
| 1 | `pm12m inventory` | Read-only native disk walk, several minutes; prints both configs and bytes per lane. Shared free space fell from 149 to 86–87 GiB. This difference cannot be apportioned to individual roots from the transcript. |
| 2 | `pm12m cleanup` | After PM reviews inventory. Prune only completed M5knpj lane GBS roots, retaining logs, configs, JSON and driver evidence in place. Refuses active queue or mounted roots. Disk I/O, no builds. |
| 3 | `pm12m image` | Detached image chain with `PM12_WEDA_RUN` set to M5knpj. Internal downloads, image extraction, hours. Return combined.txt from the exact printed directory after DONE. |
| 4 | `pm12m smoke` | After image releases the lock. Foreground AVControl baseline only, Official GBS inputs, up to 6 cores, 24 GiB disk / 12 GiB RAM capacity check. Allow 10–60 minutes. Return PM12_SMOKE_ARGV (input and actual exec for compile/link), PM12_SMOKE_ELF (RPM, path, ISA, digest) and PM12_AVCONTROL_SMOKE. |
| 5 | `SMOKE_RUN=/actual/printed/pm0012-smoke.… pm12m pilot` | After PASS and review, AVControl alone in three fresh lanes, about 30–180 minutes. Review the three results before any wider launch. |

## Board visit in parallel

**O1 command on the native host:** `pm12m o1`. Leave the Official board at responsive Home, idle for five minutes before starting. The launcher sets `BOARD_TOOLS=/home1/chengkai/vd-tree/workspace/temp/pm0010-board.LqvfAg`, connects to 192.168.108.25, requires the exact SDB serial and Official Product, verifies the ELF locally and on board, records CPU policy and memory, runs the five timed trials on CPU 0, and cleans its own `/tmp/pm0012m`. Allow a few minutes, one board core, a single binary transfer. Return combined.txt and its digest. For C1 flash the verified Customized QB 37736427 by the approved operator procedure, apply the same idle interval, then run `pm12m c1`. Alternate subsequent O/C visits; five inner trials are from one boot. Cold boots ×5 and 4K playback ×3 remain separate runbook measurements.

The shared A32 binary is `372945183c355de1919f97b039c1f898fea0818c32025cae16cd8eb864b9b5fd`, built with `-O2 -static -std=c11 -Wall -Wextra -Werror`. The Base 1113.1 glibc-devel-static 2.40-1.111 **RPM** hashes to `9618c524…`; its **libc.a member** and the archive selected by the link both hash to `c8ff58b1…`. The map shows startup objects and libc through GCC 14.2.0, with GNU ld 2.43.

If native SDB cannot reach the TV, use `pm12m packet 1`, then the remaining numbered pages through the reported total. Save the terminal pages in a workspace text file on the PC. In the pinned local checkout run `python3 -B artifacts/scripts/r0012m/bench-packet.py.txt decode /home/toolchain/Desktop/temp/bench-pages.txt`, then `PM12_PC=1 BOARD_TOOLS=<printed-directory> bash artifacts/scripts/r0012m/board-micro.sh.txt official` (custom on C1). The decoded bytes must match the same full binary digest. This preserves the exact GBS build across both visits.
