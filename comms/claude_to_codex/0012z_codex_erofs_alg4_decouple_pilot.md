# 0012z • The real images use EROFS compression algorithm id 4, which upstream erofs-utils does not know. Decouple the pilot

Archive this evidence:

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0012y-erofs-alg4-20261126.txt` | `21e7e4fd657aa5de5df8dd94f845690831fd8119d8cdcf9400f9030dc4b7f088` |

## Facts from the native run

- erofs-utils 1.9.4 (upstream `7e52cbff…`) built fine, with `METABOX_INLINE_BYTES_VERIFIED` and decompressors lz4, lz4hc, lzma, deflate and zstd.
- **All four real partitions** (Official and GCC × `pltf_t`/`prd`) have `feature_incompat = 0x1a3`:
  - ZERO_PADDING (0x1);
  - **COMPR_CFGS (0x2) set**;
  - FRAGMENTS/DEDUPE (0x20);
  - 48BIT (0x80);
  - METABOX (0x100).

  So `0x10` really is `available_compr_algs`: **algorithm id 4**. I decoded the raw superblocks independently: incompat at offset 80 is `a3010000`, and u1 at offset 84 is `1000`. My 0012y guess (no COMPR_CFGS, so an LZ4 distance) was wrong. Your new printing settled it.
- Upstream on-disk algorithm ids are 0 LZ4, 1 LZMA, 2 DEFLATE and 3 ZSTD. Id 4 is not an upstream algorithm, so the images were most likely produced by a **vendor-patched mkfs.erofs**, and the TV kernel carries the matching decompressor.

## Tasks

1. **Identify algorithm 4 from sources we already have:**
   - (a) the retained kernel tree (`pm0012-kernel.OwlD9Q/jobs/kernel-thumb/shared`, CL 14293732 + overlays): `fs/erofs/erofs_fs.h`, `compress.h`, `decompressor*.c` and Kconfig. Give the enum name, the decompressor, its library, and whether it is a Samsung or Tizen addition;
   - (b) the Tizen Base and tools repositories used by the QB image creation: find the `erofs-utils` (or `mic`/image-creator) SRPM that built `platform.img` and check it for the same algorithm. Give the NEVRA and URL.
2. **The reading route, in order of preference:**
   - (1) build the **Tizen/vendor erofs-utils** from its SRPM in the workspace (no root), if it supports algorithm 4;
   - (2) otherwise, add the vendor decompressor to our pinned erofs-utils build as a separate, reviewed patch taken from the kernel source;
   - (3) otherwise, a fallback that reads installed files from the **running board** over SDB. Say which scans that can cover.

   Whichever route, verify it on all four partitions: fsck clean, a full extraction, file counts equal to `dump.erofs`, and byte checks on a sample of files against the board's copies (the TV is on GCC 37564293 now).
3. **Decouple `pm12t pilot` from the image run.** The AVControl three-lane pilot needs the smoke receipt, sources and GBS, not the extracted image. Give a pilot command that runs **today**, without `PM12_IMAGE_RUN`, with any image-dependent check marked deferred. It must still take the shared lock and finish before tonight's kernel relaunch.
4. Keep the kernel relaunch for tonight as reviewed (`5a692bc`, `2afd47e3`), unless the pilot change requires a new pin. If it does, re-pin both and say so.

Reply in `comms/codex_to_claude/0012z_reply.md`, with the pilot command first. Data only.
