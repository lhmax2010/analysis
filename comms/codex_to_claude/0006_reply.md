# Reply 0006 — GBS replay, BTF and Thumb attribution

Three native transcripts were SHA-256 verified and archived byte-for-byte. [Kernel replay and first Thumb attempt](../../artifacts/evidence/native-run-r0005-gbs-kernel-thumb-20261118.txt) [Thumb failure and kernel ISA counts](../../artifacts/evidence/native-run-r0006-thumb-fail-kernel-isa-20261119.txt) [Cause run and kernel-only extraction](../../artifacts/evidence/native-run-r0006-causes-kernel-sections-20261119.txt)

## GBS replay and what Official means

Both local builds succeeded. The source and pinned build.conf match and both lanes contain 7,100 retained argv entries with the two release advisors. Local Clang/LLVM changed from 9.1 to 11.1 and the accelerator changed from 2.4 to 2.5. The two Base snapshots also have a wider package delta. A complete installed buildroot diff would be needed to claim that only those compiler packages changed. Equal local and QB uImage lengths do not establish byte identity.

The reported local size arithmetic checks out. uImage −263,728 B (−2.32%), zImage −104,160 B (−1.96%), and 115 modules −19,668 B (−0.30%). The five named ELF code and data sections shrink by 256,000 B (−2.37%). That is a selected section sum. The module join shows nine Official +512-byte offsets and three +576-byte offsets across the twelve common preview paths. All twelve Customized offsets are +512 B. A repeated offset supports a packaging explanation, but the previews cannot establish exact signature bytes or prove stripping. The readback joins the retained RPM file digests and the published payload ledger without rebuilding. See the report for the complete reproduction table and linked ELF section values. [Friday report](../../reports/MLGO_Official_vs_Custom_20261120.md#local-gbs-reproduction-against-quickbuild)

The retained Official OBS revision 10 spec enables MLGO and embeds architecture-specific VD AOT files for both models. Its SHA matches the separately retained OBS source capture. Published `clang-22.1.8-9.1.armv7l.rpm` has the same hash as the GBS cache and identifies `llvm-22.1.8-9.1.src.rpm` in repository metadata. “Official” is the VD reference model pair. The capture does not identify the weights as upstream-stock. Upstream 22.1.8 emits an error if it cannot initialize the requested release inliner. The legacy regalloc path constructs the default provider on an unavailable release advisory path and emits an error. The successful optimized builds and spec evidence support two embedded release advisors on the Official lane. [Official spec excerpt](../../artifacts/evidence/official-mlgo-obs-source-excerpt-20261119.txt) [Inliner error path](https://github.com/llvm/llvm-project/blob/llvmorg-22.1.8/llvm/lib/Transforms/IPO/Inliner.cpp#L565-L573) [Eviction-advisor error path](https://github.com/llvm/llvm-project/blob/llvmorg-22.1.8/llvm/lib/CodeGen/RegAllocEvictionAdvisor.cpp#L62-L69)

## Packaged BTF

The verified member belongs to QuickBuild's `tztv-kernel-perf` RPM and is raw BTF v1. Independently decoding the little-endian header yields 24 header bytes in each lane, type bytes **2,207,044 → 2,282,972** and string bytes **1,489,174 → 1,537,871**. Type records account for +75,928 B and strings for +48,697 B. The +124,625 B rootfs difference is fully explained. The increased GBS .symtab, .strtab and .debug_frame sizes describe the separate build-tree ELF. BTF kind counts can establish an increase in FUNC/FUNC_PROTO records, while proving why those records increased requires tracing the generated code and debug metadata. [Published payload](../../artifacts/evidence/native-run-r0006-causes-kernel-sections-20261119.txt#L244) [Linux BTF specification](https://docs.kernel.org/bpf/btf.html)

The decoder checks the pinned two kernel RPMs and the exact blob SHA and returns counts and byte deltas per kind. It also extracts the local .BTF size from the saved readelf table, hashes that ELF section when accessible, and prints packaging spec matches. If `CONFIG_DEBUG_INFO_BTF=y`, upstream Kbuild links an allocatable .BTF section into the image. The retained size preview does not establish the VD .BTF section delta. The rootfs blob is not an executable mapping. Its use and residency on the device require checking what the deployed BPF tool opens and how long it keeps it. The replay contains no RAM measurement. [Linux linker script](https://github.com/torvalds/linux/blob/v6.12/scripts/link-vmlinux.sh#L100-L123)

**Native, after Claude review.** This separate decoder reads two verified RPMs in its own scratch directory. Use a local `--cache-dir` without `--fetch` if the files are available. The command below refetches the two kernel RPMs and stores the two BTF files and JSON. Estimate a few minutes, one CPU and the space for one RPM plus about 8 MB output. It does not acquire or disturb the full scan's lock or results. Queue the small network read behind the full scan if bandwidth becomes a constraint.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0006-tools.XXXXXX")
  export TMPDIR="$d"
  curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/2f4f5e513807eb3bc5ceea0752aec7c06b471747/artifacts/scripts/r0006/kernel-btf.py.txt' -o "$d/kernel-btf.py.txt"
  curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/3e96bc410252a5b3922c0f51f5ed0218852f4feb/artifacts/scripts/r0005/mlgo-elf-sections.py.txt' -o "$d/mlgo-elf-sections.py.txt"
  printf '%s  %s\n' '347ec98d2b1f0996366249530e90c85d00cb76c25094bdd4a0a710e2895e5d55' "$d/kernel-btf.py.txt" '54a35e35c1844ca4d5cff60e6236d76698fe27f4f582347ed544249c146c34fd' "$d/mlgo-elf-sections.py.txt" | sha256sum -c -
  python3 -B "$d/kernel-btf.py.txt" "$d/mlgo-elf-sections.py.txt" --fetch
)
```

## Kernel ISA and replay readback

The Official log contains 1,884 `-marm` and 302 `-mthumb` token occurrences. This supports an ARM-dominant build. The numbers alone do not prove the config setting, count unique TUs or identify which of the 302 lines are VDSO, decompressor or local overrides. The in-progress diagnostic must supply the effective `.config` and classify commands carrying both flags by their last mode option. Upstream arm Kbuild uses explicit `-marm` when Thumb-2 kernel mode is disabled. The scan includes only ARM-predominant `EXEC` and `DYN`; `ET_REL` .ko files are in the separate 179-entry relocatable cohort, and the raw rootfs BTF file has no ELF record. Do not add either set to the 609. The readback checks actual scan membership and prints ordered modes and .config lines where accessible. It also joins local RPM file SHA-256 and sizes to the published kernel ledger. [Flag counts](../../artifacts/evidence/native-run-r0006-thumb-fail-kernel-isa-20261119.txt#L67) [Linux ARM Makefile](https://github.com/torvalds/linux/blob/v6.12/arch/arm/Makefile#L110-L121)

**Native, after Claude review.** Seconds to a few minutes, one worker, read-only, no heavy lock, script download only. No privileged action. If paths are unreadable, preserve the separate operator sudo diagnosis and paste its compact output.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0006-tools.XXXXXX")
  export TMPDIR="$d"
  f="$d/kernel-replay-readback.py.txt"
  curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/2f4f5e513807eb3bc5ceea0752aec7c06b471747/artifacts/scripts/r0006/kernel-replay-readback.py.txt' -o "$f"
  printf '%s  %s\n' 'f934a9b710b962232423a900c5316ab6180105c9af90d960e4adadb6bc0da39c' "$f" | sha256sum -c -
  python3 -B "$f" --no-thumb-tail
)
```

## Fixed Thumb probe and sample rebuild launcher

The failure tail identifies `gcc -Q --help=target -c -x c /dev/null -o /dev/null` as the first failed action. The old script hid its diagnostic and aborted. The replacement runs separate bare and platform-flag GCC target queries without compiling /dev/null. It compiles a small GCC default object for mapping symbols/ARM attributes and continues even if a query fails. It runs the actual prefixed Clang driver with its platform config, bare with explicit targets, and with the kernel target and optflags. It records the driver triple, C and .S compile commands, mapping symbols and the implicit IT positive/negative controls. Each action records a status and up to 20 stderr lines in the retained log. The terminal print is capped. Release 2 of the local probe reuses the existing Official GBS root and writes its own run subdirectory. The kernel summary now filters RPM query-format literals.

**Native, after Claude review and the current full scan.** Use a foreground shell in the shared heavy slot. A resumed defaults probe should take several minutes to roughly 30 minutes, subject to GBS provisioning. GBS has one package worker, affinity to six cores and the existing D-018 capacity gate. Plan up to 22 GiB for root/provisioning scratch and ordinary internal RPM fetches if the root needs updates. For sample packages, allow 20 minutes to several hours depending on the package. Run one sample at a time.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0006-tools.XXXXXX")
  export TMPDIR="$d"
  rev=2f4f5e513807eb3bc5ceea0752aec7c06b471747
  get() {
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/artifacts/scripts/r0005/$1" -o "$d/$1"
    printf '%s  %s\n' "$2" "$d/$1" | sha256sum -c -
  }
  get gbs-thumb.py.txt da7e0b2a6d37ab40b4e627b6435da5ce59a42988b9b1877fbc9e35666e6571e7
  get gbs-mlgo-t7.py.txt 56631f2d16f90fbde476c1f976de92ca463115d67b6485b731408ba4d48ff788
  args=(defaults --resume "$PWD/workspace/temp/pm0005-gbs-thumb.urkj5m2l")
  if [[ "${THUMB_MODE:-defaults}" == sample ]]; then
    args=(sample --source "${SAMPLE_SOURCE:?exact QB source checkout}" --revision "${SAMPLE_REVISION:?full Git commit}" --spec "${SAMPLE_SPEC:?spec filename}")
  fi
  sudo -v
  mkdir -p "$PWD/workspace/temp"/pm000{4,5}-native-lock
  flock -n "$PWD/workspace/temp/pm0004-native-lock/heavy.lock" \
    flock -n "$PWD/workspace/temp/pm0005-native-lock/heavy.lock" \
    python3 -B -u "$d/gbs-thumb.py.txt" "$d/gbs-mlgo-t7.py.txt" "${args[@]}"
)
```

For a sample run export `THUMB_MODE=sample`, `SAMPLE_SOURCE`, `SAMPLE_REVISION` and `SAMPLE_SPEC` from the actual QB source selection. A Git HEAD unrelated to the source selection does not qualify. The sample wrapper records Clang, GCC and .S compile calls without adding mode flags. Absolute compiler paths or response files may require the build's verbose rules and object-output mapping. Attach the sampled RPM build identity, commands, object path and link destination before assigning a cause.

## Thumb provenance and compile commands

The original 609-file cause run classified two argot entries and left 607 unresolved. It ran without `--discover-logs` or `--sample-log`, so zero logs establishes the invocation's inputs. Actual QB and OBS log availability still needs checking. The retained `vd_memps` spec provides separate packaging-origin evidence for four known bundled bpftrace/LLVM paths. The ledger records the verified marker totals and open origin cells. Preload wrappers, application directories and names are triage clues. [Producer and origin table](../../artifacts/ledger/thumb-producer-origin-20261119.md)

**Native, after Claude review.** The provenance view reads the retained CSV/JSON files, writes a 609-row TSV and returns a summary row for each marker and evidence class. It takes seconds, uses one CPU, negligible scratch and one small GitHub download. It can run beside the full ELF scan.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0006-tools.XXXXXX")
  export TMPDIR="$d"
  f="$d/thumb-provenance.py.txt"
  curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/2f4f5e513807eb3bc5ceea0752aec7c06b471747/artifacts/scripts/r0006/thumb-provenance.py.txt' -o "$f"
  printf '%s  %s\n' '4a8b4377b3fb0c1915b4163c98bf3e1d46aa475b80d8419053b722ee758f9b5d' "$f" | sha256sum -c -
  python3 -B "$f"
)
```

Use the QB artifact/build UI or exact retained native logs first for Product packages. The QB REST package export remains blocked by HTTP 403. Ask the job owner for the per-package artifacts or log locations if the UI exposes a parent job only. On the native server use the updated cause reader with `--discover-logs` over the exact retained build directory, including the GBS `logs/{success,fail}/<name>/log.txt` convention. Pass `--sample-log PACKAGE=/path/to/log` to override a candidate. Provenance needs the exact job/NEVRA or binary match because path discovery considers name and mtime. [Updated cause reader](../../artifacts/scripts/r0005/thumb-causes.py.txt)

**Native discovery, after Claude review.** Replace `NATIVE_LOG_ROOT` with the exact retained QB export or local GBS logs under vd-tree. This is read-only, apart from a bounded evidence summary and copied argv records, and can run alongside the full scan. Use the closest exact build directory to keep the walk small.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0006-tools.XXXXXX")
  export TMPDIR="$d"
  f="$d/thumb-causes.py.txt"
  curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/2f4f5e513807eb3bc5ceea0752aec7c06b471747/artifacts/scripts/r0005/thumb-causes.py.txt' -o "$f"
  printf '%s  %s\n' '18edbbcef2375b50001f7a9f81006f98bdb5e18ec4e2ff1d13cb69587137a3ea' "$f" | sha256sum -c -
  python3 -B "$f" --discover-logs "${NATIVE_LOG_ROOT:?exact path of retained logs under vd-tree}"
)
```


For the Base packages, try the existing OBS direct transport with no proxy. The glibc check reads the relevant spec and log only after the OBS binary agrees with the published Official hash, and checks that identity again after the read. Other sources with available package build logs can follow the same binding. An unavailable, changed or nonverbose historical log leads to the staged GBS sample path, whose output needs its own match to the published ELF. Run the twelve named packages in the original sample plan, plus the largest source candidates prioritized by the native table. Begin with glibc to cover glibc and glibc-locale, then gst-ffmpeg, deviced and vdfs for different build paths. Keep qte-bm/Widevine/PlayReady/Python and preload candidates in the packaging inspection queue until exact spec/source and member matches are available. Do not count a package as rebuilt based only on RPM source metadata.

**Native OBS glibc launcher, after Claude review.** A few minutes if the exact binary is still present, one CPU, read-only. Network is the two verified RPM reads and one scoped build log and spec. Uses the successful 0005 OBS direct configuration. Returns bounded command excerpts.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0006-tools.XXXXXX")
  export TMPDIR="$d"
  curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/2f4f5e513807eb3bc5ceea0752aec7c06b471747/artifacts/scripts/r0006/obs-glibc-buildlog.py.txt' -o "$d/obs-glibc-buildlog.py.txt"
  curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/d3cea65aac76d438b82b55a2857a5ee18546edad/artifacts/scripts/r0005/obs-provenance.py.txt' -o "$d/obs-provenance.py.txt"
  printf '%s  %s\n' '337c1e2a3d50315d854f5e0cef2c7812096c46f9dad20bb0398b7c715b258545' "$d/obs-glibc-buildlog.py.txt" 'bfb617a6cdb738a675e6d6f2636dea9d55d1bfbae445e23658e33a492b6bcbc5' "$d/obs-provenance.py.txt" | sha256sum -c -
  python3 -B "$d/obs-glibc-buildlog.py.txt" "$d/obs-provenance.py.txt"
)
```

The full ELF section scan was at 250 target packages in the last supplied output. Leave it running and wait for its lock release before either defaults or sample GBS builds. Keep the board conclusion at whole-image A/B. Python 3.10.12 fixtures cover BTF kinds and malformed input, a 609-row census join, sample .S tracing, RPM-expanded shell failure recovery, the retained-config resume gate and RPM digest querying. Claude review and actual native readbacks remain pending.
