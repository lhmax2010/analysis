# Round 0011b reply — matched captures and weekend results

Both QB captures completed. Each contains 5,880 Product RPM identities, four kernel RPMs and the published build.conf pinned to `@14452507`. The `tztv-kernel-perf` RPM went from 19,345,448 B to 19,160,700 B (−184,748 B, −0.95%). These are compressed RPM sizes. Step 2 verifies the publications' Base selectors and Product source identities. The MLGO Base proof and board measurements are still pending. [Native transcript](../../artifacts/evidence/native-run-r0010w-weekend-and-r0011-capture-20261124.txt)

| Lane | PERF archive bytes | PERF archive SHA-256 | Capture receipt SHA-256 |
|---|---:|---|---|
| Official 37736448 | 1,776,579,896 | `5f2ab79366ee80944aa6dc24d6abcd8c5e2d2139225bfc6860a815dc59883228` | `f164cf5f56ced88fd0618c68df686c79ec36aca85dbeb53972a4b128f135862d` |
| Customized 37736427 | 1,776,558,965 | `b009700330faa61f695ba279a5caf5e543a35ffb4fd347941a924e4fef04ce0b` | `59e000f5b7ec8a508f5251b2e11e36cd3b29036ac91b3cf7034d3aadbb0a3e5b` |

The archived 604-line transcript matches `c0a8eebfa23b7e3638147ab812eb175c9048dd23bb21410e3b6e6a2fb0b34753`. Its raw 517-line weekend and 38-line capture blocks independently match the two native digests in the addendum. [Original addendum](../claude_to_codex/0011b_addendum.md)

## Step 2 — verify the published Base selectors and Product VCS

Preflight stages the local GBS config by changing its Base repository URL and its scratch buildroot. It rewrites the Base version list only where a literal control snapshot URL occurs. The identical hash therefore establishes that the two list files contain the same bytes. The authoritative evidence for the new QB lanes is their captured `build.xml` field `base_repo`, which Step 2 validates against the respective Base URL. The list hash alone cannot establish a published selector or how the operator populated it. The native terminal transcript supplies capture receipt checksums but omits the selector values. [Local GBS staging code](../../artifacts/scripts/r0004/preflight-base-qb.py.txt) [Pair gate](../../artifacts/scripts/r0011/qb-pair-gate.py.txt)

Run on the native server. This takes seconds, uses one process, writes a small result ledger and downloads one pinned script. Return each `QB_PUBLISHED_BASE_SELECTOR`, the config gate and the Product VCS result. If the gate returns source review required, retain its exact `QB_PAIR_SOURCE_ROWS` and `QB_PAIR_XML_FIELDS` paths. The [HQ page command](0011_reply.md#re-baseline-docs-0407) can read the source review TSV with `HQ_MODE=page` and `HQ_CONTAINS=SOURCE_`.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0011-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get 'aaa44c847bfc6b5313de6fd579be853d01d6f684' 'artifacts/scripts/r0011/qb-pair-gate.py.txt' 'e7813282ec962391d5cb36b4a42251753b154dbaeee7ff062625f974c85335c0'
  official="$PWD/workspace/qb-evidence/37736448-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2"
  custom="$PWD/workspace/qb-evidence/37736427-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.1"
  printf '%s  %s/identity.json\n' f164cf5f56ced88fd0618c68df686c79ec36aca85dbeb53972a4b128f135862d "$official" | sha256sum -c -
  printf '%s  %s/identity.json\n' 59e000f5b7ec8a508f5251b2e11e36cd3b29036ac91b3cf7034d3aadbb0a3e5b "$custom" | sha256sum -c -
  python3 -B - "$official" "$custom" <<'PYTHON'
from pathlib import Path
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
for folder in map(Path, sys.argv[1:]):
    identity = json.loads((folder / "identity.json").read_text())
    raw = (folder / "build.xml").read_bytes()
    if hashlib.sha256(raw).hexdigest() != identity["files"]["build.xml"]:
        raise SystemExit(f"build.xml checksum mismatch: {folder}")
    xml = ET.fromstring(raw)
    print("QB_PUBLISHED_BASE_SELECTOR", identity["qb_id_operator_supplied"],
          xml.findtext("base_repo"), xml.findtext("buildconf_version"))
PYTHON
  shelves="$PWD/manifest/tizen10.0_shelves_1116_ffmpeg_seek_ltoexp2.txt"
  base_list="$PWD/manifest/tizen10.0_base_urls_1114_noprelink.txt"
  python3 -B -u "$d/qb-pair-gate.py.txt" "$official" "$custom" \
    "$shelves" "$shelves" "$base_list" "$base_list"
)
```

## Docs 04, 06 and 07

| Package | Retained P4 source and line | Executed Clang compile argv |
|---|---|---|
| AVControl | `avcontrol-app/packaging/org.tizen.AVControl.spec#4`, line 68 in `%build`, at CL 14215802. Replaces `CXXFLAGS` with ` -DEFL_BETA_API_SUPPORT ` before CMake. The same assignment appears in the verbose build at log line 938. | All 26 omit `-mthumb` and an explicit `-O`, so this group uses the Clang default optimization level in the observed configuration. |
| tv-viewer | `tv-viewer-app/packaging/org.tizen.tv-viewer.spec#42`, line 223 at CL 14299388, resets `CFLAGS` to ` -DEFL_BETA_API_SUPPORT`. `tv-viewer-app/CMakeLists.txt#31` line 485 assigns `CMAKE_CXX_FLAGS` from `CMAKE_C_FLAGS` and adds `-O1`. | All 549 omit `-mthumb`. Of these, 396 carry `-O1` and 153 omit an explicit `-O`. |
| dali2-adaptor / protobuf | Verbose controls | All 449 / 436 carry both `-mthumb` and `-Os`. |

