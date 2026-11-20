# Round 0010c reply — Verified hook and Monday step 8

The native `HOOK_VALUE` matches all 480 bytes of the archived value. One final LF gives SHA-256 `bdf0fecb69664a13a11ac42c4ea56337f509c87189459328b007b8a290db2e7e`. Doc 02 and Doc 04 rev2 are archived side-by-side with the originals. Both manifests verify. [Hook transcript](../../artifacts/evidence/native-run-r0010c-hook-file-roster-20261120.txt) [Archive](../../reports/README.md)

Claude approved the replacement below for Monday step 8 at `fb98eefaf6d924422466be70f4f95446583adeb1`. The other steps keep their order. The gate still verifies `Name: libtvs-core` using the matched P4 spec. A failed alias check holds that package. Ctrl-C or a bad hook checksum stops the launch before a GBS job is started.

- A is the unchanged build. B appends `-Os`. C uses the verified native `HOOK_FILE`. D appends `-Os -mthumb` for AVControl, tv-viewer, libpisa-ipc, org.tizen.webserver, libgcrypt, rpm and nnstreamer. Other packages run A/B/C.
- B−A isolates the `-Os` intervention. D−B isolates the Thumb option. C−D measures the remaining hook changes together. Confirm that each lane actually received the intended flags and comparable payload scope using its DWARF, ELF and A32 readback.
- `O_PACKAGE` selects one package, and `O_WORKDIR` reads back an existing run. On the native server allow 20–120 minutes per package, up to six pinned cores, 24 GiB per retained lane plus the reserve, and normal VD dependency traffic. A–D run serially. The launcher uses GitHub for digest-pinned downloads. Research recipes still require the approved roster and any existing experiment gate.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010b-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file"
    printf '%s  %s\n' "$sum" "$file" | sha256sum -c -
  }
  get 'fb98eefaf6d924422466be70f4f95446583adeb1' 'artifacts/scripts/r0010/olevel.py.txt' '874194ebbdbb2165b15030b97d6b5cdc1a0119df62ee605b8b2426a6f4dc9f6c'
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/ledger/olevel-sources-20261120.tsv' '788481656fce951e1434ee44df0acb40c83c44551d2fb590b381664e14151346'
  get 'd3cea65aac76d438b82b55a2857a5ee18546edad' 'artifacts/scripts/r0005/image-repo-lib.py.txt' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-mlgo-t7.py.txt' '1089c21b3b4bf4205bd13ba64cace371c57a7d4ec86376877f3b2d069f551a9c'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/thumb-qb-sample.py.txt' 'b7a725e9c5e68072b9f5388a35df91494874f13f67a00fb7426a3067e04a3579'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-thumb.py.txt' '928cff87ac0cb501a6d0575da5f1d80157bd02918d2378a5e061c2262cf11a92'
  get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/qb-forensics.py.txt' '6bc8e1bbff0a98ff7096ea7ad1806f777fa63aec04c0b9dc2a92fe256294dd82'
  get 'cfde38f9e4c6041069d28adc8b9da35894df0de9' 'artifacts/scripts/r0010b/option-source-readback.py.txt' 'fa0369c1e891ff37e290511843a4ffc8f9723536bb5c4c26ccc361b373411f6d'
  if [[ -n "${O_WORKDIR:-}" ]]; then
    python3 -B -u "$d/olevel.py.txt" readback "$O_WORKDIR"
  else
    args=()
    if [[ -n "${O_PACKAGE:-}" ]]; then args+=(--package "$O_PACKAGE"); fi
    if [[ -z "${O_RESEARCH_RECIPE:-}" ]]; then
      HOOK_FILE=/home1/chengkai/vd-tree/workspace/temp/pm0010c-nov11-hook-final.txt
      HOOK_SHA256=bdf0fecb69664a13a11ac42c4ea56337f509c87189459328b007b8a290db2e7e
      printf '%s  %s\n' "$HOOK_SHA256" "$HOOK_FILE" | sha256sum -c -
      args+=(--hook "$HOOK_FILE" --hook-sha "$HOOK_SHA256")
    fi
    if [[ -n "${SOURCE_RPM_TSV:-}" ]]; then args+=(--source-rpms "$SOURCE_RPM_TSV"); fi
    if [[ -n "${GCC_TEXT_CSV:-}" ]]; then args+=(--gcc-text-csv "$GCC_TEXT_CSV"); fi
    if [[ "${O_PRIORITY_C_ONLY:-0}" == 1 ]]; then args+=(--priority-c-only); fi
    roster=$d/olevel-sources-20261120.tsv
    if [[ -n "${O_RESEARCH_RECIPE:-}" ]]; then
      roster=${O_RESEARCH_ROSTER:?set the reviewed separate source roster}
      printf '%s  %s\n' "${O_RESEARCH_ROSTER_SHA256:?}" "$roster" | sha256sum -c -
      args+=(--recipe "$O_RESEARCH_RECIPE" --recipe-sha "${O_RESEARCH_RECIPE_SHA256:?}")
    else
      resolved="$d/olevel-sources-verified.tsv"
      if python3 -B -u "$d/option-source-readback.py.txt" --capture "${OFFICIAL_CAPTURE:?}" \
          --olevel "$d/olevel.py.txt" --repo "$d/image-repo-lib.py.txt" --gbs "$d/gbs-mlgo-t7.py.txt" \
          --stager "$d/thumb-qb-sample.py.txt" --roster "$roster" --out "$resolved"; then
        roster="$resolved"
        if [[ "${O_PACKAGE:-}" == tvs-core ]]; then args[1]=libtvs-core; fi
      elif [[ "${O_PACKAGE:-}" == tvs-core || "${O_PACKAGE:-}" == libtvs-core ]]; then
        exit 1
      else
        printf 'ALIAS_REVIEW remains open; continuing the other scoped rows\n'
      fi
    fi
    sudo -v
    nohup python3 -B -u "$d/olevel.py.txt" run "${OFFICIAL_CAPTURE:?}" "$roster" \
      "$d/image-repo-lib.py.txt" "$d/gbs-mlgo-t7.py.txt" "$d/thumb-qb-sample.py.txt" \
      "$d/gbs-thumb.py.txt" "$d/image_mode_scan.py.txt" "$d/perf-bundle.py.txt" "$d/qb-forensics.py.txt" \
      "${args[@]}" >"$d/start.log" 2>&1 </dev/null &
    printf 'O_JOB %s LOG %s\n' "$!" "$d/start.log"
    printf 'Read launch status with sed -n 1,12p %q\n' "$d/start.log"
  fi
)
```
