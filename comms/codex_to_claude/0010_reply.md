# Round 0010 and 0010a reply

The [round 0011 runbook](0011_reply.md) supplies the active QB identities and refreshed Steps 2–3.

## A. Weekly report backup

The nine original files are stored under `reports/weekly/2026-11-20/` in commit `55c09b4e4b7824d0cce42ece2d76bd2d27dd2944`. Running `sha256sum -c SHA256SUMS` returned eight `OK` entries and exit 0. The manifest is itself preserved byte-for-byte. [Archive and index](../../reports/weekly/2026-11-20/README.md)

## C. Full 609-file A32 ledger

| File | SHA-256 |
|---|---|
| [A32 ledger](../../artifacts/thumb-repro/a32-full-609.csv) | `4f0a76b186e906be4042a1eb9860b33292e30eb6f75dd31ba383342f5cdcf43a` |
| [Cause and family summary](../../artifacts/thumb-repro/a32-full-609-summary.md) | `e30e5188baf8d306c6d47c7f8829f2ffbdc330026d618324fe077abcbbe571dc` |
| [Original native evidence](../../artifacts/evidence/native-run-r0010-a32full-olevel-20261120.txt) | `5c0554c8932bbfdfb401f4810035b9b8b25eb8ad3ca712a5e44fd2d13e51032f` |

The pinned scan records **343.1 MiB** of estimated A32 code across the 609 files. The top 211 hold about 333.2 MiB and the tail holds about 9.9 MiB. The tail includes 38 sub-KiB estimates. The totals from the row-level rounded values are smaller. The 609 rows join to the installed RPM header SOURCERPM ledger. Of these, 23 also match directly observed board files by recorded owner and path. The other 586 have installed-RPM payload evidence, with a per-file check against the mounted partitions still pending. The PERF RPM roster includes `sys-tools` and the named test and driver packages. In this image, `sys-tools` ships target-side ELF payloads such as `/usr/bin/target_view/python3/bin/python3.5m`. The original Doc 05 claim that it is absent from the TV does not apply to this PERF image. [Board RPM ledger](../../artifacts/ledger/README.md)

