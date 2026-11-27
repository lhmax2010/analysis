```bash
(
set -eu -o pipefail
pin=f8b5afdb480f7913823f3c25a58e4f13b1b3f2f0
d=$(mktemp -d /home1/chengkai/vd-tree/workspace/temp/pm0013v-launch.XXXXXX)
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 \
  "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013jk/run.sh.txt" -o "$d/run"
printf '%s  %s\n' 60a7044d5c5d82f2cce841fffe605abba61d58afdc54c2cf60b82461a55898b9 "$d/run" | sha256sum -c -
bash "$d/run" "$pin" verify
)
```

Run on the native host after PM review. Use this line at the first receipt prompt in both commands.

```text
PM_OVERRIDE HOLD RECEIPT /home1/chengkai/vd-tree/workspace/temp/pm0013jk-static.mo1VRK/effects.json ef577b30f542286ccfe09a4297f186bc3e1c76262a03bd23ecad5e96a919563b
```

**Native verification for jEMVH7.** Run from the operator’s native account. The script reads the finished Official build and downloads its pinned readers. Allow several minutes for local ELF, RPM and log reads. It runs serially, creates scratch files under a new `workspace/temp/pm0013jk-build.*`, and requires no GBS, build lock or sudo.

**What Y8W62v established.** Of five zImage candidates, only `tztv-kernel-1/KANTSU2E/image/perf/zImage` matched the RPM digest `45af86f8fd2bc06dab9c1a4b1613eb8cacfe6b337b1a13b409d61abe23bf5dad`. Its sibling `vmlinux` exists. The output directory has no `.config`. The payload length was 10,996,388 B and the trailer was 260 B. Y8W62v issued the conditional board receipt and stopped before measuring the ELF. Its terminal capture is archived byte-for-byte at SHA-256 `df254c84af9ccc94435667103851353f71f2acca5d270d2d00784a915928be7b`. [Y8W62v evidence](../../artifacts/evidence/native-run-r0013u-verify-Y8W62v-20261127.txt)

| Terminal output | Evidence required for this layout |
| --- | --- |
| `PERF_ELF_BUILD_ID` | The adjacent ARM kernel ELF has the same GNU build ID as the CRC-verified uImage payload. |
| `ELF_IMAGE_BYTE_MATCH` | Image reconstructed from the ELF matches every payload byte. The verifier measures .text and unique outlined helper addresses from this ELF. K1 reference values are 8,214,312 B of .text, 20,324 helpers, 10,996,388 B of Image and 5,449,312 B of zImage. All four use the existing 0.10% tolerance. |
| `PERF_CONFIG_PROOF` | Searches the build for an effective-config digest equal to K0, checking adjacent ELF/Image identities where available. Next it checks a config shipped in the perf RPM, then IKCONFIG. The last permitted method verifies the retained spec hash and the SHA-256 of the same `linux-6.12/arch/arm/configs/KANTSU2E_perf_defconfig` input. This method reports `SPEC_PREFLIGHT_IDENTICAL_DEFCONFIG` and leaves the measured effective-config digest null. |
| `ARGV_PASS` | The retained commands show SERET-UL GCC without the option and perf Clang built-in and module compilations with effective `-moutline`. Where packaging removed the kbuild command files, the reader tracks perf flavour in the GBS log. It checks observed GCC invocations for option leakage. |
| `BUILD_RECEIPT` | Paste the whole native line, including the generated path and digest, at the shelf prompt. The board receipt still requires S12 per QB before flashing. |

**Shelve.** Run in an attended terminal after verify succeeds. Enter the same override and the new native `BUILD_RECEIPT`. Shelve checks the script digest, so use the same pin for both commands.

```bash
(
set -eu -o pipefail
pin=f8b5afdb480f7913823f3c25a58e4f13b1b3f2f0
d=$(mktemp -d /home1/chengkai/vd-tree/workspace/temp/pm0013v-launch.XXXXXX)
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 \
  "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013jk/run.sh.txt" -o "$d/run"
printf '%s  %s\n' 60a7044d5c5d82f2cce841fffe605abba61d58afdc54c2cf60b82461a55898b9 "$d/run" | sha256sum -c -
bash "$d/run" "$pin" shelve
)
```

**Validation.** Python 3.10.12 passed 11 tests. The new integration test built a real ARM ELF and a perf RPM, placed the ELF and zImage together without a .config, read compiler evidence from the log, matched every payload byte and issued a fixture receipt. It exercised all four config methods and both Image reconstruction paths. A changed payload byte and module evidence belonging only to SERET-UL were each rejected. The build and shelve routines are byte-identical to the previous pin. Claude review and the jEMVH7 native receipt are outstanding. [Regression fixture](../../artifacts/scripts/r0013v/tests/perf.py)
