# Round 0011e — chain results and KantSU2E board day

All four native chain jobs exited 0 at 16:13:39 CST. The GCC capture and both USB bundles are ready. The Base proof explicitly returned `REVIEW_STATUS INCOMPLETE`. The archived terminal transcript is 155 lines and contains a 108-line `combined.txt` block. Both SHA-256 values match the handoff. [Raw chain transcript](../../artifacts/evidence/native-run-r0011c-chain-AFkXQV-20261124.txt)

The GCC 37564293 receipt contains a 1,806,199,092 B PERF archive, 5,880 Product RPM identities and four kernel RPMs. Its published build.conf SHA-256 is `5e78db500271042c3d3d58c5f6933e6ef8365aaf1a039af45b9259bdbba20ba0`. The GCC force-options entries appear at 320/321/425. Keep the GCC kernel RPM sizes internal while checking the three kernel NEVRA/SRPM/VCS rows. The GCC 10.1 reference and LLVM 10.0 images also differ in Product date.

| Kernel evidence | Official QB 37736448 | Customized QB 37736427 | Comparison with 18 Nov GBS replay |
|---|---:|---:|---|
| USB uImage | 11,348,968 B | 11,085,240 B | Same sizes (−2.32% between lanes). QB/GBS hash comparison pending. |
| USB zImage | 5,326,504 B | 5,222,032 B | +40 B and −272 B versus GBS. |
| Linked PERF vmlinux `.text` | GBS 8,564,600 B | GBS 8,315,832 B | −2.90% applies to the retained replay. The matched QB section comparison needs a linked PERF ELF or equivalent authenticated build artifact. |
| Packaged `vmlinux` | Matched QB member readback below | Matched QB member readback below | The earlier shipped member with this name was detached BTF. Classify the new member before comparing. |

Treat kernel section hashes and sizes separately from boot blob sizes. The kernel readback below checks retained RPM member hashes against the matching replay and staged USB. It compares sections if a linked PERF ELF is present. The GCC reference rows include binary NEVRA, source RPM and pinned VCS. [GBS replay](../../artifacts/evidence/native-run-r0005-gbs-kernel-thumb-20261118.txt)

## Board-day runbook

### 1. Copy and verify both flash USBs

Use separately labelled, already mounted flash drives. Supply their actual mount roots as `OFFICIAL_USB` and `CUSTOM_USB`. The command stages a new root-level `updateSU2E/` on each drive. If the folder is already present, it checks the exact file set and every SHA-256 without copying. An existing mismatch requires a clean drive or deliberate operator cleanup. Compare the printed QB label and eject each drive cleanly. Keep the verified Official USB available for rollback.

```bash
(
  set -euo pipefail
  root=/home1/chengkai/vd-tree/workspace/usb
  mount_official=$(realpath -e "${OFFICIAL_USB:?set the Official flash USB mount root}")
  mount_custom=$(realpath -e "${CUSTOM_USB:?set the Customized flash USB mount root}")
  [[ "$mount_official" != "$mount_custom" ]]
  copy_lane() {
    local qb=$1 mount=$2 prep="$root/$1" target="$2/updateSU2E"
    mountpoint -q -- "$mount"
    (cd "$prep/updateSU2E"; sha256sum --strict --status -c ../manifest.sha256)
    cmp \
      <(awk '{print substr($0,67)}' "$prep/manifest.sha256" | LC_ALL=C sort) \
      <(find "$prep/updateSU2E" -mindepth 1 -maxdepth 1 -type f -printf '%f\n' | LC_ALL=C sort)
    [[ -z "$(find "$prep/updateSU2E" -mindepth 1 -maxdepth 1 ! -type f -print -quit)" ]]
    if [[ ! -e "$target" && ! -L "$target" ]]; then
      mkdir -- "$target"
      cp -- "$prep"/updateSU2E/* "$target/"
      sync -f -- "$target"
    fi
    [[ -d "$target" && ! -L "$target" ]]
    cmp       <(find "$prep/updateSU2E" -mindepth 1 -maxdepth 1 -printf '%f\n' | LC_ALL=C sort)       <(find "$target" -mindepth 1 -maxdepth 1 -type f -printf '%f\n' | LC_ALL=C sort)
    [[ -z "$(find "$target" -mindepth 1 -maxdepth 1 ! -type f -print -quit)" ]]
    (cd "$target"; sha256sum --strict -c "$prep/manifest.sha256")
    printf 'USB_BUNDLE_VERIFIED %s %s\n' "$qb" "$target"
  }
  copy_lane 37736448 "$mount_official"
  copy_lane 37736427 "$mount_custom"
)
```

