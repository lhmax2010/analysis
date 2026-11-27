"""Exercise the successful GBS packaging layout using an ARM ELF and a real RPM."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[2]
K = runpy.run_path(str(SCRIPTS/"r0013jk/kernel.py.txt"))
envelope = runpy.run_path(str(SCRIPTS/"r0013s/tests/verify.py"))["image"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class OutputDirectory(unittest.TestCase):
    def test_cleaned_kbuild(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            out = t/"run"
            out.mkdir()
            (out/"image_mode_scan.py.txt").symlink_to(SCRIPTS/"r0004/image_mode_scan.py.txt")
            work = t/"retained"
            root = work/"GBS-ROOT"
            build = root/"scratch/rpmbuild/BUILD/tztv-kernel-1"
            image = build/"KANTSU2E/image/perf"
            image.mkdir(parents=True)
            elf = image/"vmlinux"
            asm = t/"fixture.s"
            asm.write_text(".text\n.arm\n.global _start,OUTLINED_FUNCTION_0\n_start: bx lr\nOUTLINED_FUNCTION_0: bx lr\n")
            def run(*args):
                subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            run("llvm-mc","-triple=armv7-linux-gnueabi","-filetype=obj",asm,"-o",t/"input.o")
            run(os.environ.get("ARM_LD","ld.lld"),"-m","armelf_linux_eabi","--build-id=sha1",
                "-e","_start",t/"input.o","-o",elf)
            run("llvm-objcopy","-O","binary","-R",".comment","-R",".note","-S",elf,t/"Image")
            payload = (t/"Image").read_bytes()
            identity = K["kernel_id"](payload)
            z = image/"zImage"
            z.write_bytes(b"packed perf")
            cfg = t/"pm0012-kernel.dkyJ0S/jobs/kernel-thumb/K0/generated.config"
            cfg.parent.mkdir(parents=True)
            cfg.write_bytes(b"CONFIG_FIXTURE=y\n")
            spec = b"pinned fixture spec"
            defconfig = work/"vdlinux"/K["DEFCONFIG"]
            defconfig.parent.mkdir(parents=True)
            defconfig.write_bytes(b"CONFIG_FIXTURE=y\n")
            other_cfg = build/"separate/.config"
            other_cfg.parent.mkdir()
            shutil.copy(cfg,other_cfg)
            # Isolate T.parent/usb inside this fixture as well.
            temp = t/"workspace/temp"
            temp.mkdir(parents=True)
            official = temp.parent/"usb/37777148/updateSU2E/uImage"
            official.parent.mkdir(parents=True)
            official.write_bytes(envelope(b"reference"))
            reference = temp/cfg.relative_to(t)
            reference.parent.mkdir(parents=True)
            shutil.copy(cfg,reference)
            top = t/"rpm"
            for folder in ("SPECS","SOURCES","BUILD","BUILDROOT","RPMS","SRPMS","rpmdb"):
                (top/folder).mkdir(parents=True)
            sources = top/"SOURCES"
            (sources/"uImage").write_bytes(envelope(payload))
            shutil.copy(z,sources/"zImage")
            (sources/"config.gz").write_bytes(gzip.compress(cfg.read_bytes()))
            package = top/"SPECS/fixture.spec"
            package.write_text("""%global debug_package %{nil}
Name: tztv-kernel-perf
Version: 1
Release: 1
License: MIT
Summary: Fixture
Source0: uImage
Source1: zImage
Source2: config.gz
%description
Fixture
%install
mkdir -p %{buildroot}/perf
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{buildroot}/perf/
%files
/perf/*
""")
            run("rpmbuild","--dbpath",top/"rpmdb","--define","_topdir "+str(top),"--define","_tmppath "+str(t),
                "--define","_binary_filedigest_algorithm 8","--nodeps","-bb",package)
            rpm = next((top/"RPMS").rglob("*.rpm"))
            log = work/"gbs.log"
            clang = "clang -D__KERNEL__ -moutline -c -o kernel/core.o kernel/core.c"
            module = "clang -D__KERNEL__ -DMODULE -moutline -c -o drivers/a.o drivers/a.c"
            lines = ["+ env LLVM=1 ./BUILD.sh KANTSU2E perf",clang,module,
                     "make[1]: Entering directory '/v/SERET-UL/build/KANTSU2E/debug/vdlinux'",
                     "gcc -c -o mm/a.o mm/a.c"]
            log.write_text("\n".join(lines)+"\n")
            g = SimpleNamespace(sha=digest,CONFIG_SHA=digest(defconfig),kernel_rpms=lambda root:[rpm])
            expected=dict(text=8,helpers=1,Image=len(payload),zImage=z.stat().st_size)
            fn = K["post_build"]
            with patch.dict(fn.__globals__,W=out,T=temp,K1=expected,K0_CONFIG=digest(cfg),
                            RETAINED_SPEC=K["sha"](spec),OFFICIAL_UIMAGE=digest(official)), patch.dict(os.environ,PM_STATIC_SHA="fixture"):
                fn(work,spec,g,None)
                receipt = json.loads((out/"build.json").read_bytes())
                self.assertEqual(receipt["config_proof"]["method"],"BUILD_CONFIG_SHA256")
                self.assertEqual(receipt["sizes"],expected)
                self.assertEqual(receipt["elf_build_id"],identity)
                self.assertEqual(receipt["elf_image_sha256"],K["sha"](payload))
                self.assertFalse((image/".config").exists())
                other_cfg.unlink()
                fn(work,spec,g,None)
                self.assertEqual(json.loads((out/"build.json").read_bytes())["config_proof"]["method"],"RPM_CONFIG_SHA256")
                prove = K["perf_config"]
                base_args=(work,image,payload,identity,rpm,{},digest(cfg),spec,g)
                self.assertEqual(prove(*base_args)["method"],"SPEC_PREFLIGHT_IDENTICAL_DEFCONFIG")
                marker=b"IKCFG_ST"+gzip.compress(cfg.read_bytes())+b"IKCFG_ED"
                self.assertEqual(prove(work,image,payload+marker,*base_args[3:])["method"],"IKCONFIG_SHA256")
                log.write_text("\n".join([lines[0],clang,*lines[3:],module]))
                with self.assertRaisesRegex(ValueError,"perf-scoped"):
                    fn(work,spec,g,None)
                log.write_text("\n".join([lines[0],*lines[3:]]))
                fn(work,spec,g,None)
                self.assertEqual(json.loads((out/"build.json").read_bytes())["perf_argv_method"],
                                 "PM_ACCEPT argv-proof-by-effect")
                log.write_text("\n".join([lines[0],clang.replace("-moutline","-mno-outline"),module,*lines[3:]]))
                with self.assertRaisesRegex(ValueError,"perf-scoped"):
                    fn(work,spec,g,None)
                with patch("shutil.which",return_value=None):
                    self.assertEqual(K["packaged_perf_sizes"](elf,payload,len(b"packed perf"))[1],expected)
                with self.assertRaisesRegex(ValueError,"differs|mismatch"):
                    K["packaged_perf_sizes"](elf,payload[:-1]+bytes([payload[-1]^1]),len(b"packed perf"))


if __name__ == "__main__":
    unittest.main()
