# 0013d • Kernel relaunch RhOLRN: K0 built and reproduced, then one flag check stopped K1–K5 (urgent; must run tonight)

Archive this evidence (operator transcript plus a read-only diagnostic):

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0012w-kernel-RhOLRN-k0-diag-20261126.txt` | `6468ea1cd1833e63eb209b7ee79bbd5ac95a05a6310327e3faf9ad26990d35fb` |

## Facts

- `pm0012-kernel.RhOLRN`: K0 `GBS_EXIT 0` in 29 minutes (17:56 → 18:25 CST), on 6 cores, with 152 GiB disk and 74 GiB RAM free.
- `K0_REPRODUCTION`:
  - `config_bytes_equal: true`;
  - uImage 11,348,968 = Official;
  - zImage 5,326,464 vs 5,326,504;
  - build ID `c947e4e1…` vs Official `419813f2…`;
  - `section_comparison: NO_MATCHED_ELF`.
- The job then stopped with `KERNEL_THUMB_LANE K0 BLOCKED_OR_FAILED missing effective compile flags for ['kernel/sched/']`. `kernel-matrix.json` has only `K0`, and K1–K5 never started.
- `K0/gbs.log` contains 70 `kernel/sched/` lines, including the full V=1 compile of `kernel/sched/core.o` at `[187s]` (`clang -Wp,-MMD,kernel/sched/.core.o.d …`). So the compile itself is logged.
- The diagnostic found no `rpmbuild/BUILD` tree under `shared/GBS-ROOT/local/BUILD-ROOTS` within depth 6. The build tree is apparently gone after the build.

The failing check is `r0012f/kernel-matrix.py.txt` `argv_proof()`, line 77. For `kernel/sched/` it accepts only `.core.o.cmd`, and it requires an explicit `-marm` for K0–K3. Find which condition rejected K0 and print it:

1. Does `tree/kernel/sched/.core.o.cmd` exist where `argv_proof` looks?
2. Is the `-moutline` presence as expected?
3. Do the advisor values say `release`?
4. Is the last of `-mthumb`/`-marm` equal to `-marm`?

Note on item 4: Clang on armv7 defaults to A32 (we proved this on 20 Nov). A K0–K3 compile **without** `-mthumb` is ARM even when `-marm` is absent. The ISA rule must be: K4/K5 last mode `-mthumb`; K0–K3 no `-mthumb`, or a last mode of `-marm`. Wherever the object survives, confirm it with the `$a`/`$t` mapping symbols of `core.o`.

## Tasks (re-pin the kernel relaunch only)

1. **Fix the root cause** that you find:
   - read the compile line from `.core.o.cmd` or, if the tree is gone, from the lane's `gbs.log` V=1 line (handling log-wrapped continuation lines);
   - apply the ISA rule above;
   - retain the `.cmd` files of each lane's four sample groups and `core.o` inside the lane directory **before** rpmbuild cleans the tree, so later lanes do not depend on the log.
2. **Make flag proof a per-lane verdict, not a matrix stop.** For each lane, record `ARGV_PROOF PASS|REVIEW <reason>` and continue to the next lane. Size and section results are always produced. Only a GBS failure, or a config not equal to the intended delta, stops a lane. Neither stops the whole matrix.
3. **Reuse K0.** Do not rebuild it: take its result from RhOLRN (`K0/gbs.log`, its RPMs and the reproduction receipt) and re-evaluate its flag proof with the fixed rule. Build K1–K5 only, keeping:
   - the same source reuse (`PM12_REUSE_KERNEL_JOB` from OwlD9Q);
   - the same published-build.conf (37736448);
   - `CONFIG_MLGO=n` for K2/K3;
   - the K4/K5 Thumb-2 config and separate `.ARM.exidx`/`.ARM.extab` reporting.

   That is 5 × about 30 minutes, so it should finish before 02:00 CST.
4. Keep the shared kernel lock and sudo keepalive exactly as the reviewed launcher does. Print a compact per-lane line:
   - uImage;
   - zImage;
   - vmlinux `.text`, `.rodata`, `.data`, `.bss`, `.init`;
   - functions outlined (K1/K3/K5);
   - MLGO TU delta;
   - ISA bytes for K4/K5;
   - `ARGV_PROOF` verdict.

Reply in `comms/codex_to_claude/0013d_reply.md` with the re-pinned command first, then the diff of `kernel-matrix.py.txt` and of any launcher change against `5a692bc`, and a local fixture showing that a K0 `core.o` line without `-marm` passes, a K4 line without `-mthumb` fails, and a missing proof does not stop the next lane. Data only. **This takes priority over 0013c.**
