# Round 0011 reply — Matched MLGO QBs and GCC no-prelink reference

The supplied Step 1 launcher matches its SHA-256 and is archived as received. Its native capture results and the 0010w combined output have yet to return. Claude accepted the original helpers in 0011a. Use the [approved run order and new HQ tooling](0011a_reply.md). Monday remains Step 1 → Step 2 → Step 3 → Step 5 → Step 8. Run the MLGO Base proof after both captures. [PM handoff](../claude_to_codex/0011_pm_review.md) [Step 1 launcher](../../artifacts/evidence/native-cmd-r0011-capture-mlgo-qbs.sh)

| Lane | QB | Product | Base |
|---|---:|---|---|
| Official LLVM | 37736448 | 20261123.2 | LLVM 10.0 20261113.1 |
| Customized LLVM | 37736427 | 20261123.1 | LLVM 10.0 20261118.1 |
| GCC-REF-NOPRELINK | 37564293 | 20261113.1 | GCC 10.1 20260919.1 |

## Step 2 — Verify the new pair and its submitted lists

After the Step 1 background launcher finishes, set `CAPTURE_RUN_DIR` to its printed absolute working directory. Run this in the current native shell to retain both paths for the later commands. Each lane must finish successfully.

```bash
if grep -q '^CAP 1-official-qb37736448 END rc=0 ' "$CAPTURE_RUN_DIR/status.txt" &&
   grep -q '^CAP 2-custom-qb37736427 END rc=0 ' "$CAPTURE_RUN_DIR/status.txt"; then
  export OFFICIAL_CAPTURE="$(sed -n 's/^CAPTURE_DIR //p' "$CAPTURE_RUN_DIR/1-official-qb37736448.txt")"
  export CUSTOM_CAPTURE="$(sed -n 's/^CAPTURE_DIR //p' "$CAPTURE_RUN_DIR/2-custom-qb37736427.txt")"
  printf '%s\n' "$OFFICIAL_CAPTURE" "$CUSTOM_CAPTURE"
else
  awk 'NR<=30' "$CAPTURE_RUN_DIR/status.txt"
fi
```

The expected local source files are under `/home1/chengkai/vd-tree/manifest/`. Use this one read-only locator for the exact names and likely successors. It prints up to 100 path and SHA-256 matches. The operator's submission records must establish which copies each QB used.

```bash
find /home1/chengkai/vd-tree -xdev \
  \( -type d \( -name .git -o -name BUILD-ROOTS -o -name cache -o -name RPMS \) -prune \) -o \
  \( -type f \( -name 'tizen10.0_shelves_*ltoexp*.txt' -o -name 'tizen10.0_base_urls_*noprelink*.txt' \) \
     -exec sha256sum -- {} + \) | awk 'NR<=100 {print} END {if (NR>100) print "TOTAL_MATCHES", NR}'
```

The review pins check the `tizen10.0_shelves_1116_ffmpeg_seek_ltoexp2.txt` hash (`c89e2317…`), `tizen10.0_base_urls_1114_noprelink.txt` (`bd5e8117…`), and published `build.conf@14452507` (`98690f23…`). Set `OFFICIAL_SHELVES`, `CUSTOM_SHELVES`, `OFFICIAL_BASE_LIST` and `CUSTOM_BASE_LIST` to the actual submitted copies. A successor with different bytes needs a reviewed comparison and revised pins.

