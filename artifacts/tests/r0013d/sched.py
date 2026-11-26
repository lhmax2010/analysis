"""Exercise the scheduler argv and lane-continuation contracts using local evidence."""
import os
from pathlib import Path
import runpy
import tempfile

art=Path(__file__).resolve().parents[2]
m=runpy.run_path(str(art/"scripts/r0012f/kernel-matrix.py.txt"))
with tempfile.TemporaryDirectory(dir=os.environ["TMPDIR"]) as temp:
    seen=[]
    for lane in m["LANES"]:
        tree=Path(temp)/lane
        tree.mkdir()
        log=tree/"gbs.log"
        off=lane in ("K2","K3")
        lines=[]
        for g in m["GROUPS"]:
            obj=g+"core"
            args=["-mllvm -"+n+"=release" for n in m["ADVISORS"]] if not off else []
            if lane in ("K1","K3","K5"):args.append("-moutline")
            if lane=="K5":args.extend(["-marm","-mthumb"])
            cmd="clang -D__KERNEL__ "+" ".join(args)
            args2=f"-c -o {obj}.o ../linux-6.12/{obj}.c"
            if lane=="K2" and g=="mm/":continue
            if lane=="K1":
                directory=tree/g
                directory.mkdir(parents=True)
                (directory/".core.o.cmd").write_text("savedcmd_x := "+cmd+" "+args2+"\n")
            else:
                lines += ["[  187s] "+cmd+" \\", "[  187s] "+args2]
        for n in m["ADVISORS"]:lines.append("[  187s] --"+n+" = "+("default" if off else "release"))
        log.write_text("\n".join(lines)+"\n")
        r=m["review_argv"](tree,lane,log)
        seen.append(r["verdict"])
        print(lane,r["verdict"],r["reasons"])
        if lane=="K0":assert r["groups"]["kernel/sched/"]["last_mode"]=="Clang default A32" and not r["cmd_exists"]
        if lane=="K1":assert r["cmd_exists"]
    assert seen==["PASS","PASS","REVIEW","PASS","REVIEW","PASS"],seen
    assert not m["flags"](["clang","--target=thumbv7-linux-gnueabi"],"K0")["checks"]["isa"]
    assert not m["compile_unit"]("echo clang -D__KERNEL__ -c kernel/sched/core.c -o kernel/sched/core.o")
    assert m["review_argv"](tree,"K0",tree/"absent")["verdict"]=="REVIEW"
