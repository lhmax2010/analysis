# Round 0011c (rev2, with download retry; this is the version that ran as pm0011c-chain.AFkXQV) — background chain on the Native Server (Codex's pinned 0011 commands, unchanged, run in order):
#   1 GCC reference capture (QB 37564293, DO_NOT_DELETE)       5–60 min
#   2 Step 3 PERF_ACTION=usb-both (Official, then Customized)   5–30 min per lane
#   3 MLGO Base proof (Official vs Customized)                  10–35 min
# One log per job + status.txt; a failed job does not stop the next. Readback block at the bottom.
cd /home1/chengkai/vd-tree
W=$(mktemp -d "$PWD/workspace/temp/pm0011c-chain.XXXXXX")
cat > "$W/run.sh" <<'EOS'
set -u
W=$1; cd /home1/chengkai/vd-tree; export TMPDIR="$W"
export OFFICIAL_CAPTURE=/home1/chengkai/vd-tree/workspace/qb-evidence/37736448-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2
export CUSTOM_CAPTURE=/home1/chengkai/vd-tree/workspace/qb-evidence/37736427-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.1
get() {
  local rev=$1 path=$2 sum=$3 file="$W/${2##*/}" i
  for i in 1 2 3 4 5; do
    if curl -fsS --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file" &&
       printf '%s  %s\n' "$sum" "$file" | sha256sum -c - >> "$W/downloads.txt" 2>&1; then return 0; fi
    echo "RETRY $i ${path##*/} $(date -Is)" >> "$W/downloads.txt"; sleep 10
  done
  return 1
}
ok=1
get 'aaa44c847bfc6b5313de6fd579be853d01d6f684' 'artifacts/scripts/r0011/qb-retain.py.txt' '437135b56bc69c64571c906fe704a74c761f5d3414f5010122ed79cd31b5dc91' || ok=0
get 'd3cea65aac76d438b82b55a2857a5ee18546edad' 'artifacts/scripts/r0005/image-repo-lib.py.txt' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f' || ok=0
get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b' || ok=0
get 'cfde38f9e4c6041069d28adc8b9da35894df0de9' 'artifacts/scripts/r0010b/mlgo-base-proof.py.txt' '7254ef3de2d606826718338eb69e30253f34f36fef5dd8fb683897044fe6b9f1' || ok=0
[ "$ok" = 1 ] || { echo "DOWNLOAD_FAILED $(date -Is)" >> "$W/status.txt"; exit 1; }
job() {
  local n=$1; shift
  echo "JOB $n START $(date -Is)" >> "$W/status.txt"
  ( "$@" ) > "$W/$n.txt" 2>&1; local rc=$?
  echo "JOB $n END rc=$rc $(date -Is) lines=$(wc -l < "$W/$n.txt")" >> "$W/status.txt"
}
job 1-gcc-reference python3 -B -u "$W/qb-retain.py.txt" "$W/image-repo-lib.py.txt" reference 37564293 \
  'http://repos.vd.sec.samsung.net/products/tv/development/DO_NOT_DELETE/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261113.1/'
job 2a-usb-official python3 -B -u "$W/perf-bundle.py.txt" "$OFFICIAL_CAPTURE"
job 2b-usb-custom   python3 -B -u "$W/perf-bundle.py.txt" "$CUSTOM_CAPTURE"
job 3-mlgo-base-proof python3 -B -u "$W/mlgo-base-proof.py.txt" --perf "$W/perf-bundle.py.txt" \
  --repo "$W/image-repo-lib.py.txt" --official "$OFFICIAL_CAPTURE" --custom "$CUSTOM_CAPTURE"
echo "DONE $(date -Is)" >> "$W/status.txt"
EOS
nohup setsid bash "$W/run.sh" "$W" > "$W/nohup.log" 2>&1 < /dev/null &
echo "CHAIN_DIR $W"

# ---------------- readback (any time; final when status shows DONE) ----------------
# cd /home1/chengkai/vd-tree; W=$(ls -d workspace/temp/pm0011c-chain.* | tail -1)
# { echo "CHAIN_DIR $W"; cat "$W/status.txt" "$W/downloads.txt"; for f in "$W"/[1-3]*-*.txt; do echo "===== ${f##*/}"; cat "$f"; done; } > "$W/combined.txt"
# cat "$W/status.txt"; wc -l "$W/combined.txt"; sha256sum "$W/combined.txt"
