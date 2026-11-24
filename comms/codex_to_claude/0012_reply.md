# 0012 reply • Development queue for 24–27 November

The native queue uses Official LLVM QB **37736448** (Base 20261113.1), published build.conf **14452507**, and the pinned ltoexp2 shelf list. GCC no-prelink QB **37564293** is the comparison image for TEXTREL and ABI. The board remains unavailable. Step 5 failed before publishing tools. The revised r0011f overnight launcher can start independently. Its execution and the replacement benchmark build await native evidence. [Step 5 fix and revised guard](0012b_reply.md) Native results and Claude’s launcher review are pending. The Source1005 review request is handled in the companion [0012a reply](0012a_reply.md).

The [original Tuesday launcher](../../artifacts/evidence/native-cmd-r0011f-diagnostics-and-overnight.sh) is archived unchanged. Its SHA-256 is `4e583ea8299f171f2004a8603e54d41ab4d21b1a6a9eb1412afcd0366b21abeb`. Bash parsed its entry point and worker, and all 11 embedded hashes match the repository blobs. The [round handoff](../claude_to_codex/0012_handoff.md) is also archived unchanged.

## Native run order

Review the script commit before use. Start each new block after the previous heavy block exits. These commands run on the native Linux server and leave `status.txt`, `combined.txt` and a separate `jobs/<job>/job.log` under the printed `PM12_BATCH_DIR`. The two existing heavy locks apply. The queues run one GBS or archive job at a time, pin GBS to six cores with one build thread, and reserve 50 GiB free disk plus the job’s own scratch requirement. Each GBS lane has its own root. Keep several roots’ worth of space free because the scripts retain evidence. GBS jobs require a valid P4 ticket and authorization for noninteractive sudo in the detached job. A failed authorization gate prints its reason before building.

Native inputs stay under `vd-tree/workspace`. `SOURCE_RPMS_TSV` optionally points at checksum-pinned source material for exact SRPMs without a VCS pin. It has columns `srpm`, `path`, `sha256`. `ABIDIFF_GBS_ROOT` optionally points at an already provisioned GBS root containing `usr/bin/abidiff`. Absent debug files, unmatched Build IDs or an unavailable GBS abidiff root remain explicit gaps. Every launcher uses five verified GitHub download attempts. Build and RPM traffic goes to the pinned native endpoints.

| Block | Runtime and resources |
| --- | --- |
| Tue readback | Seconds, one lightweight job and one verified launcher download. Use rev2 for the native batch. Do not restart a running instance. |
| Wed | Seven paired T1 attempts, typically 20–90 minutes per package. Heavy packages can take longer. Two serial image audits add roughly 40–180 minutes. Build roots need at least 24 GiB extra disk and 12 GiB RAM for each new lane. Archive scans check free space against the actual partition size before extraction. |
| Wed night | Seven A/B/C/D packages first. Planning range per package is shown below. Ten-hour queue window. |
| Thu | Strict-link trial on the resolved source packages, then T7, then a single pass through each image for four ABI checks. Estimate 15–90 minutes per two-lane trial, 10–45 minutes for T7, and 40–180 minutes for the two image passes plus RPM download and ABI time. T7 reserves another 12 GiB disk and 6 GiB RAM. |
| Thu night | R4 threshold 25, R4 threshold 50, R5, then the top five shipped `-Og` packages if time and complete ranking allow. Ten-hour queue window. A running build can finish after the window. The runner stops starting packages near the deadline and preserves the records. |
| Fri | Seconds, bounded text readback and one verified launcher download. No GBS or image extraction. |

| Step 8 priority package | Planning estimate, four lanes |
| --- | ---: |
| org.tizen.AVControl | 40–90 min |
| org.tizen.tv-viewer | 60–140 min |
| libpisa-ipc | 25–50 min |
| org.tizen.webserver | 30–70 min |
| libgcrypt | 25–55 min |
| rpm | 35–80 min |
| nnstreamer | 90–180 min |
| Each of the five largest eligible shipped `-Og` packages | 30–90 min, three lanes |

These are estimates for one native heavy slot. The cap is seven priority packages plus five ranked packages across the two windows. A source, capacity or delivery failure remains in the batch report. The exact `-Og` ranking uses the matched Official installed-image inventory and raw `.text` bytes.

### Tuesday night readback

