# PM → Codex, round 0007: full section scan done, Thumb defaults answered, two 404s

Evidence file (byte-identical copy in ~/Downloads):
`native-run-r0006-fullscan-thumbprobe-20261119.txt`, 715 lines,
sha256 `b01a58a4fd42b43fdffa6782dc6a007bca48bad21f838f58af9ae759a61845d3`.

What the transcript contains:

| Lines | Run | Result |
|---|---|---|
| 1–15 | Kernel ISA diagnostic | done |
| 16–246 | Earlier diagnostics and thumb-causes, repeated | — |
| 247–263 | Kernel-only sections, repeated | — |
| 264–345 | **Full `mlgo-elf-sections --fetch`** | **DONE** |
| 346–367 | `perf-inner-tar official` | **404** |
| 369–408 | kernel-replay-readback | done |
| 423–471 | thumb-provenance | done |
| 472–485 | obs-glibc-buildlog | **404** |
| 486–512 | kernel-btf | **404** |
| 513–713 | **Fixed Thumb defaults probe** | **DONE** |

Archive the transcript. Then go through items 1–6 and answer each one with evidence. Challenge my reading wherever it is wrong.

## 1. Friday attribution: the full section scan (lines 279–345)

`SUMMARY` for the scan:
- TARGET_PACKAGES 1783.
- **USERSPACE_TEXT_IDENTICAL 4784 vs USERSPACE_TEXT_CHANGED 50.** So `.text` is byte-identical in 98.97% of the user-space ELFs compared.
- The 50 changed files sit in 9 packages, and all of them are `OUTSIDE_BASE_DELTA`.
- METADATA_ONLY_CANDIDATE 4715; OTHER_EXEC_CHANGED 45; ELF added 12 / removed 12.

The changed `.text` bytes total 18,909,078 → 20,288,252 (**+1,379,174 B, +7.29%**). Four packages account for 100% of the change:

| package | files | change (bytes) | change |
|---|---|---|---|
| org.tizen.tv.swu | 14 | +1,167,174 | +12.7% |
| liballshare-core | 5 | +134,540 | +11.0% |
| nagsam-mw | 15 | +68,170 | +1.6% |
| ug-hbbtv-efl | 11 | +9,418 | |
| gst-ffmpeg | 1 | −128 | |

Four more packages have changed `.text` content with the same size: connectivity-common-daemon, chromium-efl, key-manager-ta and ABC-test-apps.

My reading:
- The user-space compile flags carry no MLGO advisor flags. The compiler packages differ (9.1 vs 11.1), yet 4784 files have identical `.text`. So the compiler change produces no user-space codegen change.
- The 50 changed files are therefore most likely **source/version differences** between QB 37627297 and QB 37654439, not compiler effects. **Prove or refute this.** For each of the 9 packages, compare NEVRA, source revision and changelog between the two QB ledgers.

If the reading holds, the Friday statement becomes:
- **Kernel:** MLGO model change. Same source, flags and config; only the compiler package differs.
- **User space:** code unchanged in 4784/4834 ELFs (98.97%). The 50 remaining files are in 9 packages, each with its source delta named.
- **Board:** keep "whole-image A/B", qualified with this table. Do not claim more than the evidence supports.

Also explain three more things:
- **`.rodata` without code changes.** 111 files changed `.rodata`, some with no `.text` change at all (`OTHER_CHANGE_OR_UNEXPLAINED`, for example ABC-test-apps). Diff one sample: `__DATE__`/`__TIME__` stamps, a version string, or something else?
- **The `.comment` change** (4827 files). Is it only the compiler version string?
- **The kernel modules.** The scan reports KERNEL_MODULE_TEXT_CHANGED 60 and IDENTICAL 2, but there are 115 modules. Where are the other 53?

Update `reports/MLGO_Official_vs_Custom_20261120.md` with all of this. The report is due tomorrow (Fri 20 Nov).

## 2. Thumb defaults: the hypothesis is CONFIRMED by actual compile commands (lines 540–713)

All steps were run inside the official GBS-ROOT. The table shows the `-triple` each compile line resolves to and the mapping symbol found in the object:

| compile line | cc1 triple | mapping symbol |
|---|---|---|
| `armv7l-tizen-linux-gnueabi-clang -c` (with `/usr/bin/clang.cfg`, no `-m` flag) | `armv7-tizen-linux-gnueabi` | **`$a` (A32)** |
| same, `--no-default-config` | `armv7-tizen-linux-gnueabi` | `$a` |
| same + platform optflags | `thumbv8a-tizen-linux-gnueabi` | `$t` |
| **`gcc -c` (no flags)** | — | **`$t` (Thumb-2)** |
| Clang `.S` with `-Wa,-mimplicit-it=thumb` | — | `$t`, rc=0 |
| Clang `.S` with `-Wa,-mimplicit-it=never` (control) | — | rc=1, as expected |

**Conclusion.** Without `-mthumb`, Tizen **GCC 14.2 emits Thumb-2 but Tizen Clang 22.1.8 emits A32**. The shipped `clang.cfg` does not add `-mthumb`. So any package whose build system does not pass `$CFLAGS`/`$CXXFLAGS` to the compiler:
- was Thumb under GCC;
- is A32 under Clang.

