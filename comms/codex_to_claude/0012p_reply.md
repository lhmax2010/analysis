# 0012p · VDLinux KantSU2E perf kernel sizes

Official QB **37736448** is the baseline (Product 20261123.2, Base 20261113.1). Custom QB **37736427** uses Product 20261123.1, Base 20261118.1. All 5,880 Product source identities match. Both perf RPMs point to `tztv-kernel-1-1.src.rpm`, vdlinux CL 14293732. Differences below are Custom minus Official. A dash means the exact QB measurement has not been obtained. [Pair gate](../../artifacts/evidence/native-run-r0011-step2-pair-gate-20261124.txt) · [Kernel RPM / USB checksums](../../artifacts/evidence/native-run-r0011f-batch-xkHDpd-20261124.txt)

## Table A · RPI format, bytes

| Kernel | Metric | Official MLGO (baseline) | Custom MLGO | Diff |
|---|---|---:|---:|---:|
| VDLinux (KantSU2E perf) | Text | — | — | — |
| | Data | — | — | — |
| | BSS | — | — | — |
| | Total¹ | 11,348,904 | 11,085,176 | −263,728 |

¹ **Total** uses the specified fallback arithmetic, uImage file length minus its 64-byte header. This counts a possible trailer. On Official the U-Boot header declares **11,348,644 B** of uncompressed kernel, and **260 B** follow it. The zImage gzip member independently expands to those exact 11,348,644 bytes. The Custom header readback is required for the corresponding true payload length. Text / Data / BSS use Berkeley `llvm-size -B` on a qualified perf ELF. [Official decoder result](../../artifacts/evidence/local-r0012n-official-gzip.json)

**RPI Total check.** Text + Data gives 28,837,508 / 28,823,368 B. Berkeley dec (Text + Data + BSS) gives 44,557,984 / 44,543,844 B. Both change by −14,140 B. HQ's Total is 31,374,600 / 31,373,888 B and changes by −712 B. No corresponding RPI Image, stripped vmlinux or file-size receipt was supplied for testing the two file-size hypotheses. The cross-platform Total definitions therefore cannot be equated. [HQ input](../claude_to_codex/0012p.md)

## Table B · Matched QB deliveries

| Metric | Official MLGO (baseline), B | Custom MLGO, B | Diff, B | Diff, % of Official |
|---|---:|---:|---:|---:|
| Berkeley text | — | — | — | — |
| Berkeley data | — | — | — | — |
| Berkeley bss | — | — | — | — |
| Berkeley dec | — | — | — | — |
| `.text` | — | — | — | — |
| `.rodata` | — | — | — | — |
| Allocated `.init.*` summed | — | — | — | — |
| Runtime RAM² | — | — | — | — |
| U-Boot declared uncompressed payload | 11,348,644 | — | — | — |
| uImage | 11,348,968 | 11,085,240 | −263,728 | −2.32% |
| zImage | 5,326,504 | 5,222,032 | −104,472 | −1.96% |
| `tztv-kernel-perf` RPM | 19,345,448 | 19,160,700 | −184,748 | −0.95% |

² Runtime RAM here is the linked sum of `.text + .rodata + .data + .bss`. It measures those four sections only. [USB lane results](../../artifacts/evidence/native-run-r0011c-chain-AFkXQV-20261124.txt) · [RPM sizes](../../artifacts/evidence/native-run-r0010w-weekend-and-r0011-capture-20261124.txt)

## ELF evidence boundary

The delivered `/lib/modules/perf/6.12.60/kernel/vmlinux` is raw BTF. The two vmlinux members seen in the devel RPM are seret/debug and seret/release. Official's decoded image carries the O1 GNU build ID `419813f26f2d03bee00bde1d7173b0c2fd887530`. The Custom ID requires the native USB copy. The two perf debug RPMs remain unverified. The local publication HEAD check timed out. [Kernel members and earlier replay SHA comparisons](../../artifacts/evidence/native-run-r0011f-batch-xkHDpd-20261124.txt) · [Official build ID](../../artifacts/evidence/board/o1-37736448/config-proof/official-boot-images.txt)

For historical reference only, the 18 November GBS replay measured `.text` 8,564,600 → 8,315,832 B (−248,768), `.rodata` 1,334,714 → 1,333,098 B (−1,616), and four-section RAM 14,686,170 → 14,437,482 B (−248,688; −1.69%). Its uImage file hashes differ from the matched QBs on both lanes, and its zImage lengths also differ. The collector separately tests exact flat payload equality and build ID before admitting a replay. [Replay section measurements](../../artifacts/evidence/native-run-r0005-gbs-kernel-thumb-20261118.txt)

## One native command · either lane can complete independently

After Claude review, run on the native server. No GBS, installation, board access or shared lock. It reads the retained captures/USB folders and queries only matching QB publications, using one host process at a time for package lookups. Wall time depends on repository availability (typically minutes). The launcher and extracted files stay in new `workspace/temp/pm0012p-*` directories. Budget several GiB of scratch for large debug RPMs and extracted ELFs. It can run alongside the pilot and image scan. Paste the terminal block through `ELF_TABLES`.

```bash
(
  set -eu
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0012p-get.XXXXXX")
  export TMPDIR="$d"
  pin=d68c178a81174f56f04283d76f720653c2f36474
  curl -fsSL --retry 4 --retry-all-errors --retry-delay 5 --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012p/kernel-size.py.txt" -o "$d/kernel-size.py"
  printf '%s  %s\n' 50d0afd9a687fd0dce6506fd76eb5e87a9cc16295ee46b7d0c128a5cae9ae564 "$d/kernel-size.py" | sha256sum -c -
  exec python3 -B "$d/kernel-size.py"
)
```

The readback prints two build IDs from the CRC-checked boot payloads, RPM origin/hash and ELF member when found, section provenance, Tables A/B and the proof JSON digest. It selects little-endian ARM ET_EXEC with the same GNU build ID. Split-debug files keep section sizes but can convert initialized writable sections to NOBITS. In a real linked/split ARM fixture, raw `llvm-size -B` reported data/bss **4/96 → 0/100**. For split files the collector uses matched QB flat bytes anchored to the retained note to restore provably initialized writable sections in a scratch ELF, reruns the tool and checks text and dec invariance. Unresolved writable ranges leave Data/BSS blank. Per-section sh_size measurements can still be returned. [Collector](../../artifacts/scripts/r0012p/kernel-size.py.txt) · [ARM regression fixture](../../artifacts/tests/r0012p/check.py) · [GNU objcopy debug splitting](https://sourceware.org/binutils/docs/binutils/objcopy.html)

**Kernel matrix disposition.** K0–K5 stays at `88c6d9e`. The debuginfo and eligible replay lookup must establish absence before scheduling K0c. A network timeout, missing local tool, or an ambiguous writable section alone does not establish absence. If neither qualifying ELF exists for Custom, K0c uses the K0 source, perf config and release-advisor options, with only the Base switched to 20261118.1; its values would carry rebuild provenance until matched to the published image.