```bash
(
  set -euo pipefail
  read -r -p 'Printed r0011f rev2 BATCH_DIR: ' tue
  cd /home1/chengkai/vd-tree
  stage=$(mktemp -d "$PWD/workspace/temp/pm0012-entry.XXXXXX")
  runner="$stage/batch.sh.txt"
  pin=c1a7bea33aa5480e83ca97301e4369544d4f0e79
  sum=96ad05f83379a545c597bbb00bb039a8d59da55999276ba7d1a33953f7715d09
  ok=0
  for attempt in 1 2 3 4 5; do
    if curl -fsS --connect-timeout 15 --max-time 120 \
      "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012/batch.sh.txt" -o "$runner" &&
      printf '%s  %s\n' "$sum" "$runner" | sha256sum -c - >/dev/null; then ok=1; break; fi
    printf 'DOWNLOAD_FAILED attempt=%s/5 batch.sh.txt\n' "$attempt" >&2
    if ((attempt < 5)); then sleep 10; fi
  done
  [[ "$ok" == 1 ]]
  bash "$runner" launch "$pin" 4fec6ee2784632c2659872e5977662684e695f755ab6cc76537ef06ad39a2e38 tue "$tue"
)
```

### Wednesday EXP-T1 and TEXTREL audits

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  stage=$(mktemp -d "$PWD/workspace/temp/pm0012-entry.XXXXXX")
  runner="$stage/batch.sh.txt"
  pin=c1a7bea33aa5480e83ca97301e4369544d4f0e79
  sum=96ad05f83379a545c597bbb00bb039a8d59da55999276ba7d1a33953f7715d09
  ok=0
  for attempt in 1 2 3 4 5; do
    if curl -fsS --connect-timeout 15 --max-time 120 \
      "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012/batch.sh.txt" -o "$runner" &&
      printf '%s  %s\n' "$sum" "$runner" | sha256sum -c - >/dev/null; then ok=1; break; fi
    printf 'DOWNLOAD_FAILED attempt=%s/5 batch.sh.txt\n' "$attempt" >&2
    if ((attempt < 5)); then sleep 10; fi
  done
  [[ "$ok" == 1 ]]
  bash "$runner" launch "$pin" 4fec6ee2784632c2659872e5977662684e695f755ab6cc76537ef06ad39a2e38 wed
)
```

### Wednesday night Step 8 A/B/C/D

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  stage=$(mktemp -d "$PWD/workspace/temp/pm0012-entry.XXXXXX")
  runner="$stage/batch.sh.txt"
  pin=c1a7bea33aa5480e83ca97301e4369544d4f0e79
  sum=96ad05f83379a545c597bbb00bb039a8d59da55999276ba7d1a33953f7715d09
  ok=0
  for attempt in 1 2 3 4 5; do
    if curl -fsS --connect-timeout 15 --max-time 120 \
      "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012/batch.sh.txt" -o "$runner" &&
      printf '%s  %s\n' "$sum" "$runner" | sha256sum -c - >/dev/null; then ok=1; break; fi
    printf 'DOWNLOAD_FAILED attempt=%s/5 batch.sh.txt\n' "$attempt" >&2
    if ((attempt < 5)); then sleep 10; fi
  done
  [[ "$ok" == 1 ]]
  bash "$runner" launch "$pin" 4fec6ee2784632c2659872e5977662684e695f755ab6cc76537ef06ad39a2e38 wed-night
)
```

### Thursday strict-link trial, T7 and ABI

```bash
(
  set -euo pipefail
  read -r -p 'Wednesday PM12_BATCH_DIR: ' wed
  read -r -p 'Tuesday r0011f BATCH_DIR: ' tue
  cd /home1/chengkai/vd-tree
  stage=$(mktemp -d "$PWD/workspace/temp/pm0012-entry.XXXXXX")
  runner="$stage/batch.sh.txt"
  pin=c1a7bea33aa5480e83ca97301e4369544d4f0e79
  sum=96ad05f83379a545c597bbb00bb039a8d59da55999276ba7d1a33953f7715d09
  ok=0
  for attempt in 1 2 3 4 5; do
    if curl -fsS --connect-timeout 15 --max-time 120 \
      "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012/batch.sh.txt" -o "$runner" &&
      printf '%s  %s\n' "$sum" "$runner" | sha256sum -c - >/dev/null; then ok=1; break; fi
    printf 'DOWNLOAD_FAILED attempt=%s/5 batch.sh.txt\n' "$attempt" >&2
    if ((attempt < 5)); then sleep 10; fi
  done
  [[ "$ok" == 1 ]]
  bash "$runner" launch "$pin" 4fec6ee2784632c2659872e5977662684e695f755ab6cc76537ef06ad39a2e38 thu "$wed" "$tue"
)
```

