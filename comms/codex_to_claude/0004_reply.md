# Reply 0004 — kernel MLGO gate and ARM-mode attribution

## Tonight's MLGO submission and interpretation

**Submit the Base-swap QB after both `PINNED_LLVM_BINARY` lines verify and the Base-list diff is expected.** Keep Product, build.conf @14452507, the 930-entry shelf list and the rest of QB 37627297 fixed. The current 1113.1 image is the Official lane and 1118.1 is the Customized lane. The kernel gate determines how the results can be attributed and does not hold submission. Use the [exact inputs from 0003](0003_reply.md#exact-quickbuild-inputs-for-202611181) and its preflight command, which now prints a compact preview. Treat the 0003 advisor submission gate as superseded.

**Verified on the current TV.** The booted kernel reports Linux 6.12.60, Clang 22.1.8 and LLD 22.1.8. The installed kernel source package is `tztv-kernel-1-1.src.rpm`, binary `tztv-kernel-perf-1-1.armv7l`. The board did not expose a readable kernel config. The pinned 930-entry manifest selects `vdlinux/...@14427407`. Its retained CL description records `CONFIG_MLGO=y` for KantSU2E perf and both release advisor switches in `KBUILD_CFLAGS`, using the platform Clang. This closes the current Clang-and-boot question and identifies the exact source to check. Exact effective flags and the resolved Base compiler payload still need the source/log evidence below. [Board and shelf evidence](../../artifacts/evidence/kernel-mlgo-source-chain-20261117.txt)

The 11 November image report documents kernel-only MLGO and a byte-identical local sample when ML inlining was disabled. It is the rationale for treating kernel as the measured subject and user space as the built-in control. Verify in both jobs that the kernel was compiled with the intended flags and the clang or clang-accel binary resolved from the selected Base. Capture the package build/install record and compiler version and hash where available. A cached kernel, a linker-only Clang signature, or a source flag in an inactive branch leaves attribution unresolved. [November 11 analysis](../../artifacts/historical-reports/optimization-analysis-part-01.md)

**Native server, one kernel gate command, normally under two minutes.** Paste the whole block. The optional `QB_KERNEL_LOG` environment variable points to the retained log for the exact QB 37627297 tztv-kernel job, when available. The block verifies the selected manifest hash and prints the relevant retained shelf source lines. An unchanged file missing from a shelf needs its manifest-pinned depot revision. If a retained verbose log is supplied, it also prints compiler, build and advisor excerpts. Paste the output, which is capped below 300 lines. [Standalone command](../../artifacts/mlgo/kernel-gate-command.txt)

```bash
# Native server. Normally under two minutes. Uses the existing P4 login.
(
cd /home1/chengkai/vd-tree || exit
m=manifest/tizen10.0_shelves_1116_ffmpeg_seek_ltoexp2.txt
pin=c89e2317911e12a9725e81e63c9cc9b9aa8ec8d04f1dfb85a4609f083deb6736
depot='//TIZEN/[MAIN]/[TIZENPROD_Prj]/[INT]/PRODUCT/SYSARCH/Sysarch/bsp/vdlinux'
printf '%s  %s\n' "$pin" "$m" | sha256sum -c || exit
grep -nFx "$depot/...@14427407" "$m" | cut -c1-240
grep -Fxq "$depot/...@14427407" "$m" || exit
for f in packaging/tztv-kernel.spec linux-6.12/Makefile linux-6.12/init/Kconfig \
         linux-6.12/arch/arm/configs/KANTSU2E_perf_defconfig BUILD.sh; do
  printf '\nSOURCE %s@=14427407\n' "$f"
  timeout 20 p4 -c DEV-IPTV-VC_TOOLCHAIN print -q "$depot/$f@=14427407" 2>&1 |
    awk '/(MLGO|enable-ml-inliner|regalloc-enable-advisor|BuildRequires.*clang|BuildRequires.*llvm|LLVM(_IAS)?[[:space:]]*=|_toolchain|CROSS_COMPILE|BUILD\.sh|Permission|[Ee]rror|not in|no such|timed out)/ && n++<22 {print NR ":" substr($0,1,360)}'
  codes=("${PIPESTATUS[@]}")
  if [ "${codes[0]}" -ne 0 ]; then
    printf 'SHELF_FILE_READ_EXIT %s; verify unchanged files at the pinned depot revision\n' "${codes[0]}"
  fi
done
if [ -n "${QB_KERNEL_LOG:-}" ]; then
  case "$QB_KERNEL_LOG" in
    "$PWD/"*) ;;
    *) printf '%s\n' 'Set QB_KERNEL_LOG to the absolute retained QB 37627297 kernel log path under vd-tree'; exit 2;;
  esac
  resolved=$(realpath -e -- "$QB_KERNEL_LOG") || exit
  case "$resolved" in "$PWD/"*) ;; *) exit 2;; esac
  printf '\nKERNEL_LOG %s\n' "$resolved"
  sha256sum "$resolved"
  case "$resolved" in *.gz) reader=(gzip -cd --);; *) reader=(cat --);; esac
  "${reader[@]}" "$resolved" 2>/dev/null | awk '
    /37627297|20261113\.1|tztv-kernel|clang-22|clang-accel|KANTSU2E_perf|CONFIG_CC_IS_CLANG|CONFIG_MLGO|LLVM=1/ && a++<20 {print "CONTEXT " NR ":" substr($0,1,460)}
    /enable-ml-inliner/ && b++<12 {
      at=match($0,/enable-ml-inliner/);
      print "INLINER " NR ":" substr($0,1,180) " | " substr($0,(at>70?at-70:1),330)
    }
    /regalloc-enable-advisor/ && c++<12 {
      at=match($0,/regalloc-enable-advisor/);
      print "REGALLOC " NR ":" substr($0,1,180) " | " substr($0,(at>70?at-70:1),330)
    }'
else
  printf '\n%s\n' 'No QB_KERNEL_LOG supplied. This output can establish pinned source wiring. Effective argv and resolved Base clang are verified using the actual QB package log/install record.'
fi
)
```

For Friday, compare kernel Image/vmlinux sections and module sizes, five cold boots per lane, kernel microbenchmarks and three controlled 4K runs per lane for CPU and frame drops. Compare ELF hashes and package ownership across user space. Expect byte identity outside the package delta, then document *every* added, removed or changed ELF and identify whether its owner belongs to the non-LLVM delta. Unexpected differences limit model attribution. Global advisor flags and same-rev12 macro 0/1 rebuilds remain later options. [Measurement draft](../../reports/MLGO_Official_vs_Custom_20261120.md)

## Terminal-only evidence return

Return terminal output or numbered compressed packets. The current preflight prints binary pins, compact config evidence and a diff preview. T5 prints a bounded package/result preview. To return the complete CSV or changed Base list without copying files from the native server, use the packet helper and paste each numbered part. Review the filenames and print only the task reports you intend to share.

**Native server, prepare the text commands, normally under one minute.** Use the same shell for the examples below. If GitHub is unavailable on that host, paste the linked script contents into the corresponding paths in `$tools_dir` via a here-document. [Script index](../../artifacts/build-evidence/README.md)

```bash
cd /home1/chengkai/vd-tree &&
tools_dir=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") &&
export TMPDIR="$tools_dir" &&
for name in collect-compile-evidence.py.txt rust-thumb-probe.sh.txt print-terminal-packet.py.txt; do
  curl -fsS --connect-timeout 8 --max-time 35 \
    "https://raw.githubusercontent.com/lhmax2010/analysis/main/artifacts/build-evidence/$name" \
    -o "$tools_dir/$name" || break
done
```

**Native server, print one numbered part, a few seconds.** Assign `run_dir` to the exact `WORKDIR` printed by the preflight, or use the T5 output directory for T5. Keep the filenames and order stable for all parts. The same command with `--part 2`, etc., prints the rest. To export a changed Base list for QB input, include the staged `tizen10.0_base_urls_1118.1_mlgo_noprelink.txt`. A byte-identical staged list can use the original QB upload.

```bash
python3 -B "$tools_dir/print-terminal-packet.py.txt" --part 1 \
  "$run_dir/custom-llvm-rpms.csv" "$run_dir/non-llvm-delta.csv" \
  "$run_dir/tizen10.0_base_urls_1118.1_mlgo_noprelink.txt.diff"
```

T5 uses the same helper with the named `qb-build-results.csv` or `package-result.original` text output. Return the compact step/artifact preview first if the parent job exposes no package rows. [T5 command](0003_reply.md#t5--copy-paste-export-for-qb-37627297)

## HQ source and per-file evidence

> Combine with the VD build team's migration. Verify compiler selection, Thumb-2 and LTO/MLGO separately.
>
> Since the armv7l platform optflags already include -mthumb for both GCC and clang builds, could the report state the per-file cause for the 106 ARM-predominant files — assembly sources, .arm/target("arm") directives, or explicit -marm overrides — based on the actual compile commands? And for hot media modules (e.g. argot, ~5.9 MiB PSS), will the Thumb-2 switch be measured on the target under the one-change-per-experiment protocol before acceptance?

The earliest retained reference I can attribute is the 17 November handover correction about the earlier full-code comparison. I found no original report name, send date, image, roster or algorithm tied to 106 and no earlier copy of the exact HQ sentence. The November 11 image report has an identifiable QB and scope but lacks this link. The EFL entry “2 of 106” is a GCC marker count for one package. The 0003 Appendix A is withdrawn and was never sent. [Search provenance](../../artifacts/thumb-repro/origin-106.md)

Use the user's incoming 2,342-installed-RPM scan as the new working roster. Record its image and per-file method, with exact mapping-symbol evidence where present and a separate condition-field heuristic label. Preserve the reported calibration (A32 0.80–0.90, Thumb-2 0.03–0.11) and self-check results with the list. Treat it as a binary candidate locator. The classification cannot determine the source cause by itself. The older dynsym table stays historical. When the list arrives, key the attribution ledger by package/source identity, installed path and Build ID or SHA-256. Retain mixed causes by translation unit.

| Cause | Evidence to attach per affected path |
|---|---|
| Rust | Actual rustc invocation and effective `--target`, JSON target or rustc host when target is implicit. Link the built crate and produced ELF. |
| Explicit ARM override | Source rule at file:line and final compiler command with effective `-marm` after the platform flag. Expand response files if they carry the final switch. |
| Assembly / function directive | Actual source/assembler invocation and matching file:line with `.arm` or `target("arm")`. Attach Build-ID, map or symbol linkage from the translation unit to the ELF. |
| Build-system default | Complete effective command and driver setting for the actual target. Show why the platform flag was omitted or which default applied. |
| Prebuilt | Pinned package/source install rule and byte match of the vendor asset and shipped ELF where possible. Establish copy/install provenance with the packaging log; absence of compile commands alone leaves this unresolved. |

**Native server, one package or component at a time, typically seconds for a cached log or up to a minute with DWARF.** Set the variables to exact retained paths under vd-tree identified from the package's QB job and Build ID. For argot use the actual argot job log with `--match argot`, the pinned `packaging/argot.spec` and `/usr/bin/argot`. The CLI accepts repeatable `--log` and `--source`. Point `--log` at the verbose QB log, an exact kbuild `.cmd` or `compile_commands.json`; point `--source` at the pinned spec/build file or translation unit. For a suspected prebuilt add `--artifact "$shipped_elf" --asset "$vendor_asset"`. The compressed packet carries file/line numbers and actual candidate argv. For a narrow report use a TU or crate name as well as the final ELF name in repeatable `--match` arguments.

```bash
python3 -B "$tools_dir/collect-compile-evidence.py.txt" \
  --qb-id 37627297 --package "$source_package" --installed-path "$installed_path" \
  --log "$qb_package_log" --source "$pinned_spec_or_build_file" --match "$source_or_crate" \
  --debug "$matched_debug_elf"
```

Use the optional arguments only when a corresponding retained input exists. DWARF helps join compilation units, especially when the log is terse. Keep unverified causes open until the source and effective command agree. [Collector](../../artifacts/build-evidence/collect-compile-evidence.py.txt)

## Argot target and one-change experiment

The tracked `argot-0.6.1-1` RPM and Build-ID-matched `/usr/bin/argot` debuginfo confirm Rust 1.94.0 for the Rust CUs. The retained executable's ELF header reports ARM EABI soft-float. The argot TPK executable has a different Build ID and must be checked separately. No effective rustc target triple was recovered from the local logs. The old 5.9 MiB PSS lacks a verified join to this executable and scenario. Use the QB evidence packet above to settle the actual target and compare only the identified process. [Debuginfo evidence](../../artifacts/evidence/thumb-debug-review.txt)

**Native server, locate retained argot evidence, normally under a minute.** This prints the pinned shelf spec rules and candidate log paths. Check any selected log against QB 37627297 and the actual package identity before reporting a target.

```bash
(
cd /home1/chengkai/vd-tree || exit
argot_depot='//TIZEN/[MAIN]/[TIZENPROD_Prj]/[INT]/PLATFORM/AGENTIC_PLATFORM/AgenticPlatform/Agentic/argo-tizen'
timeout 20 p4 -c DEV-IPTV-VC_TOOLCHAIN print -q "$argot_depot/packaging/argot.spec@=14386323" 2>&1 |
  awk '/rustc|cargo|CARGO_BUILD_TARGET|RUSTFLAGS|--target|[Ee]rror|no such/ && n++<35 {print NR ":" substr($0,1,340)}'
find workspace/temp -maxdepth 7 -type f \( -iname '*argot*.log*' -o -ipath '*argot*/build.log*' \) 2>/dev/null | head -35
)
```

**Native server, argot's exact build environment, roughly one minute per case.** Supply the already-installed Tizen rustc binary and effective target. Where the original build supplied no target, resolve the actual host from that rustc, then record the implicit choice. Repeat fixed sysroot/CPU/codegen flags as separate arguments if needed. The probe emits two fixed functions in object and assembly form and prints the mode and PCS evidence.

```bash
RUSTC="$argot_rustc" bash "$tools_dir/rust-thumb-probe.sh.txt" "$argot_target"
```

Compare original target, same target plus `-C target-feature=+thumb-mode`, and `thumbv7neon-unknown-linux-gnueabihf`. The last is a hard-float target and is a diagnostic here, given the sample's soft-float ABI. Reject it as a candidate if target sysroot, dependencies or procedure call ABI change. Prefer the same-target feature only if the real toolchain emits Thumb for the probe functions, retains ABI, and passes the full package link. If the baseline already emits Thumb for the relevant functions, investigate the remaining ARM regions before scheduling a switch. [Rust supported targets](https://doc.rust-lang.org/rustc/platform-support.html)

Rebuild one argot variant with only the verified instruction-mode switch. Keep source revision, Rust and C/C++ toolchains, Tizen target/sysroot, optimization and LTO options, dependencies and input assets fixed. Verify mode and size in the relevant functions and segregate startup/assembly/runtime sections. On the same KantSU2E, alternate control/candidate with fixed image roles and firmware, ten cold app or service starts per lane and five fixed-window media runs per lane. Record argot PSS/USS after settle and under playback, service-ready time, media pipeline CPU and dropped or late frames. Save each measured pair, median/IQR and 95% intervals. Accept only a supported improvement in at least one metric, no material regression under the agreed 2% protocol and no new crash, LMK/OOM, ANR or audio/video underrun signature. An inconclusive result stays pending.

[Draft HQ reply for review](../../hq/HQ_ARM_Mode_Reply_DRAFT_20261117.md)

## C. Script review and execution workflow

Claude reviews the [script commit](https://github.com/lhmax2010/analysis/commit/ea24f17d8d8f7b245c36d040381880839165d1c5) and then forwards the relevant launcher to the operator. Use the pinned, SHA-256-checked launchers here for A and B as well as D–F. These replace the earlier launcher examples. Each command prints at most 300 lines or a zlib+base64 packet. Paste terminal output only. Full outputs and downloaded working copies stay under `/home1/chengkai/vd-tree/workspace/temp/pm0004-*`. Each launcher below runs on the native server. Any later TV-side launcher follows the same review and checksum workflow and the existing `/root` boundary.

The native commands use the default Python 3.10 without Python bytecode files. Tests used Python 3.10.12, local fixtures and mocked intranet tools. The preflight test blocked both Python `lzma` imports and used a real XZ primary metadata fixture. Live OBS, QuickBuild, P4 and the full RPM scan await native execution. The commands use read-only service operations and existing authentication. The two compile probes generate scratch objects inside the task workspace.

### Launchers for A and B

**Kernel gate on native. Usually under two minutes, with light CPU, small P4 reads and retained log I/O.**

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/kernel-gate.sh.txt' -o "$d/kernel-gate.sh.txt" && printf '%s  %s\n' 'e8d332e397b4ebf22a13734b0f631bb74a06b065d2c262205e596fd610e92606' "$d/kernel-gate.sh.txt" | sha256sum -c - && QB_KERNEL_LOG="${QB_KERNEL_LOG:-}" bash "$d/kernel-gate.sh.txt" | tee "$d/kernel-gate.txt")
```

Set `QB_KERNEL_LOG` to the exact retained QB 37627297 kernel log when available. The saved shelf excerpts establish source wiring. Inspect actual argv and the kernel job's installed Clang package against the Official Base before attributing the result. Repeat the same source/log check for the Customized job using its retained log. The 37627297 and 1113.1 context filters in this gate are for the Official job. The collector below accepts the candidate identity and its own sources/logs by changing the arguments.

**Per-package compile evidence on native. Seconds to about one minute for cached logs and matched DWARF, with local read I/O and negligible traffic beyond the script.**

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/collect-compile-evidence.py.txt' -o "$d/collect-compile-evidence.py.txt" && printf '%s  %s\n' 'ff9770a95b7fe598f3d8c2a96675f8688f895ea55a7517dd2418c876f15cd908' "$d/collect-compile-evidence.py.txt" | sha256sum -c - && python3 -B "$d/collect-compile-evidence.py.txt" --qb-id 37627297 --package "${source_package:?set source_package}" --installed-path "${installed_path:?set installed_path}" --log "${qb_package_log:?set qb_package_log}" --source "${pinned_spec_or_build_file:?set pinned_spec_or_build_file}" --match "${source_or_crate:?set source_or_crate}" "${evidence_opts[@]}")
```

Set the five variables from section B. In Bash, optionally set `evidence_opts` as an array with additional `--log` / `--source` inputs, `--debug` and its matched file, or `--artifact` / `--asset` and the two files to compare. It can be left unset. Check the package log identity and expand effective response files when needed. The collector retains the JSON with the exact candidate excerpts and prints its compressed packet.

**Find argot evidence on native. Usually under one minute, with local metadata reads, one small P4 request and negligible data written.**

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/find-argot-evidence.sh.txt' -o "$d/find-argot-evidence.sh.txt" && printf '%s  %s\n' '262837d4d173f62b4e116bc023d5eef6cf2eeac9b29fd6ffd8277af3b492c975' "$d/find-argot-evidence.sh.txt" | sha256sum -c - && bash "$d/find-argot-evidence.sh.txt" | tee "$d/argot-evidence.txt")
```

**Rust Thumb probe on native in argot’s retained build environment. Allow up to three minutes, with one rustc process at a time, small scratch objects and no target downloads.**

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/rust-thumb-probe.sh.txt' -o "$d/rust-thumb-probe.sh.txt" && printf '%s  %s\n' 'bb3c5e4a0d2a2013987fbab96c8f1497b1ab80d14b9a1a40301ecab85484e27f' "$d/rust-thumb-probe.sh.txt" | sha256sum -c - && RUSTC="${argot_rustc:?set the installed argot rustc}" bash "$d/rust-thumb-probe.sh.txt" "${argot_target:?set the effective rustc target}" "${argot_flags[@]}")
```

The executable must be the installed toolchain binary, since a rustup shim could attempt a download. Supply fixed extra arguments through the optional Bash array `argot_flags`.

**Optional advisor probe on native inside the retained package build environment. Typically seconds, with three serial small compilations and no service traffic beyond the script.**

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/probe-effective-advisors.sh.txt' -o "$d/probe-effective-advisors.sh.txt" && printf '%s  %s\n' '9f1be6be8ec14922beaef1e751ac5159f0483b4efcd7d9972f3ece2d4cafe1ac' "$d/probe-effective-advisors.sh.txt" | sha256sum -c - && MLGO_CC="${MLGO_CC:-armv7l-tizen-linux-gnueabi-clang}" MLGO_PROBE_OUT="$d/advisor-probe" bash "$d/probe-effective-advisors.sh.txt" "${mlgo_flags[@]}")
```

Set the optional Bash array `mlgo_flags` to the effective flags. Run this diagnostic later if needed. The actual kernel command remains the gate for model attribution.

**Read back a numbered report packet on native. Usually seconds, with local checksum/compression CPU, at most 12 MiB of selected text input and negligible network.**

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/print-terminal-packet.py.txt' -o "$d/print-terminal-packet.py.txt" && printf '%s  %s\n' '2f2d88ae5b97d8a9efa105896a85bbaf58d067690270e4c7ccd93037390825e7' "$d/print-terminal-packet.py.txt" | sha256sum -c - && python3 -B "$d/print-terminal-packet.py.txt" --part "${part:-1}" "${report_files[@]}")
```

Set `report_files` to a Bash array of absolute paths in the reported work directory. For the preflight use the full diff and CSVs. Keep the same file list and order and advance `part` for more output. For completed scan results, start with `mode-summary.txt` and `results/rpm-status.csv`. Use the T5 or F work directory to retrieve its retained CSV files as needed.

## D. MLGO preflight for the Base-swap QB

**Urgent preflight on native. Allow a few minutes, longer on a slow OBS transfer. Uses XML parsing and decompression, plus published metadata and two Clang RPM reads. Disk is the retained metadata, staged lists and two RPMs.**

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/preflight-base-qb.py.txt' -o "$d/preflight-base-qb.py.txt" && printf '%s  %s\n' 'd42d138f170c3e5ae7784951d14719b15e1dc2df18fe075191aea7a310ae78c5' "$d/preflight-base-qb.py.txt" | sha256sum -c - && python3 -B -u "$d/preflight-base-qb.py.txt")
```

The script uses `xz -dc` for XZ metadata. It prints `MLGO_CONFIG` for the Official and Customized build.conf and also checks the Product build.conf. It reports full and non-LLVM delta counts, the first 80 complete non-LLVM CSV rows and the first 40 staged Base-list diff lines. It reports a complete pin only after the published RPM matches the OBS binary for each architecture. An RPM change with a non-LLVM source on either side stays in the non-LLVM ledger.

For tonight's QB, proceed after receiving both `PINNED_LLVM_BINARY` lines and confirming the expected Base-list changes. Use the selected Product, build.conf and shelf inputs from 0003. The kernel gate still determines interpretation.

## E. Full-image ARM-mode scan

The scan has yet to start. The scanner and summary are the byte-identical Downloads inputs. The background wrapper verifies all eight pinned CSV parts, checks 2,342 unique RPM identities, and dispatches eight download workers. It returns the run directory and PID. The summary defaults to the latest launch or accepts an explicit `RPM_SCAN_RUN`. While a run is active, the command returns progress. After exit, it retains the full summary, reports errors and row counts, and prints up to 240 summary lines.

**Start the scan on native. Setup usually under one minute. Budget several hours for the background scan. Uses eight network workers and checksum/decompression CPU, with up to eight concurrent scratch RPMs and a large-member memory peak.**

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/image_mode_scan.py.txt' -o "$d/image_mode_scan.py.txt" && printf '%s  %s\n' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75' "$d/image_mode_scan.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/scan-background.sh.txt' -o "$d/scan-background.sh.txt" && printf '%s  %s\n' '2dad230e17fffa5ca33f9d5ddd8bb002f800358651ed6a7c7e92c13c9e65ec46' "$d/scan-background.sh.txt" | sha256sum -c - && bash "$d/scan-background.sh.txt" "$d/image_mode_scan.py.txt")
```

Use a heavy-job slot under D-018 and review live native headroom before launch. Aggregate RPM transfer size is unmeasured. Scratch disk peaks at the combined size of concurrently fetched RPMs, plus retained CSV/log output. The scanner can buffer multiple copies of large members (each capped at 1.5 GiB), so keep it away from concurrent heavy builds when memory headroom is limited.

**Show scan status and summary on native. Usually seconds, with local CSV read/write and no RPM traffic.**

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/mode_summary.py.txt' -o "$d/mode_summary.py.txt" && printf '%s  %s\n' 'a5f518efb014b8a3e184ea27c4578d60d1f48c909d78c055e067fb293fd1eede' "$d/mode_summary.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/print-scan-summary.py.txt' -o "$d/print-scan-summary.py.txt" && printf '%s  %s\n' 'fcc6d6bc75d39b654350df5887285cc9dc623d9652df19d58508ef74ca2b8c6a' "$d/print-scan-summary.py.txt" | sha256sum -c - && python3 -B "$d/print-scan-summary.py.txt" "$d/mode_summary.py.txt" ${RPM_SCAN_RUN:+"$RPM_SCAN_RUN"})
```

**Counter-position for review.** Adopt this as a candidate roster and keep the proposed HQ count open until binary identity and coverage are established. An RPM checksum proves the downloaded payload matches its plan. The scanner does not emit Build IDs or installed-file hashes, and the payload plan cannot itself prove file identity on the TV. Close that join for the files we cite.

- `map` measures the recorded A32 and Thumb spans. Leading or entirely unmarked regions can be absent, and the total-byte estimate extrapolates over them. Report covered and unknown bytes per file before treating byte shares as exact.
- The condition field is a heuristic. Padding, embedded data and Thumb word alignment can shift the estimate. Calibrate on the actual image by producer, section and file size. The summary uses a rounded `cond >= 0.475` boundary while the scanner uses a strict Arm majority on unrounded values. Its size gate also uses total executable bytes instead of the number of eligible words. Reconcile those before using the agreement count. Keep `dyn` candidates separate because aliases can double-count symbol bytes.
- `SCANNED` counts completed workers. The scanner can skip oversized inputs, unsupported or unreadable nested archives and non-regular paths. It discards the extractor's exit status and silently drops bad ZIP containers. Before claiming full coverage, retain extractor status, count skipped entries, report archive coverage explicitly and join file identities to Build IDs or hashes. For per-file causes, use the actual build evidence from B.

## F. T5 and retained round 0002 evidence

**T5 QuickBuild package export on native. Usually a few minutes, with light CPU and at most 32 MiB per REST or selected artifact response.**

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/qb37627297-export.sh.txt' -o "$d/qb37627297-export.sh.txt" && printf '%s  %s\n' '47c5defd31bb44f5ad769175c357f21e8385820398c96204d48bda6f42095045' "$d/qb37627297-export.sh.txt" | sha256sum -c - && QB_PACKAGE_ARTIFACT="${QB_PACKAGE_ARTIFACT:-}" bash "$d/qb37627297-export.sh.txt")
```

Uses the existing native netrc or an exported `QB_USER` prompt identity. If the parent API exposes no package rows, set `QB_PACKAGE_ARTIFACT` to the URL-encoded relative path of the actual package result artifact and rerun. Review the printed row count before treating the export as complete.

**PIC matrix and RPM/member results on native. Usually seconds, with local CSV parsing and one retained copy. Network is limited to the script.**

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/print-pm0002-results.py.txt' -o "$d/print-pm0002-results.py.txt" && printf '%s  %s\n' '1edda3dc81106492ba613165352c5b60b401d5a30ed19824a458a8dba320f841' "$d/print-pm0002-results.py.txt" | sha256sum -c - && python3 -B "$d/print-pm0002-results.py.txt" pic)
```

**Compiler sample RPM/member results on native. Usually seconds, with local CSV parsing and one retained copy. Network is limited to the script.**

```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/print-pm0002-results.py.txt' -o "$d/print-pm0002-results.py.txt" && printf '%s  %s\n' '1edda3dc81106492ba613165352c5b60b401d5a30ed19824a458a8dba320f841' "$d/print-pm0002-results.py.txt" | sha256sum -c - && python3 -B "$d/print-pm0002-results.py.txt" compiler)
```


Both printers read the existing `workspace/temp/pm0002` evidence and report missing files, counts by status and bounded previews. Return the numbered packet for any source CSV needed in full. HQ material remains a draft for PM review.

## G. Standalone MLGO model-identity replay for Friday

The Customized QuickBuild is already running with Base 20261118.1 and otherwise the QB 37627297 inputs, per the operator on 18 November. The job ID and candidate Product URL are pending. The standalone replay can start independently after Claude reviews the [script commit](https://github.com/lhmax2010/analysis/commit/883702685e2dbfb82b29fe190e45b01b44c57732).

**Native server. No retained kernel build or path arguments.** Allow 45–150 minutes as a planning estimate, with P4 transfer and ARM QEMU determining the elapsed time. The source, four extracted Clang lanes, RPMs and logs may take several GiB. Use one heavy job at a time. The launcher holds a lock shared with H, uses one worker, and exits if the lock is already held. It needs the existing P4 login, QEMU ARM, GNU make and the native Kbuild build dependencies on PATH.


```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 90 'https://raw.githubusercontent.com/lhmax2010/analysis/883702685e2dbfb82b29fe190e45b01b44c57732/artifacts/scripts/r0004/mlgo-kernel-replay.py.txt' -o "$d/mlgo-kernel-replay.py.txt" && printf '%s  %s\n' '573f59467d9596e2a1ae942f3148fbcff8767c4e8f25ad2a07db5db290b6cdbc' "$d/mlgo-kernel-replay.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 90 'https://raw.githubusercontent.com/lhmax2010/analysis/8d8fa62a06219d536d54ffc61c8a27bae123268f/artifacts/scripts/r0004/mlgo-model-identity.py.txt' -o "$d/mlgo-model-identity.py.txt" && printf '%s  %s\n' 'f5e48b4e9fc6d4934c510ddda00af38cc032fc6e9558534ee40a2d819dda19f4' "$d/mlgo-model-identity.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 90 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/preflight-base-qb.py.txt' -o "$d/preflight-base-qb.py.txt" && printf '%s  %s\n' 'd42d138f170c3e5ae7784951d14719b15e1dc2df18fe075191aea7a310ae78c5' "$d/preflight-base-qb.py.txt" | sha256sum -c - && mkdir -p "$PWD/workspace/temp/pm0004-native-lock" && flock -n "$PWD/workspace/temp/pm0004-native-lock/heavy.lock" python3 -B -u "$d/mlgo-kernel-replay.py.txt" "$d/mlgo-model-identity.py.txt" "$d/preflight-base-qb.py.txt")
```

The replay prints vdlinux from baseline CL 14293732 to a new `pm0004-kernel-src.*`, overlays the Linux files in shelf 14427407, and applies shelf deletions in that scratch copy. It stages both fixed Base snapshots and hashes the RPMs. Matching Custom preflight RPMs and OBS buildinfo are discovered automatically. When unavailable, `SNAPSHOT_SHA256_ONLY` records the evidence level. It prints the compiler versions, ELF hashes and selection by Base and host/target role. When a published accelerator resolves to a unique x86_64 Clang ELF it is exercised as the standalone host lane. QB effective compiler identity remains pending until the actual job evidence is available. [Perforce print to a local tree](https://help.perforce.com/helix-core/server-apps/cmdref/current/content/CmdRef/p4_print.html)

The script uses `ARCH=arm LLVM=1 CROSS_COMPILE=arm-linux-gnueabi-` and serial Kbuild to configure `KANTSU2E_perf_defconfig`, prepare headers and capture actual object commands for `kernel/sched/core.c`, `mm/page_alloc.c` and `kernel/fork.c`. Seed builds force heuristic advisors through the compiler wrapper so the replay can record release failures independently. The four-mode matrix uses the captured Kbuild flags and a shared probe. It prints raw object SHA-256, inline remarks and function-level spill/reload counts per Base. Any pure IR also gets a labelled native diagnostic. Expect identical objects in (d) and differences in (a)–(c). Preserve every deviation and compiler error. [Linux Kbuild LLVM options](https://docs.kernel.org/kbuild/llvm.html)

## H. Official versus Customized Product payloads

**Native server.** Once the immutable Product artifacts URL arrives, set the Bash array `PRODUCT_ARGS` to that single URL. The full pass downloads and checksum-verifies both RPMs when a pair is resolvable. It processes one pair at a time and releases its scratch RPMs after comparison. Estimate several hours and substantial cumulative network traffic for 2,342 installed identities. Disk peaks at one RPM and one unpacked member plus metadata and reports. The same heavy-job lock as G prevents overlap.


```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 90 'https://raw.githubusercontent.com/lhmax2010/analysis/883702685e2dbfb82b29fe190e45b01b44c57732/artifacts/scripts/r0004/mlgo-image-compare.py.txt' -o "$d/mlgo-image-compare.py.txt" && printf '%s  %s\n' 'aa7a93f16b9848d806641a4b16e0933b873179f9c13cde53feed493fa1fd1919' "$d/mlgo-image-compare.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 90 'https://raw.githubusercontent.com/lhmax2010/analysis/ea24f17d8d8f7b245c36d040381880839165d1c5/artifacts/scripts/r0004/preflight-base-qb.py.txt' -o "$d/preflight-base-qb.py.txt" && printf '%s  %s\n' 'd42d138f170c3e5ae7784951d14719b15e1dc2df18fe075191aea7a310ae78c5' "$d/preflight-base-qb.py.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 90 'https://raw.githubusercontent.com/lhmax2010/analysis/8d8fa62a06219d536d54ffc61c8a27bae123268f/artifacts/scripts/r0004/mlgo-model-identity.py.txt' -o "$d/mlgo-model-identity.py.txt" && printf '%s  %s\n' 'f5e48b4e9fc6d4934c510ddda00af38cc032fc6e9558534ee40a2d819dda19f4' "$d/mlgo-model-identity.py.txt" | sha256sum -c - && if [[ "${PRODUCT_ARGS[0]:-}" == --readback ]]; then python3 -B "$d/mlgo-image-compare.py.txt" "$d/preflight-base-qb.py.txt" "$d/mlgo-model-identity.py.txt" "${PRODUCT_ARGS[@]}"; else mkdir -p "$PWD/workspace/temp/pm0004-native-lock" && flock -n "$PWD/workspace/temp/pm0004-native-lock/heavy.lock" python3 -B -u "$d/mlgo-image-compare.py.txt" "$d/preflight-base-qb.py.txt" "$d/mlgo-model-identity.py.txt" "${PRODUCT_ARGS[@]}"; fi)
```

The fixed old Product is `TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261117.2`. Baseline matching uses installed NEVRA. Candidate matching uses unique package name and architecture. The corresponding Base is searched for entries absent from Product, with each route recorded. Missing or ambiguous matches remain unresolved. The tool computes non-LLVM Base membership from both pinned Base inventories and distinguishes binary identity matches from source RPM matches.

Kernel results include image file sizes, shipped module totals, top per-module deltas and available vmlinux sections. The retained package report records every in-scope package status, member changes and changed ELF paths, including ELF members of recognized ZIP-based TPK/WGT containers. The report flags changed user-space ELF and other payload members, unreadable containers, and RPM differences outside the non-LLVM delta as confounders. The bound is the baseline installed roster. Candidate-only installed packages require a fresh on-board RPM inventory when the image boots.

For full terminal readback, reuse the launcher with `PRODUCT_ARGS=(--readback "$image_run_dir" --page 1)` and increment the page. Include `--all-packages` to return identical package records too. Readback is local and normally takes seconds. It prints up to 100 rows per page.

## I. KantSU2E collection and image switching

**Review before use. Stage from native, then run on the board.** Set `TV_SERIAL` to the attended KantSU2E SDB serial. Staging normally takes under a minute with an installed ARM Linux cross GCC and static runtime. It uses light native CPU, a small static benchmark executable and the SDB link. The same verified sources and the same built microbenchmark SHA-256 must be used on both images. The board-side files live under `/root/llvm-pm/pm0004-mlgo`.


```bash
(set -o pipefail; cd /home1/chengkai/vd-tree && d=$(mktemp -d "$PWD/workspace/temp/pm0004-tools.XXXXXX") && export TMPDIR="$d" && curl -fsS --connect-timeout 8 --max-time 90 'https://raw.githubusercontent.com/lhmax2010/analysis/883702685e2dbfb82b29fe190e45b01b44c57732/artifacts/scripts/r0004/mlgo-tv-stage.sh.txt' -o "$d/mlgo-tv-stage.sh.txt" && printf '%s  %s\n' '567df3912d0d2f8334f22a29320b53ed49f3b9c37b796ac410e9bd6cd0875f1c' "$d/mlgo-tv-stage.sh.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 90 'https://raw.githubusercontent.com/lhmax2010/analysis/883702685e2dbfb82b29fe190e45b01b44c57732/artifacts/scripts/r0004/mlgo-tv-measure.sh.txt' -o "$d/mlgo-tv-measure.sh.txt" && printf '%s  %s\n' 'a1a6535ca42a1e6f5ce88c7198d0e3ca84236aa760d8f71d54f6b7bc36b5d586' "$d/mlgo-tv-measure.sh.txt" | sha256sum -c - && curl -fsS --connect-timeout 8 --max-time 90 'https://raw.githubusercontent.com/lhmax2010/analysis/883702685e2dbfb82b29fe190e45b01b44c57732/artifacts/scripts/r0004/mlgo-tv-microbench.c.txt' -o "$d/mlgo-tv-microbench.c.txt" && printf '%s  %s\n' '9ece8727da564d33a069b69ccf7187aa43b0f8e803b9c51a6a1e11b5ae776a2e' "$d/mlgo-tv-microbench.c.txt" | sha256sum -c - && bash "$d/mlgo-tv-stage.sh.txt" "$d" "${TV_SERIAL:?set the attended KantSU2E SDB serial}")
```

Run the commands in the board shell with `lane=official` or `lane=custom`, and `measure=/root/llvm-pm/pm0004-mlgo/measure.sh`.

| Measurement | Invocation and protocol |
|---|---|
| Boot, five per image | `"$measure" boot "$lane" "$run" "$home_pid"` after Home is usable. Use a full cold power cycle for runs 1–5. The script checks a distinct boot ID and reports kernel-to-Home process start and operator-observed readiness as separate elapsed times. Use the same Home process identity and connection method on both images. The observed value includes the operator and SDB delay. |
| Kernel microbenchmarks | `"$measure" micro "$lane" "$cpu"`. The binary warms up and runs five trials pinned to the same permitted CPU. It records gettid latency, pipe round trips and first-write anonymous page fault latency. Keep the CPU policy, ambient load and thermal conditions matched. Expect seconds and about 16 MiB of transient mapping with 4 KiB pages. |
| 4K playback, three per image | `"$measure" playback "$lane" "$run" 60 "$drop_counter" "$player_pid"`. Append other relevant decoder PIDs as separate arguments. Use the same stream, USB device, player path and steady-playback window after the same warm-up. Record system CPU and process CPU normalized to one core, plus the delta of a verified monotonic player/decoder drop counter. Use `NA` when that counter is unavailable and report the measurement gap. PID replacement or a counter reset invalidates the sample. |
| Terminal return | `"$measure" summary "$lane"`. Return both summaries with the image and stream SHA-256, device/firmware identity and benchmark SHA-256. Export the first lane before flashing, since a flash may replace `/root`. |

Boot, benchmark and playback measurements run separately. The CPU sample uses `/proc/stat` and process ticks, and keeps the raw board records. Compare the run values and medians per image. Record visible stalls or failures alongside the per-image frame-drop results.

### Attended flash and rollback

1. Record the exact KantSU2E model, loader/firmware and SDB serial. Resolve and archive the complete Official and candidate flash bundles from the two QB jobs locally, including their manifests and SHA-256. Use the QB flash bundle manifest to identify the flashable image. Record the project's approved installer, board-specific flash command, partition mapping and recovery procedure before the first switch. The existing handover does not contain those commands.
2. While the Official image runs, verify its identity on the device and record boot/playback smoke. Run and export the Official measurements, save the relevant board configuration through the established board procedure, and confirm that the known-good Official bundle and recovery access are available.
3. Bring up the candidate using the approved KantSU2E procedure in the attended session. Verify board serial, expected boot/kernel and image identifiers, SDB, HomeUI and test media. Stage the same benchmark artifacts and take the candidate measurements.
4. If the candidate fails to reach expected boot, HomeUI, SDB or playback, capture the visible state and logs. Use the established recovery entry and reinstall the verified Official bundle with the recorded loader/partition mapping. Check the restored identity, Home and playback. Use the same rollback sequence to restore the control after the comparison if needed. The scripts collect measurements only. [Recovered flash evidence and gaps](../../handover/03_sources_rpms_image.md)

Python 3.10.12 fixtures checked G and H, including shelf overlays, kernel commands, both Base modes, RPM/ZIP payload comparison and paged output. The C benchmark passed a local five-trial run and both shell scripts passed syntax checks. Live P4, Product, QEMU and KantSU2E validation are pending. These are review drafts. All native GitHub operations are downloads.
