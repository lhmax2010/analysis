# Tonight · K0–K5 on the native server

```bash
(
set -eu
cd /home1/chengkai/vd-tree
p=b019f7611394ffce25152df17295612f8ea73f42
d=$(mktemp -d "$PWD/workspace/temp/pm0012t-launch.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0012r/reviewed-run.sh.txt" -o "$d/run"
printf '%s  %s\n' 2afd47e386fa3d4f95f0271bb5136c6eb874c84963570acba1dae95af63e1d38 "$d/run" | sha256sum -c -
exec bash "$d/run" "$p" 810ed3917b082d78fc54b7ca6557d03f39099aa0f661daeca6f3048df1fa0897 a984c67ad51ee218c32a0e138ee45d1dfc09ad31e1996a510bf89ebb16aca2a7 kernel
)
```

Native Bash terminal after PM review. Valid P4 ticket and interactive sudo. Six serial GBS builds, up to six pinned cores, overnight or longer. The 55 GiB disk / 16 GiB memory capacity check runs before each lane. Source and dependency downloads use the intranet. Keep the printed `PM12_BATCH_DIR` for readback.

`pm0012-image.mKv04z` recorded `JOB sources END rc=0` at 20:43:57 +08. The kernel consumes that job’s single `native-proofs.json`, the pinned Official config and matched captures, and the four-stage AVControl smoke receipt from `pm0012-smoke.neJb0i`. It checks the SRPM spec and model evidence in the receipt. The platform/HQ extraction status has been removed from the launch gate. The one deferred measurement is the build and compatibility check of **externally shipped modules selected by installed RPM ownership**. In-tree module measurement, K0 image/config qualification, effective compiler/linker and outliner gates remain active. Kernel completion with an external-module deferral leaves that part of acceptance open. [Native status](../../artifacts/evidence/native-run-r0012r-image-mKv04z-erofs-20261125.txt) · [Kernel runner](../../artifacts/scripts/r0012f/kernel-matrix.py.txt)

## Tomorrow · image and AVControl commands

Define this downloader once in the native Bash session. Each invocation checks the launcher, manifest and downloaded scripts before use. The two code pins in this reply are independent.

```bash
pm12t() (
  set -eu
  cd /home1/chengkai/vd-tree
  p=cdb571361ae2e3e8ae2b8587fba3ccfdef8256a7
  d=$(mktemp -d "$PWD/workspace/temp/pm0012t-launch.XXXXXX")
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0012t/next.sh.txt" -o "$d/run"
  printf '%s  %s\n' 9556607c280158caf57a6a568fc8454bfc1d958ff3ba2ffc2bf2a70b04a93049 "$d/run" | sha256sum -c -
  exec bash "$d/run" "$p" 0c2f5df57805efce90d8c20bf631058e8ebf4abba4172e7112493d87784da2cf a984c67ad51ee218c32a0e138ee45d1dfc09ad31e1996a510bf89ebb16aca2a7 "$1"
)
pm12t erofs
```

1. `erofs` first reads the named Official and GCC partition superblocks and compression records. It then builds the tools under a new `workspace/temp/pm0012t-erofs-utils.*`. Expect `SOURCE_COMPRESSORS` for both captures, `METABOX_INLINE_BYTES_VERIFIED`, the tool version and an `export PM12_EROFS_RECEIPT=… PM12_EROFS_SHA=…` line. **Paste that export in the launching shell.** Allow roughly 5–30 min, two make jobs, scratch for the GCC platform and sparse expansion, and outbound read-only source downloads. The compiler build alone can overlap GBS. The combined command also reads/unpacks the GCC PERF and can expand a sparse disk, so schedule it after K0–K5 if free space cannot cover both workloads and their reserves.
2. `pm12t image` starts the detached image scan. Retain its **exact** printed directory. Wait for `DONE image rc=0`. Allow hours, substantial sequential I/O and space for the cached extracted image trees; this job takes the shared heavy lock. To return compact progress and the partition checks, use the following in the same shell.

```bash
read -r -p 'Paste the PM12_BATCH_DIR printed by pm12t image: ' PM12_IMAGE_RUN
export PM12_IMAGE_RUN
tail -n 18 "$PM12_IMAGE_RUN/status.txt"
grep -E '^(EROFS_PARTITION|EROFS_CHECK_EXTRACT|PLATFORM_ROSTER|PRD_ROSTER)' "$PM12_IMAGE_RUN/jobs/platform/job.log" | head -n 35
```