**Doc 07 comparison.** Rank, package and path agree across the 40 rows available in an independent retained preview. Fourteen floored estimates differ at ranks **8, 9, 10, 11, 16, 19, 20, 22, 28, 29, 36, 37, 38 and 39**. The summary lists each old and observed value. Ranks 41–211 use the archived report and still need the native export below. The independent return does not carry the mode basis and full shares for ranks 1–211. Five of the 11 original explicit-`-marm` labels lack a positive producer match in the retained board table. I retained those as Doc 07 hypotheses and listed the five exceptions. One tail Bluetooth file has a positive path-and-owner DWARF match. [Mismatch details](../../artifacts/thumb-repro/a32-full-609-summary.md#doc-07-reconciliation)

The WebAPI/Crosswalk category has 94 files, including 70 in the tail. The retained history names an individual `webapi-microphone-pepper-plugin/src/microphone/microphone.gyp`, and retained DWARF identifies both Chromium extension source files and ARM assembly. I found no evidence tying the 94 ELFs to one shared GYP or CMake rule that drops `CFLAGS`. The next package samples must record the specific include chain and actual compile command before we assign this cause. The Glibc class records the Base build's lack of the Product wrapper. The effective GCC ISA of individual objects still needs build evidence. [Family summary](../../artifacts/thumb-repro/a32-full-609-summary.md#estimated-a32-by-package-family)

## B. Optimization-level source mapping and replay

The header join yields **24 shipped exact source names**, **nine with no exact installed source or established alias**, and **one shipped alias candidate requiring spec confirmation**. Two apparent prefix subpackages are unrelated sources. `org.tizen.webappservice-api` belongs to its own SRPM, as does `tvs-api-lite`. In contrast, `rpm-security-plugin` really belongs to rpm, and `nnstreamer-tensorflow2-lite` really belongs to nnstreamer. Doc 05 supplies the candidate `tvs-core` → `libtvs-core`, whose two binary RPMs are installed. The matching spec name has not been verified. Neither spelling of `ug_rct`/ `ug-rct` has a matching installed header in this PERF roster. The content-only or no-loadable-ELF RPMs still appear in the header mapping. [All 34 exact mappings with SRPMs and current code figures](../../artifacts/ledger/olevel-sources-20261120.tsv)

| Doc 04 source | Installed binary RPMs in scope | Code / est. A32 KiB |
|---|---|---:|
| `org.tizen.AVControl` | `org.tizen.AVControl` | 723 / 723 |
| `org.tizen.tv-viewer` | `org.tizen.tv-viewer`, `org.tizen.tv-viewer-theme-resource` | 4918 / 4796 |
| `org.tizen.webappservice` | `org.tizen.webappservice` | 6571 / 40 |
| `libpisa-ipc` | `libpisa-ipc` | 894 / 894 |
| `machine-learning-api` | `NOT_SHIPPED` | — |
| `nnstreamer` | `nnstreamer`, `nnstreamer-core`, `nnstreamer-default-configuration`, `nnstreamer-flatbuf`, `nnstreamer-misc`, `nnstreamer-single`, `nnstreamer-tensorflow2-lite`, `nnstreamer-tizen-sensor` | 6523 / 6235 |
| `rpm` | `rpm`, `rpm-security-plugin` | 2791 / 2784 |
| `source-service` | `source-service` | 193 / 6 |
| `vulkan-utility-libraries` | `NOT_SHIPPED` | — |
| `vulkan-validation-layers` | `NOT_SHIPPED` | — |
| `org.tizen.webserver` | `org.tizen.webserver`, `org.tizen.webserver_popup` | 1596 / 1595 |
| `libiri` | `libiri` | 3 / 0 |
| `libgcrypt` | `libgcrypt` | 648 / 647 |
| `mmi` | `NOT_SHIPPED` | — |
| `mmi-plugins-default` | `NOT_SHIPPED` | — |
| `org.tizen.rct-app` | `NOT_SHIPPED` | — |
| `org.tizen.reminder` | `org.tizen.reminder` | 12 / 1 |
| `rct-service` | `NOT_SHIPPED` | — |
| `reminder-api` | `reminder-api` | 133 / 5 |
| `reminder-service` | `reminder-service` | 44 / 2 |
| `tvs-api` | `tvs-api`, `tvs-api-ipc` | 701 / 8 |
| `tvs-api-native` | `tvs-api-native` | 608 / 17 |
| `tvs-chms` | `tvs-chms` | 226 / 7 |
| `tvs-core` | `ALIAS_REVIEW` · `libtvs-core`, `libtvs-core-apps` | — |
| `tvs-dbms` | `tvs-dbms` | 101 / 3 |
| `tvs-dvb-chms` | `tvs-dvb-chms` | 54 / 2 |
| `tvs-dvbbase-chms` | `tvs-dvbbase-chms` | 24 / 1 |
| `tvs-ewbs` | `tvs-ewbs` | 61 / 2 |
| `tvs-ht` | `tvs-ht` | 240 / 8 |
| `tvs-iss` | `tvs-iss` | 417 / 9 |
| `tvs-list-app` | `NOT_SHIPPED` | — |
| `tvs-nrt` | `tvs-nrt` | 69 / 3 |
| `tvs-util` | `tvs-util` | 384 / 11 |
| `ug_rct` | `NOT_SHIPPED` | — |

### Historical hook and three lanes

The retained 11 November report describes exporting `CCC_OVERRIDE_OPTIONS` from `%clang_force_incompatible` and ending the option set with `%__vd_flags_toolchain_clang`. Its exact expanded string is missing from the retained files I could read. I cannot verify whether the historical string added `-mthumb`. The later `clang-force-options` RPM is a different mechanism and does not resolve that question. The historical readback command below collects the candidate macro and expanded log lines without running them. Lane C prints the original expanded line and reports whether it appends `-mthumb` before the first GBS package run. Lane C remains held without the reviewed historical value. [11 November report](../../artifacts/historical-reports/optimization-analysis-part-01.md#closing-the-gap-and-verification) [Clang driver override syntax](https://clang.llvm.org/docs/UsersManual.html#ccc-override-options)

| Lane | Intervention |
|---|---|
| A | Unchanged spec and build policy |
| B | Append only `-Os` using `CCC_OVERRIDE_OPTIONS`. Preserve the existing ISA and all other options. |
| C | Append the verified, expanded November 11 hook value. Prioritize the original rows 1–4, `libgcrypt`, `org.tizen.webserver`, `rpm` and `nnstreamer`. `libgcrypt` remains a diagnostic reference with the current production setting marked Keep. |

B minus A measures the level intervention. C minus B includes all extra hook changes, potentially ISA, hardening, char signedness and other target options. It still does not isolate ISA alone. EXP-T1 provides the independent default-ISA experiment. A marker or nearly full A32 output is insufficient to attribute the old `-O` improvement to any specific replacement of CFLAGS. The replay records per-ELF `.text`, allocated sections, file size and A32 estimates, and checks linked DWARF compilation units and signed-char flags by build ID. Missing or unrecorded producer flags leave the `-Os` gate open. GNU assembler units are reported separately. Current r0010 image columns are executable-section totals. The archive's first four measured `.text` values were 720, 4,630, 6,534 and 877 KB in Doc 04 order and refer to the 11 November controls. Use like-for-like `.text` from an exact RPM to prove A matches the current matched image. [Historical optimization table](../../reports/weekly/2026-11-20/04_HQ_Table_O_Level.md)

The replay verifies the Official capture, Base 1113.1, published `@14452507` bytes and local 930-shelf input. It matches the observed PERF source roster against the captured Product and Official Base metadata. It stages a pinned P4 revision plus matching shelves. Where metadata and the binary header lack immutable VCS it requires the checksummed matching SRPM. If a re-publication changes installed package selection, revalidate the roster before quoting it for that image. A fault in a single package or lane is recorded and other eligible work continues. No eligible Base source is replaced with a current OBS head.

## D. Monday run order and next-week gates

All commands below run on the native server after Claude review. Select values from the new QBs, never the expired Official Product. The capture and scan use the two existing heavy locks. Phase 1 is independent of the later measurements and should run as soon as each job publishes. Use one heavy job at a time.

### 1. Capture each finished QB

Run once per lane as soon as it publishes. Set `QB_ID` and `QB_PRODUCT_URL` to that job’s numeric ID and fixed Product URL. Optional `QB_IMAGE_SHA256` is the independently published PERF digest. Keep the printed `CAPTURE_DIR` as `OFFICIAL_CAPTURE` or `CUSTOM_CAPTURE` for subsequent commands. Expect `CAPTURE_COMPLETE` and fewer than 100 lines. Budget roughly 5–60 minutes per lane, one transfer stream and the PERF size plus RPMs.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' 'artifacts/scripts/r0007/qb-retain.py.txt' 'a2f8e7ef82b1c330e1d50239f07e3454c2440d1dff8d2773d950fddaf488c2fe'
  get 'd3cea65aac76d438b82b55a2857a5ee18546edad' 'artifacts/scripts/r0005/image-repo-lib.py.txt' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
  args=(capture "${QB_ID:?set the finished job ID}" "${QB_PRODUCT_URL:?set its fixed Product URL}")
  if [[ -n "${QB_IMAGE_SHA256:-}" ]]; then args+=(--image-sha256 "$QB_IMAGE_SHA256"); fi
  python3 -B -u "$d/qb-retain.py.txt" "$d/image-repo-lib.py.txt" "${args[@]}"
)
```

### 2. Verify the matched inputs

After both captures, set the four file variables below to the retained submission copies for the two jobs. This verifies both published configs, the two Base selectors and the pinned submitted lists in seconds. Expect `QB_PAIR_CONFIG_GATE_PASS`. Retain any effective Product source differences, since the publication config and submitted list checks cannot establish source identity.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/scripts/r0010/qb-pair-gate.py.txt' 'ccb0aa3fc65f8964fc04df98b4faf7c50bb812b8e75dec80d9c54a511618a6f7'
  python3 -B -u "$d/qb-pair-gate.py.txt" "${OFFICIAL_CAPTURE:?}" "${CUSTOM_CAPTURE:?}" \
    "${OFFICIAL_SHELVES:?submitted shelf list}" "${CUSTOM_SHELVES:?submitted shelf list}" \
    "${OFFICIAL_BASE_LIST:?submitted no-prelink list}" "${CUSTOM_BASE_LIST:?submitted no-prelink list}"
)
```

### 3. Audit the Official archive and prepare both USB directories

Set `PERF_ACTION=audit` to audit Official. It prints counts and bounded coverage/finding rows. Exit 1 means findings and exit 2 means incomplete scope. Then set `PERF_ACTION=usb` and `CAPTURE` to Official first, then Customized. `USB_PREP_READY` prints the verified staging path. Use the board checklist for the per-file USB copy and BOOST sequence. Audit typically takes 20–90 minutes. Staging takes roughly 5–30 minutes per lane. Both use local file I/O and the 50 GiB reserve plus expanded partition/USB staging space.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-relocations.py.txt' 'f678d0f9c479d6a183c3f83d7a14917ea46c15533f41d97a3baeb732b6905cf7'
  case "${PERF_ACTION:-audit}" in
    audit)
      python3 -B -u "$d/perf-relocations.py.txt" --capture "${OFFICIAL_CAPTURE:?}" \
        --bundle-library "$d/perf-bundle.py.txt" --sample-asan
      ;;
    usb) python3 -B -u "$d/perf-bundle.py.txt" "${CAPTURE:?set the lane capture}" ;;
    *) exit 2 ;;
  esac
)
```

### 4. Export the exact A32 rows and optimization-package paths

This can run independently in a few seconds. The native data packet is under 110 lines per call. Set `A32_PART=2` only if the packet reports a second part. Optional `PERF_TREE` must be an already assembled, provenance-checked rootfs under vd-tree including applicable mounts. An absent path in a partial tree establishes only a coverage gap. The `A32_RESULT_SHA256` covers the complete uncompressed result.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/scripts/r0010/a32-readback.py.txt' '6352e5fbb1df524e9226511624a8e4a16c755a8e863911cf45c6e08188db55c7'
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/thumb-repro/a32-full-609.csv' '4f0a76b186e906be4042a1eb9860b33292e30eb6f75dd31ba383342f5cdcf43a'
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/ledger/olevel-sources-20261120.tsv' '788481656fce951e1434ee44df0acb40c83c44551d2fb590b381664e14151346'
  args=(--part "${A32_PART:-1}")
  if [[ -n "${PERF_TREE:-}" ]]; then args+=(--perf-tree "$PERF_TREE"); fi
  python3 -B -u "$d/a32-readback.py.txt" "$d/a32-full-609.csv" "$d/olevel-sources-20261120.tsv" "${args[@]}"
)
```

