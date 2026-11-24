# 0012b reply • Step 5 benchmark source and overnight queue

The fixed [benchmark builder](../../artifacts/scripts/r0012b/gbs-board-bench.py.txt) is pinned to `abd1546447dd7c8f0765301117a5b7527a5d8714`, SHA-256 `e816a4feb40eb8f5786e137a7eed30d2a0a037acc0959269dceae7a35c12e7a6`. It puts `bench.c` in `packaging/`, declares it as `Source0`, and copies RPM’s staged source into the build directory during `%prep`. The failed directories remain available for evidence.

I ran the exact generated spec with `rpmbuild --nodeps -bb` in a clean local build tree containing only `SOURCES/bench.c`. The log shows `%prep` copying it, the checksum of the original C source, the static link completing and the RPM containing `/usr/bin/pm-board-microbench`. The fixture used host GCC and an RPM-owner shim to test file staging and proof parsing. Its output does not stand in for the native armv7l binary. [Local build log](../../artifacts/evidence/local-r0012b-step5-rpmbuild-20261124.txt)

The benchmark keeps `-O2 -static -std=c11 -Wall -Wextra -Werror` and records an additional link map. `board-tools.json` records those flags, the in-root compiler, the actual ISA of `main` from its ARM symbol, the linked image’s ISA summary and the frozen binary SHA-256 used for both board lanes. The static gate checks that the ELF has neither an interpreter nor a needed shared library. The link map, archive SHA-256, installed RPM owner and matching Base download line establish the actual `libc.a` provenance on the successful rebuild. The failed native log already shows that the solver downloaded `glibc-devel-2.40-1.111.armv7l.rpm` from Base 20261113.1. Linking the rebuilt ARM binary against it remains to be confirmed by `GBS_BENCH_GLIBC_ORIGIN BASE_PROVEN_FROM_GBS_DOWNLOAD`. Record `BASE_ORIGIN_REVIEW` if the download line is missing. [Native failure and dependency log](../../artifacts/evidence/native-run-r0011e-step5-bench-fail-20261124.txt)

| Archived native input | SHA-256 |
| --- | --- |
| [Step 5 failure transcript](../../artifacts/evidence/native-run-r0011e-step5-bench-fail-20261124.txt) | `e60e3942b263b9be6fbbcd4e2181c09d46e32ab3a8b0bae9ac7762d2fead256e` |
| [Overnight launcher rev1](../../artifacts/evidence/native-cmd-r0011f-diagnostics-and-overnight.sh) | `4e583ea8299f171f2004a8603e54d41ab4d21b1a6a9eb1412afcd0366b21abeb` |
| [Overnight launcher rev2](../../artifacts/evidence/native-cmd-r0011f-diagnostics-and-overnight-rev2.sh) | `77680b779bdac8daa2a1bfad403638e8c8ca83a87caf24faebc8f48af09f1102` |

The rev2 worker and its 11 pinned inputs match rev1 byte for byte. Its launcher guard watches for active heavy work and releases the dependency on `BOARD_TOOLS`. Use rev2 for the board-free diagnostics. Current native execution status awaits a returned `BATCH_DIR`. Run Step 5 after rev2 finishes and the shared lock is free. Claude review of the replacement pin is pending.

## Step 5 on the native server

Use one attended foreground GBS build, 10–40 minutes, up to six cores, a 24 GiB scratch allowance plus the shared reserve, and pinned Product/Base dependency traffic. The command matches the existing Step 5 launcher with the benchmark pin updated. A successful run prints `GBS_BENCH_READY`, `GBS_BENCH_ISA`, `GBS_BENCH_STATIC_GLIBC`, `GBS_BENCH_GLIBC_ORIGIN` and the new `BOARD_TOOLS` path. Keep that path for both lanes.

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
  get 'abd1546447dd7c8f0765301117a5b7527a5d8714' 'artifacts/scripts/r0012b/gbs-board-bench.py.txt' 'e816a4feb40eb8f5786e137a7eed30d2a0a037acc0959269dceae7a35c12e7a6'
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
