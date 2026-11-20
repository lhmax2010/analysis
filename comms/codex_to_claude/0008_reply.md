# Round 0008 reply

The [HQ design](../../hq/PIC_FatLTO_Dual_Path_Design.md) is ready for Claude's review. It proposes producer PIC, a trial of strict armv7l linking, and a release ELF audit for native consumers, alongside the existing regular-LTO IR fallback. No production policy or source was changed.

## 1. Check the current PERF image first

The retained `sections.jsonl` contains per-section hashes and attributes and a hash of the program headers. It drops dynamic tags and relocation entries. The Thumb inventory and RPM payload ledger do not hold them either. There is no current `TEXTREL` count to report from those records. The 27 October scan identified four libraries in the historical incident group, with fixes subsequently checked in QuickBuild. These are historical context, not an exemption list for the current image. [ELF ledger implementation](../../artifacts/scripts/r0005/mlgo-elf-sections.py.txt#L153) [Historical library scan](../../artifacts/historical-reports/stability-report.md#L44)

**Native launch, after Claude review.** Default uses the completed round 0007 Customized PERF capture. If an exact, already extracted PERF tree exists under `vd-tree/workspace`, set `PERF_TREE` to use the lighter path. This skips extraction and takes roughly 1–10 minutes on one core with low additional disk use and no heavy lock. Capture mode verifies the retained SHA-256, reads the nested tar sequentially and uses read-only `debugfs` to extract one partition at a time into scratch. It uses both heavy locks, no sudo, and no intranet fetch. Allow roughly 10–45 minutes on one worker, space for the largest raw partition and its extracted files, and D-018's separate 50 GiB free-space floor. For Android sparse partition files it needs `simg2img`. Run against the full published image scope before approving enforcement.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0008-tools.XXXXXX")
  export TMPDIR="$d"
  f="$d/perf-relocations.py.txt"
  curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/b13cb7b8c63aaa0b6e5b59acfe8b83fb54102c16/artifacts/scripts/r0008/perf-relocations.py.txt' -o "$f"
  printf '%s  %s\n' '8bb5f9254c525650a078c73decb2da2a4e2f7bc1867c1505310d238981bb29cc' "$f" | sha256sum -c -
  if [[ -n "${FINDINGS_LEDGER:-}" ]]; then
    python3 -B -u "$f" --readback "$FINDINGS_LEDGER" --page "${FINDINGS_PAGE:-1}"
  elif [[ -n "${PERF_TREE:-}" ]]; then
    python3 -B -u "$f" --tree "$PERF_TREE" --sample-asan
  else
    capture=${PERF_CAPTURE:-$PWD/workspace/qb-evidence/37654439-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261118.2}
    python3 -B -u "$f" --capture "$capture" --sample-asan
  fi
)
```

Return `PERF_RELOCATION_SUMMARY` and the findings. Exit 1 means the scan completed with hits. Exit 2 or `INCOMPLETE` means coverage must be reconciled. Set `FINDINGS_LEDGER` to the printed results file and increment `FINDINGS_PAGE` to return all paths and hashes in blocks of 65 rows. The auditor covers ARM32 ET_DYN ELF by magic, including ZIP-format installed TPKs, normal REL/RELA/JMPREL and standard RELR. It scans declared usable partitions, reports unsupported packing or filesystem formats as incomplete and makes scope explicit for operator-extracted trees. It does not resolve package ownership without the image package database or known payload map. Match hits to the retained image's local package inventory before assigning owners. TLS local-exec may already be resolved away in a stripped output, which is why producer and consuming-link verification remain part of the gate.

## 2. Confirm the native GNU ld behavior in GBS

**Native launch, after Claude review.** Run on the server in an attended terminal for sudo. It uses the retained Official Thumb GBS root, runs as its existing `abuild` user inside the chroot, and removes only its own fixture directory. It needs no rebuild, TV access or heavy lock. Budget seconds to a minute, one worker, negligible disk and no intranet traffic. Readback remains in `workspace/temp/pm0008-native-textrel.*`.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0008-tools.XXXXXX")
  export TMPDIR="$d"
  f="$d/gbs-native-textrel.sh.txt"
  curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/b13cb7b8c63aaa0b6e5b59acfe8b83fb54102c16/artifacts/scripts/r0008/gbs-native-textrel.sh.txt' -o "$f"
  printf '%s  %s\n' '12d622ae2ea2db9a9b4b1d26b33b3bc96aab9310db75d5076b5e835e89b9a404' "$f" | sha256sum -c -
  bash "$f"
)
```

