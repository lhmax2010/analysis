# 0012r · KantSU2E PERF

## §1. C1 warm reboot and Table A

Custom QB **37736427**, Product **20261123.1**, kernel GNU build ID **4d95bb9eb9dc71983a87f90352fc8c2b7bd8a006**. One software reboot changed the boot ID from `ff29a9c0-8770-4e41-a211-cad14de6e31e` to `91ef2da6-afb4-4556-9480-701f14e982d9`. The first successful SDB read returned the early kernel line at uptime **27.15 s**. [First connection](../../artifacts/evidence/board/c1-37736427/warm/first-connection.txt) · [Product and kernel identity](../../artifacts/evidence/board/c1-37736427/warm/identity.txt)

```text
[    0.047076] Memory: 1279812K/1631488K available (8120K kernel code, 665K rwdata, 1636K rodata, 396K init, 4025K bss, 29664K reserved, 311296K cma-reserved, 726272K highmem)
```

| VDLinux · bytes | Official 37736448 (O1 cold) | Custom 37736427 (C1 warm) | Custom − Official | Measurement |
|---|---:|---:|---:|---|
| Text | 8,564,632 | 8,315,864 | −248,768 (−2.90%) | Inclusive kernel-code extents in each board’s /proc/iomem |
| Data | 681,984 | 680,960 | −1,024 | Boot-line rwdata × 1,024 |
| BSS | 4,120,576 | 4,121,600 | +1,024 | Boot-line bss × 1,024 |
| Total | 11,348,904 | 11,085,176 | −263,728 | Verified uImage file length minus its 64-byte header |

Total includes the 260-byte trailer in each file. HQ's RPI Total definition remains unverified. The boot-line fields have 1 KiB resolution. Berkeley accounting from the linked ELF is a separate measurement (§4). [O1 boot line](../../artifacts/evidence/board/o1-37736448/cold/early-memory-log.txt) · [C1 boot line](../../artifacts/evidence/board/c1-37736427/warm/early-memory.txt) · [Inclusive physical ranges](../../artifacts/evidence/board/c1-37736427/kernel-resource-sizes.tsv) · [Matched image sizes](0011e_reply.md)

| Additional measurement | Official | Custom | Δ | Method |
|---|---:|---:|---:|---|
| rodata (KiB) | 1,640 | 1,636 | −4 | dmesg |
| init (KiB) | 404 | 396 | −8 | dmesg |
| Reserved (KiB) | 29,920 | 29,664 | −256 | dmesg |
| CMA reserved (KiB) | 311,296 | 311,296 | 0 | dmesg |
| Available at kernel initialization (KiB) | 1,279,556 | 1,279,812 | +256 | dmesg |
| uImage (B) | 11,348,968 | 11,085,240 | −263,728 | Retained QB file |
| zImage (B) | 5,326,504 | 5,222,032 | −104,472 | Retained QB file |
| tztv-kernel-perf RPM (B) | 19,345,448 | 19,160,700 | −184,748 | Retained RPM |

**Home and idle memory.** At uptime 28.48 s the focused PID was 483 and /proc/483/comm returned TA_native-home. This is the first observation of Home focus. The same PID and name were present at every sample. The exit check returned SDK uid 5001, the same boot ID and focused PID 483. The TV remains on Custom at Home. [Home evidence](../../artifacts/evidence/board/c1-37736427/warm/home-first-observed.txt) · [Exit](../../artifacts/evidence/board/c1-37736427/warm/exit.txt)

| Sample | O1 cold uptime (s) | O1 MemAvailable (KiB) | C1 warm uptime (s) | C1 MemAvailable (KiB) | Δ KiB |
|---|---:|---:|---:|---:|---:|
| 1 | 345.20 | 1,082,736 | 360.72 | 1,086,360 | +3,624 |
| 2 | 405.20 | 1,080,224 | 420.69 | 1,084,280 | +4,056 |
| 3 | 465.20 | 1,084,480 | 480.71 | 1,088,472 | +3,992 |

Each column contains three observations of one boot. Boot type and uptime differ between columns. The earlier C1 visit at 117 minutes is excluded. The observed memory differences do not establish an MLGO saving. [O1 idle samples](../../artifacts/evidence/board/o1-37736448/cold/idle-summary.tsv) · [C1 raw samples and hashes](../../artifacts/evidence/board/c1-37736427/warm/SHA256SUMS)

