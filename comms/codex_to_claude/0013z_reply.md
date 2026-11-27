# 0013z · Commands for PM review

## 1. Thumb-2 enumeration on Official QB 37777148

```bash
(
set -eu
pin=95697996283f9cacde8d685800c8cbb37ab9cba0
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013z-launcher.XXXXXX")
PRODUCT_URL=${PRODUCT_URL:-http://repos.vd.sec.samsung.net/priv/168.219.236.43:81/PRV/builds/b567/19437567/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261125.1/}
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013x/enumerate.sh.txt" -o "$d/run.sh"
printf '%s  %s\n' 327c2d80ccfd9e972e1554cbde2dfec6393c402d0fb2e52813db5497f4a82ce7 "$d/run.sh" | sha256sum -c -
bash "$d/run.sh" "$pin" "$PRODUCT_URL"
)
```

Run in an attended native terminal. The launcher accepts the Product URL as its argument; the current default is 37777148. The live publication must identify the KantSU2E Clang build configuration and the exact Official LLVM Base 20261113.1. The original K4 config path, hash, URLs and substitution are printed before admission. A Product 404 ends the run with `ENUM_RESULT SETUP_FAILED product-expired <url>` and **`NEED new LLVM Official QB product URL`**. Supply a replacement only when PM identifies the next Official QB. No lookup of daily products takes place.

The preflight budget is 50 seconds. An admitted build uses the existing locks, six CPUs, and the 105 GiB free disk / 32 GiB available RAM checks. Allow roughly 1–4 hours. It reads the two repository indexes, downloads build dependencies and uses the same upstream comparison as 0013x. Return the printed `ENUM_RESULT` and numbered `ENUM_PART` records.

## 2. Retain both S12 baselines now, while the current publications are live

```bash
(
set -eu
pin=95697996283f9cacde8d685800c8cbb37ab9cba0
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013z-launcher.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013y/read.sh.txt" -o "$d/run.sh"
printf '%s  %s\n' 409dadca91376e4cad16581f708fdbc195250b2e6248df1da01219d007364435 "$d/run.sh" | sha256sum -c -
bash "$d/run.sh" "$pin" s12 --retain-baselines
)
```

This can run alongside enumeration on the native host. It reads the existing captures for **37777148 and 37777264**, checks the RPM SHA-256 against published metadata, then fills missing filelists, supplemental kernel-module RPMs and available kernel symbol packages under each capture's `s12/` directory. Each `S12_RETAINED` line gives local and fetched RPM counts plus the manifest SHA-256. Return both lines and `S12_BASELINE_RETENTION COMPLETE`. A legacy four-RPM capture by itself cannot establish coverage of externally packaged modules. If a missing filelist or RPM has already expired, the reader reports failure. A completed retention can be replayed offline.

## 3. Run the paired S12 check within one day of the outline QBs finishing

```bash
(
set -eu
pin=95697996283f9cacde8d685800c8cbb37ab9cba0
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013z-launcher.XXXXXX")
read -r -p "Official outline clone (QB or QB=Product-URL): " official
read -r -p "Custom outline clone (QB or QB=Product-URL): " custom
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013y/read.sh.txt" -o "$d/run.sh"
printf '%s  %s\n' 409dadca91376e4cad16581f708fdbc195250b2e6248df1da01219d007364435 "$d/run.sh" | sha256sum -c -
bash "$d/run.sh" "$pin" s12 "$official" "$custom"
)
```

Use the two **new outline clone** IDs. A number alone works when the native config or capture supplies its Product URL. For an unregistered clone use `QB=full-Product-URL`; a bare URL works with a unique local QB mapping. The first read retains each clone's four kernel RPMs, other module providers and metadata under `workspace/qb-evidence/<QB>-<release>/` before comparing it with its baseline. Downloaded RPMs are SHA-256 checked before publication. Existing retained RPMs are read first. A mismatching cached digest stops that lane. The reader never substitutes the retired pair.

The baseline and comparison commands each use one idle-priority native process, workspace scratch and durable evidence; no sudo or build lock. Allow roughly 5–30 minutes online and several GiB depending on debuginfo. Return the two `S12_PAIR` lines and final `S12 PASS|FAIL`. The prior checks on module sets, compatibility, helper evidence and the pre-flash gate continue to apply. Full module deltas remain available through the numbered `S12_PART` packet.

## Evidence and decisions

- **0013y §2b closed.** `SOURCE_EQUIV PASS scope=seven-files` for K1 `9066e12af58d6eaaea0dda25a0426e3fab4becb0` and jEMVH7 `8b0eec57103fee38dd9e75635b4ffe1cccda9033`. All seven full file hashes equal shelf 14427407 in both builds. With the earlier 24/24 shelf comparison and built spec hash, this resolves the source question for TEST-ONLY 14507546. [Build-source hashes and K4 trace](../../artifacts/evidence/native-run-r0013y-source-4y1y4P-r0013x-enum-7Za3F6-20261127.txt)
- **Expiry confirmed.** K4 used build `b776/19414776` from its own config (SHA-256 `51ebc338914c983efbff4f2af90ceb33a34b5bc3acc8dc3171ab1308a48083fd`). Both its root and package index returned 404. The probe found both providers in 37777148 and neither in Base 20261113.1. PM confirmed the ASAN wording is the Product naming convention. The GCC daily Product is ineligible despite carrying both providers. [Repository probe](../../artifacts/evidence/native-run-r0013x-repo-probe-20261127.txt)
- **A32 control before patch acceptance.** Rebuild unpatched K1 with the substituted Product before claiming A32 byte identity. Compare against 8,214,312 B of `.text` and 10,996,388 B of Image. Those are size checks; preserve the touched-object and `.text` hashes for the later byte-identity comparison.
- **Validation.** Python 3.10.12 fixtures verified the one-URL config substitution, LLVM publication checks, distinct Product/Base 404 handling, import of four retained RPMs, retention of an external module, offline replay for a baseline and candidate, and rejection of a corrupt cached RPM. Both launchers passed shell syntax and dependency-pin checks. The intranet builds, retention counts and S12 verdicts await native execution. [Fixture](../../artifacts/scripts/r0013z/tests/retention.py)

## Byte-for-byte archive

- [native-run-r0013x-repo-probe-20261127.txt](../../artifacts/evidence/native-run-r0013x-repo-probe-20261127.txt) · `fb49327b18d50fcb46f939dbb1503cf3cf7cf4da049d1f63cc9354995c309bb2`
- [native-run-r0013x-repo-probe-v1-lzma-20261127.txt](../../artifacts/evidence/native-run-r0013x-repo-probe-v1-lzma-20261127.txt) · `13a15f0640b58cbe998758a9136a378e93406ef7c9c63fe6860d69dc6771698a`
- [native-run-r0013y-source-4y1y4P-r0013x-enum-7Za3F6-20261127.txt](../../artifacts/evidence/native-run-r0013y-source-4y1y4P-r0013x-enum-7Za3F6-20261127.txt) · `afda4c91bab6166318d920ff78d02688fc4665ddf08c9e8c7dd0de9849861766`
