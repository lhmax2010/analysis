import contextlib
import hashlib
import io
from pathlib import Path
import runpy
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[2] / "r0013jk/kernel.py.txt"
CALL = b'\tenv $KERNEL_TOOLCHAIN_ENV ./BUILD.sh "$PROJECT" "$RELEASE_MODE" "$SIGN_CHIP" "$VERIFIER" "$SANITIZER"\n'
EXPECTED = (
    b'\tenv $KERNEL_TOOLCHAIN_ENV KCFLAGS="${KCFLAGS:+$KCFLAGS }"'
    b"'$(if $(filter clang clang-%% %%-clang,$(notdir $(lastword $(CC)))),-moutline)'"
    b' ./BUILD.sh "$PROJECT" "$RELEASE_MODE" "$SIGN_CHIP" "$VERIFIER" "$SANITIZER"\n'
)
LATER = b'\t./BUILD.sh "--target=fixture"\n' * 3


class SpecTest(unittest.TestCase):
    def setUp(self):
        self.kernel = runpy.run_path(str(SCRIPT))

    def stage(self, raw, digest=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tztv-kernel.spec.before-trace").write_bytes(raw)
            values = {"OLD": root, "ORIGINAL": digest or hashlib.sha256(raw).hexdigest()}
            stage = self.kernel["staged"]
            with patch.dict(stage.__globals__, values):
                return stage(show_diff=True)

    def test_one_line_edit(self):
        prefix = b"\n" * 300
        tail = b"\n" * 31 + LATER
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = self.stage(prefix + CALL + tail)
        self.assertEqual(result, prefix + EXPECTED + tail)
        self.assertEqual(output.getvalue().splitlines()[2:],
                         ["@@ -301 +301 @@", "-" + CALL.decode().rstrip("\n"),
                          "+" + EXPECTED.decode().rstrip("\n")])

    def test_spaces(self):
        with self.assertRaisesRegex(ValueError, "found 0"):
            self.stage(CALL.replace(b"\t", b"    "))

    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError, "found 2"):
            self.stage(CALL + CALL)

    def test_wrong_digest(self):
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            self.stage(CALL, "0" * 64)

    def test_expired_ticket(self):
        args = ["p4", "-c", self.kernel["CLIENT"], "login", "-s"]
        failure = subprocess.CompletedProcess(args, 1, "P4PASSWD invalid or unset")
        with patch.object(subprocess, "run", return_value=failure) as run:
            with self.assertRaisesRegex(SystemExit, "P4_LOGIN_REQUIRED: P4PASSWD invalid or unset"):
                self.kernel["shelve"]()
        self.assertEqual(run.call_count, 1)
        self.assertEqual(run.call_args.args, (args,))


if __name__ == "__main__":
    unittest.main()
