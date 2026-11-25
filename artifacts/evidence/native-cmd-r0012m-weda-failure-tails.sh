# Read-only: print the real failure cause of every Wed-A lane (no GBS, no sudo, no writes).
(
  set -u
  WEDA=/home1/chengkai/vd-tree/workspace/temp/pm0012-wed-a.M5knpj
  for job in "$WEDA"/jobs/thumb-*; do
    [ -d "$job" ] || continue
    printf '=== JOB %s\n' "${job##*/}"
    for f in "$job"/*.log; do [ -f "$f" ] && { printf '--- %s (last 6)\n' "${f##*/}"; tail -n 6 "$f"; }; done
    for lane in baseline default package; do
      [ -d "$job/$lane" ] || continue
      log=$(find "$job/$lane/GBS-ROOT/local/repos" -path '*fail*' -name log.txt 2>/dev/null | head -1)
      [ -n "$log" ] || log=$(find "$job/$lane/GBS-ROOT/local/repos" -name log.txt 2>/dev/null | head -1)
      if [ -n "$log" ]; then
        printf -- '--- %s %s\n' "$lane" "${log#$job/}"
        grep -n -E 'error:|Error [0-9]|[Ee]rror:|fatal|nothing provides|unresolvable|have choice|No such file|not found|undefined reference|cannot find|Bad exit|CMake Error' "$log" | grep -v -E '^[0-9]+:\+ ' | head -n 12
        printf -- '--- %s tail\n' "$lane"; tail -n 8 "$log"
      else
        printf -- '--- %s NO_LOG_TXT; gbs.log tail\n' "$lane"; tail -n 12 "$job/$lane/gbs.log" 2>/dev/null
      fi
    done
  done
  df -h /home1 | tail -1
)
