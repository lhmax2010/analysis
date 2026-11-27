# 0013y · S12 for the two outline QBs

```bash
(
set -eu
read -r -p "Official outline clone QB number or Product URL: " official
read -r -p "Custom outline clone QB number or Product URL: " custom
pin=3a1362f95adc86bc5d4119e97ba8181174d987e0
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013y-launcher.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013y/read.sh.txt" -o "$d/run.sh"
printf '%s  %s\n' 8ee2be9a3671e2880f0ea8eaf0cb0d9dfa231b56fd70cf8c6ca991421b2118d5 "$d/run.sh" | sha256sum -c -
bash "$d/run.sh" "$pin" s12 "$official" "$custom"
)
```

**Native server, read-only against the four publications; PM review before execution.** Enter the two **new clone** numbers or full Product artifact URLs in Official, Custom order. The baselines are fixed at 37777148 and 37777264. A numeric ID resolves through an existing capture or its operator GBS config. Use the exact Product URL if neither exists. Budget approximately 5–30 minutes and several GiB of workspace scratch, depending on published debuginfo and download speed. One low-priority process performs the reads. No build lock or sudo is required.

The check verifies the published Base and Product ID, joins filelists to primary metadata by package checksum and verifies each fetched RPM and selected member. It compares shipped perf and applicable external modules by RPM/path, module name, kernel release, vermagic, signature-marker presence, relocation types and shipped `Module.symvers` CRCs. The reference perf RPM must account for 115 modules. It records both module sizes and each `.text` delta. Signature presence is the scope of this offline check. Size deltas are measurements. A set, compatibility or CRC difference is reported for review.

Each `S12_PAIR` gives the reference and candidate outlined-helper counts, using distinct text addresses for `OUTLINED_FUNCTION_<n>`. Counts come from the corresponding perf System.map or a symbol-bearing ELF matching the Build ID in the CRC-checked uImage and decompressed zImage. A retained jEMVH7 ELF can qualify for Official by Build ID. If a clone publishes its full vmlinux separately, `S12_OFFICIAL_ELF` / `S12_CUSTOM_ELF` can point to that ELF under the native workspace. Missing candidate symbols, unresolved inputs or contradictory counts keep S12 at FAIL with a reason. The final line is `S12 PASS` only when both comparisons pass. Full rows are retained in the printed workdir. The `S12_PACKET` line gives the return command, part count and raw JSON SHA-256. Run the printed `sed` for each part in order. Both clone IDs and a passing result are still outstanding. S12 remains a prerequisite for flashing.

## Verified local build and QB inputs

| Item | Recorded result |
|---|---|
| dMztOS | **VERIFY PM_ACCEPT argv-proof-by-effect** for the retained jEMVH7 PERF build |
| PERF compared with K1 | `.text` 8,214,312 B; 20,324 helpers; Image 10,996,388 B; zImage 5,449,312 B. All four equal. |
| Identity and config | ELF Build ID `99518c24394ed1496461993969922d425986ddc5`; reconstructed Image matches every payload byte; `SPEC_PREFLIGHT_IDENTICAL_DEFCONFIG`. |
| Compiler evidence | PERF retained 0 compile lines. The measured helpers and the successful SERET-UL GCC step support the PM inference. The earlier GCC invocation with unconditional `-moutline` failed. The historical verifier stopped before emitting a receipt. |
| Pending TEST-ONLY CL | **14507546 alone** in both clones, for this vdlinux path. The w5 result supersedes the w3 instruction to stack two shelves. |
| Shelf contents | `SHELF_CHECK match=24 mismatch=0 of 24`. The other 23 files match 14427407. The spec differs from the 14427407 spec only at line 301 and matches the GBS-built spec, SHA-256 `0994c745b120f29218f96e6262b7af84f50d073a94716c4212263285a0448b23`. The operator restored the original client state. |
| Baselines | Official 37777148, Base 20261113.1; Custom 37777264, Base 20261118.1. Each new clone adds the same TEST-ONLY shelf. |

The verifier now records absent PERF argv as INFO in the retained packaged-ELF path when the pinned spec and all four measured K1 values match. GCC evidence remains required. Contradictory observed compile lines still fail. A Python 3.10.12 integration fixture exercised both cases; the historical dMztOS log is preserved as received.

## Section 2b · the seven source files

**The build records point to the 14427407 overlay for both builds. Full seven-file byte identity is still unproved.** The source receipt records 14293732 plus 24 shelf overlays. The build scripts clone the verified staged source and commit the lane spec. The clean jEMVH7 preflight records commit `8b0eec57103fee38dd9e75635b4ffe1cccda9033`. The operator's synced client was a separate checkout. Its seven unopened files explain the w5 shelf repair; they do not establish what was in either GBS checkout. [Source receipt](../../artifacts/evidence/native-run-r0012t-kernel-OwlD9Q-20261126.txt) · [Clean build preflight](../../artifacts/evidence/native-run-r0013p-build-jEMVH7-and-s11-20261127.txt)

| Under `linux-6.12/` | 14427407 SHA-256 prefix | Direct retained build evidence |
|---|---|---|
| Makefile | b9da89aa1a9d | Staging record |
| arch/arm/configs/KANTSU2E_debug_defconfig | 6bf8e5380ca2 | Staging record |
| arch/arm/configs/KANTSU2E_perf_defconfig | 11c224a1247e | Full jEMVH7 defconfig digest in dMztOS |
| arch/arm/configs/KANTSU2E_release_defconfig | 2053dab86bdb | Staging record |
| fs/minimal_core.c | 8500db4e7a10 | Staging record |
| init/Kconfig | 325ccaa4df64 | Staging record |
| ipc/kdbus/connection.c | f1d2a1bf16e6 | Staging record |

This independent readback checks the immutable Git objects of the two measured builds against `p4 print @=14427407`. K1's commit comes from its own preflight in the retained job log. Each row prints the full shelf, K1 and jEMVH7 SHA-256. A discrepancy identifies the affected build; use the QB as authoritative for that measurement. A missing object or expired P4 ticket yields UNPROVED. The reader normally takes seconds, uses one CPU and reads seven shelf files. Run it now, independently of the new QBs.

```bash
(
set -eu
pin=3a1362f95adc86bc5d4119e97ba8181174d987e0
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013y-launcher.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013y/read.sh.txt" -o "$d/run.sh"
printf '%s  %s\n' 8ee2be9a3671e2880f0ea8eaf0cb0d9dfa231b56fd70cf8c6ca991421b2118d5 "$d/run.sh" | sha256sum -c -
bash "$d/run.sh" "$pin" source
)
```

Python 3.10.12 local checks covered ARM module metadata, relocation and section sizes, a real RPM/cpio hardlink, checksum verification, signature/CRC differences and missing helper evidence. They also verified every launcher dependency digest. The proposed commands await PM review.

## Archived originals

- [native-run-r0013v-verify-dMztOS-20261127.txt](../../artifacts/evidence/native-run-r0013v-verify-dMztOS-20261127.txt) · `119eb87081386bc6a03114bb3d9c6f9b624fe29787656545e264922863418273`
- [native-run-r0013w3-shelve-CL14507546-20261127.txt](../../artifacts/evidence/native-run-r0013w3-shelve-CL14507546-20261127.txt) · `c56ca9d6c1afea9c87c43657a295322d95159997e29b6248714c711249e0f70a`
- [native-run-r0013w5-merge-CL14507546-20261127.txt](../../artifacts/evidence/native-run-r0013w5-merge-CL14507546-20261127.txt) · `1c8812e8df5b1019d0e6fe039a23efa5aa0b999af524bdec236da2cabbee2e10`
