# Round 0010c native command — read-only except one new file under workspace/temp.
# 1) Tags every 11 Nov z901 log by hook variant; 2) writes the final (no-warning) hook value as HOOK_FILE;
# 3) prints the z901 experiment / GBS-root package rosters for the R1–R7 22-source recovery.
cd /home1/chengkai/vd-tree
OUT="workspace/temp/pm0010c-hook-roster-$(date +%Y%m%d-%H%M%S).txt"
(
set -u
Z=workspace/temp/z901
echo "PM0010C START $(date -Is)"
echo "== hook variant per log (FINAL = no warning flags; WARN = with -Wall/-Wshadow): variant | mtime | path"
find "$Z" -xdev \( -name 'log.txt' -o -name 'gbs.log' \) -print0 2>/dev/null | xargs -0 -r grep -l 'CCC_OVERRIDE_OPTIONS=' 2>/dev/null | sort | while read -r f; do
  v=$(grep -h -o -m1 "CCC_OVERRIDE_OPTIONS=.*" "$f")
  case "$v" in *"+-Wall"*) t=WARN ;; *"+-Wno-cast-function-type-strict"*) t=FINAL ;; *) t=OTHER ;; esac
  echo "V $t | $(date -r "$f" +%m-%dT%H:%M) | $f"
done
echo "== distinct FINAL values (count | sha256 of value)"
find "$Z" -xdev \( -name 'log.txt' -o -name 'gbs.log' \) -print0 2>/dev/null | xargs -0 -r grep -h -o "CCC_OVERRIDE_OPTIONS=.*" 2>/dev/null \
  | grep -v -- '+-Wall' | sed -e "s/^CCC_OVERRIDE_OPTIONS=//" -e "s/^'//" -e "s/'\$//" | sort | uniq -c \
  | while read -r n val; do echo "FV $n | $(printf '%s' "$val" | sha256sum | cut -c1-16) | ${#val} chars"; done
H=workspace/temp/pm0010c-nov11-hook-final.txt
find "$Z" -xdev \( -name 'log.txt' -o -name 'gbs.log' \) -print0 2>/dev/null | xargs -0 -r grep -h -o "CCC_OVERRIDE_OPTIONS=.*" 2>/dev/null \
  | grep -v -- '+-Wall' | sed -e "s/^CCC_OVERRIDE_OPTIONS=//" -e "s/^'//" -e "s/'\$//" | sort | uniq -c | sort -rn | head -1 \
  | sed 's/^ *[0-9]* //' > "$H"
echo "HOOK_FILE $PWD/$H"
echo "HOOK_SHA256 $(sha256sum "$H" | cut -c1-64)"
echo "HOOK_VALUE $(cat "$H")"
echo "HOOK_HAS_MTHUMB $(grep -c -- '+-mthumb' "$H")  HOOK_HAS_OS $(grep -c -- '+-Os' "$H")"
echo "== z901 experiment dirs: exp | package dirs"
for e in "$Z"/exp*; do [ -d "$e" ] && echo "E ${e##*/} | $(ls -1 "$e" | tr '\n' ' ')"; done
echo "== z901 GBS roots: root | built packages (success / fail)"
for r in "$Z"/gbs-root*; do
  [ -d "$r" ] || continue
  s=$(ls -1 "$r"/local/repos/*/armv7l/logs/success 2>/dev/null | sed 's/-[0-9][^-]*-[0-9][^-]*$//' | sort -u | tr '\n' ' ')
  x=$(ls -1 "$r"/local/repos/*/armv7l/logs/fail 2>/dev/null | sed 's/-[0-9][^-]*-[0-9][^-]*$//' | sort -u | tr '\n' ' ')
  echo "R ${r##*/} | S: $s| F: $x"
done
echo "== all z901 package names seen in success/fail logs (count | names)"
n=$(ls -1 "$Z"/gbs-root*/local/repos/*/armv7l/logs/{success,fail} 2>/dev/null | grep -v ':$' | grep . | sed 's/-[0-9][^-]*-[0-9][^-]*$//' | sort -u)
echo "N $(echo "$n" | grep -c .) | $(echo "$n" | tr '\n' ' ')"
echo "PM0010C DONE $(date -Is)"
) 2>&1 | tee "$OUT"
sha256sum "$OUT"
