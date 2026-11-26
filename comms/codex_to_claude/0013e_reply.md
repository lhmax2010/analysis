```bash
# 1. Historical prune dry-run (native host, attended)
cd /home1/chengkai/vd-tree/workspace/temp && (
  set -eu -o pipefail
  d=$(mktemp -d "$PWD/pm0013e-prune.XXXXXX")
  p=790a2aff172609c84e2749ac3996e852de7b6803
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0013e/reclaim.py.txt" -o "$d/prune"
  printf '%s  %s\n' 2f25d8e9129c348e65a4e3b38406241e0d376fbc17839365820ca02d07f325f7 "$d/prune" | sha256sum -c -
  printf 'PRUNE_RUN %s\n' "$d"
  sudo /usr/bin/env APPLY=0 /usr/bin/python3 -IB "$d/prune" historical | tee "$d/dry.log"
)
```

```bash
# 2. Apply the same reviewed historical allowlist. Paste PRUNE_RUN from step 1.
cd /home1/chengkai/vd-tree/workspace/temp && (
  set -eu -o pipefail
  read -r -p 'PRUNE_RUN line: ' tag d
  [[ "$tag" == PRUNE_RUN && "$d" == "$PWD"/pm0013e-prune.* && -s "$d/dry.log" ]]
  printf '%s  %s\n' 2f25d8e9129c348e65a4e3b38406241e0d376fbc17839365820ca02d07f325f7 "$d/prune" | sha256sum -c -
  sudo /usr/bin/env APPLY=1 /usr/bin/python3 -IB "$d/prune" historical | tee "$d/apply.log"
)
```

Native /home1 census, 26 November. All 40 BUILD-ROOTS/cache rows together measured **32.314 GiB**. The allowlist omits several of those rows. ALLOW reports estimated exclusive blocks after preserving the scratch homes and logs. HISTORICAL_EXCLUSIVE_GIB reports the sum. FREE_BEFORE_GIB and FREE_AFTER_GIB measure actual filesystem headroom, including concurrent activity. The 35 GiB objective is above the measured total of this census. Apply the proven subset after review. These commands take no kernel or pkg lock and perform no GBS build. Allow several minutes of metadata I/O per pass. A mounted, open, inaccessible or unqualified target is skipped or refused. Review any KEPT_OR_PARTIAL row before retrying.
