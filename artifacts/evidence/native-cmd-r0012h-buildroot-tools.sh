# Read-only: which tools exist in the Official armv7l build root kept by the failed Step 5 run, and which RPM owns them.
# Safe to run while the Wed-A pilot is running (no GBS, no sudo, no writes).
(
  set -u
  base=/home1/chengkai/vd-tree/workspace/temp/pm0010-gbs-board-bench.eli_m1on/GBS-ROOT
  R=$(find "$base" -maxdepth 4 -type d -name 'scratch.armv7l.*' 2>/dev/null | head -1)
  [ -n "$R" ] || R=$(find "$base" -maxdepth 4 -type f -path '*/usr/bin/rpm' 2>/dev/null | head -1 | sed 's#/usr/bin/rpm$##')
  echo "BUILDROOT ${R:-NOT_FOUND}"
  [ -n "$R" ] || exit 2
  for t in armv7l-tizen-linux-gnueabi-clang armv7l-tizen-linux-gnueabi-clang++ clang clang++ cc c++ ld ld.bfd ld.lld readelf sha256sum tail head awk gawk sort cut tr sed grep rpm realpath readlink stat dirname basename chmod mktemp find xargs; do
    hit=
    for d in usr/bin bin usr/sbin sbin; do
      p="$R/$d/$t"
      if [ -e "$p" ] || [ -L "$p" ]; then
        if [ -L "$p" ]; then hit="$hit /$d/$t->$(readlink "$p")"; else hit="$hit /$d/$t"; fi
      fi
    done
    printf 'TOOL %-38s %s\n' "$t" "${hit:-MISSING}"
  done
  if command -v rpm >/dev/null 2>&1; then
    echo "HOST_RPM $(rpm --version)"
    for f in /usr/bin/armv7l-tizen-linux-gnueabi-clang /usr/bin/ld /usr/bin/readelf /usr/bin/sha256sum /usr/bin/tail /usr/bin/awk /usr/bin/gawk /usr/bin/rpm /bin/rpm /usr/bin/readlink /usr/bin/stat; do
      [ -e "$R$f" ] || [ -L "$R$f" ] || continue
      printf 'OWNER %-42s %s\n' "$f" "$(rpm --root "$R" -qf "$f" 2>&1 | head -1)"
    done
    for pkg in clang binutils coreutils gawk rpm; do
      printf 'PKG %-10s %s\n' "$pkg" "$(rpm --root "$R" -q "$pkg" 2>&1 | head -1)"
    done
  else
    echo "HOST_RPM MISSING (owner lookup skipped)"
  fi
)
