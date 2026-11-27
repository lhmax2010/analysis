import os
import runpy
import struct
import tempfile
import unittest
import zlib
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[2]
K = runpy.run_path(str(BASE / "r0013jk/kernel.py.txt"))
B = runpy.run_path(str(BASE / "r0013s/board.py.txt"))


def image(payload=b"image", trailer=b"x" * 260):
    h = bytearray(64)
    struct.pack_into(">7I", h, 0, 0x27051956, 0, 0, len(payload), 0, 0, zlib.crc32(payload))
    h[28:32] = bytes((5, 2, 2, 0))
    struct.pack_into(">I", h, 4, zlib.crc32(h))
    return bytes(h) + payload + trailer


class Verify(unittest.TestCase):
    def test_envelope(self):
        ref = image(b"official")
        fn = K["compare_uimage"]
        with patch.dict(fn.__globals__, OFFICIAL_UIMAGE=K["sha"](ref)):
            payload, head = fn(image(), ref)
            self.assertEqual((payload, head["trailer_bytes"]), (b"image", 260))
            for corrupt in (image()[:65], image()[:-1], image()[:64] + b"X" + image()[65:],
                            image()[:4] + bytes(4) + image()[8:]):
                with self.assertRaises(ValueError):
                    fn(corrupt, ref)
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                fn(image(), ref[:-1])

    def test_registers(self):
        for op, reg, expect in (("mrc", "3", "TPIDRURO read"), ("mrcne", "4", "TPIDRPRW read"),
                                ("mcr", "3", "owner review")):
            for args in (f"p15, #0x0, r6, c13, c0, #0x{reg}", f"p15, 0, r6, cr13, cr0, {reg}"):
                self.assertEqual(B["classify"](op, args), expect)
        self.assertEqual(B["classify"]("mrc", "p15, 0, pc, c13, c0, 3"), "owner review")

    def test_residual(self):
        checks = {"S1": ["FAIL", {"critical": 0}], "S2": ["FAIL", {
            "helper_chain_extra_save_lower_bound_bytes": 8, "stack_budget": 8192}],
            "S4": ["PASS"], "S9": ["PASS"], "S11": ["REVIEW", {"system_state_instructions": 119}]}
        rows = [dict(pc=hex(4*i), op="mrc", operand="p15, #0x0, r6, c13, c0, #0x3")
                for i in range(119)]
        for op, passed in (("mrceq", True), ("mcrne", False), ("swine", False)):
            rows[-1]["op"] = op
            self.assertEqual(B["adjudicate"]("K1", rows, checks)["PM_conditions_met"], passed)
        with self.assertRaises(ValueError):
            B["adjudicate"]("K1", rows[:-1], checks)

    def test_postcheck_and_receipt(self):
        fn = K["post_build"]
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            work, out = t/"pm0013jk-build.jEMVH7", t/"pm0013jk-build.fixture"
            out.mkdir()
            root = work/"GBS-ROOT"
            tree = root/"x/rpmbuild/BUILD/perf"
            z = tree/"arch/arm/boot/zImage"
            z.parent.mkdir(parents=True)
            z.write_bytes(b"compressed")
            cfg = t/"pm0012-kernel.dkyJ0S/jobs/kernel-thumb/K0/generated.config"
            cfg.parent.mkdir(parents=True)
            cfg.write_text("config")
            (tree/".config").write_bytes(cfg.read_bytes())
            bid = "0123456789abcdef" * 2 + "12345678"
            (tree/"vmlinux").write_bytes(b"\x7fELF\x01\x01" + bytes(10) + struct.pack("<HH", 2, 40))
            def cmd_file(path, text):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
            cmd_file(tree/"drivers/.example.o.cmd","cmd_x := clang -DMODULE -moutline -c d.c")
            cmd_file(tree/"kernel/.sched.o.cmd", "cmd_x := clang -moutline -c s.c")
            (work/"gbs.log").write_text("Entering directory 'SERET-UL'\ngcc -c s.c\n")
            rpm = root/"local/repos/tztv-kernel-perf.rpm"
            rpm.parent.mkdir(parents=True)
            rpm.write_text("fixture RPM")
            (out/"image_mode_scan.py.txt").write_text("def secs_of(x): return [('.text',[0]*5+[12]),('.symtab',[])]")
            g = SimpleNamespace(kernel_rpms=lambda root: [rpm], sha=B["digest"])
            rpm_zhash = B["digest"](z)
            def read(*args):
                if args[0:2] == ("nm","-n"):
                    return b"00000000 T OUTLINED_FUNCTION_1\n"
                if args[0] == "readelf":
                    return (" Build ID: "+bid).encode()
                if "--dump" in args:
                    return f"/perf/zImage 10 0 {rpm_zhash}".encode()
                return b"tztv-kernel-perf"
            payload = struct.pack("<III",4,20,3)+b"GNU\x00"+bytes.fromhex(bid)
            changes = dict(W=out,T=t,read=read,rpm_boot=lambda *args: (payload,10,{}),
                           K1=dict(text=12,helpers=1,Image=len(payload),zImage=10))
            with patch.dict(fn.__globals__,changes), patch.dict(os.environ,PM_STATIC_SHA="static"):
                fn(work,b"spec",g,None)
                path = out/"build.json"
                with patch.dict(os.environ,PM_BUILD=str(path),PM_BUILD_SHA=B["digest"](path)):
                    r = K["receipt"]("PM_BUILD","build.json","pm0013jk-build.")
                    self.assertEqual(r["status"],"PASS")
                    self.assertEqual(r["script"],B["digest"](BASE/"r0013jk/kernel.py.txt"))
                    self.assertEqual(r["elf_build_id"],bid)
                (tree/"vmlinux").unlink()
                fn(work,b"spec",g,None)
                import json
                r=json.loads(path.read_bytes())
                self.assertIsNone(r["elf_build_id"])
                self.assertEqual(r["image_build_id"],bid)
                self.assertEqual(r["sizes"]["helpers"],"NOT_MEASURED_NO_ELF")
                self.assertEqual(r["sizes"]["text"],"NOT_MEASURED_NO_ELF")
                with patch.dict(fn.__globals__["K1"], Image=len(payload)+1), self.assertRaisesRegex(ValueError,"exactly"):
                    fn(work,b"spec",g,None)
                with patch.dict(fn.__globals__["K1"], zImage=11), self.assertRaisesRegex(ValueError,"zImage outside"):
                    fn(work,b"spec",g,None)
                (tree/".config").write_text("CONFIG_TEST=y\n")
                with self.assertRaisesRegex(ValueError,"no single perf tree"):
                    fn(work,b"spec",g,None)
                diag=json.loads((out/"tree-candidates.json").read_bytes())[0]
                self.assertEqual(diag["symbol_diff_K0_to_candidate"],{"CONFIG_TEST":[None,"y"]})
                (tree/".config").write_bytes(cfg.read_bytes())
                cmd_file(tree/"kernel/.sched.o.cmd", "cmd_x := clang -c s.c")
                with self.assertRaisesRegex(ValueError,"Clang kernel or module argv"):
                    fn(work,b"spec",g,None)
                cmd_file(tree/"kernel/.sched.o.cmd", "cmd_x := clang -moutline -c s.c")
                (work/"gbs.log").write_text("Entering directory 'SERET-UL'\ngcc -moutline -c s.c\n")
                with self.assertRaisesRegex(ValueError,"GCC received"):
                    fn(work,b"spec",g,None)
                z.unlink()
                with self.assertRaisesRegex(ValueError,"no single perf tree"):
                    fn(work,b"spec",g,None)


if __name__ == "__main__":
    unittest.main()
