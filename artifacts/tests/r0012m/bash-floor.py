"""Run generated build-root shell with a real Bash 3.2.57. External target tools are fixtures."""
import argparse
import ast
import os
from pathlib import Path
import re
import runpy
import shlex
import subprocess
import tempfile
from unittest.mock import patch

ART = Path(__file__).resolve().parents[2]
S = ART/"scripts"
def read(path):
    return (S/path).read_text()
def load(path):
    return runpy.run_path(str(S/path))

# Apply this conservative lint to the generated shell as well as running the floor interpreter.
rules = {
    "new declaration": r"\b(?:declare|typeset|local)\s+-[a-zA-Z]*[An]",
    "new builtin": r"\b(?:mapfile|readarray|coproc)\b",
    "case conversion": r"\$\{\w+(?:,,|\^\^|,|\^)[^}]*\}",
    "variable test": r"\[\[[^\n]*?(?:^|\s)-v\s",
    "negative subscript": r"\w+\[\s*-\s*\d+\s*\]",
    "new control operator": r";;&|;&|\|&",
    "globstar": r"\bglobstar\b",
    "time printf": r"(?<!%)%\([^)]*\)T",
    "BASHPID": r"\$\{?BASHPID\b",
}
def scan(name, body):
    for feature,pattern in rules.items():
        if re.search(pattern,body): raise ValueError(f"{name}: {feature}")
    guarded=re.sub(r'\$\{(\w+)\[@\]\+"\$\{\1\[@\]\}"\}', '', body)
    if re.search(r'\$\{\w+\[@\]\}',guarded): raise ValueError(f"{name}: unguarded array")

