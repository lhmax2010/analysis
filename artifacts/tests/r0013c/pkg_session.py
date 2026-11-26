"""Run in a controlling PTY. Exercise real process-group cancellation and simulated admission."""
import json
import os
import runpy
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

PKG = Path(__file__).resolve().parents[2] / "scripts/r0013a/pkg.py.txt"
pkg = runpy.run_path(str(PKG))
run = pkg["run_owned"]
Stop = pkg["Stop"]
assert os.isatty(0)
child = """
import json, os, signal, time
from pathlib import Path
def finish(signum, frame):
    Path("terminated").write_text(str(os.getpid()))
    os._exit(0)
pid = os.fork()
if pid == 0:
    signal.signal(signal.SIGTERM, finish)
    Path("ready").touch()
    signal.pause()
else:
    while not Path("ready").exists(): time.sleep(.01)
    with open("/dev/tty", "rb", buffering=0) as tty:
        Path("ids").write_text(json.dumps([os.getpid(), os.getsid(0), os.getpgrp(), os.tcgetpgrp(tty.fileno()), pid]))
    os.waitpid(pid, 0)
"""
with tempfile.TemporaryDirectory(dir=os.environ["TMPDIR"]) as directory:
    work = Path(directory)
    checks = []
    def interrupt_after_ready():
        if checks:
            for _ in range(300):
                if (work / "ids").exists() and (work / "ids").stat().st_size:
                    break
                time.sleep(.01)
            else:
                raise AssertionError((work / "log").read_text() or "child failed to start")
            raise Stop("test cancellation")
        checks.append(True)
    with patch.dict(run.__globals__, capacity=interrupt_after_ready):
        try:
            run([sys.executable, "-Bc", child], work, work / "log", 20)
        except Stop as exc:
            assert str(exc) == "test cancellation"
        else:
            raise AssertionError("expected cancellation")
    pid, sid, pgid, foreground, grandchild = json.loads((work / "ids").read_text())
    assert sid == os.getsid(0) and foreground == os.tcgetpgrp(0)
    assert pgid == pid and pgid != os.getpgrp()
    for _ in range(300):
        if (work / "terminated").exists() and (work / "terminated").stat().st_size:
            break
        time.sleep(.01)
    assert int((work / "terminated").read_text()) == grandchild
    print("TTY same_session", sid, "foreground", foreground, "owned_group", pgid, "killpg_descendant_received_TERM")

admit = pkg["admit_lane"]
with patch("pathlib.Path.read_text", side_effect=["MemAvailable: 1048576 kB", "MemAvailable: 29360128 kB"]), \
     patch("shutil.disk_usage", return_value=SimpleNamespace(free=74 * 1024**3)), \
     patch.dict(admit.__globals__, capacity=lambda: None, CUTOFF=time.time()+7200), \
     patch("time.sleep") as sleep, patch.dict(admit.__globals__, check_credential=lambda *args: None):
    admit(Path("baseline"), 24, 12)
    sleep.assert_called_once_with(300)
with patch("pathlib.Path.read_text", return_value="MemAvailable: 29360128 kB"), \
     patch("shutil.disk_usage", return_value=SimpleNamespace(free=73 * 1024**3)), \
     patch.dict(admit.__globals__, capacity=lambda: None), patch("time.sleep") as sleep:
    try:
        admit(Path("treatment"), 24, 12)
    except Stop as exc:
        assert str(exc) == "disk admission requires 74 GiB"
    else:
        raise AssertionError("disk refusal expected")
    sleep.assert_not_called()
for command, reason in ((["p4", "login", "-s"], "p4-ticket"), (["sudo", "-n", "true"], "sudo")):
    with patch("subprocess.run", return_value=SimpleNamespace(returncode=1)):
        try:
            pkg["check_credential"](command, reason)
        except Stop as exc:
            assert str(exc) == reason
        else:
            raise AssertionError("expired credential accepted")
print("PASS admission RAM wait, disk stop, credential stops")
