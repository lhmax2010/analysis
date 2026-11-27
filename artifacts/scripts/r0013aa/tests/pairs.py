"""Offline S12 CLI, ELF and acceptance regression checks. ARM_LD may name a local ld.lld."""
import contextlib
import hashlib
import io
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

repo = Path(__file__).resolve().parents[4]
launcher = repo / "artifacts/scripts/r0013y/read.sh.txt"
plan = ["Official:37836579=37836693", "Custom:37836654=37836727"]
pub = "http://repos.vd.sec.samsung.net/priv/168.219.236.43:81/PRV/builds/b567/19437567/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261127."
ids = ("37836579", "37836693", "37836654", "37836727")
urls = {qb:pub+str(i)+"/" for i,qb in enumerate(ids, 1)}

def rejected(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return
    raise AssertionError(args)

with TemporaryDirectory() as tmp:
    stage = Path(tmp)
    for line in launcher.read_text().split("done <<'PINS'\n")[1].split("\nPINS")[0].splitlines():
        checksum, name = line.split()
        src = repo/name
        assert hashlib.sha256(src.read_bytes()).hexdigest() == checksum
        shutil.copyfile(src,stage/src.name)
    api = runpy.run_path(str(stage/"s12.py.txt"))
    parse = api["pairs"]
    explicit = plan.copy()
    for qb in ids:
        explicit = [s.replace(qb,qb+"="+urls[qb]) for s in explicit]
    assert parse(explicit)["Custom"] == tuple(q+"="+urls[q] for q in ids[2:])
    assert parse(plan[::-1]) == parse(plan)
    for bad in ([plan[0],plan[0]], [plan[0].replace(ids[0],ids[1]),plan[1]],
                [plan[0],plan[1].replace(ids[2],"37736427")], [plan[0],plan[1].replace(ids[3],"37777264")],
                [plan[0].replace(ids[0],ids[2]),plan[1]]):
        rejected(parse,bad)
    env = api["main"].__globals__
    vd = stage/"vd"
    ws = vd/"workspace"
    work = ws/"temp/pm0013y-s12.test"
    work.mkdir(parents=True)
    (vd/"config").mkdir()
    (vd/"config"/("gbs_qb"+ids[0]+".conf")).write_text("[repo.product_NikeM]\nurl="+urls[ids[0]])
    with patch.dict(env,WS=ws,VD=vd):
        assert api["operand"](ids[0])==(ids[0],urls[ids[0]])
        assert api["operand"](ids[1]+"="+urls[ids[1]])==(ids[1],urls[ids[1]])
        rejected(api["operand"],ids[0]+"="+urls[ids[1]])
        rejected(api["operand"],ids[1])
    mod = dict(name="demo",vermagic="6.12",release="6.12",signed=True,text=40,relocations=[2])
    baseline = dict(build_id="aa",release="6.12",modules={"p!/a.ko":mod},symvers={"map":{"x":2}},text=8564600,helpers=0)
    outline = dict(baseline,build_id="bb",text=8214312,helpers=20324)
    compare = api["compare"]
    assert not compare(baseline,outline)[1]
    for changes in (dict(helpers=0),dict(helpers=20345),dict(text=None),dict(symvers={}),dict(modules={}),
                    dict(modules={"p!/a.ko":dict(mod,signed=False)})):
        assert compare(baseline,dict(outline,**changes))[1]
    assert compare(dict(baseline,helpers=None),outline)[1]
    repro = api["repro"]
    assert repro(baseline,baseline)[0]=="IDENTICAL"
    assert repro(baseline,dict(baseline,modules={ }))[0]=="DIFFERENT"
    assert repro(dict(baseline,text=None),dict(baseline,text=None))[0]=="UNAVAILABLE"
    seen=[]
    def read(label,url,lane,path,qb,inputs=None):
        seen.append(qb)
        if qb=="37777148":
            raise ValueError("historical inputs unavailable")
        if qb=="37777264":
            return dict(baseline,text=33)
        return outline if qb in ids[1::2] else baseline
    def invoke(args,**changes):
        buf=io.StringIO()
        run_dir = work.with_name("pm0013y-s12."+str(len(list(work.parent.iterdir()))))
        run_dir.mkdir()
        changes.setdefault("retained_inputs",lambda *a: {})
        with patch.dict(env,W=run_dir,WS=ws,VD=vd,read_snapshot=read,**changes),patch.object(sys,"argv",["s12",*args]),contextlib.redirect_stdout(buf):
            rc=api["main"]()
        return rc,buf.getvalue()
    rc,out=invoke(explicit)
    assert not rc and "S12_REPRO Official UNAVAILABLE" in out and "S12_REPRO Custom DIFFERENT" in out
    assert "helpers=0/20324" in out and "delta=-350288" in out and "S12 PASS" in out
    seen.clear()
    rc,out=invoke([explicit[0].replace(ids[0]+"="+urls[ids[0]],"38888888"),explicit[1]])
    assert rc and all(q in seen for q in ids[1:]) and "S12 FAIL" in out
    retained=[]
    rc,out=invoke(["--retain",ids[0],ids[3]+"="+urls[ids[3]]],retained_inputs=lambda q,url,l,w:retained.append((q,l)))
    assert not rc and retained==[(ids[0],"Official"),(ids[3],"Custom")] and "S12_RETENTION COMPLETE" in out
    # Use real ARM ELF32 section headers, local text symbols and a GNU build-ID.
    obj,elf=stage/"test.o",stage/"vmlinux"
    asm=".text\n.globl _stext\n_stext: nop\nlocal_function: nop\nOUTLINED_FUNCTION_0: nop\n"
    subprocess.run(["llvm-mc","-triple=armv7-linux-gnueabi","-filetype=obj","-o",obj],input=asm,text=True,check=True)
    subprocess.run([os.environ.get("ARM_LD","ld.lld"),"-e","_stext","--build-id=sha1",obj,"-o",elf],check=True)
    bid=re.search(r"Build ID: (\w+)",subprocess.check_output(["readelf","-n",elf],text=True))[1]
    assert api["symbols"](elf,bid)==(12,1)
    assert api["symbols"](elf,"bad") is None
    assert api["helper_count"]("0010 T _stext\n") is None
print("PASS same-day grammar, distinct IDs/publications, retention, lane isolation, info-only history, module gates, and ARM ELF metrics")
