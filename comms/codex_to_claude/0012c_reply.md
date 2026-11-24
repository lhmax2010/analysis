# Round 0012c+d • Native evidence and replacement commands

**The installed-roster comparison and the benchmark build are still open.** In batch `pm0011f-batch.xkHDpd`, jobs 1–7 returned zero, and HQ job 8 returned 2 with zero installed headers. The two platform images have GPT and an EROFS partition starting at sector 2048. The benchmark now stages the correct C input (`04981794…`), then the original armv7l link fails on `-lc`. [Batch transcript](../../artifacts/evidence/native-run-r0011f-batch-xkHDpd-20261124.txt) · [Benchmark transcript](../../artifacts/evidence/native-run-r0012b-step5-bench-fail-20261124.txt)

## Native command order for Claude review

Use the function below on the native server. The runner and its dependent-file manifest are pinned separately. Each invocation prints the explicit run directory. The batch retains one log per job and a bounded combined readback. Downloads use five attempts.

```bash
pm12() (
  set -eu
  cd /home1/chengkai/vd-tree
  mode=$1; shift
  pin=0a4e9ec3592aa1fa870d7b2aa0119426a1f40220
  index=414d3eb332ea41387ea0c315045492275920790d3bc7414c70e698fb9005bb1d
  d=$(mktemp -d "$PWD/workspace/temp/pm0012-launch.XXXXXX")
  curl -fsSL --retry 4 --retry-all-errors --retry-delay 5 --connect-timeout 15 --max-time 120 \
    "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012/batch.sh.txt" -o "$d/batch.sh"
  printf '%s  %s\n' e8cecabe4ee4155cc1320f74cc934cbb16a22893aecc37bcd329d0fea421be4d "$d/batch.sh" | sha256sum -c -
  if [ "$mode" = image ]; then
    exec bash "$d/batch.sh" launch "$pin" "$index" "$mode" "$@"
  fi
  if [ -t 0 ] && command -v screen >/dev/null && [ -z "${STY:-}" ]; then
    exec screen -S "pm12-$mode" bash "$d/batch.sh" attended "$pin" "$index" "$mode" "$@"
  fi
  exec bash "$d/batch.sh" attended "$pin" "$index" "$mode" "$@"
)
```

1. **Wed-A pilot**, independent of the image audit. Run `pm12 wed-a`. This stages three lanes from Official 37736448 with up to six pinned cores, one GBS job at a time. Allow one night or longer depending on source size. Each build needs at least 24 GiB free and 12 GiB RAM available at its start. Roots accumulate. Dependencies and sources come from pinned internal repos/P4. With GNU screen, enter sudo credentials in that terminal, note the printed run directory, then detach with Ctrl+A, D. Reattach using `screen -r pm12-wed-a`. The original terminal owns a 45-second sudo validation loop. With no screen, keep the foreground terminal connected. A rejected refresh or an expired P4 ticket is logged. Confirm `p4 login -s` first.
2. **Image chain**, after the pilot exits or in an earlier exclusive slot. Run `pm12 image`. It runs installed rosters → Base proof with the returned SRPM manifest → direct SRPM, symbol and config evidence → GCC and LLVM HQ scans/compare → roster cross-check → both TEXTREL audits/compare → Official A32 roster. Budget several hours, CPU primarily decompression, substantial internal debuginfo and package traffic. The extraction checks for four partition lengths of working room above a 50 GiB reserve. It reuses one extraction per SHA-256 across jobs. A `DONE` alone is insufficient. Inspect per-job return codes, both `ROSTER_MATCH` counts, omissions and scan errors.
3. Use the explicit path from the launcher with `pm12read "$RUN"`. For the direct SRPM evidence run `python3 -B "$RUN/proofs.py.txt" "$RUN"/jobs/sources/proof.*/native-proofs.json --page 1`; increment the page through its printed total. For the A32 roster use `python3 -B "$RUN/development.py.txt" packet "$RUN/jobs/thumb-roster/thumb-roster.json" 1`. Return the combined terminal text first. These readbacks require no heavy lock.

```bash
pm12read() (
  set -eu
  run=$(realpath -e -- "$1")
  case "$run" in /home1/chengkai/vd-tree/workspace/temp/pm0012-* ) ;; *) exit 2 ;; esac
  if [ -f "$run/combined.txt" ]; then head -n 260 "$run/combined.txt"; sha256sum "$run/combined.txt"
  else tail -n 55 "$run/status.txt"; fi
)
```

## Filesystem and RPM ownership verification