**Installed package delta.** Both live rosters have exactly 2,342 unique name/architecture pairs. 2,164 rows match all six fields. All **178** remaining pairs have equal epoch/version and different release. There are **zero** version changes, additions or removals. The ledger names every package, including library carriers with names such as abseil-cpp, fribidi, krb5, pam and soundtouch. Its optional DSO-path column comes from the older retained board-10813 file list; a missing example has no bearing on release classification. The image job also queries the exact matched images’ RPM file lists for shared-object owners. [Complete classified ledger](../../artifacts/evidence/board/c1-37736427/warm/roster-classification.tsv) · [Original six-field comparison](../../artifacts/evidence/board/c1-37736427/roster-delta.tsv)

| Affected family | Changed installed packages |
|---|---|
| C/C++ and OpenMP runtime | glibc, glibc-locale, libgcc, libstdc++, libatomic, libgomp, libomp, libunwind |
| Compression | gzip, xz, liblzma, zlib, libbz2, bzip2, libzstd1, libzip, minizip, zip, unzip, libarchive |
| TLS / cryptography | openssl1.1, openssl3, libopenssl11, libopenssl3, libgcrypt, libgpg-error, libfreebl3, libsoftokn3, nss, nspr, libxcrypt, xmlsec1, xmlsec1-openssl |
| Other measurement and binary tooling | util-linux, coreutils, rpm, pkg-config, libelf, libdw, sqlite, libsqlite |

The rosters contain no package named clang, llvm or compiler-rt, including packages with those prefixes. Runtime packages carry changes from both compiler ecosystems. For example, libomp 22.1.8 release 9.1 → 11.1, libgcc and libstdc++ 14.2.0 release 1.77 → 1.80, and glibc 2.40 release 1.111 → 1.119. gzip 1.3.12 and xz/liblzma 5.8.1 also have new releases. C1's gzip loads libc, the loader and libgcc_s; xz also loads liblzma and libpthread. The package metadata establishes a rebuild confounder. Compare O2 workload binaries and loaded libraries by hash before interpreting timings. Whole-board measurements currently describe the **Base swap**. [C1 workload dependencies and SHA-256](../../artifacts/evidence/board/c1-37736427/workloads.txt)

## §2. Image rerun and kernel dependency

**After review, run `pm12r image` first.** The function below downloads one immutable entry point and verifies its hash. Use a native Bash terminal. The image job detaches, holds the existing image locks, and prints its new run directory and PID. Allow hours for three extractions and the follow-on audits; reserve at least the existing 50 GiB scratch floor plus extraction space. The kernel gate requires the new run’s `DONE image rc=0`, source proof, installed-owner ledger and the approved smoke receipt. `pm0012-image.6nhIbn` ended with rc=1 and cannot supply that gate.

```bash
pm12r() (
  set -eu
  cd /home1/chengkai/vd-tree
  pin=3660bfe60ae5e30e2976e6625e436beca0ebab73
  d=$(mktemp -d "$PWD/workspace/temp/pm0012r-launch.XXXXXX")
  curl -fsSL --retry 4 --retry-all-errors --retry-delay 5 --connect-timeout 15 --max-time 120 \
    "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012r/reviewed-run.sh.txt" -o "$d/run"
  printf '%s  %s\n' e848aa98c393462a4e226c33d0d81080e3ffca173772962bf4f91938a428718e "$d/run" | sha256sum -c -
  exec bash "$d/run" "$pin" b220d2ae1ecc26066d00a8e78ba3c7d4101a37ab9c74555e60d45f11c8d1d36b c4290314f1926819217f331cb384d3cd5d2a7ab7f576ec07ae60cc2baad3285a "$1"
)
pm12r image
```

The platform job now reads both GPT entries by name, checks their extent and EROFS superblocks and verifies each filesystem. It places the extracted product tree at /prd. Each lane emits PRD_ROSTER with filesystem, root entries, the actual count of RPM-owned files and the full inventory path. The reversed-order fixture mounted the correct trees and rejected a corrupted product superblock. The native /prd contents and ownership counts require the rerun. [Fixture](../../artifacts/tests/r0012r/dual.py) · [Tests](../../artifacts/evidence/local-r0012r-checks.txt)

