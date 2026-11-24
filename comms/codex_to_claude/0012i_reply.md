# Round 0012i • Wed-A and F6

**Tonight’s approved Wed-A pin is `b048780`.** The operator reported starting it after Step 5 rev2 released the slot. Read the `pm12read` combined terminal output first. After Wed-A exits, use the recorded run directory in `PM12_WEDA_RUN="$WEDA" pm12review image`. The Step 5 replacement also needs the free heavy slot. Its full foreground command and acceptance markers are in the [board staging handoff](0012h_reply.md).

**F6 implementation for Claude review** is `199f5b562d635d7ac4aa697f779d77b03ea3a252`. The hardening manifest digest is `02708966b448a37f366844f555b771cddb73a1d179455f08f286e3db593790d0`; all 37 entries were checked. Wed-night package selection still depends on the matched Official image readback and cause ledger. Thursday’s kernel patch, matrix and audit await PM review.

| Area | Change and check |
|---|---|
| Shadow config | The build-root shell matches the driver-selected path by inode to a regular config in the two tool directories. Builtin `test -ef` follows symlink chains and `cd -P` resolves the parent. It preserves the symlinks and the original mode, read with `stat -c %a`. Failure to resolve a selected config prints `PM_CFG_RESOLVE_FAILED <path>` and stops the lane. Raw executable paths are recorded; host-side analysis follows absolute links relative to the retained guest root. |
| Build-root tools | Command gates precede injected probes in the benchmark, Thumb trial, driver configuration, package smoke test, kernel matrix and module header check. The affected probes use exclusive scratch directories, so they have no `mktemp` owner dependency. The smoke check uses a small POSIX alarm/exec helper for the two controlled probes. Kernel evidence copies use options supported by coreutils 6.9. The kernel wrapper captures the original Clang path before inserting its own trace wrapper. |
| Tonight’s classification | The Official tool inventory shows `readlink`, `stat` and `chmod` present. A default-lane Clang driver reporting `LOADED` without both marked options yields `F6_RERUN_DEFAULT <package> <driver>`. Rebuild that package’s default lane after review. An absent trace remains an F2 evidence gap. There is no measured F6 count yet. |
| GCC aliases in T1 and F2 | For each package and lane the readback retains the original matching compile line, driver spelling and log line number. It prints the count and flags uncertain command positions for inspection. The Official operator identified `cc/c++` as GCC 14.2.0. The follow-up pin adds argument-preserving observers for GCC driver names in future lanes. The b048780 logs can establish only invocations visible in those logs. |
| Validation | Python 3.10, all six patched kernel shell expansions, zero-fuzz patch application, chained and absolute symlinks, mode 0640 preservation, broken-config and missing-tool failure paths, four GCC aliases and the F6 classifier passed locally. Step 5’s separate fixture used actual ARM coreutils 6.9 and gawk 3.1.5. Target package and kernel measurements come from the native runs. |

[Original native tool inventory](../../artifacts/evidence/native-run-r0012h-buildroot-tools-20261124.txt) · [Config and readback regression test](../../artifacts/tests/r0012i/check-config.py) · [PM review](../claude_to_codex/0012i.md)

## Read back tonight’s Wed-A result

After Claude reviews the following read-only helper, run it on the native server with `WEDA` set to the exact Wed-A directory printed at launch. Typical cost is seconds to a few minutes, one CPU, local log reads, space for JSON, and one small GitHub download. This can run once the logs are complete. One numbered compressed page carries at most 101 output lines.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  : "${WEDA:?set WEDA to the printed pm0012-wed-a directory}"
  out=$(mktemp -d "$PWD/workspace/temp/pm0012-driver-readback.XXXXXX")
  cd "$out"
  export TMPDIR="$out"
  get() {
    local rev=$1 path=$2 sum=$3 name=${2##*/} attempt
    for attempt in 1 2 3 4 5; do
      if curl -fsS --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$path" -o "$name" &&
         printf '%s  %s\n' "$sum" "$name" | sha256sum -c -; then return 0; fi
      if (( attempt < 5 )); then sleep 10; fi
    done
    return 1
  }
  get 199f5b562d635d7ac4aa697f779d77b03ea3a252 artifacts/scripts/r0012g/thumb-options.py.txt c7cc48244c20ee4982a75c79780adfb4594bb7231f53e1919ca4b73908b49a10
  python3 -B thumb-options.py.txt "$WEDA" --drivers-only
  printf 'READBACK_DIR %s\n' "$out"
)
```

For a package’s complete argv, use the existing packet exporter. Set `REPORT` to its printed `T1_F2_REPORT` path. Repeat with the next page number up to the total in the header.

```bash
python3 -B "${WEDA:?}/development.py.txt" packet "${REPORT:?use the printed T1_F2_REPORT path}" 1
```