The gate verifies each published ID, Base URL and build.conf, then compares source-related `build.xml` fields and the Product publication's immutable VCS and source-version rows. Product snapshot labels and RPM releases can differ between builds. `QB_PAIR_CONFIG_GATE_PASS` verifies the artifact and supplied list pins. `QB_PAIR_PRODUCT_VCS_MATCH` means all published Product rows also have matching source identities. `QB_PAIR_PRODUCT_SOURCE_REVIEW_REQUIRED` exits 2 and identifies evidence to return before calling the pair source-matched. For rows without published P4 values, matching SRPM names alone leave source identity unproved. The full checked `build.xml` fields and per-package results stay under `pm0011-pair.*`. Use the bounded HQ page mode below to return the difference rows. Both checks remain pending native input. Runtime seconds, hashing only and small ledger writes, with the pinned GitHub download.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0011-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}" attempt
    for attempt in 1 2 3 4 5; do
      if curl -fsS --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file" &&
         printf '%s  %s\n' "$sum" "$file" | sha256sum -c -; then
        return 0
      fi
      printf 'DOWNLOAD_FAILED attempt=%s/5 %s\n' "$attempt" "${path##*/}" >&2
      if (( attempt < 5 )); then sleep 10; fi
    done
    return 1
  }
  get 'aaa44c847bfc6b5313de6fd579be853d01d6f684' 'artifacts/scripts/r0011/qb-pair-gate.py.txt' 'e7813282ec962391d5cb36b4a42251753b154dbaeee7ff062625f974c85335c0'
  python3 -B -u "$d/qb-pair-gate.py.txt" "${OFFICIAL_CAPTURE:?}" "${CUSTOM_CAPTURE:?}" \
    "${OFFICIAL_SHELVES:?}" "${CUSTOM_SHELVES:?}" "${OFFICIAL_BASE_LIST:?}" "${CUSTOM_BASE_LIST:?}"
)
```

## Step 3 and the MLGO Base proof

The Step 3 command defaults to the existing Official PERF audit. Set `PERF_ACTION=usb-both` for serial staging of Official and then Customized, or set `PERF_ACTION=usb` and `CAPTURE` to retry one lane. Audit takes roughly 20–90 minutes. USB staging takes roughly 5–30 minutes per lane. Use the existing capacity reserve and board validation before copying to the real USB. Step 5 and the four-lane Step 8 use the new `OFFICIAL_CAPTURE`. Revalidate the installed replay roster against the new capture before quoting package-level results. [Board and benchmark runbook](0010_reply.md#d-monday-run-order-and-next-week-gates) [Step 8](0010c_reply.md)

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0011-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}" attempt
    for attempt in 1 2 3 4 5; do
      if curl -fsS --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file" &&
         printf '%s  %s\n' "$sum" "$file" | sha256sum -c -; then
        return 0
      fi
      printf 'DOWNLOAD_FAILED attempt=%s/5 %s\n' "$attempt" "${path##*/}" >&2
      if (( attempt < 5 )); then sleep 10; fi
    done
    return 1
  }
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-relocations.py.txt' 'f678d0f9c479d6a183c3f83d7a14917ea46c15533f41d97a3baeb732b6905cf7'
  case "${PERF_ACTION:-audit}" in
    audit)
      python3 -B -u "$d/perf-relocations.py.txt" --capture "${OFFICIAL_CAPTURE:?}" \
        --bundle-library "$d/perf-bundle.py.txt" --sample-asan
      ;;
    usb-both)
      python3 -B -u "$d/perf-bundle.py.txt" "${OFFICIAL_CAPTURE:?}"
      python3 -B -u "$d/perf-bundle.py.txt" "${CUSTOM_CAPTURE:?}"
      ;;
    usb) python3 -B -u "$d/perf-bundle.py.txt" "${CAPTURE:?set the lane capture}" ;;
    *) exit 2 ;;
  esac
)
```