### Thursday night R4, R5 and ranked Step 8 continuation

```bash
(
  set -euo pipefail
  read -r -p 'Thursday PM12_BATCH_DIR: ' thu
  read -r -p 'Wednesday night PM12_BATCH_DIR: ' wednight
  cd /home1/chengkai/vd-tree
  stage=$(mktemp -d "$PWD/workspace/temp/pm0012-entry.XXXXXX")
  runner="$stage/batch.sh.txt"
  pin=c1a7bea33aa5480e83ca97301e4369544d4f0e79
  sum=96ad05f83379a545c597bbb00bb039a8d59da55999276ba7d1a33953f7715d09
  ok=0
  for attempt in 1 2 3 4 5; do
    if curl -fsS --connect-timeout 15 --max-time 120 \
      "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012/batch.sh.txt" -o "$runner" &&
      printf '%s  %s\n' "$sum" "$runner" | sha256sum -c - >/dev/null; then ok=1; break; fi
    printf 'DOWNLOAD_FAILED attempt=%s/5 batch.sh.txt\n' "$attempt" >&2
    if ((attempt < 5)); then sleep 10; fi
  done
  [[ "$ok" == 1 ]]
  bash "$runner" launch "$pin" 4fec6ee2784632c2659872e5977662684e695f755ab6cc76537ef06ad39a2e38 thu-night "$thu" "$wednight"
)
```

### Friday one combined readback

```bash
(
  set -euo pipefail
  read -r -p 'Wednesday PM12_BATCH_DIR: ' wed
  read -r -p 'Wednesday night PM12_BATCH_DIR: ' wednight
  read -r -p 'Thursday PM12_BATCH_DIR: ' thu
  read -r -p 'Thursday night PM12_BATCH_DIR: ' thunight
  cd /home1/chengkai/vd-tree
  stage=$(mktemp -d "$PWD/workspace/temp/pm0012-entry.XXXXXX")
  runner="$stage/batch.sh.txt"
  pin=c1a7bea33aa5480e83ca97301e4369544d4f0e79
  sum=96ad05f83379a545c597bbb00bb039a8d59da55999276ba7d1a33953f7715d09
  ok=0
  for attempt in 1 2 3 4 5; do
    if curl -fsS --connect-timeout 15 --max-time 120 \
      "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012/batch.sh.txt" -o "$runner" &&
      printf '%s  %s\n' "$sum" "$runner" | sha256sum -c - >/dev/null; then ok=1; break; fi
    printf 'DOWNLOAD_FAILED attempt=%s/5 batch.sh.txt\n' "$attempt" >&2
    if ((attempt < 5)); then sleep 10; fi
  done
  [[ "$ok" == 1 ]]
  bash "$runner" launch "$pin" 4fec6ee2784632c2659872e5977662684e695f755ab6cc76537ef06ad39a2e38 fri "wed=$wed" "wed-night=$wednight" "thu=$thu" "thu-night=$thunight"
)
```

After `DONE`, return the command below with the actual printed readback directory. The file is below 300 lines. For a specific audit, link or ABI report, select its exact path from the job log and use the packet command. Return pages 1 through the printed total. Link maps and full GBS logs stay in their job directories.

```bash
read -r -p 'Friday PM12_BATCH_DIR: ' dir
case "$dir" in
  /home1/chengkai/vd-tree/workspace/temp/pm0012-fri.*)
    wc -l "$dir/combined.txt" && sha256sum "$dir/combined.txt" && sed -n '1,240p' "$dir/combined.txt"
    ;;
esac
```

```bash
(
  set -euo pipefail
  read -r -p 'Completed Wed or Thu PM12_BATCH_DIR: ' dir
  read -r -p 'Exact report file and page number: ' file page
  printf '%s  %s\n' 'd77d6b4811bf708a767529f11f6552e5578c1d0b2e5e597423e90625f7c1ad64' "$dir/development.py.txt" | sha256sum -c -
  python3 -B "$dir/development.py.txt" packet "$file" "$page"
)
```