Native has fsck.erofs, dump.erofs and mkfs.erofs 1.7.1. The shared reader uses sfdisk sector size/start/length, verifies EROFS magic at partition offset +1024 and checks the partition with fsck before extraction. When an offset input is needed it copies the exact GPT extent to scratch, extracts with file modes and symlinks preserved, and releases the extent. Each receipt records image SHA-256, offset and length in bytes, superblock features/compression configuration, tool/version, unpacked regular-file bytes and ELF counts. A corruption message blocks extraction even if fsck returns zero. The scanner walks regular files and retains RPM ownership from the extracted database. The image chain compares the independently exported sorted headers to the actual same-image RPM roster for GCC 37564293 and Official 37736448. Check the `PERF_PARTITION_SCANNED` lines for data/do_not_use, systemrw and factory_peq, including their actual /prd and /opt mapping, before declaring scope complete. Their native filesystem and ELF counts await the run.

Local regression used actual erofs-utils 1.7.1, GPTs starting at sectors 2048 and 4096, a fixture RPM database, cache reuse and a corrupted superblock. Both rosters matched the fixture. Real-image counts await the native run. [Validation log](../../artifacts/evidence/local-r0012c-validation-20261124.txt) · [Shared reader](../../artifacts/scripts/r0012c/image-tree.py.txt)

## Base, kernel and source evidence

Both LLVM SRPMs were located under `repos/base/source/<filename>`. Official `llvm-22.1.8-9.1.src.rpm` has SHA-256 `6a724a43b3ce9bfda5acdb732e8fbd969d2707b60ecb2eb5ec15b9a16950189d`; Customized `llvm-22.1.8-11.1.src.rpm` has `57cd3038e058472e1ead070a56608fc29d166f54b16afa5b5c0d1212560cc0a9`. The chain verifies the manifest `pm0011e-qb._zp0q98j/mlgo-proof-rpms.tsv` against `4b5ec62a9fcb161754e0f7179b6261254aeee35f52e2fc7fb56df4a7c7ed8231`.

The retained source diff adds six split model archives, three runtime archives, the input verifier and the default model/runtime selectors. The VD driver and regular-LTO patch declarations remain in both specs. The published rev12 source manifest and the archived fallback agree on the expected patch identity. The direct **9.1 and 11.1 SRPM member byte comparison is pending**. The sources job checks both bytes, both archive-member hashes and the model objects, exports the two SRPM spec texts as a unified diff, and compares defined model-symbol sets for ARM and accel libLLVM. The observed model symbols belong to the ARM and accel libLLVM libraries. Both clang drivers lack the symbols. Static symbol evidence alone cannot identify the loaded library for a particular compiler invocation. Retain the source-matched **Base-swap** attribution. [Retained spec diff](../../artifacts/ledger/r0012c-obs-spec.diff) · [Input hash ledger with provenance](../../artifacts/ledger/r0012c-mlgo-inputs.tsv)

| Matched QB kernel artifact | Official QB / GBS, B | Customized QB / GBS, B | Interpretation |
|---|---:|---:|---|
| uImage | 11,348,968 / 11,348,968 | 11,085,240 / 11,085,240 | Equal sizes within each lane. The recorded QB/replay SHA differs. The matched QB pair shrinks 2.32%. |
| zImage | 5,326,504 / 5,326,464 | 5,222,032 / 5,222,304 | The matched QBs shrink 1.96%. |
| Shipped perf vmlinux | 3,696,242 | 3,820,867 | Detached BTF, magic 9feb0100. |
| Linked Linux ELF | GBS measurement | GBS measurement | Replay .text −2.90%, loaded code/data −2.37%. No linked QB Linux ELF has been identified. SERET is a different image. |

GCC and LLVM carry CL 14293732 in different VCS spellings. The direct kernel SRPM check compares all member hashes including the spec. Hold the GCC kernel RPM size comparison until that result and build-input differences can be qualified. The sources job also queries perf .config, auto.conf and autoconf.h in the replay and kernel-devel RPM. Access failures are retained.

## Doc 04 and Doc 01 measurement scope

tv-viewer row 2 covers two production executables. The main .text is 4,541,188 → 2,303,342 B (GCC 4,021,208). tvcontrol-notify-manager contributes 199,476 → 115,126 B (GCC 156,784). Their sum is **4,740,664 → 2,418,468 B** (GCC 4,177,992), or **4,630 → 2,362 KB** with KB = 1,024 B. The eight-ELF, three-RPM aggregate includes six additional test ELFs, 10,760,504 → 5,005,836 B (−53.5%). The historical forceL boundary is preserved.