Run the approved Base proof with the capture variables above. It precedes the Doc 02 board table. Until it establishes a narrower explanation, the attribution is **Base swap**. Keep native source RPM and installed-RPM fallbacks from the previous runbook. Budget 10–35 minutes, one local decompression reader, the extracted images and 50 GiB reserve, plus downloads of pinned RPMs when needed. [Base proof fallbacks and paging](0010b_reply.md#matched-qb-mlgo-base-package-proof)

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0011-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}" attempt
    for attempt in 1 2 3 4 5; do
      if curl -fsS --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file" &&
         printf '%s  %s\n' "$sum" "$file" | sha256sum -c -; then
        return 0
      fi
      printf 'DOWNLOAD_FAILED attempt=%s/5 %s\n' "$attempt" "${path##*/}" >&2
      if (( attempt < 5 )); then sleep 10; fi
    done
    return 1
  }
  get 'd3cea65aac76d438b82b55a2857a5ee18546edad' 'artifacts/scripts/r0005/image-repo-lib.py.txt' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  get 'cfde38f9e4c6041069d28adc8b9da35894df0de9' 'artifacts/scripts/r0010b/mlgo-base-proof.py.txt' '7254ef3de2d606826718338eb69e30253f34f36fef5dd8fb683897044fe6b9f1'
  if [[ -n "${MLGO_PROOF_REPORT:-}" ]]; then
    python3 -B "$d/mlgo-base-proof.py.txt" --page "$MLGO_PROOF_REPORT" "${MLGO_PROOF_PAGE:-0}"
  else
    args=()
    if [[ -n "${MLGO_PROOF_RPMS:-}" ]]; then args+=(--rpms "$MLGO_PROOF_RPMS"); fi
    if [[ -n "${MLGO_OFFICIAL_ROSTER:-}" ]]; then args+=(--official-roster "$MLGO_OFFICIAL_ROSTER"); fi
    if [[ -n "${MLGO_CUSTOM_ROSTER:-}" ]]; then args+=(--custom-roster "$MLGO_CUSTOM_ROSTER"); fi
    python3 -B -u "$d/mlgo-base-proof.py.txt" --perf "$d/perf-bundle.py.txt" \
      --repo "$d/image-repo-lib.py.txt" --official "${OFFICIAL_CAPTURE:?}" --custom "${CUSTOM_CAPTURE:?}" \
      "${args[@]}"
  fi
)
```

## GCC reference capture

The fixed `DO_NOT_DELETE` URL is accepted only in the new `reference` mode for QB 37564293. Expected completion includes `CAPTURE_LANE GCC-REF-NOPRELINK` and `CAPTURE_COMPLETE`. The script retains the PERF archive, publication identity, primary metadata and RPM ledger, kernel RPMs, and published build.conf. It checks the 10.1 Base URL and the existing `TIZEN_KantSU2e_build.conf@14452502` evidence. Use the printed `CAPTURE_DIR` as `GCC_CAPTURE`. Native use is one stream, typically 5–60 minutes, with PERF size plus the kernel RPMs and reserve. Run after the new LLVM captures release the shared locks. [Retained GCC build identity](../../artifacts/evidence/native-cmd-r0011-capture-mlgo-qbs.sh)

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0011-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}" attempt
    for attempt in 1 2 3 4 5; do
      if curl -fsS --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file" &&
         printf '%s  %s\n' "$sum" "$file" | sha256sum -c -; then
        return 0
      fi
      printf 'DOWNLOAD_FAILED attempt=%s/5 %s\n' "$attempt" "${path##*/}" >&2
      if (( attempt < 5 )); then sleep 10; fi
    done
    return 1
  }
  get 'aaa44c847bfc6b5313de6fd579be853d01d6f684' 'artifacts/scripts/r0011/qb-retain.py.txt' '437135b56bc69c64571c906fe704a74c761f5d3414f5010122ed79cd31b5dc91'
  get 'd3cea65aac76d438b82b55a2857a5ee18546edad' 'artifacts/scripts/r0005/image-repo-lib.py.txt' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
  url='http://repos.vd.sec.samsung.net/products/tv/development/DO_NOT_DELETE/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261113.1/'
  args=()
  if [[ -n "${GCC_PERF_SHA256:-}" ]]; then args+=(--image-sha256 "$GCC_PERF_SHA256"); fi
  python3 -B -u "$d/qb-retain.py.txt" "$d/image-repo-lib.py.txt" reference 37564293 "$url" "${args[@]}"
)
```

## Re-baseline Docs 04–07

