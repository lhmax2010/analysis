```bash
(
set -eu -o pipefail
p=1a9d27cfef4549c14a74a951c8ba18f77f9270f6
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013l-launch.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0013l/run.sh.txt" -o "$d/run"
printf '%s  %s\n' 91d68f974bc5edbf82c2585cba7e122f04e6fed7f217e26fa1ff02cbb81688ec "$d/run" | sha256sum -c -
bash "$d/run" "$p" static | tee "$d/combined.txt"
)
```

### Evidence and follow-up verdicts

| Question | Current evidence | Follow-up output |
|---|---|---|
| Old/new Official platform identity | Both images have 4,793 ELFs, 701,762,092 executable bytes and 300,990,787 estimated A32 bytes across platform and prd. Both Official platform inodes total 81,321. | Verified platform.img and GPT partition hashes, then regular-file and symlink differences if a slice differs. Equal partition digests establish zero file-content differences. Attribution to republication or deterministic rebuild requires publication provenance. |
| A32 roster | GCC→Official has +24,873,239 estimated A32 bytes and −33,871,486 executable bytes. Unclassified ELFs are 159/162. | Per-RPM byte totals, top 30 positive A32 deltas and per-file ARM/MIXED_ARM roster. Kernel modules are separate. Historical source/prebuilt and explicit -marm classifications require an identity/argv join on the new image. JIT name matches are candidates. |
| C2 interworking | 74,405 historical C2 rows grouped by function and instruction class; 2,931 possible caller rows. Neither count measures incompatible returns. | Exclude ordinary ARM-state ALUWritePC and load-to-PC returns. Count mapped Thumb MOV/ADD to PC, distinguish proved same-ELF direct A32 BLX plus straight-line reachability, candidates and unknown-mode bytes. Indirect, cross-DSO and multiblock reachability still need owner or board evidence. |
| GAP ownership | 4,510 prior GAP rows, 4,398 unknown owners. | Query a scratch copy of the image RPM DB for per-file lists; reconcile installed.tsv, published ELF path/digest, nested container owner and unresolved ambiguities. Recount C1/C2/C4/C5 with source/mode coverage. |
| Loader DT_RELR | Target loader SHA-256 starts aec21fb5. HgSjf0 could not identify its provider. | Exact installed glibc file digest/EVRA, version node and read-only target-loader fixture. Eight correctly relocated words establish YES. Version alone is insufficient; missing loader execution leaves the result unproved. |
| E1 | CU evidence for 781/14,852 ELFs. | Classify .comment alone for installed and published views. Report Clang/LLVM observed, GCC only, other, missing, unavailable. Report candidate sources with no Clang marker and all 27 historical rows with gap counts. GCC CRT can account for the only comment. |
| AVControl | **Size-qualified; production acceptance deferred to the Thumb QB board gates.** Baseline/default/package .text is 736,944 / 441,362 / 179,660 B. Each treatment retains 88 A32 bytes. The package lane also changes optimization/LTO. | Compare defined exports/tags with the actual 37777148 executable, run the target loader's dependency list in its sysroot using its cache and effective RPATH/RUNPATH, collect object-byte candidates alongside retained link-map evidence. N/A for zero defined exports requires equal dynamic tags. |

O1 SDB capability reports `cpu_arch:armv7`. The archived 16 November TV system-state dump explicitly records `/proc/cpuinfo` architecture 7 on CPUs 0–3, implementer 0x41, part 0xd03, revision 4. Separate cpuinfo files for the O1/C1/G1 visits were not located. For a Thumb-state ALU write to PC, the relevant return path is to an ARM caller. ARMv7 load-to-PC returns can interwork. [O1 capability](../../artifacts/evidence/board/o1-37736448/capability.txt) · [Arm branch and call reference](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/branch-and-call-sequences-explained)

**RELR coverage correction.** The producer of the original E6 row prints [covered, unmatched, number of input tables]. The returned [374, 4419, 2] means both partition tables were processed and 374 of 4,793 ELFs had an exact join. The estimated 2,136,444 B saving applies to those 374; the largest contributor there is lightweight-web-engine-profile_tv, 1,194,020 B. The new command reads the installed ELFs and computes each object's REL and packed estimate independently. [Native return](../../artifacts/evidence/native-run-r0013i-read-a0Pmc0-0013f-HgSjf0-0013g-nkPaPY-20261126.txt) · [Coverage calculation](../../artifacts/scripts/r0013f/review.py.txt)

**Pilot gates.** T3 reference/PASS/PASS and T5/T8 N/A remain as returned. T1/T7 need matching Official input/final-link evidence. A single CU or missing FILE symbols in a stripped executable cannot establish the final link mode. T2 passed on baseline; both treatment intervals are 60 B and 28 B, outside the PLT, with input attribution open. T6 has an independent interworking/runtime prerequisite even if the dependency chain resolves. The new archive records T1–T8 per lane, candidate object matches and the actual Official hash relative to the historical fa474d0e… executable.