3. `pm12t pilot` runs **baseline, scoped default and package-fix AVControl together**, in the foreground after that exact image passes. Allow ~30–90 min depending on dependency availability, one GBS job at a time, with the package disk/RAM gates. It prints the eight gates per treatment and reasons for open results. A failed build produces the available failure log. `pm12t retained` separately reads the two old lanes without compiling (minutes; mainly local reads). [Launcher](../../artifacts/scripts/r0012t/next.sh.txt)

### EROFS reproducibility

| Check | Result |
|---|---|
| Source | Upstream v1.9.4 tag archive SHA-256 `7d135aa2550326a5acf20f53c518aea5a8900015ce50700044e40f818c31dd80`. The committed configure-ready source distribution is `b461c83774c4dde715b3bdacaabe132b6a28dd5fa0b114cf9c3b6db0b0635bd1`. All 133 upstream regular files, including all 102 C/header files, matched byte for byte. A clean build from the committed distribution passed the staged patch and extraction tests. |
| Local tool build | Private prefix. Local missing LZ4 and Zstd development inputs were built from pinned sources. LZMA and zlib were available. The native builder checks its own header/library pairs, builds missing dependencies under the same prefix, and verifies all four decoders. |
| Additional defect reproduced | Stock 1.9.4 exited successfully and extracted the expected entry counts, but returned zero bytes **in place of the contents** of both nonempty metabox-inline fixture files. Its fsck uncompressed-data path read an inline offset from the block device. The local patch routes this specific case through the inode reader. |
| Local byte test | Real GPT, reversed partition order, 48-bit + metabox. LZ4 platform had 4 entries and Zstd product had 2, including roots. Both exact file contents matched. Corrupting the product superblock failed extraction. |
| Production evidence | Await the native run for GCC/Official × `pltf_t`/`prd_t`. Each partition requires decoder verification and extraction, with an independent `dump.erofs -S` count. Each receipt records version, path, superblock, compression records, counts and tool-manifest digest. Both absolute tool paths and their SHA-256s are checked before opening the cache. |

