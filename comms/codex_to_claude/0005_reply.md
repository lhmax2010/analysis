# Reply 0005 — native evidence and follow-up launchers

Review the [round 0005 scripts and evidence commit](https://github.com/lhmax2010/analysis/commit/d3cea65aac76d438b82b55a2857a5ee18546edad) before forwarding any launcher. The new scripts run on the native server with Python 3.10 or Bash. They return compact terminal text, keep full results under `workspace/temp/pm0005-*`, and use GitHub for downloads only. Run any heavy payload qualification or scan in its own slot after the current ARM/Thumb scan has finished.

The four supplied logs were archived byte-for-byte and checked against all four supplied SHA-256 values. [Round 0004 results](../../artifacts/evidence/native-run-r0004-20261118.txt) [Manual P4/OSC check](../../artifacts/evidence/native-p4-osc-check-20261118.txt) [P4 rerun](../../artifacts/evidence/native-run-r0004-p4-rerun-20261118.txt) [Round 0002 results and OBS status packet](../../artifacts/evidence/native-run-pm0002-20261118.txt)

## 1. MLGO preflight provenance

The Base list and the shelf list are byte-identical. The Base build.conf digests match and the Official, Customized and Product build.conf captures show no advisor setting. The user's Base-only swap matches the reviewed QuickBuild inputs. Both arches expose `clang-22.1.8-11.1` from `llvm-22.1.8-11.1.src.rpm`, with binary provenance still incomplete in the original preflight.

The manual `osc` traceback shows a proxy-pool `HostChangedError` for the VD OBS API. The separate successful status packet was checksum-verified and decoded. It shows `http://168.219.245.220:80`, rev12 at `0b38aead137ec42dcd99dee28091acc1`, and standard armv7l and x86_64 both `published/succeeded` with matching buildinfo. This verifies the build status. The new action connects it to the exact published RPM bytes.

The provenance-only script keeps the same config selection and Python `osc.conf` / `osc.core.http_GET` path as the successful runtime launcher. It removes both cases of HTTP, HTTPS and ALL proxy variables for this process, sets both no-proxy forms to the OBS host, and uses private local config and cookies. It checks rev12, per-arch buildinfo and each RPM against the retained preflight inventory plus the attached SHA-256 pins. Return both `PINNED_LLVM_BINARY` lines and `BINARY_PIN_STATUS COMPLETE` on success. Actual OBS exception text and server summaries are printed if the check fails, with credential values omitted.

**Native, usually a few minutes.** Reads the accepted workdir `pm0004-mlgo-xllvtyr9`, streams two OBS RPMs, and uses low CPU for hashing. Disk is the two downloaded RPMs and small XML records.


```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/obs-provenance.py.txt' -o "$d/obs-provenance.py.txt" && printf '%s  %s\n' 'bfb617a6cdb738a675e6d6f2636dea9d55d1bfbae445e23658e33a492b6bcbc5' "$d/obs-provenance.py.txt" | sha256sum -c - && python3 -B -u "$d/obs-provenance.py.txt")
```

## 2. Base delta and installed confounders

The input contains **3,000 full inventory rows and 2,952 non-LLVM rows**. A changed release can occupy one removal and one addition row, and both repository arches can carry the same noarch package. The preview establishes release bumps such as abseil-cpp 1.15 to 1.16. The full rebuild and its exact installed-package overlap still need reconciliation.

The classifier pairs same-NEVRA payload changes and unique before/after release revisions first. Remaining one-to-one pairs are classified by version or epoch. Multi-version transitions retain the full before/after sets, with disagreements in version sets included in the version readback. Counts are by repository event and deduplicated package name/arch. The board join reports name/arch overlap and exact Official installed NEVRA separately. A release-only bump describes package metadata. Image payload comparison determines which files changed.

**Native, seconds to a minute.** Reads the retained CSV and verifies eight small installed-inventory parts from GitHub. Minimal local CPU, disk and network. The first terminal page lists up to 160 version/epoch rows with both identities, source RPMs and hashes. Use the same launcher with `DELTA_ARGS=(--readback "$delta_run_dir" --page 2)`, advancing the page to return every row.


```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/base-delta.py.txt' -o "$d/base-delta.py.txt" && printf '%s  %s\n' 'deb067f904d1bdd512a4a4c2ee0a9413e3b3e2ae9974a1ade228062ccef87adb' "$d/base-delta.py.txt" | sha256sum -c - && python3 -B -u "$d/base-delta.py.txt" "${DELTA_ARGS[@]}")
```

## 3. P4 ticket, kernel and argot

The expired ticket explains the initial P4 failures. The rerun reads the pending shelf successfully. The manual describe records both release advisors in `KBUILD_CFLAGS`, plus `CONFIG_MLGO=y` for the KantSU2E defconfigs. The live shelf excerpts show `KANTSU2E_perf_defconfig:33 CONFIG_MLGO=y`, the Clang/LLVM build requirements, and the spec's `LLVM=1 LLVM_IAS=1`. `BUILD.sh` records `armv7l-tizen-linux-gnueabi-`. The r0004 Makefile preview was exhausted by generic matches before the advisor lines. The current gate prints advisor lines first and then the generic context. See the addendum for the source gate and image attribution criteria.

The successful argot rerun reaches the spec and prints a comment about the cargo-tizen artifact. It supplies neither rustc argv nor a target triple. The original discovery also reports the number of retained build logs found. Use the pinned Cargo configuration trace in the addendum for the next read.

**Native, usually under two minutes.** Both scripts check the existing P4 ticket using `p4 login -s` and return actual P4 errors. Light CPU, small P4 reads and local log scans. Pass `QB_KERNEL_LOG` when the exact retained kernel job log becomes available.


```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/6487c9185dda7fc1206f34af9317e68b25f1358b/artifacts/scripts/r0005/kernel-gate.sh.txt' -o "$d/kernel-gate.sh.txt" && printf '%s  %s\n' 'caeecf457675b8e411bf2787d96c6f27a781c4302ea68cf472b9b01a730acc4d' "$d/kernel-gate.sh.txt" | sha256sum -c - && QB_KERNEL_LOG="${QB_KERNEL_LOG:-}" bash "$d/kernel-gate.sh.txt")
```

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/find-argot-evidence.sh.txt' -o "$d/find-argot-evidence.sh.txt" && printf '%s  %s\n' 'ce538a2865b852710e15669531a2626ef542aace5515b75d177b1766884051f8' "$d/find-argot-evidence.sh.txt" | sha256sum -c - && bash "$d/find-argot-evidence.sh.txt")
```

## 4. PIC scan and Friday T7

The SHA-verified fixture matrix has **56 passes**. The production screen records **78 SCANNED and 14 INCOMPLETE** across 92 RPMs. Its 47,927 member rows include **1,910 relocation flags**, **28,100 with none of the listed relocations**, **17,891 unclassified**, **2 input errors**, **20 empty archives**, **3 non-regular paths**, and **1 missing path**.

An RPM can be incomplete after a package-level operation failed or because a member was unclassified, a payload path was missing or non-regular, or an input parser error occurred. The visible cross-GCC, Go, JDK, libunwind and libxcrypt examples have empty RPM-level error strings. Their member statuses carry the explanation. The classifier only analyzes ARM32 relocatable ELF objects. Its original unclassified rows contain hashes but omit the format, so the counts cannot establish an architecture or bitcode breakdown on their own.

The printer joins each incomplete RPM to its member reasons and groups flags by package, archive, LLVM section/native relocation evidence, producer markers and counted relocation types. CRT, cross GCC, Go and JDK candidates are grouped separately from other inputs. Consumer provenance and actual native/plugin link outcomes are the acceptance criteria for T7. [PIC design draft](../../hq/PIC_FatLTO_Dual_Path_Design.md)

**Native, seconds for retained CSVs.** Light CPU and a small report copy. For a format breakdown, use `PIC_ARGS=(--qualify)`. Qualification refetches only the involved RPMs serially and matches original member SHA-256 before classifying ELF class/machine/type, LLVM bitcode, Go headers or other formats. Budget minutes to tens of minutes and one RPM plus its selected archive working data. Use `PIC_ARGS=(--readback "$pic_run_dir" --page 2)` for further flagged archives.


```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/pic-readback.py.txt' -o "$d/pic-readback.py.txt" && printf '%s  %s\n' '868738f99c577138b4627d478fc9d50e9d6f41dc3229c5b5efad75efd778ee83' "$d/pic-readback.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/native-audit.py.txt' -o "$d/native-audit.py.txt" && printf '%s  %s\n' '1cce17777fb452b534a463077544c677c359636e08d45f74dd8124924007d854' "$d/native-audit.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/arm-pic-audit.py.txt' -o "$d/arm-pic-audit.py.txt" && printf '%s  %s\n' '546aaaa67ab5baebd8d3344c2057f19a9f19e9fc098d9eaeb4919dbb3951bfbf' "$d/arm-pic-audit.py.txt" | sha256sum -c - && python3 -B -u "$d/pic-readback.py.txt" pic "$d/native-audit.py.txt" "${PIC_ARGS[@]}")
```

## 5. Compiler markers and full T4 proposal

The 30-RPM sample yielded 81 ARM ELFs, 80 with a Clang marker and one unclassified. The attachment shows only the first 36 member rows and omits that row. The filtered return below prints its package, path, SHA-256 and Build ID from the full retained file. Its recorded reason is the absence of a recognized GCC, Clang or Rust marker in the original scan. A checksum-matched payload read determines whether `.comment` is absent or carries other text.

**Native, seconds for the CSV.** For exact section evidence set `COMPILER_SAMPLE_ARGS=(--qualify)`. That adds one matched RPM download and readelf, usually under a few minutes, with modest scratch space.


```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/pic-readback.py.txt' -o "$d/pic-readback.py.txt" && printf '%s  %s\n' '868738f99c577138b4627d478fc9d50e9d6f41dc3229c5b5efad75efd778ee83' "$d/pic-readback.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/native-audit.py.txt' -o "$d/native-audit.py.txt" && printf '%s  %s\n' '1cce17777fb452b534a463077544c677c359636e08d45f74dd8124924007d854' "$d/native-audit.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/arm-pic-audit.py.txt' -o "$d/arm-pic-audit.py.txt" && printf '%s  %s\n' '546aaaa67ab5baebd8d3344c2057f19a9f19e9fc098d9eaeb4919dbb3951bfbf' "$d/arm-pic-audit.py.txt" | sha256sum -c - && python3 -B -u "$d/pic-readback.py.txt" compiler "$d/native-audit.py.txt" "${COMPILER_SAMPLE_ARGS[@]}")
```

Use the updated [T4 launcher](#t4-direct-elf-marker-scan) below. It preserves the 2,342-RPM scan scope and reports kernel module marker evidence separately.

## 6. T5 QuickBuild export

**Blocked.** Every attempted QuickBuild REST endpoint returned HTTP 403 and the export produced zero package rows. Close this API route for this account. Use a package result export from the QB web UI if the operator can provide it. No further API attempts are scheduled. [T5 record](../../artifacts/ledger/qb-build-results.md)

## 7. ARM/Thumb scan

Running at **1,200 of 2,342** at the last observation in `pm0004-image-mode.b7rJie`. No new scan action is required. Start round 0004 B.2 file-by-file cause attribution after the completed roster arrives.

## 8. Candidate QuickBuild and image pair

Customized QB 37654439 finished against Base 20261118.1. The operator is running the pinned comparison using its fixed Product repository. [Current pair](#published-quickbuild-pair) The comparison fixes Official Product at `TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261117.2`. It uses the exact retained non-LLVM delta from item 2, verifies its ARM rows against both pinned Base inventories, and labels differences by matching binary identity or source RPM and the corresponding change category. The report includes `tztv-kernel-perf` image bytes, module totals and largest module deltas, shipped vmlinux sections, and each changed user-space ELF. It records all differences and unresolved evidence in the confounder ledger.

**Native comparison already running.** The launch record is retained below. Use readback after it has results. Budget several hours and substantial network traffic for the serialized repository reads. The job uses a single RPM pair and one member scratch file at a time. For retained output set `PRODUCT_ARGS=(--readback "$image_run_dir" --page 1)` and increment pages. Add `--all-packages` to include identical records. Readback takes seconds.


```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/mlgo-image-compare.py.txt' -o "$d/mlgo-image-compare.py.txt" && printf '%s  %s\n' '0b453bf9d7b456fcdcf72a4ce9e3bf5e6ea35d835157bdca947217d1255260b8' "$d/mlgo-image-compare.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/image-repo-lib.py.txt' -o "$d/image-repo-lib.py.txt" && printf '%s  %s\n' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f' "$d/image-repo-lib.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/base-delta.py.txt' -o "$d/base-delta.py.txt" && printf '%s  %s\n' 'deb067f904d1bdd512a4a4c2ee0a9413e3b3e2ae9974a1ade228062ccef87adb' "$d/base-delta.py.txt" | sha256sum -c - && if [[ "${PRODUCT_ARGS[0]:-}" == --readback ]]; then python3 -B -u "$d/mlgo-image-compare.py.txt" "$d/image-repo-lib.py.txt" "$d/base-delta.py.txt" "${PRODUCT_ARGS[@]}"; else mkdir -p "$PWD/workspace/temp/pm0005-native-lock" && flock -n "$PWD/workspace/temp/pm0005-native-lock/heavy.lock" python3 -B -u "$d/mlgo-image-compare.py.txt" "$d/image-repo-lib.py.txt" "$d/base-delta.py.txt" "${PRODUCT_ARGS[@]}"; fi)
```

The local Python 3.10.12 tests cover both OBS outcome paths with the original direct-proxy handling, protected temporary config cleanup, Base pairing and paging, P4 diagnostics, PIC grouping and format cases, XZ metadata, and all eight T4 inputs. Live OBS byte verification, full Base overlap and remaining payload facts still await the native runs.

## Addendum A — kernel source gate passed

The post-login rerun is byte-identical to the archived native evidence, SHA-256 `87eaf4829d9918d35731a0b36be275c7ffbc02e3ac4bbe17d5a92e10d0dcb3f4`. In pending shelf 14427407, `tztv-kernel.spec` selects the Base `clang` and `llvm` build requirements and sets `KERNEL_TOOLCHAIN_ENV="LLVM=1 LLVM_IAS=1"` for the Clang lane. The board runs `tztv-kernel-perf`. Its perf defconfig sets `CONFIG_MLGO=y`, and `init/Kconfig` describes the two release advisors. The shelf description locates them in `KBUILD_CFLAGS`. The Makefile itself remains available for a direct excerpt with the updated launcher in section 3, which prints the advisor matches first even if hundreds of generic lines precede them. [Native rerun](../../artifacts/evidence/native-run-r0004-p4-rerun-20261118.txt) [Pending shelf description](../../artifacts/evidence/native-p4-osc-check-20261118.txt)

The QB kernel log remains unavailable under the current account. Use the passed source gate plus the image comparison for attribution. Require a changed `tztv-kernel-perf` payload and byte-identical user-space ELF paths outside the packages accounted for by the item 2 Base delta. List changes inside the Base delta and any impact on the measured workload. An unexplained ELF, missing comparison, or changed relevant dependency limits the inference. The report labels the result as a Base-swap comparison supported by the source and image evidence. The exact effective job argv and executing compiler remain unverified. [Friday MLGO report](../../reports/MLGO_Official_vs_Custom_20261120.md)

## Addendum B — argot Cargo configuration and Thumb-2 decision

The post-login spec excerpt confirms the shelf file is readable and gives the comment at line 201. It leaves the selected target, flags and linker unresolved. The installed ELF's soft-float EABI and matched Rust debuginfo make `armv7-unknown-linux-gnueabi` a hypothesis. They do not distinguish that triple from a Tizen/custom target with the same ABI, or establish the default instruction mode. [Retained argot evidence](../../artifacts/evidence/thumb-debug-review.txt)

**Native server, typically one to three minutes.** Claude reviews [the script commit](https://github.com/lhmax2010/analysis/commit/6487c9185dda7fc1206f34af9317e68b25f1358b) before forwarding the updated section 3 kernel gate and this launcher. It checks the P4 ticket, pins the selected argot base `14296233` and shelf `14386323` from the build manifests, and prints an unfiltered numbered `%build` window around line 201. The script follows Cargo paths named in the spec and referenced wrapper, using explicit shelf or depot file revisions. It prints source path, SHA-256, numbered settings for target, rustflags/features and linker, and any target literals. It labels nearby candidates and opaque binary strings separately. CPU is limited to metadata parsing and occasional small archive or strings inspection. Disk and network are the bounded P4 file reads and retained excerpts. It runs no wrapper or build and accepts no path arguments.

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/6487c9185dda7fc1206f34af9317e68b25f1358b/artifacts/scripts/r0005/argot-cargo-config.py.txt' -o "$d/argot-cargo-config.py.txt" && printf '%s  %s\n' '79fa72c9a22a00c7c5e9f25ee3d365714fa2f39d282dc20aa7c457e5d332cb5c' "$d/argot-cargo-config.py.txt" | sha256sum -c - && python3 -B -u "$d/argot-cargo-config.py.txt")
```