The failed run established byte equality of LLVM Source1005 in Official and Custom at `7d89083453e1d75707a4a6b3a6d9510a4c31e09d8e99865de2a18e07945bf76f`. GCC's source label `vbs-vdlinux-20260929.194254-0-14293732` and both LLVM kernels point to CL 14293732. KERNEL_SRPM_CONTENT_MATCH compares **GCC vs Official** kernel source RPM payload members. At least one of those two SRPMs could not be fetched, validated and enumerated from the three attempted publication paths. The per-lane HTTP/header/payload errors are in native-proofs.json. That outcome predates and is independent of the GPT extraction fix. [Source proof implementation](../../artifacts/scripts/r0012c/proofs.py.txt)

## §3. AVControl LTO delivery

The retained run measured 28 compile calls and two final DWARF CUs. Final A32 shares were 99.98% baseline and 0.95% scoped default. The old per-CU join left 28 inputs unmatched. The new receipt joins actual final-target driver/linker argv, individual compile receipts, the fat objects’ .llvm.lto definitions and their target-features, and final ELF build ID and mapping symbols. Unresolved response or archive inputs, missing IR, ambiguous target membership and unknown modes stay in REVIEW. The helper currently resolves retained CMake object lists. Other layouts require their own object-to-link evidence. [Delivery rule](../../artifacts/scripts/r0012r/lto-delivery.py.txt)

For each driver, the scoped config check now resolves the loaded spelling within its GBS root, checks the probe-time SHA, reads the marked block there, and reports gaps for the default triple, explicit ARM override and C/assembly probes independently. A log naming /usr/bin/clang.cfg alone cannot qualify the policy. The real-ELF fixture detected both a missing compile receipt and a changed selected cfg. [Driver check](../../artifacts/scripts/r0012g/thumb-options.py.txt) · [Joined-object fixture](../../artifacts/tests/r0012r/delivery.py)

| Gate | Retained default evidence | Evidence required to close it |
|---|---|---|
| T1 delivery | REVIEW under the old rule, 28 inputs unmatched | Per-object LTO receipts/attributes and final ISA, returned by the readback |
| T2 ISA | REVIEW, 0.95% A32 remains | Name and account for residual A32 ranges and verify mapping coverage |
| T3 size/scope | File sizes observed, scoped default .text −295,582 B | Read retained T3 and RPM scope result |
| T4 ABI | REVIEW | Return per-file dynamic/export comparison and abidiff status/rc; a review flag alone establishes no ABI break |
| T5 tests | CHECK_NOT_OBSERVED | Show the %check entry and executed tests |
| T6 smoke | REVIEW | Show interworking receipt and per-changed-ELF smoke marker |
| T7 source coverage | REVIEW_GENERATED_SOURCES | Resolve generated paths and compile membership |
| T8 exempt controls | N/A for AVControl | Applies to protected controls |

**Native commands after review.** `pm12r retained` re-evaluates FejM73 read-only, prints both config/LTO results, T1–T8 and the ABI/test evidence, and emits the full per-lane packets. Allow several minutes, one CPU process, local GBS-root reads plus small scratch JSON. `pm12r pilot-package` runs the package lane alone in a fresh root using the cf4e0e9 stage-wrapper fix. It needs an attended sudo terminal and P4 ticket; allow a normal AVControl build with the existing 24 GiB/12 GiB disk/RAM checks. It keeps its own lane.json. The retained GBS roots and corrected acceptance results reside on the native host. No new native PASS is recorded here.

## §4. Table B and published perf debuginfo

**Native command after review:** `pm12r size`. It reads the matched capture receipts and verified USB images, downloads each perf debuginfo RPM from the published Product armv7l/debug directory first, and uses a 20 s connect timeout and up to 1,800 s per transfer with four retries. Allow up to 1 GiB per debug package plus extracted ELFs and scratch. No GBS or board access. The command checks the RPM identity and joins ELF notes to the image's full running build ID before measuring. It also starts the §5 symbol comparison. [ELF measurement and accounting](../../artifacts/scripts/r0012p/kernel-size.py.txt)

