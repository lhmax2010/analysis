# Round 0011a reply — Approved order and overnight HQ comparison

Claude accepted `aaa44c8` and `8688058`. The previous capture and Step 2 pins stand. The revised HQ scanner and overnight wrapper are pinned to `a134afbc404508dfc32e479a2c88dd4a850f4c62` and ready for Claude review. [Recorded review](../claude_to_codex/0011a_review.md) [Capture, gate and board commands](0011_reply.md)

1. Let Official `37736448` and Customized `37736427` finish in sequence. The Official capture was reported in progress at 15:09 CST.
2. Run the read-only shelf/Base-list locator in parallel.
3. After both captures, return `QB_PAIR_CONFIG_GATE_PASS` and the Product VCS result. Keep unresolved or differing rows for review.
4. Capture GCC reference `37564293` after the shared locks are free.
5. Stage both USB directories with `PERF_ACTION=usb-both`, run the board A/B, then run the MLGO Base proof. Keep the attribution as Base swap pending the proof.
6. After USB staging, run the HQ batch overnight. Use a heavy-job slot after the Base proof releases the shared locks if the proof is running.
7. Run four-lane Step 8 after the HQ scans exit. Use the new `OFFICIAL_CAPTURE` and revalidate the installed replay roster. A CPU limit alone cannot isolate disk I/O and the shared lock. [Step 8](0010c_reply.md)

## Overnight HQ comparison

Run once on the native server with `GCC_CAPTURE` and `OFFICIAL_CAPTURE` set to the completed capture paths. The wrapper runs GCC, LLVM and compare in one background job. It stops on a failed stage and writes `status.txt`, three stage logs for a complete run, and one bounded `combined.txt`. Each scan typically takes 20–90 minutes. Budget one local archive reader, the expanded partition space and the 50 GiB reserve. The join takes seconds. Network use is limited to pinned GitHub downloads during setup. After `DONE`, return the combined output. All batch output stays under `workspace/temp/pm0011a-hq-batch.*`.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0011a-hq-batch.XXXXXX")
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
  get 'a134afbc404508dfc32e479a2c88dd4a850f4c62' 'artifacts/scripts/r0011/hq-elf-rebaseline.py.txt' '55ea44b32389fe60137e5d06e314def73d695f7b86e879d707ed7533afbc6120'
  if [[ -n "${HQ_REPORT:-}" ]]; then
    args=()
    if [[ -n "${HQ_CONTAINS:-}" ]]; then args+=(--contains "$HQ_CONTAINS"); fi
    python3 -B "$d/hq-elf-rebaseline.py.txt" page "$HQ_REPORT" "${HQ_PAGE:-0}" "${args[@]}"
    exit 0
  fi
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-relocations.py.txt' 'f678d0f9c479d6a183c3f83d7a14917ea46c15533f41d97a3baeb732b6905cf7'
  get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75'
  get 'a134afbc404508dfc32e479a2c88dd4a850f4c62' 'artifacts/scripts/r0011a/hq-overnight.sh.txt' '5f287377758b319572bb30e40914067e796546b0b250da401fc119ea908cf723'
  nohup setsid bash "$d/hq-overnight.sh.txt" "$d" "${GCC_CAPTURE:?}" "${OFFICIAL_CAPTURE:?}" \
    >"$d/nohup.log" 2>&1 </dev/null &
  printf 'HQ_BATCH_DIR %s PID %s\n' "$d" "$!"
)
```

Read progress or return the final combined file using the printed `HQ_BATCH_DIR`.

```bash
case "$HQ_BATCH_DIR" in
  /home1/chengkai/vd-tree/workspace/temp/pm0011a-hq-batch.*)
    if [[ -f "$HQ_BATCH_DIR/combined.txt" ]]; then
      sha256sum "$HQ_BATCH_DIR/combined.txt"
      cat "$HQ_BATCH_DIR/combined.txt"
    else
      awk 'NR<=40' "$HQ_BATCH_DIR/status.txt"
    fi
    ;;
  *) printf 'Invalid HQ_BATCH_DIR\n' >&2 ;;