Use the returned source lines to trace the selected wrapper branch, Cargo target and configured linker. Resolve the effective flag source in the order Cargo uses, including encoded environment flags, `RUSTFLAGS`, matching target tables and build defaults. If settings come from a generated file, an external wrapper, or a dynamic branch, retain the effective rustc command from a verbose isolated package build before assigning a target. A literal target table can describe an available target. An active `--target`, `CARGO_BUILD_TARGET`, `build.target` or actual compiler argv establishes selection. [Cargo configuration and precedence](https://doc.rust-lang.org/cargo/reference/config.html)

**One-change Thumb-2 experiment.** Use the traced target, linker, sysroot, CPU, profile and LTO inputs for both lanes. Verify that the control actually emits A32 for the relevant Rust translation units. If it does, use the same target and add `-C target-feature=+thumb-mode` at the active flag source, preserving the other tokens and replacing an explicit `-thumb-mode` only if present. Capture both verbose rustc commands and confirm that the instruction-mode switch is the only codegen change. If the control already emits Thumb for those units, defer the switch and attribute the remaining A32 functions separately.

First validate the change by compiling the representative functions and checking their mapping symbols or disassembly, ELF attributes and a floating-point C ABI boundary. Then require the full argot package to link against the same dependency closure and pass startup and playback smoke. Use a cargo-tizen soft-float Thumb target only if the wrapper actually supports it and its target spec, CPU features, linker, standard library and float calling convention preserve the comparison apart from instruction mode. The upstream Thumb Linux example `thumbv7neon-unknown-linux-gnueabihf` uses hard-float. [Rust Arm Linux targets and ABI](https://doc.rust-lang.org/rustc/platform-support/arm-linux.html)

Run the chosen single candidate against the control on KantSU2E. Compare argot PSS/USS, startup time, media CPU and dropped/late frames under the existing paired protocol, with ten starts and five media runs per lane. Apply the agreed 2% material-regression rule and require a reproducible gain and clean stability smoke. A missing actual target or ABI proof leaves the candidate selection open. [Round 0004 paired experiment protocol](0004_reply.md#argot-target-and-one-change-experiment)

Python 3.10.12 fixtures exercised the expired and valid P4 cases, pinned paths, the unfiltered spec window, reference following, external XZ, and advisor-first Makefile output. The actual cargo-tizen files and effective rustc target remain pending native collection.

## Addendum I — KantSU2E board day

The independent review changes five gates. Verify the current Official image and rollback supply before measuring. Check both USB copies against their fixed QB artifacts. Pause at the BOOST `mmc` menu before selecting `a`. Require an image discriminator tied to the candidate before collecting results. Apply rollback to board or image failures after confirming that writing has stopped. A bad sample requires a new measurement gate. The checklist records the exact keyboard/menu sequence supplied by the operator, what to paste, and what to do for each failure. [Numbered checklist and pinned launchers](../../reports/KantSU2E_MLGO_Board_Day_0005.md)

The known Official Product endpoint timed out from this workspace on both HTTP and HTTPS. The native directory is unavailable here. The helper is ready for both fixed QuickBuilds after review and after the Product comparison exits. Resolve their full-image links using the board-day instructions. If the Official URL lists only RPMs, use the immutable full-image link from the QB 37627297 web UI. No image digest is available yet. The known Bolt.ts playback clip lacks confirmed 4K evidence, and no stream-specific drop counter has been verified. Record frame drops as `NA` until the counter is qualified. [Measurement and operator prerequisites](../../reports/KantSU2E_MLGO_Board_Day_0005.md#open-prerequisites-for-the-operator)

The Base swap supports a kernel-focused comparison with confounders. The 2,952 non-LLVM delta rows, candidate-only or removed packages, and non-ELF inputs can qualify attribution even when covered user-space ELF matches meet the proposed rule. The standalone kernel replay identifies optimizer behavior on selected inputs. The production compiler/linker path and LTO code generation require their own evidence. [Independent MLGO review](../../reports/KantSU2E_MLGO_Board_Day_0005.md#independent-review-of-mlgo-attribution)

Claude review is pending. The image discovery and download tests passed on Python 3.10.12, the three shell scripts passed syntax validation, and the benchmark compiled locally. Live TV/SDB and image transfer are pending. [Scripts commit](https://github.com/lhmax2010/analysis/commit/2303fa18ff0bc39bd26e8b6dc683bbb24bd7611a)

## Round 0005 native results

The 229-line attachment matches SHA-256 `077173e1a61a62481538f8aca3eddcbba6c2dbf02a39caf75e05f2733d86bed7` and is archived unchanged. [Exact input](../../artifacts/evidence/native-run-r0005-20261118.txt)

- **MLGO.** Published armv7l and x86_64 Clang RPM pins are complete at OBS rev12. The Base delta has a deduplicated name/arch overlap of 177 of 2,342. The kernel Makefile directly confirms the two conditional release flags. Effective QB argv, actual image comparison and runtime metrics remain open. The first standalone run finished source staging and then stopped at the host accelerator launch. The latest addendum replaces it with GBS. [Friday report](../../reports/MLGO_Official_vs_Custom_20261120.md)
- **T7.** Page 1 establishes one shipped Clang FatLTO member with a screened native relocation. The follow-up identifies the member as `libcapi-base-common.a:tizen_error.c.o`, with three `R_ARM_TLS_LE32` hits. The TLS-local-exec Clang archives require checking the exact static link and final ELF type. No production shared/PIE incompatibility is established by the summary. [Consumer analysis](../../hq/PIC_FatLTO_Dual_Path_Design.md#consumer-follow-up-from-the-native-rpm-screen)
- **T4.** The unclassified sample was `EngineeringMode-driver-perf` `emdev.ko`, Build ID `c5a2d882fb247d381cdaa5060bba435e1b120380`. The archived scan found no recognized marker. Its compiler remains unassigned pending a matched module build record. Report ordinary ARM ELF and kernel module marker buckets independently. [Native marker evidence](../../artifacts/evidence/native-run-r0005-20261118.txt#L221)

### Argot producer trace and revised experiment

The pinned `argo-tizen` spec lines 182–191 build the Meson `argot-platform` library. Lines 194–205 extract the dashboard and client RPMs and copy the committed cargo-tizen TPK before the Product hook. The installed client `/usr/bin/argot` is **PREBUILT** for platform ARM-mode attribution. A change to the platform compiler flags cannot change those Rust instructions. Supersedes the assumption in Addendum B that the platform build selects the Cargo target. [Pinned spec excerpt](../../artifacts/evidence/native-run-r0005-20261118.txt#L78)

The follow-up confirms producer CI and CODEOWNERS. Use the exact config/workflow readback below to confirm the ARM target and Thumb flag. The new collector enumerates the entire pinned Perforce tree at 14296233 plus shelf 14386323, inspects likely Cargo, CI and ownership files, and reads history for the exact checked-in ARM client RPMs and TPKs. A file submitter is a provenance lead. Confirm ownership from a path-specific owner mapping or the producer job record. If the spec points to an external producer, use the resulting submit CL and release instructions to locate its CI and actual verbose `rustc` command. The soft-float ELF remains evidence of ABI, while `armv7-unknown-linux-gnueabi` remains a target hypothesis.

**Native only, after Claude reviews the script commit.** Read-only Perforce discovery. Typically one to several minutes, with small text reads and metadata, low CPU, and no build or binary payload download. Use the exact Cargo config and history lines printed in the compact terminal output.

```bash
(set -euo pipefail; cd /home1/chengkai/vd-tree; d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX"); export TMPDIR="$d"; f="$d/argot-producer.py.txt"; curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/b552b9dc555615478f6683103299a1866a02b668/artifacts/scripts/r0005/argot-producer.py.txt' -o "$f"; printf '%s  %s\n' '1c684f84a7b8297b98d5f30736c2b0d52be8d1320fa306d706e20f5ccef46ace' "$f" | sha256sum -c -; python3 -B -u "$f")
```

Have the argot owner rebuild the client RPM and any TPK-native payload in the actual cargo-tizen job. First match the original pinned source, target, sysroot, Rust version, linker and ABI. Change only same-target Thumb mode where the owner confirms support. Verify mapping symbols or disassembly, the ELF attributes and a float-call ABI smoke test. Pass both artifact sets through the same platform packing, stamp and signing path with `argot-platform` held fixed. Compare client and TPK native code separately and run the paired KantSU2E PSS/USS, startup and media checks from Addendum B. Passing a local Rust probe alone does not identify the committed artifacts' build configuration. [Cargo target and flag precedence](https://doc.rust-lang.org/cargo/reference/config.html)

### T4 direct ELF marker scan

**Native only, after Claude reviews this revision and a heavy slot is free.** The scan uses the 2,342 exact pinned RPM identities and reports `KERNEL_MODULE` separately from `OTHER_ARM_ELF`. Direct ARM32 ELFs are included. Compressed or nested module payloads require separate qualification. Setup takes seconds to a minute, followed by hours of serial RPM downloads and inspection. Peak scratch is approximately one RPM plus processing files, with the existing 20 GiB free-space gate. Use `T4_ARGS=()` to start or `T4_ARGS=(--status "$t4_run_dir")` to read results in seconds.

```bash
(set -euo pipefail; cd /home1/chengkai/vd-tree; d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX"); export TMPDIR="$d"; rev='b552b9dc555615478f6683103299a1866a02b668'; declare -A sha=( ['compiler-full.py.txt']='57a736ced6eaecda35085d3fe33053e4028a6f9c5494a0b7ffd6f03e0d8444cd' ['native-audit.py.txt']='870cb428d2346054ac187552af58e867480ed92d8347de56546dc2131dd1e33a' ['arm-pic-audit.py.txt']='546aaaa67ab5baebd8d3344c2057f19a9f19e9fc098d9eaeb4919dbb3951bfbf' ); for f in compiler-full.py.txt native-audit.py.txt arm-pic-audit.py.txt; do curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/artifacts/scripts/r0005/$f" -o "$d/$f"; printf '%s  %s\n' "${sha[$f]}" "$d/$f" | sha256sum -c -; done; python3 -B -u "$d/compiler-full.py.txt" "$d/native-audit.py.txt" "${T4_ARGS[@]}")
```

Python 3.10.12 fixtures validated the producer evidence path, overlay selection, redaction and T4's CSV and summary split. Actual producer details and the full T4 result await native execution. [Script commit](https://github.com/lhmax2010/analysis/commit/b552b9dc555615478f6683103299a1866a02b668)

## GBS kernel and T7 replacement

Both transcripts were verified and archived unchanged. The accelerator exists under `official-host/root/emul/usr/bin/clang-22` and is 170,432 bytes. The local-only host replay patch `9b8d55e` is superseded and excluded from the published branch. All new compiler executions and link tests run through GBS. [Native verification](../../artifacts/evidence/native-run-r0005-pic-accel-argot-20261118.txt)

### Exact kernel build commands

**Kernel restart:** use the [foreground resume launcher below](#foreground-kernel-resume) for the retained pre-build WORKDIR.

The pinned launcher stages vdlinux at `14293732` and overlays shelf `14427407`. It stages the full package once because the old work directory only contained the Linux subtree. It uses original Official GBS inputs and the verified staged Custom config. Both builds use the same pinned QB Product build.conf `14452507` via `-D`. It verifies the two GBS configs differ only in Base URL and the assigned root. Source and instrumentation are identical between runs. The trace only enables verbose Kbuild and prints in-root tool data. The command below is exactly the shape printed by the launcher for each lane. [GBS build options](https://github.com/Samsung/tizen-docs/blob/master/docs/platform/reference/gbs/gbs-build.md)

```bash
cd "$work/vdlinux"
taskset -c "$cpu" gbs -c "$work/official/gbs.conf" build -A armv7l -B "$work/official/GBS-ROOT" -D "$qb_build_conf" --threads 1 --spec tztv-kernel.spec
taskset -c "$cpu" gbs -c "$work/custom/gbs.conf" build -A armv7l -B "$work/custom/GBS-ROOT" -D "$qb_build_conf" --threads 1 --spec tztv-kernel.spec
```

**Native, after Claude review.** Estimate 30–120 minutes for staging and 45–150 minutes per kernel lane, subject to P4/QEMU and signing inputs. Allow about 20–25 GiB per GBS root plus the source/cache. The launcher reserves 55 GiB at start for both roots and rechecks 25 GiB before lane two. Each check retains the D-018 50 GiB disk and 16 GiB RAM headroom floors. It reserves a further 16 GiB available RAM for the kernel job. It uses one GBS package worker with CPU affinity limited to up to six CPUs and holds both heavy-job locks. Use the same launcher for `MODE=pic` after the heavy slot is free. The PIC estimate is 10–45 minutes and up to 12 GiB plus the headroom floor. Keep regular sudo/GBS authorization in the terminal. Compiler execution remains inside the build.

```bash
MODE=kernel
# For T7 use MODE=pic. Retained package source and GBS log trees can be narrowed explicitly.
CONSUMER_ARGS=()
```

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX")
  export TMPDIR="$d"
  rev=cd7f97e9cf75fd9bb70e0abe85ca626a073c64be
  get() {
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/artifacts/scripts/r0005/$1" -o "$d/$1"
    printf '%s  %s\n' "$2" "$d/$1" | sha256sum -c -
  }
  get gbs-mlgo-t7.py.txt 119aefdcc39d6f121c560f464963ee3f42fe232594611598180b48617a038ed3
  args=( "${MODE:?set kernel or pic}" )
  if [[ "$MODE" == pic ]]; then
    get gbs-t7-link.sh.txt c36498246c21dbd6de23567cbf7e3320f80cef7a0c61a499acee0a74feb01c77
    args+=( --probe "$d/gbs-t7-link.sh.txt" "${CONSUMER_ARGS[@]}" )
  fi
  mkdir -p "$PWD/workspace/temp"/pm000{4,5}-native-lock
  flock -n "$PWD/workspace/temp/pm0004-native-lock/heavy.lock" \
    flock -n "$PWD/workspace/temp/pm0005-native-lock/heavy.lock" \
    python3 -B -u "$d/gbs-mlgo-t7.py.txt" "${args[@]}"
)
```

Kernel acceptance needs the two successful GBS exits, output image/module inventories, sections from a uniquely identified vmlinux and real compiler commands showing both release advisors. The launcher retains the full command lines and prints examples, tool paths and ELF SHA-256, owner package and RPM NEVRA. Cached RPM file hashes are reported when available; compare these and the executable hash independently. Installed accelerator presence alone leaves effective dispatch open. This evidence proves the corresponding local GBS commands. The optional four-mode in-root TU replay is deferred until the package pair establishes its actual commands and completeness.

For T7, the default search reads build log, link map and source metadata under `vd-tree/workspace/temp` with a file/byte cap. Use `CONSUMER_ARGS=(--consumer-dir "$retained_gbs_root" --consumer-dir "$retained_source_root")` to focus on real consumer evidence. A scanned `-l` line alone leaves link mode unresolved. The GBS probe uses the same Official inputs and `gbs … build -A armv7l -B "$work/official/GBS-ROOT" -D "$qb_build_conf" --threads 1 --spec pm-t7-probe.spec --fallback-to-native`. Inspect `T7_RESULT`, `T7_RUNTIME` and `CONSUMER_CANDIDATE`. A TLS-local-exec link that succeeds requires runtime or actual consumer qualification. The CAPI case includes a thread isolation check against any linked DSO and matched driver PIE routes. [T7 consumer matrix](../../hq/PIC_FatLTO_Dual_Path_Design.md#consumer-follow-up-from-the-native-rpm-screen)

### Argot owner and uncapped config readback

Workflow `.github/workflows/tizen-build.yml` pins `ci-cargo-tizen-v0.6.7` from the private cargo-tizen producer repository. CODEOWNERS is **@AGENTIC/argo-tizen-maintainers**. `youngb.shin` submitted the retained artifacts. Exact armv7l Rust target and Thumb mode await the config and workflow below. A target used to build the host cargo-tizen tool itself is irrelevant to the Arm artifacts.

**Native, after Claude review.** Usually under a minute. Read-only Perforce, two text files, small disk and network. Prints the full config and every matching workflow line, using a compressed text packet if it exceeds 290 lines.

```bash
(set -euo pipefail; cd /home1/chengkai/vd-tree; d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX"); export TMPDIR="$d"; f="$d/argot-ci-target.py.txt"; curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/cd7f97e9cf75fd9bb70e0abe85ca626a073c64be/artifacts/scripts/r0005/argot-ci-target.py.txt' -o "$f"; printf '%s  %s\n' '58782c19c75a22753709609f0c21a6b65eb857f3ebb275a2799c51f7bb106693' "$f" | sha256sum -c -; python3 -B -u "$f")
```

Local Python 3.10.12 fixtures passed config staging, seven-row member selection, RPM spec parsing and explicit archive/search-path classification. Bash syntax passed. The fixed internal repositories and native workspace are inaccessible here, so neither GBS build nor the exact Argot config read has run. [Scripts commit](https://github.com/lhmax2010/analysis/commit/cd7f97e9cf75fd9bb70e0abe85ca626a073c64be)

## Native scan result and Thumb verification

Verified the 442-line log and SHA-256 `1e45ccfcb339bbc44d7fca64feb1c19bfc5d1ca9d2bcd0e088b8dd95e395b2d6`. It contains the complete Argot config, the scan summary preview and the pre-build GBS failure. The native `elf-modes.csv` remains the complete file-level input. [Exact transcript](../../artifacts/evidence/native-run-r0005-argot-scan-gbs-20261118.txt)

### Foreground kernel resume

The real QuickBuild pair takes priority. Use this for supporting effective argv only, after the Product comparison releases the heavy lock. Run after Claude review on the native server in a plain foreground terminal. The launcher verifies the exact existing Workdir contents and reuses the 24 overlaid files, the source logs and the two staged configs. It preserves the uninstrumented spec and adds its owner-write bit inside that Workdir. It accepts only the recorded pre-build failure and unused GBS roots. It prints `GBS_SOURCE_REUSED … P4_FETCH_SKIPPED` and then the two normal `GBS_START` lines. No tmux dependency. Refresh sudo in the attended terminal and allow the normal prompt during GBS. Estimate 45–150 minutes per kernel lane once source staging is skipped. Retain 50 GiB disk and 16 GiB RAM headroom with the existing additional job reservation. The locks keep this serial with other heavy work.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX")
  export TMPDIR="$d"
  f="$d/gbs-mlgo-t7.py.txt"
  curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d2542fa0292e06b3368cfaa61fb678f2496071b6/artifacts/scripts/r0005/gbs-mlgo-t7.py.txt' -o "$f"
  printf '%s  %s\n' c261656a64fa4ae62958c9c68518b5bdb7befa1818d5d232b3aee68df6e9e38a "$f" | sha256sum -c -
  sudo -v
  mkdir -p "$PWD/workspace/temp"/pm000{4,5}-native-lock
  flock -n "$PWD/workspace/temp/pm0004-native-lock/heavy.lock" \
    flock -n "$PWD/workspace/temp/pm0005-native-lock/heavy.lock" \
    python3 -B -u "$f" kernel --resume "$PWD/workspace/temp/pm0005-gbs-kernel.mtob625f"
)
```

### Verified scan and attribution queue

The 2,342-RPM sweep completed with zero reported errors. The 5,166 loadable ELFs contain 837.6 MiB of executable code and an estimated 358.9 MiB of A32 code. The 609-file ARM-predominant cohort comprises DYN 593 ARM and 4 mixed-ARM, and EXEC 11 ARM and 1 mixed-ARM. The 179 ARM relocatables and 2 too-small relocatables are separate. The condition signal agreed with mapping-symbol classification on 4,305 files and disagreed on 30. The scan uses mapping-symbol evidence when available. [Native scan summary](../../artifacts/evidence/native-run-r0005-argot-scan-gbs-20261118.txt#L162)

The top 40 can already be recovered in scan rank order. The attached TSV preserves the printed code KiB and A32 share values. Use `elf-modes.csv` for exact estimated byte counts and all 609 rows. [Top 40 native preview](../../artifacts/ledger/thumb-a32-top40-20261118.tsv)

| Producer marker strings in the 609 | Files | Estimated A32 MiB |
|---|---:|---:|
| GCC+Clang | 445 | 134.66 |
| GCC only | 157 | 186.38 |
| GCC+Rust | 4 | 12.38 |
| None | 3 | 9.67 |

The optflags hypothesis remains open. GCC and Clang marker strings identify the population to sample. They can come from linked objects and cannot identify the producer of every ARM code range. A package demonstrates cause (i) when a compile line for the matching output omits the intended mode flag and that precise driver, target and config combination defaults to ARM. A later `-marm` and a response file or per-target config are different evidence cases. Test defaults first using GCC's configuration and effective options, then Clang macros and `-###` with and without optflags and default config. [Clang configuration-file behavior](https://clang.llvm.org/docs/UsersManual.html#configuration-files)

Ten initial Clang-marker sample packages are `inference-engine-tflite`, `nnstreamer-tensorflow2-lite`, `deviced`, `gst-plugins-dash`, `libgcrypt`, `gst-ffmpeg`, `libpisa-ipc`, `vdfs`, `webapi-plugins` and `nodejs`. Confirm the CMake, Meson, Autotools, custom Make and gyp coverage from the pinned package sources and actual build driver. Include `com.samsung.tv.cobalt-perf` as a GN candidate and producer control because its visible ARM rows are GCC-only. Check glibc separately. Use verbose in-root GBS logs or exact matching published logs, and join to the linked output by package identity, path, Build ID/hash and source revision. A launcher can capture an individual GBS sample when a matched published log is absent.

The Argot config sets `arch = "armv7l"` and has no explicit Thumb setting. CI installs both `armv7-unknown-linux-gnueabi` and `armv7-unknown-linux-gnueabihf` and calls `cargo tizen … -A armv7l`. The retained installed Argot client has soft-float EABI evidence, consistent with the GNU EABI candidate. ABI flags can distinguish the convention. The exact Rust triple and underlying Thumb mode setting still require cargo-tizen's actual rustc argv or equivalent producer mapping. The two Argot payload paths are prebuilt from the platform build's perspective. Keep any Rust producer details as secondary attribution. Do the same ABI/argv match for `rust-std-shared` and `pkgmgr-server`. The presence of a library in a TPK alone leaves its provenance open. For glibc, inspect the pinned spec/rules and actual compile line before asserting `-marm`. [Argot config and CI](../../artifacts/evidence/native-run-r0005-argot-scan-gbs-20261118.txt#L5) [Rust Arm Linux target conventions](https://doc.rust-lang.org/rustc/platform-support/arm-linux.html)

### GBS Thumb defaults, sample and paired code-size builds

Native foreground after review. Start with `THUMB_MODE=defaults` and `THUMB_ARGS=()`. A small GBS build runs the compiler probes inside the dedicated root. Estimate 10–45 minutes, up to 22 GiB scratch and one package worker with affinity to up to six CPUs. For `sample`, use `THUMB_ARGS=(--source "$pinned_native_git_checkout" --revision "$full_checkout_commit" --spec "$spec_basename")`. This is one normal verbose GBS build of that exact source with the Official QB build.conf. For `pair`, add `--package "$installed_rpm_name" --elf "$exact_elf_path" --cause-ledger "$reviewed_causes_json"` and repeat `--elf` for matching outputs. Only start the three pairs once the respective cause-(i) rows are reviewed. The paired runner adds `-mthumb` to intercepted C/C++ compiler invocations inside GBS, keeps the control identical apart from that flag, and measures paired executable section bytes and A32 estimates. Verify wrapper coverage and same artifact paths, especially for LTO or absolute compiler paths, before accepting a pair. Allow up to 45 GiB for the two roots plus the capacity floor and estimate 30–150 minutes per lane depending on package size.

```bash
THUMB_MODE=defaults
THUMB_ARGS=()
```

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local commit=$1 file=$2 digest=$3
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$commit/artifacts/scripts/$file" -o "$d/${file##*/}"
    printf '%s  %s\n' "$digest" "$d/${file##*/}" | sha256sum -c -
  }
  rev=d2542fa0292e06b3368cfaa61fb678f2496071b6
  get "$rev" r0005/gbs-mlgo-t7.py.txt c261656a64fa4ae62958c9c68518b5bdb7befa1818d5d232b3aee68df6e9e38a
  get "$rev" r0005/gbs-thumb.py.txt 45fc17842a210b3a1a3f7ebfb81691eb57055ce60bd803bef57550e0e36984bb
  args=("${THUMB_MODE:?set defaults, sample or pair}" "${THUMB_ARGS[@]}")
  if [[ "$THUMB_MODE" == pair ]]; then
    get ea24f17d8d8f7b245c36d040381880839165d1c5 r0004/image_mode_scan.py.txt 1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75
    args+=(--scan-lib "$d/image_mode_scan.py.txt")
  fi
  sudo -v
  mkdir -p "$PWD/workspace/temp"/pm000{4,5}-native-lock
  flock -n "$PWD/workspace/temp/pm0004-native-lock/heavy.lock" \
    flock -n "$PWD/workspace/temp/pm0005-native-lock/heavy.lock" \
    python3 -B -u "$d/gbs-thumb.py.txt" "$d/gbs-mlgo-t7.py.txt" "${args[@]}"
)
```

### Full cause ledger and compact evidence return

Native after Claude review. This is read-only analysis of the completed scan and supplied evidence, with outputs under `workspace/temp/pm0005-thumb-causes.*`. It normally takes seconds for the inventory and longer if reading verbose package logs. Scratch is the ledger and selected command excerpts. Start with `CAUSE_ARGS=(--discover-logs /home1/chengkai/vd-tree/workspace/temp)`. Supply explicit `--sample-log "package=$exact_verbose_log"` for matching logs and `--defaults-log "$gbs_default_probe_log"`. Read relevant source flags with `--flag-source "$pinned_glibc_spec"` or inspect extracted Rust ELF attributes with `--abi-elf "$exact_elf"`. The initial join assigns the two known Argot prebuilts and preserves unknowns. Fill the returned evidence-template TSV with exact reviewed source/argv/artifact provenance and pass it via `--evidence`. One cause per ELF is a primary explanation; mixed TUs can record secondary reasons in the note. Print additional package counters via `--page`. Fetch the 609-file JSON in numbered packets with `--packet --part N`, or retrieve complete source commands for a sampled package via `--sample-packet NAME --part N` and the same sample-log arguments.

Run the estimate only after three reviewed pairs using `--pair-metrics` three times and the same confirmed cause ledger. The reported disk-code projection adds measured savings to the remaining confirmed A32 bytes times the pooled measured saving per control A32 byte. The minimum and maximum observed package ratios give sensitivity bounds. Keep the unverified 445-file cohort out of that extrapolation until its affected bytes are attributed. This projects executable-section bytes, with runtime PSS/RSS still requiring separate measurements.

```bash
CAUSE_ARGS=(--discover-logs /home1/chengkai/vd-tree/workspace/temp)
```

```bash
(set -euo pipefail; cd /home1/chengkai/vd-tree; d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX"); export TMPDIR="$d"; f="$d/thumb-causes.py.txt"; curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/4fd539751c65cea70d4540f33a132731015383f8/artifacts/scripts/r0005/thumb-causes.py.txt' -o "$f"; printf '%s  %s\n' 3bc1bbb70987ea950518864ba599be55cbd374fee7e4b1a1818dfa22076252e8 "$f" | sha256sum -c -; python3 -B -u "$f" "${CAUSE_ARGS[@]}")
```

Python 3.10.12 tests exercised the 24-entry retained-source resume, a read-only staged spec, RPM spec processing, command mode extraction and the cause-(i) proof gate. These were staging and parsing tests. Effective native compiler defaults, actual per-file causes beyond known evidence and matched package size results await the reviewed native jobs. [Scripts commit](https://github.com/lhmax2010/analysis/commit/d2542fa0292e06b3368cfaa61fb678f2496071b6)

## Published QuickBuild pair

QB **37654439** finished with Customized Base `tizen-10.0-base-dev-llvm-standard_20261118.1` and pinned LLVM rev12. Official **37627297** uses `20261113.1`. The user completed the `d3cea65` image comparer against [Customized Product 20261118.2](http://repos.vd.sec.samsung.net/priv/168.219.246.226:81/PRV/builds/b993/19368993/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261118.2/), with [Official Product 20261117.2](http://repos.vd.sec.samsung.net/priv/168.219.236.62:81/PRV/builds/b658/19350658/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261117.2/) as its existing control. The compare report is Friday's primary evidence. Use its readback after completion. The GBS kernel resume remains queued for supporting argv, after the comparison releases the heavy lock. [Friday report](../../reports/MLGO_Official_vs_Custom_20261120.md)

### Compare the two native GBS configs

Run on the native server. This takes seconds and uses no network, scratch files or heavy lock. It prints up to 70 lines of the original diff, requires exactly one occurrence of each expected URL, one buildroot and `profile.qb1111` per file, then checks the remaining normalized configuration. `GBS_CONFIG_DIFF_ONLY_BASE_PRODUCT_BUILDROOT` confirms the expected change set. The actual config files are unavailable in this checkout.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree/config
  old=gbs_vd_llvm_11.16_qb37627297.conf
  new=gbs_vd_llvm_11.16_qb37654439.conf
  repo=http://repos.vd.sec.samsung.net
  base="$repo/obs220/tizen-rsa/tizen-10.0-base-dev-llvm/standard/tizen-10.0-base-dev-llvm-standard_"
  prod_old="$repo/priv/168.219.236.62:81/PRV/builds/b658/19350658/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261117.2/"
  prod_new="$repo/priv/168.219.246.226:81/PRV/builds/b993/19368993/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261118.2/"
  raw=$(diff -U1 -- "$old" "$new") || [[ $? == 1 ]]
  printf '%s\n' "$raw" | sed -n '1,70p'
  normalize() {
    awk -v base="$1" -v product="$2" '
      match($0, /^[[:space:]]*url[[:space:]]*=[[:space:]]*/) {
        value = substr($0, RLENGTH+1)
        if (value == base) { b++; $0 = substr($0, 1, RLENGTH) "<BASE>" }
        if (value == product) { p++; $0 = substr($0, 1, RLENGTH) "<PRODUCT>" }
      }
      match($0, /^[[:space:]]*buildroot[[:space:]]*=[[:space:]]*/) {
        if (substr($0, RLENGTH+1) ~ /[^[:space:]]/) { r++; $0 = substr($0, 1, RLENGTH) "<BUILDROOT>" }
      }
      /^[[:space:]]*profile[[:space:]]*=[[:space:]]*profile\.qb1111[[:space:]]*$/ { q++ }
      { print }
      END {
        if (b != 1 || p != 1 || r != 1 || q != 1) {
          printf "GBS_CONFIG_CHECK_FAILED %s base=%d product=%d buildroot=%d qb1111=%d\n", FILENAME, b, p, r, q > "/dev/stderr"
          exit 2
        }
      }' "$3"
  }
  left=$(normalize "${base}20261113.1/" "$prod_old" "$old")
  right=$(normalize "${base}20261118.1/" "$prod_new" "$new")
  if [[ "$left" == "$right" ]]; then
    printf '%s\n' GBS_CONFIG_DIFF_ONLY_BASE_PRODUCT_BUILDROOT
  else
    printf '%s\n' GBS_CONFIG_UNEXPECTED_DELTA
    delta=$(diff -U1 <(printf '%s\n' "$left") <(printf '%s\n' "$right")) || [[ $? == 1 ]]
    printf '%s\n' "$delta" | sed -n '1,100p'
    exit 2
  fi
)
```

### Resolve the two full flash artifacts

Both HTTP Product directories and parent `artifacts/` directories timed out from this workspace. Both HTTPS parent checks also timed out. No exact `updateSU2E` download URL, size or hash could be verified here. In each completed QB's **Artifacts** view, select the KantSU2e release full image or follow the linked image-generation/publish job. Capture the versioned link to the exact file `updateSU2E`, its byte length and published SHA-256 if shown. If only an archive is listed, capture the immutable bundle link and the member path. The pinned downloader can search the exact fixed Product or parent directory when it is browsable, and it takes the direct file URL when available. [Directory links and pinned downloader](../../reports/KantSU2E_MLGO_Board_Day_0005.md#download-a-flash-image)

After the comparison and its readback, use the heavy slot for the two downloads serially, Official first for rollback. Then the retained foreground kernel GBS resume can use the slot for argv. The config diff and QB UI lookup can happen while the compare runs. No new native build or download was started from here.

## Thumb scan layout fix

Review [4fd539751c65cea70d4540f33a132731015383f8](https://github.com/lhmax2010/analysis/commit/4fd539751c65cea70d4540f33a132731015383f8). The launcher in [Per-file cause collection](#full-cause-ledger-and-compact-evidence-return) uses this commit. The two CSVs live under `pm0004-image-mode.b7rJie/results/` and `mode-summary.txt` lives at the run root. The Python 3.10.12 check used that directory layout and validated 2,342 completed packages and 609 ARM-predominant files. GBS pair mode reads the explicit `--cause-ledger` and inspects its own rebuilt RPMs, so it already supports the layout.

## Published image comparison and attribution

The native comparison covered 2,342 Official package identities. It found 2,289 differing RPMs, 50 identical and 3 unresolved. The 2,279 confounder flags combine ELF changes, other file changes, incomplete evidence and RPMs outside the Base delta. They do not provide a count of changed machine code. The figure of 177 is the separate installed-name/arch intersection with the non-LLVM Base delta. The Friday comparison should state the published image deltas, qualify workload differences and label board measurements as whole-image A/B. [Byte-verified native result](../../artifacts/evidence/native-run-r0005-image-compare-20261118.txt) [Friday report](../../reports/MLGO_Official_vs_Custom_20261120.md#published-kernel-payload-sizes)

The 3.7–3.8 MB packaged `vmlinux` has no section output in the retained transcript. The exact RPM member determines its container format, ELF headers, section sizes, and symbol and debug section presence. The smaller uImage/zImage and larger packaged vmlinux can coexist because their included bytes and compression differ. The reason for the observed growth is still open.

The earlier comparer deleted each downloaded RPM after extracting file hashes. The follow-up verifies the recorded RPM SHA-256 and each changed ELF's SHA-256 before inspecting the sections. It handles direct ELFs, hard-linked entries and supported nested ZIP/TPK/WGT members. It records per-section hashes and attributes, .text differences, other executable sections and conservative metadata-only candidates. Full per-ELF results stay in `sections.jsonl` under `workspace/temp/pm0005-elf-sections.*`. Keep the three unresolved packages in the coverage notes. Any remaining parser or payload errors appear separately. Only the kernel RPMs are read in `--kernel-only` mode.

**Native launcher, after Claude review.** First use `--kernel-only --fetch` if the vmlinux explanation is urgent. Expect roughly 1–10 minutes with network access and a free heavy slot. Use `--fetch` alone for the full run after the GBS job releases both heavy locks, plausibly several hours and multiple GB of network traffic. Current workspace data cannot establish a closer transfer estimate. Working scratch is one RPM and selected members at a time. Reserve 5 GiB free for downloads and use of temporary decoder space. Existing exact RPMs can be reused with repeatable `--cache-dir /path/under/vd-tree`. Cache-only runs omit `--fetch`, use no network or heavy lock, and report missing packages. The default command prints a bounded summary and uses one worker.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX")
  export TMPDIR="$d"
  f="$d/mlgo-elf-sections.py.txt"
  curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/3e96bc410252a5b3922c0f51f5ed0218852f4feb/artifacts/scripts/r0005/mlgo-elf-sections.py.txt' -o "$f"
  printf '%s  %s\n' '54a35e35c1844ca4d5cff60e6236d76698fe27f4f582347ed544249c146c34fd' "$f" | sha256sum -c -
  python3 -B "$f" --kernel-only --fetch
)
```

For the full run, remove `--kernel-only` in the last line. Return `INPUT`, `VMLINUX_FILE`, `VMLINUX_SECTION`, `TOP_TEXT_CHANGED_PACKAGE`, `USERSPACE_CHANGED_SECTION`, `TEXT_IDENTICAL_SECTION_SAMPLE`, `UNRESOLVED_SAMPLE` and `SUMMARY` lines. Exit status 2 preserves the analysis with incomplete coverage.

If .text changes are broad, bind the exact Official clang binaries to their archived source RPM before comparing with the pinned Customized OBS rev12 source. Compare SRPM member hashes, compiler source/patches, expanded `llvm.spec`, config files and the build environment. The rev12 record documents changes to `llvm.spec`, model/runtime archives and input verification. It does not establish the complete Baseline-to-rev12 source diff. Even when .text differs widely, package source, generated inputs, dependency or linker changes, and build flags are competing explanations. Reproduce representative changed user-space TUs in GBS with fixed source, flags, linked inputs and heuristics/default advisors before assigning ordinary codegen differences to Clang. The existing release flags apply to the kernel source configuration. [Rev12 submit record](../../artifacts/evidence/mlgo-source-submit.txt)

### Inspect the inner PERF tar

The retained evidence identifies the two loop-format archives and their nested tar names. The launcher streams one pinned outer tar.gz through GNU tar and prints at most the first 200 member rows plus total members and the count of paths whose basename matches `updateSU2E` case-insensitively. It creates no extracted image. A case-insensitive hit still requires checking the actual filename and full-image provenance. A miss leaves the full-image producer or publication path open. This checks only the named inner tar. [Native archive discovery](../../artifacts/evidence/native-run-r0005-image-compare-20261118.txt)

**Native launcher, after Claude review and with a free heavy slot.** Expect roughly 5–30 minutes per lane depending on link speed. About 1.78 GB network per invocation, one gzip stream, and negligible disk output. Run Official first, then change the final argument to `customized` for the second stream.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX")
  export TMPDIR="$d"
  f="$d/perf-inner-tar.sh.txt"
  curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/3e96bc410252a5b3922c0f51f5ed0218852f4feb/artifacts/scripts/r0005/perf-inner-tar.sh.txt' -o "$f"
  printf '%s  %s\n' 'b31f14648d75dd5e5f48732151dd7ad1d55a0e49635e8271594e98d532833988' "$f" | sha256sum -c -
  bash "$f" official
)
```

Python 3.10.12 fixture validation exercised a real disposable RPM, hardlinks, a gzip-wrapped ELF, .text mutations, and a nested TPK-format ZIP. The shell fixture exercised a path-prefixed inner member in a gzip tar. Claude review and actual native section/stream outputs are pending. The retained native ledger and published RPMs are available on the intranet. No board mutation was performed.
