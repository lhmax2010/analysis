"""Check Berkeley accounting on linked and split-debug ARM ELFs and signed package images."""
import gzip
from pathlib import Path
import os
import runpy
import struct
import subprocess
import tempfile
import zlib

m=runpy.run_path(str(Path(__file__).resolve().parents[2]/"scripts/r0012p/kernel-size.py.txt"))
with tempfile.TemporaryDirectory(dir=os.environ["TMPDIR"]) as tmp:
    w=Path(tmp)
    (w/"source.s").write_text("""
.text
.global _start
_start: bx lr
.section .rodata,"a"
.word 42
.section .init.text,"ax"
bx lr
.data
.word 0x12345678
.bss
.space 96
""")
    (w/"layout.ld").write_text("""SECTIONS {
       . = 0xc0008000; .text : { *(.text) } .rodata : { *(.rodata) }
       .notes : { *(.note.gnu.build-id) } .init.text : { *(.init.text) }
       .data : { *(.data) } .bss (NOLOAD) : { *(.bss) } }""")
    def call(*argv):
        subprocess.run(argv,cwd=w,check=True)
    call("llvm-mc","-triple=armv7-linux-gnueabi","-filetype=obj","source.s","-o","source.o")
    call(os.environ.get("LD_LLD","ld.lld"),"--build-id=sha1","-T","layout.ld","source.o","-o","vmlinux")
    call("llvm-objcopy","-O","binary","vmlinux","Image")
    call("llvm-objcopy","--only-keep-debug","vmlinux","vmlinux.debug")
    payload=(w/"Image").read_bytes()
    z=b"stub"+gzip.compress(payload)
    hdr=bytearray(64)
    hdr[:4]=bytes.fromhex("27051956")
    hdr[28:32]=bytes((5,2,2,0))
    struct.pack_into(">I",hdr,12,len(payload))
    struct.pack_into(">I",hdr,24,zlib.crc32(payload))
    struct.pack_into(">I",hdr,4,zlib.crc32(hdr))
    flat,bid=m["raw_kernel"](hdr+payload+b"trailer",z)
    assert flat==payload
    expected,info=m["measure"](w/"vmlinux",payload,bid,w,True)
    recovered,dbg=m["measure"](w/"vmlinux.debug",payload,bid,w)
    assert expected["Data"]==4 and expected["BSS"]==96 and expected["runtime RAM"]==108,expected
    assert dbg["raw_berkeley"]["Data"]==0 and dbg["raw_berkeley"]["BSS"]==100,dbg
    assert recovered==expected and recovered[".init.*"]==4,(recovered,expected)
    for ident,data in [(bid[:-2]+"ff",payload),(bid,payload+b"wrong")]:
        try:
            m["measure"](w/"vmlinux",data,ident,w,True)
        except ValueError:
            pass
        else:
            raise AssertionError("wrong identity/image accepted")
    print("ARM_ELF_MATCHED_SPLIT_AND_LINKED",expected)
    print("RAW_SPLIT",dbg["raw_berkeley"],"RESTORED",dbg["restored_sections"])
    print("WRONG_ID_OR_IMAGE_REJECTED; UIMAGE_TRAILER_EXCLUDED")
