```bash
(
set -eu -o pipefail
pin=598e2e4664bd4a1fbccf828f4ac907fcc5206052
d=$(mktemp -d /home1/chengkai/vd-tree/workspace/temp/pm0013q-launch.XXXXXX)
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 \
  "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013q/static.sh.txt" -o "$d/static.sh"
printf '%s  %s\n' 7c43b68bef017924068a561ea5181e320024ee9bbd75f5574a19786ef6f78d2b "$d/static.sh" | sha256sum -c -
bash "$d/static.sh" "$pin" | tee "$d/combined.txt"
)
```

**Native host, after PM review.** One low-priority worker with idle I/O scheduling. Budget 30–150 minutes for the kernel checks, plus C7/C8 if the installed-file scan can run, and several GiB of scratch. The command reads the retained lanes and writes to fresh workspace temp directories. It downloads the analyzer and six dependencies. It takes no build lock and invokes neither GBS nor P4. Return the S1–S15, C7/C8, `BOARD_FLASH`, `STATIC_GATE` and `TABLES` lines from the combined terminal output.

| Item | Verified result |
| --- | --- |
| Input identity | Same K1/K0 and K3/K2 pairs as mo1VRK. The analyzer verifies `pm0013i-read.a0Pmc0/lanes.json` against `f7f1148e7927bc4e0b8353213932d3a5ba077cf9319a021c71a7c53588cfcf06`, then checks the dkyJ0S matrix, kernel ELFs and config identities. |
| S2 direct path | Breadth-first traversal retains the first parent of each reachable address. Each critical-stack TSV row has the root-to-caller sequence with addresses, symbols and sections. A name-only IRQ/entry match with no observed direct path has an empty sequence and still counts as a critical stack site. |
| Failure isolation | Each of the 15 checks records its own verdict. A check exception records `REVIEW` and a lane/check traceback in the tables archive. A lane identity or shared evidence failure can still block checks that require that evidence. |
| Fixture | Python 3.10.12, llvm-mc and LLD 18.1.3. All 15 checks returned structured results on a linked ARM ELF. S2 identified two LR_STACK sites, one with the verified path `__entry_fixture → fixture_caller` and one with an empty path. Reinjecting the missing-route NameError changed only S2 to REVIEW. All other 14 results matched the first run exactly. |
| Pins | Static analyzer SHA-256 `727f0f925ef2b1e5a1a9d1bc5a99ce45809d81431b11caba33468b1bd4902ebc`. All seven downloaded file hashes verified. The running build/shelve launcher stays at `d428782`. |

**Native status.** The NzBk1N run recorded STATIC_GATE HOLD and BOARD_FLASH HOLD. Its C7/C8 readback reported a missing supported RPM database. The fixed static run awaits native execution. The board gate remains HOLD pending review of native results.

The original NzBk1N terminal output is archived byte-for-byte, SHA-256 `54dc08637bd8ccc7694647b2e210c3b55a710db5aaeccd98bf00b7b8d36ee0b1`. [Archived evidence](../../artifacts/evidence/native-run-r0013m-static-NzBk1N-20261127.txt)
