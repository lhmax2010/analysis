# 0012j · KantSU2E O1 · 24 November 2026

**Official QB 37736448 confirmed on the board.** SDB from the PC reached `192.168.108.25:26101`. The operator reported flashing the verified USB bundle. Two independent byte checks distinguish this lane from Customized QB 37736427.

| Evidence | Board | Official capture | Customized capture |
|---|---|---|---|
| Actual `/etc/prd_info.ini` | Product `20261123.2`, perf, SHA-256 `8524ea1e…edb3d` | `8524ea1e…edb3d` | `2fd15451…a349e1`, Product `20261123.1` |
| Actual `/lib/modules/6.12.60/kernel/vmlinux` (raw BTF) | `a4cf6f3b…7e810d` | `a4cf6f3b…7e810d` | `2aecd204…6d353` |
| uImage / zImage in the board RPM database | `eb458b69…` / `f8530555…` | Both match | `12d21cf5…` / `5481cf2e…` |
| Published Base for this Product | Board Product joined to the QB publication | `20261113.1` | `20261118.1` |

Running kernel GNU build ID `419813f26f2d03bee00bde1d7173b0c2fd887530`. Linux 6.12.60, `abuild@A1106DJG`, clang and LLD 22.1.8, SMP PREEMPT, built 23 Nov 06:24:04 UTC. Board BUILD_ID `T-KSU2EJAKUC-0101-PERF-202611232029`. The USB and BTF matches establish lane identity. The matched-QB linked ELF was unavailable in the capture. The separate GBS replay build-ID comparison is included in the native join below. [Board product and kernel RPM](../../artifacts/evidence/board/o1-37736448/kernel-receipt.txt) · [Actual BTF and process stat](../../artifacts/evidence/board/o1-37736448/linked-layout.txt) · [Release files and running notes](../../artifacts/evidence/board/o1-37736448/identity.txt) · [USB digests](../../artifacts/evidence/native-run-r0011c-chain-AFkXQV-20261124.txt) · [QB kernel digests and replay](../../artifacts/evidence/native-run-r0011f-batch-xkHDpd-20261124.txt) · [Published inputs](../../artifacts/evidence/native-run-r0011-step2-pair-gate-20261124.txt)

## Installed software

The sorted six-column RPM roster contains **2,342 rows**, SHA-256 `9ddc02f5d7c6cb3fa328e31e5422b016ec2ddb82ba182b3aa4514d5cb1d7f3da`. The Official Product catalog has 5,880 rows covering available RPMs. An installed-image difference count requires the authenticated EROFS roster. The Product difference count requires the native catalog rows. Both counts remain unmeasured here. Of the four kernel RPM rows returned for the Official Product, the board matches every identity field of tztv-kernel-perf. The tztv-kernel, -devel and -release rows are catalog-only on O1. The native join reports membership in each direction, preserving multiplicity. A Product-only row can be an available package omitted from the image. [Board roster](../../artifacts/evidence/board/o1-37736448/installed-rpms.tsv)

## Running kernel configuration

| Requested symbols | Board result |
|---|---|
| THUMB2_KERNEL, ARM_UNWIND, FRAME_POINTER | Unavailable |
| CC_OPTIMIZE_FOR_*, KALLSYMS*, FUNCTION_TRACER, KPROBES, MODULES | Unavailable |
| CMA*, CC_VERSION_TEXT, CLANG_VERSION | Unavailable |

A root read confirmed that `/proc/config.gz` is absent. The running compile string supplies clang 22.1.8. Live CMA counters are available. The effective configuration prerequisite for the kernel trial stays open. [Root path check](../../artifacts/evidence/board/o1-37736448/kernel-receipt.txt)

## Memory layout

| Quantity | O1 |
|---|---:|
| DRAM layout identified by the boot configuration | 2 GiB (`kantsu2e-2.0G-Builtin`) |
| Linux System RAM, three banks | 687.25 + 394 + 512 = 1,593.25 MiB |
| Outside Linux System RAM on the 2 GiB layout | 454.75 MiB |
| Named vendor regions outside System RAM, union by address | 454.00 MiB inclusive of the 48 MiB secure_os region starting at zero; residual 0.75 MiB |
| Reserved at boot, excluding the separately reported CMA | 29,920 KiB |
| Present RAM minus managed RAM after freeing initmem (7,379 pages × 4 KiB) | 29,516 KiB |
| Linux MemTotal | 1,601,972 KiB (1,564.43 MiB) |
| 15 reusable reserved-memory pools | 304 MiB, all inside System RAM; CmaTotal 311,296 KiB |
| CMA as sampled during inventory | 13,140 KiB free, 2,724 KiB DMA-used, 295,432 KiB user-used |
| zram0 swap as sampled | 1,041,012 KiB logical, 108,284 KiB used; physical memory 34,611,200 bytes |

