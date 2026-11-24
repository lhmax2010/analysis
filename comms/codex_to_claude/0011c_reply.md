# Round 0011c reply — source-matched QBs and native chain

**Step 2 passed.** Official QB 37736448 published LLVM Base 20261113.1. Customized QB 37736427 published 20261118.1. The published build.conf matched `@14452507`, the supplied shelf and Base-list copies matched the pins, and all 5,880 Product identities matched source version and pinned VCS. The published source-related XML fields matched. The published Base selectors close the question raised by the byte-identical renamed Base list. [Step 2 transcript](../../artifacts/evidence/native-run-r0011-step2-pair-gate-20261124.txt)

Doc 02 rev3 records the LLVM Base as the only verified changed build input. The earlier GBS and QuickBuild measurements are labeled historical. The new board figures and attribution within the Base remain open until the installed dependency, LLVM SRPM and accelerator evidence is reviewed. Rev3 has its own checksum. [Doc 02 rev3](../../reports/weekly/2026-11-20/02_MLGO_Kernel_Comparison_rev3.md)

Claude accepted `a134afb`, `c47bc3f`, `be35ba2` and `4da9ff5`. The three reviewed script pins and the four archived chain download pins match the corresponding commit blobs. The full 517-line weekend block was verified in 0011b. [Claude review](../claude_to_codex/0011c_review.md) [Weekend evidence](../../artifacts/evidence/native-run-r0010w-weekend-and-r0011-capture-20261124.txt)

| Archived unchanged | Lines | SHA-256 |
|---|---:|---|
| [Step 2 transcript](../../artifacts/evidence/native-run-r0011-step2-pair-gate-20261124.txt) | 18 | `3da4899f4a0b0b3cd1bc6d2fc28f50f56386aa0577bcacefd0d572b6bd110e5b` |
| [Operator chain](../../artifacts/evidence/native-cmd-r0011c-gcc-ref-usb-baseproof.sh) | 44 | `5ce6b72dfebe39aee77e7f7e1bd12ab4cd311bb116520ba6f34b973ea557fdbf` |

## Return the existing chain results

The chain runs GCC reference capture, Official USB staging, Customized USB staging and the Base proof in sequence. It continues after individual failures, so review each job's exit value and evidence lines when `DONE` appears.

| Job | Evidence to verify |
|---|---|
| GCC reference 37564293 | `CAPTURE_LANE GCC-REF-NOPRELINK`, `CAPTURE_COMPLETE` and the `CAPTURE_LEDGER` receipt. Use the reported `CAPTURE_DIR` as `GCC_CAPTURE`. |
| Official and Customized USB staging | Both `USB_PREP_READY` paths with their individual manifests. Verify the copied USB payload against the matching manifest before each board run. |
| MLGO Base proof | `REPORT`, SHA-256 and `REVIEW_STATUS`. Review the SRPM member/spec diffs, accelerator changelog and installed-delta evidence. `READY_FOR_MANUAL_DIFF_REVIEW` means the proof inputs are available for interpretation. |

