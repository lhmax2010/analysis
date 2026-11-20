# Round 0010b reply — Base attribution, A32 evidence and Monday step 8

Round 0010 at `18e939a0e8d52935e3fb8fcae868a6598e3ab816` is accepted. Monday steps 1–10 stay in their reviewed order. The launchers below use the new script commit `cfde38f9e4c6041069d28adc8b9da35894df0de9`, pending Claude review before native execution. [Review received](../claude_to_codex/0010b_addendum.md) [Monday order](0010_reply.md#d-monday-run-order-and-next-week-gates)

## 20 November archive and Monday refresh

Doc 02 rev2 is archived at `97cac6a29806b54d11121334bb7c87766c5bafb8`, SHA-256 `082557b8b6bf6038570068ab7b2d294a1eae6844e3abcb68cf39cf8d3418bb41`. The revision note is in the parent reports README because the weekly README is covered by the original manifest. All eight original checks and the separate rev2 check passed. [Reports index](../../reports/README.md) [Rev2 manifest](../../reports/weekly/2026-11-20/SHA256SUMS.rev2)

| Doc | Evidence now | Monday update |
|---|---|---|
| 02 | Rev2 attributes the kernel comparison to the LLVM Base swap. | Add matched board data from step 5 and qualify attribution with the Base package proof below. |
| 04 | 24 exact installed source names, nine without a matching installed RPM, and one alias awaiting the P4 spec. | Mark the nine rows “Not shipped in this product (no installed RPM)”. Apply the alias on `ALIAS_VERIFIED` and add step 8 measurements. |
| 05 | The 2,342-RPM PERF inventory includes `sys-tools-0-0.armv7l` and `*-perf` / `*-test` entries. No retail roster has been returned. | Rows 17–18 should say “Installed in the PERF image (debug tooling). Retail inclusion is unverified.” Scope this count to PERF. Add §3 rows 1–4 from step 10. |
| 07 | Seven files have path-and-owner DWARF evidence for `-marm`. Six are in the top 211 (13, 14, 36, 38, 58, 59) and one in the tail (361). Five Bluetooth rows (5, 20, 50, 160, 195) lack a qualifying `-marm` producer record in the retained table. | Step 4 supplies the exact basis and values for ranks 1–211 and the installed-evidence column. Preserve the 14 rounding differences as an audit trail. |

[Installed RPM inventory](../../artifacts/ledger/README.md) [A32 reconciliation](../../artifacts/thumb-repro/a32-full-609-summary.md) [DWARF evidence](../../artifacts/thumb-repro/retained-board-arm-baseline.csv)

Use `reports/weekly/2026-11-27/` for the next weekly archive.

## Matched-QB MLGO Base package proof

Attribute matched board measurements to the **Base swap** until the proof returns. The lanes change LLVM `22.1.8-9.1` to `22.1.8-11.1` and the accelerator RPM `0.4-2.4` to `0.4-2.5`. The accelerator is an `armv7l` RPM with an x86_64-host executable. An empty installed NEVRA diff still leaves same-NEVRA rebuilds possible. Review non-model source changes, effective spec changes, the accelerator difference and user-space ELF results before narrowing attribution.

**Native server.** Set `OFFICIAL_CAPTURE` and `CUSTOMIZED_CAPTURE` to the new matched step 1 captures. The proof verifies both published `@14452507` configs and the repository and PERF ledgers. It compares the exact LLVM SRPM members and SHA-256 digests, spec declarations and changelog, and the two pinned accelerator RPM changelogs. It prints all installed NEVRA differences across pages and flags differences in candidate publication digests for identical NEVRAs. Publication metadata cannot prove which of several published RPMs provided an installed payload.

Budget 10–35 minutes, one archive reader under the existing heavy lock, two extracted platform images plus sparse conversion if needed, RPM downloads and the 50 GiB reserve. Network reads are the pinned GitHub helper and VD metadata/RPMs. `REVIEW_STATUS INCOMPLETE` identifies missing inputs. For unavailable SRPM metadata use `MLGO_PROOF_RPMS`, a workspace TSV with columns `lane`, `kind`, `path`, `sha256` for `official`/`custom` and `llvm`/`accel`. Use retained published inputs. A digest with no publication metadata is tagged operator-retained. If the platform RPM DB cannot be queried, supply `MLGO_OFFICIAL_ROSTER` and/or `MLGO_CUSTOM_ROSTER` from the corresponding same-image `rpm -qa` export. Use tab-separated `NAME EPOCHNUM VERSION RELEASE ARCH SOURCERPM` with no header and record the exact image identity. Set `MLGO_PROOF_REPORT` to the returned report and increment `MLGO_PROOF_PAGE` through `LAST_PAGE`. Readback returns up to 108 data lines per page and skips extraction. The default installed scope is the RPM DB in the captured platform partition. If the target uses an additional DB or an overlay, use the same-QB board export after the identity gate. Run this fallback on the native host connected to the confirmed image. Keep each printed path for the corresponding lane.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010b-board-roster.XXXXXX")
  sdb -s "${TV_SERIAL:?}" shell "rpm -qa --qf '%{NAME}\t%{EPOCHNUM}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{SOURCERPM}\n'" >"$d/installed.tsv"
  wc -l "$d/installed.tsv"
  sha256sum "$d/installed.tsv"
)
```

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010b-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
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
      --repo "$d/image-repo-lib.py.txt" --official "${OFFICIAL_CAPTURE:?}" --custom "${CUSTOMIZED_CAPTURE:?}" \
      "${args[@]}"
  fi
)
```