def main(shell, base):
    version=subprocess.check_output([shell,"-c",'echo "$BASH_VERSION"'],text=True).strip()
    assert version.startswith("3.2.57"), version
    print("SHELL",version)
    bad=subprocess.run([shell,"-uc",'x=(); echo "${x[@]}"'],capture_output=True)
    assert bad.returncode and b"unbound variable" in bad.stderr
    for sample in ('declare -A t','local -n t','mapfile x','readarray x','${v,,}','${v^^}',
                   '[[ -v x ]]','${a[-1]}',';&',';;&','|&','coproc x','shopt -s globstar',
                   "printf '%(x)T'","$BASHPID",'echo "${x[@]}"'):
        try: scan("negative",sample)
        except ValueError: continue
        raise AssertionError(sample)
    for step in ("bench","driver","check","kernel","t7"): (base/step).mkdir()
    binpath=base/"tools"; binpath.mkdir()
    def stub(name,code):
        path=binpath/name
        path.write_text("#!"+str(shell)+"\n"+code+"\n")
        path.chmod(0o755)
    fake_driver=r'''case " $* " in
        *" -### "*) echo '"-cc1"' >&2; exit 0 ;;
    esac
    if [ -n "${ARG_LOG:-}" ]; then printf '%s\0' "$@" >"$ARG_LOG"; fi
    prev=""
    for arg do
        if [ "$prev" = -o ]; then printf '#!/bin/sh\nexit 0\n' >"$arg"; chmod +x "$arg"; fi
        prev=$arg
    done'''
    clang="armv7l-tizen-linux-gnueabi-clang"
    for name in ("clang","clang++",clang,clang+"++","gcc","g++","cc","c++","ld.lld"):
        stub(name,fake_driver)
    env=dict(os.environ,PATH=str(binpath)+":"+os.environ["PATH"],TMPDIR=str(base))
    def run(name,code,folder,extra=None):
        scan(name,code)
        subprocess.run([shell,"-n"],input=code,text=True,check=True)
        out=subprocess.run([shell,"-e"],cwd=folder,input=code,text=True,env={**env,**(extra or {})},
                           stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if out.returncode: raise ValueError(name+"\n"+out.stdout[-2000:])
        print("PASS",name)
        return out.stdout

    dev=load("r0012/development.py.txt"); work=base/"driver"
    def generate(path,name,treatments):
        folder=work/name; folder.mkdir()
        body=read(path)
        setup=dev["hook_source"](body,treatments)
        setup=setup.replace('export PATH="$pm12_bin:$PATH"',dev["GCC_TRACE"]+'export PATH="$pm12_bin:$PATH"')
        run(name+" setup",setup.replace("%%","%"),folder)
        return folder/".pm12-driver"
    for name,flags in (("phase-empty",dev["EMPTY"]),("phase-edited",dict(compile=["-Os"],link=["-Wl,-z,text"],plugin=["-flto"]))):
        wrappers=generate("r0012/phase-driver.sh.txt",name,flags)
        for args in (["-c","file.c"],["file.o","-o","final"],["-flto","file.c","-o","final"],["-Wl,--version"]):
            subprocess.run([shell,wrappers/clang,*args],cwd=work,env=env,capture_output=True,check=True)
    wrappers=generate("r0012m/observe-driver.sh.txt","observe",dev["EMPTY"])
    receipts=work/"receipts"; receipts.mkdir()
    for args in (["-c","testCXXCompiler.cxx","-DSTRING=a b","-o","cmTC_a.o"],["cmTC_a.o","-o","cmTC_a"]):
        dest=work/"argv"
        subprocess.run([shell,wrappers/(clang+"++"),*args],cwd=work,env=dict(env,PM12_RECEIPTS=str(receipts),ARG_LOG=str(dest)),check=True)
        assert dest.read_bytes()==b''.join(os.fsencode(a)+b'\0' for a in args)
    log=work/"gbs.log";log.write_bytes(b''.join(p.read_bytes() for p in receipts.iterdir()))
    assert set(dev["smoke_argv"](log))=={"compile","link"},log.read_text()
    subprocess.run([shell,wrappers/"cc","-c","file.c"],env=dict(env,PM12_RECEIPTS=str(receipts)),check=True)
    # Existing successful cfg-link/permission fixture, executed with this shell.
    orig=subprocess.run
    def use_floor(cmd,*args,**kw):
        if cmd[0] in ("sh","/bin/sh"): cmd=[shell,*cmd[1:]]
        return orig(cmd,*args,**kw)
    cfg=read("r0012g/driver-config.sh.txt");scan("cfg",cfg)
    bench=load("r0012c/gbs-board-bench.py.txt")
    with patch.object(subprocess,"run",use_floor):
        runpy.run_path(str(ART/"tests/r0012i/check-config.py"))
        fixture=runpy.run_path(str(ART/"tests/r0012h/bench-fixture.py"))
        fixture["check"](base/"bench",ART/"tests/r0012h/official-owner-readback.tsv",False)
    spec=bench["SPEC"]
    for section,end in [("prep","build"),("build","install"),("install","files")]:
        body=spec.split("\n%"+section+"\n",1)[1].split("\n%"+end,1)[0].replace("%%","%")
        scan("bench "+section,body)
    # Also execute %prep's RPM ownership/inode checks in a simulated installed tree.
    b=base/"bench"
    paths=b/".pm-bench-bin"
    tool_rows="".join("fixture\t"+str(paths/t)+"\n" for t in bench["BUILD_TOOLS"])
    # Separate prep cwd and owner fixture to keep the earlier missing-tool cases intact.
    prep=b/"prep";prep.mkdir()
    stub("rpm",'printf %s '+shlex.quote(tool_rows))
    for tool in bench["BUILD_TOOLS"]:
        if not (binpath/tool).exists(): (binpath/tool).symlink_to(paths/tool)
    prep_body=spec.split("\n%prep\n")[1].split("\n%build")[0].replace("%%","%").replace("%{SOURCE0}",str(b/"bench.c"))
    # Deliver a file list matching the command-visible fake path.
    prep_body=prep_body.replace('"/usr/bin/"tool','"'+str(binpath)+'/"tool')
    stub("rpm","printf %s "+shlex.quote(tool_rows.replace(str(paths),str(binpath))))
    run("Step5 prep",prep_body,prep)
    run("Step5 install",spec.split("\n%install\n")[1].split("\n%files")[0].replace("%{buildroot}",str(b/"buildroot")),b)
    # Restore real host tools for readelf/hash utilities used by later fixtures.
    for tool in ("readelf","ld","awk","sha256sum","tail"):
        (binpath/tool).unlink(missing_ok=True)
    check=base/"check"; (check/"empty").mkdir()
    run("thumb-check",read("r0012e/thumb-check.sh.txt").replace("%{buildroot}",str(check/"empty")),check)

    k=base/"kernel";specpath=k/"spec"
    specpath.write_text("%build\n"+load("r0008a/gbs-mlgo-t7.py.txt")["INSTRUMENT"])
    subprocess.run(["patch","--fuzz=0","--batch",specpath,ART/"patches/kernel/perf-machine-outliner.spec.patch"],check=True,stdout=subprocess.DEVNULL)
    kernel=specpath.read_text().split("%build\n")[1].replace("%{_builddir}",str(k)).replace("%%","%").replace("@LANE@","K1")
    run("matrix spec and inventory",kernel,k)
    for wrapper,var in [("clang","PM_REAL_CLANG"),("make","PM_REAL_MAKE"),("ld.lld","PM_REAL_LLD")]:
        body=(k/".pm0012f-tools"/wrapper).read_text()
        run("matrix "+wrapper,body,k,{var:"/bin/true","PM_KERNEL_LANE":"K1"})
    with patch.object(subprocess,"run",use_floor):
        for round_ in ("r0012k","r0012l"):
            runpy.run_path(str(ART/"tests"/round_/"check.py"))
    probe=load("r0009/thumb-force-pilot.py.txt")["PROBE"].replace("%%","%")
    run("startup probe",probe,work)
    module=ast.parse(read("r0012e/kernel-modules.py.txt"))
    expr=next(n.value for n in ast.walk(module) if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=="check")
    stub("rpm","echo fixture")
    run("module header guard",eval(compile(ast.Expression(expr),"kernel-modules","eval"),{"sha":"fixture"}).replace("%%","%"),k)
    stub("ld","echo 'GNU ld'"); (base/"t7/cases.tsv").touch()
    run("T7 probe",read("r0012/gbs-t7-link.sh.txt"),base/"t7")
    print("PASS real Bash 3.2.57, static rejection corpus and cmTC exec argv")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("bash32",type=Path)
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(dir=os.environ["TMPDIR"]) as temp:
        main(str(args.bash32.resolve()),Path(temp))
