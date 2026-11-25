# 0012q · AVControl pilot and matched PERF kernels

## Kernel size · Table A, bytes

| VDLinux, KantSU2E perf | Official MLGO · QB 37736448 | Custom MLGO · QB 37736427 | Custom − Official |
|---|---:|---:|---:|
| Text · boot kernel code | 8,563,712 | — | — |
| Data · boot rwdata | 681,984 | — | — |
| BSS · boot bss | 4,120,576 | — | — |
| Total · uImage file minus 64-byte header | 11,348,904 | 11,085,176 | −263,728 |
| rodata · boot | 1,679,360 | — | — |
| init · boot | 413,696 | — | — |
| U-Boot declared payload | 11,348,644 | 11,084,916 | −263,728 |
| uImage file | 11,348,968 | 11,085,240 | −263,728 |
| zImage file | 5,326,504 | 5,222,032 | −104,472 |
| tztv-kernel-perf RPM | 19,345,448 | 19,160,700 | −184,748 |

Boot rows express the kernel’s integer KiB readout in bytes. Their resolution is 1,024 B. Berkeley ELF sizes remain a separate measurement. The RPI Total definition remains unverified. Both fallback Total values include a 260-byte trailer beyond the header-declared payload. Both CRC-checked payloads match the respective expanded zImages. Custom boot rows await the C1 cold-boot line. The source-matched pair changes the LLVM Base. [Matched pair](../../artifacts/evidence/native-run-r0011-step2-pair-gate-20261124.txt) · [QB size receipts](../../artifacts/evidence/native-run-r0012m-pilot-and-r0012p-size-20261125.txt)