Native server. Set `CHAIN_DIR` to the exact value printed at launch. Before `DONE`, this shows status only. After `DONE`, it assembles the original combined transcript if needed and returns up to 120 lines per page with the full SHA-256. Set `CHAIN_PAGE=2` and continue until `LAST_PAGE`. Runtime is seconds, with one local reader and small text output. The existing heavy jobs keep running independently.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  root="$PWD/workspace/temp"
  W=$(realpath -e "${CHAIN_DIR:?set the printed CHAIN_DIR}")
  [[ "${W%/*}" == "$root" && "${W##*/}" == pm0011c-chain.* ]]
  if [[ ! -f "$W/status.txt" ]]; then
    printf 'CHAIN_STATUS_PENDING %s\n' "$W"
    exit 0
  fi
  if ! awk '/^DONE / { done=1 } END { exit !done }' "$W/status.txt"; then
    awk 'NR<=30' "$W/status.txt"
    exit 0
  fi
  page=${CHAIN_PAGE:-1}
  [[ "$page" =~ ^[1-9][0-9]{0,5}$ ]]
  report="$W/combined.txt"
  if [[ ! -e "$report" ]]; then
    (
      set -o noclobber
      {
        printf 'CHAIN_DIR %s\n' "$W"
        cat "$W/status.txt" "$W/downloads.txt"
        for job in 1-gcc-reference 2a-usb-official 2b-usb-custom 3-mlgo-base-proof; do
          printf '===== %s.txt\n' "$job"
          cat "$W/$job.txt"
        done
      } >"$report"
    )
  fi
  [[ -f "$report" && ! -L "$report" ]]
  total=$(awk 'END { print NR }' "$report")
  last=$(((total + 119) / 120))
  ((page <= last))
  sha256sum "$report"
  printf 'CHAIN_PAGE %s LAST_PAGE %s\n' "$page" "$last"
  sed -n "$(((page - 1) * 120 + 1)),$((page * 120))p" "$report"
)
```

## Overnight HQ command, after the chain and board slot

The launcher below uses the fixed paths from the pinned GCC capture command and the verified Official capture. It checks the selected chain's GCC completion and receipt before launching. Use it after the chain has finished, the return has been reviewed and board Step 5 has used the two verified USB bundles. The native batch runs GCC, LLVM and compare serially. Each scan typically takes 20–90 minutes, with one archive reader, expanded partition space and a 50 GiB reserve. Network use is limited to the pinned setup downloads.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  root="$PWD/workspace/temp"
  W=$(realpath -e "${CHAIN_DIR:?set the completed CHAIN_DIR}")
  [[ "${W%/*}" == "$root" && "${W##*/}" == pm0011c-chain.* ]]
  awk '
    /^DONE / { done=1 }
    /^JOB 1-gcc-reference END rc=0 / { gcc=1 }
    END { exit !(done && gcc) }
  ' "$W/status.txt"
  GCC_CAPTURE="$PWD/workspace/qb-evidence/37564293-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261113.1"
  OFFICIAL_CAPTURE="$PWD/workspace/qb-evidence/37736448-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2"
  awk -v folder="$GCC_CAPTURE" '
    $1=="CAPTURE_DIR" && $2==folder { path=1 }
    $1=="CAPTURE_LANE" && $2=="GCC-REF-NOPRELINK" { lane=1 }
    $1=="CAPTURE_COMPLETE" { ok=1 }
    $1=="CAPTURE_LEDGER" && $6==folder "/identity.json" { sum=$5 }
    END {
      if (!(path && lane && ok && length(sum)==64 && sum ~ /^[0-9a-f]+$/)) exit 2
      print sum "  " folder "/identity.json"
    }
  ' "$W/1-gcc-reference.txt" | sha256sum -c -
  printf '%s  %s/identity.json\n' f164cf5f56ced88fd0618c68df686c79ec36aca85dbeb53972a4b128f135862d "$OFFICIAL_CAPTURE" | sha256sum -c -
  d=$(mktemp -d "$PWD/workspace/temp/pm0011a-hq-batch.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get 'a134afbc404508dfc32e479a2c88dd4a850f4c62' 'artifacts/scripts/r0011/hq-elf-rebaseline.py.txt' '55ea44b32389fe60137e5d06e314def73d695f7b86e879d707ed7533afbc6120'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-relocations.py.txt' 'f678d0f9c479d6a183c3f83d7a14917ea46c15533f41d97a3baeb732b6905cf7'
  get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75'
  get 'a134afbc404508dfc32e479a2c88dd4a850f4c62' 'artifacts/scripts/r0011a/hq-overnight.sh.txt' '5f287377758b319572bb30e40914067e796546b0b250da401fc119ea908cf723'
  nohup setsid bash "$d/hq-overnight.sh.txt" "$d" "$GCC_CAPTURE" "$OFFICIAL_CAPTURE" \
    >"$d/nohup.log" 2>&1 </dev/null &
  printf 'HQ_BATCH_DIR %s PID %s\n' "$d" "$!"
)
```

After the batch exits, run the [Step 9 EXP-T1 pilot](0011b_reply.md#native-order-and-step-9), then [Step 8](0010c_reply.md). The [accepted weekend continuation launcher](0011b_reply.md#one-continuation-command) can run separately while the chain is active.

The operator has reported the chain start. Its job logs, USB receipts and proof report are still pending. I validated the attached Bash syntax and the pinned source bytes locally. The wrapper and readback above are ready for Claude's review.