### 5. Stage the GBS-built benchmark for board day

Use the verified Official capture. The command makes a single isolated GBS build under the shared lock and prints `GBS_BENCH_READY` then `BOARD_TOOLS`. Budget roughly 10–40 minutes, up to six cores, 24 GiB peak scratch plus reserves and dependency traffic. Reuse this exact tools path and benchmark across both flashes.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010-board.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/scripts/r0010/gbs-board-bench.py.txt' 'ec400673256b6b0ce318aebf33b6336eb785fd0c2a9defba17f5a983cd334db7'
  get '97a50bcacc7402d8297b25a47b1f2117b40c6d72' 'artifacts/scripts/r0010/olevel.py.txt' '7ea4a4c99204ae9a280e83d46a1e3de2b7ff721ce7a8079294e36393401259bf'
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/scripts/r0010/mlgo-tv-run.sh.txt' 'fa28ef445fed4ee573d1504ad0b7b19aad066d9b595cb90ea9a8d53c0aa64f3b'
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/scripts/r0010/mlgo-tv-measure.sh.txt' 'd065017fb0bd825bb9c1ff86ced0616406f414ef7f41b794b35c54fcf17850e4'
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/scripts/r0010/mlgo-tv-microbench.c.txt' '04981794ea071c5d7aef39a911086abf451cb136796e4e8edc6bffa39f66796a'
  get '2303fa18ff0bc39bd26e8b6dc683bbb24bd7611a' 'artifacts/scripts/r0005/mlgo-tv-identity.sh.txt' '21070fc762b878343faac9a331235ad2dfde06eb87cfa7f2f5ac24a5b855e5cf'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-mlgo-t7.py.txt' '1089c21b3b4bf4205bd13ba64cace371c57a7d4ec86376877f3b2d069f551a9c'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-thumb.py.txt' '928cff87ac0cb501a6d0575da5f1d80157bd02918d2378a5e061c2262cf11a92'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/thumb-qb-sample.py.txt' 'b7a725e9c5e68072b9f5388a35df91494874f13f67a00fb7426a3067e04a3579'
  get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  (cd "$d"; sha256sum mlgo-tv-identity.sh.txt mlgo-tv-measure.sh.txt mlgo-tv-microbench.c.txt > inputs.sha256)
  sudo -v
  python3 -B -u "$d/gbs-board-bench.py.txt" "$d" "${OFFICIAL_CAPTURE:?}" "$d/mlgo-tv-microbench.c.txt" \
    "$d/olevel.py.txt" "$d/gbs-mlgo-t7.py.txt" "$d/thumb-qb-sample.py.txt" "$d/gbs-thumb.py.txt" \
    "$d/image_mode_scan.py.txt" "$d/perf-bundle.py.txt"
  printf 'BOARD_TOOLS %s\n' "$d"
)
```

After setting `BOARD_TOOLS` and `TV_SERIAL`, stage and confirm identity. Use the commented commands one action at a time. Set `LANE` to `official` or `custom`, `N` to the trial number, `MEDIA_PIDS` to a Bash array containing validated numeric PIDs, and the three counters to verified scalar paths or `NA`. Mark manually observed stalls in the session log if no verified counter exists. The native runner retains raw logs. The per-trial memory export stays within 240 output lines. Export each lane before flashing.

```bash
sdb devices | head -30
board() {
  bash "${BOARD_TOOLS:?set the printed tools directory}/mlgo-tv-run.sh.txt" \
    "$BOARD_TOOLS" "${TV_SERIAL:?set the confirmed KantSU2E serial}" "$@"
}
board stage
board identity
# For one attended trial at a time, after gating identity and setting the variables:
# board processes
# board boot "$LANE" "$N" "$HOME_PID"
# board micro "$LANE" "$CPU"
# board playback "$LANE" "$N" 60 "${DROP_COUNTER:-NA}" "${LATE_COUNTER:-NA}" "${STALL_COUNTER:-NA}" "${MEDIA_PIDS[@]}"
# board memory "$LANE" "$N"
# board top-mappings "$LANE" "${MEDIA_PIDS[@]}"
# board summary "$LANE"
```

### 6. Read the retained PERF kernel ISA

Lightweight and read-only on the kernel build trees. Use the output proof path as `KERNEL_PROOF` for the Thumb pilot. Missing configs remain open even with usable mapping-symbol coverage.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/kernel-perf-isa.py.txt' '755fcb77482b88cea0ba19c2ae911a16221fc2b90ee740de77243242e45d5b85'
  get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75'
  python3 -B -u "$d/kernel-perf-isa.py.txt" "$d/image_mode_scan.py.txt"
)
```

