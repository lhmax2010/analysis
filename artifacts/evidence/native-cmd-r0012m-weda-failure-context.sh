# Read-only: show the real error before "Bad exit status (%build)" in each Wed-A baseline lane,
# plus CMake's own error log from the retained build root. No GBS, no sudo, no writes.
(
  set -u
  WEDA=/home1/chengkai/vd-tree/workspace/temp/pm0012-wed-a.M5knpj
  noise='liblto_plugin\.so|/usr/bin/lua|gcc-warning-build-env|gcc-force-options-only|limits\.conf|systemctl: command|kernel-install|hal-compatibility-checker|Macro expanded in comment'
  for job in "$WEDA"/jobs/thumb-*; do
    lane="$job/baseline"
    [ -d "$lane" ] || continue
    log=$(find "$lane/GBS-ROOT/local/repos" -path '*/logs/fail/*' -name log.txt 2>/dev/null | head -1)
    [ -n "$log" ] || continue
    echo "=== ${job##*/} baseline"
    n=$(grep -n -m1 -E 'Bad exit status from .*\(%build\)' "$log" | cut -d: -f1)
    [ -n "$n" ] || { echo "NO_BAD_EXIT_LINE"; continue; }
    s=$((n>45 ? n-45 : 1))
    sed -n "${s},${n}p" "$log" | grep -v -E "$noise" | grep -v -E '^\[ *[0-9]+s\] \+ ' | tail -n 25
    br="$lane/GBS-ROOT/local/BUILD-ROOTS/scratch.armv7l.0/home/abuild/rpmbuild/BUILD"
    for f in $(find "$br" -maxdepth 6 \( -name CMakeError.log -o -name CMakeConfigureLog.yaml \) 2>/dev/null | head -2); do
      echo "--- ${f#$br/} (error lines)"
      grep -n -E 'error:|undefined reference|cannot find|ld(\.lld)?: |failed|unrecognized|unknown argument' "$f" | head -n 12
    done
  done
  echo "=== default-lane driver probe (AVControl): does the scoped block reach the driver?"
  grep -h -m4 -E 'PM_CFG .*(LOADED|OPTION|MARK)' "$WEDA"/jobs/thumb-org.tizen.AVControl/default/gbs.log 2>/dev/null | cut -c1-300
  df -h /home1 | tail -1
)
