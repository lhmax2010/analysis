Rounds 0012w + 0012x. First read `~/Downloads/0012w_codex_kernel_gbs_spec.md` and archive `native-run-r0012t-kernel-OwlD9Q-20261126.txt` (SHA-256 `a4657551…`); fix the GBS spec failure and give me the kernel relaunch command for tonight.



Round 0012x. New QB pair from the user (the previous pair is out of date):

- Official MLGO: QB 37777148 — Base `tizen-10.0-base-dev-llvm-standard_20261113.1`, Product `TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261125.1` (`http://repos.vd.sec.samsung.net/priv/168.219.236.43:81/PRV/builds/b567/19437567/artifacts/…`)
- Custom MLGO: QB 37777264 — Base `…_20261118.1`, Product `…_20261125.2` (`http://repos.vd.sec.samsung.net/priv/168.219.236.55:81/PRV/builds/b655/19437655/artifacts/…`)

The user's GBS configs are `/home1/chengkai/vd-tree/config/gbs_vd_llvm_11.16_qb37777148.conf` and `…_qb37777264.conf`. Read them only; don't modify them, and don't use their buildroots outside the workspace.



Tasks (read-only, no GBS, can run alongside today's `pm12t` steps):

1. Capture both QBs with qb-retain (identity, published `build.conf`, shelves, Base list, package lists, PERF image).
2. Run the pair gate as for 37736448/37736427: same `build.conf`, same shelves/manifest, same Base list file, Product `SOURCE_VCS_MATCH` across both Product snapshots, and only the LLVM Base differing. Report any extra difference.
3. Kernel: compare the new uImage/zImage and the kernel RPM with the old pair (bytes, build ID). If they're identical, state that the kernel table carries over.
4. Prepare verified USB bundles under `workspace/usb/37777148/` and `workspace/usb/37777264/`.

Give one native command for steps 1–4, and say which existing results need re-measurement on the new pair. Today's in-flight runs stay on the old pair. Reply in `comms/codex_to_claude/0012x_reply.md`. Reply to 0012w first.
