"""Run the RPM-expanded bench build body with only tools listed in an ARM RPM inventory.

Input TSV is NEVRA<TAB>absolute-file, as obtained with rpm -q --qf in the
builder. By default provider releases must occur in the retained Official GBS
installation log. --compare-layout allows a separately labelled older root.
No compiler or linker binary runs in this local fixture.
"""
import argparse
import os
from pathlib import Path
import re
import runpy
import subprocess
import tempfile


ART = Path(__file__).resolve().parents[2]
builder = runpy.run_path(str(ART/"scripts/r0012c/gbs-board-bench.py.txt"))
tools = builder["BUILD_TOOLS"]


def check(work, inventory, alternate):
    installed = (ART/"evidence/native-run-r0011e-step5-bench-fail-20261124.txt").read_text()
    owners = {}
    for line in inventory.read_text().splitlines():
        nevra, path = line.split("\t")
        name = Path(path).name
        if name not in tools or path not in ("/bin/"+name, "/usr/bin/"+name):
            continue
        if not re.search(r"installing "+re.escape(nevra.removesuffix(".armv7l"))+r"\s*$", installed, re.M) and not alternate:
            raise ValueError("release missing from Official installed-package transcript: "+nevra)
        owners[name] = (nevra, path)
    assert set(owners) == set(tools), set(tools)-owners.keys()
    spec = work/"pkg.spec"
    spec.write_text(builder["SPEC"])
    expanded = subprocess.check_output(["rpmspec","--define","_topdir "+str(work),"-P",spec],text=True)
    body = "set -eu\n" + expanded.split("\nset -eu\n",1)[1].split("\n%install",1)[0]
    fast_body = builder["SPEC"].split("\n%build\n",1)[1].split("\n%install\n",1)[0].replace("%%","%")
    assert body.strip() == fast_body.strip()
    assert "realpath" not in body and "readlink" not in body
    builder["restricted_build_fixture"](work,owners,ART/"scripts/r0010/mlgo-tv-microbench.c.txt",body)
    print("PACKAGE_SET", "ALTERNATE_ARM_GBS_RELEASES" if alternate else "OFFICIAL_INSTALL_LOG_MATCH")
    for name,(nevra,path) in sorted(owners.items()): print("FIXTURE_TOOL",name,nevra,path)
    print("PASS exact RPM-expanded %build; restricted PATH; physical libc parent, linker, GCC CRT and libc lookup, static proof")
    print("PASS each of seven missing commands rejected before compiler invocation; target tools replayed")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rpm_files",type=Path)
    parser.add_argument("--compare-layout",action="store_true")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(dir=os.environ["TMPDIR"]) as directory:
        check(Path(directory),args.rpm_files,args.compare_layout)