### 7. Recover historical hook provenance

Set `HISTORICAL_OPTIONS_FILE` to the retained 11 November GBS log or build.conf. Repeat for the macro definition if stored separately. The signed-off historical expanded value can be kept as one line in a workspace file with its SHA in `HOOK_FILE` and `HOOK_SHA256`. A macro reference alone does not establish the expanded value. Output is capped and read-only.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/scripts/r0010/option-hook-readback.py.txt' '39754354132049bb8dda82526e2115d7e3c7d3ef9c02445b0ca12d1143b36266'
  python3 -B -u "$d/option-hook-readback.py.txt" "${HISTORICAL_OPTIONS_FILE:?set the retained November 11 input}"
)
```

### 8. Start or read the optimization replay

Use the [updated step 8 launcher](0010b_reply.md#step-8--optimization-replay). It checks the tvs-core alias and selects the recovered historical hook. The remaining steps keep their reviewed order.

### 9. Run the separate Thumb-default pilot after its gate

Later Tuesday or Wednesday. The retained launcher uses the reviewed Official Product URL and completed PERF kernel proof. Run one package at a time when comparing with the optimization queue. It does not change the scheduled QB or published artifacts.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get 'b4e88f29f06ca8aeea921ee6205834022038fc42' 'artifacts/scripts/r0009/thumb-force-pilot.py.txt' 'f03c13e908726adc50415b6721ac75abee7164d355b30fbdac7db7593d3fd7a9'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  get 'd3cea65aac76d438b82b55a2857a5ee18546edad' 'artifacts/scripts/r0005/image-repo-lib.py.txt' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-mlgo-t7.py.txt' '1089c21b3b4bf4205bd13ba64cace371c57a7d4ec86376877f3b2d069f551a9c'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/thumb-qb-sample.py.txt' 'b7a725e9c5e68072b9f5388a35df91494874f13f67a00fb7426a3067e04a3579'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-thumb.py.txt' '928cff87ac0cb501a6d0575da5f1d80157bd02918d2378a5e061c2262cf11a92'
  get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75'
  get 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' 'artifacts/ledger/qb37627297-source-pins-20261120.tsv' 'e7877e499ca148ba17095c72e2ef13c20cfbae17404182294c84d8781d77baaf'
  args=()
  if [[ -n "${PILOT_PACKAGE:-}" ]]; then args+=(--package "$PILOT_PACKAGE"); fi
  sudo -v
  python3 -B -u "$d/thumb-force-pilot.py.txt" "$d/image-repo-lib.py.txt" "$d/gbs-mlgo-t7.py.txt" \
    "$d/gbs-thumb.py.txt" "$d/thumb-qb-sample.py.txt" "$d/image_mode_scan.py.txt" "$d/perf-bundle.py.txt" \
    "$d/qb37627297-source-pins-20261120.tsv" --dependency-product-url "${OFFICIAL_PRODUCT_URL:?}" \
    --kernel-proof "${KERNEL_PROOF:?}" "${args[@]}"
)
```