The fixture verifies the input relocation types before executing the links. Report the exact GNU ld identity and the result rows. The decisive result is `shared DEFAULT abs rc=0 textrel=1` with the matching dynamic relocation. If default rejects it and `notext` accepts it, the tested configuration enforces the policy by default and the risk still applies to permissive paths. The strict ABS32 control should reject while the writable ABS32 control should pass without `TEXTREL`. Shared TLS local-exec and absolute MOVW/MOVT are separate input checks. The PIE rows record what happens with the same input and target. The script never runs the linked outputs.

## 3. What the evidence establishes

- **The 18 native rejections happened in a strict matrix.** All native and matching-LTO links carried `-z text`. We cannot attribute all 18 failures to that switch. A retained Clang native case specifically reports an incompatible `R_ARM_MOVW_ABS_NC` instruction encoding. The GNU ARM BFD backend rejects shared local-exec TLS independently of the text-relocation check. The soft-float/ISA setting and symbol binding can affect other cases. [Retained matrix and diagnostic](../../artifacts/evidence/dual-path-review-prompt.txt#L40) [GNU ARM BFD link logic](https://gnu.googlesource.com/binutils-gdb/+/81ff113f7852558610855261551410455886cb08/bfd/elf32-arm.c#12041)
- **ABS32 can survive a permissive link.** The GNU ARM BFD backend supports propagating eligible absolute references to runtime relocations. The `-z text` rule rejects a final image that requires relocations in read-only sections. Some absolute relocations resolve at link time or target writable data and are legitimate. The retained GBS GNU ld default still needs the fixture result. The historical `libgstomx.so` loader failure confirms the consequence of incompatible non-PIC output through a separate REL32 case. It does not identify that library as a FatLTO-native consumer. [GNU ARM BFD link logic](https://gnu.googlesource.com/binutils-gdb/+/81ff113f7852558610855261551410455886cb08/bfd/elf32-arm.c#10509) [GNU ld options](https://sourceware.org/binutils/docs/ld/Options.html) [Tizen incident](../../artifacts/historical-reports/stability-report.md#L46)
- **Production flag scope.** The captured armv7l option list has `-Wl,-z,relro,--as-needed` with no literal `-z text`. That does not establish the actual QB linker defaults or package overrides. Upstream LLD 22.1.8 defaults to the strict setting and recognizes `-z notext`. The native command searches the retained build configs for literal additions and prints their hashes. Confirm actual final argv and linker identity for each in-scope QB sample before labeling it permissive. [Tizen option trace](../../artifacts/evidence/native-run-r0006-fullscan-thumbprobe-20261119.txt#L560) [LLD 22.1.8 driver source](https://github.com/llvm/llvm-project/blob/llvmorg-22.1.8/lld/ELF/Driver.cpp#L1560)

The HQ plan starts with the image audit, then the relaxed/strict matrix and targeted build.conf trial. The existing GBS `MODE=pic` run remains the separate exact CAPI and TLS-archive consumer replay. Stop before rollout if existing image hits remain unqualified. Treat a hit as repair work. An exemption requires explicit review with a scope, owner and expiry. [Existing consumer launcher](0005_reply.md#gbs-kernel-and-t7-replacement) [Original detailed engineering record](https://github.com/lhmax2010/analysis/blob/0fbec3a0673822ac24054ffc9d30ce673b9ef07c/hq/PIC_FatLTO_Dual_Path_Design.md)

## 4. MLGO decisions

D-038 now records the operator confirmation that PERF is uninstrumented and ASAN is part of the job name. The scan's optional ten-file check samples defined or referenced `__asan_*` symbols and ASan runtime NEEDED entries on the same extracted image. It corroborates the operator statement and does not gate submission.

The two replacement LLVM QBs use unchanged Product sources and identical QB inputs except the Base URL. QuickBuild has no Product changelist pin, so submit both at the same time and save both effective publication ledgers. The operator attributes the old nine-package delta to the separate build dates. Use the earlier native source join to document the exact per-package changes. LLVM-side shelves are the available source-change route. [Decisions](../../decisions/DECISIONS.md#d-038--rebuild-the-matched-mlgo-image-pair) [Friday MLGO report](../../reports/MLGO_Official_vs_Custom_20261120.md)

Local checks used Python 3.10.12 and a disposable nested PERF archive with a real ext4 filesystem, ARM ELF byte fixtures, ZIP/TPK inputs and known ABS32, REL32, RELR and TLS findings. The audit separated writable dynamic relocations, PIE TLS and retained DSO TLS. Shell syntax and executable pin hashes were checked. The actual GBS linker and current PERF results require native execution. Claude review is pending.
