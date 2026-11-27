```bash
(
set -eu -o pipefail
pin=dad2b85ee6868e7fcc7cdc8af648b06f57cf36f4
d=$(mktemp -d /home1/chengkai/vd-tree/workspace/temp/pm0013s-launch.XXXXXX)
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 \
  "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013jk/run.sh.txt" -o "$d/run"
printf '%s  %s\n' 880111930007bbbf19c957c46a8c74c5650c407ed5438d990523412f6da3ce2a "$d/run" | sha256sum -c -
bash "$d/run" "$pin" verify
)
```

Run on the native host after PM review. Use this line at the first receipt prompt in both commands.

```text
PM_OVERRIDE HOLD RECEIPT /home1/chengkai/vd-tree/workspace/temp/pm0013jk-static.mo1VRK/effects.json ef577b30f542286ccfe09a4297f186bc3e1c76262a03bd23ecad5e96a919563b
```

**Verify.** Reads the completed Official build in `pm0013jk-build.jEMVH7` (source commit `8b0eec57`, spec `0994c745…`). One process, predominantly local file reads, estimated several minutes depending on cache. Only the pinned scripts are downloaded. Full argument evidence and receipts go in a fresh `workspace/temp/pm0013jk-build.*`. No GBS invocation, build lock or sudo. Copy the complete `BUILD_RECEIPT <absolute path>/build.json <sha256>` line for the next step.

**Shelve** after a passing build receipt, on the same native host in an attended terminal.
```bash
(
set -eu -o pipefail
pin=dad2b85ee6868e7fcc7cdc8af648b06f57cf36f4
d=$(mktemp -d /home1/chengkai/vd-tree/workspace/temp/pm0013s-launch.XXXXXX)
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 \
  "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013jk/run.sh.txt" -o "$d/run"
printf '%s  %s\n' 880111930007bbbf19c957c46a8c74c5650c407ed5438d990523412f6da3ce2a "$d/run" | sha256sum -c -
bash "$d/run" "$pin" shelve
)
```

Paste the same override at the first prompt, then paste the verbatim `BUILD_RECEIPT` line printed by verify at the second. The native paths and hash are generated at verification time. The existing P4 procedure checks the ticket, shows the diff, requires the review hash, creates the TEST-ONLY pending CL, verifies the shelf and restores the working file. Its function body is byte-identical to d428782. Estimated under two minutes plus operator review, one process, small local diff files and P4 server traffic.

**Board decision.** The verifier independently hash-checks the 00KP3P static receipt and its TSV archive. It prints `S11_REMAINING K1` and `S11_REMAINING K3` with PC, helper, mnemonic, operands, direct callers and disposition. It emits `BOARD_FLASH PM_PASS RECEIPT … S12_REQUIRED_BEFORE_FLASH` only when both residuals are identified reads and the pinned S1/S2/S4/S9 evidence meets the PM conditions. Unknown instructions, writes or missing evidence retain HOLD. S1 has zero observed direct critical calls. S2 has an 8-byte lower bound on an 8,192-byte stack, including five K1 and eight K3 sites reviewed by PM. S4 and S9 passed both lanes. STATIC_GATE remains HOLD. Before flashing either TEST-ONLY QB, compare its shipped module set, sizes and relocation types with its own reference, 37777148 for Official or 37777264 for Custom, and review differences. The archived S12 covered 0 of 115 modules per lane.

**S11 evidence.** The returned text identifies 118/119 K1 and 164/165 K3 as unconditional TPIDRURO reads. Its mnemonic filter omits the two residual rows. Their names require the retained TSVs. The previous classifier accepted decimal 3 and 4, but failed to normalize hex immediates such as `#0x0` and `#0x3`. The correction recognizes both decimal and hex encodings of TPIDRURO and TPIDRPRW, including conditional forms.

**Build checks.** The verifier checks each boot member against its RPM digest. It validates the uImage header CRC and computes the data CRC over exactly `u[64:64+ih_size]`. It compares the remaining length with the hash-pinned Official 37777148 USB uImage and prints both lengths. One retained perf tree must match all three of zImage SHA-256, kernel config and the GNU build ID in the verified payload. Against K1, each metric must be within 0.10%: .text 8,214,312 bytes, 20,324 helper addresses, Image 10,996,388 bytes, zImage 5,449,312 bytes. The argument checks cover SERET-UL GCC, perf Clang and module compilation. The real jEMVH7 verdict awaits native execution.

**Local validation.** Python 3.10.12 passed ten tests across the 0013p, 0013q and 0013s fixtures, including corrupt/truncated uImages, trailer mismatch, loss of the matching zImage tree, erroneous GCC `-moutline`, a conditional read and a state write. Earlier retained Official and GCC uImages passed both CRCs and each had a 260-byte trailer. The local receipt test used fixture artifacts. Both Bash launchers passed syntax checks. The manifest digests match the script commit.

**Archived terminal originals.** [00KP3P static](../../artifacts/evidence/native-run-r0013q-static-00KP3P-20261127.txt) `0deec1bd0f73a84e5f0da0ff2279768ec3ab6faad4212f79aab0d55c4e197455`. [jEMVH7 and S11](../../artifacts/evidence/native-run-r0013p-build-jEMVH7-and-s11-20261127.txt) `8f367caec3068d89340e2b661a199b0382d8aacb0a98d45045345aace77b4720`. PM approved the 0013r reader at ee9983f.