Native host after Claude review. One idle-I/O worker, no lock, GBS or sudo. Estimate 1–6 hours depending on image I/O and private repository availability. The command uses qp4O4m, HgSjf0, nkPaPY and fresh workspace scratch; reserve 50 GiB plus one expanded image and extraction. It may download missing immutable RPMs for the E1/source census. Missing published bytes, database, disassembler or emulator remain coverage gaps. Paste the compact terminal results and archive hash.

### USB export

Run on the native host with the transfer USB mounted. Confirm the device printed by findmnt. A fresh directory prevents overwriting the existing archives or a flash bundle.

```bash
(
set -eu
read -r -p 'Exact USB mount point: ' usb
mountpoint -q -- "$usb"
findmnt -T "$usb" -o SOURCE,TARGET,FSTYPE
read -r -p 'Confirm transfer stick (type USB): ' ok
test "$ok" = USB
dest="$usb/pm0013l-tables"
mkdir -- "$dest"
t=/home1/chengkai/vd-tree/workspace/temp
check() { (cd "$1" && printf '%s  %s\n' "$2" "$3" | sha256sum -c -); }
f=09d2b2dd28814bbea8668991fbdb252c93288fdc6942b8a18ad74fdec479a74e
g=0915605bb62e6f45acdc0d2d428639377672d887ed47b13b2f31c2d4e3f80803
check "$t/pm0013f-review.HgSjf0" "$f" tables.tar.gz
check "$t/pm0013g-static.nkPaPY" "$g" static-tables.tar.gz
cp -- "$t/pm0013f-review.HgSjf0/tables.tar.gz" "$t/pm0013g-static.nkPaPY/static-tables.tar.gz" "$dest/"
sync
check "$dest" "$f" tables.tar.gz
check "$dest" "$g" static-tables.tar.gz
)
```

After safe eject on the native host and operator confirmation that the stick is plugged into the TV, resolve the removable mount from the board mount table, pull the two named archives over SDB and verify both complete digests in the Desktop workspace. The USB handoff is still open. [Archive receipts](../../artifacts/evidence/native-run-r0013i-read-a0Pmc0-0013f-HgSjf0-0013g-nkPaPY-20261126.txt)

PC readback after the stick is on the TV. This reads the board mount table and requires exactly one mounted copy with both archives.

```bash
(
set -eu
cd /home/toolchain/Desktop/temp
python3 -B - <<'PY'
from pathlib import Path
import hashlib, re, subprocess, tempfile
board = "192.168.108.25:26101"
expected = {"tables.tar.gz":"09d2b2dd28814bbea8668991fbdb252c93288fdc6942b8a18ad74fdec479a74e",
            "static-tables.tar.gz":"0915605bb62e6f45acdc0d2d428639377672d887ed47b13b2f31c2d4e3f80803"}
subprocess.run(["sdb","connect",board],check=True)
sdb = ["sdb","-s",board]
mounts = subprocess.check_output(sdb+["shell","cat /proc/mounts"],text=True)
copies = set()
for row in mounts.splitlines():
    fields = row.split()
    if len(fields)<3 or not re.fullmatch(r"/[A-Za-z0-9_./-]+",fields[1]): continue
    folder = fields[1].rstrip("/")+"/pm0013l-tables"
    probe = " && ".join("test -f "+folder+"/"+name for name in expected)
    if subprocess.run(sdb+["shell",probe+" && echo FOUND"],capture_output=True,text=True).stdout.strip()=="FOUND":
        copies.add(folder)
if len(copies)!=1: raise SystemExit(f"Expected one mounted archive folder, found {len(copies)}")
folder = copies.pop()
dest = Path(tempfile.mkdtemp(prefix="pm0013l-usb.",dir=Path.cwd()))
for name,expected_sha in expected.items():
    file = dest/name
    subprocess.run(sdb+["pull",folder+"/"+name,str(file)],stdout=subprocess.DEVNULL,check=True)
    h = hashlib.sha256()
    with file.open("rb") as stream:
        for data in iter(lambda:stream.read(1<<20),b""): h.update(data)
    if h.hexdigest()!=expected_sha: raise SystemExit("SHA mismatch "+name)
    print("VERIFIED",h.hexdigest(),file)
print("USB_READBACK_COMPLETE")
PY
)
```

Local checks passed under Python 3.10.12, including an ARM/Thumb ELF fixture with a direct BLX and a Thumb ALU return. The full-image results require the native partitions and RPMs.
