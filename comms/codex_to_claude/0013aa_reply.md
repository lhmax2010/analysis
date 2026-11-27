# 0013aa · S12 on the four submitted QBs

## 1. Retain any finished QB immediately

```bash
(
set -eu
pin=4d71d0e85fca85760f4065f4f40988ae6723f89e
t=/home1/chengkai/vd-tree/workspace/temp
read -r -a qbs -p "Finished QB(s), separated by spaces, as QB or QB=full-Product-URL: "
(( ${#qbs[@]} > 0 ))
d=$(mktemp -d "$t/pm0013aa-launcher.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013y/read.sh.txt" -o "$d/run.sh"
printf '%s  %s\n' a395c5a0382bb03185a24e03fcbecb0438e98de5608b07c0778ec2a11e527a72 "$d/run.sh" | sha256sum -c -
bash "$d/run.sh" "$pin" s12 --retain "${qbs[@]}"
)
```

Run on the native server as each Product publishes. Enter one or more finished IDs from the table below. For a first capture with no operator config, enter the exact published URL as `QB=Product-URL`. A bare ID works after retention. Return each `S12_RETAINED` line and `S12_RETENTION COMPLETE`. A partial run can be retried with the same inputs. A different result for an already retained checksum is an error.

## 2. Compare the same-day twins after all four publish

```bash
(
set -eu
pin=4d71d0e85fca85760f4065f4f40988ae6723f89e
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013aa-launcher.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013y/read.sh.txt" -o "$d/run.sh"
printf '%s  %s\n' a395c5a0382bb03185a24e03fcbecb0438e98de5608b07c0778ec2a11e527a72 "$d/run.sh" | sha256sum -c -
bash "$d/run.sh" "$pin" s12 Official:37836579=37836693 Custom:37836654=37836727
)
```

| Lane | Published LLVM Base | MLGO only · 14427407 | MLGO + clang-only `-moutline` · 14507546 | Historical reference for INFO |
|---|---|---:|---:|---:|
| Official | 20261113.1 | 37836579 | 37836693 | 37777148 |
| Custom | 20261118.1 | 37836654 | 37836727 | 37777264 |

Both commands run at idle CPU and I/O priority on the native server. Estimate 5–30 minutes per online QB, depending on Product availability and debuginfo. Allow several GiB per publication for verified RPMs and scratch, plus space for extracted ELFs during comparison. The first command reads the Product repository and writes durable inputs under `workspace/qb-evidence/<QB>-<release>/s12/`. The second reads verified local inputs first and captures any missing primary inputs before analyzing ELFs. Neither command requires sudo, GBS, a build lock or board access.

Return both `S12_PAIR` lines, both `S12_REPRO` lines, `S12_PACKET` and final `S12 PASS|FAIL`. For the full per-module comparison, use the printed packet path and print one numbered line at a time with the reported `sed` command, changing its line number for later parts. The final verdict requires both primary comparisons to pass.

## Measurements and review decision

The operator supplies the numeric QB-to-URL association. The reader checks it against existing config or capture evidence where available, then checks the published Product ID, Clang build.conf name and lane-specific Base URL. Same-day submission and shelf assignments come from the operator. S12 measures the binaries and modules delivered by those publications.

Each pair prints reference/candidate helper counts, PERF ELF `.text` sizes and their signed byte delta, module counts and counts of available `Module.symvers` sources. Module checks cover package/path set, internal module name, vermagic, release, signature presence, loadable relocation types and CRC tables where shipped. Zero CRC tables on both sides means CRC evidence was unavailable. PERF `.text` comes from a GNU-build-ID-matched ARM kernel ELF. K0 was 8,564,600 B and K1 was 8,214,312 B. A matching difference in sizes alone cannot establish module compatibility.

**Tolerance for PM review.** The no-outline reference must measure zero outlined helpers. For the candidate, the implementation reuses the existing K1 verification tolerance of ±0.10% around 20,324 distinct helper addresses (20,304–20,344 inclusive) in both lanes. K1 was measured on Official. A Custom count outside that window is reported with its measured value and holds the primary gate for review. Missing helper or ELF evidence also holds that gate. To supply a retained local PERF ELF, set `S12_<eight-digit-QB>_ELF` to its absolute workspace path before running command 2. Its GNU build ID must match the verified boot payload. [K1 verification criterion](0013v_reply.md)

The INFO check compares each new no-outline reference against the earlier reference for that lane. It compares PERF `.text` size, unique helpers and the module set. It prints `IDENTICAL`, `DIFFERENT` with the measured differences, or `UNAVAILABLE` when evidence is insufficient to decide. Historical differences and missing historical symbols leave both primary verdicts independent.

## Evidence and validation

The archived terminal output confirms 130 RPMs retained per historical QB. Each reused 4 RPMs and fetched 126. The historical retention manifests begin `24efe905` and `b6780cf0`. It also records stooH5 entering enumeration with the replacement Official Product. Its completion and all four new publication results await native readback. Archive SHA-256 is `7d67313a3232fdae25940cbd59aae991bcd36b9c1490eeeb6bd0af3f4ddb5b6a`. [Original evidence](../../artifacts/evidence/native-run-r0013z-retain-and-enum-stooH5-start-20261127.txt)

Python 3.10.12 fixtures passed for operator pair parsing, release identity, single and multiple retention, corrupt and offline caches, isolated historical errors, partial primary coverage, and module verdicts. An ARM ELF32 fixture measured a 12-byte `.text` and one outlined helper. A mismatching build ID was rejected. Launcher syntax and hashes were checked locally. The operator has submitted the four QBs. Board testing uses the four cells after both primary pairs pass, comparing outline on/off within each Base and comparing Bases at fixed outline setting. PM review of this pin is pending. [Pair fixture](../../artifacts/scripts/r0013aa/tests/pairs.py) · [Retention fixture](../../artifacts/scripts/r0013z/tests/retention.py)
