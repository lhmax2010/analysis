"""Build a tiny ARM ELF with critical and name-only LR_STACK callers. Never execute it."""
import csv
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[1]


class SideEffects(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name).resolve()
        self.out = root
        self.tree = root / "K1"
        self.tree.mkdir()
        obj = self.tree / "fixture.o"
        elf = self.tree / "vmlinux"
        subprocess.run(["llvm-mc", "-triple=armv7-linux-gnueabi", "-filetype=obj",
                        TESTS / "stack.s", "-o", obj], check=True)
        subprocess.run([os.environ.get("ARM_LD", "ld.lld"), "-m", "armelf_linux_eabi",
                        "-e", "__entry_fixture", obj, "-o", elf], check=True)
        (self.tree / "System.map").write_bytes(subprocess.check_output(["nm", "-n", elf]))
        (self.tree / ".fixture.o.cmd").write_text("cmd := clang -c fixture.s\n")
        shutil.copyfile(obj, self.tree / "fixture.ko")
        (self.tree / "modules.order").write_text("fixture.ko\n")
        (self.tree / "Module.symvers").write_text("0x00000001 fixture vmlinux\n")
        (root / "kernel-matrix.json").write_text('{"K1":{}}')
        source = root / "arch/arm/kernel/module.c"
        source.parent.mkdir(parents=True)
        source.write_text("case R_ARM_CALL:\ncase R_ARM_JUMP24:\n")
        (root / "outline-metrics.py.txt").symlink_to(SCRIPTS / "r0012n/outline-metrics.py.txt")
        env = runpy.run_path(str(SCRIPTS / "r0013q/effects.py.txt"))
        self.lane = env["lane"]
        self.g = self.lane.__globals__
        self.g.update(OUT=root, TEMP=root, JOB=root, SOURCE=root,
                      SCAN=runpy.run_path(str(SCRIPTS / "r0004/image_mode_scan.py.txt"))["secs_of"],
                      AUDIT=runpy.run_path(str(SCRIPTS / "r0012f/kernel-audit.py.txt")))
        self.metrics = {"helpers": 1, "sha256": env["sha"](elf)}

    def evaluate(self):
        return self.lane("K1", self.tree, self.tree, [self.tree], 1, {}, self.metrics)

    def test_all_checks_and_error_isolation(self):
        normal = self.evaluate()
        self.assertEqual(set(normal), {f"S{i}" for i in range(1, 16)})
        for key, (verdict, detail) in normal.items():
            self.assertIsInstance(detail, dict, (key, verdict, detail))
        self.assertEqual(list(self.out.glob("*-error.txt")), [])
        self.assertEqual(normal["S2"][0], "FAIL")
        self.assertEqual(normal["S2"][1]["critical_stack_sites"], 2)
        self.assertEqual(normal["S11"][1]["system_state_instructions"], 1)
        self.assertEqual(normal["S12"][1]["covered"], 1)
        with (self.out / "K1-critical-stack.tsv").open() as f:
            paths = {row["caller"]: json.loads(row["direct_path"])
                     for row in csv.DictReader(f, delimiter="\t")}
        self.assertEqual([v["symbol"] for v in paths["fixture_caller"]],
                         ["__entry_fixture", "fixture_caller"])
        self.assertEqual(paths["irq_unreachable"], [])
        with patch.dict(self.g, route=unavailable_route):
            broken = self.evaluate()
        self.assertEqual(broken["S2"], ("REVIEW", "NameError: injected missing route"))
        self.assertEqual({k for k in normal if normal[k] != broken[k]}, {"S2"})
        self.assertEqual([p.name for p in self.out.glob("*-error.txt")], ["K1-S2-error.txt"])


def unavailable_route(*args):
    raise NameError("injected missing route")


if __name__ == "__main__":
    unittest.main()
