# 0013u • URGENT: verify got further. uImage is OK, but `perf_tree` finds no vmlinux, because the spec deletes it after a successful build

Archive this evidence:

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0013s-verify-BbbAhy-20261127.txt` | `ba02d39579a4e3244d109c789ebdfaa32d9c815a9341c45ac2e09c4f3b4ac916` |

## Facts (`verify`, dad2b85, workdir `pm0013jk-build.BbbAhy`, retained `jEMVH7`)

- `BOARD_FLASH PM_PASS` receipt `060446c6…`, with `S12_REQUIRED_BEFORE_FLASH`. `S11_REMAINING` is `mrcne` TPIDRURO in both lanes.
- `UIMAGE_VERIFIED`: `ih_size` **10,996,388** (that is **byte-for-byte the K1 Image size**), `ih_dcrc 9742a207`, header CRC OK, trailer 260 = the Official trailer.
- It then failed in `perf_tree`: `no single perf tree matches RPM zImage SHA-256, config and uImage build ID`.

## Likely cause

`perf_tree` requires `tree/vmlinux`. The tztv-kernel spec **deletes `vmlinux`, `System.map` and `.btf.*` after packaging**; the K1/K3 `GCC_CONTEXT` shows `+ rm -f vmlinux`, `+ rm -f System.map`. The K1/K3 trees kept vmlinux only because those builds failed earlier, at SERET-UL. A successful build like `jEMVH7` has no vmlinux left, so no tree can match. Second check: `goodcfg` is the sha of `dkyJ0S/K0/generated.config`. Make sure the jEMVH7 perf `.config` is expected to be byte-equal to that (same defconfig, same toolchain detection). If it is not, print the actual sha and the diff of symbols.

## Fix (verify mode only; build and shelve unchanged)

1. Print a diagnostic for every zImage candidate tree: the zImage sha vs RPM, the `.config` sha vs `goodcfg`, whether vmlinux, System.map and `.config` exist, and the tree path.
2. Accept the perf tree on **zImage sha equality + `.config` equality**. For the ELF:
   - first look for a vmlinux in the build's other RPMs (debuginfo or devel) in `GBS-ROOT/local/repos/**`, or in a retained copy, and match its Build ID against the uImage payload;
   - if no ELF exists, derive the build ID from the payload's GNU note and accept the size gate on **Image size equality with K1 (10,996,388)** plus zImage size within 0.1%. Mark `.text` and the helper count `NOT_MEASURED_NO_ELF`.
3. Keep every argv proof (SERET-UL GCC without `-moutline`; Clang kernel and modules with it) from the retained logs and `.cmd` files.
4. Emit `BUILD_RECEIPT`, and re-pin `run.sh` and `kernel.py` only. The `shelve` path stays byte-identical.

Reply in `comms/codex_to_claude/0013u_reply.md`, the verify command first. This is the only thing blocking the user's QB submission today.