## November 11 hook and 22-source roster

The most frequent expanded value appeared nine times quoted and nine times unquoted. Both renderings yield the same bytes. These are occurrences across logs that include duplicate copies. The recovered `HOOK_FILE` has one trailing LF and SHA-256 `bdf0fecb69664a13a11ac42c4ea56337f509c87189459328b007b8a290db2e7e`. It contains `+-mthumb`, and `+-Os` follows `+-O2`. Lane C has a historical input. It combines the ISA change, optimization level, hardening, signed-char and target flags. EXP-T1 remains the independent ISA comparison. [Expanded hook](../../artifacts/ledger/nov11-clang-hook-expanded.txt) [Original locator](../../artifacts/evidence/native-cmd-r0010b-nov11-hook-roster.sh) [Byte-identical terminal return](../../artifacts/evidence/native-run-r0010b-hook-roster-20261120.txt)

```text
# +-O2 +-g2 +-pipe +-Wp,-D_FORTIFY_SOURCE=2 +-fexceptions +-fstack-protector-strong +-fmessage-length=0 +-Wl,-z,relro,--as-needed +--param=ssp-buffer-size=4 +-mcpu=cortex-a53 +-mtune=cortex-a53 +-march=armv8-a+crc +-mlittle-endian +-mfpu=neon-vfpv4 +-mfloat-abi=softfp +-mthumb +-Wp,-D__SOFTFP__ +-Wl,-O1 +-Wl,--hash-style=gnu +-Wa,-mimplicit-it=thumb +-fno-common +-fsigned-char +-Os +-Wno-unknown-warning-option +-Wno-cast-function-type-strict +-Wno-unused-command-line-argument
```