### 2. Stage the Step 5 benchmark

Run this on the native host while preparing the USBs. It uses Official QB 37736448 and makes one GBS build under the shared lock. Keep the printed `BOARD_TOOLS` directory for every visit. Budget 10–40 minutes, up to six cores, 24 GiB scratch plus reserves and native dependency traffic. The benchmark and three board files are hash-checked on the TV during staging.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0010-board.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}" attempt
    for attempt in 1 2 3 4 5; do
      if curl -fsS --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file" &&
         printf '%s  %s\n' "$sum" "$file" | sha256sum -c -; then
        return 0
      fi
      printf 'DOWNLOAD_FAILED attempt=%s/5 %s\n' "$attempt" "${path##*/}" >&2
      if (( attempt < 5 )); then sleep 10; fi
    done
    return 1
  }
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/scripts/r0010/gbs-board-bench.py.txt' 'ec400673256b6b0ce318aebf33b6336eb785fd0c2a9defba17f5a983cd334db7'
  get '97a50bcacc7402d8297b25a47b1f2117b40c6d72' 'artifacts/scripts/r0010/olevel.py.txt' '7ea4a4c99204ae9a280e83d46a1e3de2b7ff721ce7a8079294e36393401259bf'
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/scripts/r0010/mlgo-tv-run.sh.txt' 'fa28ef445fed4ee573d1504ad0b7b19aad066d9b595cb90ea9a8d53c0aa64f3b'
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/scripts/r0010/mlgo-tv-measure.sh.txt' 'd065017fb0bd825bb9c1ff86ced0616406f414ef7f41b794b35c54fcf17850e4'
  get '07883080780af09b3f195ac6efaba639b0ab7bb8' 'artifacts/scripts/r0010/mlgo-tv-microbench.c.txt' '04981794ea071c5d7aef39a911086abf451cb136796e4e8edc6bffa39f66796a'
  get '2303fa18ff0bc39bd26e8b6dc683bbb24bd7611a' 'artifacts/scripts/r0005/mlgo-tv-identity.sh.txt' '21070fc762b878343faac9a331235ad2dfde06eb87cfa7f2f5ac24a5b855e5cf'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-mlgo-t7.py.txt' '1089c21b3b4bf4205bd13ba64cace371c57a7d4ec86376877f3b2d069f551a9c'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-thumb.py.txt' '928cff87ac0cb501a6d0575da5f1d80157bd02918d2378a5e061c2262cf11a92'
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/thumb-qb-sample.py.txt' 'b7a725e9c5e68072b9f5388a35df91494874f13f67a00fb7426a3067e04a3579'
  get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  (cd "$d"; sha256sum mlgo-tv-identity.sh.txt mlgo-tv-measure.sh.txt mlgo-tv-microbench.c.txt > inputs.sha256)
  OFFICIAL_CAPTURE="$PWD/workspace/qb-evidence/37736448-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2"
  printf '%s  %s/identity.json\n' f164cf5f56ced88fd0618c68df686c79ec36aca85dbeb53972a4b128f135862d "$OFFICIAL_CAPTURE" | sha256sum -c -
  sudo -v
  python3 -B -u "$d/gbs-board-bench.py.txt" "$d" "${OFFICIAL_CAPTURE:?}" "$d/mlgo-tv-microbench.c.txt" \
    "$d/olevel.py.txt" "$d/gbs-mlgo-t7.py.txt" "$d/thumb-qb-sample.py.txt" "$d/gbs-thumb.py.txt" \
    "$d/image_mode_scan.py.txt" "$d/perf-bundle.py.txt"
  printf 'BOARD_TOOLS %s\n' "$d"
)
```

### 3. Flash, verify and measure one visit at a time

Use one board and alternate `O1 C1 O2 C2 O3 C3 O4 C4 O5 C5`. Use the same cold-boot, Home readiness, idle, clip, temperature and governor procedure. At each visit verify the USB label and manifest, reboot into BOOST with the confirmed input (`~`), enter `mmc`, confirm the menu's USB full-image option `a`, then flash using the established board procedure. Keep power and the USB connected while writing. Save the successful flash receipt or console transcript on the native host. When flash status is uncertain, stop at the console and follow the board owner's recovery procedure. [BOOST and recovery procedure](../../reports/KantSU2E_MLGO_Board_Day_0005.md#gated-board-day-checklist)

Once per board day on the native machine, set `BOARD_TOOLS` to the printed path and `TV_SERIAL` to the confirmed `sdb devices` serial. Keep the value of `BOARD_RUN`. Logs copied to this directory survive a full flash.

```bash
cd /home1/chengkai/vd-tree
sdb devices | sed -n '1,30p'
export BOARD_RUN=$(mktemp -d "$PWD/workspace/temp/pm0011e-board.XXXXXX")
printf 'BOARD_RUN %s\n' "$BOARD_RUN"

