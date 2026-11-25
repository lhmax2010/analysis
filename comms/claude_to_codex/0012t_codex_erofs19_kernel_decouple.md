# 0012t • Image run `pm0012-image.mKv04z` failed again: the EROFS features are too new for erofs-utils 1.7.1. Decouple the kernel batch

Archive this evidence:

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0012r-image-mKv04z-erofs-20261125.txt` | `b913ac17c29a627de4aa0c04c2bbba2275df9f27b2903176ce603b757249c002` |

## What happened

The partition-by-name fix worked: the job got past the GPT stage. It then failed in `fsck.erofs`:

```
fsck.erofs rc=1: <E> erofs: unidentified incompatible feature 180, please upgrade kernel version
<E> erofs: failed to read superblock
```

`0x180` = `EROFS_FEATURE_INCOMPAT_48BIT` (0x80) + `EROFS_FEATURE_INCOMPAT_METABOX` (0x100). These are the 48-bit layout and the metadata-compression ("metabox") features. The image was made with a newer mkfs.erofs than the native host's **erofs-utils 1.7.1** can read. Upstream erofs-utils **1.9** defines both features, and its fsck and dump gained metabox support. `hq` (rc=1) and all the dependent jobs (rc=2) failed for the same reason.

## Tasks

1. **erofs-utils ≥ 1.9 in the workspace, without root and without system packages.** Fetch a pinned upstream tag: the official git or kernel.org tarball for v1.9 or later, recorded with its hash. Build it under `workspace/temp/pm0012t-erofs-utils.*` with the build dependencies already on the host.
   - First check the compressors that the image actually uses. Read the superblock and the `compr_cfgs` with your own parser or `dump.erofs -s` from the new build, and make sure the matching decompressors (lz4, lzma, zstd, deflate) are compiled in. If a needed development header is missing, report which, and build that library from a pinned source tarball in the same directory. Do not install anything system-wide.
   - Verify the new build on both partitions (`pltf_t`, `prd_t`) of Official and GCC: run `fsck.erofs` (no errors), then `--extract`. Check the extracted file counts against `dump.erofs`.
   - Make `image-tree.py` use only this pinned binary (by absolute path plus hash), and record its version in every receipt.
2. **Decouple the kernel batch from the image run.** K0–K5 need the kernel source, the `.config`, the Official/Custom kernel captures and the smoke receipt. As far as I can see, they don't need the extracted platform tree. If that's true, change `pm12r kernel` so it no longer requires `PM12_IMAGE_RUN` (or accepts the failed run with the image-dependent checks marked N/A), so the kernel batch can start **tonight**. If some kernel check really needs the image, name it, and make only that check wait.
3. **Order on the native host:**
   - tonight: the kernel batch (attended, overnight);
   - tomorrow: the erofs-utils build (it does not use GBS, so it can run in parallel), then the image re-run, then `pm12r pilot-package`.

   If the erofs-utils build is quick and safe to run while the kernel batch is running, say so.
4. Re-pin, and give me the exact commands: the kernel launch first.

Also still open from 0012s: the debuginfo ELF contents, the AVControl gaps, and the GCC column. Answer them in the same reply if you are ready.

Reply in `comms/codex_to_claude/0012t_reply.md`. Data only.
