"""Local hash/range and directory index fixtures. Run with TMPDIR inside the workspace."""
import csv
import gzip
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
from unittest.mock import patch

artifacts = Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory() as tmp:
    work = Path(tmp)
    for r, name in (("r0012p", "kernel-size"), ("r0012q", "native-readback")):
        shutil.copy(artifacts / "scripts" / r / (name + ".py.txt"), work)
    mod = runpy.run_path(str(work / "native-readback.py.txt"))
    left = mod["P"]["NOTE"] + bytes(20) + b"Linux version test host 001\n\0hello"
    right = left.replace(bytes(20) + b"Linux", bytes(range(20)) + b"Linux").replace(b"001", b"002")
    sections = [(0, 36, ".notes"), (36, len(left), ".rodata")]
    outfile = work / "ranges.tsv.gz"
    check = mod["diff_ranges"]
    assert check(left, left, sections, outfile)["ranges"] == 0
    assert check(left, right, sections, outfile)["other_bytes"] == 0
    result = check(left, right[:-1] + b"axy", sections, outfile)
    with gzip.open(outfile, "rt") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    assert sum(int(r["end_exclusive_hex"], 16) - int(r["start_hex"], 16) for r in rows) == result["different_bytes"]
    assert result["other_bytes"] == 3
    assert check(left, right, [(0,len(left),".text")], outfile)["other_bytes"] == 19
    flat = work / "flat"
    subprocess.run(["objcopy","-O","binary","-R",".comment","-R",".note","-S","/bin/true",flat], check=True)
    assert any(name==".text" for _,_,name in mod["sections"](Path("/bin/true"),flat.read_bytes()))
    root = "http://test.invalid/pub/release/"
    debug = root + "repos/product/armv7l/debug/"
    rpm = "tztv-kernel-perf-debuginfo-1-1.armv7l.rpm"
    def index(cmd, **kwargs):
        ok = cmd[-1] == debug
        Path(cmd[cmd.index("-o")+1]).write_text(f'<a href="{rpm}">rpm</a><a href="http://away.invalid/bad/">away</a>')
        return subprocess.CompletedProcess(cmd, 0, "200" if ok else "403")
    with patch("subprocess.run", side_effect=index), patch.dict(mod["P"], metadata_rows=lambda u,f: []):
        assert mod["debug_dirs"](root,work) == {debug+rpm}
print("PASS identical / note / banner / code / tail / range conservation / LMA / publication listing")
