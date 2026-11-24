"""Exercise the driver preflight, cfg lookup and next-morning log reader."""
import os
from pathlib import Path
import runpy
import shlex
import subprocess
import tempfile

scripts = Path(__file__).resolve().parents[2]/"scripts"
code = (scripts/"r0012g/driver-config.sh.txt").read_text()
reader = runpy.run_path(str(scripts/"r0012g/thumb-options.py.txt"))

with tempfile.TemporaryDirectory(dir=os.environ["TMPDIR"]) as temp:
    work = Path(temp)
    real = work/"usr/bin"
    real.mkdir(parents=True)
    cfg = real/"target-clang.cfg"
    cfg.write_text("-target armv7l-tizen-linux-gnueabi\n")
    cfg.chmod(0o640)
    alias = real/"alias.cfg"
    alias.symlink_to(cfg.name)
    (real/"outer.cfg").symlink_to(alias.name)
    # Substitute fixture directories for the two fixed target bin directories.
    local = code.replace("for dir in /usr/bin /emul/usr/bin",
                         "for dir in "+shlex.quote(str(real))).replace("@SCOPED@", "yes")
    drivers = ["clang","clang++","armv7l-tizen-linux-gnueabi-clang","armv7l-tizen-linux-gnueabi-clang++",
               "cc","c++","gcc","g++"]
    for name in drivers:
        path = real/name
        path.write_text('#!/bin/sh\ncase "$*" in *-###*) echo "Configuration file: $CFG" >&2; echo \'"-cc1"\' >&2;; *) exit 1;; esac\n')
        path.chmod(0o755)
    env = {**os.environ,"PATH":str(real)+":"+os.environ["PATH"]}
    for case in ("success","broken","missing"):
        folder = work/case
        folder.mkdir()
        target = real/"outer.cfg" if case=="success" else real/"absent.cfg"
        testenv = {**env,"CFG":str(target)}
        if case=="missing": testenv["PATH"]=str(folder)
        proc = subprocess.run(["/bin/sh","-e"],input=local,text=True,cwd=folder,env=testenv,
                              stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if case=="success":
            assert proc.returncode==0, proc.stdout
            assert alias.is_symlink() and cfg.stat().st_mode & 0o777 == 0o640
            assert cfg.read_text().count("-mthumb -mimplicit-it=thumb")==1
        else:
            assert proc.returncode and ("PM_CFG_RESOLVE_FAILED" if case=="broken" else "PM_BUILD_MISSING_TOOL") in proc.stdout
    lane=work/"default"
    lane.mkdir()
    (lane/"gbs.log").write_text("""PM_CFG clang LOADED Configuration file: /usr/bin/clang.cfg
PM_CFG clang OPTION -mthumb
PM_CFG clang EXE /usr/bin/clang
[  4s] cd subdir && /bin/cc -O2 -c a.c
[  5s] c++ -c b.cpp
[  6s] ccache gcc -c z.S
[  7s] PM_GCC_ARGV /usr/bin/g++ -c test.cpp
[  8s] grep cc config.log
""")
    data=reader["summarize"](work,True)["default"]
    assert data["F6_loaded_missing_marked_options"]==["clang"]
    assert [line["driver"] for line in data["gcc_family_compile_lines"]]==["/bin/cc","c++","gcc","/usr/bin/g++"]
    assert reader["guest_target"](work,"/usr/bin/outer.cfg")=="/usr/bin/target-clang.cfg"
    (real/"absolute.cfg").symlink_to("/usr/bin/outer.cfg")
    assert reader["guest_target"](work,"/usr/bin/absolute.cfg")=="/usr/bin/target-clang.cfg"
print("PASS cfg chain, exact mode, idempotent edit across driver names, loud failure and missing-tool gate")
print("PASS F6 classification, guest-root absolute links and four GCC driver spellings with original argv")
