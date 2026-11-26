```bash
(
  set -eu
  cd /home1/chengkai/vd-tree/workspace/temp
  d=$(mktemp -d "$PWD/pm0013f-get.XXXXXX")
  pin=985a3ae403108831edc0e0c17b2173ed9dac0919
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 150 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013f/run.sh.txt" -o "$d/run"
  printf '%s  %s\n' 8cf27272747dd785a41c49d448eae089d7ca3fdd44cef3f30fe90155cce626c8 "$d/run" | sha256sum --check --status
  bash "$d/run" "$pin"
)
```

Native host, after PM review. One worker, nice 19, idle I/O class. Allow roughly 30 minutes to several hours depending on contention. The snapshot readers check the existing 50 GiB reserve plus partition scratch. The run retains the new Official platform tree for 0013g. Network is limited to missing pinned scripts, reader RPMs, Official AVControl inputs, and the subset of published RPMs with relocatable objects or static archives found through the repository file lists. Stage output, error logs and the export stay in the newly printed workspace run. No build or lock acquisition.

**USB export.** Set `TABLES` to the absolute path on the final `TABLES` line and `USB` to the mounted stick. This creates one uniquely named archive and reads the copy back.

```bash
( set -eu; : "${TABLES:?absolute path on TABLES line}" "${USB:?USB mountpoint}"; mountpoint -q "$USB"; src=$(realpath -e "$TABLES"); dest="$USB/$(basename "$(dirname "$src")")-tables.tar.gz"; test ! -e "$dest"; cp -- "$src" "$dest"; h=$(sha256sum "$src"); printf '%s  %s\n' "${h%% *}" "$dest" | sha256sum -c - )
```

| Retained measurement | Result |
|---|---|
| Platform | Both platforms returned errno 39 at `modules`. The one-line exceptions do not identify the first failing operation. The rootless extractor previously retained image permission bits and used automatic recursive cleanup. The replacement uses fresh roots, normalizes operator access without following links, records the failing phase separately, and requires the walked count to equal the vendor dump count. |
| Product partitions | GCC and old Official each yielded 902 entries, 529 compressed and 167 ELFs. GCC board sample matched. Official product board hashes remain outstanding. |
| AVControl | Reference/default/package .text = 736,944 / 441,362 / 179,660 B. Default and package each retain 88 mapped A32 bytes. The evaluator anchors the shipped ELF to `fa474d0e…` and tries the pinned RPM as well as extracted files. A linker map or symbol interval must agree before a stub is named. Every residual REVIEW receives its own line. Passing still requires all original treatment gates. |
| Published inventory | 6,770 RPM identities, four scan errors. The 2,172 marker-bearing sources include linked-in runtime code. E1 now records producer, CU path and source-ownership evidence, separates CRT, and reports the fixed-27 statuses and byte counts. The fallback inspects actual ARM relocatable objects for GCC and the absence of Clang. A package-qualified file symbol or object path must support attribution. Object-only counts and bytes are separate from CU-qualified linked ELF totals. Missing producer evidence stays unproved. The byte metric is the .text of ELFs containing own GNU C/C++ CUs; mixed-producer ELF bytes cannot be apportioned by CU from these records. |
| Relocations | The prior 8,145,714 relative relocations span the published inventory. E6 now joins installed path and SHA to that inventory and gives REL bytes, estimated RELR bytes, savings, top 20 and unmatched count. The saving applies to relocation metadata. A separate check reads the actual ARM interpreter, joins its SHA to glibc and tests eight relocated data words using the image's own Python and loader under QEMU. Unavailable prerequisites yield UNPROVED. |

The raw transcript was archived byte for byte with SHA-256 `e47544f21f8fd65368e4f2cf1ddd1a2f27536cd1d83d61f9e7ca539f5d8edeea`. Python 3.10 parsing, the read-only directory/symlink cleanup fixture, source ownership checks and shell syntax passed locally. New platform counts, gate decisions and loader behavior require the native return. The run emits the full tables as one compressed tar.