O1, boot ID `45fac48b-bc2b-4ba9-9b98-a75d0b5f3bf0`, log SHA-256 `b97c0c648cfbb5f7720a34d564977f416c33a096c42a1f694d29dc3461f83de5`. [Cold-boot log, line 48](../../artifacts/evidence/board/o1-37736448/cold/early-memory-log.txt#L48)

```text
[    0.046730] Memory: 1279556K/1631488K available (8363K kernel code, 666K rwdata, 1640K rodata, 404K init, 4024K bss, 29920K reserved, 311296K cma-reserved, 726272K highmem)
```

## AVControl and the kernel wrappers

| Pilot lane | .text B | Allocated B | ELF file B | A32 share | Native result |
|---|---:|---:|---:|---:|---|
| baseline | 736,944 | 1,055,461 | 2,386,562 | 99.98% | Built, NOT_DELIVERED |
| default | 441,362 | 758,644 | 2,088,630 | 0.95% | Built, NOT_DELIVERED |
| package | — | — | — | — | Cached clang++ ran in %install with PM12_RECEIPTS unset |

The default .text difference is −295,582 B (−40.1%). In the two successful builds the aggregate delivery decision can fail on compile or final-link evidence, DWARF coverage/options, unresolved response files, or the default driver-config check. The receipt returned by the native launcher prints only status, sizes and error. It does not identify which predicate failed. The package lane has a diagnosed %install failure. Applying that diagnosis to either built lane requires its own receipts. The readback below prints the failed predicates from experiment.json and the separate T1–T8 gates from thumb-acceptance.json when available. T1 includes source-to-CU and mode coverage. The retained pilot supplies no acceptance for the size reduction. [Original transcript](../../artifacts/evidence/native-run-r0012m-pilot-and-r0012p-size-20261125.txt) · [Delivery decision](../../artifacts/scripts/r0012/development.py.txt) · [T1–T8](../../artifacts/scripts/r0012e/thumb-accept.py.txt)

Wrapper commit `cf4e0e9962c5942e3f70cdb05502126b05070010`. RPM phases now share wrapper state in a stable build-directory location. The generated package and kernel wrappers recover their settings from that location even when CMake calls an absolute cached driver in a new shell. Kernel clang, make and ld.lld preserve their argument vectors, including response-file arguments. The local fixture passed separate %prep, %build, %install and %check invocations and two rpmbuild -bb runs under Bash 3.2.57, with the compatibility checks for coreutils 6.9 and gawk 3.1.5. Fixture drivers stand in for native builds. The new native pilot and kernel batch have yet to run. Claude review requested. [Fixture](../../artifacts/tests/r0012q/stages.py) · [Test output](../../artifacts/evidence/local-r0012q-rpm-stages.txt)

**Kernel launcher after review and successful image scan.** Native foreground terminal, one GBS job at a time. Allow overnight or longer for six serial GBS lanes. Up to six pinned cores, with the 55 GiB disk and 16 GiB RAM gate per lane. Dependencies and source come from the internal services. The image dependency is the explicit run reported by the operator.

```bash
(
  set -eu
  cd /home1/chengkai/vd-tree
  export PM12_IMAGE_RUN="$PWD/workspace/temp/pm0012-image.6nhIbn"
  export PM12_SMOKE_RUN="$PWD/workspace/temp/pm0012-smoke.neJb0i"
  p4 login -s
  pin=cf4e0e9962c5942e3f70cdb05502126b05070010
  d=$(mktemp -d "$PWD/workspace/temp/pm0012q-get.XXXXXX")
  curl -fsSL --retry 4 --retry-all-errors --retry-delay 5 --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012/batch.sh.txt" -o "$d/batch"
  printf '%s  %s\n' ad3eb1ee6d01e6848adb3a05fd4ecfe4d10589768f38a4f41c68a65a0c35bf35 "$d/batch" | sha256sum -c -
  exec bash "$d/batch" attended "$pin" bd88ae61ed3380b3609ec145f9bc4bc690f85771840503b1f5ea6d998256acab kernel
)
```

## Native readback · delivery, directory listings and replay ranges

The two canonical debug RPM paths did not yield a kernel ELF in either QB. Repository-wide publication is still open. The shipped payload GNU IDs are `419813f26f2d03bee00bde1d7173b0c2fd887530` and `4d95bb9eb9dc71983a87f90352fc8c2b7bd8a006`. The GBS IDs start `e0b8e` and `33f711d0d`; equality of file sizes cannot qualify either replay. The native helper records HTTP outcomes, actual directory entries, matching debug RPM candidates and ELF IDs. It maps replay section LMAs back to verified flat bytes and records every mismatch with its start and exclusive end offset. Only a verified note digest or a same-position, same-length Linux banner can qualify as an exception. Any other changed byte keeps that lane’s replay section sizes out of Table A. Full ranges and directory lists stay in the printed workdir. The native-only records are unavailable on the PC. [Readback code](../../artifacts/scripts/r0012q/native-readback.py.txt) · [Python 3.10 range and listing fixture](../../artifacts/tests/r0012q/readback.py)

**Read-only native launcher after review.** One CPU process, no GBS, sudo, board access or shared build lock. Allow several minutes for metadata and retained payloads; a responding debug repository can extend the run and require up to 1 GiB per candidate RPM plus extracted ELF space. Return the terminal summary. The optional packet reader takes an absolute directories.json or ranges.tsv.gz from the printed lane directory and a 1-based part number.

```bash
(
  set -eu
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0012q-get.XXXXXX")
  export TMPDIR="$d"
  pin=684b7c0bab63ecc4d1166cb73b37d6a7fc6cb0ac
  get() {
    f=${1##*/}
    curl -fsSL --retry 4 --retry-all-errors --retry-delay 5 --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/$1" -o "$d/$f"
    printf '%s  %s\n' "$2" "$d/$f" | sha256sum -c -
  }
  get r0012p/kernel-size.py.txt 50d0afd9a687fd0dce6506fd76eb5e87a9cc16295ee46b7d0c128a5cae9ae564
  get r0012q/native-readback.py.txt 6f9f6260740d06829925405c75ad54294cfe94db8726ba04b2eb03f444670ab6
  exec python3 -B -u "$d/native-readback.py.txt"
)
```

## Board evidence and signed workloads

C1 awaits operator confirmation that Home is idle for five minutes after the Custom cold boot. First collect the entire boot Memory line and verify boot ID, product 20261123.1 and the Custom running kernel ID. Then return Table A, collect shipped BTF hash, six-column RPM roster, three idle samples a minute apart, and the slot and p5/p6 image-prefix evidence. A journal entry must refer to the current boot. If the ring has rolled over, use a retained same-boot serial or journal line. Neither prior GBS measurements nor a previous QB boot fills a missing cell.

The O1 installed roster lists gzip 1.3.12 and xz 5.8.1. C1 executable discovery, RPM ownership, exact binary/library hashes, execution checks and affinity precede the timing. Planned repeatable workload per available tool: create 16 MiB of zero bytes in a unique authorized scratch directory under /tmp, verify input length 16,777,216 B and SHA-256 `080acf35a507ac9849cfcba47dc2ad83e01b75663a516279c8b9d243b719643e`, then run five timed trials each of `taskset -c 0 gzip -n -6 -c "$input" >/dev/null` and `taskset -c 0 xz -T1 -3 -c "$input" >/dev/null` as the SDK user. Record installed versions, CPU governor/frequency, thermal and Home state, trial wall times, median, range and coefficient of variation. Apply the same input, settings and ordering on O2. Report any missing tool, unsupported option or refused execution separately. O1 has zero signed-workload timings. An installed executable can come from any toolchain; the source gate established the release advisors for the kernel. A difference in these workloads measures the whole-board result of the Base swap. Tool and library identity, plus the Base proof, constrain narrower attribution. [O1 roster](../../artifacts/evidence/board/o1-37736448/installed-rpms.tsv) · [O1 execution evidence](0012o_reply.md)

Input SHA-256 `6d818ebe45b05729b2173c1a11f00e02c1c8a4926e8baf8249666d20b92202f4`. Native pilot predicates, directory coverage, replay ranges and all C1 measurements are open.