[Upstream erofs-utils v1.9.4](https://github.com/erofs/erofs-utils/tree/v1.9.4) · [Inline extraction correction](https://github.com/lhmax2010/analysis/blob/cdb571361ae2e3e8ae2b8587fba3ccfdef8256a7/artifacts/scripts/r0012t/metabox-inline.patch) · [Native builder](../../artifacts/scripts/r0012t/erofs-build.sh.txt) · [Two-partition regression test](../../artifacts/tests/r0012r/dual.py)

## 0012s · kernel columns and debug payloads

| Metric (bytes) | GCC 37564293 | Official 37736448 | Custom 37736427 |
|---|---:|---:|---:|
| Text · board kernel-code extents | G1 required | 8,564,632 | 8,315,864 |
| Data · boot rwdata | G1 required | 681,984 | 680,960 |
| BSS · boot bss | G1 required | 4,120,576 | 4,121,600 |
| Total · uImage file minus 64 | Await GCC capture read | 11,348,904 | 11,085,176 |
| U-Boot declared payload | Await GCC capture read | 11,348,644 | 11,084,916 |
| uImage file | Await GCC capture read | 11,348,968 | 11,085,240 |
| zImage file | Await GCC capture read | 5,326,504 | 5,222,032 |
| PERF kernel RPM | 20,018,029 | 19,345,448 | 19,160,700 |

GCC’s retained RPM SHA-256 is `e78789c2d95eb9a0e629646fad73e01d02a088ae470cce9e297ee8642b7399e5`. Its VCS label ends in 14293732. The GCC Base is `tizen-10.1-base-standard_20260919.1`; equality of source CL does not establish config equality. The two LLVM images each carry 260 bytes after the declared payload. [GCC capture](../../artifacts/evidence/native-run-r0011c-chain-AFkXQV-20261124.txt) · [Board Table A](0012r_reply.md) · [Native size readback](../../artifacts/evidence/native-run-r0012r-size-retained-20261125.txt)

- **Debuginfo command:** `pm12t debug`. Both perf downloads previously returned rc=0. The historical lookup filtered filenames before reading ELF headers. The empty dictionaries and subsequent missing `elf` key cannot distinguish a different filename, a different ID or modules only. The replacement inventories the four RPMs, reuses retained RPMs of the expected identity, and streams their regular members exactly once. The compressed terminal packets include the entire RPM path lists and every detected ELF path, byte size, type and GNU build ID, including hardlink aliases. A matched linked kernel is saved by ID for section measurement. The actual (a)/(b)/(c) verdicts and section totals require the native result. Expected IDs: Official `419813f26f2d03bee00bde1d7173b0c2fd887530`; Custom `4d95bb9eb9dc71983a87f90352fc8c2b7bd8a006`. Allow minutes to tens of minutes, one CPU plus read I/O, up to 1 GiB/download if the files need fetching. No GBS.
- **GCC config + verified USB command:** `pm12t gcc`. It compares both retained devel RPMs’ `/usr/include/kernel_header/perf/.config`, pins Official to `2a31652557d89d100d3c1bc6b0116556e32a56f03b0145eba12af425c75379f3` and returns all changed symbols (Official → GCC) as a packet. It stages the verified GCC PERF in `workspace/usb/37564293/updateSU2E`, checks the manifest there, cross-checks the uImage/zImage hashes against the captured kernel RPM and checks the declared U-Boot payload CRC. The terminal result includes its sizes and build ID. Shared disk lock; schedule after heavy jobs. Allow 5–20 min, sequential PERF reads and expanded bundle space above the staging reserve. G1 remains a separate operator flash/board visit. [Kernel inventory](../../artifacts/scripts/r0012t/kernel-inventory.py.txt)

## 0012s · AVControl acceptance

| Gate | Retained observation and next evidence |
|---|---|
| T1 · link and function ISA | The old message combined zero links, several links, and a link without effective LTO into one result. Both returned packets contained exactly the same single gap. The revised join reports actual link counts, effective LTO, retained wrapper receipt count, CMake plans and response filenames. It reads saved wrapper invocations and verbose compiler runs, expands target-local response files, and joins target objects to actual compile receipts, bitcode function modes and linker plans. An unexecuted CMake plan alone cannot qualify the link. The cause on this pair awaits `retained`. |
| Driver config | Each Clang C/C++ driver was invoked with `-x c` or `-x c++` on inline conditional assembly, and separately with `-x assembler-with-cpp` on unified assembly containing `moveq` without an IT block. The old summary says the pair of expected results was incomplete for all four drivers. It gives neither individual mode nor assembler error. `ISA_PROBE` now prints the observed `BUILT c/S` mappings and `FAILED` tags per driver, with the retained probe diagnostics when available. An absent tag is missing evidence. |
| T2 · delivered ISA | The original metric measured the ELF in the delivered RPM using the image scanner. Baseline 740,645 / 740,764 executable bytes classified A32 (99.984%). Default 4,245 / 445,170 (0.954%). The retained receipt now prints the classification basis and SHA per ELF. The separate exact-symbol analysis left 441,362 default **.text** bytes unknown. These measurements cover different sections and methods. The revised audit also tries retained link output when its build ID and .text bytes match the delivered file. |
| T3 · scope | Retained default passed. Its .text was 441,362 B versus 736,944 B baseline (−295,582 B). |
| T4 · ABI | Same dynamic surface; zero changes to exports, versions, SONAME and NEEDED. `ABIDIFF_UNAVAILABLE` specifically means the analyzer could not find the abidiff executable. Dynamic identity is insufficient for the existing type-ABI acceptance rule when the executable changes. |
| T5/T6 · tests and load | No retained check, interworking or executable-smoke marker. The captured AVControl spec builds and installs the app, then enters %clean. The new AVControl instrumentation runs at the end of %install, enumerates registered CTest tests if available, exercises the ARM/Thumb DSO callback and runs the executable interpreter’s dependency listing. The loader receipt is separate from functional launch; the latter still needs a qualified app invocation. |
| T7 · real source inputs | 28 reported gaps include CMakeCXXCompilerABI.cpp and CMakeCXXCompilerId.cpp. Exclude confirmed configure paths. Compare the 26 other names with sources joined to actual final objects. Assembly sites, missing DWARF and unmatched inputs remain visible. No count of successfully joined real sources was present in the native readback. |
| T8 · explicit ARM control | N/A for AVControl. |

[Retained gap packet](../../artifacts/evidence/native-run-r0012r-size-retained-20261125.txt) · [Original ISA totals](../../artifacts/evidence/native-run-r0012m-pilot-and-r0012p-size-20261125.txt) · [Delivery join](../../artifacts/scripts/r0012r/lto-delivery.py.txt)

## Archive and validation

| Byte-exact input | Verified SHA-256 |
|---|---|
| native-run-r0012r-size-retained-20261125.txt | `104969dcf70d3a3ba5a1e08864420030567e7094412652099d22288e5dabf66b` |
| native-run-r0012r-image-mKv04z-erofs-20261125.txt | `b913ac17c29a627de4aa0c04c2bbba2275df9f27b2903176ce603b757249c002` |

Python 3.10.12 verified 52 manifest entries. Local fixtures passed the raw-receipt/response-file ARM link join, GNU build-ID extraction and RPM hardlink aliases, Bash 3.2.57 injected-script checks, and actual two-partition EROFS content checks. Native execution, board G1 and Claude review are pending.
