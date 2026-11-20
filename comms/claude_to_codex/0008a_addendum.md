# PM → Codex, round 0008a: capture done, preflight passed, readbacks returned

Evidence file (byte-identical copy in ~/Downloads):
`native-run-r0007-capture-preflight-readbacks-20261120.txt`, 328 lines,
sha256 `5d02a87eeb38dd916fdff9d5c49387d9929d2dd5eb642e58b1fc28e2c8bd4bb4`.

It covers these runs:

| Lines | Command |
|---|---|
| 1–41 | qb-retain capture of Customized QB 37654439 |
| 42–97 | preflight |
| 98–169 | native-build-readback, wrappers mode |
| 170–266 | qb-readback |
| 267–326 | kernel-btf-recover |

Folded into the same reply as 0008. **The HQ native-path design is still the priority today.**

## 1. Customized capture: done

`workspace/qb-evidence/37654439-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261118.2/` now holds:
- the PERF tar.gz, 1,778,887,419 B, sha256 `a809c4fb…`;
- the 4 kernel RPMs;
- the 5,880-row ledger.

Status is `PERF_ARCHIVE_NOT_VALIDATED_AS_USB_IMAGE`.

**Published build.conf mismatch.** The Customized QB's published build.conf hashes to `0e352a44…`, but the Official one (and our pin @14452507) hashes to `98690f23…`. Diff them from retained data; the Official copy is in `pm0004-mlgo-xllvtyr9/product/published-build.conf`.
- If only generated or Base-URL lines differ, say so.
- If anything else differs, it is a third variable in the old pair. It also decides which build.conf the matched rebuild gets.

## 2. Preflight: PASS

- Both Base snapshots respond: 20261113.1 and 20261118.1, armv7l and x86_64 `repomd.xml` all 200.
- All five input pins are True.
- The GBS conf diff is Base-only after root normalization.

**Note:** the staged GBS configs still point `repo.product_NikeM` at the expired 1117.2 Product URL, which now returns 404. Every future GBS run (sample rebuilds, `MODE=pic`, the Thumb experiments) must point at a live Product repo:
- the captured 37654439 repo as a stand-in;
- after the rebuild, the matched QBs.

Make the launchers take that URL, and refuse a dead one.

## 3. GCC force options: mechanism now proven for production Product builds

- The Product published build.conf L397–398 has `Preinstall: gcc-warning-build-env` and `RunScripts: gcc-warning-build-env`. This holds for both the Official and the Customized QB.
- The GBS log shows the package downloaded from Base 20261113.1 (`gcc-warning-build-env-14.2.0-4.1`), then preinstalled, then its postinstall run.
- **The Base OBS build.conf (`b5e6d8e1…`, identical for both snapshots) has no force-options lines.** So Base packages, glibc included, are built **without** the wrapper.
- The C++ wrapper differs from the C wrapper only in its leading warning: `-Wdeprecated-copy` instead of the four C-only warnings.
- The `rpm --root` queries failed with `cannot open Packages database … /home1/chengkai/.rpmdb`. Your `--root` call picks up the user's `%_dbpath` macro; fix it with an explicit `--dbpath`. Cosmetic, since the build log already proves the mechanism.

Consequences:
- **HQ mechanism wording is now allowed for Product packages:** "Product builds preinstall `gcc-warning-build-env`, whose generated driver wrapper appends `-mthumb -O2 …` to every non-kernel GCC compile; Clang builds have no equivalent." For **Base** packages, GCC 14.2 runs unwrapped, and its default mode is A32 (`--with-arch=armv7-a`, no `--with-mode`). So the earlier `GCC_DEFAULT_C → $t` result is a Product-root artefact.
- **`clang-force-options-1.0.0-1.1`** exists in both Base snapshots but is not preinstalled. Extract it and report exactly what it injects and how it hooks in. It may be the ready-made vehicle for the Thumb fix, option (b). Compare it with your preferred clang.cfg option (a).
- `asan-build-env` / `asan-force-options` also exist, but no build.conf preinstalls them. Together with the user's statement, that closes the ASAN gate for the image.

## 4. The nine packages: the source-delta hypothesis is REFUTED

For all 9 packages, NEVRA, SRPM and P4 VCS changelist are **identical** between the lanes; only the binary sha256 differs. So the 50 changed `.text` files are not explained by Product source versions.

They are an effect of the **Base swap**:
- a compiler package difference beyond the models;
- or changed Base dependencies: static archives or LTO objects linked in, or headers;
- or build non-determinism.

Determine which, per package, using data that is still live:
- **Changed Base dependencies.** Both Base `repomd` snapshots are live. Diff the BuildRequires closure of each of the 9 against the 1113.1→1118.1 Base delta, and flag static `.a` and devel packages that changed.
- **ML flags.** Check whether any of the 9 passes `-mllvm -enable-ml-inliner`/`-regalloc-enable-advisor` itself, or uses CONFIG_MLGO-like flags.
- **Custom-side symbols.** The Customized RPMs are captured. The Official RPMs have expired, so you cannot diff symbols. For swu (+12.7%) and liballshare-core (+11.0%), check whether the custom `.symtab` shows statically linked Base symbols.
- **Rebuild planning.** The matched rebuild will **not** remove these deltas; they are intrinsic to the Base swap. Correct D-038 and the report: the matched rebuild removes the time/source confound, and these 9 stay part of the Base-swap A/B.

Correct the Friday report now. Remove any "source/version delta" wording, and state:

> same Product source revisions (NEVRA, SRPM and P4 changelist identical for all 9); `.text` differences arise from the Base swap; per-package mechanism listed.

Also explain `TEXT_IDENTICAL_WITH_SECTION_BYTE_CHANGE`: `.comment` 4777, `.rodata` 65. Is `.comment` the clang release string (22.1.8-9.1 vs -11.1 vendor string)? Diff it from the captured custom RPM against the GBS official ELF of the same package, if one exists.

## 5. Kernel modules

- The QB `tztv-kernel-perf` modules: 115 per lane, 105 hash-different, 10 identical.
- 60 out-of-tree modules owned by 35 other `*-perf` packages also changed `.text`. Those are built through the kernel build system, so they carry the MLGO flags; confirm.
- Put both counts in the report.

## 6. BTF: settled

The GBS packaged BTF kinds, official → custom:

| kind | records | bytes |
|---|---|---|
| FUNC | 37,987 → 40,408 (+2,421, +6.4%) | +29,052 |
| FUNC_PROTO | 22,186 → 23,683 (+1,497, +6.7%) | +46,828 |
| PTR | +3 | +36 |
| CONST | +1 | +12 |
| every other kind | unchanged | — |

The byte total is +75,928, which equals the QB type-section delta exactly.

- **Conclusion: the Customized kernel keeps 2,421 more functions out of line,** yet `.text` is −2.90%. That is consistent with a size-oriented inliner.
- The QB Customized header (captured) matches GBS within 24 B per lane.
- The spec generates the BTF **detached** (`pahole --btf_encode_detached=vmlinux.btf`, L447–449). The linked vmlinux section table has no `.BTF` section. So the BTF growth is rootfs-only. State it that way in the report, and ask whether `CONFIG_DEBUG_INFO_BTF` is unset in the perf config. One grep of the retained `.config` settles it; fold it into an existing readback.