# 0012a reply • Source1005 independent review

The full patch, its three original parts and the verbatim review prompt are in the repository. The patch is 944 lines. Its SHA-256 is `7d89083453e1d75707a4a6b3a6d9510a4c31e09d8e99865de2a18e07945bf76f`. The prompt SHA-256 is `925199f30e857543401ea3f240ea18b1eb82069df7312abdff2807cbae361be2`. The [review directory](../../reviews/lto-nonpic-fallback/README.md) has the review output convention.

**Shipped source.** The retained Official OBS Source1005 matches byte for byte. The Customized rev12 OBS source-directory check matched the complete pinned manifest, including the identical Source1005 MD5. Both retained exact specs apply Source1005 with `--fuzz=0`. The readback binds rev12 to the published clang binaries. Neither exact SRPM payload was available in the local workspace. If the 0011f `3-qb-srpm` job succeeds, compare the two members directly before describing the packages as byte-verified. There is no differing shipped copy in the evidence reviewed so far. [Published rev12 pin](../../artifacts/evidence/native-run-r0005-20261118.txt)

**Extra test.** The patch adjusts the existing upstream `wrap-unreferenced-before-codegen.test` expectations for the fallback's GOT access to `__emutls_v.x` and expresses the section-index check symbolically. The wrapper assertions remain. The upstream test came from the 2022 lld fix for wrapping symbols generated during LTO codegen, commit `1af25a986069`. The Tizen patch contains no lld implementation hunk. [LLVM review D124056](https://reviews.llvm.org/D124056)

## Native workspace copy

After review, run on the native server. This downloads 45,397 bytes from GitHub, takes seconds plus retry time, and writes one patch under `workspace/patches`. A pre-existing copy is checked without overwriting it.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree/workspace
  mkdir -p patches
  target=patches/lto-nonpic-in-pic-output-fallback.patch
  expected=7d89083453e1d75707a4a6b3a6d9510a4c31e09d8e99865de2a18e07945bf76f
  url='https://raw.githubusercontent.com/lhmax2010/analysis/8b17b91ee39bc71d617a875d878ee231a3e644ad/artifacts/patches/lto-nonpic-in-pic-output-fallback.patch'
  if [[ ! -e "$target" ]]; then
    scratch=$(mktemp patches/.lto-source1005.XXXXXX)
    trap 'rm -f -- "$scratch"' EXIT
    ok=0
    for attempt in 1 2 3 4 5; do
      if curl -fsS --connect-timeout 15 --max-time 120 "$url" -o "$scratch" &&
        printf '%s  %s\n' "$expected" "$scratch" | sha256sum -c - >/dev/null; then
        ok=1
        break
      fi
      printf 'DOWNLOAD_FAILED attempt=%s/5 Source1005\n' "$attempt" >&2
      if ((attempt < 5)); then sleep 10; fi
    done
    [[ "$ok" == 1 ]]
    ln -- "$scratch" "$target"
  fi
  printf '%s  %s\n' "$expected" "$target" | sha256sum -c -
  sha256sum "$target"
)
```

## Exact SRPM payload readback when 0011f has the inputs

Set `BATCH_DIR` to the printed Tuesday batch directory. This runs read-only, requires the native `rpm2cpio` and `cpio`, and prints only the Source1005 evidence for the two lanes. Decompression uses one process per tool, serial by lane, no network and no extra disk. A mismatch reserves the affected copy for independent review after the exact bytes are retrieved.

```bash
(
  set -euo pipefail
  log="${BATCH_DIR:?Use the printed r0011f BATCH_DIR}/3-qb-srpm.txt"
  mapfile -t proof < <(awk '$1=="MLGO_PROOF_RPMS" {print $2, $3}' "$log")
  [[ ${#proof[@]} == 1 ]] || { echo 'SOURCE1005_SRPM_UNAVAILABLE'; exit 2; }
  read -r roster digest <<<"${proof[0]}"
  printf '%s  %s\n' "$digest" "$roster" | sha256sum -c -
  expected=7d89083453e1d75707a4a6b3a6d9510a4c31e09d8e99865de2a18e07945bf76f
  while IFS=$'\t' read -r lane kind rpm sha; do
    [[ "$kind" == llvm && "$rpm" == /home1/chengkai/vd-tree/workspace/* ]] || exit 2
    printf '%s  %s\n' "$sha" "$rpm" | sha256sum -c -
    mapfile -t matches < <(rpm -qpl "$rpm" | awk -F/ '$NF=="lto-nonpic-in-pic-output-fallback.patch"')
    [[ ${#matches[@]} == 1 ]] || { printf 'SOURCE1005_MEMBER_NOT_UNIQUE %s\n' "$lane"; exit 2; }
    actual=$(rpm2cpio "$rpm" | cpio -i --quiet --to-stdout -- "${matches[0]}" "./${matches[0]#./}" | sha256sum)
    actual=${actual%% *}
    if [[ "$actual" == "$expected" ]]; then outcome=MATCH; else outcome=DIFFERS; fi
    printf 'SOURCE1005_SRPM %s %s %s %s\n' "$lane" "${rpm##*/}" "$actual" "$outcome"
  done < <(tail -n +2 "$roster")
)
```
