```diff
-read -r -p 'Paste STATIC_GATE PASS RECEIPT <path> <sha>: ' tag gate label PM_STATIC PM_STATIC_SHA
-[[ $tag == STATIC_GATE && $label == RECEIPT && $gate == PASS ]]
+read -r -p 'Paste STATIC_GATE PASS or PM_OVERRIDE HOLD followed by RECEIPT <path> <sha>: ' tag gate label PM_STATIC PM_STATIC_SHA
+[[ $label == RECEIPT ]]
+case "$tag/$gate" in STATIC_GATE/PASS|PM_OVERRIDE/HOLD) ;; *) exit 2 ;; esac
+export PM_AUTH="$tag"
```

### TEST-ONLY Official GBS verification and test shelf

Native host, after Claude review. Run in a foreground terminal. Use `build` first and `shelve` after BUILD_RECEIPT PASS. The builder also verifies the PM decision bytes, the exact HOLD path and digest, and the operation. The shelf requires the build receipt from the same builder and same spec. Board-flash receipt status is **HOLD** for S1, S2, S11 and S12. Neither operation writes to a TV. The earlier K1/K3 perf ELF measurements stand.

```bash
(
set -eu
t=/home1/chengkai/vd-tree/workspace/temp
p=9e8886d877244b9a75d16f6fa1a8f3fae734c600
d=$(mktemp -d "$t/pm0013m-launch.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0013jk/run.sh.txt" -o "$d/run"
printf '%s  %s\n' eab44a8bada480181c2dbfda067e21f8ead269fa76c0ccbbc423a39a314e5b67 "$d/run" | sha256sum -c -
read -r -p 'Operation (build or shelve): ' action
case "$action" in build|shelve) ;; *) exit 2 ;; esac
bash "$d/run" "$p" "$action"
)
```

At the receipt prompt paste this exact line.

```text
PM_OVERRIDE HOLD RECEIPT /home1/chengkai/vd-tree/workspace/temp/pm0013jk-static.mo1VRK/effects.json ef577b30f542286ccfe09a4297f186bc3e1c76262a03bd23ecad5e96a919563b
```

Build resource gate is 105 GiB disk, 32 GiB RAM and six cores. Estimate 30–90 minutes and repo downloads. The shelf takes seconds and writes one pending TEST-ONLY CL after the operator confirms. Submit the two test QBs only after the clean build, GCC SERET-UL check and verified shelf.

The 0013n shelf policy adds a diff review before opening the CL. This pin prints the depot and preceding-shelf diffs and their SHA-256s. A clean build receipt from the urgent 8add84d override remains eligible for this scope. Verify the shelved bytes in local GBS and both test QBs before an on-board trial.

### Retained kernel static follow-up

```bash
(
set -eu -o pipefail
p=9e8886d877244b9a75d16f6fa1a8f3fae734c600
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013m-launch.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0013jk/run.sh.txt" -o "$d/run"
printf '%s  %s\n' eab44a8bada480181c2dbfda067e21f8ead269fa76c0ccbbc423a39a314e5b67 "$d/run" | sha256sum -c -
bash "$d/run" "$p" static | tee "$d/combined.txt"
)
```

Native host, idle priority, one worker, read-only retained inputs, workspace output. No GBS or build lock. Estimate 30–150 minutes plus ELF scans and several GiB of scratch. Return the STACK_SITE, S1–S15, STATIC_GATE, BOARD_FLASH and TABLES lines. Keep both K1 and K3.

