"""Exercise the spec's actual perf-defconfig edit with Bash 3.2 and check matrix gates."""
from pathlib import Path
import tempfile
import os
import runpy
import subprocess
import sys

root=Path(__file__).resolve().parents[2]
matrix=runpy.run_path(str(root/"scripts/r0012f/kernel-matrix.py.txt"))
patch=(root/"patches/kernel/perf-machine-outliner.spec.patch").read_text()
block="case \"$pm_lane\" in K2|K3)"+patch.split('+case "$pm_lane" in K2|K3)',1)[1].split('+esac',1)[0]+"esac\n"
block=block.replace("\n+","\n")
with tempfile.TemporaryDirectory(dir=os.environ["TMPDIR"]) as d:
    f=Path(d)/"linux-6.12/arch/arm/configs/KANTSU2E_perf_defconfig"
    f.parent.mkdir(parents=True)
    for lane in ("K0","K1","K2","K3"):
        f.write_text("CONFIG_MLGO=y\nCONFIG_OTHER=y\n")
        subprocess.run([sys.argv[1],"-eu","-c",block],cwd=d,env=dict(os.environ,pm_lane=lane),check=True)
        off=lane in ("K2","K3")
        assert f.read_text()==(("# CONFIG_MLGO is not set" if off else "CONFIG_MLGO=y")+"\nCONFIG_OTHER=y\n")
base=dict(CONFIG_MLGO="y",CONFIG_MLGO_INLINER="y",CONFIG_MLGO_REGALLOC="y",CONFIG_OTHER="y")
changed=dict(CONFIG_MLGO="n",CONFIG_OTHER="y")
assert matrix["off_config"](base,changed)
assert not matrix["off_config"](base,dict(changed,CONFIG_OTHER="n"))
for lane,off in (("K0",False),("K1",False),("K2",True),("K3",True)):
    with tempfile.TemporaryDirectory(dir=os.environ["TMPDIR"]) as d:
        t=Path(d)
        flags="" if off else "-mllvm -enable-ml-inliner=release -mllvm -regalloc-enable-advisor=release"
        for g in matrix["GROUPS"]:
            p=t/g;p.mkdir(parents=True)
            cmd=f'clang -D__KERNEL__ -c {g}core.c -marm {flags}'
            (p/'.core.o.cmd').write_text('cmd := '+cmd+(' -moutline' if lane in ("K1","K3") else ''))
        mode='default' if off else 'release'
        (t/'kernel/sched/core.o.pm0012f-options').write_text(''.join(f'--{name} = {mode}\n' for name in matrix["ADVISORS"]))
        argv,_=matrix["argv_proof"](t,lane)
        assert matrix["advisor_argv"](argv["kernel/sched/"])==flags.split()
print("PASS K0-K3 parent edit, effective config drift gate and scheduler argv comparison")
