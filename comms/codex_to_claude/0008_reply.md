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

## Round 0008a native results

**HQ first.** The Customized 37654439 capture is complete. The default PERF scan now has its input. Run it first and then the GNU ld probe. The 1,778,887,419-byte archive SHA-256 is `a809c4fb597ac42ea0479e80bc6fa972e45a8a061ea64f0358dca6b988bf7d67`. Four kernel RPMs and 5,880 Product identities were retained. The PERF archive’s USB flash format remains unverified. This transcript does not contain the two HQ runs. [Native capture](../../artifacts/evidence/native-run-r0007-capture-preflight-readbacks-20261120.txt#L25)

**The published build.conf mismatch matters.** All four Base indices returned 200, all five pins matched, and the staged GBS config diff passed after buildroot normalization. Official published build.conf SHA-256 `98690f23…` is `@14452507`. Customized `0e352a44…` matches the retained Product `@14431365` digest. The archived P4 diff shows one edited configuration line between those revisions. The newer revision removes five names from `%lto_uncompatible_pkgs`. Four coincide with the positive-growth ELF group: swu, liballshare-core, nagsam-mw and ug-hbbtv-efl. The fifth is ci-module. The change affects LTO eligibility. Effective LTO requires package argv or link evidence. Use `@14452507` and the same shelf list on both replacement QBs, started together with only the Base URL changed. The native diff prints both publication versions and the exact retained file diff. [Native preflight](../../artifacts/evidence/native-run-r0007-capture-preflight-readbacks-20261120.txt#L58) [Archived P4 diff](../../artifacts/evidence/clang-buildconf-14431365-to-14452507-20261120.diff.txt)

**GCC and Clang options.** Both Product configs preinstall and run the GCC force-options helper. The matching GBS root proves download, preinstallation and postinstall of `gcc-warning-build-env-14.2.0-4.1` from the Official Base. The generated driver appends Thumb and other options for ordinary GCC invocations that cross this path. Package exemptions and the `__KERNEL__`/`-nostdlib` escape still apply. The C versus C++ list difference is `-Wdeprecated-copy` in place of four C-only warnings. The identical Base OBS configs omit force-options initialization, so the Product wrapper is outside the default Base glibc environment. A no-flags ELF from unwrapped Base GCC would confirm its actual ISA default. The tested Product Clang config contained three lines and no equivalent force-options block. The updated RPM query uses an explicit build-root database path. [Wrapper and GBS package evidence](../../artifacts/evidence/native-run-r0007-capture-preflight-readbacks-20261120.txt#L119)

Both Base snapshots publish `clang-force-options-1.0.0-1.1`. The published Product and Base configs omit preinstall for it. The archived 10.0 Base source shows that postinstall makes the bindir writable and adds macros to `tizen_macros`. The `%__spec_build_pre` hook calls `%clang_force_incompatible`, which writes a marked block to `clang.cfg` and `clang++.cfg`, honors package exemptions and cleans up in `%__spec_build_post`. Its default is `%{optflags}` plus `-Wl,-z,relro,--as-needed -Wl,-O1 -Wl,--hash-style=gnu`. The `%clang_force_options` override can limit it to `-mthumb` for option (a). Explicit arguments retain precedence, so the helper cannot implement option (b)'s semantics. Verify prefixed-driver and accelerator config forwarding and read both exact RPM payloads via the native `helpers` action. The omission of ASan helpers corroborates the operator's statement. The PERF scan includes the independent spot-check. [Snapshot helper inventory](../../artifacts/evidence/native-run-r0007-capture-preflight-readbacks-20261120.txt#L194) [Clang config documentation](https://clang.llvm.org/docs/UsersManual.html#configuration-files)

**Nine changed packages.** All nine match on NEVRA, SRPM and P4 VCS. Changelogs were unavailable in the default readback. Effective LTO, changed Base inputs, compiler differences and build variability remain separate possible contributors. The matched rebuild controls the identified configuration difference and reduces time drift. Base-dependent differences can still appear. The package readback joins checksummed metadata and P4 packaging, and flags unresolved conditional BuildRequires and provider ambiguities. It screens SHA-verified Customized swu and liballshare-core ELF .symtab and .comment. Optional selected Base archives provide symbol-name overlap evidence. Flag presence in a recipe or a symbol-name match requires effective argv or a link map for attribution. An optional Official local GBS RPM tree provides .comment controls where they exist. The 4,777 .comment and 65 .rodata byte changes apply to the .text-identical subset. The release suffixes alone do not identify the differing comment strings. [Source join and byte counts](../../artifacts/evidence/native-run-r0007-capture-preflight-readbacks-20261120.txt#L204) [Friday report](../../reports/MLGO_Official_vs_Custom_20261120.md)

**Kernel and BTF.** Of the 115 `tztv-kernel-perf` members per lane, 105 change hash and ten match. The section scan separately found 60 changed external-module .text rows. The first 35 changed owners cover only 49 of those rows. Effective advisor usage requires actual external-module argv. The new modules action counts the full list and checks nominated retained logs. The detached GBS BTF gained 2,421 FUNC, 1,497 FUNC_PROTO, three PTR and one CONST records. The +75,928 type bytes equal the published type delta. The increase is consistent with more represented out-of-line functions. It does not quantify individual inlining decisions. The packaging spec explicitly creates and installs a detached rootfs blob. The GBS linked section readbacks expose no .BTF. The added kernel readback prints linked .BTF rows and the actual PERF `CONFIG_DEBUG_INFO_BTF` value if the generated config was retained. [Module evidence](../../artifacts/evidence/native-run-r0007-capture-preflight-readbacks-20261120.txt#L222) [Detached BTF](../../artifacts/evidence/native-run-r0007-capture-preflight-readbacks-20261120.txt#L295)

### Additional pinned launchers for Claude review

**Configuration, exact helper RPMs and package forensics.** On the native server, use the default `config` first. It reads the checked publication files in seconds, with negligible disk/CPU and no intranet transfer. `FORENSICS_MODE=helpers` reads both exact Base helper RPMs in seconds to a minute, with small transfers and no install or scriptlet execution. Use `FORENSICS_MODE=packages` after the HQ scan and fixture. Allow minutes to tens of minutes depending on the P4 queries and transferred RPMs, one worker, hundreds of MiB of network and scratch depending on candidate inputs. It takes a valid P4 ticket. Source or RPM errors are reported per package. Use `FORENSICS_ARGS=(--archive-provider name --official-gbs-root /home1/chengkai/vd-tree/workspace/temp/retained-root)` only when those inputs are known. Other provider names may be appended up to a limit of three. If the retained configuration diff exceeds one page, add `--page 2` to `FORENSICS_ARGS`.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0008a-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 file=$2 digest=$3
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$file" -o "$d/${file##*/}"
    printf '%s  %s\n' "$digest" "$d/${file##*/}" | sha256sum -c -
  }
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/qb-forensics.py.txt' '6bc8e1bbff0a98ff7096ea7ad1806f777fa63aec04c0b9dc2a92fe256294dd82'
  get 'd3cea65aac76d438b82b55a2857a5ee18546edad' 'artifacts/scripts/r0005/image-repo-lib.py.txt' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
  get '3e96bc410252a5b3922c0f51f5ed0218852f4feb' 'artifacts/scripts/r0005/mlgo-elf-sections.py.txt' '54a35e35c1844ca4d5cff60e6236d76698fe27f4f582347ed544249c146c34fd'
  python3 -B -u "$d/qb-forensics.py.txt" "${FORENSICS_MODE:-config}" \
    "$d/image-repo-lib.py.txt" "$d/mlgo-elf-sections.py.txt" "${FORENSICS_ARGS[@]}"
)
```

**Wrapper, module and BTF config readback.** Native, no build or intranet transfer. Default fixes the root RPM database query. Set `BUILD_READBACK=kernel-isa` for the retained PERF .config and linked BTF check, or `BUILD_READBACK=modules` for the exact external-owner count. For effective advisor flags pass `BUILD_ARGS=(--module-log-dir /home1/chengkai/vd-tree/workspace/temp/retained-module-logs)` with the actual retained module-log directory. If it is unavailable, report the count and leave the effective flags unclassified. Expected seconds to a few minutes, one worker and no additional data files beyond the launcher.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0008a-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 file=$2 digest=$3
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$file" -o "$d/${file##*/}"
    printf '%s  %s\n' "$digest" "$d/${file##*/}" | sha256sum -c -
  }
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/native-build-readback.py.txt' '9fe720021b649c3a5fa6c603c7c22c70e29e49a523aea3f40d6b263357bc6410'
  python3 -B -u "$d/native-build-readback.py.txt" "${BUILD_READBACK:-wrappers}" "${BUILD_ARGS[@]}"
)
```

**Future GBS runs.** These commands supersede the expired-dependency entry points. On the native server, `GBS_MODE=pic` is the default for the exact CAPI/TLS archive probes. The dependency URL defaults to the captured 37654439 publication as a stand-in. Set `PRODUCT_URL` to the reviewed replacement Product URL when the new jobs finish. A 404 or unexpected URL aborts before P4 source staging or a GBS build. The stand-in cannot recreate the expired Official dependency universe. Archive hashes still have to match for exact-member acceptance.

Use `GBS_MODE=sample` with `THUMB_PACKAGE` for the known source pins. That mode stages only unless `RUN_GBS=1` is exported. Use `GBS_MODE=thumb` with `THUMB_MODE=defaults`, `sample` or `pair`. For sample or pair, put the original `--source`, `--revision`, and `--spec` arguments in `GBS_ARGS`. Pair also takes the reviewed `--package`, `--elf` and `--cause-ledger` arguments. Use fresh roots after changing dependencies. An optional `GBS_MODE=kernel` uses the supplied Product in both lanes unless a reviewed `--custom-dependency-product-url` is passed in `GBS_ARGS`. The build config stays at the pinned `@14452507` for these replays. The launchers retain D-018 headroom, one GBS worker on up to six CPUs and both heavy locks. Roughly 10–45 minutes and 12 GiB for T7, 20–120 minutes and about 22 GiB or more per normal sample, longer for paired or kernel runs. Network is one live index check plus the normal dependency and source transfers. Run in an attended terminal for sudo.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0008a-tools.XXXXXX")
  export TMPDIR="$d"
  get() {
    local rev=$1 file=$2 digest=$3
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$rev/$file" -o "$d/${file##*/}"
    printf '%s  %s\n' "$digest" "$d/${file##*/}" | sha256sum -c -
  }
  get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-mlgo-t7.py.txt' '1089c21b3b4bf4205bd13ba64cace371c57a7d4ec86376877f3b2d069f551a9c'
  url=${PRODUCT_URL:-http://repos.vd.sec.samsung.net/priv/168.219.246.226:81/PRV/builds/b993/19368993/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261118.2/}
  mode=${GBS_MODE:-pic}
  lock="$PWD/workspace/temp"
  mkdir -p "$lock"/pm000{4,5}-native-lock
  heavy() { flock -n "$lock/pm0004-native-lock/heavy.lock" flock -n "$lock/pm0005-native-lock/heavy.lock" "$@"; }
  case "$mode" in
    pic|kernel)
      args=("$mode" --dependency-product-url "$url")
      if [[ "$mode" == pic ]]; then
        get 'cd7f97e9cf75fd9bb70e0abe85ca626a073c64be' 'artifacts/scripts/r0005/gbs-t7-link.sh.txt' 'c36498246c21dbd6de23567cbf7e3320f80cef7a0c61a499acee0a74feb01c77'
        args+=(--probe "$d/gbs-t7-link.sh.txt")
      fi
      sudo -v
      heavy python3 -B -u "$d/gbs-mlgo-t7.py.txt" "${args[@]}" "${GBS_ARGS[@]}"
      ;;
    thumb)
      get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-thumb.py.txt' '928cff87ac0cb501a6d0575da5f1d80157bd02918d2378a5e061c2262cf11a92'
      args=("${THUMB_MODE:-defaults}" --dependency-product-url "$url")
      if [[ "${THUMB_MODE:-defaults}" == pair ]]; then
        get 'ea24f17d8d8f7b245c36d040381880839165d1c5' 'artifacts/scripts/r0004/image_mode_scan.py.txt' '1f419accc77f0f5b6fdb7077030f8d2b51e4069ea995cc48fefd92c735043d75'
        args+=(--scan-lib "$d/image_mode_scan.py.txt")
      fi
      sudo -v
      heavy python3 -B -u "$d/gbs-thumb.py.txt" "$d/gbs-mlgo-t7.py.txt" "${args[@]}" "${GBS_ARGS[@]}"
      ;;
    sample)
      get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/gbs-thumb.py.txt' '928cff87ac0cb501a6d0575da5f1d80157bd02918d2378a5e061c2262cf11a92'
      get '988001a92e58e272390553aea4a27e34e6a87d82' 'artifacts/scripts/r0008a/thumb-qb-sample.py.txt' 'b7a725e9c5e68072b9f5388a35df91494874f13f67a00fb7426a3067e04a3579'
      get 'd3cea65aac76d438b82b55a2857a5ee18546edad' 'artifacts/scripts/r0005/image-repo-lib.py.txt' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
      get 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' 'artifacts/ledger/qb37627297-source-pins-20261120.tsv' 'e7877e499ca148ba17095c72e2ef13c20cfbae17404182294c84d8781d77baaf'
      args=("${THUMB_PACKAGE:-deviced}" --dependency-product-url "$url")
      if [[ "${RUN_GBS:-0}" == 1 ]]; then args+=(--build); sudo -v; fi
      python3 -B -u "$d/thumb-qb-sample.py.txt" "$d/image-repo-lib.py.txt" "$d/gbs-mlgo-t7.py.txt" \
        "$d/gbs-thumb.py.txt" "$d/qb37627297-source-pins-20261120.tsv" "${args[@]}"
      ;;
    *) printf 'Unknown GBS mode %s\n' "$mode" >&2; exit 2 ;;
  esac
)
```

Local Python 3.10.12 checks covered the new programs, enforced the HTTP-404 guard in a fixture, verified live-dependency staging leaves each Base selector intact, and exercised the checksummed metadata and dependency-candidate joins. The native publication diff, exact helper RPM extraction, effective source/consumer traces and the two HQ probes still require the reviewed native runs.