The [0011a overnight launcher](0011a_reply.md#overnight-hq-comparison) supersedes the comparison command below for new HQ tables. It applies the revised source and stripped-ELF gates.

Run the same ELF scan once with `HQ_MODE=gcc` and once with `HQ_MODE=llvm`, serially. The scan reads actual retained PERF filesystem images through the existing ext4 traversal. It uses the captured platform RPM DB to associate each image path with its owner and fills missing VCS from the exact Product RPM ledger where available. It records ELF section sizes, file sizes, FILE-symbol evidence, ARM/Thumb estimates and prelink markers. Unmapped partitions or ownership gaps are reported. If a capture uses an unsupported layout or its RPM DB is unreadable, return that evidence before treating the inventory as complete. Native scan budget 20–90 minutes per image and expanded partition space plus reserve, using one reader and no network after script download. The join and paging take seconds.

Save the two reported `HQ_ELF_WORKDIR` paths as `GCC_ELF_WORKDIR` and `LLVM_ELF_WORKDIR`. Use `HQ_MODE=compare` to produce the matched package table, the LTO gap candidate list and the coverage summary. `HQ_MODE=page` accepts `HQ_REPORT`, `HQ_PAGE` and optional `HQ_CONTAINS`. Use it for these files and the Step 2 reports, at most 135 data lines per page.

| Doc | Output used |
|---|---|
| 04 | GCC `.text` by owned ELF and package. Map the historical package names to the installed source names before totaling. |
| 05 | GCC LTO/all counts and `.text`, with stripped ELF coverage tracked separately. The same-path GCC-heuristic/LLVM-project-FILE list is a shortlist for build-log and final-link proof. |
| 06 | GCC and LLVM ELF file and `.text` bytes, retaining both sides of source-different rows. |
| 07 | A32 estimates from mapping symbols and the approved fallback, with GCC outliers and unknown modes retained for provenance checks. Prebuilt origin requires package evidence. |

The reference removes the known prelink-policy mismatch. The ELF scan reports sampled image marker counts separately. GCC 10.1 and LLVM 10.0 use different Base series, and the Product snapshots are ten days apart. The join uses pinned VCS plus source version or matching declared SRPM and NEVRA when VCS is absent on both sides. A source difference or unproved identity excludes that package from the matched totals. Those rows retain their raw sizes. Even matched source rows remain comparisons across two Base series. The totals are for comparable RPM-owned paths and require coverage review before any whole-image statement. Chapter 4's FILE-symbol rule is a heuristic because stripping may remove project filenames. [Historical LTO method](../../artifacts/historical-reports/optimization-analysis-part-01.md#4-lto-coverage) [ELF symbol table specification](https://gabi.xinuos.com/elf/05-symtab.html) [RPM query formats](https://rpm.org/docs/latest/man/rpm-queryformat.7)

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0011-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}" attempt
    for attempt in 1 2 3 4 5; do
      if curl -fsS --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file" &&
         printf '%s  %s\n' "$sum" "$file" | sha256sum -c -; then
        return 0
      fi
      printf 'DOWNLOAD_FAILED attempt=%s/5 %s\n' "$attempt" "${path##*/}" >&2
      if (( attempt < 5 )); then sleep 10; fi
    done
    return 1
  }
  get 'aaa44c847bfc6b5313de6fd579be853d01d6f684' 'artifacts/scripts/r0011/hq-elf-rebaseline.py.txt' 'd07075cdeee20e73036a82e6951e7a8779f46d8f69f2bbe6177d5ccc3ea67efb'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-relocations.py.txt' 'f678d0f9c479d6a183c3f83d7a14917ea46c15533f41d97a3baeb732b6905cf7'
  get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75'
  case "${HQ_MODE:?set gcc, llvm, compare or page}" in
    gcc|llvm)
      if [[ "$HQ_MODE" == gcc ]]; then
        capture=${GCC_CAPTURE:?}
      else
        capture=${OFFICIAL_CAPTURE:?}
      fi
      python3 -B -u "$d/hq-elf-rebaseline.py.txt" scan \
        "$d/perf-bundle.py.txt" "$d/perf-relocations.py.txt" "$d/image_mode_scan.py.txt" "$capture"
      ;;
    compare)
      python3 -B -u "$d/hq-elf-rebaseline.py.txt" compare "${GCC_ELF_WORKDIR:?}" "${LLVM_ELF_WORKDIR:?}"
      ;;
    page)
      args=()
      if [[ -n "${HQ_CONTAINS:-}" ]]; then args+=(--contains "$HQ_CONTAINS"); fi
      python3 -B "$d/hq-elf-rebaseline.py.txt" page "${HQ_REPORT:?}" "${HQ_PAGE:-0}" "${args[@]}"
      ;;
    *) exit 2 ;;
  esac
)
```

## GCC GBS local repository hazard

The supplied `repo.local_NikeM` points into an LLVM buildroot. Capturing or scanning a published image uses no GBS configuration. For a future GCC build, generate a run-specific GCC configuration with an isolated buildroot and a new empty local repository. The strict guard below requires all `repo.local_*` paths to resolve to that directory and rejects either a literal or symlinked LLVM path. Run the guard immediately before GBS and only proceed on `GCC_LOCAL_REPO_GUARD_PASS`. Without `GCC_DEDICATED_REPO`, the same helper prints configured paths and historical log references instead. Native runtime seconds to a few minutes, local log reads and a pinned download.

The retained Nov 12 `gccL` and `gbs-root-r8-G1/G2` evidence identifies AVControl and tv-viewer builds. It does not identify the GBS configuration or package dependency URLs used in those runs. The earlier November 14 GCC validation used a generated config from `gbs_llvm_fixes__khag0ff.conf` with an explicit GCC compiler override against LLVM dependencies. That is a separate local build cohort. Retain the historical experiment as unproved for the `37564293` configuration until the command/config logs establish it. [Retained exp8 inventory](../../artifacts/evidence/native-run-r0010d-z901-exp8-inventory-20261120.txt)

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0011-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}" attempt
    for attempt in 1 2 3 4 5; do
      if curl -fsS --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file" &&
         printf '%s  %s\n' "$sum" "$file" | sha256sum -c -; then
        return 0
      fi
      printf 'DOWNLOAD_FAILED attempt=%s/5 %s\n' "$attempt" "${path##*/}" >&2
      if (( attempt < 5 )); then sleep 10; fi
    done
    return 1
  }
  get 'aaa44c847bfc6b5313de6fd579be853d01d6f684' 'artifacts/scripts/r0011/gcc-gbs-config.py.txt' 'ad6961a59ff3399e05c500e69ea4b941ec45f371abb2c3c19256f9df2363528f'
  args=()
  if [[ -n "${GCC_GBS_CONFIG:-}" ]]; then args+=(--config "$GCC_GBS_CONFIG"); fi
  if [[ -n "${GCC_DEDICATED_REPO:-}" ]]; then args+=(--dedicated-empty-repo "$GCC_DEDICATED_REPO"); fi
  python3 -B -u "$d/gcc-gbs-config.py.txt" "${args[@]}"
)
```