| Check | Verified in mo1VRK | Follow-up evidence |
|---|---|---|
| S1 | Direct critical section hits 0/0. The direct graph nevertheless reaches 3,466/4,602 helpers from critical roots. 616/664 counts **distinct reachable functions** with an unresolved indirect control transfer. Each function counts once even if it contains several such instructions. | Shortest observed direct symbol paths, each flagged indirect PC and operand, and verified linker-map attribution where available. Reachability through conditional branches is a potential call path; static edges do not identify the runtime IRQ state. |
| S2 | 5/8 LR stack sites match the reachability or IRQ/entry name test; lower bound 8 B in each lane. | Prints each site address, caller, section, input object and context. Full root-to-caller chain in critical-stack.tsv. No names or actual execution context were returned in mo1VRK. |
| S4 | Matched table counts in each pair and zero destinations inside helpers. K1 has 210 and K3 215 references outside a sized function symbol. | Verify each destination is in exactly one allocated executable section under the uniquely decoded table encoding. Save exact symbols and section for each unsized PC. Assembly origin needs symbol/source evidence. |
| S7/S9 | Export names match (10,348); zero long-branch thunks. | Compare Module.symvers by symbol and CRC on matched output trees. Missing files leave CRC comparison open. |
| S11 | 119/165 sensitive instructions; 14 incomplete helper decodes per lane. | Emit helper, PC, operand, caller set and disposition. Only matching CP15 TPIDR read forms are auto-classified. Retry missing A32 words with a second decoder under mapping-symbol proof. Preserve data/mode ambiguity and all writes or other state changes for owner review. |
| S12 | 0/115 comparable modules in both treatments. | Look in trees sharing the full perf ELF digest, their module orders, matching RPM rows, and record unjoined staging candidates. Compare size, helpers, relocation kinds and PLT. Unmatched flavour or incomplete roster holds this check. |
| S13 | Zero helper entries resolve to both function and source line in each lane. | Known debug cost. Retain the build ID and symbolize the caller return address and call site. Runtime frame-walk verification remains open. |

### Image census and loader follow-up

```bash
(
set -eu -o pipefail
p=9e8886d877244b9a75d16f6fa1a8f3fae734c600
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013m-launch.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0013l/run.sh.txt" -o "$d/run"
printf '%s  %s\n' 94cb68f745deb95297017fd58ae66c33e2c4ebc653aad79a683c415d7e565ff3 "$d/run" | sha256sum -c -
bash "$d/run" "$p" static | tee "$d/combined.txt"
)
```

Native host after review, idle I/O, no GBS, sudo or build lock. Budget hours and repository bandwidth for published ELF/file lists, temporary space for one verified RPM at a time per pass and sparse data.img expansion if needed. Outputs remain under the printed workspace. Send the compact console result. The original gBXGor archive remains usable.

- Official 37736448 → 37777148 is **rebuilt, same measured sizes**. Both partition hashes changed. 447 regular-file/symlink records changed on platform, 2 on prd, with zero additions/removals. This establishes different published contents. Equal ELF counts and executable sizes do not identify which build action produced those differences.
- The old code replaced the output roster list with a Path. The revised code keeps them separate. A section-table offset outside the ELF payload now yields an unsupported record and allows E1 to continue; these rows count as coverage gaps.
- Inspect the guest RPM DB symlink and read the DB from data.img if a supported ext filesystem is available. When unavailable, record the image format and join checksum-verified published file lists to O1 roster names and current ELF or enclosing-container digests. O1 is the older image. A matching name alone cannot establish current ownership. G1 has a separate roster. C7/C8 can consume the resulting owners; unknowns remain explicit.
- The target loader provider remains unproved until a published glibc payload matches. loader-providers.tsv contains NEVRA, published RPM digest, both file digests, section differences and O1 roster match. Report its GLIBC_ABI_DT_RELR version node separately from the eight-word relocation fixture result.
- AVControl T4 passed on baseline/default. Package REVIEW means the defined exports or selected dynamic tags differed from Official. The original transcript omits the specific symbol/tag. T4_DIFF_package and pilot-followup.json return the difference. Pilot status stays size-qualified.
- No pm0013-pkg directory existed at capture. The operator reported starting the worker afterwards; its status and measurements need a run receipt.

Local validation used Python 3.10.12, a truncated ELF with the reported 161,016-byte length and out-of-range offset, the earlier ARM interworking fixture, launcher hash checks, and positive/negative override scope tests. Native data-dependent verdicts await the operator return. [Raw evidence](../../artifacts/evidence/native-run-r0013jk-static-mo1VRK-r0013l-gBXGor-20261126.txt)
