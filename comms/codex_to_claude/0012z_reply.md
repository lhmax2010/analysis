# 0012z · AVControl pilot

```bash
pm12t() (
  set -eu
  test "$1" = pilot
  cd /home1/chengkai/vd-tree/workspace/temp
  p=dd210fb3fef72e58e5b0fd29026f86527fc4fba9
  d=$(mktemp -d "$PWD/pm0012z-pilot.XXXXXX")
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0012t/next.sh.txt" -o "$d/run"
  printf '%s  %s\n' b3104be667cd433352250e850d712b04c36ba45cabaac8570af310e02eaaa68e "$d/run" | sha256sum -c -
  bash "$d/run" "$p" 34007ce035d5d89b9f21ab7baed085f6e68a6949fc97286ca6f48906abd66707 a984c67ad51ee218c32a0e138ee45d1dfc09ad31e1996a510bf89ebb16aca2a7 pilot
)
pm12t pilot
```

Native Bash, foreground after PM review. This terminal function is scoped to the pilot. Allow 30–90 minutes, 62 GiB free, one GBS job at a time, up to six cores, P4 access, intranet dependency reads and attended sudo. First gate: `KERNEL_SMOKE_GATE_PASS …/pm0012-smoke.neJb0i` is the existing shared smoke validator. The run prints `PILOT_DEFERRED`, the native batch directory and the T1–T8 results for the scoped-default and package-fix treatments against the same baseline. The three builds still use the queue and heavy-job locks. RPM contents, compiler argv, delivered ISA, ABI and board acceptance retain their existing evidence requirements. Installed-image membership, equality to the installed ELF and the image-wide A32 census await image evidence. The local Python 3.10.12 replay accepted the archived smoke argv/ELF/PASS with the image environment unset, rejected a missing PASS, and all 53 batch manifest hashes matched. A native pilot result has yet to return. [Smoke evidence](../../artifacts/evidence/native-run-r0012m-inventory-cleanup-smoke-20261125.txt) · [Pilot launcher](../../artifacts/scripts/r0012t/next.sh.txt)

**Tonight's kernel command stays at `5a692bca11e88830955df5c174bd0675bc2da5cb`, launcher SHA-256 `2afd47e386fa3d4f95f0271bb5136c6eb874c84963570acba1dae95af63e1d38`.** Start after the foreground pilot exits and releases its locks. The image scan can remain blocked. [Full kernel command](0012y_reply.md)

## EROFS identification and four-partition status

