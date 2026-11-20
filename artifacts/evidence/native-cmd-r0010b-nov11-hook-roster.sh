# Round 0010b native command — read-only. Locates the 11 Nov forced-option hook value and the R1–R7 sample roster.
# Searches logs/build.conf files under vd-tree modified 1–14 Nov; prints paths, SHA-256, the distinct expanded
# CCC_OVERRIDE_OPTIONS values, the hook definition lines, and the package list of each GBS root that used the hook.
cd /home1/chengkai/vd-tree
OUT="workspace/temp/pm0010b-hook-roster-$(date +%Y%m%d-%H%M%S).txt"
(
set -u
echo "PM0010B START $(date -Is)"
L=$(mktemp -p workspace/temp pm0010b-list.XXXXXX)
timeout 900 find . -xdev \( -name 'log.txt' -o -name '*.log' -o -name '*build.conf*' -o -name '*.spec' \) \
  -newermt 2026-11-01 ! -newermt 2026-11-15 -size -300M -print0 2>/dev/null \
  | xargs -0 -r grep -l -E 'CCC_OVERRIDE_OPTIONS|clang_force_incompatible' 2>/dev/null > "$L" || true
echo "HIT_FILES $(wc -l < "$L")"
echo "== build.conf / spec files defining the hook (path | sha256 | lines)"
grep -E 'build\.conf|\.spec$' "$L" | head -20 | while read -r f; do
  echo "F $f | $(sha256sum "$f" | cut -c1-64)"
  grep -n -E '^%(define )?clang_force_incompatible|CCC_OVERRIDE_OPTIONS|^%__vd_flags_toolchain_clang' "$f" | head -8 | cut -c1-600 | sed 's/^/  L /'
done
echo "== distinct expanded CCC_OVERRIDE_OPTIONS values in build logs (count | value)"
grep -v -E 'build\.conf|\.spec$' "$L" | tr '\n' '\0' | xargs -0 -r grep -h -o -E 'CCC_OVERRIDE_OPTIONS=.*' 2>/dev/null \
  | cut -c1-700 | sort | uniq -c | sort -rn | head -12
echo "== GBS roots using the hook: root | packages with a log (first 40 names)"
grep -v -E 'build\.conf|\.spec$' "$L" | sed -n 's#^\(.*/GBS-ROOT[^/]*\)/.*#\1#p' | sort -u | head -15 | while read -r r; do
  p=$(find "$r" -path '*/logs/*' -name 'log.txt' 2>/dev/null | sed -n 's#.*/logs/[a-z]*/\([^/]*\)/log.txt#\1#p' | sed 's/-[0-9][^-]*-[0-9][^-]*$//' | sort -u)
  echo "R $r | $(echo "$p" | grep -c .) | $(echo "$p" | head -40 | tr '\n' ' ')"
done
echo "== log files with the hook, newest 15 (mtime | path | sha256)"
grep -v -E 'build\.conf|\.spec$' "$L" | xargs -r -d '\n' ls -t 2>/dev/null | head -15 | while read -r f; do
  echo "G $(date -r "$f" +%m-%dT%H:%M) | $f | $(sha256sum "$f" | cut -c1-16)"
done
rm -f "$L"
echo "PM0010B DONE $(date -Is)"
) 2>&1 | tee "$OUT"
sha256sum "$OUT"
