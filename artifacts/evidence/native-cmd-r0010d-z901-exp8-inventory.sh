# Round 0010d native command — read-only. Inventory of the 11 Nov option experiments in z901/exp and z901/exp8:
# one line per package/variant with RPM and log presence and the experiment flags found in its build log.
cd /home1/chengkai/vd-tree
OUT="workspace/temp/pm0010d-exp8-inventory-$(date +%Y%m%d-%H%M%S).txt"
(
set -u
Z=workspace/temp/z901
echo "PM0010D START $(date -Is)"
echo "== top-level files in exp/ and exp8/ (name | bytes | sha256-16)"
for e in "$Z"/exp "$Z"/exp8; do
  find "$e" -maxdepth 1 -type f 2>/dev/null | sort | while read -r f; do
    echo "T ${f#$Z/} | $(stat -c %s "$f") | $(sha256sum "$f" | cut -c1-16)"
  done
done
echo "== package | variant | mtime | rpms | log | experiment flags in log"
P='-flto=thin|-flto=full|-flto\b|-ffat-lto-objects|inline-threshold=[0-9]+|inlinehint-threshold=[0-9]+|enable-machine-outliner(=[a-z-]+)?|-fuse-ld=[a-z.]+|--icf=[a-z]+|pack-relative-relocs|--pack-dyn-relocs=[a-z]+|-fvisibility-inlines-hidden|-fvisibility=[a-z]+|-ffunction-sections|-fdata-sections|--gc-sections|-fstack-protector-strong|-fsigned-char|-mthumb|-marm|CCC_OVERRIDE_OPTIONS'
for e in "$Z"/exp "$Z"/exp8; do
  for d in "$e"/*/*/; do
    [ -d "$d" ] || continue
    d=${d%/}; v=${d##*/}; p=${d%/*}; p=${p##*/}
    r=$(find "$d" -name '*.rpm' 2>/dev/null | wc -l)
    l=$(ls "$d"/log.txt "$d"/gbs.log 2>/dev/null | head -1)
    if [ -n "$l" ]; then
      fl=$(grep -o -h -E -- "$P" "$d"/log.txt "$d"/gbs.log 2>/dev/null | sort | uniq -c | sort -rn | awk '{printf "%s(%s) ", $2, $1}' | cut -c1-300)
      echo "X ${e##*/}/$p | $v | $(date -r "$l" +%m-%dT%H:%M) | $r | y | $fl"
    else
      echo "X ${e##*/}/$p | $v | $(date -r "$d" +%m-%dT%H:%M) | $r | n | $(ls -1 "$d" | head -6 | tr '\n' ' ')"
    fi
  done
done
echo "PM0010D DONE $(date -Is)"
) 2>&1 | tee "$OUT"
sha256sum "$OUT"