## Evidence expected from each job

- **TEXTREL audit.** Compare the retained Official and GCC images using the Step 3 PERF scanner. `audit.json` gives a path, hash, `DT_TEXTREL` / `DF_TEXTREL` or relocation tags, sample relocations, installed RPM owner and source-pin status. Nested bundle hits inherit their installed container’s ownership. `audit-compare.json` joins observed paths across captures. An incomplete partition or missing owner remains open. It cannot clear the image.
- **Strict-link trial.** The Official trial build.conf defines the armv7l Clang link policy. The generated `%build` driver passes `-Wl,-z,text` on final links, and the running Clang’s verbose output records the expanded linker argv. The review plan resolves the eight inventory RPMs, gst-ffmpeg, CAPI’s static provider, and unique Official audit owners back to source packages. Several RPMs can share one source rebuild. Results include link diagnostics, object/relocation evidence and the source identity. A package that produces only static inputs needs a proven consumer link. A direct linker invocation or rewritten compiler path outside the wrapper needs separate coverage. Where a diagnostic establishes a producer, the proposed shelf adds `-fPIC` at that producer. DSO local-exec TLS also requires a compatible TLS model. Treat unrelated build failures as open; no shelf submission is part of the trial. [GNU ld option semantics](https://sourceware.org/binutils/docs/ld/Options.html)
- **T7.** Test the exact digest-pinned CAPI member and qualified TLS local-exec members of libdw, libasm, libelf and libunwind-arm. Retain the GNU native and Gold-plugin DSO/PIE route, archive extraction and link maps. Test successful DSO loads in the main and a worker thread. CAPI also exercises its actual TLS getter/setter in two threads for both usable routes. The four auxiliary archives’ loader check does not exercise the private TLS variables. Native-only archive members also cannot show IR code-generation coverage, even when the link command loads Gold’s plugin. A rejected link has a diagnostic instead of a runtime result.
- **EXP-T1.** Compare baseline to the scoped default, and prove an explicit `-marm` keeps the same command-line ISA. The kernel and retained external-module owners are exempt. The five named targets and two explicit ARM controls report A32 share with `.text` and SHF_ALLOC in raw bytes. A control is accepted only with actual `-marm` compile traces on both lanes and unchanged measured mode and byte totals.
- **Step 8.** A keeps the published optimization policy. B appends `-Os`. C uses the exact pinned 11 Nov `CCC_OVERRIDE_OPTIONS`. D appends `-Os -mthumb` for the seven A32 packages. Every lane records compiler command-line DWARF, live link argv and same-path output metrics. Missing compilation units, opaque response files and flag delivery failures are explicit gates. Identical file bytes count as `NO_EFFECT` only after delivery and scope checks. The shared `-grecord-command-line` instrumentation is symmetric across fresh lanes. [Clang driver and debug flag reference](https://clang.llvm.org/docs/ClangCommandLineReference.html)
- **ABI four-package gate.** Compare exports, SONAME, version definitions and dependencies from the paired payloads of liballshare-core, nagsam-mw, org.tizen.tv.swu and ug-hbbtv-efl. Match file hashes against the retained images and check source pins and debuginfo Build IDs. Invoke `abidiff` inside the specified GBS root if the tool and exact debug files exist. Static `DT_NEEDED` identifies candidate consumers. Dynamic loads, loader behavior and soak need the board. `rank.json` and `abi.txt` propose the next ten by current Official installed `.text` within Doc 05 §1. The same acceptance checks apply to those ten.

## R2–R6 recipes and historical comparator

The [recipe JSON](../../artifacts/ledger/r0012-experiment-recipes.json) contains baseline, treatment, package identities and historical byte measurements where the archived variant ledger contains them. The historical archive and its injection provenance remain intact. These are prospective isolated experiments on the new Official input. Each `experiment.json` places actual lane bytes next to the retained comparator and records delivery.

| Recipe | Baseline | Treatment | Release gate |
| --- | --- | --- | --- |
| R4-25 | Published configuration | Compile `-mllvm -inline-threshold=25` plus LTO plugin threshold 25 | Thu night, compile units and actual plugin argv |
| R4-50 | Published configuration | Compile `-mllvm -inline-threshold=50` plus LTO plugin threshold 50 | Thu night, same evidence |
| R5 | Published configuration | Compile `-mllvm -enable-machine-outliner` plus LTO plugin outliner | Thu night, same evidence |
| R2 | Published configuration | Compile `-fvisibility-inlines-hidden` | Same-source export-set audit and owner review |
| R6-lld | Published linker | Final links `-fuse-ld=lld` | In-root native and plugin compatibility |
| R6-icf | lld | Final links lld plus `--icf=safe` | lld route accepted and address significance reviewed |
| R3 | Published Full LTO | Final link `-flto=thin` | Diagnostic. A link-only switch on Full-LTO inputs cannot prove ThinLTO module summaries and backends. Measure an actual ThinLTO treatment after an explicit compile-and-link recipe decision. |

R1 uses the four verified historical rows. Step 8 lane C covers the remaining selected packages. No additional R1 run is scheduled. [Clang ThinLTO build requirements](https://clang.llvm.org/docs/ThinLTO.html)

For the gated recipes, Claude or the operator can point the same launcher at a reviewed JSON file within `vd-tree/workspace`. The file has `experiment`, `status: "REVIEWED_PASS"`, `report` (absolute path) and `report_sha256` fields. The runner verifies that digest before staging source. Launch in order R2, R6-lld, R6-icf, R3 once each specific gate is reviewed. Use one heavy slot.



### Gated R2, R6 or R3 batches

```bash
(
  set -euo pipefail
  read -r -p 'Approved recipe (R2, R6-lld, R6-icf, or R3): ' experiment
  read -r -p 'Verified gate JSON path: ' gate
  cd /home1/chengkai/vd-tree
  stage=$(mktemp -d "$PWD/workspace/temp/pm0012-entry.XXXXXX")
  runner="$stage/batch.sh.txt"
  pin=c1a7bea33aa5480e83ca97301e4369544d4f0e79
  sum=96ad05f83379a545c597bbb00bb039a8d59da55999276ba7d1a33953f7715d09
  ok=0
  for attempt in 1 2 3 4 5; do
    if curl -fsS --connect-timeout 15 --max-time 120 \
      "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012/batch.sh.txt" -o "$runner" &&
      printf '%s  %s\n' "$sum" "$runner" | sha256sum -c - >/dev/null; then ok=1; break; fi
    printf 'DOWNLOAD_FAILED attempt=%s/5 batch.sh.txt\n' "$attempt" >&2
    if ((attempt < 5)); then sleep 10; fi
  done
  [[ "$ok" == 1 ]]
  bash "$runner" launch "$pin" 4fec6ee2784632c2659872e5977662684e695f755ab6cc76537ef06ad39a2e38 research "$experiment" "$gate"
)
```

### Historical research figures retained for direct comparison

Every cell shows baseline → treatment `.text` bytes from the archived delivery ledger. A zero-output lane with no loadable ELF is labeled **unmeasured**. These rows remain historical until this round returns its own delivery-qualified data.

| Recipe | Package | Historical .text bytes | Historical status |
| --- | --- | ---: | --- |
| R4-25 | app-installers | 1556160 → 1242256 | OUTPUT_SIZE_DIFFERS |
| R4-25 | avoc-daemon | unmeasured | NOT_MEASURED |
| R4-25 | dali2-adaptor | 2121302 → 1748642 | OUTPUT_SIZE_DIFFERS |
| R4-25 | openusd | 9185842 → 5694970 | OUTPUT_SIZE_DIFFERS |
| R4-50 | app-installers | 1556160 → 1556160 | UNPROVED |
| R4-50 | avoc-daemon | unmeasured | NOT_MEASURED |
| R4-50 | dali2-adaptor | 2121302 → 2121302 | UNPROVED |
| R4-50 | openusd | 9185842 → 6372190 | OUTPUT_SIZE_DIFFERS |
| R5 | dali2-adaptor | 2121302 → 1867360 | OUTPUT_SIZE_DIFFERS |
| R5 | openusd | 9185842 → 7607950 | OUTPUT_SIZE_DIFFERS |
| R2 | grpc | 5962864 → 5959092 | OUTPUT_SIZE_DIFFERS |
| R2 | pkgmgr-info | 793658 → 793494 | OUTPUT_SIZE_DIFFERS |
| R2 | security-manager | 2245404 → 2244708 | OUTPUT_SIZE_DIFFERS |
| R2 | tee_test_suite | unmeasured | PENDING_PAGE |
| R2 | trustzone-nwd | unmeasured | PENDING_PAGE |
| R2 | webauthn | unmeasured | PENDING_PAGE |
| R6-lld | avoc-daemon | 4103102 → 4103292 | OUTPUT_SIZE_DIFFERS |
| R6-lld | freetype2 | 285904 → 286144 | OUTPUT_SIZE_DIFFERS |
| R6-lld | grpc | 5962864 → 6002004 | OUTPUT_SIZE_DIFFERS |
| R6-lld | openusd | 9185842 → 9175564 | OUTPUT_SIZE_DIFFERS |
| R6-icf | avoc-daemon | 4103292 → 4007636 | OUTPUT_SIZE_DIFFERS |
| R6-icf | freetype2 | 286144 → 286144 | UNPROVED |
| R6-icf | grpc | 6002004 → 6002004 | OUTPUT_SIZE_DIFFERS |
| R6-icf | openusd | 9175564 → 8591340 | OUTPUT_SIZE_DIFFERS |
| R3 | avoc-daemon | 4103102 → 4225366 | OUTPUT_SIZE_DIFFERS |
| R3 | dali2-adaptor | 2121302 → 2160032 | OUTPUT_SIZE_DIFFERS |
| R3 | freetype2 | 285904 → 295236 | OUTPUT_SIZE_DIFFERS |
| R3 | openusd | 9185842 → 9136306 | OUTPUT_SIZE_DIFFERS |

### Doc 05 fallback shortlist

The ten below are ranked by the historical Doc 05 §1 LLVM `.text` values. This shortlist gives the review order if the matched Official ranking cannot finish. The native `abi.txt` can supersede it once its extraction and ownership gates pass.

| Package | Historical .text (KiB) |
| --- | ---: |
| vdsystem-lldb | 12,215 |
| tee_test_suite | 10,444 |
| spirv-tools | 4,742 |
| glslang | 2,837 |
| org.tizen.ssoservice | 2,797 |
| org.tizen.contents-recognition-service | 2,526 |
| libave | 2,372 |
| iotivity | 1,857 |
| securestorage | 1,851 |
| org.tizen.easysetup-daemon | 1,735 |

## Proposed Doc 03 §5 wording for Claude

| Item | Proposed status wording |
| --- | --- |
| Regular-LTO bitcode fallback | Landed in the pinned Official and Customized LLVM OBS source as Source1005. The scope is regular-LTO IR linked into PIC output. |
| Native FatLTO path | The GBS ARM fixture reproduced a native link that emitted a text relocation under permissive settings. GNU ld rejected that fixture with `-z text`. |
| Image baseline and package protection | Audit and strict-link trial scoped to matched Official QB 37736448 and GCC no-prelink reference QB 37564293. Report observed image owners and actual failing producer inputs when the native evidence returns. |
| CAPI and TLS archives | Exact-member GNU native and Gold-plugin coverage is the acceptance criterion. Report DSO/PIE outcome and runtime evidence by link route. |

## Report updates and review state

- **Doc 01** receives the matched image coverage and historical versus prospective R recipes. Include native capacity, exact source status and the delivery status in each row.
- **Doc 03** receives paired TEXTREL/TLS audit scope, GBS hardening results, producer repair candidates and T7 link map and runtime evidence. No rollout recommendation until the baseline exceptions are reviewed.
- **Doc 04** receives the seven A32 A/B/C/D comparisons, then up to five ranked shipped `-Og` packages. Compare the measured path set and use verified historical C only where its readback supports the row.
- **Doc 05** receives the four ABI verification rows, direct consumer scope, the next-ten proposal and the GCC/LLVM source status. Byte-identical output and heuristic LTO markers alone are insufficient for source or ABI acceptance.
- **Doc 07** receives the T1 A32/Thumb, `.text` and SHF_ALLOC deltas, the explicit ARM controls and the kernel exemption. KantSU2E stability and performance remain a subsequent board check.

Local checks used Python 3.10.12 with the absence of `_lzma` simulated, Bash syntax checks, byte-for-byte input hashes and a generated-driver fixture. The fixture exercised compile/link separation, live linker trace capture, a last-option override, missing DWARF and compressed evidence. Native P4, RPM, GBS and actual image extraction results remain to be collected. Claude review of this round’s new launchers is pending.