The first locator missed the lowercase `gbs-root-*` names. Its R8 paths show AVControl, libpisa-ipc and tvs-si. Those R8 logs do not establish the R1–R7 roster. The historical report names outcomes for packages including openusd, avoc-daemon, dali2-adaptor, libfreetype, libgrpc, boost, abseil-cpp, icu, aurum, org.tizen.mbr-daemon and native-home. It does not identify all 22 pinned source inputs. Keep `r1-r7-roster-20261111.tsv` pending the full return. Preserve `workspace/temp/z901/exp*/` and `gbs-root*/local/repos/*/armv7l/logs/` when cleaning caches. [Historical results and failures](../../artifacts/historical-reports/optimization-analysis-part-01.md#exempt-packages-inlining-policy)

**Native server, before step 8.** The locator reads the z901 experiment directories and case-insensitive GBS root prefixes. It reports sources inferred from the directory and log keys plus individual log hashes for reconciliation. Allow 1–5 minutes, one reader, kilobytes to low MiB for the report, and GitHub download only. Return page 0 and the R1–R7 pages using `NOV11_ROSTER_REPORT` and `NOV11_ROSTER_PAGE`.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010b-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get 'cfde38f9e4c6041069d28adc8b9da35894df0de9' 'artifacts/scripts/r0010b/nov11-roster.py.txt' 'acfce14ad6e18b0c85198662d13f1dae41ece9094d53b03187236c0c20edda29'
  if [[ -n "${NOV11_ROSTER_REPORT:-}" ]]; then
    python3 -B "$d/nov11-roster.py.txt" --page "$NOV11_ROSTER_REPORT" "${NOV11_ROSTER_PAGE:-0}"
  else
    python3 -B -u "$d/nov11-roster.py.txt"
  fi
)
```

## Step 8 — Optimization replay

Use the [updated Step 8 launcher](0010c_reply.md) with the four-lane measurement and verified native hook.

## Crosswalk representatives for the sampling gate

| Product RPM | ELF | Rank | Estimated A32 |
|---|---|---:|---:|
| `webapi-plugins` | `/usr/lib/tizen-extensions-crosswalk/libtizen_mediacontroller.so` | 67 | 792 KiB |
| `webapi-network-pepper-plugin` | `/usr/lib/tizen-extensions-crosswalk/libwebapis_network.so` | 137 | 297 KiB |

Sample these two first. The source reader records file:line build references from the matched Official source. The optional GBS build records actual compiler argv. Trace the recorded source and object through the generated build graph to the named ELF before citing a compile line. Dynamic includes and wrapper-bypassing compile commands may need the full retained log and generated graph. A common rule remains unproven. [A32 ledger](../../artifacts/thumb-repro/a32-full-609.csv)

**Native server.** Set `CROSSWALK_PACKAGE` to one of the two source names at a time. The default stages source and prints static references. Allow 2–15 minutes, one P4 reader, source-sized disk use and P4/GitHub traffic. After the sampling gate and with a live matched dependency repo, `CROSSWALK_BUILD=1` runs one unchanged-options GBS build with tracing. Budget 20–120 minutes, up to six pinned cores and 24 GiB plus reserve and normal VD dependency traffic. Both paths use the heavy lock. To return the retained rule or argv file, set CROSSWALK_WORKDIR to the printed workdir and CROSSWALK_EVIDENCE to include-evidence.txt, compiler-invocations.txt or gbs.log. Use CROSSWALK_LINE for the first line of each 90-line page.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010b-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get '97a50bcacc7402d8297b25a47b1f2117b40c6d72' 'artifacts/scripts/r0010/olevel.py.txt' '7ea4a4c99204ae9a280e83d46a1e3de2b7ff721ce7a8079294e36393401259bf'
  get 'd3cea65aac76d438b82b55a2857a5ee18546edad' 'artifacts/scripts/r0005/image-repo-lib.py.txt' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-mlgo-t7.py.txt' '1089c21b3b4bf4205bd13ba64cace371c57a7d4ec86376877f3b2d069f551a9c'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/thumb-qb-sample.py.txt' 'b7a725e9c5e68072b9f5388a35df91494874f13f67a00fb7426a3067e04a3579'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-thumb.py.txt' '928cff87ac0cb501a6d0575da5f1d80157bd02918d2378a5e061c2262cf11a92'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  get 'cfde38f9e4c6041069d28adc8b9da35894df0de9' 'artifacts/scripts/r0010b/option-source-readback.py.txt' 'fa0369c1e891ff37e290511843a4ffc8f9723536bb5c4c26ccc361b373411f6d'
  if [[ -n "${CROSSWALK_WORKDIR:-}" ]]; then
    root=$(realpath -e "$CROSSWALK_WORKDIR")
    [[ "$root" == "$PWD/workspace/temp/pm0010b-option-source."* ]]
    name=${CROSSWALK_EVIDENCE:-include-evidence.txt}
    case "$name" in include-evidence.txt|compiler-invocations.txt|gbs.log) ;; *) exit 2 ;; esac
    start=${CROSSWALK_LINE:-1}
    [[ "$start" =~ ^[1-9][0-9]{0,6}$ ]]
    [[ -f "$root/$name" && ! -L "$root/$name" ]]
    sha256sum "$root/$name"
    wc -l "$root/$name"
    sed -n "$start,$((start+89))p;$((start+90))q" "$root/$name"
    exit 0
  fi
  args=()
  if [[ "${CROSSWALK_BUILD:-0}" == 1 ]]; then sudo -v; args+=(--build); fi
  python3 -B -u "$d/option-source-readback.py.txt" --capture "${OFFICIAL_CAPTURE:?}" \
    --olevel "$d/olevel.py.txt" --repo "$d/image-repo-lib.py.txt" --gbs "$d/gbs-mlgo-t7.py.txt" \
    --stager "$d/thumb-qb-sample.py.txt" --sample "${CROSSWALK_PACKAGE:?}" \
    --thumb "$d/gbs-thumb.py.txt" --perf "$d/perf-bundle.py.txt" "${args[@]}"
)
```

## Validation and remaining evidence

Python 3.10.12 passed syntax and focused checks using a real synthetic SRPM, ext4 RPM database extraction and empty-DB handling, NEVRA/publication comparison, lowercase roster collection, P4 shelf overlays and the existing hook parser. Actual P4, Base SRPM availability, captured RPM DBs and GBS traces require native execution. The exact historical roster, measured option results and board data remain pending. All HQ material remains internal for review.