board() {
  bash "${BOARD_TOOLS:?set BOARD_TOOLS}/mlgo-tv-run.sh.txt" \
    "$BOARD_TOOLS" "${TV_SERIAL:?set the confirmed KantSU2E serial}" "$@"
}
board_log() {
  local name=$1
  shift
  (
    set -o pipefail
    board "$@" | tee "${VISIT:?set VISIT}/$name.txt"
  )
}
```

For each visit use `LANE=official` or `custom` and `N=1…5`. Perform the measured cold boot before staging tools and capturing identity for that visit. Fill `FLASH_RECORD` with the actual verified flash completion reference, including QB and USB label. Start measurements only after confirming the identity. A displayed build identifier or an unambiguous kernel fingerprint can corroborate the flash receipt. A matching kernel NEVRA alone is insufficient because the two lanes can share it. The first accepted identity and full board roster per lane are the Base-proof inputs. Repeated visits verify roster consistency.

```bash
case "$LANE:$N" in
  official:[1-5]) QB=37736448; PRODUCT=20261123.2 ;;
  custom:[1-5]) QB=37736427; PRODUCT=20261123.1 ;;
  *) printf 'Set LANE=official or custom and N=1..5\n' >&2; false ;;
esac
VISIT="$BOARD_RUN/$LANE/$N"
mkdir -p -- "$VISIT"
printf 'QB %s PRODUCT %s FLASH %s\n' "$QB" "$PRODUCT" "${FLASH_RECORD:?record the observed successful flash}" >"$VISIT/flash.txt"
board_log stage stage && board_log identity identity
```

After comparing the identity with the flash receipt, export the board RPM roster. Exact epoch/version/release/arch/SRPM rows stay in the native workspace. The terminal shows only row count, path and digest.

```bash
(
  set -euo pipefail
  grep -qx 'BOARD_IDENTITY_END' "$VISIT/identity.txt"
  grep -qx 'PM0010_REMOTE_EXIT 0' "$VISIT/identity.txt"
  sdb -s "$TV_SERIAL" shell "rpm -qa --qf '%{NAME}\t%{EPOCHNUM}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{SOURCERPM}\n'; rc=\$?; printf '\nBOARD_ROSTER_EXIT %s\n' \"\$rc\"" |
    tr -d '\r' >"$VISIT/rpm-raw.txt"
  grep -qx 'BOARD_ROSTER_EXIT 0' "$VISIT/rpm-raw.txt"
  awk -F '\t' '
    /^BOARD_ROSTER_EXIT 0$/ || /^$/ { next }
    NF!=6 || $2 !~ /^[0-9]+$/ { bad=1; next }
    { print; n++ }
    END { exit (bad || n==0) }
  ' "$VISIT/rpm-raw.txt" | LC_ALL=C sort >"$VISIT/installed.tsv"
  lane_roster="$BOARD_RUN/$LANE/installed.tsv"
  if [[ -f "$lane_roster" ]]; then
    cmp -- "$lane_roster" "$VISIT/installed.tsv"
  else
    cp -- "$VISIT/installed.tsv" "$lane_roster"
  fi
  printf 'BOARD_ROSTER %s %s %s\n' "$QB" "$(wc -l <"$lane_roster")" "$lane_roster"
  sha256sum "$lane_roster"
)
```

- **Boot ×5 per lane.** After the flash, use a fresh cold boot under the same conditions and note the stopwatch time from the agreed start event to a responsive Home screen. Refresh the HomeUI PID on that boot. The script also records kernel uptime to HomeUI process start. These are distinct measurements. Record each unique boot ID on the native host.
- **Microbench ×5 per lane.** On visit 1 of each lane, use the same CPU and idle settling interval. One call produces five benchmark samples. Confirm exactly five `MICRO` rows with the same staged binary on both lanes.
- **4K ×3 and memory.** On visits 1–3, use the same 4K clip, player and playback segment. Verify the clip hash, resolution and duration first. Open Home → USB → the clip, start from the beginning, warm up 10 seconds, refresh the validated PIDs and sample 60 seconds. The runner records start, midpoint and end memory, system CPU and process CPU. Use verified drop/late/stall counters or `NA`. Record manually observed stalls and visible failures separately.

```bash
board_log processes processes
# After refreshing HOME_PID and setting the manual stopwatch seconds:
board_log boot boot "$LANE" "$N" "${HOME_PID:?set the observed HomeUI PID}"
printf 'HOME_READY_STOPWATCH_S %s\n' "${HOME_READY_SECONDS:?record the observed Home-ready time}" >"$VISIT/manual.txt"

