# Round 0012h • Step 5 benchmark staging

**Claude review requested for the replacement foreground launcher.** Official QB 37736448 linked the static benchmark with GNU ld 2.43. The unavailable `realpath` then left the libc path empty and stopped RPM packaging. The 59-line transcript matches SHA-256 `1598dd6f4b974fcdec986b9f63147892f6e18d5a5950e7ae3d4cdd7e26222204`. [Native evidence](../../artifacts/evidence/native-run-r0012c-step5-bench-realpath-fail-20261124.txt)

## Replacement Step 5

Run on the native server, in a foreground terminal after Claude reviews the pin. Allow 10–40 minutes, one GBS job, one build thread, affinity up to six cores. The capacity gate requires 74 GiB free disk and 28 GiB available RAM including reserves. Downloads are the pinned scripts and Base/Product dependencies. This stages a fresh tools directory under vd-tree. The first proof is seven `OFFICIAL_TOOL_FILE` rows and `PM_BENCH_FIXTURE_PASS` before `GBS_START`. Board measurements can use the benchmark after `GBS_BENCH_READY` and the final `BOARD_TOOLS`. Use that directory and its one binary digest for both images.

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
  get '9c65ec5bc7c55b3bdf62ff11b36ad4834e141a22' 'artifacts/scripts/r0012c/gbs-board-bench.py.txt' '0159982a99f3fa50dc2a2459d922e8aaaa62cdd0c22d716e8ff01b85bf628a88'
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

## What changed and what was tested

- Builder commit `9c65ec5bc7c55b3bdf62ff11b36ad4834e141a22`, SHA-256 `0159982a99f3fa50dc2a2459d922e8aaaa62cdd0c22d716e8ff01b85bf628a88`. Only the builder line changed in the rev2 command. The Official capture digest, benchmark C source, flags, GBS helpers and board scripts retain their pins.
- The new preflight obtains the exact tool allowlist from checksum-verified Base RPM file lists for the five providers in the Official installation log. Inside GBS the spec checks the installed file records and `command -v` before compilation. It resolves physical parent directories using shell builtins, preserving the filename and original map spelling for evidence.
- Local Python 3.10.12 executed the RPM-expanded build body with the seven Official tool names on PATH. Real ARM gawk 3.1.5, sha256sum 6.9 and tail 6.9 ran under QEMU from a local GBS root. Target compiler, linker, readelf and rpm responses were test doubles. Each of seven missing-tool tests failed before the compiler ran. The portable expansion used by the native preflight matched `rpmspec -P`. [Fixture](../../artifacts/tests/r0012h/bench-fixture.py) · [Official path and provider input](../../artifacts/tests/r0012h/official-owner-readback.tsv)
- The operator observed all seven paths and supplied the provider identities. The displayed host ownership query targeted a nonexistent user RPM database. The release numbers also appear in the earlier installation log. The new run emits ownership directly from the RPM header lists and rechecks inside the build root. [Installation transcript](../../artifacts/evidence/native-run-r0011e-step5-bench-fail-20261124.txt)
- The old map proves that Clang found libc.a through the ARM GCC 14.2.0 search directory. The `9618c524…` digest belongs to the provider RPM. The new receipt verifies the linked archive against the same member extracted from that pinned RPM, records both digests, and records the search path, physical directory and GCC-directory match for each startup object and libc.a. CRT rows, final ISA, ELF hash and `board-tools.json` await the real GBS run. [Builder](../../artifacts/scripts/r0012c/gbs-board-bench.py.txt)
