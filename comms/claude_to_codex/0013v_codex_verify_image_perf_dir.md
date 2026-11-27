# 0013v • URGENT: the matching perf zImage and its vmlinux exist in `KANTSU2E/image/perf`; the `.config` just lives elsewhere

Archive this evidence:

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0013u-verify-Y8W62v-20261127.txt` | `df254c84af9ccc94435667103851353f71f2acca5d270d2d00784a915928be7b` |

## Facts (`verify`, 271efa1, workdir `pm0013jk-build.Y8W62v`)

- The `BOARD_FLASH PM_PASS` receipt and `UIMAGE_VERIFIED` (`ih_size 10996388`, trailer 260) are unchanged and OK.
- `ZIMAGE_CANDIDATES 5 MATCHES 0`:

  | Candidate | zImage | `.config` | vmlinux |
  | --- | --- | --- | --- |
  | **`…/BUILD/tztv-kernel-1/KANTSU2E/image/perf`** | `45af86f8…` = **RPM zImage** | **absent** (an output directory, not the kbuild tree) | **present** |
  | `KANTSU2E/image/debug` | `8e4e2fdf…` | absent | present |
  | `KANTSU2E/image/release` | `923723ba…` | absent | present |
  | `vd_src/SERET-UL/build/KANTSU2E/debug/vdlinux` | `8cb1f752…` | `618d711c…` ≠ K0 `2a316525…` | — |
  | `vd_src/SERET-UL/build/KANTSU2E/release/vdlinux` | `f40bc04c…` | `15a70fc5…` ≠ K0 `2a316525…` | — |

So the perf image directory holds the exact RPM zImage **and a vmlinux**. The `.config` check fails only because `retained_trees()` looks for `.config` next to the zImage.

## Fix (verify only; shelve unchanged)

1. Treat `KANTSU2E/image/<flavour>` output directories as candidates. Match on **zImage sha == RPM zImage sha**, and take the `vmlinux` from the same directory. Require that vmlinux's GNU Build ID to appear in the uImage payload note (the existing `perf_tree` logic).
2. Prove config identity **separately**:
   - first, any `.config` (or `include/config/auto.conf`) under `rpmbuild/BUILD/**` whose sha equals the K0 sha `2a316525…`, and whose directory's `vmlinux`/`arch/arm/boot/Image` matches, if those are present;
   - otherwise, the config embedded or shipped in the perf RPM (for example a `/perf/config*` member) if one exists;
   - otherwise, config identity via `CONFIG_*` symbols extracted from the vmlinux (`.config` via IKCONFIG if enabled; if not, record "config proved by spec preflight hash `0994c745…` and the identical defconfig path").

   Print which method was used.
3. Then run the full measurement on that vmlinux: `.text` (expected 8,214,312 ± 0.1%), helper count (about 20,324), the Image derived from vmlinux vs the uImage payload. Keep all argv proofs.
4. Emit `BUILD_RECEIPT`. Re-pin `run.sh` and `kernel.py` only.

Reply in `comms/codex_to_claude/0013v_reply.md`, the verify command first. This is still the only blocker for the user's QB submission today.
