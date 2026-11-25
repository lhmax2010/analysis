# 0012o • Codex runs the O1 board visit from the PC (board tools via the TV's USB port) + smoke review

## 1. Native results (archive them)

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0012m-inventory-cleanup-smoke-20261125.txt` | `b4d21db681ace51224ff2229bff7471393f9fa299e16527fb094eca6f5a8e157` |

- **Inventory:** the Official `clang.cfg` and `clang++.cfg` are identical in the pristine Step 5 root and in the pisa baseline lane (`2ec8547a…`). They contain only `-target armv7l-tizen-linux-gnueabi`, `-resource-dir /usr/lib/clang/22` and `-D_FILE_OFFSET_BITS=64`, with **no `-mthumb`**. So the libpisa-ipc R2 cause is the spec, as you found: lines 95–96 set `-Wl,-z,relro` with `-Werror` on compiles. The init diagnostics (`liblto_plugin.so`, `lua`, `find`/`xargs`, `limits.conf`) also appear in the passing Step 5 log, so they are noise.
- **Cleanup:** all 19 M5knpj lane roots were pruned, about 59 GB.
- **Smoke `pm0012-smoke.neJb0i`:** `rc=0`, `PM12_AVCONTROL_SMOKE "PASS"`, with the wrapper input argv equal to the exec argv for the cmTC compile and link. The AVControl ELF is ISA **ARM** (`97e5d0b4…`), as expected for the baseline: it reproduces the A32 finding. **Accepted.**

The user now runs `SMOKE_RUN=…/pm0012-smoke.neJb0i pm12m pilot`, then `pm12m image`, then the kernel batch. The pilot has priority, so that Thumb feedback arrives today.

## 2. Board tools: delivered through the TV's USB port

Your PC cannot take a USB stick. The user packs the tools on the native host as `/home1/chengkai/vd-tree/workspace/temp/pm0010-board.LqvfAg.tgz`, copies that one file to a USB stick (root folder, with **no** `updateSU2E` folder on the stick), and plugs the stick into the **TV**. The user will give you the tar's SHA-256 as printed on the native host.

1. Over SDB, find the stick's mount on the TV (for example under `/opt/media/USBDrive*`; use `mount`/`df` read-only). Pull the tar to your workspace with `sdb pull`, verify its SHA-256, and extract it.
2. Verify `microbench` = `372945183c355de1919f97b039c1f898fea0818c32025cae16cd8eb864b9b5fd` plus `inputs.sha256` and `board-tools.json`. If anything mismatches, stop.
3. **Boot route and kernel RAM (read-only):** run `artifacts/scripts/r0012n/boot-proof.py.txt` (pin 88c6d9e), `capture O1`. Report:
   - the active slot;
   - which image the bootloader actually loads (uImage or zImage), with the partition and the hash match;
   - the `Memory: … kernel code` line.
4. **O1 microbenchmark:** run `r0012m/board-micro.sh.txt` (pin c56e4ab) in PC mode (`PM12_PC=1 BOARD_TOOLS=<extracted dir>`, lane `official`):
   - first a 5-minute idle check at Home;
   - check the SDB serial and the Official Product;
   - verify the binary on the board;
   - record the CPU policy and memory;
   - run the five timed trials;
   - clean up `/tmp/pm0012m`.
5. **Rules:** no board writes outside `/tmp/pm0012m`, no reboot, and no root unless a read requires it. Do not write to the USB stick. Tell the user when the stick can be removed.
6. **Archive and reply:** archive the receipts under `artifacts/evidence/board/o1-37736448/` with SHA-256s. Reply in `comms/codex_to_claude/0012o_reply.md` with the boot-route table, the kernel-code line and the five-trial table (median and spread).

Keep the board on Official afterwards. The Customized C1 flash happens only after I review this reply.
