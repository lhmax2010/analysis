"""Construct a real reverse-order GPT and two compressed EROFS filesystems."""
from pathlib import Path
import runpy
import subprocess
import tempfile

script = Path(__file__).resolve().parents[2]/"scripts/r0012c/image-tree.py.txt"
lib = runpy.run_path(str(script))
with tempfile.TemporaryDirectory() as tmp:
    work = Path(tmp)
    cache = lib["cached_tree"]
    cache.__globals__["CACHE"] = work/"cache"
    disk = work/"disk"
    with disk.open("wb") as stream:
        stream.truncate(8*1024**2)
    subprocess.run(["sfdisk",disk],input=b'label: gpt\nstart=2048,size=2048,name="prd_t.img"\nstart=4096,size=2048,name="pltf_t.img"\n',stdout=subprocess.DEVNULL,check=True)
    for sector, name in [(2048,"product"), (4096,"platform")]:
        src = work/name
        src.mkdir()
        (src/name).write_bytes(b"\x7fELF"+name.encode())
        if name=="platform":
            (src/"prd").mkdir()
            (src/"prd"/"hidden").touch()
        image=work/(name+".ero")
        subprocess.run(["mkfs.erofs","-E48bit","-m4096","-zzstd" if name=="product" else "-zlz4",image,src],check=True,stdout=subprocess.DEVNULL)
        with disk.open("r+b") as stream:
            stream.seek(512*sector)
            stream.write(image.read_bytes())
    tree, info=cache(disk, work)
    assert sorted(x.name for x in (tree/"prd").iterdir())==["product"]
    assert info["elf_files"]==2 and info["elf_files_under_prd"]==1 and (tree/"platform").exists()
    assert (tree/"platform").read_bytes()==b"\x7fELFplatform"
    assert (tree/"prd/product").read_bytes()==b"\x7fELFproduct"
    assert info["partitions"]["prd"]["partition_start"]==2048*512
    with disk.open("r+b") as stream:
        stream.seek(2048*512+1024)
        stream.write(bytes(4))
    try:
        cache(disk, work)
    except ValueError as exc:
        assert "filesystem" in str(exc)
    else:
        raise AssertionError("accepted invalid product filesystem")
    print("PASS reversed named GPT, both EROFS trees, /prd overlay, ELF counts, corrupted product rejected")
