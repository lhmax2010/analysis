# Round 0011 — capture the two new matched MLGO QBs (Monday step 1), in the background, one after another.
# Order: Official MLGO (qb37736448) → Customized MLGO (qb37736427). The GCC no-prelink image (qb37564293) is under
# DO_NOT_DELETE and does not expire; qb-retain only accepts PRV build URLs, so Codex extends it in round 0011.
# Uses Codex's pinned qb-retain launcher (r0007 @adb0ba7). Each capture writes its own log; one failure does not stop the next.
cd /home1/chengkai/vd-tree
W=$(mktemp -d "$PWD/workspace/temp/pm0011-capture.XXXXXX")
cat > "$W/run.sh" <<'EOS'
set -u
W=$1; cd /home1/chengkai/vd-tree; export TMPDIR="$W"
get() {
  local rev=$1 path=$2 sum=$3 file="$W/${2##*/}"
  curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file" &&
  printf '%s  %s\n' "$sum" "$file" | sha256sum -c - >> "$W/downloads.txt" 2>&1
}
get 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' 'artifacts/scripts/r0007/qb-retain.py.txt' 'a2f8e7ef82b1c330e1d50239f07e3454c2440d1dff8d2773d950fddaf488c2fe' &&
get 'd3cea65aac76d438b82b55a2857a5ee18546edad' 'artifacts/scripts/r0005/image-repo-lib.py.txt' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f' ||
  { echo "DOWNLOAD_FAILED $(date -Is)" >> "$W/status.txt"; exit 1; }
cap() {  # name id product_url
  echo "CAP $1 START $(date -Is)" >> "$W/status.txt"
  python3 -B -u "$W/qb-retain.py.txt" "$W/image-repo-lib.py.txt" capture "$2" "$3" > "$W/$1.txt" 2>&1; local rc=$?
  echo "CAP $1 END rc=$rc $(date -Is) $(grep -m1 -o 'CAPTURE_DIR [^ ]*' "$W/$1.txt") $(grep -c CAPTURE_COMPLETE "$W/$1.txt") complete" >> "$W/status.txt"
}
cap 1-official-qb37736448   37736448 'http://repos.vd.sec.samsung.net/priv/168.219.246.226:81/PRV/builds/b776/19414776/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2/'
cap 2-custom-qb37736427     37736427 'http://repos.vd.sec.samsung.net/priv/168.219.236.27:81/PRV/builds/b755/19414755/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.1/'
echo "DONE $(date -Is)" >> "$W/status.txt"
EOS
nohup setsid bash "$W/run.sh" "$W" > "$W/nohup.log" 2>&1 < /dev/null &
echo "CAPTURE_RUN_DIR $W  PID $!"

# ---------------- readback (run any time; final when status shows DONE) ----------------
# cd /home1/chengkai/vd-tree; W=$(ls -d workspace/temp/pm0011-capture.* | tail -1)
# { echo "RUN_DIR $W"; cat "$W/status.txt" "$W/downloads.txt"; for f in "$W"/[1-2]-*.txt; do echo "===== ${f##*/}"; cat "$f"; done; } > "$W/combined.txt"
# cat "$W/status.txt"; wc -l "$W/combined.txt"; sha256sum "$W/combined.txt"
