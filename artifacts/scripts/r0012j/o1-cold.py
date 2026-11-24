"""Collect three scheduled O1 samples following an operator Home readiness receipt."""
import json
from pathlib import Path
import runpy
import sys
import time

board = runpy.run_path(str(Path(__file__).with_name("o1-board.py")))
out = Path(sys.argv[1])
old_boot = sys.argv[2]
anchor = json.loads((out/"home-receipt.json").read_text())["pc_monotonic"]
read = board["read"]
rc, boot = read(out, "confirmed-boot.txt", "cat /proc/sys/kernel/random/boot_id")
boot = boot.strip().decode()
if rc or not boot or boot == old_boot:
    sys.exit("Cold boot unconfirmed")
read(out, "confirmed-product.txt", "cat /etc/prd_info.ini; cat /proc/version /proc/uptime; id -u")
board["privileged"](lambda: read(out, "early-memory-log.txt",
    "dmesg | grep -iE 'Memory:|cma:|reserved.memory|reserved mem|carve.?out|zone ranges|early memory node'"))
read(out, "before-settle-uid.txt", "id -u")
print("O1_COLD_BOOT", boot, flush=True)
with (out/"sample-timing.tsv").open("x") as timing:
    print("sample\trequested_s\tstart_s\tend_s", file=timing, flush=True)
    for number, offset in enumerate((300,360,420), 1):
        time.sleep(max(0, anchor + offset - time.monotonic()))
        started = time.monotonic() - anchor
        board["sample"](out,number,boot)
        end = time.monotonic() - anchor
        print(f"{number}\t{offset}\t{started:.3f}\t{end:.3f}",file=timing,flush=True)
        print("O1_SAMPLE",number,round(started,1),round(end,1),flush=True)
read(out,"exit-state.txt","cat /proc/sys/kernel/random/boot_id; id -u; test ! -e /tmp/pm0012j && echo NO_SCRATCH")
