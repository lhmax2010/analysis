"""Verify the feature-dependent union, partition offset and independent compressed-file census."""
import os
from pathlib import Path
import runpy
import struct
import subprocess
import sys
import tempfile

tree=runpy.run_path(str(Path(__file__).resolve().parents[2]/"scripts/r0012c/image-tree.py.txt"))
tools=Path(sys.argv[1]).resolve()
with tempfile.TemporaryDirectory(dir=os.environ["TMPDIR"]) as tmp:
    work=Path(tmp)
    data=bytearray(4096)
    data[1024:1028]=bytes.fromhex("e2e1f5e0")
    raw=work/"union.img"
    for flags,word in [(0x180,0x10),(0x182,0x10),(0x182,9)]:
        struct.pack_into("<IH",data,1104,flags,word)
        struct.pack_into("<H14xH14x",data,1152,14,14)
        raw.write_bytes(bytes(4096)+data)
        try:
            info=tree["filesystem"](raw,4096)
        except tree["IntegrityError"] as err:
            assert flags==0x182 and word==0x10 and "unsupported algorithm bits=0x10" in str(err)
        else:
            if flags==0x180:
                assert info["lz4_max_distance"]==16 and "available_compr_algs" not in info
            else:
                assert word==9 and info["compression_config"]==["LZ4","ZSTD"]
    src=work/"src"
    src.mkdir()
    (src/"example").write_bytes(b"abcde"*50000)
    for name,opts,compressed in (("plain",[],False),("lz4",["-zlz4"],True),("zstd",["-zzstd"],True)):
        image=work/name
        subprocess.run([tools/"mkfs.erofs",*opts,image,src],check=True,stdout=subprocess.DEVNULL)
        joined=work/"partition"
        joined.write_bytes(bytes(4096)+image.read_bytes())
        info=tree["filesystem"](joined,4096)
        stats=tree["command"](tools/"dump.erofs","-S","--offset=4096",joined)
        tree["compression_usage"](info,stats)
        assert (info["file_compression"]!="none")==compressed
        print(name,info)