### 10. Compare ABI for the first four LTO packages

Use this after staging exact GCC and matched LLVM ELF pairs. Set `ABI_PAIRS` to a workspace TSV with `package path gcc gcc_sha256 llvm llvm_sha256` columns. Optional `gcc_debug gcc_debug_sha256 llvm_debug llvm_debug_sha256` columns name detached Build-ID debuginfo. Set `ABI_GBS_ROOT` to the actual retained GBS chroot directory containing `usr/bin` to enable `abidiff`. The launcher checks tool presence and matching Build IDs first. Expect <190 lines with a result SHA-256. This is a static check using local files and one optional two-thread `abidiff` process at a time. The native run should take minutes on small pairs and longer on the largest debug inputs. Loader/consumer and 24-hour stability checks remain board measurements. [Libabigail options](https://sourceware.org/libabigail/manual/abidiff.html)

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010-tools.XXXXXX")
  f="$d/lto-abi.py.txt"
  export TMPDIR="$d"
  curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/1bcea33e793a3c6538d9a3b631b50948d00f70aa/artifacts/scripts/r0010/lto-abi.py.txt' -o "$f"
  printf '%s  %s\n' '28c32eac9f378063dc7963f614d6745ba5d94a2c91d0045b220a9909167f107b' "$f" | sha256sum -c -
  args=()
  if [[ -n "${ABI_GBS_ROOT:-}" ]]; then sudo -v; args+=(--gbs-root "$ABI_GBS_ROOT"); fi
  python3 -B -u "$f" "${ABI_PAIRS:?set the paired TSV}" "${args[@]}"
)
```

### Research and strict-link recipe mode

Use launcher 8 with one reviewed recipe per invocation. Set `O_RESEARCH_ROSTER` and `O_RESEARCH_ROSTER_SHA256` for a TSV with the same columns as the optimization roster. Set `O_RESEARCH_RECIPE` and `O_RESEARCH_RECIPE_SHA256` for a workspace JSON file with `id`, `baseline` and `treatment`. The two option fields carry expanded `CCC_OVERRIDE_OPTIONS` edits. For example, R3 has empty baseline and treatment `+-flto=thin` when the chosen packages' compile and final link route have been verified. R2, R6, R7 and EXP-Z1 also need a verified `gate_receipt` and `gate_sha256` in the recipe. The receipt records the exact `experiment` and `status: REVIEWED_PASS`, with the reviewed evidence. Use `R4-50`, `R4-25`, `R6-lld` and `R6-icf` as separate IDs. The driver-based recipe does not reach packages that call ld directly. Verify those final commands and consumer maps with the existing GBS link tooling. The launcher waits for the exact historical 22-source roster for R1–R7. For EXP-Z1 use the affected package source roster and retain the archived `tztv` and static-input boundaries.

### Monday–Friday follow-through

| When | Work | Evidence and gate |
|---|---|---|
| Mon–Tue | KantSU2E whole-image Official/Customized A/B | Use the reviewed board checklist and the r0010 runner. Keep a verified Official rollback. Alternate attended measurement blocks on one TV, balance their order where practical, and record firmware, temperatures and image fingerprints. Five unique cold boots per lane use the same Home-ready marker. Five microbench runs in each lane cover syscall, pipe roundtrip, page faults and memory copy bandwidth. Three playback runs use the same hashed 4K clip and count CPU and qualified drops, late frames and stalls. PSS/private dirty and kernel memory snapshots share each playback window. |
| Tue | PERF kernel and EXP-T1 | Run the kernel ISA check first. Use its proof and the new live Official Product in the three-package GBS pilot. Require unchanged explicit `-marm`, a measured default-Thumb change, and full kernel/module source exclusions before a wider QB. |
| Tue–Wed | Optimization level | Start A/B with the first eight packages, then the rest. Enable C using the verified historical option value. Use one serial build and review measured cohort, producer flags and image pairing. |
| Tue–Wed | R1–R7 | Reuse the frozen-source A/control workflow and make a separate option-specific treatment. R1 uses the exact recovered historical hook. R2 requires the export/consumer audit. R3 requires proof that full LTO was replaced by ThinLTO. For R4 use separate 50 and 25 thresholds and confirm their compile/link backend route. R5 checks unwind growth and hot-path performance. R6 requires accelerated lld, loader acceptance and the dali2 link fix, with lld-only and safe ICF as separate comparisons. R7 uses the validated lld baseline and requires loader support before measuring RELR. The supplied report gives examples and 151 build outcomes, and the exact 22-source manifest and experimental settings still need recovery before preparing the complete re-run. |
| Wed–Thu | Strict link and actual consumers | Use the existing T7 GBS archive runner for CAPI and the four local-exec TLS cases, with `GBS_MODE=pic` and `PRODUCT_URL` from the new control. Use launcher 8 in EXP-Z1 recipe mode for source-buildable samples after the baseline gate. Use the Official image audit to prioritize the eight RPM inventory entries and gst-ffmpeg. Qualify actual used inputs through link maps, final `-z text` argv and board loader tests. The full eight-package trial is a later gated step. |
| Wed–Fri | LTO API/ABI and stability | For liballshare-core, nagsam-mw, org.tizen.tv.swu and ug-hbbtv-efl pair exact GCC and matched LLVM RPMs and Build-ID debuginfo first. Record dynsym exports, SONAME, NEEDED and symbol versions. Check `abidiff` inside GBS before running it, and report missing results as missing. Resolve real consumers from link/loader logs and run the same smoke and 24-hour soak on both lanes. Launcher 10 performs the static checks once exact GCC payloads are retained. The actual consumer list and runtime actions remain prerequisites. |
| Thu–Fri | Broader Thumb QB and 1 GiB playback | Submit only after pilot and full kernel/module exclusion review. At the verified physical memory limit, reuse the playback collector and take one top-mapping read during each comparable run. Compare PSS, private dirty and kernel slab with normal-memory controls. |
| Fri | Weekly publication | Archive the original report files and checksum manifest under `reports/weekly/2026-11-27/`. Update Docs 04, 05 and 07 with measured rows and unresolved coverage. |

[Board prerequisites and rollback](../../reports/KantSU2E_MLGO_Board_Day_0005.md) · [Existing T7 GBS run](0008_reply.md#round-0008a-native-results) · [Scope of 11 November option measurements](../../artifacts/historical-reports/optimization-analysis-part-02.md#68-local-rebuild-measurements-thinlto-machineoutliner-lld-icf--fstack-protector-strong) · [LTO acceptance table](../../reports/weekly/2026-11-20/05_HQ_Table_LTO_Enablement.md)

### Evidence and review

Round 0009 is accepted in the received PM handoff. Round 0010 review is pending. Local checks used Python 3.10.12 and shell syntax validation, exact source joins, ELF/CU and progress fixtures. GBS and board execution require the real intranet inputs. Weekly documents remain archived verbatim. The working conclusions about MLGO stay scoped to the Base swap, since the compiler and accelerator packages also changed. The archived Doc 02 goes beyond that evidence when it attributes the result solely to the models. [Working MLGO attribution](../../reports/MLGO_Official_vs_Custom_20261120.md)
