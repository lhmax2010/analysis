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