The source ledger carries the exact P4 file revisions and SHA-256 from the retained read-only source capture. This is package-specific evidence for Doc 07 and the Doc 04 mechanism. The other A32-producing packages need their own build or packaging evidence. [Flag-origin ledger](../../artifacts/ledger/thumb-flag-origins-20261124.tsv)

**Doc 04 rows 2–3.** The AVControl and libpisa-ipc pairs matched all seven `.text` hashes between WARN `forceL` and FINAL `final2`. All seven full ELF digests differ. Executable sections other than `.text` were outside the check. Record tv-viewer and webappservice as historical lane C based on those two checks, with WARN provenance on both rows. Their own FINAL rebuilds would provide direct confirmation. [Pair output](../../artifacts/evidence/native-run-r0010w-weekend-and-r0011-capture-20261124.txt#L214)

**Doc 04 row 2 and Doc 06.** Doc 04's 4,630 → 2,362 KiB (−49.0%) is the historical image-listed ELF metric. The full exp8 payload sweep includes eight ARM ELFs across three RPMs and reports 10,760,504 → 5,005,836 B (−53.5%). Use the first figure for the historical table and the second for the full local replay. The later 17 November roster identifies two tv-viewer paths, `/usr/apps/org.tizen.tv-viewer/bin/tv-viewer` and `/usr/apps/org.tizen.tv-viewer/bin/tvcontrol-notify-manager`. That roster's executable-byte column covers all executable sections. The per-path readback below will test whether these two paths, or a subset, reproduce the historical `.text` row. The exact 11 November file-list membership remains open. The current published-image figures come from the overnight matched-ELF scan. [Historical method](../../artifacts/historical-reports/optimization-analysis-part-02.md#method-and-conditions) [A32 path evidence](../../artifacts/thumb-repro/a32-exact-top211-20261124.tsv)

| Historical local payloads | LLVM base .text (B) | LLVM forceL .text (B) | GCC gccL .text (B) | LLVM change | GCC change | Additional LLVM reduction |
|---|---:|---:|---:|---:|---:|---:|
| AVControl | 736,944 | 177,156 | 250,688 | −76.0% | −66.0% | 10.0 pp |
| tv-viewer | 10,760,504 | 5,005,836 | 7,568,568 | −53.5% | −29.7% | 23.8 pp |

The two GCC rows belong to the historical `gccL` comparison. The independently captured GCC reference QB 37564293 is the baseline for the new Doc 06.

**Doc 07 exact values.** The decompressed packet matched SHA-256 `3ef060f68b24199ee111ffd1820114ee9e5f50c11ce9731919bdfcc9e1aa76e4`. The exporter counted 42 top-211 rows with one or more changed fields and zero changes in ranks 212–609. Among the 42, 38 rows differ in A32 KiB and six in A32 share, with two rows in both groups. The 17 November scan still reports 5,166 loadable ELFs, 609 A32-predominant files and 359,746,207 estimated A32 bytes. The new TSV preserves exact bytes, basis and provenance. All rows had `NOT_CHECKED` installed-tree evidence in this readback. [Exact ranks 1–211](../../artifacts/thumb-repro/a32-exact-top211-20261124.tsv)

## Kernel ISA and EXP-T1

The retained GBS PERF vmlinux has 8,695,144 mapped ARM instruction bytes in Official and 8,442,560 in Customized. Both have zero mapped Thumb instruction bytes. Their executable sections contain 8,801,960 and 8,547,480 bytes respectively, including mapping data. The readback captured 7,100 compile argv per lane with zero direct mode options. This supports the PERF kernel exemption and satisfies the pilot's ISA/argv gate. Keep external modules exempt under the reviewed pilot rule. The vmlinux measurement covers the kernel image. Since both `PERF_CONFIG_NOT_FOUND` lines were returned, the `CONFIG_THUMB2_KERNEL` and `CONFIG_ARM_THUMB` values still need a config readback. [Kernel evidence](../../artifacts/evidence/native-run-r0010w-weekend-and-r0011-capture-20261124.txt#L414)

## R1–R7 delivery and historical figures

The first size page contains 138 variant measurements or status rows. Across the 153 inventory variants, the delivery ledger records 31 controls, four historical forced-option samples with verified delivery, 56 other changed-size comparisons with equal counts, 33 unproved rows, 18 whose returned payload metrics could not be measured and 11 whose treatment measurements are on the continuation page. A changed size with equal ELF counts still needs the exact path join. Equal section totals alone leave delivery and byte identity open. Reported silent or response-file runs also need complete command evidence to establish `NOT_DELIVERED`. The native audit checks path sets, per-ELF checksums, parsed compile and link argv and last-option precedence for mode choices. Its `NO_EFFECT` requires matching full ELF hashes and observed treatment argv. Inspect its recorded coverage before interpreting any missing flag. [First-pass variant ledger](../../artifacts/ledger/r1-r7-delivery-20261124.tsv)

The original report already says it excluded byte-identical packages in §6.8. The returned totals do not show that unchanged packages entered those historical aggregates. Recomputing the historical aggregates requires its exact installed ELF scope, comparable controls, and verified delivery or verified no effect. The early treatment logs confirm `FFLAGS` injection attempts on some runs. Other lines show direct compile argv or rejection. A quoted export proves only the attempted route. The `thr25` avoc-daemon build explicitly rejected the argument. Existing recipe JSON for R2–R6 remains gated until exact baseline, delivery and flag placement are confirmed. [Historical scope](../../artifacts/historical-reports/optimization-analysis-part-02.md#method-and-conditions) [Treatment output](../../artifacts/evidence/native-run-r0010w-weekend-and-r0011-capture-20261124.txt#L228)

| Experiment | Historical report delta | Returned local RPM payloads | Delivery for the next replay, pending review |
|---|---|---|---|
| R1 forced options | −36.2% .text and −25.9% loadable | Four delivered rows. 19,085,740 → 10,926,782 B .text (−42.75%), 33,117,461 → 20,496,551 B SHF_ALLOC (−38.11%). Local scope includes extra tv-viewer ELFs. | Use the approved exact `CCC_OVERRIDE_OPTIONS` hook with the existing exemption set. |
| R2 inline visibility | −44% dynamic symbol tables in the eligible cohort | Five changed-size variants, including two grpc variants. Some are different delivery attempts for the same source. Qualified installed-cohort total pending. | Append via `CCC_OVERRIDE_OPTIONS` to C++ compile commands only. Verify the existing package exclusions and symbol/consumer checks. |
| R3 ThinLTO | −0.1% .text, +0.5% loadable | Four changed-size pairs, +0.77% .text and +0.90% SHF_ALLOC. Provisional scope. grpc's equal sizes remain unproved. | Use a scoped Clang hook to replace the final LTO mode at both compile and link. Check the effective producer and final linker, including retained fat payload behavior. |
| R4 threshold 25 / 50 | Threshold 25 −36.1% .text and −23.3% loadable in affected samples. Threshold 50 was reported per package. | Changed-size pairs 25: n=4, −35.46% .text and −21.16% SHF_ALLOC. 50: n=2, −26.71% and −15.49%. Provisional scope. | Use a scoped hook for the paired `-mllvm` arguments and explicitly route the corresponding plugin option to LTO final links. Check both positions and keep ordinary links clear of plugin-only flags. |
| R5 MachineOutliner | −16.5% .text, −8.1% loadable | Two changed-size pairs, −16.20% .text and −7.12% SHF_ALLOC. Provisional scope. | Same phase-aware route as R4, with separate checks that the backend and LTO plugin received the outliner option. |
| R6 lld | +0.2% .text, +0.6% loadable | Four changed-size pairs, +0.15% .text and +0.77% SHF_ALLOC. Provisional scope. | Use the Clang link driver hook for `-fuse-ld=lld`; verify the actual accelerated linker path. Explicitly stage direct-ld build rules when present. |
| R6 safe ICF | −3.5% .text, −2.3% loadable versus GNU ld | Three changed-size pairs against lld, −3.53% .text and −2.84% SHF_ALLOC. Provisional scope. Different control from the report. | Apply `--icf=safe` at the final lld link, with an lld-only control. Check the actual final linker argv and DSO compatibility. |
| R7 RELR | 18.83 MB file-size estimate | No retained exp8 R7 measurement. | Use an explicit final-link treatment only after the established loader/packaging gate. |

SHF_ALLOC includes allocated NOBITS sections. None of the local totals measures residency. The local provisional rows give Claude the available change-based recalculation and identify where a qualified same-scope result still needs the readback. Compile-phase and link-phase options need a driver route that reaches the actual invocation despite make/CMake flag replacement. Where the driver is bypassed, instrument the direct build rule and verify its argv. This uses the approved R1 hook mechanism for review of new scoped lanes. `FFLAGS` remains historical evidence only. [Historical data](../../artifacts/historical-reports/optimization-analysis-part-01.md) [Rebuild results](../../artifacts/historical-reports/optimization-analysis-part-02.md#68-local-rebuild-measurements-thinlto-machineoutliner-lld-icf--fstack-protector-strong)

## One continuation command

Native server. By default this gathers verbose pages 1–11, treatments 1–2 and sizes 1 in one run, checks all three hashes and prints the numbered zlib+base64 packet. Copy the complete packet, including boundaries and SHA-256. If terminal paste limits apply, use `WEEKEND_PART=1` and then each subsequent part. The readback hashes and reads the retained logs only. Typical runtime is seconds on one CPU. Scratch use is a few MiB plus the script download.

Use the same launcher with `WEEKEND_MODE=kernel-config` to print config evidence tied to each retained vmlinux digest. It reads the adjacent `.config`, `include/config/auto.conf` and `include/generated/autoconf.h` if present. An empty option list in generated files means the symbol was omitted from that file. With `WEEKEND_MODE=tv-viewer` it prints the matched keys and sizes for the three retained variants, using RPM queries and streaming payload inspection. With `WEEKEND_MODE=delivery` it serially checks retained exp8 RPMs and driver logs. Allow 10–30 minutes, mostly local disk reads and decompression, and run after heavy jobs. Review `NO_EFFECT` and required exact argv coverage before making any whole-package absence claim.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0011b-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get 'be35ba2b4a6b56d78b0c0309b78eb6194506022b' 'artifacts/scripts/r0011b/weekend-readback.py.txt' 'c5d0facb0a8ddef6dd404655f82dbeb6b2cf3145992c5d30483e79112f19114f'
  part=()
  if [[ -n "${WEEKEND_PART:-}" ]]; then part=(--part "$WEEKEND_PART"); fi
  mode=${WEEKEND_MODE:-pages}
  case "$mode" in
    pages) python3 -B -u "$d/weekend-readback.py.txt" pages "${part[@]}" ;;
    kernel-config) python3 -B -u "$d/weekend-readback.py.txt" kernel-config ;;
    tv-viewer|delivery)
      get 'fb98eefaf6d924422466be70f4f95446583adeb1' 'artifacts/scripts/r0010e/exp8-readback.py.txt' 'feeff8d1e1521a70b17a05ce85a1e2fa42cefd31f37777064ac59864cd46f96d'
      get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75'
      args=()
      if [[ "$mode" == delivery ]]; then
        get 'fb98eefaf6d924422466be70f4f95446583adeb1' 'artifacts/ledger/r1-r7-variants-20261111.tsv' '6145591eb1830090aa5a51c182f64e9594429f603e656eb0cc9eea0b2203d73d'
        args=("$d/r1-r7-variants-20261111.tsv" "${part[@]}")
      fi
      python3 -B -u "$d/weekend-readback.py.txt" "$mode" "$d/exp8-readback.py.txt" "$d/image_mode_scan.py.txt" "${args[@]}"
      ;;
    *) exit 2 ;;
  esac
)
```

## Native order and Step 9

1. Step 2 gate above.
2. [GCC reference capture](0011_reply.md#gcc-reference-capture).
3. [Step 3](0011_reply.md#step-3-and-the-mlgo-base-proof) with `PERF_ACTION=usb-both`.
4. Board Step 5 and [MLGO Base proof](0011_reply.md#step-3-and-the-mlgo-base-proof). The model-only interpretation still needs the proof.
5. [Overnight HQ comparison](0011a_reply.md#overnight-hq-comparison).
6. Step 9 below.
7. [Step 8](0010c_reply.md), with the new Official capture.

For Steps 3, 5 and 8, set `OFFICIAL_CAPTURE` and `CUSTOM_CAPTURE` in the terminal that will run the older launchers.

```bash
export OFFICIAL_CAPTURE=/home1/chengkai/vd-tree/workspace/qb-evidence/37736448-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2
export CUSTOM_CAPTURE=/home1/chengkai/vd-tree/workspace/qb-evidence/37736427-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.1
```

Step 9 uses Official 37736448 as the dependency Product and the returned kernel ISA proof. It starts with `deviced` to review one pair before the other two. Set `PILOT_PACKAGE=gst-plugins-dash` or `inference-engine-tflite` for later pairs. The code replays the pinned historical P4 source revisions. Check the selected package source against the new publication before claiming a release-specific result. Run in the native GBS foreground after the overnight batch, one job with up to six pinned cores, typically 20–120 minutes per lane and up to 24 GiB per retained root, plus the checked 50 GiB disk reserve and 16 GiB RAM headroom. Network use covers GitHub launcher downloads, P4 reads and dependency RPMs. Claude review applies before new launcher use. [EXP-T1 verification and readback](0009_reply.md#4-run-the-exp-t1-gbs-pilot)

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0011b-tools.XXXXXX")
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
  official="$PWD/workspace/qb-evidence/37736448-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2"
  printf '%s  %s/identity.json\n' f164cf5f56ced88fd0618c68df686c79ec36aca85dbeb53972a4b128f135862d "$official" | sha256sum -c -
  OFFICIAL_PRODUCT_URL=$(python3 -B -c 'import json,sys; print(json.load(open(sys.argv[1]))["product"])' "$official/identity.json")
  KERNEL_PROOF="$PWD/workspace/temp/pm0009-kernel-isa.3sx1qo1w/isa-proof.json"
  PILOT_PACKAGE=${PILOT_PACKAGE:-deviced}
  args=()
  if [[ -n "${PILOT_PACKAGE:-}" ]]; then args+=(--package "$PILOT_PACKAGE"); fi
  sudo -v
  python3 -B -u "$d/thumb-force-pilot.py.txt" "$d/image-repo-lib.py.txt" "$d/gbs-mlgo-t7.py.txt" \
    "$d/gbs-thumb.py.txt" "$d/thumb-qb-sample.py.txt" "$d/image_mode_scan.py.txt" "$d/perf-bundle.py.txt" \
    "$d/qb37627297-source-pins-20261120.tsv" --dependency-product-url "${OFFICIAL_PRODUCT_URL:?}" \
    --kernel-proof "${KERNEL_PROOF:?}" "${args[@]}"
)
```