The decoded delivery packet contains 122 comparisons across all experiments. Its classifier labeled 65 delivered, including nine with direct argument evidence and 56 inferred solely from changed output. One showed verified delivery with no effect and 56 remained unproved. Each percentage below weights rows by bytes and uses all matched ELFs in that retained sample. Package count is the number represented among delivered rows. An output delta alone cannot establish a treatment's causal effect. [Raw counts and bytes](../../artifacts/ledger/r0012c-delivery.tsv)

| Experiment | Delivered rows / packages | Argv confirmed | No effect / unproved | Δ .text | Δ allocated | Prior Doc 01 scope and disposition for PM |
|---|---:|---:|---:|---:|---:|---|
| R1 | 10 / 6 | 0 | 0 / 2 | -35.94% | -32.36% | Original four-package production targets have their own R1 scope. |
| R2 | 9 / 8 | 3 | 1 / 12 | -0.02% | -11.94% | Six-package metadata −43.9%, alloc −11.4%. Different measure and sample. |
| R3 | 4 / 4 | 1 | 0 / 1 | +0.77% | +0.90% | Original four packages: .text −0.1%, alloc +0.5%. Check link-only treatment. |
| R4-25 | 4 / 4 | 0 | 0 / 1 | -35.46% | -21.16% | Original −23.3% at 25. Verify selected files and actual injection. |
| R4-50 | 2 / 2 | 0 | 0 / 3 | -26.71% | -15.49% | Original −14.3% at 50. Two retained rows pass the output discriminator. |
| R5 | 2 / 2 | 0 | 0 / 3 | -16.20% | -7.12% | Original .text −16.5%, alloc −8.1%, unwind +21.6%. No comparable unwind figure here. |
| R6-lld | 4 / 4 | 1 | 0 / 1 | +0.15% | +0.77% | Original lld approximately equal. Record one direct link example. |
| R6-icf | 3 / 3 | 1 | 0 / 2 | -3.53% | -2.84% | Original ICF alloc −2.3%. Record one direct link example. |
| R7 | 0 / 0 | 0 | 0 / 0 | — | — | Projected 18.83 MB. No retained treatment measurement. |
| R1-canonical | 4 / 4 | 0 | 0 / 0 | -42.75% | -38.11% | Original production .text −36.2%, alloc −25.9%. Current sum covers additional ELFs. |

For Doc 01 retain measurements alongside their original file lists. Label the recomputation as a retained-build comparison and identify the argv-confirmed subset. R2 and R6 have direct examples. R1, both R4 doses and R5 need end-to-end treatment evidence before extending their conclusions to the retained aggregate. R7 remains a projection. The decoded continuation packet SHA-256 is `929ebe824d338f43ea05c69e454a96257ef3f54ecd92f215e9c31401463a9a8a`; the delivery packet is `c5e8189a60b239b5fadfdc4221e3eb8b4f618a89ec31638b7a0764822f1ab315`.

## Step 5 • static libc preflight and replacement launcher

Base 20261113.1 primary metadata identifies `glibc-devel-static-0:2.40-1.111.armv7l` and its file list contains `/usr/lib/libc.a`. The arm RPM SHA-256 is `9618c524c413b837e439146130d346655693c31eea90f3355526a0366b87f24a`. [Base RPM](http://repos.vd.sec.samsung.net/obs220/tizen-rsa/tizen-10.0-base-dev-llvm/standard/tizen-10.0-base-dev-llvm-standard_20261113.1/repos/base/armv7l/packages/armv7l/glibc-devel-static-2.40-1.111.armv7l.rpm)

The spec now requires the static subpackage. It checks the archive before linking, lists installed glibc RPMs on failure and records the actual linker path, resolved path and version, alongside the static archive owner/hash in board-tools.json. Source bytes and compiler flags are frozen. The failed trace used /usr/bin/ld. The successful link must independently record its actual linker. Local validation exercises the real retained Base identities, missing archive/requirement, competing Product provider, and matching the static subpackage's solver line. The complete 37736448 Product list is native-only. The native launcher checks its captured digest and applies the provider gate before starting GBS. Run after the heavy queue releases its lock. Estimate 10–40 minutes, six cores, at least 24 GiB disk and Base/Product dependency traffic. A successful build returns one hashed binary for both lanes.

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
  get '0a4e9ec3592aa1fa870d7b2aa0119426a1f40220' 'artifacts/scripts/r0012c/gbs-board-bench.py.txt' 'ba8fcf9ae89d94fefef414160b82c99be7f246ab91fe4aaf4e25ae41fe0b3049'
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