**Algorithm 4 is vendor ZLIB.** The GCC 37564293 board BTF matches the retained RPM SHA-256 `1a5ee77d0f3760df26546522966b0083a703343f1609b5d0decc473980ab979f`. Its enum assigns 4 to `Z_EROFS_COMPRESSION_ZLIB`, 2 to `Z_EROFS_COMPRESSION_DEFLATE` and 7 to the runtime-only `Z_EROFS_COMPRESSION_ZLIB_HW`. It contains `z_erofs_load_zlib_config`, `z_erofs_zlib_decompress` and a `z_stream_s` in `struct z_erofs_zlib`. The kernel contains its own `zlib_inflate*` implementation. Both shipped uImages independently map slot 4 to the string `zlib` in the eight-entry decompressor table. The GCC and Official table offsets within the uImage payload are 0xb44e78 and 0xa70a44. This identifies the codec and software implementation in VDLinux. Source attribution to a particular Samsung/Tizen change, the exact window/wrapper initialization and the NEVRA/URL of the mkfs used by QB remain open. [Board BTF and both dispatch tables](../../artifacts/evidence/board/g1-37564293/0012z/btf-and-dispatch.txt) · [Upstream disk enum at the tested revision](https://git.kernel.org/pub/scm/linux/kernel/git/xiang/erofs-utils.git/tree/include/erofs_fs.h?id=7e52cbffa83fbe9eb10bbf110cb12d503a048081)

| QB | Partition | Image offset (bytes) | Incompat / algorithm bitmap | Existing board reference | Vendor fsck / extraction / counts |
| --- | --- | ---: | --- | --- | --- |
| Official 37736448 | pltf_t | 1,048,576 | 0x1a3 / 0x10 | O1 AVControl and tv-viewer | Pending |
| Official 37736448 | prd | 1,163,919,360 | 0x1a3 / 0x10 | Collect the two lower-mount hashes on the next Official visit | Pending |
| GCC 37564293 | pltf_t | 1,048,576 | 0x1a3 / 0x10 | G1 os-release and gzip | Pending |
| GCC 37564293 | prd | 1,190,133,760 | 0x1a3 / 0x10 | G1 rpmi and usb_mount.sh | Pending |

All four raw superblocks have little-endian `a3010000` at offset 80 and `1000` at offset 84. The COMPR_CFGS bit selects a bitmap. Upstream erofs-utils 1.9.4 passed the metabox byte fixture; its available decoders cover IDs 0–3. The local parser stopped before fsck on each real partition. **0/4 real partitions have passed the offline reader checks.** G1's two live lower mounts reported EROFS and read-only, and all four sample hashes were collected with SDK UID 5001. The protected BTF read used temporary root; SDK UID 5001 and the same boot ID were verified afterwards. The TV stayed on GCC. [Raw native evidence](../../artifacts/evidence/native-run-r0012y-erofs-alg4-20261126.txt) · [G1 sample hashes](../../artifacts/evidence/board/g1-37564293/0012z/lower-mount-hashes.txt) · [O1 ELF hashes](../../artifacts/evidence/board/o1-37736448/target-hashes.tsv)

## Image writer and reading route

Run the source probe independently of GBS. It reads the retained OwlD9Q kernel tree, both published build descriptions, Base/Product RPM metadata and discoverable tools-repo references. It checks primary metadata and SRPM checksums and reads specs, patches and relevant inner sources without installation. If the job's separate tools repository is known, `PM12Z_TOOLS_REPO` accepts its exact repodata base URL on the VD repository host. A source match establishes available implementation; attributing the writer requires the image job's tool inventory, NEVRA/build log or equivalent trace. The native workdir and full source log are retained. Local tests used a real source RPM with a source tarball. Native source acquisition is outstanding.

```bash
pm12z_reader() (
  set -eu
  cd /home1/chengkai/vd-tree/workspace/temp
  d=$(mktemp -d "$PWD/pm0012z-launch.XXXXXX")
  p=dac63b2d2afe63d0c6fdc42dcdaa93961135492c
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0012z/reader-run.sh.txt" -o "$d/run"
  printf '%s  %s\n' 1501ffe15159371091c73fe274aa35ec5c8ed8e59ae8f77c9fa3256ee154dcd3 "$d/run" | sha256sum -c -
  bash "$d/run" "$p" "$1"
)
pm12z_reader source
```

Native host, no sudo. Estimate 2–20 minutes, one CPU, repository metadata and selected source downloads, normally under 1 GiB scratch. The independently identified on-disk enum gives the following order for the reader.

1. **Vendor userspace first.** Match the image-creator's mkfs package to its SRPM. Check the enabled compressor, config structure and corresponding fsck/dump decoder. Build that reviewed source and its needed dependencies in a private workspace prefix and hash both binaries. The vendor version must support the 48-bit and metabox features on these images as well as ZLIB.
2. **Reviewed decoder port if the vendor package has only a writer.** Use the retained kernel's config parser, padding, partial decoding, input bounds and inflate initialization as the format reference. Register slot 4 separately from raw DEFLATE. Exercise a vendor-written compressed fixture, truncation, invalid config, partial last block and metabox, then run the four real partitions. A successful link with libz alone does not qualify this route.
3. **Board fallback available today for installed-content reads.** Hash and inspect named files on `/.org_rootfs` and `/.org_rootfs/prd`, join installed RPMs to paths, and inspect shipped ELF sections, producer markers and ISA where readable. Requires the matching image on the TV for each lane. Raw offline integrity, extraction-count equality, uninstalled RPMs and historical compile argv remain separate checks. No flash is required for the GCC reads already saved.

**Verification once a reviewed reader is available.** In the same native shell, set `PM12_EROFS_RECEIPT` and `PM12_EROFS_SHA` to the vendor build's two-binary receipt and its SHA-256, then run `pm12z_reader verify`. Allow 10–60 minutes, sequential local disk I/O, one partition at a time, 50 GiB reserve plus extraction scratch. The runner pins both USB platform.img hashes, holds the native queue lock, checks the GPT slices, runs fsck with decompression, fully extracts, compares the entry count with dump -S, requires a positive compressed-file count and prints sample digests. It emits one row per partition. For the remaining Official prd reference, collect the Product line from /etc/prd_info.ini and sha256sum of both /.org_rootfs/prd/bin/rpmi and /.org_rootfs/prd/bin/usb_mount.sh on the next Official visit. Point `PM12Z_OFFICIAL_PRD_SHA256SUMS` at that saved terminal text under the native workspace. Until then the checker reports that row open. The upstream-only receipt cannot qualify the vendor reader. [Source probe](../../artifacts/scripts/r0012z/vendor-source.py.txt) · [Four-partition checker](../../artifacts/scripts/r0012z/verify-reader.py.txt)

Raw native input SHA-256: `21e7e4fd657aa5de5df8dd94f845690831fd8119d8cdcf9400f9030dc4b7f088`. Claude review pending.
