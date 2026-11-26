"""Read local fixtures only. Test input binding, Product identities and USB source verification."""
from pathlib import Path
import gzip
import hashlib
import io
import json
import os
import runpy
import struct
import tarfile
import tempfile
import xml.etree.ElementTree as ET
import zlib

scripts=Path(__file__).resolve().parents[2]/"scripts"
load=lambda n:runpy.run_path(str(scripts/(n+".py.txt")))
p=load("r0012x/new-pair")
gate=load("r0011/qb-pair-gate")
size=load("r0012p/kernel-size")
perf=load("r0009/perf-bundle")
def fail(fn,*args):
    try:
        fn(*args)
    except ValueError:
        return
    raise AssertionError("fixture should have been rejected")
with tempfile.TemporaryDirectory(dir=os.environ["TMPDIR"]) as directory:
    work=Path(directory)
    pub=work/"qb-evidence/37777148-fixture"
    pub.mkdir(parents=True)
    p["submitted"].__globals__["ROOT"]=work
    xml=ET.fromstring("<build><id>fixture</id></build>")
    url="http://example.invalid/qb/"
    def fetch(url,limit):
        if url.endswith("/"):
            return b'<a href="shelves.txt">s</a><a href="base_urls.txt">b</a>'
        return url.encode()
    assert set(p["submitted"](work,pub,"37777148",xml,url,{"fetch":fetch}))=={"SHELVES","BASE_LIST"}
    empty=work/"unknown";empty.mkdir()
    assert not p["submitted"](work,empty,"2",xml,url,{"fetch":lambda *_:b""})
    cfg=b"[general]\nprofile=profile.q\n[profile.q]\nrepos=repo.product, repo.base\nbuildroot=/outside\n[repo.product]\nurl=product\n[repo.base]\nurl=base\n"
    assert p["normalized_config"](cfg,"product","base")==p["normalized_config"](cfg.replace(b"outside",b"another"),"product","base")
    fail(p["normalized_config"],cfg,"wrong","base")
    key=("x","armv7l")
    r=dict(epoch="0",version="1",release="1",srpm="x-1-1.src.rpm",vcs="//p#21",sha256="1")
    assert not p["sources"]({key:r},{key:dict(r,release="2",srpm="x-1-2.src.rpm",sha256="2")},gate,work)
    for change in [dict(vcs="//p#22"),dict(vcs="floating"),dict(version="2")]:
        assert p["sources"]({key:r},{key:dict(r,**change)},gate,work)
    file=pub/"fixture-PERF.tar.gz"
    payload=b"kernel"+size["NOTE"]+bytes(range(20))
    hdr=bytearray(64); hdr[:4]=bytes.fromhex("27051956");hdr[28:32]=bytes([5,2,2,0])
    struct.pack_into(">I",hdr,12,len(payload));struct.pack_into(">I",hdr,24,zlib.crc32(payload))
    struct.pack_into(">I",hdr,4,zlib.crc32(hdr))
    images=dict(uImage=bytes(hdr)+payload,zImage=b"loader"+gzip.compress(payload))
    with tarfile.open(file,"w:gz") as t:
        for name in perf["REQUIRED"]|{"partition_8G.txt"}:
            data=images.get(name,(name+" content").encode()); h=tarfile.TarInfo(name);h.size=len(data)
            t.addfile(h,io.BytesIO(data))
    digest=perf["sha"](file)
    (pub/"identity.json").write_text(json.dumps(dict(qb_id_operator_supplied="37777148",payloads=[dict(file=file.name,sha256=digest,bytes=file.stat().st_size)],files={file.name:digest})))
    for fn in (perf["captured"],perf["stage"],p["verified_usb"]):
        fn.__globals__.update(WORKSPACE=work,WS=work,RESERVE=1)
    usb=p["verified_usb"]("37777148",pub,perf)
    assert p["verified_usb"]("37777148",pub,perf)==usb
    checks={"/perf/"+k:(len(v),hashlib.sha256(v).hexdigest()) for k,v in images.items()}
    _,bid=p["kernel"]("37777148",usb,file,{"member_checksums":lambda _:checks},size)
    assert bid==bytes(range(20)).hex()
    (usb/"dtb.bin").write_bytes(b"bad")
    fail(p["verified_usb"],"37777148",pub,perf)
print("PASS submitted inputs, absent evidence, config, source changes, fresh and reused USB, build ID and damaged DTB")