esac
```

### Output rules

- Every TSV keeps integer byte measures. `summary.json` and `HQ_JOIN_RESULT` include bytes and their exact division by 1,024 for display in KiB. Use that value for Doc 04 and Doc 06 KB labels and divide by 1,024 again for Doc 07 MiB.
- `packages.tsv` uses `MATCHED`, `SOURCE_DIFFERS` and `UNPROVED`. The matching rule requires the same source version and pinned VCS on both sides. Without a matching pin, even equal NEVRA and SRPM leave source identity unproved. Matched totals also require the same owned ELF path and architecture set. Raw measures remain visible for other rows. GCC 10.1 versus LLVM 10.0 and the ten-day Product gap remain report confounders.
- The automatic Doc 05 shortlist requires positive GCC FILE-symbol evidence and an LLVM static symbol table with a project FILE entry on a matched path. Stripped or FILE-symbol-missing pairs go to `lto-unverifiable.tsv` and its separate count. Actual build-log proof from the same LLVM publication may qualify a row for manual review. The scanner does not infer missing `-flto` from a stripped binary and does not promote candidates to confirmed faults.
- `HQ_PRELINK_MARKED` reports a count for each image, including zero. Any nonzero result retains `prelink-marked.tsv` with owned or unresolved ELF paths and shows the first 20. A zero covers only files parsed at the recorded coverage. For additional pages rerun the launcher with `HQ_REPORT` pointing to the TSV and set `HQ_PAGE` to the page number.

## Weekend follow-up pages

The 517-line combined transcript has yet to arrive in the local workspace. The pager below verifies the native combined file and fills in the exact `REPORT` path from its receipt. Run it separately with `EXP8_PAGE_MODE=verbose`, `treatments` and `sizes`. Start at `EXP8_PAGE=1` and continue through each result's `LAST_PAGE`. It takes seconds, reads local files after the pinned download, and prints fewer than 150 lines per call. No exp8 jobs are rerun.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0011a-weekend-tools.XXXXXX")
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
  combined="$PWD/workspace/temp/pm0010w-weekend.BcoAvm/combined.txt"
  printf '%s  %s\n' ea30ccdbe37e7c10ed4e33e69a6cebed6e2a60d1b273e5734bee87c0fea73b2a "$combined" | sha256sum -c -
  case "${EXP8_PAGE_MODE:?set verbose, treatments or sizes}" in
    verbose) tag=VERBOSE ;;
    treatments) tag=TREATMENT ;;
    sizes) tag=VARIANT_SIZE ;;
    *) exit 2 ;;
  esac
  matches=()
  while read -r _ candidate digest; do
    [[ "$candidate" == "$PWD"/workspace/temp/pm0010e-exp8.*/result.txt && -f "$candidate" && ! -L "$candidate" ]] || continue
    [[ "$digest" =~ ^[0-9a-f]{64}$ ]] || continue
    if grep -m1 -q "^$tag " "$candidate"; then
      printf '%s  %s\n' "$digest" "$candidate" | sha256sum -c -
      matches+=("$candidate")
    fi
  done < <(awk '$1=="REPORT" && NF==3 {print}' "$combined" | sort -u)
  if ((${#matches[@]} != 1)); then
    printf 'Expected one %s report, found %s\n' "$tag" "${#matches[@]}"
    awk '/^(REPORT |PAGE )/ {if (++n<=60) print}' "$combined"
    exit 2
  fi
  EXP8_REPORT=${matches[0]}
  python3 -B "$d/exp8-readback.py.txt" --page "$EXP8_REPORT" "${EXP8_PAGE:-1}"
)
```

| Return | Evidence needed for the next update |
|---|---|
| Verbose | Doc 07 compile groups and the flag variable's actual file and line |
| Pairs | Doc 04 rows 2–3 disposition from complete AVControl and libpisa-ipc WARN/FINAL pairs |
| Treatments | R2–R6 original injection commands and exact values wherever proved |
| A32 | Doc 07 exact path, estimate basis and per-file values |
| Kernel ISA | EXP-T1 kernel exemption based on the verified PERF config and kernel argv |

Local checks passed for source-status classification, exact KiB conversion, stripped-row exclusion, unknown GCC FILE symbols, and the wrapper's serial success path and bounded combined output. Native captures and measurements remain pending.
