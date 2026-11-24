# Round 0011f rev2 — board-free batch for the Native Server. Step 5 staging failed (bench.c not in %build; Codex fixes it),
# so this version does not wait for BOARD_TOOLS; it only refuses to start while another GBS build or heavy scan is running.
# Uses Codex's pinned launchers unchanged (0011e / 0011b / 0011a), serially, one log per job, in the background:
#   1 qb-platform   2 qb-kernel   3 qb-srpm                          (matched-qb @30d0d29)   seconds–minutes each
#   4 wk-pages      5 wk-kernel-config   6 wk-tv-viewer   7 wk-delivery (weekend-readback @be35ba2)  delivery 10–30 min
#   8 hq-overnight  (GCC 37564293 scan → LLVM 37736448 scan → compare, hq-overnight @a134afb)        20–90 min per image
# Usage:  paste this whole file.
cd /home1/chengkai/vd-tree
busy=$(pgrep -af 'gbs build|hq-elf-rebaseline|perf-bundle|qb-retain|gbs-board-bench' | grep -v pgrep)
if [ -z "$busy" ]; then
W=$(mktemp -d "$PWD/workspace/temp/pm0011f-batch.XXXXXX")
cat > "$W/run.sh" <<'EOS'
set -u
W=$1; cd /home1/chengkai/vd-tree; export TMPDIR="$W"
GCC_CAPTURE="$PWD/workspace/qb-evidence/37564293-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261113.1"
OFFICIAL_CAPTURE="$PWD/workspace/qb-evidence/37736448-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2"
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
get '30d0d296abc99c989078a5bf832c1cdd60ced1ec' 'artifacts/scripts/r0011e/matched-qb.py.txt' 'f44a2f0f36f01cae2d5744baeeb7a222cd639e51d2fc0093a5b883a1d2829e81' || ok=0
get 'd3cea65aac76d438b82b55a2857a5ee18546edad' 'artifacts/scripts/r0005/image-repo-lib.py.txt' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f' || ok=0
get '3e96bc410252a5b3922c0f51f5ed0218852f4feb' 'artifacts/scripts/r0005/mlgo-elf-sections.py.txt' '54a35e35c1844ca4d5cff60e6236d76698fe27f4f582347ed544249c146c34fd' || ok=0
get 'be35ba2b4a6b56d78b0c0309b78eb6194506022b' 'artifacts/scripts/r0011b/weekend-readback.py.txt' 'c5d0facb0a8ddef6dd404655f82dbeb6b2cf3145992c5d30483e79112f19114f' || ok=0
get 'fb98eefaf6d924422466be70f4f95446583adeb1' 'artifacts/scripts/r0010e/exp8-readback.py.txt' 'feeff8d1e1521a70b17a05ce85a1e2fa42cefd31f37777064ac59864cd46f96d' || ok=0
get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75' || ok=0
get 'fb98eefaf6d924422466be70f4f95446583adeb1' 'artifacts/ledger/r1-r7-variants-20261111.tsv' '6145591eb1830090aa5a51c182f64e9594429f603e656eb0cc9eea0b2203d73d' || ok=0
get 'a134afbc404508dfc32e479a2c88dd4a850f4c62' 'artifacts/scripts/r0011/hq-elf-rebaseline.py.txt' '55ea44b32389fe60137e5d06e314def73d695f7b86e879d707ed7533afbc6120' || ok=0
get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b' || ok=0
get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-relocations.py.txt' 'f678d0f9c479d6a183c3f83d7a14917ea46c15533f41d97a3baeb732b6905cf7' || ok=0
get 'a134afbc404508dfc32e479a2c88dd4a850f4c62' 'artifacts/scripts/r0011a/hq-overnight.sh.txt' '5f287377758b319572bb30e40914067e796546b0b250da401fc119ea908cf723' || ok=0
[ "$ok" = 1 ] || { echo "DOWNLOAD_FAILED $(date -Is)" >> "$W/status.txt"; exit 1; }
job() {
  local n=$1; shift
  echo "JOB $n START $(date -Is)" >> "$W/status.txt"
  ( "$@" ) > "$W/$n.txt" 2>&1; local rc=$?
  echo "JOB $n END rc=$rc $(date -Is) lines=$(wc -l < "$W/$n.txt")" >> "$W/status.txt"
}
Q="python3 -B -u $W/matched-qb.py.txt $W/image-repo-lib.py.txt"
job 1-qb-platform $Q platform
job 2-qb-kernel   $Q kernel "$W/mlgo-elf-sections.py.txt"
job 3-qb-srpm     $Q srpm
K="python3 -B -u $W/weekend-readback.py.txt"
job 4-wk-pages         $K pages
job 5-wk-kernel-config $K kernel-config
job 6-wk-tv-viewer     $K tv-viewer "$W/exp8-readback.py.txt" "$W/image_mode_scan.py.txt"
job 7-wk-delivery      $K delivery  "$W/exp8-readback.py.txt" "$W/image_mode_scan.py.txt" "$W/r1-r7-variants-20261111.tsv"
hq() {
  printf '%s  %s/identity.json\n' acd8413894dc1e7ee8dd3625a308ad36ff9d1523e7388cf72f30bd218f4060c5 "$GCC_CAPTURE" | sha256sum -c - &&
  printf '%s  %s/identity.json\n' f164cf5f56ced88fd0618c68df686c79ec36aca85dbeb53972a4b128f135862d "$OFFICIAL_CAPTURE" | sha256sum -c - &&
  H=$(mktemp -d "$PWD/workspace/temp/pm0011a-hq-batch.XXXXXX") && echo "HQ_BATCH_DIR $H" && echo "$H" > "$W/hq-dir.txt" &&
  cp "$W"/hq-elf-rebaseline.py.txt "$W"/perf-bundle.py.txt "$W"/perf-relocations.py.txt "$W"/image_mode_scan.py.txt "$W"/hq-overnight.sh.txt "$H/" &&
  TMPDIR="$H" bash "$H/hq-overnight.sh.txt" "$H" "$GCC_CAPTURE" "$OFFICIAL_CAPTURE"
}
job 8-hq-overnight hq
echo "DONE $(date -Is)" >> "$W/status.txt"
EOS
nohup setsid bash "$W/run.sh" "$W" > "$W/nohup.log" 2>&1 < /dev/null &
echo "BATCH_DIR $W"
else
echo "Another heavy job is running; wait for it to finish:"; echo "$busy"
fi

# ---------------- progress (explicit directory; do not use ls|tail) ----------------
# W=<BATCH_DIR printed above>; cat "$W/status.txt"; tail -2 "$W"/[1-8]-*.txt 2>/dev/null; [ -f "$W/hq-dir.txt" ] && tail -3 "$(cat "$W/hq-dir.txt")/status.txt"
# ---------------- readback when status shows DONE ----------------
# { echo "BATCH_DIR $W"; cat "$W/status.txt" "$W/downloads.txt"; for f in "$W"/[1-8]-*.txt; do echo "===== ${f##*/}"; cat "$f"; done;
#   [ -f "$W/hq-dir.txt" ] && { echo "===== hq combined.txt"; cat "$(cat "$W/hq-dir.txt")/combined.txt"; }; } > "$W/combined.txt"
# cat "$W/status.txt"; wc -l "$W/combined.txt"; sha256sum "$W/combined.txt"
