# 0013y — `-moutline` TEST-ONLY CL 14507546 recorded; PM acceptance of the 0013v verify; S12 for the QBs

**Evidence (archive under `artifacts/evidence/`):**
- `native-run-r0013v-verify-dMztOS-20261127.txt`, sha256 `119eb87081386bc6a03114bb3d9c6f9b624fe29787656545e264922863418273`
- `native-run-r0013w3-shelve-CL14507546-20261127.txt`, sha256 `c56ca9d6c1afea9c87c43657a295322d95159997e29b6248714c711249e0f70a`
- `native-run-r0013w5-merge-CL14507546-20261127.txt`, sha256 `1c8812e8df5b1019d0e6fe039a23efa5aa0b999af524bdec236da2cabbee2e10`

## 1. PM decision on the 0013v verify (dMztOS)

PERF measured exactly the same as K1, with config proof `SPEC_PREFLIGHT_IDENTICAL_DEFCONFIG`:

| | Value |
|---|---|
| `text` | 8214312 |
| `helpers` | 20324 |
| `Image` | 10996388 (equal to the uImage payload) |
| `zImage` | 5449312 |

The run then failed on `PERF_ARGV_COUNTS 0`. **PM accepts the build anyway (PM_OVERRIDE, recorded):**
- 20,324 outlined helpers exist only if Clang received `-moutline`;
- the SERET-UL GCC step succeeded, and before the conditional it failed with `unrecognized option '-moutline'`, so GCC did not receive it.

Record this as `VERIFY PM_ACCEPT argv-proof-by-effect`.

Do not use `PERF_ARGV_COUNTS` as a hard gate on spec builds that discard their compile command lines. In future, either capture argv through a `KCFLAGS`/`V=1` side channel or downgrade it to INFO.

## 2. TEST-ONLY CL

The user created it manually in `DEV-IPTV-VC_TOOLCHAIN`, because the spec was already open in that client's default change. The local open file was restored afterwards and is byte-identical.

| | |
|---|---|
| CL | **14507546** (pending, never submit) |
| Shelved files | 24: the spec (`…/packaging/tztv-kernel.spec#61`) plus the other 23 files of 14427407 |
| Spec sha256 | `0994c745b120f29218f96e6262b7af84f50d073a94716c4212263285a0448b23` (equal to the GBS-built spec) |
| Diff vs `@=14427407` | exactly one line (301), the clang-only `KCFLAGS` conditional |
| QB shelf | **14507546 only**. QB allows one shelve CL per path, so r0013w5 added 14427407's other 23 files unchanged: `SHELF_CHECK match=24 mismatch=0 of 24`. |

The spec in 14507546 is a superset of the spec in 14427407: it is that file plus one line. Every other file in 14507546 is byte-identical to 14427407 (checked by sha256 in r0013w5).

Two QBs are being submitted:

| | Official | Custom |
|---|---|---|
| Clone of | 37777148 (Base 20261113.1) | 37777264 (Base 20261118.1) |
| Shelve | 14507546 only | 14507546 only |

The user will report the QB numbers.


## 2b. Question for you: which source did the dMztOS build use?

When r0013w5 ran, 7 of the 24 files in 14427407 were **not open** in the user's `DEV-IPTV-VC_TOOLCHAIN` workspace. The local copies were the synced revisions, not the 14427407 versions:

| File | Synced (have) | 14427407 sha256 (prefix) |
|---|---|---|
| `linux-6.12/Makefile` | #10 | `b9da89aa1a9d` |
| `arch/arm/configs/KANTSU2E_debug_defconfig` | #23 | `6bf8e5380ca2` |
| `arch/arm/configs/KANTSU2E_perf_defconfig` | #22 | `11c224a1247e` |
| `arch/arm/configs/KANTSU2E_release_defconfig` | #22 | `2053dab86bdb` |
| `fs/minimal_core.c` | #4 | `8500db4e7a10` |
| `init/Kconfig` | #8 | `325ccaa4df64` |
| `ipc/kdbus/connection.c` | #8 | `f1d2a1bf16e6` |

**Answer from your records. No new build.**

Did the source trees for the K1 lane and the r0013p/dMztOS `-moutline` build contain the **14427407** versions of these 7 files? Prove it with the file hashes recorded at build time. If you have none, give a read-only command that hashes them inside the retained build workdirs.

- **If yes:** the QB (14507546) and the measured build are the same source. Report `SOURCE_EQUIV PASS`.
- **If no:** state exactly which K-lane numbers are affected. The QB is then the authoritative measurement.

## 3. Request: S12 module check, ready for when the QBs finish

S12 must pass before BOARD_FLASH (`060446c6…`, `S12_REQUIRED_BEFORE_FLASH`). Give one hash-pinned, read-only native command. It takes a QB number or an artifact URL plus the matching baseline (37777148 or 37777264) and does the following:

1. Download only the kernel and kernel-module RPMs, plus their checksums, into `workspace/temp`.
2. Compare the module sets:
   - names;
   - `vermagic`;
   - kernel release string;
   - module signature presence;
   - `Module.symvers` CRC set, if shipped;
   - size per module (`.text` delta).
3. Confirm the `-moutline` effect in the QB kernel: the outlined-helper count, in the same `OUTLINED_FUNCTION_` metric as the 20,324 above. For Official vs Custom MLGO, report both.
4. Output a compact `S12 PASS|FAIL` line with the reasons.

Same rules as before: workspace only, no sudo unless justified, no GitHub submission from the Native Server, and the PM reviews the command before it runs.

## 4. Still open (unchanged)

- 0013x: fix the Thumb-2 enumeration repo provenance (sent together with this prompt).
- 0013o: pkg worker fix review.
