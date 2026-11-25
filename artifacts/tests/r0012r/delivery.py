"""Exercise retained-object LTO delivery with a real ARM ELF, bitcode section and selected cfg."""
from pathlib import Path
import os
import runpy
import shutil
import subprocess
import tempfile

scripts=Path(__file__).resolve().parents[2]/"scripts"
audit=runpy.run_path(str(scripts/"r0012r/lto-delivery.py.txt"))["audit"]
opt=runpy.run_path(str(scripts/"r0012g/thumb-options.py.txt"))
with tempfile.TemporaryDirectory() as temp:
    work=Path(temp)
    for r,n in (("r0004","image_mode_scan"),("r0012e","thumb-map")):
        shutil.copy(scripts/r/(n+".py.txt"),work)
    lane=work/"default"
    root=lane/"GBS-ROOT/local/BUILD-ROOTS/scratch.armv7l.0"
    project=root/"home/abuild/rpmbuild/BUILD/pkg"
    obj="CMakeFiles/App.dir/main.c.o"
    (project/obj).parent.mkdir(parents=True)
    (project/obj).with_name("link.txt").touch()
    def cmd(*args, data=None):
        return subprocess.check_output(args,cwd=project,input=data)
    cmd("llvm-mc","-triple=thumbv7-linux-gnueabi","-filetype=obj","-o",obj,
        data=b".thumb\n.text\n.globl main\n.thumb_func\nmain: bx lr\n")
    cmd(os.environ["LD_LLD"],"--build-id","-e","main",obj,"-o","App")
    cmd("llvm-as","-o","bitcode",data=b'define i32 @main() #0 { ret i32 0 }\nattributes #0 = { "target-features"="+thumb-mode" }\n')
    cmd("llvm-objcopy","--add-section",".llvm.lto=bitcode",obj)
    (lane/"driver-argv.txt").write_text(f"PM12_DRIVER compile clang -flto -c main.c -o {obj}\nPM12_DRIVER link clang -flto {obj} -o App\n")
    (lane/"link-argv.txt").write_text(f"PM12_LINK_ARGV ld.lld {obj} -o App\n")
    build_id=cmd("readelf","-nW","App").decode().split("Build ID: ")[1].split()[0]
    metrics={"files":[{"text":2,"path":"/usr/bin/App","build_id":build_id,"debug_file":str(project/"App")}]}
    r=audit(work,lane,metrics)
    assert r["status"]=="PASS",r
    raw=project.parent/".pm12-driver/receipts/driver.123"
    raw.parent.mkdir(parents=True)
    raw.write_text(f"PM12_DRIVER compile clang -flto -c main.c -o {obj} HOOK=\nPM12_DRIVER link clang -flto @objects.rsp -o App HOOK=\n")
    (project/"objects.rsp").write_text(obj)
    (project/obj).with_name("link.txt").write_text("clang -flto @objects.rsp -o App\n")
    (lane/"driver-argv.txt").write_text("")
    assert audit(work,lane,metrics)["status"]=="PASS"
    raw.unlink()
    (lane/"driver-argv.txt").write_text(f"PM12_DRIVER link clang -flto {obj} -o App\n")
    assert audit(work,lane,metrics)["status"]=="REVIEW"
    cfg=root/"usr/bin/clang.cfg"
    cfg.parent.mkdir(parents=True)
    cfg.write_text("# tizen-force-options begin\n-mthumb -mimplicit-it=thumb\n# tizen-force-options end\n")
    alias=cfg.with_name("clang++.cfg"); alias.symlink_to(cfg.name)
    import hashlib
    row={"LOADED":["Configuration file: /usr/bin/clang++.cfg"],"CONFIG":["/usr/bin/clang.cfg "+hashlib.sha256(cfg.read_bytes()).hexdigest()],
         "ARGV":['"-triple" "thumbv7-tizen"'],"ARM_OVERRIDE":['"-triple" "armv7-tizen"'],"BUILT":["c t","S t"]}
    rows={name:row for name in opt["DRIVERS"]}
    assert opt["config_gate"](rows,True,lane)==[],opt["config_gate"](rows,True,lane)
    cfg.write_text("-mthumb\n")
    assert len(opt["config_gate"](rows,True,lane))==len(rows)
    print("PASS bitcode function mode, link and compile coverage, final Thumb mappings, selected alias/hash, stale policy rejected")
