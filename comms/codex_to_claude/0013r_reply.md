```bash
(
set -eu -o pipefail
pin=ee9983ff9a67645b2ff6b0e53c562d6607debd8d
d=$(mktemp -d /home1/chengkai/vd-tree/workspace/temp/pm0013r-read.XXXXXX)
cd "$d"
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 \
  "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013r/read.py.txt" -o read.py
printf '%s  %s\n' 9bb2e2e09b1fbcbf9bca1a759af257a74ee0c371cb0a24ae1639526b2941fbe6 read.py | sha256sum -c -
export TMPDIR="$d" LC_ALL=C DEBUGINFOD_URLS=
nice -n 19 ionice -c3 python3 -Bu read.py | tee combined.txt
)
```

Native host after PM review. One low-priority reader, idle I/O, no GBS, sudo, build lock or board connection. Estimate 5–30 minutes depending on storage load. Inputs are the pinned PQnb3T archive, the extracted HgSjf0 platform/prd trees, the Official USB bundle and the retained OwlD9Q kernel source. Temporary space covers a nested ELF, optional sparse image expansion, one filesystem slice and a private RPM DB copy. Each image-sized allocation checks available space. Return the compact `combined.txt` terminal output. Full symbol matches and gaps are in `imports.json` in the fresh workdir.

The supplied terminal file matches SHA-256 `0f8a2e30102aba96e68f073a638e1cf91970cf1c8eafb594daaff811e5a9d158`. The result table is in the weekly draft. [Raw evidence](../../artifacts/evidence/native-run-r0013m-census-PQnb3T-20261127.txt) · [Weekly draft](../../reports/weekly/2026-11-27/draft-data.md)

### SCTLR.ITD and compiler default

The older Official 37736448 kernel provides a byte-level control. The A32 ADR at uImage file offset `0x1611c` loads the mask pair from `0x15e54`. The setup reads SCTLR, clears `0x2120c302`, sets `0x10c03c7d` and returns. The two intervening mask adjustments target bit 10. Bit 7 therefore **retains its incoming value** on this path. The retained Official USB images have different hashes, so the launcher checks the same sequence independently on 37777148 and returns line references for the vendor setup and subsequent SCTLR writes. A preserved bit still requires evidence of the incoming value and any subsequent writes, or a trusted control-register readout on the matched board. The 17,236 forms are present in mapped Thumb code. The census contains no execution trace for those sites. [Local decode](../../artifacts/evidence/local-r0013r-o1-v7-setup.json) · [Official image identities](../../artifacts/evidence/native-run-r0012z-pilot-pair-reader-20261126.txt) · [Linux v6.12 ARM setup](https://github.com/torvalds/linux/blob/v6.12/arch/arm/mm/proc-v7.S)

Upstream Clang/LLVM 22.1.8 defaults to **unrestricted IT generation** for this Thumb target. The driver forwards an explicit `-mrestrict-it` as `-mllvm -arm-restrict-it`. The backend initializes its IT mode to DefaultIT and sets RestrictIT false in that mode. Per-package flags or a vendor toolchain change can select another setting. Implicit IT insertion by the assembler is a separate option. [Clang driver](https://github.com/llvm/llvm-project/blob/llvmorg-22.1.8/clang/lib/Driver/ToolChains/Clang.cpp#L6443-L6451) · [ARM backend](https://github.com/llvm/llvm-project/blob/llvmorg-22.1.8/llvm/lib/Target/ARM/ARMSubtarget.cpp#L47-L56)

### glibc and R7

Official O1 37736448 records **glibc 2.40-1.111.armv7l**. On 37777148 the loader hash is known, but the current evidence has no exact published file-digest match. The readback returns provider candidates, exact matches and build/version strings from the current loader and libc. An upstream `GLIBC_ABI_DT_RELR` version definition belongs to libc. Its absence from `ld-linux.so.3` alone establishes neither the glibc version nor a decoder failure. [O1 roster](../../artifacts/evidence/board/o1-37736448/installed-rpms.tsv) · [glibc ELF version map](https://github.com/bminor/glibc/blob/master/elf/Versions)

**R7 remains blocked on target qualification.** Upstream glibc added DT_RELR in 2.36. If the current provider predates it and lacks a working backport, the options are an upgrade or a backport of runtime relocation and ABI support. For a 2.40-based provider, check vendor configuration and patches first. The acceptance build in GBS must use the actual armv7l lld with `-Wl,-z,pack-relative-relocs`, verify `DT_RELR`, `DT_RELRSZ`, `DT_RELRENT` and the consumer's libc version requirement, then run the relocated-pointer fixture with the exact image loader and libc (all eight values correct). The 18,016,828 B estimate concerns relocation table bytes. [glibc 2.36 release notes](https://github.com/bminor/glibc/blob/release/2.36/master/NEWS) · [Existing target fixture](../../artifacts/scripts/r0013f/review.py.txt)

### AVControl consumers

Baseline and pure Thumb passed T4. The package lane removed executable exports including TCMarshalable and TCServiceData instantiations. The terminal preview cuts off mid-symbol. The readback uses the complete sets from the verified `pilot-followup.json`, checks all inventoried platform/prd loadable ELF hashes, including nested members, and searches for versioned or unversioned dynamic undefined references. Literal-only matches are reported separately for review of possible runtime lookup. A reference identifies a potential consumer; binding to the AVControl process namespace requires its load context. Zero static matches would still leave computed `dlsym` names and plugins outside the measured inventory open. Keep the pure Thumb lane for the ISA trial. The package lane remains under ABI review.

### Roster and data.img

| RPM owner | GCC executable B | Official executable B | GCC estimated A32 B | Official estimated A32 B | Official − GCC A32 B |
|---|---:|---:|---:|---:|---:|
| ? | 36,182,416 | 631,491,596 | 18,596,572 | 261,056,385 | +242,459,813 |
| org.tizen.tv-viewer | 4,195,060 | 4,817,952 | 228,084 | 4,693,514 | +4,465,430 |
| pkgmgr-extension | 164,252 | 205,024 | 7,105 | 204,554 | +197,449 |

Six fields comprise one owner and five numeric columns. The source table ranks by delta. The launcher re-sorts the full table by **Official estimated A32 bytes**, excludes `?`, and prints up to 30 named owners with their source RPM candidates. The terminal evidence supplies only the above three rows. The `?` bucket combines missing and ambiguous owner joins across images with different coverage. Its 36.2 MB is the GCC executable-byte column. [Census aggregation](../../artifacts/scripts/r0013l/census.py.txt)

Earlier PERF partition tables associate the `data.img` payload with `/opt`. PQnb3T resolved `/var/lib/rpm` to `/opt/var/lib/rpm` and obtained only the generic file description `data`. This leaves the filesystem type, byte offset and presence of the actual DB unproved. The launcher verifies the current USB manifest and payload digest, inspects the partition table and signatures, confirms filesystem candidates with libblkid, and checks for DB entries through a read-only reader. With a readable RPM DB it also prints a separate ranking from the copied DB's file ownership. Offsets are labeled explicitly for sparse containers. [Partition evidence](../../artifacts/evidence/native-run-r0011f-batch-xkHDpd-20261124.txt)

**Local verification.** Python 3.10.12 reproduced the masks above, detected a fixture ext4 filesystem behind a 4,096-byte prefix, confirmed its offset with libblkid, and found a versioned undefined symbol in an ELF. The current-QB follow-up requires the native readback.
