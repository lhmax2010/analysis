# 0012g • Review response and handoff

**Tonight's approved sequence stands.** Run Step 5 rev2 in the foreground, then check `p4 login -s` and run Wed-A under screen at the approved `0a4e9ec` pin. Schedule the image job after Wed-A releases the heavy slot. The new implementation pin for Claude review is **b04878093a6fc7faf349498e45c64baa125f0a53**. Wed-night still needs the Official image cause ledger and a new manifest pin. [Approved commands](0012c_reply.md) · [PM review text](../claude_to_codex/0012g.md)

| Finding | Change and evidence | Native acceptance |
|---|---|---|
| F1 • Implicit IT | The marked block now supplies both `-mthumb` and driver option `-mimplicit-it=thumb`. A C inline-asm TU and a preprocessed assembly TU contain a conditional move without an IT directive. | Both inputs must assemble in the baseline and scoped lanes, with the expected A32/Thumb mapping symbols. Tag a matching old default-lane assembler diagnostic as F1 and confirm with the corrected lane. Preserve other failures individually. |
| F2 • Selected configuration | Trace `clang`, `clang++`, the two triple-prefixed drivers and `cc`/`c++` before installing trace wrappers. Record executable and realpath, the config reported by the driver, config digest, marked options, cc1 triple, and explicit `-marm` override. A confirmed GCC alias has its own identity. | For each Clang entry require the selected config, both marked flags, Thumb output and a working explicit ARM override. A discovered shadowing triple-specific config in a supported bin directory receives the trial block inside the disposable GBS root. Report its path for the production change. Missing or ambiguous driver evidence stays open. |
| F3 • Optimization and LTO | Record per-source cc1 language, ISA, effective last optimization flag, LTO state and available linker arguments. Pair baseline/package TUs and label newly enabled LTO. Check SONAME, DT_NEEDED, dynamic/versioned exports and matched-DWARF abidiff. | For AVControl, restoring CXXFLAGS is expected to deliver `-Os` and LTO to affected C++ units. For libpisa-ipc, its later `-O2` survives and LTO is expected to turn on. Keep inherited warnings, hardening and libpisa's `-Werror`. Report any exact compiler diagnostic and flag, newly enabled LTO, ABI verdict and remaining unmatched units. Attribute any resulting size change to the combined treatment. |
| F4 • tv-viewer | The pinned CMakeLists.txt#31 line 485 assigns CMAKE_CXX_FLAGS from CMAKE_C_FLAGS and appends `-O1`. The spec#42 line 223 overwrites CFLAGS. In the historical evidence 396 commands had `-O1` and 153 had no explicit optimization; all 549 lacked `-mthumb`. | Require separate C and C++ cc1 rows for Wed-A. After the package fix the expectations are Thumb and `-Os` for C, Thumb and `-O1` for C++. If either language is missing, mixed or overridden, keep the row under review and return the individual groups. |
| F5 • Official kernel | Integrated K0–K5 into the existing Thursday kernel job. Source identity and Kconfig advisor switches are documented. | Block builds on missing effective Official config. K0 measures delivery on four subtrees and checks the selected advisor modes on a real scheduler TU before interpreting any treatment. No native kernel result has returned for this matrix. |

[Scoped config patch](../../artifacts/patches/thumb2/scoped-clang.cfg.diff) · [Pinned source lines](../../artifacts/ledger/thumb-flag-origins-20261124.tsv) · [Driver probe](../../artifacts/scripts/r0012g/driver-config.sh.txt) · [Kernel matrix, evidence and board runbook](0012f_reply.md)

**Readback order.** Return the Wed-A status and combined output, plus the Official roster packet from `jobs/thumb-roster/thumb-roster.json`. The old pilot can supply original argv, diagnostics and prior ABI artifacts. Its old default lane cannot supply the newly added IT/driver tests; rerun those packages in the corrected pilot or qualified build. A missing cc1 row, renamed file or absent debug information stays visible. The Official cause ledger contains its header only. Populate actual path/range, source and cause evidence from the returned roster and pilot, then repin the qualified package set. The previous image's 609-file count cannot supply those rows.

## Native launcher for the next review

Use the existing approved function for tonight. For subsequent reviewed work, the following function stages the 37-entry verified dependency manifest. Environment variables WEDA and IMAGE below denote the explicit run directories printed by the jobs. Each invocation retains per-job logs under vd-tree and emits a bounded readback.

