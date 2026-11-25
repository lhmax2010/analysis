"""Validate HQ measurements, DWARF inline locations and the prerequisite using offline fixtures."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import runpy
import struct
import subprocess
import tempfile
import zlib

root=Path(__file__).resolve().parents[3]/"artifacts"
def load(name):
    return runpy.run_path(str(root/"scripts"/name))
m=load("r0012n/outline-metrics.py.txt")
matrix=load("r0012f/kernel-matrix.py.txt")
def u32(value):return struct.pack("<I",value)
def unit(data):return u32(len(data))+data
def fails(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("expected rejection")

with tempfile.TemporaryDirectory(dir=os.environ["TMPDIR"]) as tmp:
    w=Path(tmp)
    payload=bytes(range(256))*12
    encoded=gzip.compress(payload)
    header=bytearray(64);header[:4]=bytes.fromhex("27051956")
    header[12:16]=len(payload).to_bytes(4,"big");header[24:28]=zlib.crc32(payload).to_bytes(4,"big")
    header[28:32]=bytes([5,2,2,0]);header[4:8]=zlib.crc32(header).to_bytes(4,"big")
    u=header+payload+b"trailer";z=b"boot stub"+encoded+b"padding"
    info=m["image_pair"](u,z)
    assert (info["uImage"],info["zImage"],info["gzip_bytes"])==(len(u),len(z),len(encoded))
    fails(lambda:m["image_pair"](u,z[:-12]))
    bad=bytearray(u);bad[4]^=1;fails(lambda:m["image_pair"](bad,z))
    # Minimal DWARF v4 with an inlined function in [1000,1004) inside caller [1000,1010).
    # Real addr2line must report the enclosing call_file (1), call_line (9).
    def abbrev(i,tag,children,*attrs):return bytes([i,tag,children,*attrs,0,0])
    abbrevs=(abbrev(1,0x11,1,0x03,0x08,0x10,0x17,0x11,0x01,0x12,0x06)+
             abbrev(2,0x2e,0,0x03,0x08,0x20,0x0b)+
             abbrev(3,0x2e,1,0x03,0x08,0x11,0x01,0x12,0x06)+
             abbrev(4,0x1d,0,0x31,0x13,0x11,0x01,0x12,0x06,0x58,0x0b,0x59,0x0b)+b"\0")
    prefix=b"\x04\0"+u32(0)+b"\x04\x01sched.c\0"+u32(0)+u32(0x1000)+u32(16)
    abstract=len(prefix)+4
    di=unit(prefix+b"\x02inline_fn\0\x03\x03caller\0"+u32(0x1000)+u32(16)+b"\x04"+u32(abstract)+
            u32(0x1000)+u32(4)+bytes([1,9,0,0]))
    prolog=bytes([1,1,1,251,14,13,0,1,1,1,1,0,0,0,1,0,0,1])+b"\0sched.c\0\0\0\0\0"
    program=b"\0\x05\x02"+u32(0x1000)+b"\x01\x02\x10\0\x01\x01"
    dl=unit(b"\x04\0"+u32(len(prolog))+prolog+program)
    prior=runpy.run_path(str(root/"tests/r0012l/check.py"))
    old=w/"old";old.write_bytes(prior["elf"]()[0])
    cmd=["llvm-objcopy"]
    for sec,data in ((".debug_info",di),(".debug_abbrev",abbrevs),(".debug_line",dl)):
        p=w/sec;p.write_bytes(data);cmd.extend(["--add-section",f"{sec}={p}"])
    peer=w/"vmlinux";subprocess.run([*cmd,old,peer],check=True)
    frames=m["frames"](peer,[0x1000,0x1004])
    assert [loc for _,loc in frames[0x1000]]==["sched.c:1","sched.c:9"] and frames[0x1000][1][0]=="caller",frames
    assert m["inline_kind"](frames[0x1004])=="NO_INLINE_FRAME_RECORDED"
    assert m["inline_kind"]([("caller","??:0")])=="UNKNOWN_DWARF"
    body=[(0x2000,"add","r0, r1"),(0x2004,"bx","lr")]
    site=dict(pc=0x1000,caller="caller",section=".text",before=[],after=[],input_candidates=[("kernel/sched/core.o",".text")])
    helpers={0x2000:dict(name="OUTLINED_FUNCTION_0",bytes=8,body=body,calls=[site])}
    oldins=[(0x1000,"add","r0, r1"),(0x1004,"bx","lr")]
    dis=lambda p:[(".text","caller",0x1000,oldins)]
    out=m["write_sites"](w,peer,peer,helpers,dis)
    assert out["site_counts"]=={"INLINE":1} and out["mapped_original_bytes"]=={"INLINE":4} and out["hot_path_sites"]==1,out
    oldins.extend([(0x1008,"add","r0,r1"),(0x100c,"bx","lr")])
    assert not m["original_ranges"](peer,helpers,dis)[(0x2000,0x1000)]
    for args,label in [(("push","{lr}"),"PROLOGUE_EPILOGUE"),(("str","r0, [sp]"),"SPILL_RELOAD"),
                       (("bl","0xc000"),"CALL_SETUP"),(("add","r0,r1"),"OTHER")]:
        assert m["body_pattern"]([(0,*args)])==label
    assert m["hot"]("drivers/media/a.o","f")=="media" and not m["hot"]("fs/test.o","k")
    rows={k:dict(status="STATIC_MEASURED",outliner_hq={".text":n}) for k,n in zip(matrix["LANES"],[100,84,120,116,110,108])}
    m["write_summary"](w,rows)
    assert json.loads((w/"outline-interaction.json").read_text())["bytes"][".text"]["interaction"]==-12
    rows["K0"]["status"]="RAW_ONLY";m["write_summary"](w,rows)
    assert not json.loads((w/"outline-interaction.json").read_text())["qualified"]
    smoke=w/"pm0012-smoke.fixture";j=smoke/"jobs/thumb-org.tizen.AVControl";j.mkdir(parents=True)
    (smoke/"status.txt").write_text("DONE smoke rc=0\n")
    (j/"job.log").write_text('PM12_AVCONTROL_SMOKE "PASS"\n')
    fails(lambda:matrix["smoke_gate"](w,str(smoke)))
    with (j/"job.log").open("a") as f:
        f.write('PM12_SMOKE_ELF [["rpm","file","ARM","sha"]]\nPM12_SMOKE_ARGV '+json.dumps(
            {k:{"wrapper_input":["clang","cmTC"],"exec":["clang","cmTC"]} for k in ("compile","link")})+'\n')
    matrix["smoke_gate"](w,str(smoke))
print("PASS separate image sizes, gzip denominator, header and payload CRC, real ARM DWARF inline DIE/call_file/call_line, ambiguous ranges, pattern and hot rows, interaction and smoke gates")
