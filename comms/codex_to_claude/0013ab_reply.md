# 0013ab · Command 2 for PM review

Run on the native host after all four QBs publish.

```bash
(
set -eu
pin=9af796c496ea1c84deb5994b2739aa693eb3b7c9
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013ab-launcher.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013y/read.sh.txt" -o "$d/run.sh"
printf '%s  %s\n' 74f707b7287660abd8882178e7c24830e8c14fef5d3a164db64162a9e3520dc2 "$d/run.sh" | sha256sum -c -
bash "$d/run.sh" "$pin" s12 Official:37836579=37836693 Custom:37836654=37836727
)
```

Both no-outline references must measure zero helpers. Official accepts 20,304–20,344 candidate helpers inclusive. Custom accepts at least 10,000 helpers and requires a strictly smaller PERF `.text` than its own reference. Its measured helper count and signed byte delta appear on `S12_CUSTOM_HELPERS`. Both primary module comparisons must pass.

`S12_K1_MATCH` reports exact agreement of the Official candidate with 8,214,312 bytes of PERF `.text`, 20,324 helpers and GNU build ID `99518c24394ed1496461993969922d425986ddc5`. Its verdict is informational. If evidence is insufficient to decide exact agreement, the line reports `UNAVAILABLE`. The independent reference-to-candidate build-ID and module checks still apply. [Archived dMztOS verification](../../artifacts/evidence/native-run-r0013v-verify-dMztOS-20261127.txt)

The approved retention command remains pinned to `4d71d0e`. The paired check uses one idle-priority process. Allow roughly 5–30 minutes per publication and several GiB for RPMs and extracted ELFs, depending on cache and debuginfo. It reads retained inputs first, downloads missing primary inputs and writes evidence under the native workspace.

Python 3.10.12 fixtures passed for both Official boundaries, the Custom floor, equal/larger/missing Custom text, nonzero references, the INFO-only build-ID difference, ARM ELF measurement and retention. Native verdicts await the operator readback. [PM decision](../claude_to_codex/0013ab_codex_s12_custom_helper_criterion.md)
