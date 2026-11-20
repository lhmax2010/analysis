# PM → Codex, round 0007a: QB 1117.2 expired, rebuild decision, gcc wrapper

Evidence file (in ~/Downloads, copied from the user's terminal paste): `native-run-r0007-clangcfg-gccwrapper-qb404-20261120.txt`. Commit it with its sha256.

## 1. QB artifacts are gone

All three paths return HTTP 404, including the build root `.../PRV/builds/b658/19350658/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261117.2/` itself. Retention removed the 1117.2 artifacts about 2–3 days after the build. Answer each of these:

- **Friday report.** Confirm that the report can be completed from data we already hold: `packages.jsonl`, `sections.jsonl`, the image-compare ledgers and the GBS replays in the native workdirs. List anything Friday still needs from QB.
- **Customized QB 37654439.** Is it still alive? Give the user a HEAD-check command. If it is still up, decide what must be captured from it into the vd-tree workspace now. At minimum: the PERF image tar.gz and the kernel RPMs.
- **Rule from now on.** When a QB we depend on completes, capture its identity ledger and the PERF image into `vd-tree/workspace` straight away. Add this rule to `decisions/DECISIONS.md`.

## 2. Rebuild decision: I need your agreement or your objection

The user must rebuild the KantSU2E image. The question is whether to keep the ltoexp manifest or use another one.

**My recommendation.** Keep the exact 1117 inputs:

- `build.conf` `TIZEN_KantSU2E_Clang_build.conf@14452507`;
- Base list `tizen10.0_base_urls_1114_noprelink.txt`;
- shelf list `tizen10.0_shelves_1116_ffmpeg_seek_ltoexp2.txt` (930 shelves).

Reasons:

- **One change per experiment.** All verified evidence is tied to this configuration: the 609 ARM-predominant files on the "LTO and PIE image", the section scans, the LTO coverage. Changing the manifest would mix a second variable into the MLGO A/B and the Thumb experiments.
- **Remove the source confound.** A rebuild picks up newer Product sources anyway. So build **both MLGO lanes at the same time from the same Product state**: one QB with the Official Base 1113.1 and one with the Customized Base 1118.1. Everything else stays identical. That removes the 9-package source delta from the board A/B.

Verify these before the user starts:

1. The two Base snapshot URLs (20261113.1 and 20261118.1) are still served.
2. The `gbs_vd_llvm_11.16_qb37627297.conf` vs `gbs_vd_llvm_qb37627297_mlgo_20261118.1.conf` pair differs **only** in the Base URL. Print the diff.
3. **ASAN.** The QB job template is named `TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE`. Confirm from the build config or kickstart that AddressSanitizer is not enabled in the PERF image. If it is, the board performance and memory numbers are invalid.
4. Whether the "other" manifest the user may mean (the 932-entry seek-only control?) has anything the next board round needs. If you know of a newer list carrying needed fixes, say what it changes.

Reply with:

- **AGREE**, or a concrete alternative with reasons;
- the exact list of QB inputs per lane;
- a capture-and-ledger launcher to run right after each QB completes.

## 3. The GCC "Thumb by default" claim is withdrawn until the wrapper is read

Inside the official GBS build root:

- `/usr/bin/gcc` and `/usr/bin/armv7l-tizen-linux-gnueabi-gcc` are **1684-byte POSIX shell scripts** with mtime Nov 19 15:02. That is when the build root was created, not the Nov 12 RPM mtime that `clang.cfg` has.
- `/emul/usr/bin/gcc` is the real accelerator binary.
- No GCC `specs` file mentions thumb or marm.

Our probe does not create this file: its wrapper lives in `$PWD/.pm-thumb-compiler`. So the build environment generates the script.

Consequences:

- The `GCC_DEFAULT_C → $t` result may come from this wrapper injecting `-mthumb`, not from GCC itself.
- The user is printing the script now. Use its content to state the mechanism exactly. If it injects `-mthumb`, the HQ wording becomes: "the Tizen build environment forces Thumb for GCC via a compiler wrapper; Clang has no equivalent (clang.cfg = `-target armv7l-tizen-linux-gnueabi`, `-resource-dir`, `-D_FILE_OFFSET_BITS=64`), so builds that drop CFLAGS become A32 under Clang".
- Also find out which package or build script creates the wrapper (the build-root setup in GBS/OBS `build`?).
- The fix design in 0007 §2.3 may then simply mirror that mechanism for Clang.

**Confirmed regardless of the wrapper:** `clang.cfg` contains no `-mthumb`, and Clang without `-mthumb` emits A32.
