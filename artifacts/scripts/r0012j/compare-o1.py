"""Compare the O1 board readback with the retained QB receipt and extracted Official tree."""
import csv
import hashlib
import json
import subprocess
from collections import Counter, deque
from pathlib import Path, PurePosixPath

ROOT = Path("/home1/chengkai/vd-tree/workspace")
CAPTURE = ROOT/"qb-evidence/37736448-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2"
IMAGE = "4dedcae9475edb6ba18c522ba34887c928d28ba910a2c178a5631ee6b1d7e823"
work = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def roster(path):
    rows = [tuple(line.split("\t")) for line in path.read_text().splitlines()]
    if not rows or any(len(row) != 6 for row in rows):
        raise ValueError(f"invalid six-column RPM roster: {path}")
    return Counter(rows)

def compare(label, left, right):
    for direction, delta in (("board-only",left-right),("reference-only",right-left)):
        lines = ["\t".join(row) for row in sorted(delta.elements())]
        path = work/f"{label}-{direction}.tsv"
        path.write_text("".join(line+"\n" for line in lines))
        print(label, direction, len(lines), sha(path), str(path))
    print(label, "shared", (left & right).total())

def rooted_file(root, name):
    parts = deque(PurePosixPath(name).parts)
    path = root
    links = 0
    while parts:
        item = parts.popleft()
        if item == "/":
            path = root
        elif item == "..":
            if path == root:
                raise ValueError(name)
            path = path.parent
        else:
            path = path/item
            if path.is_symlink():
                links += 1
                if links > 40:
                    raise ValueError(name)
                parts.extendleft(reversed(path.readlink().parts))
                path = path.parent
    return path

def main():
    board = roster(work/"installed-rpms.tsv")
    receipt = CAPTURE/"identity.json"
    assert sha(receipt) == "f164cf5f56ced88fd0618c68df686c79ec36aca85dbeb53972a4b128f135862d"
    table = CAPTURE/"rpm-identities.tsv"
    assert sha(table) == json.loads(receipt.read_text())["files"][table.name]
    with table.open() as stream:
        product = Counter(tuple(row[k] for k in ("name","epoch","version","release","arch","srpm"))
                          for row in csv.DictReader(stream, delimiter="\t"))
    compare("Product-catalog", board, product)
    kernel = (ROOT/"temp/pm0005-gbs-kernel.mtob625f/official/GBS-ROOT/local/BUILD-ROOTS/"
              "scratch.armv7l.0/home/abuild/rpmbuild/BUILD/tztv-kernel-1/KANTSU2E/image/perf/vmlinux")
    try:
        proc = subprocess.run(["readelf","-nW",kernel],capture_output=True,text=True)
        ids = [line.split("Build ID:")[-1].strip() for line in proc.stdout.splitlines() if "Build ID:" in line]
        print("GBS_OFFICIAL_BUILD_IDS",ids,"BOARD","419813f26f2d03bee00bde1d7173b0c2fd887530")
        if not ids:
            print("GBS_BUILD_ID_UNAVAILABLE",proc.stderr.strip()[:250])
    except OSError as err:
        print("GBS_BUILD_ID_UNAVAILABLE",str(err))
    matches = set()
    for receipt in (ROOT/"temp").glob("pm0011e-qb.*/official-platform.json"):
        info = json.loads(receipt.read_text())
        path = receipt.with_name("official-installed.tsv")
        if (str(info["qb"]) == "37736448" and info.get("image_sha256") == IMAGE
            and sha(path) == info["roster_sha256"]):
            matches.add(path)
    if matches:
        if len({sha(path) for path in matches}) != 1:
            raise ValueError("conflicting Official rosters")
        compare("EROFS-installed", board, roster(sorted(matches)[0]))
    else:
        print("EROFS-installed AWAIT_VERIFIED_ROSTER")
    cache = ROOT/"temp/pm0012c-image-cache-v1"/IMAGE
    if not (cache/"receipt.json").exists():
        print("ELF AWAIT_OFFICIAL_TREE")
        return
    assert json.loads((cache/"receipt.json").read_text())["image_sha256"] == IMAGE
    counts = Counter()
    with (work/"image-elf-match.tsv").open("w") as dest:
        for row in csv.DictReader((work/"target-hashes.tsv").open(), delimiter="\t"):
            file = rooted_file(cache/"tree",row["path"])
            digest = sha(file) if file.is_file() else "-"
            status = "MATCH" if digest == row["sha256"] else "MISSING" if digest == "-" else "DIFF"
            print(row["path"],row["sha256"],digest,status,sep="\t",file=dest)
            counts[status] += 1
    print("ELF", dict(counts), str(work/"image-elf-match.tsv"))
if __name__ == "__main__":
    main()
