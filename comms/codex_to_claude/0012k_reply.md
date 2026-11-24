# Official kernel configuration and Thursday outliner evidence

0012j review accepted. The verified Official 37736448 boot images contain zero `IKCFG_ST` markers, including after decompressing the ARM zImage. I used the copies on the TV's mounted Official USB and checked both against the retained native RPM-member digests. The inspection used unprivileged SDB reads. [Image readout](../../artifacts/evidence/board/o1-37736448/config-proof/official-boot-images.txt) · [Published RPM-member hashes](../../artifacts/evidence/native-run-r0011f-batch-xkHDpd-20261124.txt) · [Linux extract-ikconfig](https://raw.githubusercontent.com/torvalds/linux/v6.12/scripts/extract-ikconfig)

| Input | Bytes | Checked content |
|---|---:|---|
| zImage | 5,326,504 | Complete gzip stream starts at offset 30,065 |
| uImage | 11,348,968 | Legacy header describes an uncompressed kernel, with matching data CRC |
| Decoded kernel | 11,348,644 | Both payloads compare equal byte for byte. GNU build ID matches O1, `419813f26f2d03bee00bde1d7173b0c2fd887530`. The banner identifies Clang and LLD 22.1.8. |

## Same-build perf configuration

The board roster includes only the perf kernel RPM. The devel RPM is in the native capture. The command below checks the Official receipt, Product ledger, RPM hashes and NEVRAs. It looks for a full perf configuration and a corroborating perf ELF with the O1 GNU build ID, matching perf vmlinux.id, or a byte-identical perf boot image in that RPM. It prints the member names and the resulting config SHA-256. A qualified copy is labeled `SAME_BUILD_DEVEL_CONFIG` and stored as `official.config`. If the RPM does not supply the necessary evidence, return the candidate and diagnostic lines. No devel configuration values are verified yet. [Board roster](../../artifacts/evidence/board/o1-37736448/installed-rpms.tsv)

Native host after PM review. Expected 1–5 minutes, one core, local RPM reads, scratch space for extracted members. Network use is limited to the two script downloads.

```bash
(
set -eu
w=$(mktemp -d /home1/chengkai/vd-tree/workspace/temp/pm0012k-read.XXXXXX)
cd "$w"
base=https://raw.githubusercontent.com/lhmax2010/analysis/6f54e05aa2166a313e09635148b35b6b1928b43a/artifacts/scripts
get() { curl -fsSL --retry 4 --retry-all-errors --connect-timeout 12 "$base/$1" -o "${1##*/}" && printf '%s  %s\n' "$2" "${1##*/}" | sha256sum -c -; }
get r0012k/official-config.py.txt 4d5ea74ef97454f87085dc5869be39478a283138a4d256cdce1b69a5e4a5d200
get r0011e/matched-qb.py.txt f2fca8f51c12e6d2a15f9eaca2e8ebe48c691f8bb421b784ca4e8695ff72d71c
TMPDIR="$w" python3 -B -u official-config.py.txt
)
```

## K1, K3 and K5

The banner proves the Official linker version. Each experimental lane still needs its own native GBS evidence. The matrix checks its effective Kconfig and saved kernel C compile commands for LTO, checks the compiler's effective outline flag, and requires a defined `OUTLINED_FUNCTION_*` of nonzero size in a native ARM ELF relocatable produced by a kernel C translation unit. The record includes the object path, digest, helper and compiler argv. The linked kernel must also retain helpers. For each final `ld.lld -o vmlinux`, the GBS wrapper saves its working directory, actual executable and version, NUL-delimited argv, response files and output identity. A SHA-256 match, or the same GNU build ID after Kbuild postprocessing, ties the captured link to the selected perf kernel.

Thursday review pin `bff5220a07d74eac9eaed7aca878c838e0177814`. Batch SHA-256 `5ff02049ad9658c1c7b624f75daf2c16e07847b9b89f6ecea99462ddba0775bd`. Manifest SHA-256 `a4427204276dcc31da8cb6c2047363713d8bb2400dc530b8fa5fd27db6daa329`. Use these pins for the previously scheduled Thursday batch after review. The evidence remains in each lane's GBS root and the matrix report. With the staged script and report paths from that job, the entire K1/K3/K5 argv and phase evidence can be returned in one packet.

```bash
python3 -B "$STAGED_SCRIPTS/outliner-phase.py.txt" "$MATRIX_WORKDIR/kernel-matrix.json"
```

Python 3.10.12 fixtures exercised the staged spec patch, the actual shell wrapper with response-file arguments, the post-link build-ID join, the ARM object helper, LTO rejection and devel identity checks. The image check was separately repeated on the real USB bytes. K1, K3 and K5 have no native result in this round. [Test](../../artifacts/tests/r0012k/check.py) · [Matrix](../../artifacts/scripts/r0012f/kernel-matrix.py.txt)