# Visit 1 in each lane only. Set CPU to the same eligible CPU for both lanes.
board_log micro micro "$LANE" "${CPU:?set the matched CPU}"
test "$(grep -c '^MICRO ' "$VISIT/micro.txt")" -eq 5

# Visits 1–3. Set MEDIA_PIDS to a Bash array of the verified player/process PIDs.
board_log playback playback "$LANE" "$N" 60 "${DROP_COUNTER:-NA}" "${LATE_COUNTER:-NA}" "${STALL_COUNTER:-NA}" "${MEDIA_PIDS[@]}"
board_log memory memory "$LANE" "$N"
```

Before changing lanes, confirm the local files for the completed visit. Preserve the playback and memory raw logs if a sample fails. Record retries, boot IDs, changed PIDs and missing counters. Keep failed trials out of the reported counts.

### 4. Return one combined file per lane

The command generates `official/combined.txt` and `custom/combined.txt` under the same `BOARD_RUN`. The full RPM rosters stay separate. Run with `LANE=official` and again with `LANE=custom`. Return the checksum and each page, setting `BOARD_PAGE=2` and so on. One page is at most 120 lines.

```bash
(
  set -euo pipefail
  case "$LANE" in official|custom) ;; *) exit 2 ;; esac
  root=$(realpath -e "${BOARD_RUN:?set BOARD_RUN}")
  [[ "$root" == /home1/chengkai/vd-tree/workspace/temp/pm0011e-board.* ]]
  lane="$root/$LANE"
  page=${BOARD_PAGE:-1}
  [[ "$page" =~ ^[1-9][0-9]{0,5}$ ]]
  report="$lane/combined.txt"
  if [[ ! -e "$report" ]]; then
    for n in 1 2 3 4 5; do
      for file in flash identity boot manual; do [[ -s "$lane/$n/$file.txt" ]]; done
      grep -qx 'PM0010_REMOTE_EXIT 0' "$lane/$n/identity.txt"
      grep -qx 'PM0010_REMOTE_EXIT 0' "$lane/$n/boot.txt"
      grep -q "^BOOT $n " "$lane/$n/boot.txt"
      boot=$(awk '/^BOOT_ID / { print $2 }' "$lane/$n/identity.txt")
      [[ -n "$boot" ]]
      grep -qxF "LANE $LANE BOOT_ID $boot" "$lane/$n/boot.txt"
    done
    for n in 1 2 3; do
      for file in playback memory; do
        [[ -s "$lane/$n/$file.txt" ]]
        grep -qx 'PM0010_REMOTE_EXIT 0' "$lane/$n/$file.txt"
      done
      grep -q "^PLAYBACK $n " "$lane/$n/playback.txt"
    done
    [[ -s "$lane/1/micro.txt" && -s "$lane/installed.tsv" ]]
    grep -qx 'PM0010_REMOTE_EXIT 0' "$lane/1/micro.txt"
    [[ "$(grep -c '^MICRO ' "$lane/1/micro.txt")" -eq 5 ]]
    test "$(awk '/^BOOT_ID /{print $2}' "$lane"/[1-5]/identity.txt | sort -u | wc -l)" -eq 5
    (
      set -o noclobber
      {
        printf 'BOARD_RESULT %s %s\n' "$LANE" "$root"
        printf 'RPM_COUNT %s\n' "$(wc -l <"$lane/installed.tsv")"
        sha256sum "$lane/installed.tsv"
        for n in 1 2 3 4 5; do
          printf 'VISIT %s\n' "$n"
          for name in flash identity boot manual micro playback memory; do
            input="$lane/$n/$name.txt"
            if [[ -f "$input" ]]; then
              printf '===== %s =====\n' "$name"
              if [[ "$name" == playback ]]; then awk '!/^MEM_/' "$input"; else cat "$input"; fi
            fi
          done
        done
      } >"$report"
    )
  fi
  [[ -f "$report" && ! -L "$report" ]]
  sha256sum "$report"
  total=$(wc -l <"$report")
  last=$(((total + 119) / 120))
  ((page <= last))
  printf 'BOARD_PAGE %s LAST_PAGE %s\n' "$page" "$last"
  sed -n "$(((page - 1) * 120 + 1)),$((page * 120))p" "$report"
)
```

## Close the Base proof and verify the kernel table

**Compiler provenance.** The retained GBS argv call `clang`, and the recorded logical path is `/bin/clang → /usr/bin/clang-22`. The same roots contain a distinct x86-64 accelerator. The evidence records both installed candidates, their ELF architecture and owner. It contains no process-level execution trace tying either candidate to the actual QB compilation.

| GBS lane | ARM driver /usr/bin/clang-22 | x86-64 driver /emul/usr/bin/clang-22 |
|---|---|---|
| Official | clang 22.1.8-9.1, SHA `9234b72f…` | clang-accel 0.4-2.4, SHA `41f12a2e…` |
| Customized | clang 22.1.8-11.1, SHA `a4344025…` | clang-accel 0.4-2.5, SHA `8a463a75…` |

The retained LLVM specs enable `LLVM_LINK_LLVM_DYLIB` and feed precompiled InlinerSizeModel and RegAllocEvictModel objects into the LLVM build for each host architecture. This locates the model inputs in the LLVM source/build flow. The separate accelerator SRPM identity alone gives no evidence about which MLGO objects were linked into its Clang or loaded through its libLLVM. The native readback checks both drivers' `DT_NEEDED`, `RPATH/RUNPATH`, file digests and available model symbols in the roots. Stripped symbols may leave the link map unresolved. To name the actual QB compiler and model, obtain the QB compile/acceleration trace or equivalent build-root provenance tying the executed binary and resolved library to their hashes. A traced GBS invocation would establish the replay path. Keep attribution at Base swap while this evidence is incomplete. [GBS tool owners and hashes](../../artifacts/evidence/native-run-r0005-gbs-kernel-thumb-20261118.txt#L85) [Official AOT spec excerpt](../../artifacts/evidence/official-mlgo-obs-source-excerpt-20261119.txt)

**SRPM.** The 404 applies to `repos/base/src/packages/repodata/repomd.xml`. The other layouts are unverified because the snapshots are intranet-only. The `srpm` action probes bounded source-repository layouts under the exact two snapshot URLs, checks primary metadata and downloads only the exact published `llvm-22.1.8-9.1.src.rpm` and `llvm-22.1.8-11.1.src.rpm` with a verified SHA-256. It writes the `MLGO_PROOF_RPMS` TSV when both are verified. If the snapshots omit SRPMs, use the matching historical OBS exports or a retained mirror. Set `OFFICIAL_SRPM` and `CUSTOM_SRPM` to their local workspace paths to generate the same TSV. Such rows carry the operator-retained provenance unless matched against published metadata. An OBS current-head RPM with a different release does not qualify.

**Platform.** “Not ext2/3/4” is the old parser's observation, so the actual filesystem remains unknown. The `platform` action reads the checksum-verified staged `platform.img` files with `file`, `blkid -p` and aligned ext, sparse, SquashFS and EROFS signature checks. A unique SquashFS match can extract only known RPM DB paths into scratch with one processor and no mount. On other formats, missing tooling or an unreadable DB, use the board rosters collected above. [SquashFS extraction options](https://github.com/plougher/squashfs-tools/blob/master/Documentation/4.7.4/USAGE-UNSQUASHFS.md) [EROFS format documentation](https://www.kernel.org/doc/html/latest/filesystems/erofs.html)

Native host after Claude review. Set `QB_ACTION=platform`, `kernel`, or `srpm`. Platform normally needs seconds to minutes and reads both staged platform images, about 2.4 GB total, plus any targeted RPM DB extraction. Kernel inspects local RPMs and retained GBS paths, with a few minutes of disk I/O and scratch for any exact PERF ELF payload. SRPM uses intranet metadata reads and up to two LLVM SRPM downloads, with several minutes possible. Run these away from competing disk-intensive work when practical. The outputs are compact; full artifacts stay under `workspace/temp/pm0011e-qb.*`.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0011e-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}" attempt
    for attempt in 1 2 3 4 5; do
      if curl -fsS --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file" &&
         printf '%s  %s\n' "$sum" "$file" | sha256sum -c -; then
        return 0
      fi
      printf 'DOWNLOAD_FAILED attempt=%s/5 %s\n' "$attempt" "${path##*/}" >&2
      if (( attempt < 5 )); then sleep 10; fi
    done
    return 1
  }
  get '30d0d296abc99c989078a5bf832c1cdd60ced1ec' 'artifacts/scripts/r0011e/matched-qb.py.txt' 'f44a2f0f36f01cae2d5744baeeb7a222cd639e51d2fc0093a5b883a1d2829e81'
  get 'd3cea65aac76d438b82b55a2857a5ee18546edad' 'artifacts/scripts/r0005/image-repo-lib.py.txt' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
  case "${QB_ACTION:-platform}" in
    platform) args=(platform) ;;
    kernel)
      get '3e96bc410252a5b3922c0f51f5ed0218852f4feb' 'artifacts/scripts/r0005/mlgo-elf-sections.py.txt' '54a35e35c1844ca4d5cff60e6236d76698fe27f4f582347ed544249c146c34fd'
      args=(kernel "$d/mlgo-elf-sections.py.txt")
      ;;
    srpm)
      args=(srpm)
      if [[ -n "${OFFICIAL_SRPM:-}${CUSTOM_SRPM:-}" ]]; then
        args+=(--local "${OFFICIAL_SRPM:?set both retained SRPMs}" "${CUSTOM_SRPM:?set both retained SRPMs}")
      fi
      ;;
    *) exit 2 ;;
  esac
  python3 -B -u "$d/matched-qb.py.txt" "$d/image-repo-lib.py.txt" "${args[@]}"
)
```

