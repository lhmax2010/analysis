```bash
(
set -eu -o pipefail
pin=271efa19ae17a0d28dc9abe6abad5f0b1f32df76
d=$(mktemp -d /home1/chengkai/vd-tree/workspace/temp/pm0013u-launch.XXXXXX)
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 \
  "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013jk/run.sh.txt" -o "$d/run"
printf '%s  %s\n' 6899fec380bfc8c6db50595650fd1027ff1550a06cad838bfc8951682c1e184e "$d/run" | sha256sum -c -
bash "$d/run" "$pin" verify
)
```

Run on the native host after PM review. Use this line at the first receipt prompt in both commands.

```text
PM_OVERRIDE HOLD RECEIPT /home1/chengkai/vd-tree/workspace/temp/pm0013jk-static.mo1VRK/effects.json ef577b30f542286ccfe09a4297f186bc3e1c76262a03bd23ecad5e96a919563b
```

**Native verification.** This reuses the completed Official build in `pm0013jk-build.jEMVH7`. Estimated several minutes, one process with local reads and pinned script downloads. Runtime and scratch usage depend on the size of any debug RPMs. New receipts, selected debug members and diagnostics stay in a fresh `workspace/temp/pm0013jk-build.*`. The command requires neither a GBS rebuild nor sudo or a build lock.

| Check | Required result |
| --- | --- |
| Candidate tree | The same tree contains a zImage matching the perf RPM SHA-256 and a byte-identical copy of K0’s effective config. Each candidate reports its path, both hash pairs and the presence of `.config`, `vmlinux` and `System.map`. Config mismatches include symbol differences. The full inventory is in `tree-candidates.json`. |
| Kernel identity | Read the GNU build ID from the CRC-verified uImage payload. Search retained copies and kernel debuginfo/devel RPM members for an ARM kernel ELF with that ID. Raw BTF does not provide ELF section or symbol measurements. |
| Matching ELF | Measure .text and unique outlined helper addresses and check both against K1, along with Image and zImage sizes, each within 0.10%. A matched ELF with missing evidence or out-of-range measurements fails verification. |
| No matching ELF | Require Image **exactly 10,996,388 B** and zImage within **0.10% of 5,449,312 B**. The receipt records `NOT_MEASURED_NO_ELF` separately for .text and helpers, the payload build ID, and a null ELF build ID. Size equality establishes length only. |
| Compiler arguments | Require SERET-UL GCC without `-moutline`, and built-in kernel and module Clang compilations with it in the selected perf tree. The verifier retains `argv.json` and its SHA-256. |
| Receipt | A successful run ends with `BUILD_RECEIPT <absolute path>/build.json <sha256>`. Return that whole line. |

**Shelve after the native receipt.** Use this pin for both steps because shelve checks the verifier script digest. At the prompts paste the override above and the new native `BUILD_RECEIPT` line. The attended P4 ticket, diff review and TEST-ONLY shelf procedure is unchanged.

```bash
(
set -eu -o pipefail
pin=271efa19ae17a0d28dc9abe6abad5f0b1f32df76
d=$(mktemp -d /home1/chengkai/vd-tree/workspace/temp/pm0013u-launch.XXXXXX)
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 \
  "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013jk/run.sh.txt" -o "$d/run"
printf '%s  %s\n' 6899fec380bfc8c6db50595650fd1027ff1550a06cad838bfc8951682c1e184e "$d/run" | sha256sum -c -
bash "$d/run" "$pin" shelve
)
```

**BbbAhy evidence.** The archived run verified header CRC `980d92a8`, payload CRC `9742a207`, Image length 10,996,388 B and a 260 B trailer matching the Official trailer length. It issued `BOARD_FLASH PM_PASS` receipt `060446c6ce292bac41198c1bf6cfe62da096d939c5c918822a3df369dfeaf5cf`. S12 module review is required before each QB flash. BbbAhy stopped at the old combined tree check. The spec cleanup explains why an otherwise matching tree can lack its ELF. The new inventory identifies which files actually survived in jEMVH7. [Original terminal evidence](../../artifacts/evidence/native-run-r0013s-verify-BbbAhy-20261127.txt)

**Validation.** The terminal evidence matched the requested SHA-256, `ba02d39579a4e3244d109c789ebdfaa32d9c815a9341c45ac2e09c4f3b4ac916`. Python 3.10.12 passed all ten 0013p/q/s tests. The receipt fixture exercised the no-ELF path and refused a one-byte Image discrepancy, an out-of-range zImage, a mismatched config, missing Clang flags and GCC receiving the flag. An additional real armv7hl debug RPM, with its separate-debug ELF data stored under a hardlink alias, yielded the matching build ID, 8 B of .text and one helper. The payload-note reader also reproduced the retained Official image ID `419813f26f2d03bee00bde1d7173b0c2fd887530`. The build and shelve function bodies match dad2b85 byte for byte. Native jEMVH7 verification and Claude review of this pin are outstanding.
