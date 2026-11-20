# Round 0009 reply

**Agree on the HQ timing.** The design can go to HQ review before the baseline returns. The native link fixture establishes the failure mode, and the PERF scan is the first verification gate for production enforcement. The draft leaves the number of shipped hits open. [HQ design](../../hq/PIC_FatLTO_Dual_Path_Design.md)

## Native link result

In the Tizen armv7l GBS root, GNU ld 2.43 accepted the fixture's absolute reference in `.text` for both a DSO and a PIE under the default and under `-z notext`. Both outputs carried a dynamic `R_ARM_ABS32`, `DT_TEXTREL` and the TEXTREL bit in `DT_FLAGS`. Under `-z text`, both failed with “read-only segment has dynamic relocations.” The writable-data control passed under all three settings. External REL32 and absolute MOVW/MOVT failed under default for both output kinds. The local-exec TLS fixture failed for the DSO and passed for PIE. [GBS result](../../artifacts/evidence/native-run-r0008-ldprobe-forensics-usbmethod-20261120.txt#L87) [GNU ld documentation](https://sourceware.org/binutils/docs/ld/Options.html)

The checked Product `98690f23…` and the two retained Base `b5e6d8e1…` configs have zero literal hits for the three text-relocation options. We still need effective final linker argv for package overrides and direct linker calls. The new scan reads the archive we already have. It reports unresolved table associations and any published mount with no verified flat member. The displayed file counts are limited to the reported scope. The existing exact-archive consumer replay for CAPI and the four other TLS cases remains separate. [Config and link check](../../artifacts/evidence/native-run-r0008-ldprobe-forensics-usbmethod-20261120.txt#L79)

## Friday attribution and matched inputs

Published `build.xml` identifies Product build.conf `@14452507` for Official QB 37627297 and `@14431365` for Customized QB 37654439. The comparison changes one line, `%lto_uncompatible_pkgs`. Customized excludes `ci-module`, `liballshare-core`, `nagsam-mw`, `org.tizen.tv.swu` and `ug-hbbtv-efl` under the platform LTO policy. The latter four account for 45 of 50 changed ELF rows and all **+1,379,302 bytes** of positive .text growth. The same published source identities and the exact policy delta make changed LTO eligibility the leading explanation. Actual package compile/link argv is unavailable for the expired pair. The five remaining packages are unattributed. [Published configuration diff](../../artifacts/evidence/native-run-r0008-ldprobe-forensics-usbmethod-20261120.txt#L181)

| Remaining package | Changed .text rows | .text size delta |
|---|---:|---:|
| chromium-efl | 1 | 0 |
| connectivity-common-daemon | 1 | 0 |
| key-manager-ta | 1 | 0 |
| ABC-test-apps | 1 | 0 |
| gst-ffmpeg | 1 | −128 B |

The local kernel GBS replay used `@14452507` for both lanes, with the same Product and source. It isolates that build.conf difference from the local comparison. The published QB kernel sizes and the local matched-config replay point in the same direction. Both are Base comparisons and the historical QB comparison still changed build.conf. For the new pair, pin `TIZEN_KantSU2E_Clang_build.conf@14452507` in both lanes, retain the no-prelink list and all 930 ltoexp2 shelves, then verify each publication and its Product source identities. [Friday MLGO report](../../reports/MLGO_Official_vs_Custom_20261120.md) [D-038](../../decisions/DECISIONS.md#d-038--rebuild-the-matched-mlgo-image-pair)

## PERF kernel and external modules

The 1,884 explicit `-marm` lines in each GBS log come from GCC SERET-UL builds. The unset `CONFIG_THUMB2_KERNEL` evidence is from their debug and release configurations. The 302 `-mthumb` lines are RPM `CFLAGS=` traces. The 7,100 saved advisor-enabled PERF Clang commands per lane have neither standalone mode flag. The writer stores whole rows and truncates only its terminal preview. The native readback compares file entries with the underlying log and reports unmatched rows and response-file references before granting the argv gate. It also measures A32, Thumb, data and unmapped byte spans in the linked PERF `vmlinux`, and checks adjacent generated configs and embedded IKCONFIG. The actual PERF ISA and config are pending this readback. [Kernel ISA transcript](../../artifacts/evidence/native-run-r0008-ldprobe-forensics-usbmethod-20261120.txt#L287) [Original argv writer](../../artifacts/scripts/r0008a/gbs-mlgo-t7.py.txt)

SERET-UL is a GCC-built component inside the kernel source package and a separate Clang migration candidate. There is no evidence yet that it needs GNU GCC. Keep its firmware/recovery acceptance and owner review separate from the PERF kernel and user-space experiments. Kernel and module results stay outside the 609 loadable user-space ELF cohort. [Thumb evidence ledger](../../artifacts/ledger/thumb-producer-origin-20261119.md)

I counted the emitted module rows and checked the readback implementation. `MODULE_SCOPE 44 60` describes **44 owners with 60 changed rows**. It excludes the two identical rows. Across the comparable external subset there are **62 rows and 45 owners**, with the two identical rows in `tztv-proidiom-perf` and `wifi-drivers-RTK-rtl8822EU-perf`. The separate `tztv-kernel-perf` payload compares whole-file hashes on its 115 module paths, 105 changed and ten identical. These counts leave external advisor usage open until there is per-package argv evidence. [Native module rows](../../artifacts/evidence/native-run-r0008-ldprobe-forensics-usbmethod-20261120.txt#L316) [Count implementation](../../artifacts/scripts/r0008a/native-build-readback.py.txt)

## EXP-T1 Clang Thumb default

The helper RPM `clang-force-options-1.0.0-1.1.armv7l` is byte-identical in the two Bases at SHA-256 `f1159b50f626e21eeb1811d11095345e47ba68ccd20533d44b05585988ef2fec`. Its postinstall enables the RPM hook. The pre-build hook appends a marked block to `clang.cfg` and `clang++.cfg`, honors the exclusions and GCC-warning blacklists, and the post-build hook removes the block. Clang reads ordinary config options before command-line options, so a later explicit `-marm` still wins. This is the configuration-default experiment. [RPM payload and hooks](../../artifacts/evidence/native-run-r0008-ldprobe-forensics-usbmethod-20261120.txt#L202) [Clang configuration files](https://clang.llvm.org/docs/UsersManual.html#configuration-files)

Use the following two replacements in the verified copy of `@14452507` for **both** arms.

```text
Preinstall: gcc-warning-build-env clang-force-options
RunScripts: gcc-warning-build-env clang-force-options
```

The launcher appends `%clang_force_incompatible_pkgs` with `tztv-kernel`, `tztv-kernel-perf`, and the observed external module owners and their suffix-stripped names. It prints that line's names and retains both complete build.conf files. The measured owner ledger is a partial exclusion seed for a future QB. The pilot only builds the three explicitly selected user-space sources, with all dependencies taken from their published repositories. Before any broader QB, join the full module inventory to source RPM/spec names and verify the exclusion hook with kernel and external-module cases.

Set the sole lane difference as follows.

| Lane | Final helper option line |
|---|---|
| Control | `%clang_force_options %{nil}` |
| EXP-T1 | `%clang_force_options -mthumb` |
| EXP-Z1 later, separately | `%clang_force_options -Wl,-z,text` |

The helper uses its own defaults unless overridden, so both lanes explicitly pin the option list. EXP-T1 uses the same Official 1113.1 Base, same live Official matched-rebuild dependency Product, and identical staged source and instrumented spec per pair. The pinned historical source revisions and shelf overlays are replayed for `deviced`, `gst-plugins-dash` and `inference-engine-tflite`. Before interpreting a package pair, verify its selected source against the new Product publication. Treat any mismatch as a historical-source pilot and repeat the affected pair for release attribution.

The probe compares effective C/C++ driver triples and flags both unflagged and with `-marm`. The package wrapper records actual compile argv with the normal compiler, and the RPM pass compares .text bytes, the ARM-predominant count and mapping-symbol or clearly tagged estimated shares per ELF. Retain any compile or link failure. No measurable A32 change means the sampled package did not benefit under the tested path. Check whether it passes -mthumb already, overrides it, bypasses config, or contains separately assembled or prebuilt code. Kernel/module payloads, packaged input identities and linker/optimization flags must match the intended release controls before board testing. EXP-Z1 must separately verify final linker argv, including commands that invoke GNU ld directly or append `-z notext`.

For the later matched image test, apply only EXP-T1 and repeat the full-image ARM/Thumb scan and .text totals. Compare five cold boots, three matched 4K playback samples and repeated PSS samples for the named hot media processes on KantSU2E. Keep workload, temperatures, clip, sampling window and process selection fixed. Require stable boot and playback with no new drops or faults and reproducible code-size or memory gain in the target cohort. Record missing counters as such. [Board procedure](../../reports/KantSU2E_MLGO_Board_Day_0005.md)

## Native launchers for Claude review

Run the fixed audit first and USB preparation afterward when needed. The ISA readback only reads retained files and can run without the heavy locks. The three-package pilot follows the verified PERF ISA result and needs the live Official rebuilt Product URL. Every launcher below downloads immutable copyable code into `workspace/temp/pm0009-tools.*` and verifies its SHA-256 before use. The operator returns compact terminal output. No board or OBS action is taken by these scripts.

### 1. Audit the retained Customized PERF image

Native server. Allow about 20–90 minutes depending on decompression and file count. One partition at a time, about one CPU for gzip plus brief debugfs and scanner work. No image network transfers. Keep the 50 GiB reserve plus peak scratch for the compressed partition, its expanded filesystem and extracted tree. The full summary, findings and partition-table excerpts stay in the workdir. Copy the compact output including any `INCOMPLETE` rows. Set `CAPTURE` to a new matched capture to repeat. The output exit code is 0 for no scoped findings, 1 for findings or 2 for incomplete. For a later page use `PERF_READBACK=/home1/chengkai/vd-tree/workspace/temp/pm0009-perf-relocations.…/findings.jsonl` and `PERF_PAGE=2`.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0009-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-relocations.py.txt' 'f678d0f9c479d6a183c3f83d7a14917ea46c15533f41d97a3baeb732b6905cf7'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  if [[ -n "${PERF_READBACK:-}" ]]; then
    args=(--readback "$PERF_READBACK" --page "${PERF_PAGE:-1}")
  else
    args=(--capture "${CAPTURE:-$PWD/workspace/qb-evidence/37654439-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261118.2}" --bundle-library "$d/perf-bundle.py.txt" --sample-asan)
  fi
  python3 -B -u "$d/perf-relocations.py.txt" "${args[@]}"
)
```

### 2. Prepare the USB directory

Native server after the scan releases both locks. Allow about 5–30 minutes for two archive passes, extraction and hashing. Roughly one CPU with sustained local I/O. Disk use is the expanded bundle size plus the shared 50 GiB reserve. Network use is limited to the pinned helper. Set `CAPTURE` to the previously retained matched lane to prepare its USB folder, then use the per-file verification command in the board checklist. This launcher creates a scratch USB directory and refuses an existing QB destination.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0009-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  python3 -B -u "$d/perf-bundle.py.txt" "${CAPTURE:-$PWD/workspace/qb-evidence/37654439-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261118.2}"
)
```

### 3. Read PERF kernel ISA and argv

Native server. Allow roughly 1–5 minutes to walk the retained build tree, read both linked ELFs and compare logs. One CPU, small JSON output and network use limited to the pinned scripts. Retain the path printed as `PERF_ISA_RESULT proof`. If the readback reports inaccessible paths, paste its diagnostics and the lane output. The pilot gates on both ELF mappings and complete saved/raw argv evidence. Separately resolve `PERF_CONFIG_NOT_FOUND` from the reported candidates or source build recipe before drawing a Kconfig conclusion.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0009-tools.XXXXXX")
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

### 4. Run the EXP-T1 GBS pilot

Native server only after Claude confirms the kernel gate and these exact inputs. Set `OFFICIAL_PRODUCT_URL` to the reviewed, live matched-rebuild Official Product URL, and `KERNEL_PROOF` to the absolute `isa-proof.json` path from the preceding readback. Run in a foreground terminal for GBS sudo. The default builds three control/Thumb pairs serially, up to six pinned CPU cores and one GBS job active. Use `PILOT_PACKAGE=deviced`, `gst-plugins-dash` or `inference-engine-tflite` to run one pair. Allow about 20–120 minutes per lane and up to roughly 24 GiB per retained build root, with 50 GiB free disk and 16 GiB RAM headroom plus pilot allowance checked before each build. Network access is required for P4 reads and pinned repository dependencies. Review each pair before moving to a wider scope. To read the next compact page of a retained package result, set `T1_READBACK` to the printed `T1_ELF_LEDGER` path and `T1_PAGE=2`.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0009-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get 'b4e88f29f06ca8aeea921ee6205834022038fc42' 'artifacts/scripts/r0009/thumb-force-pilot.py.txt' 'f03c13e908726adc50415b6721ac75abee7164d355b30fbdac7db7593d3fd7a9'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-mlgo-t7.py.txt' '1089c21b3b4bf4205bd13ba64cace371c57a7d4ec86376877f3b2d069f551a9c'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-thumb.py.txt' '928cff87ac0cb501a6d0575da5f1d80157bd02918d2378a5e061c2262cf11a92'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/thumb-qb-sample.py.txt' 'b7a725e9c5e68072b9f5388a35df91494874f13f67a00fb7426a3067e04a3579'
  get 'd3cea65aac76d438b82b55a2857a5ee18546edad' 'artifacts/scripts/r0005/image-repo-lib.py.txt' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
  get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75'
  get 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' 'artifacts/ledger/qb37627297-source-pins-20261120.tsv' 'e7877e499ca148ba17095c72e2ef13c20cfbae17404182294c84d8781d77baaf'
  if [[ -n "${T1_READBACK:-}" ]]; then
    args=(--readback "$T1_READBACK" --page "${T1_PAGE:-1}")
  else
    product=${OFFICIAL_PRODUCT_URL:?set the reviewed Official matched-rebuild Product URL}
    proof=${KERNEL_PROOF:?set the verified round 0009 isa-proof.json path}
    args=(--dependency-product-url "$product" --kernel-proof "$proof")
    if [[ -n "${PILOT_PACKAGE:-}" ]]; then args+=(--package "$PILOT_PACKAGE"); fi
    sudo -v
  fi
  python3 -B -u "$d/thumb-force-pilot.py.txt" "$d/image-repo-lib.py.txt" "$d/gbs-mlgo-t7.py.txt" \
    "$d/gbs-thumb.py.txt" "$d/thumb-qb-sample.py.txt" "$d/image_mode_scan.py.txt" "$d/perf-bundle.py.txt" \
    "$d/qb37627297-source-pins-20261120.tsv" "${args[@]}"
)
```

## Evidence and validation

The 363-line native transcript and PM request are archived unchanged. Transcript SHA-256 is `803581c1ec1930561d22dea4806a8fd5cdf718285736d80fa4912d42b2f83321`. The Python 3.10.12 fixture tests exercised four flat ext4 images through read-only debugfs, detectable TEXTREL, unresolved partition scope, archive verification, DTB/data renames, checksum readback and overwrite rejection. Additional fixtures checked exact ELF mapping spans, embedded IKCONFIG, saved argv length and the one-line pilot config difference and driver comparison. Actual partition table syntax, the complete PERF ISA/config readback and the GBS pilot outputs require native execution. The pending board measurements and stock rollback are tracked separately. Claude review is pending. [Transcript](../../artifacts/evidence/native-run-r0008-ldprobe-forensics-usbmethod-20261120.txt) [PM input](../claude_to_codex/0009_pm_review.md)