This explains the 445 `GCC+Clang`-marker files out of the 609 (lines 434–444; 141.2 MB). It also explains why the ARM-predominant count went up after the switch to LLVM.

Remaining work for this item:

1. **Why GCC defaults to Thumb.** `gcc -v` shows `--with-arch=armv7-a` and no `--with-mode=thumb`. Is it a specs file, a Tizen patch, or a wrapper? The user is running a host-side read-only check now (`clang.cfg`, the gcc binary/wrapper, specs). Use its output. **`GCC_DEFAULT rc=1`** (the `-Q --help=target` query fails in the assembler) can stay a footnote; the object test is decisive.
2. **Per-package proof for the HQ answer.** Take 3–4 `GCC+Clang` packages from the sample plan (deviced, gst-plugins-dash, inference-engine-tflite, nodejs) and show from their real compile lines that `-mthumb` is absent.
   - Get the lines from the QB build log if one exists, otherwise from a GBS sample rebuild.
   - The user said vd-tree can download source to compile and verify. Build the sample launcher so that it fetches the exact QB source revision itself. SAMPLE_SOURCE/SAMPLE_REVISION must not depend on the user finding them.
3. **The fix, as one-change experiments, one variable each.** Design both and tell me which you prefer:
   - (a) `-mthumb` (or the `thumbv7`/`thumbv8a` default triple) in the Tizen `clang.cfg` for armv7l;
   - (b) per-package fixes, so the build systems honour CFLAGS.

   Also say which packages (a) could break: hand-written A32 inline asm or `.S` without `.arm`. Each experiment needs a size and code-memory measurement, then a KantSU2E on-target check following the one-change-per-experiment protocol. This is our biggest code-size and memory lever so far; it bears directly on the 1 GB goal.
4. **The `GCC`-only class: 157 files, 195.4 MB.** It includes the 4 bundled bpftrace LLVM 19 libraries proven prebuilt from the spec (134.7 MB). GCC defaults to Thumb, so a GCC-marked A32 file needs one of these: an explicit `-marm`, asm, or a prebuilt built elsewhere. Classify on that basis. qte-bm, Widevine, PlayReady, python3.5m and glibc fall here.

## 3. Kernel ISA: settled

- Both `.config` files: `# CONFIG_THUMB2_KERNEL is not set`, `CONFIG_ARM_THUMB=y`.
- `arch/arm/Makefile` line 152: `CFLAGS_ISA := $(call cc-option,-marm,)`.
- **The 609 holds no kernel files.** IMAGE_MODE_KERNEL_MEMBERSHIP is arm_predominant 609, loadable 5166, module_REL 180. Kernel ISA is one line in the HQ reply ("kernel built A32 by config"), not a row in the 609 table.

Three smaller kernel items:
- **The 302 `-mthumb` lines.** They carry no `-Wp,-MMD` and none of them also carries `-marm`. Identify them; my guess is cc-option probes, not object compiles. Low priority.
- **`KERNEL_ARGV_ISA ... []`.** Why does the retained argv have no ISA flags when the log contains 1884 `-marm`? Is the argv truncated?
- **Wording.** QB vs GBS: uImage, zImage and the BTF file are `SHA_DIFFERENT` with equal or near-equal sizes, and the module offsets are 512/576 B. The report must say "size-reproduced, not byte-reproduced" and give the likely reason (timestamps or build-id, signing). Do not claim more.

## 4. Two 404s: is the QB artifact gone?

- `perf-inner-tar official`: the outer `.tar.gz` under `PRV/builds/b658/19350658/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261117.2/...` returned 404.
- `kernel-btf`: the RPM under the same build path returned 404.
- The full scan fetched 1783 packages successfully just before. So the artifacts were removed or moved during the run, or the scan used another URL.

The user is running a HEAD check now. Tell me:
- whether retention deleted the Official QB artifacts;
- whether we still hold what Friday needs locally (your workdirs);
- whether the BTF decoder can run from the retained local RPMs. The GBS replay RPMs exist locally, but they are GBS RPMs, not QB ones.

Also explain **"ASAN"** in the job name `TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE`. If the image is AddressSanitizer-instrumented, board performance and memory numbers are invalid. The optflags show no `-fsanitize`, but confirm it from the QB build config.

## 5. glibc OBS 404

`glibc-2.40-1.111.armv7l.rpm` is no longer in the OBS build results; the package has been rebuilt since. Choose and justify one of these:
- the OBS build history (`_history`, or the old build log by job);
- the 20261113.1 snapshot RPM plus a GBS glibc sample rebuild.

glibc is GCC-only. HQ needs its cause from compile commands: `-marm` in the spec, `.S`, or `sysdeps` asm.

## 6. Deliverables for your next reply

- Commit the evidence.
- Friday report: the section-scan table and the 9-package source-delta check.
- The Thumb defaults finding written into the ledger, with the per-class cause table filled where proven.
- Sample-rebuild launcher(s) that fetch exact source.
- The clang.cfg experiment design.
- Fixes for the BTF decoder and glibc readers, or a statement of why they are moot.
- Answers on the 404s and on ASAN.