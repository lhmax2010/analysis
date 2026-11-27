```diff
-read -r -p 'Paste STATIC_GATE PASS RECEIPT <path> <sha>: ' tag gate label PM_STATIC PM_STATIC_SHA
-[[ $tag == STATIC_GATE && $label == RECEIPT && $gate == PASS ]]
+read -r -p 'Paste STATIC_GATE PASS or PM_OVERRIDE HOLD followed by RECEIPT <path> <sha>: ' tag gate label PM_STATIC PM_STATIC_SHA
+[[ $label == RECEIPT ]]
+case "$tag/$gate" in STATIC_GATE/PASS|PM_OVERRIDE/HOLD) ;; *) exit 2 ;; esac
+export PM_AUTH="$tag"
```

### TEST-ONLY Official GBS verification and test shelf

Native host, after Claude review. Run in a foreground terminal. Use `build` first and `shelve` after BUILD_RECEIPT PASS. The builder also verifies the PM decision bytes, the exact HOLD path and digest, and the operation. The shelf requires the build receipt from the same builder and same spec. Board-flash receipt status is **HOLD** for S1, S2, S11 and S12. Neither operation writes to a TV. The earlier K1/K3 perf ELF measurements stand.

```bash
(
set -eu
t=/home1/chengkai/vd-tree/workspace/temp
p=8add84d6e57d7631f885b8b3456784a9ffc7516d
d=$(mktemp -d "$t/pm0013m-launch.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0013jk/run.sh.txt" -o "$d/run"
printf '%s  %s\n' 33984865fcd39dc2beae2d46fb2b1783f1b8ca0a96833bb9b91c7b5be4d7ca29 "$d/run" | sha256sum -c -
read -r -p 'Operation (build or shelve): ' action
case "$action" in build|shelve) ;; *) exit 2 ;; esac
bash "$d/run" "$p" "$action"
)
```

At the receipt prompt paste this exact line.

```text
PM_OVERRIDE HOLD RECEIPT /home1/chengkai/vd-tree/workspace/temp/pm0013jk-static.mo1VRK/effects.json ef577b30f542286ccfe09a4297f186bc3e1c76262a03bd23ecad5e96a919563b
```

Build resource gate is 105 GiB disk, 32 GiB RAM and six cores. Estimate 30–90 minutes and repo downloads. The shelf takes seconds and writes one pending TEST-ONLY CL after the operator confirms. Submit the two test QBs only after the clean build, GCC SERET-UL check and verified shelf.