## Weekend readback pages

The PM reports six jobs with rc=0. The combined transcript is 517 lines, and the `verbose`, `treatments` and `sizes` outputs are first pages. The board ISA result, A32 packet, WARN/FINAL parity and option-injection interpretation await that transcript. The GitHub-pinned pager below verifies the retained combined digest and prints the `REPORT` and `PAGE` lines when `EXP8_REPORT` is unset. Use it again with the `REPORT` path for each of `verbose`, `treatments` and `sizes`, starting at `EXP8_PAGE=1` and increasing through the mode's `LAST_PAGE`. Each execution prints no more than 142 report lines, runs in seconds and does not rerun a scan. Return combined content in separate numbered excerpts of at most 300 lines if it has yet to be pasted. [Prior result gates](0010f_reply.md#exp8-execution-and-report-links)

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0011-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}" attempt
    for attempt in 1 2 3 4 5; do
      if curl -fsS --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file" &&
         printf '%s  %s\n' "$sum" "$file" | sha256sum -c -; then
        return 0
      fi
      printf 'DOWNLOAD_FAILED attempt=%s/5 %s\n' "$attempt" "${path##*/}" >&2
      if (( attempt < 5 )); then sleep 10; fi
    done
    return 1
  }
  get 'fb98eefaf6d924422466be70f4f95446583adeb1' 'artifacts/scripts/r0010e/exp8-readback.py.txt' 'feeff8d1e1521a70b17a05ce85a1e2fa42cefd31f37777064ac59864cd46f96d'
  report=/home1/chengkai/vd-tree/workspace/temp/pm0010w-weekend.BcoAvm/combined.txt
  if [[ -z "${EXP8_REPORT:-}" ]]; then
    printf '%s  %s\n' ea30ccdbe37e7c10ed4e33e69a6cebed6e2a60d1b273e5734bee87c0fea73b2a "$report" | sha256sum -c -
    awk '/^(REPORT |PAGE |=====)/ { if (++n <= 70) print }' "$report"
  else
    python3 -B "$d/exp8-readback.py.txt" --page "$EXP8_REPORT" "${EXP8_PAGE:-1}"
  fi
)
```

The Python 3.10 checks covered matched-source classification, strict snapshot URL routing, blocking a symlinked LLVM repository, ELF section/FILE behavior on synthetic ARM and a local ELF64 binary, and exclusion of source-different rows from totals. The launch commands passed Bash syntax and their Git blob hashes match. The native publications and captures still need live verification.