Normal zone present/managed pages 148,480/141,101; HighMem 181,568/181,568; Movable 0/0; CMA 77,824/77,824. In the vendor interval union, overlapping entries at address zero are counted once. The cold-boot ring buffer reported 1,279,556/1,631,488 KiB available at 0.047 s, 29,920 KiB reserved and 311,296 KiB cma-reserved. It recorded the release of 404 KiB initmem at 0.357 s; 29,920 − 404 = 29,516 KiB. [Cold-boot kernel log](../../artifacts/evidence/board/o1-37736448/cold/early-memory-log.txt) The System RAM and managed-page totals reconcile independently using iomem, zoneinfo and meminfo. Recorded VM counters include pgpgin 362,219, pswpin 18,224 and file/anon workingset refaults 354/18,242. [Command line](../../artifacts/evidence/board/o1-37736448/cmdline.txt) · [System RAM](../../artifacts/evidence/board/o1-37736448/iomem.txt) · [Vendor regions](../../artifacts/evidence/board/o1-37736448/vendor-memory.tsv) · [Reserved pools](../../artifacts/evidence/board/o1-37736448/device-tree.tsv) · [Zones](../../artifacts/evidence/board/o1-37736448/zoneinfo.txt) · [VM counters](../../artifacts/evidence/board/o1-37736448/vmstat.txt) · [zram](../../artifacts/evidence/board/o1-37736448/swap.txt)

**1 GiB projection.** Holding the 454.75 MiB outside Linux fixed leaves **569.25 MiB** of System RAM. If the 29,516 KiB present-to-managed gap also stays fixed, **553,396 KiB (540.43 MiB)** remains managed by Linux, including reusable CMA. With all 304 MiB of CMA retained, the managed portion outside CMA would be **236.43 MiB**. The board shows user pages in CMA. Actual userspace headroom also depends on kernel allocations, active DMA, reclaim and the 1 GiB bank layout. A 1 GiB idle MemAvailable value requires a measurement.

## Cold boot and idle

The operator cold-booted the board and estimated about 10 s to a responsive Home without a stopwatch. SDB confirmed a new boot, `45fac48b-bc2b-4ba9-9b98-a75d0b5f3bf0`, and the same Official Product. Sampling offsets are measured from receipt of the operator confirmation, so the first sample had at least five minutes at Home. [Operator confirmation](../../artifacts/evidence/board/o1-37736448/cold/home-receipt.json) · [Boot identity](../../artifacts/evidence/board/o1-37736448/cold/confirmed-product.txt)

| Sample | MemTotal | MemFree | MemAvailable | Cached | Shmem | Slab | KernelStack |
|---|---:|---:|---:|---:|---:|---:|---:|
| Post-flash snapshot, uptime 1,454.33 s (KiB) | 1,601,972 | 74,248 | 1,033,704 | 954,496 | 6,500 | 92,144 | 6,144 |
| Home +5 min | 1,601,972 | 219,808 | 1,082,736 | 856,460 | 5,208 | 92,148 | 6,092 |
| Home +6 min | 1,601,972 | 216,616 | 1,080,224 | 857,060 | 5,216 | 92,348 | 6,240 |
| Home +7 min | 1,601,972 | 220,836 | 1,084,480 | 857,020 | 5,172 | 92,576 | 6,220 |

In the post-flash snapshot, 109 processes returned a PSS reading. The largest five were `DN_g.tizen.menu` (51,328 KiB), `wrt-loader` (45,510), `TA_native-home` (38,285), `DN_function-osd` (24,687) and `home-mainhub` (17,509). With CLK_TCK 250, the mainhub process started at 3,504 ticks (**14.016 s** since kernel boot) and native-home at 649 ticks (**2.596 s**). Operator-observed Home readiness is a separate endpoint. [All 25 ranked processes](../../artifacts/evidence/board/o1-37736448/postflash/top25.tsv) · [Raw PSS and start ticks](../../artifacts/evidence/board/o1-37736448/postflash/idle-1-pss.tsv) · [Executable identities](../../artifacts/evidence/board/o1-37736448/process-candidates.tsv)