After both lane rosters and the SRPM TSV exist, rerun the [pinned MLGO Base proof](0011_reply.md#step-3-and-the-mlgo-base-proof) using the second Bash block under Step 3, with both original capture directories. Set the following values in the same terminal. The Base proof shares the heavy lock with Step 5 and the overnight scan. Keep its report and pages for Claude.

```bash
unset MLGO_PROOF_REPORT
export MLGO_OFFICIAL_ROSTER="${BOARD_RUN:?set BOARD_RUN}/official/installed.tsv"
export MLGO_CUSTOM_ROSTER="$BOARD_RUN/custom/installed.tsv"
export MLGO_PROOF_RPMS="${MLGO_PROOF_RPMS:?set the printed verified TSV path}"
export OFFICIAL_CAPTURE=/home1/chengkai/vd-tree/workspace/qb-evidence/37736448-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2
export CUSTOM_CAPTURE=/home1/chengkai/vd-tree/workspace/qb-evidence/37736427-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.1
```

## Start HQ overnight after Step 5 staging

The captures are filled in below. Wait for `GBS_BENCH_READY`, the final `BOARD_TOOLS` line and the Step 5 staging command to exit. Keep the overnight batch in its own heavy-job slot. Native scan estimate is 20–90 minutes per image, serial GCC then LLVM, plus the comparison. Budget one archive reader, expanded-partition scratch and the shared 50 GiB reserve. GitHub traffic is limited to pinned setup downloads.

The current approved overnight scanner shares the ext/sparse-ext traversal. The Base proof's platform failure is therefore relevant. If the overnight logs show an unsupported rootfs, missing owner DB or incomplete coverage, keep `combined.txt`, `coverage.txt` and the platform probe. Those results cannot support a complete installed-image comparison. [Overnight results and output rules](0011a_reply.md#overnight-hq-comparison)

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  tools=$(realpath -e "${BOARD_TOOLS:?set the completed Step 5 BOARD_TOOLS}")
  [[ "$tools" == "$PWD"/workspace/temp/pm0010-board.* ]]
  (cd "$tools"; sha256sum -c microbench.sha256)
  GCC_CAPTURE="$PWD/workspace/qb-evidence/37564293-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261113.1"
  OFFICIAL_CAPTURE="$PWD/workspace/qb-evidence/37736448-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2"
  printf '%s  %s/identity.json\n' acd8413894dc1e7ee8dd3625a308ad36ff9d1523e7388cf72f30bd218f4060c5 "$GCC_CAPTURE" | sha256sum -c -
  printf '%s  %s/identity.json\n' f164cf5f56ced88fd0618c68df686c79ec36aca85dbeb53972a4b128f135862d "$OFFICIAL_CAPTURE" | sha256sum -c -
  d=$(mktemp -d "$PWD/workspace/temp/pm0011a-hq-batch.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 path=$2 sum=$3 file="$d/${2##*/}" attempt
    for attempt in 1 2 3 4 5; do
      if curl -fsS --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$file" &&
         printf '%s  %s\n' "$sum" "$file" | sha256sum -c -; then
        return 0
      fi
      printf 'DOWNLOAD_FAILED attempt=%s/5 %s\n' "$attempt" "${path##*/}" >&2
      if (( attempt < 5 )); then sleep 10; fi
    done
    return 1
  }
  get 'a134afbc404508dfc32e479a2c88dd4a850f4c62' 'artifacts/scripts/r0011/hq-elf-rebaseline.py.txt' '55ea44b32389fe60137e5d06e314def73d695f7b86e879d707ed7533afbc6120'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-bundle.py.txt' '4f27cada1fc6d707b463d0c713fa683b2027db1a0dbc393e64022e58aa09715b'
  get '713883c9f21439a84b83a07ef3a4b2c555f18db5' 'artifacts/scripts/r0009/perf-relocations.py.txt' 'f678d0f9c479d6a183c3f83d7a14917ea46c15533f41d97a3baeb732b6905cf7'
  get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75'
  get 'a134afbc404508dfc32e479a2c88dd4a850f4c62' 'artifacts/scripts/r0011a/hq-overnight.sh.txt' '5f287377758b319572bb30e40914067e796546b0b250da401fc119ea908cf723'
  nohup setsid bash "$d/hq-overnight.sh.txt" "$d" "$GCC_CAPTURE" "$OFFICIAL_CAPTURE" \
    >"$d/nohup.log" 2>&1 </dev/null &
  printf 'HQ_BATCH_DIR %s PID %s\n' "$d" "$!"
)
```