| Table B · bytes | Official | Custom | Δ bytes | Δ % |
|---|---:|---:|---:|---:|
| Berkeley text / data / bss / dec | Await matched debug ELF | Await matched debug ELF | — | — |
| .text / .rodata / .data / .bss / .init.* | Await matched debug ELF | Await matched debug ELF | — | — |
| .text + .rodata + .data + .bss | Await matched debug ELF | Await matched debug ELF | — | — |
| uImage | 11,348,968 | 11,085,240 | −263,728 | −2.32% |
| zImage | 5,326,504 | 5,222,032 | −104,472 | −1.96% |
| tztv-kernel-perf RPM | 19,345,448 | 19,160,700 | −184,748 | −0.95% |

The requested IDs are `419813f26f2d03bee00bde1d7173b0c2fd887530` and `4d95bb9eb9dc71983a87f90352fc8c2b7bd8a006`. The tool prints individual metric rows and retains section sizes in proof.json. llvm-size -B on a separate-debug ELF can label initialized writable data as BSS. The code restores provable initialized sections from the matched image, checks totals and leaves ambiguous data/BSS open. The native debug artifacts are unavailable on this PC. Table A’s dmesg and iomem values remain independent.

## §5. Replay attribution and K0 qualification

The retained replay and shipped payloads have equal lengths but about 7.72 MB Official and 7.52 MB Custom differ, starting in .text at flat offset 0x594. This rules out a build-ID/banner-only explanation. A four-byte stride alone cannot distinguish changed instructions, branch displacements or literal addresses.

On a successful debug join, `pm12r size` compares each uniquely named text function at its own address, counts unchanged bodies that moved, changed bodies, length changes and symbol-order inversions. It checks A32 mapping symbols before decoding branches and reports changed B/BL encodings that resolve to the same named target in both images. It also prints ELF toolchain markers and config hashes joined to the replay by vmlinux hash. These checks distinguish layout effects from changed function bodies. A toolchain or build-path cause still needs the corresponding effective inputs; exact causation awaits native evidence. [Symbol comparison](../../artifacts/scripts/r0012r/replay-symbols.py.txt)

K0 now requires matching config, required image lengths, a matching section comparison and a complete flat Image comparison. Only a verified equal-position GNU build-ID digest or same-length complete Linux banner can explain changed bytes automatically. Any unexplained byte keeps K0 unqualified. The earlier GBS replays cannot substitute for the shipped ELF table. To use a matched Official separate-debug reference, export PM12_OFFICIAL_PERF_ELF with the actual reference path from the §4 receipt. After the image job finishes successfully, set PM12_IMAGE_RUN to **that exact new directory** and run `pm12r kernel` in an attended terminal. The six lanes run serially with the existing resource checks. [K0 qualification](../../artifacts/scripts/r0012l/kernel-qualification.py.txt)

## §6. Shared disk and retention

Native command `pm12r disk` measures allocated bytes for every immediate directory or symlink under workspace and workspace/temp, without traversing other filesystems. It prints the largest entries and the complete TSV in one zlib/base64 packet. The workspace/temp aggregate includes the child rows, and separately measured trees can share hardlinks. Permission errors mark sizes partial. Allow minutes to tens of minutes of metadata I/O on a large build tree. Running it locally would measure a different filesystem.

| Native entry | Current retention decision |
|---|---|
| pm0005-gbs-kernel.mtob625f | Keep for replay bytes, symbols and config |
| pm0010-gbs-board-bench.eli_m1on | Keep pristine tool inventory |
| pm0012-smoke.neJb0i, pm0012-pilot.FejM73, pm0012-wed-a.M5knpj | Keep for launch gate, LTO receipts and Wed-A evidence |
| qb-evidence, usb | Keep immutable QB and rollback inputs |
| z901 (reported 17G), manifest_state (23G), s895c (12G) | Keep experiment/manifest evidence and checkout awaiting owner review |
| llvm22_bootstrap101_* (reported 10G), vd-gbs-applied-full-build-r3-*, o*, core*, ctx* | Keep pending census and consumer review; prefixes alone do not establish disposal eligibility |
| pm0010-gbs-board-bench.hadnvlae and .hfmy3w53 | Operator already removed both |

**Additional confirmed reclaimable space: 0 B.** `pm12r prune-confirmed` checks the two exact retired paths and exits without deleting anything. A reappearing path requires fresh review. Logs, JSON, mounts and builds remain intact. The native census will supply measured sizes and per-row coverage. [Census and exact-path check](../../artifacts/scripts/r0012r/workspace-disk.py.txt)
