# Round 0010e reply — exp8 reconciliation, compiler argv and retained RPMs

The 0010c hook transcript, 0010d inventory and original locators are archived with their matching SHA-256 values. The archived terminal transcript and the native file each have their own digest. Doc 02 and Doc 04 rev2 are separately checksummed. Monday steps 1–10 keep their order. [Hook evidence](../../artifacts/evidence/native-run-r0010c-hook-file-roster-20261120.txt) [Exp8 inventory](../../artifacts/evidence/native-run-r0010d-z901-exp8-inventory-20261120.txt) [Rev2 checks](../../reports/weekly/2026-11-20/SHA256SUMS.rev2) [Updated Step 8](0010c_reply.md)

## R1–R7 ledgers

Both are committed at `fb98eefaf6d924422466be70f4f95446583adeb1`.

| Ledger | SHA-256 | Scope |
|---|---|---|
| [Roster](../../artifacts/ledger/r1-r7-roster-20261111.tsv) | `f9af9ccbcb50ed1be5d355a7fa466d5939f71bccab175fcad3ee51554dfb85db` | 25 observed source-directory candidates with per-experiment participation. The historical 22-source membership and exact source pins remain open. Where shown, the RPM header identities are from the later November 17 image. |
| [Variants](../../artifacts/ledger/r1-r7-variants-20261111.tsv) | `6145591eb1830090aa5a51c182f64e9594429f603e656eb0cc9eea0b2203d73d` | 153 exp8 variants with timestamp, RPM count, experiment group, flag or direct-hook evidence and report link status. The 19 earlier exp variants stay in the original inventory as November 3–4 probes. |

The 153 exp8 directories split into 128 with RPMs and 25 without. The report states 151 builds, 126 successes and 25 failures. Five zero-RPM directories match explicit failures in the report (avoc-daemon thr50, thr25 and outliner, and dali2-adaptor lld and lldicf). For the other 20, zero RPMs only establishes that no artifact was found. `OK` in the ledger means an RPM is present. We need a run-result or RPM-to-log join to establish which two artifact-bearing directories fall outside the report and whether all 25 correspond to reported failures.

