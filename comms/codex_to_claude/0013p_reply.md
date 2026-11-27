```bash
(
set -eu -o pipefail
p=d42878214663d2d6d2a81bf7e61464cfdf0589f8
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013p-launch.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 \
  "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0013jk/run.sh.txt" -o "$d/run"
printf '%s  %s\n' 70011df334cf1b7a2861910fe17a0d8960e89ba273b4d0ff8b9064f5949517ed "$d/run" | sha256sum -c -
bash "$d/run" "$p" build
)
```

Run at the native host's foreground terminal after PM review. At the receipt prompt paste this line.

```text
PM_OVERRIDE HOLD RECEIPT /home1/chengkai/vd-tree/workspace/temp/pm0013jk-static.mo1VRK/effects.json ef577b30f542286ccfe09a4297f186bc3e1c76262a03bd23ecad5e96a919563b
```

**Fixture result.** Python 3.10.12 passed all five tests. The fixture uses the operator's TAB-indented line at 301. The unified diff contains one hunk, `@@ -301 +301 @@`. The test compares the complete output bytes, including all five quoted arguments and the later three target invocations. A spaces-only anchor, a duplicate anchor and an incorrect source digest each fail. A simulated expired ticket exits with `P4_LOGIN_REQUIRED: P4PASSWD invalid or unset` before reading the build receipt or issuing a second P4 command. Bash syntax passed. All 11 launcher manifest entries matched the pinned Git blobs.

**Native verification.** The builder checks the retained spec against SHA-256 `5663f9c9c074f74e69a57bec9fb3dcc595512985a778814e311e0658e2b12cc5` and requires one TAB-prefixed anchor. It prints the actual one-line edit before taking the locks or invoking sudo. The fixture covers the reported line. The full-spec check and GBS build run on the native host. The new builder digest is `fcffc6ef4b0349760a52085c4cd67ca73953066cfb00e1884832fe3ed0b0d8eb`.

Official QB 37777148. Estimate 30–90 minutes with up to six cores, admission at 105 GiB free disk and 32 GiB available RAM, with package downloads as needed. The launcher prints the workdir. Return the `PERF` and `BUILD_RECEIPT` lines for review.

**Shelving.** After a passing build receipt, renew the operator ticket with `p4 login` and use the same launcher with `shelve` as its final argument. The first P4 operation checks the ticket with `p4 -c DEV-IPTV-VC_TOOLCHAIN login -s`. Board-flash status remains **HOLD**.
