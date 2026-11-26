"""Filesystem fixtures for the three deletion scopes and the disk-only continuation."""
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import tempfile
from unittest.mock import patch

SCRIPTS=Path(__file__).resolve().parents[2]/"scripts/r0013e"
def module(name):
    env=runpy.run_path(str(SCRIPTS/(name+".py.txt")))
    return next(v for v in env.values() if callable(v) and getattr(v,"__module__",None)=="<run_path>").__globals__
def put(path,data=b"x"):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data)
    return path
def sha(data):return hashlib.sha256(data).hexdigest()
def rejects(f):
    try:f()
    except (ValueError,OSError):return
    raise AssertionError("unexpected admission")

def test(temp):
    c=module("reclaim")
    c["TEMP"]=temp
    for bad in c["FORBIDDEN"]:
        rejects(lambda:c["safe"](temp/bad/"GBS-ROOT"))
    link=temp/"link"
    link.symlink_to(temp.parent)
    rejects(lambda:c["safe"](link/"cache"))
    mount=temp/"mount"
    put(mount/"mountinfo",b"1 0 8:0 / /targets/child rw - x\n")
    rejects(lambda:c["mount_guard"](mount,["/targets"]))
    c["idle"]=lambda paths:None  # Underlying scope and receipt tests run without root.
    root=temp/c["HIST"][0]
    guest=root/"local/BUILD-ROOTS/scratch.armv7l.0"
    for f in ("home/abuild/only","var/tmp/proof","var/log/log","usr/bin/tool"):put(guest/f)
    for f in ("foo.rpm","log.txt"):put(root/"local/repos"/f)
    c["historical"](False)
    assert guest.exists()
    c["historical"](True)
    assert not guest.exists() and (root/"pm0013e-retained/scratch.armv7l.0/var/tmp/proof").exists()
    package="000-N4-lib-a"
    run=temp/"pm0013-pkg.123abc"
    folder=run/package/"baseline"
    binary=put(folder/"elf-proof"/(sha(b"x")+".elf"))
    put(folder/"GBS-ROOT/local/repos/lib-a-1-1.armv7l.rpm")
    scratch=put(folder/"GBS-ROOT/local/BUILD-ROOTS/scratch.armv7l.0/bin/x")
    for f in ("gbs.log","driver-argv.txt","link-argv.txt"):put(folder/f)
    put(folder/"lane.json",json.dumps(dict(label="baseline",error=None,metrics=dict(files=[dict(sha256=sha(b"x"),rpm="lib-a")]))).encode())
    binary.write_bytes(b"bad")
    rejects(lambda:c["package_lane"](run,package,"baseline",True))
    assert scratch.exists()
    binary.write_bytes(b"x")
    c["package_lane"](run,package,"baseline",True)
    assert binary.exists() and not scratch.exists()
    job=temp/"pm0012-kernel.123abc/jobs/kernel-thumb"
    lane=job/"K1"
    guest=lane/"GBS-ROOT/local/BUILD-ROOTS/scratch.armv7l.0"
    source=guest/"var/tmp/pm0013d-evidence"/sha(b"x")
    saved=lane/"pm0013e-build-evidence"/sha(b"x")
    symbols=job/"symbols/123/K1"
    hashes={k:sha(b"x") for k in ("vmlinux","System.map",".config")}
    for f in hashes:put(symbols/f);put(source/f)
    for f in ("complete","arch/arm/boot/zImage","mm/.a.o.cmd","net/core/.b.o.cmd","arch/arm/.c.o.cmd","kernel/sched/core.o"):put(source/f)
    for f in ("gbs.log","GBS-ROOT/local/repos/tztv-kernel-perf-1-1.armv7l.rpm","uImage","zImage","generated.config"):put(lane/f)
    row=dict(intended_config=True,argv_proof={"verdict":"PASS"},sizes={"x":1},static={"x":1},
             images={n:[1,sha(b"x")] for n in ("uImage","zImage")},
             symbols=dict(build_id="123",directory=str(symbols),sha256=hashes))
    rejects(lambda:c["stash_kernel"](job,"K1",row,True))
    put(source/"kernel/sched/.core.o.cmd")
    c["stash_kernel"](job,"K1",row,False)
    assert guest.is_dir()
    c["stash_kernel"](job,"K1",row,True)
    assert (saved/"kernel/sched/core.o").exists() and not guest.exists() and (symbols/".config").exists()
    assert c["stash_kernel"](job,"K1",row,True)==0
    rejects(lambda:c["stash_kernel"](job,"K0",row,True))
    retry=module("disk-resume")
    refusal={"status":"BLOCKED_OR_FAILED","diagnostic":"D-018 headroom needs 50+55 GiB disk and 16+16 GiB RAM"}
    old=temp/"pm0012-kernel.9abcde"
    oldjob=old/"jobs/kernel-thumb"
    for name,key in (("downloads.tsv","INDEX"),("kernel-matrix.py.txt","MATRIX")):
        put(old/name);retry[key]=sha(b"x")
    put(old/"status.txt",b"date DONE kernel rc=1\n")
    effective=put(oldjob/"official.config")
    rows={k:{"status":"RAW_ONLY"} for k in retry["LANES"]}
    rows["K0"].update(qualification={"config_bytes_equal":True},images={"uImage":[11348968,"0"]})
    for refused in (set(),{"K4"},{"K5"},{"K4","K5"}):
        log=""
        for k in retry["LANES"]:
            if k in ("K4","K5"):rows[k]=refusal if k in refused else {"status":"RAW_ONLY"}
            log+=f"CAPACITY disk_free_gib {99 if k in refused else 123} ram_available_gib 32\nKERNEL_THUMB_LANE {k} {rows[k]['status']}\n"
        put(oldjob/"job.log",log.encode());put(oldjob/"kernel-matrix.json",json.dumps(rows).encode())
        assert retry["read"](temp,"auto",effective)[2]==refused
    for free,ram in ((105,32),(95,31)):
        assert not retry["disk_only"](refusal,f"CAPACITY disk_free_gib {free} ram_available_gib {ram}",oldjob/"K4")
    put(oldjob/"K4/gbs.log")
    assert retry["read"](temp,"auto",effective)[2]=={"K5"}
    # Local bytes + primary entry + live response are independent deletion gates.
    r=module("rpm-originals")
    r["TEMP"]=temp
    r["HERE"]=temp
    for name in r["ROOTS"]:(temp/name).mkdir(parents=True)
    a,b,unmatched=[put(temp/r["ROOTS"][0]/n,data) for n,data in (("a.rpm",b"a"),("b.rpm",b"b"),("lost.rpm",b"?"))]
    class Response(io.BytesIO):
        def geturl(self):return self.url
    class Server:
        def open(self,url,timeout):
            res=Response(b"a" if url.endswith("/a.rpm") else b"wrong")
            res.url=url
            return res
    entries={sha(n.encode()):[("http://example/"+n+".rpm","primary","abc")] for n in ("a","b")}
    mf=temp/"manifest.tsv"
    r["scan"](entries,mf)
    rejects(lambda:r["remove"](entries,mf,"wrong",Server()))
    r["remove"](entries,mf,sha(mf.read_bytes()),Server())
    assert not a.exists() and b.exists() and unmatched.exists() and mf.exists()

if __name__=="__main__":
    with tempfile.TemporaryDirectory() as d:test(Path(d))
    print("0013e receipts, protected paths, three deletion scopes and recovery selection PASS")