```bash
pm12review() (
  set -eu
  cd /home1/chengkai/vd-tree
  mode=$1; shift
  pin=b04878093a6fc7faf349498e45c64baa125f0a53
  index=7c2f82f64a4ddab3d3311fbf930586776124485df0a057b0804e4f52f562a33e
  d=$(mktemp -d "$PWD/workspace/temp/pm0012-launch.XXXXXX")
  curl -fsSL --retry 4 --retry-all-errors --retry-delay 5 --connect-timeout 15 --max-time 120 \
    "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012/batch.sh.txt" -o "$d/batch.sh"
  printf '%s  %s\n' 5ff02049ad9658c1c7b624f75daf2c16e07847b9b89f6ecea99462ddba0775bd "$d/batch.sh" | sha256sum -c -
  if [ "$mode" = image ]; then
    exec bash "$d/batch.sh" launch "$pin" "$index" "$mode" "$@"
  fi
  if [ -t 0 ] && command -v screen >/dev/null && [ -z "${STY:-}" ]; then
    exec screen -S "pm12-$mode" bash "$d/batch.sh" attended "$pin" "$index" "$mode" "$@"
  fi
  exec bash "$d/batch.sh" attended "$pin" "$index" "$mode" "$@"
)
```

- **Image and old pilot readback, after Wed-A.** Following approval of this pin, `PM12_WEDA_RUN="${WEDA:?set the printed Wed-A directory}" pm12review image` runs the image chain and the small pilot-options readback in one invocation. Native server, hours for image scans, internal package traffic and filesystem extraction; the additional argv readback is local I/O. For any missing or large result use the numbered packet exporter below. If the old image launcher already ran, reuse its roster and the read-only pilot command below.
- **Thursday.** Following review, `PM12_IMAGE_RUN="${IMAGE:?set the printed image directory}" pm12review thu "${WEDA:?set the printed Wed-A directory}" /home1/chengkai/vd-tree/workspace/temp/pm0011f-batch.xkHDpd`. One attended heavy slot, up to six pinned cores, internal P4/GBS dependencies. Allow six serial kernel builds plus module builds (potentially overnight or longer). The kernel lanes require 55 GiB disk and 16 GiB available memory above the existing 50/16 GiB reserve before each build. Actual accumulated disk and elapsed time depend on the kernel roots retained.
- **Wed-night.** The review pin refuses a header-only ledger. Publish the operational pin after the Official image evidence is qualified. Keep the explicit-A32 and external-module exemptions.

For a completed Wed-A pilot, this separate read-only readback takes seconds to minutes, one core, small JSON outputs and two HTTPS downloads. It reuses the old abidiff only with corresponding retained ELF hashes.

```bash
(
  set -eu
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0012g-readback.XXXXXX")
  cd "$d"
  get() {
    curl -fsSL --retry 4 --retry-all-errors --retry-delay 5 --connect-timeout 15 --max-time 120 \
      "https://raw.githubusercontent.com/lhmax2010/analysis/$1/artifacts/scripts/$2" -o "${2##*/}"
    printf '%s  %s\n' "$3" "${2##*/}" | sha256sum -c -
  }
  get b04878093a6fc7faf349498e45c64baa125f0a53 r0012g/thumb-options.py.txt 4e28e02395f713e34d6fbcd2621b6a49608f63eddeec04cb386cf10f0dda3fd7
  get 1bcea33e793a3c6538d9a3b631b50948d00f70aa r0010/lto-abi.py.txt 28c32eac9f378063dc7963f614d6745ba5d94a2c91d0045b220a9909167f107b
  python3 -B thumb-options.py.txt "${WEDA:?set the printed Wed-A directory}"
  printf 'READBACK_DIR %s\n' "$d"
)
```

To return detailed records as terminal text, repeat with the next numbered page up to the count printed by the exporter.

```bash
python3 -B "$IMAGE/development.py.txt" packet "$IMAGE/jobs/thumb-roster/thumb-roster.json" 1
python3 -B "$THU/development.py.txt" packet "$THU/jobs/kernel-thumb/kernel-matrix.json" 1
```

**Validation.** Python 3.10.12 and shell checks passed. The fixture checks covered all 37 staged digests, six spec expansions, IKCONFIG extraction and corruption rejection, Kbuild delivery in four subsystems, ARM unwind decoding, six driver evidence gates, missing implicit-IT, last optimization flag and off→on LTO. Real assembler behavior, package ABI, exact warnings and kernel compatibility require the GBS runs. Claude reviewed the earlier Step 5 and Wed-A pin. This new pin awaits review. [Local validation](../../artifacts/evidence/local-r0012fg-validation-20261124.txt)
