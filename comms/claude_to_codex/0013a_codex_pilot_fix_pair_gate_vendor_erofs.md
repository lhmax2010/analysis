# 0013a • Pilot ran end to end but is not decision-ready; new pair accepted; vendor erofs-utils 1.8.10 found

Archive this evidence (three native runs: new-pair capture, AVControl pilot, reader-source):

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0012z-pilot-pair-reader-20261126.txt` | `7f052f1b43d0d9baaf573b4eb25abd6ea6d6e78e29caf3dd050f4aa0073df5b0` |

The kernel relaunch (`5a692bc`, `2afd47e3`, K0–K5) is starting now and holds the shared build lock overnight. **Nothing in this prompt may take the build lock or run GBS.**

## A. New QB pair: PM decision

Facts:

- Product sources match: `SOURCE_VCS_MATCH 5880/5880`. Of the RPMs, 138 are identical and 5742 differ.
- I decoded `REVIEW_ZLIB_BASE64` (sha `f8e02142…`). It holds four items:
  - `SHELVES` and `BASE_LIST`: unprovable, because there is no submission input;
  - `product_version`: Official `0825.10` vs Custom `0825.20`;
  - `quickbuild`: `19437567` vs `19437655`.
- Kernel vs the old pair:
  - uImage sizes are identical (Official 11,348,968; Custom 11,085,240);
  - zImage is −8 bytes on each side;
  - the RPMs differ slightly;
  - hashes and build IDs all differ.

**Decision:** accept 37777148 (Official) and 37777264 (Custom) as the current A/B pair, with the four review items recorded as publication metadata. This pair is the reference for the Thumb-2 QB board comparison.

The HQ kernel table already sent stays labelled with the old pair (37736448 and 37736427). Do not re-measure it. Add the new-pair kernel bytes as a separate row in `reports/weekly/2026-11-27/draft-data.md`.

## B. AVControl pilot (`pm0012-pilot.WRwYTx`): fix the harness, re-evaluate without rebuilding

Results: smoke gate PASS; T3 PASS in both lanes; every other gate is REVIEW. Most of these are harness or tool gaps, not compiler results. Fix them and **re-evaluate the existing batch outputs in place**. Do not rebuild.

1. **T1 (package lane).** The checker used host `/usr/bin/llvm-dis` from LLVM 18.1.3 on LLVM 22.1.8 bitcode.
   - Use the lane's own 22.1.8 tools from its build root.
   - Fail closed on any producer/reader version mismatch.
2. **T1 (default lane)** reports `effective -flto=0`.
   - Show whether the shipped Official AVControl is built with LTO, using its spec, its flags and the DWARF producer.
   - If Official is LTO and this lane is not, the lane is not representative. Say what the lane must change.
3. **T2.** Unknown bytes: default 441,362 and package 179,660.
   - Classify them from the unstripped linked output (`.symtab` mapping symbols `$a`/`$t`/`$d`) or from the debuginfo file.
   - If neither has mapping symbols, use the sum over the linked `.o` files.
   - Report ARM, Thumb and data bytes per lane, with `unknown = 0` as the pass condition.
4. **T4.** `abidiff` is unavailable.
   - Use the reviewed fallback, with 22.1.8 `llvm-readelf` against the Official binary:
     - the dynamic symbol table (name, type, binding, version, size);
     - `DT_NEEDED`;
     - SONAME;
     - `.dynamic` flags.
   - Report the result as `ABI_FALLBACK_PASS` or as the diff.
5. **T5.** Prove the test inventory from the spec (`%check`) and from CMake `add_test`/ctest.
   - If the package registers no tests, T5 is N/A, with the spec lines as evidence.
6. **T6.** The executable smoke is missing.
   - **Host part:** if `qemu-arm` is available, run the build root's `ld-linux-armhf.so.3 --list` on AVControl, so that every `DT_NEEDED` and relocation resolves. Also run a static interwork check with 22.1.8 `llvm-objdump`: no `BL` into a code span of the other state where a `BLX` or veneer is required.
   - **Board part:** deferred to the signed Thumb-2 QB image. The PERF image rejects unsigned binaries.
   - Report the result as `HOST_LOADER_PASS` + `BOARD_DEFERRED`.
7. **T7 (default lane).** All AVControl sources are unjoined, while the package lane has only `CMakeCXXCompilerId.cpp` unjoined.
   - Explain the join-key failure (`DW_AT_name` and `DW_AT_comp_dir` vs the compile commands) and fix it.
   - Exclude CMake compiler-ID probes by rule.
8. **Only two lanes printed** (default and package).
   - State where the third lane (the Official/ARM reference) is.
   - Print a three-column summary: file size, `.text`, ARM, Thumb and data bytes, and T1–T8, for reference, default and package.

**Pass rule for the pilot:** T1–T7 each PASS, or N/A with evidence. T8 must stay N/A with its reason printed.

When the pilot passes, the full A32 roster follows. Give that roster command now as well, gated on the pilot PASS. It must still use the build lock, so I can run it after the kernel run finishes.

## C. EROFS: use the vendor erofs-utils 1.8.10

Facts:

- The product repos carry `erofs-utils-1.8.10-0.x86_64.rpm`:
  - `TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261113.1`: `cec29e50…`;
  - `…_20261123.2`: `19878237…`.
- The source repo returns 404, so the SRPM is not available.
- The retained kernel tree confirms the vendor format:
  - `Z_EROFS_COMPRESSION_ZLIB = 4`, plus a `Z_EROFS_COMPRESSION_ZLIB_HW` entry;
  - the decompressor is `zlib_inflateInit2(-MAX_WBITS)`;
  - a header comment calls it "zlib-wrapped" and names `mkfs.erofs --gzip`;
  - the Kconfig text names NVT/Samsung Tizen TV images.
- `mic` and `image-configurations` are not the reader. Read `image-configurations` only if it states the `mkfs.erofs` options.

Route (replaces 0012z route 1):

1. Also probe the product x86_64 repos of the new pair (`20261125.1` and `.2`) and of the build that produced the images under test. Prefer the exact snapshot match, and print every candidate with its sha256.
2. Fetch one candidate, pinned by URL and sha256. Unpack it with `rpm2cpio` into the workspace (no root). Then print:
   - `ldd`, with any missing libraries;
   - `--version`;
   - the compression names it lists.
3. Verify it on all four partitions (Official and GCC × `pltf_t`/`prd`):
   - `fsck.erofs` is clean;
   - a full `--extract` into the workspace (print the free disk space first);
   - the file counts equal `dump.erofs`;
   - a byte check of a sample of files against the board copies (the board is on GCC 37564293).
4. Only if the binary cannot run on the server: fall back to a separate reviewed patch to our pinned 1.9.4 that maps id 4 to zlib inflate. The patch must follow the kernel decompressor exactly (raw `-MAX_WBITS` plus any header skip), not the comment.
5. Then run the deferred pilot image checks (image membership, ELF hash and ISA, image-wide A32 totals) and the image scan that feeds the full roster.

## D. Command shape

Give **one** pinned native command for B (re-evaluate) plus C (vendor reader and four-partition verification):

- two independent sections: a failure in one must not stop the other;
- no lock, no GBS, no sudo;
- it must be safe to run while the kernel job is running;
- compact output, one line per result, with any long data as a hash plus a zlib/base64 block.

Separately, give the gated full-roster command for after the kernel run.

Reply in `comms/codex_to_claude/0013a_reply.md`, commands first. Data only.