Cold-boot samples provided PSS for 113, 114, 113 processes, respectively. Across all three samples, home-mainhub PID 1618 started at **19.764 s** after kernel boot and TA_native-home PID 486 at **3.156 s**. Start times use field 22 of /proc/PID/stat divided by the live CLK_TCK. [Full top 25 for each sample](../../artifacts/evidence/board/o1-37736448/cold/top25-per-sample.tsv) · [Sample starts and runtime](../../artifacts/evidence/board/o1-37736448/cold/sample-timing.tsv)

| Rank | +5 min · PSS KiB | +6 min · PSS KiB | +7 min · PSS KiB |
|---|---|---|---|
| 1 | wrt-loader · 45,626 | wrt-loader · 45,623 | wrt-loader · 45,624 |
| 2 | TA_native-home · 44,423 | TA_native-home · 44,411 | TA_native-home · 44,528 |
| 3 | DN_g.tizen.menu · 31,355 | DN_g.tizen.menu · 31,363 | DN_g.tizen.menu · 31,375 |
| 4 | enlightenment · 17,613 | enlightenment · 17,612 | enlightenment · 17,609 |
| 5 | home-mainhub · 17,250 | home-mainhub · 17,245 | home-mainhub · 17,249 |

## Thumb-target payloads

61 ELF paths have full SHA-256, byte sizes, owner names and ELF header bytes in the ledger, including aliases. The seven requested target families are represented. These hashes identify the shipped files. Instruction-mode attribution requires the matching image scan. [Full path and hash list](../../artifacts/evidence/board/o1-37736448/target-hashes.tsv)

| Selected path | Bytes | SHA-256 prefix |
|---|---:|---|
| `/bin/rpm` | 18,244 | `ac69255c1493b5a7` |
| `/usr/apps/org.tizen.AVControl/bin/AVControl` | 1,061,724 | `fa474d0ea3a18677` |
| `/usr/apps/org.tizen.tv-viewer/bin/tv-viewer` | 6,719,102 | `ac95b4f07e7277b2` |
| `/usr/apps/org.tizen.tv-viewer/bin/tvcontrol-notify-manager` | 416,180 | `6592c8993508bcef` |
| `/usr/apps/org.tizen.webserver/bin/webserver` | 63,552 | `b5f6f22efc144fc6` |
| `/usr/lib/gstreamer-1.0/libnnstreamer.so` | 308,672 | `3fa1439aed6f947f` |
| `/usr/lib/libgcrypt.so.20.5.0` | 893,448 | `b2e850554fdb7866` |
| `/usr/lib/libnnstreamer.so` | 308,672 | `3fa1439aed6f947f` |
| `/usr/lib/libpisa-ipc.so` | 1,606,448 | `3e5b6ecc27a5a5ef` |

## Native comparison for Claude review

Run on the native server after the Official image job. Read-only against the captures, one core, typically seconds, less than 2 MiB of result files plus about 200 KiB of downloads; no board access. Full set differences and per-target comparisons stay beside the script. For the target comparison, symlinks are resolved relative to the captured filesystem.

```bash
(
set -eu
cd /home1/chengkai/vd-tree/workspace/temp
w=$(mktemp -d "$PWD/pm0012j-board.XXXXXX"); cd "$w"
base=https://raw.githubusercontent.com/lhmax2010/analysis/94c3ea37616080cb8e4c4b07c43871b99d7cb104/artifacts
get() { curl --fail --silent --show-error --location --retry 4 --retry-all-errors --connect-timeout 12 "$base/$1" -o "${1##*/}" && printf '%s  %s\n' "$2" "${1##*/}" | sha256sum -c -; }
get scripts/r0012j/compare-o1.py d9ff8f8bc1bb9b4a6f2a415523bd84e039339680b7a28189cd59a29829174ebe
get evidence/board/o1-37736448/installed-rpms.tsv 9ddc02f5d7c6cb3fa328e31e5422b016ec2ddb82ba182b3aa4514d5cb1d7f3da
get evidence/board/o1-37736448/target-hashes.tsv 9e326039bcb7ef2a3ea4b0994c69e5a0f2bdeefa9a7b4662c1a5931676ea23cc
python3 -B compare-o1.py
)
```

SDB was restored to uid 5001. The board remained on Official; the collector created no board files. [Checksums for each readout](../../artifacts/evidence/board/o1-37736448/SHA256SUMS)