tvs-si is a documented R1 compatibility control and was also tested in R2. openusd and grpc `final` are R1 exemption checks, while both packages have measured rows in other experiments. They cannot account for two extra **source directories**. `exp/openusd` duplicates the source across the earlier experiment tree and `exp/remote-management` belongs to that earlier tree alone. The other exclusions from the 22-source cohort remain unidentified. All 153 variant rows reported a log, though some yielded no relevant flag tokens. [Report scope and counts](../../artifacts/historical-reports/optimization-analysis-part-02.md#method-and-conditions) [R1 controls](../../artifacts/historical-reports/optimization-analysis-part-01.md#closing-the-gap-and-verification)

## AVControl and tv-viewer compile commands

| Verbose variant | Inventory hits for `-mthumb` | Inventory hits for `-fstack-protector-strong` |
|---|---:|---:|
| AVControl | 12 | 54 |
| tv-viewer | 20 | 838 |
| dali2-adaptor | 956 | 0 captured |
| protobuf | 894 | 0 captured |

The inventory merges two logs and counts token occurrences, including shell traces and repeated argv. The AVControl and tv-viewer imbalance makes dropped Thumb flags a plausible explanation. The counts cannot establish how many compile commands carried each mode or optimization level, or identify the variable that replaced the flags. The four verbose logs remain on the native server. The launcher below prints deduplicated actual driver invocations by `-marm`/`-mthumb`/unspecified and final `-O`, a sample for each observed group, and flagged references to CMake/Make flags. Response-file cases stay open. Use the emitted source/command evidence to prove a particular flag replacement before updating Doc 07.

## Recipe evidence for Step 8

| Recipe | Archived treatment evidence | Status |
|---|---|---|
| [R1](../../artifacts/ledger/r1-r7-recipes/R1.json) | Verified `CCC_OVERRIDE_OPTIONS` for `final2`. | Use the pinned `HOOK_FILE` in lane C. |
| [R2](../../artifacts/ledger/r1-r7-recipes/R2.json) | `-fvisibility-inlines-hidden` in `vih/vihL/vihO`. | Exact injection remains open. Preserve the distinct optflags route identified for grpc/protobuf and documented exclusions. |
| [R3](../../artifacts/ledger/r1-r7-recipes/R3.json) | `-flto=thin` in five `thin` variants. | Verify which command and flag position replaced full LTO at compile and link. |
| [R4-50](../../artifacts/ledger/r1-r7-recipes/R4-50.json) / [R4-25](../../artifacts/ledger/r1-r7-recipes/R4-25.json) | `inline-threshold=50` or `=25` in each respective log group. | Verify the compiler and plugin argument sequence separately. The report documents a delivery failure in avoc-daemon. |
| [R5](../../artifacts/ledger/r1-r7-recipes/R5.json) | `enable-machine-outliner` in the `outliner` group. | Verify the complete compile and link arguments and package eligibility. |
| [R6-lld](../../artifacts/ledger/r1-r7-recipes/R6-lld.json) / [R6-icf](../../artifacts/ledger/r1-r7-recipes/R6-icf.json) | `-fuse-ld=lld`, with `--icf=safe` in `lldicf`. | Establish the lld-only command and provider. The ICF comparison uses the verified lld lane as its baseline. |
| R7 | No exp8 variant. The report's 18.83 MB is calculated from relocation encodings. | Requires separate loader and packaging validation. |

The JSON records each package set and the observed tokens. When the original injection route or exact option strings are missing, `baseline` and `treatment` are deliberately unset. Launcher 8 must wait for that evidence and its reviewed roster before running those recipes. The separate `treatments` readback prints original lines and their context, rather than turning aggregate token counts into executable options.

## Native readback for verbose logs, WARN/FINAL and per-variant sizes

After review, use this one launcher with `EXP8_MODE=verbose` (default) first, then `treatments`, `pairs`, or `sizes`. `pairs` compares AVControl and libpisa-ipc `forceL` against `final2` at each matched ELF path. It reports both `.text` SHA-256 and full ELF SHA-256 and checks the RPM-owner/source and ELF sets. Doc 04 rows 2–3 stay labeled WARN history until this result. Matching pairs would support using the figures as historical proxies for C. A measured FINAL rebuild is the direct check for tv-viewer and webappservice.

`sizes` also sums `.text` and SHF_ALLOC bytes per retained ARM payload variant. Those totals cover the retained release RPMs and include alloc sections such as NOBITS. The original report numbers require its exact image file list and byte units. The readback flags errors and missing coverage and keeps the raw path-level details for the selected pair. No compile or installation.

Run on the native server. Logs and pair mode should take minutes, using one process and little scratch space. Run the optional full size sweep after other heavy jobs because it may decompress hundreds of local RPMs serially. Budget 10–30 minutes depending on disk throughput. GitHub traffic is limited to the pinned downloads. Each call prints at most 142 report lines plus download checks. For more use `EXP8_REPORT` and increment `EXP8_PAGE` through `LAST_PAGE`. Native output stays under `workspace/temp/pm0010e-exp8.*`.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010e-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75'
  get 'fb98eefaf6d924422466be70f4f95446583adeb1' 'artifacts/scripts/r0010e/exp8-readback.py.txt' 'feeff8d1e1521a70b17a05ce85a1e2fa42cefd31f37777064ac59864cd46f96d'
  get 'fb98eefaf6d924422466be70f4f95446583adeb1' 'artifacts/ledger/r1-r7-variants-20261111.tsv' '6145591eb1830090aa5a51c182f64e9594429f603e656eb0cc9eea0b2203d73d'
  if [[ -n "${EXP8_REPORT:-}" ]]; then
    python3 -B "$d/exp8-readback.py.txt" --page "$EXP8_REPORT" "${EXP8_PAGE:-0}"
  else
    python3 -B -u "$d/exp8-readback.py.txt" --mode "${EXP8_MODE:-verbose}" \
      --scan "$d/image_mode_scan.py.txt" --ledger "$d/r1-r7-variants-20261111.tsv"
  fi
)
```

The Python 3.10 checks covered command extraction, rejection of shell echoes and driver queries, the 153-row ledger and the four-lane readback. Live compiler argv, exact recipes, WARN/FINAL code identity and the historical sample membership remain open. Preserve `z901/exp*/` and `gbs-root*/local/repos/*/armv7l/logs/` in any cleanup.
