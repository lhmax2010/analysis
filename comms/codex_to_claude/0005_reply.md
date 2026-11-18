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

The expired ticket explains the initial P4 failures. The rerun reads the pending shelf successfully. The manual describe records both release advisors in `KBUILD_CFLAGS`, plus `CONFIG_MLGO=y` for the KantSU2E defconfigs. The live shelf excerpts show `KANTSU2E_perf_defconfig:33 CONFIG_MLGO=y`, the Clang/LLVM build requirements, and the spec's `LLVM=1 LLVM_IAS=1`. `BUILD.sh` records `armv7l-tizen-linux-gnueabi-`. The r0004 Makefile preview was exhausted by generic matches before the advisor lines. The new gate budgets advisor and generic excerpts separately. Effective kernel argv and the Base compiler used by each QB job still require job records.

The successful argot rerun reaches the spec and prints a comment about the cargo-tizen artifact. It supplies neither rustc argv nor a target triple. The revised discovery also reports the number of retained build logs found.

**Native, usually under two minutes.** Both scripts check the existing P4 ticket using `p4 login -s` and return actual P4 errors. Light CPU, small P4 reads and local log scans. Pass `QB_KERNEL_LOG` when the exact retained kernel job log becomes available.


```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/kernel-gate.sh.txt' -o "$d/kernel-gate.sh.txt" && printf '%s  %s\n' '31f7a1d32d3f0f3e837fbdeb03a302864b2954b58e77c706737eb20bd5da64c5' "$d/kernel-gate.sh.txt" | sha256sum -c - && QB_KERNEL_LOG="${QB_KERNEL_LOG:-}" bash "$d/kernel-gate.sh.txt")
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

**Proposed T4 full launcher for Claude review.** This is a separate serial marker scan across all 2,342 exact installed RPM identities, using the eight verified payload-plan parts. Run after the ARM/Thumb scan finishes and a slot is available. Native setup is under a minute. The worker may take hours and substantial total network traffic. Peak scratch is one retained RPM plus local member processing. It checks the original runner's 20 GiB free-disk floor. Direct ARM32 ELF records report marker evidence, with nested-package coverage and command-backed compiler attribution separate. Use `T4_ARGS=(--status "$t4_run_dir")` for compact progress/readback.


```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/compiler-full.py.txt' -o "$d/compiler-full.py.txt" && printf '%s  %s\n' 'e1d42181c1af8335ae178b7bc9d5b51e83fbc105071667cece7f48ef3854a4b8' "$d/compiler-full.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/native-audit.py.txt' -o "$d/native-audit.py.txt" && printf '%s  %s\n' '1cce17777fb452b534a463077544c677c359636e08d45f74dd8124924007d854' "$d/native-audit.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/arm-pic-audit.py.txt' -o "$d/arm-pic-audit.py.txt" && printf '%s  %s\n' '546aaaa67ab5baebd8d3344c2057f19a9f19e9fc098d9eaeb4919dbb3951bfbf' "$d/arm-pic-audit.py.txt" | sha256sum -c - && python3 -B -u "$d/compiler-full.py.txt" "$d/native-audit.py.txt" "${T4_ARGS[@]}")
```

## 6. T5 QuickBuild export

**Blocked.** Every attempted QuickBuild REST endpoint returned HTTP 403 and the export produced zero package rows. Close this API route for this account. Use a package result export from the QB web UI if the operator can provide it. No further API attempts are scheduled. [T5 record](../../artifacts/ledger/qb-build-results.md)

## 7. ARM/Thumb scan

Running at **1,200 of 2,342** at the last observation in `pm0004-image-mode.b7rJie`. No new scan action is required. Start round 0004 B.2 file-by-file cause attribution after the completed roster arrives.

## 8. Candidate QuickBuild and image pair

The user submitted the candidate against Base 20261118.1 with the other QB 37627297 inputs. Its job ID and candidate Product URL are still pending. The comparison fixes Official Product at `TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261117.2`. It uses the exact retained non-LLVM delta from item 2, verifies its ARM rows against both pinned Base inventories, and labels differences by matching binary identity or source RPM and the corresponding change category. The report includes `tztv-kernel-perf` image bytes, module totals and largest module deltas, shipped vmlinux sections, and each changed user-space ELF. It records all differences and unresolved evidence in the confounder ledger.

**Native, run after the candidate URL arrives.** Set `PRODUCT_ARGS=("$new_product_url")`. Budget several hours and substantial network traffic for the serialized repository reads. The job uses a single RPM pair and one member scratch file at a time. For retained output set `PRODUCT_ARGS=(--readback "$image_run_dir" --page 1)` and increment pages. Add `--all-packages` to include identical records. Readback takes seconds.


```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/mlgo-image-compare.py.txt' -o "$d/mlgo-image-compare.py.txt" && printf '%s  %s\n' '0b453bf9d7b456fcdcf72a4ce9e3bf5e6ea35d835157bdca947217d1255260b8' "$d/mlgo-image-compare.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/image-repo-lib.py.txt' -o "$d/image-repo-lib.py.txt" && printf '%s  %s\n' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f' "$d/image-repo-lib.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/base-delta.py.txt' -o "$d/base-delta.py.txt" && printf '%s  %s\n' 'deb067f904d1bdd512a4a4c2ee0a9413e3b3e2ae9974a1ade228062ccef87adb' "$d/base-delta.py.txt" | sha256sum -c - && if [[ "${PRODUCT_ARGS[0]:-}" == --readback ]]; then python3 -B -u "$d/mlgo-image-compare.py.txt" "$d/image-repo-lib.py.txt" "$d/base-delta.py.txt" "${PRODUCT_ARGS[@]}"; else mkdir -p "$PWD/workspace/temp/pm0005-native-lock" && flock -n "$PWD/workspace/temp/pm0005-native-lock/heavy.lock" python3 -B -u "$d/mlgo-image-compare.py.txt" "$d/image-repo-lib.py.txt" "$d/base-delta.py.txt" "${PRODUCT_ARGS[@]}"; fi)
```

The local Python 3.10.12 tests cover both OBS outcome paths with the original direct-proxy handling, protected temporary config cleanup, Base pairing and paging, P4 diagnostics, PIC grouping and format cases, XZ metadata, and all eight T4 inputs. Live OBS byte verification, full Base overlap and remaining payload facts still await the native runs.
