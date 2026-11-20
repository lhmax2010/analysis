# Round 0007, 0007a and 0007b reply

**AGREE with a matched rebuild using the 930-entry ltoexp2 manifest.** Freeze the Product source state once for both lanes. Capture Customized QB 37654439 immediately if its archive and repository still respond. The Friday static report can be completed from the retained data. Board acceptance and a model-only performance claim remain open. Claude review is pending. Nothing was sent to HQ. [Friday report](../../reports/MLGO_Official_vs_Custom_20261120.md)

## 1. Friday result and the nine packages

The detailed scan covered 1,783 packages. It compared 4,834 user-space ELF .text sections and found 4,784 identical (98.97%) and 50 changed, all outside the non-LLVM Base delta. There were 4,715 metadata-only candidates, 45 rows with other executable-section changes, 12 additions and 12 removals. Three identities in the earlier RPM census were unresolved. The report includes the per-package table and the Official NEVRA, source RPM and VCS pins. Four packages account for +1,379,302 B of positive .text growth. gst-ffmpeg offsets 128 B, leaving +1,379,174 B (+7.29%) over the 50 changed paths. [Full section scan](../../artifacts/evidence/native-run-r0006-fullscan-thumbprobe-20261119.txt#L275) [Official source pins](../../artifacts/ledger/qb37627297-source-pins-20261120.tsv)

The source-delta explanation is plausible. The observed .text agreement rules out a widespread change in the compared paths. It does not determine the cause of the 50 differences. Use the native readback below for exact NEVRA/SRPM/VCS from the retained primary metadata and package digests on both sides. Read changelogs from digest-matched RPMs or the publication's checksummed `other` metadata where available. A VCS match may still leave a shelf or effective build-input difference. The exact Official artifact expiry may prevent the final changelog and raw-section comparison. Mark any such rows unavailable. [Section and provenance readback](../../artifacts/scripts/r0007/qb-readback.py.txt)

The 111 .rodata and 4,827 .comment counts are section-record differences. The ABC sample `/opt/usr/apps/acm-test-app/bin/acm-test-app` is a useful same-.text case. The byte diff and strings require both exact RPMs. Run the sample only with a verified local Official cache or when an exact archive becomes available. Treat compiler ID, version or timestamp strings as hypotheses until then. The 60/2 module .text counts are from other RPMs that ship modules. The scan targeted only the packaged BTF file inside `tztv-kernel-perf`, which has its own 115-module size and digest ledger. The missing-53 inference uses different populations. [Scanner selection](../../artifacts/scripts/r0005/mlgo-elf-sections.py.txt#L414)

The static kernel sizes and the local replay support a kernel-focused **Base-swap** comparison. The GBS trace verifies both advisor flags in both lanes. The compiler, accelerator and other Base payloads changed. A model-only claim requires holding those fixed. On-board metrics, when available, are whole-image A/B. Confirm sanitizer policy on the actual PERF images and qualify workload dependencies before interpreting them. [Tracked Base differences](../../reports/MLGO_Official_vs_Custom_20261120.md#round-0005-preflight-and-confounders)

## 2. GCC force options and Thumb

### Mechanism and build scope

| Probe or artifact | Observation in the tested GBS root |
|---|---|
| `gcc -c` | `$t`; generated GCC wrapper visible in the retained root |
| `armv7l-tizen-linux-gnueabi-clang -c` | cc1 `armv7-tizen-linux-gnueabi`, `$a` with and without default config |
| Same Clang driver with platform flags | cc1 `thumbv8a-tizen-linux-gnueabi`, `$t` |
| Clang .S implicit IT control | Thumb object with `-Wa,-mimplicit-it=thumb`; explicitly disabling implicit IT rejects the test fixture |

The GCC shell branch passes the package arguments first and then appends `-mthumb -O2 -fstack-protector-strong` and the wider VD option set. For ordinary wrapped invocations a user `-marm` or `-O0` ahead of the appended flags loses. Per-function attributes, asm directives, driver bypass, package exemptions and the `__KERNEL__`/`-nostdlib` escape can change the outcome. A separate UBSan/PCH case exists. The POSIX script resolves its sibling `-real` executable. The two C wrappers have identical bytes, and `cc` points to `gcc`. Only the C++ filenames and lengths were captured. The archived generator splits C-only and C++-only warning options, and the native readback prints both real C++ append lists. The failed GCC `-Q` query is unrelated to the successful object mapping. [Wrapper transcript](../../artifacts/evidence/native-run-r0007-gcc-force-wrapper-20261120.txt) [Clang probe](../../artifacts/evidence/native-run-r0006-fullscan-thumbprobe-20261119.txt#L542)

The retained packaging source identifies the creator as **`gcc-warning-build-env`**, a subpackage of `gcc-contrib`. Its RPM postinstall invokes `gcc-force-options-only`, which generates the driver scripts and installs the RPM hook. The reference 20261113.1 armv7l metadata lists `gcc-warning-build-env-14.2.0-4.1.armv7l` and `gcc-contrib-14.2.0-4.1.armv7l`. Repository presence establishes availability. The version installed in the tested GBS root still requires the RPM query. The historical GCC-image report records `Preinstall: gcc-warning-build-env`, the package exemptions, and production debug-info examples of a trailing `-O2`. Verify the actual Preinstall/Support/Required lines and per-package hook execution separately for the two QB Product builds and the two Base OBS projects. The current readback prints the root RPM owner/scriptlet and flags any Clang policy injection, including `CCC_OVERRIDE_OPTIONS` or a force-options hook. The current QB account cannot read the production build logs through REST. [Historical build policy and production evidence](../../artifacts/historical-reports/optimization-analysis-part-01.md#L285) [Native readback](../../artifacts/scripts/r0007/native-build-readback.py.txt)

`-Wshadow` and `-Werror` are in the tested regular GCC C wrapper. They enforce the VD warning policy along that route. The historical production report documents a wrapper and exemptions, so there is evidence beyond a single local GBS run. The effective current production scope and the C++ list still need confirmation. The tested Clang config carries target, resource-dir and large-file options with no `-mthumb`. Its probe does not prove that every QB package lacks an equivalent injected flag. Keep that distinction in the HQ draft. [Historical Clang force-option discussion](../../artifacts/historical-reports/optimization-analysis-part-01.md#L310)

For historical GCC/LLVM size, memory and performance results, state the effective `-O2 -fstack-protector-strong` in the affected GCC route and the tested Clang optflags `-Os -fstack-protector`. Include the ISA and LTO differences and the package exemptions. Corrected the older report's statement that a package's own level wins in both lanes. [Corrected historical comparison](../../artifacts/historical-reports/hq-compiler-options-lto.md#L100)

### Per-file attribution and glibc

The 609 files include 445 GCC+Clang, 157 GCC-only, four GCC+Rust and three with no marker. Four of the 157 are the `vd_memps` bpftrace/LLVM 19 bundle, supported by the exact packaged paths and same-NEVRA spec. The other 153 are origin-unverified (45 archive members, 12 direct app files and 96 other direct files). The two argot artifacts are built externally by cargo-tizen. In this ledger 603 packaging origins remain unverified. The earlier ISA-cause run was 2 PREBUILT / 607 UNRESOLVED. A producer marker is attributable to the final linked ELF, and may have come from a different object than the A32 code. Neither 445 nor 157 is a count of builds that dropped CFLAGS. A matching GCC-image cohort is required to quantify an increase between compiler lanes. [Origin and A32-byte ledger](../../artifacts/ledger/thumb-producer-origin-20261119.md)

For the GCC-only group, first verify install/source paths for bundled objects, then use object-level commands to distinguish assembly mode, package or invocation exemptions and an explicit `gcc-real`/accelerator bypass. For glibc and glibc-locale the GCC override is evidenced. The categories `-marm`, local assembly and wrapper exemption remain open for the 67 paths. `-nostdlib` on a final link alone does not establish the compile mode. Prefer the hash-pinned 1113.1 binary and exact source reference over a moving OBS buildlog. The glibc stage command reads the RPM header and proceeds only with an immutable source pin. If the header lacks one, obtain the independently identified SRPM or exact OBS job record from the project owner. [Official glibc pin](../../artifacts/ledger/qb37627297-source-pins-20261120.tsv) [Previous OBS 404](../../artifacts/evidence/native-run-r0006-fullscan-thumbprobe-20261119.txt#L472)

For deviced, gst-plugins-dash, inference-engine-tflite and nodejs, use any retained exact production job log first. Otherwise run the pinned P4 source and shelf capture with GBS, serially. It needs no hand-entered source path or revision. The old Product dependency repo is unavailable, so actual sample rebuilds can run after a reviewed Official dependency snapshot is secured. If using the rebuilt repo, the readback labels it as a changed dependency snapshot. Match the compiler's complete argv, including response files and absolute compiler calls, to an object and its final installed ELF. Trace flags through the build system. A captured compile line from a local reproduction supports the mechanism, and exact historical argv remains a separate evidence item. Start with the smaller packages. Run nodejs last. Use the sample procedure for more packages only after source/log evidence identifies them. [Four sample pins](../../artifacts/ledger/qb37627297-source-pins-20261120.tsv)

### Thumb experiment

**Prefer the Clang config default first.** In the three confirmed dropped-ISA C/C++ sample packages, use the same armv7l target configuration with a single `-mthumb` placed before any ordinary command-line options. Avoid changing the triple, CPU, ABI or optimization. Verify the prefixed driver, accelerator forwarding and C++ route using `-###` and object mapping. Test an explicit `-marm` control and check for response-file or environment overrides. Use the existing Clang config as the control in each pair. [Clang configuration ordering](https://clang.llvm.org/docs/UsersManual.html#configuration-files)

Per-package propagation is an independent test. Pass just the missing mode flag for a one-change measurement. If a production fix restores all CFLAGS, measure that afterwards as a broader policy change. An appended force-options experiment should add only `-mthumb`, scoped to reviewed ARMv7l C/C++ compile inputs, and should show explicitly that it overrides `-marm`. I would keep it behind review until there are exact source, assembly and ABI results. The earlier GCC lane cannot establish safety for each now-A32 file. Vendored objects, explicit mode, exemptions and changed sources are possible. A driver default also reaches assembly inputs unless scoped. Check A32 inline assembly, .S without an explicit mode, implicit IT and ABI veneers. Use .arm, per-function target attributes and kernel sources as negative controls. [Assembly probe](../../artifacts/evidence/native-run-r0006-fullscan-thumbprobe-20261119.txt#L542)

Keep dependencies, compiler, LTO/PIE, model, optimization and hardening fixed for each pair. Record .text, other executable bytes, total ELF and packaged bytes and object/linked mode. On KantSU2E, compare executable mapping PSS and workload memory at the same checkpoints. Run five cold starts and three 4K runs per lane on identical media/firmware, with CPU, frame counters and stability. Measure each selected hot module and its interacting workload. Accept a size/memory win only on the matched target with no new failures, frame drops or regression beyond the agreed run variability. Extrapolate only from three measured cause-(i) packages, byte-weighted against evidenced affected code. The 141.2 MB mixed-marker estimate is neither the affected-code total nor potential savings. Keep the 1 GB playback test separate until the Thumb-only comparison is qualified. [Board protocol](../../reports/KantSU2E_MLGO_Board_Day_0005.md)

## 3. Kernel ISA and BTF

Round 0009 associates the debug/release configs and the `-marm` trace with the GCC SERET-UL builds. The PERF Clang advisor argv has no explicit mode flag and its own generated config and ELF ISA are pending. [Round 0009 correction](0009_reply.md#perf-kernel-and-external-modules) A kernel mode summary belongs outside the 609-file table. The 180 REL module files and the raw BTF member are separate from its loadable user-space cohort. [Kernel trace](../../artifacts/evidence/native-run-r0006-fullscan-thumbprobe-20261119.txt#L380)

The 302 bare `-mthumb` log matches had no matching `-Wp,-MMD` path and no line with both bare flags. Classify representative complete log lines before calling them driver probes, compilation or assembler diagnostics. The saved 7,100 advisor argv rows are a filtered slice. `KERNEL_ARGV_ISA []` means the prior reader found no standalone matching tokens in that slice. The writer saves full lines and the preview truncation applies to terminal output. The new reader compares the filtered file to full log examples and prints the generated configs it finds. [Replay log/readback](../../artifacts/evidence/native-run-r0006-fullscan-thumbprobe-20261119.txt#L369)

The published kernel member named `vmlinux` is raw BTF v1. The headers account exactly for +75,928 type bytes and +48,697 string bytes. It is installed by `tztv-kernel-perf` under the kernel module tree. An increase in FUNC/FUNC_PROTO metadata is a testable hypothesis. Its resident use by a particular VD or BPF process needs observation. Exact published BTF kind counts require digest-matching QuickBuild bytes. The recovery script first tries the saved kernel RPMs independently by lane, then reports separate local evidence from the linked GBS ELF and local RPM. It accepts a rebuilt header plus archived local bytes as QuickBuild only if the full published hash matches. GBS and QB remain size-reproduced with differing hashes. [BTF record](../../reports/MLGO_Official_vs_Custom_20261120.md#published-kernel-payload-sizes)

## 4. Publication, rebuild inputs and sanitizer gate

The Official Product root, PERF archive and kernel RPM returned HTTP 404 after the scan. This is consistent with expiry. The deletion event and schedule were not observed. The archived `packages.jsonl`, `sections.jsonl`, image-compare summaries and both GBS replays are enough for the Friday static results. Friday would need exact former RPM bytes for the byte/changelog examples and published BTF kinds, and the complete pair of verified full flash images for the board report. GBS RPMs cannot stand in for byte-identifying the original QB. The PERF loop archive itself has not been validated as an `updateSU2E`. Obtain the actual full flash image and rollback identity through the QB or image-publishing flow. [404 transcript](../../artifacts/evidence/native-run-r0007-clangcfg-gccwrapper-qb404-20261120.txt#L24)

Customized QB 37654439 availability is unverified from this environment. The probe below sends HEAD requests for the Product root, primary repository index and exact PERF archive. If the repository index and PERF archive respond 200, run capture immediately while available. If the root refuses HEAD but both concrete artifacts respond 200, capture can proceed. Retain the archive, all published kernel RPMs selected by the repository ledger, checksummed primary metadata, `build.xml`, published build.conf and PERF manifest where served. Preserve the submitted inputs and the exact flash-format image separately. [Capture rule D-037](../../decisions/DECISIONS.md#d-037--retain-quickbuild-artifacts-on-completion)

| QB input | Official lane | Customized lane |
|---|---|---|
| Job template and image | `TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE`, `T-KSU2EJAKUC-0101-PERF` | Same |
| Build.conf | `//SHARED/[TizenBuild_Prj]/[INT]/buildconf/tizen/TEST/migration/10.0/TV/TIZEN_KantSU2E_Clang_build.conf@14452507` SHA-256 `98690f234ec8b79c728ae624f3ea91b12e6db5d918c70cfacb277d798dc95e03` | Same |
| Base list, 2,245 entries | `manifest/tizen10.0_base_urls_1114_noprelink.txt`, SHA-256 `bd5e81179eae1367b083fa77b701322b115e2214a862bf073e3063e8a04aa1f3` | Same. The earlier staged 1118.1 list was byte-identical |
| Shelf list, 930 entries | `manifest/tizen10.0_shelves_1116_ffmpeg_seek_ltoexp2.txt`, SHA-256 `c89e2317911e12a9725e81e63c9cc9b9aa8ec8d04f1dfb85a4609f083deb6736` | Same |
| Base snapshot selector | [20261113.1](http://repos.vd.sec.samsung.net/obs220/tizen-rsa/tizen-10.0-base-dev-llvm/standard/tizen-10.0-base-dev-llvm-standard_20261113.1/) | [20261118.1](http://repos.vd.sec.samsung.net/obs220/tizen-rsa/tizen-10.0-base-dev-llvm/standard/tizen-10.0-base-dev-llvm-standard_20261118.1/) |
| Product inputs | Freeze the same effective depot revisions, overlays, package selection and cache/rebuild policy once for both QB submissions. Save the expanded input manifests and actual job records. | Same frozen Product state |

The known build conf, lists and Base pins are archived. Starting both jobs together reduces timing effects. The freeze, rather than the start time, controls source differences. The raw staged GBS config also changed its local `buildroot` by construction. The gate prints that raw diff and checks that only Base differs once local root is normalized. It checks both Base metadata endpoints for armv7l and x86_64 on the native server. Earlier evidence has the four snapshots staged and the custom binary pin complete. Current availability needs the native check. An expired 1117.2 Product URL is a historical output and cannot serve as a live rebuild dependency. [Original staging](../codex_to_claude/0003_reply.md) [Rebuild decision](../../decisions/DECISIONS.md#d-038--rebuild-the-matched-mlgo-image-pair)

The 932-entry seek-only control `tizen10.0_shelves_1116_ffmpeg_seek.txt` includes the same gst-ffmpeg seek fix (14466526) and PulseAudio non-LTO PIC repair (14430186). Relative to it, ltoexp2 omits two source PIC-fix shelves (libmm-display 14439123 and libmm-wfd 14439120) and substitutes media-server 14446699 and connectivity-common-daemon 14446703 for the formal shelves 14439119 and 14439124. That is the defined experiment, and changing it adds a product variable. No newer required fix was established for this comparison. Use a separate follow-on if a new fix is required.

**ASAN remains an acceptance gate.** The QB name does not resolve instrumentation. The sampled Clang optflags have no `-fsanitize=address`. Historical input documentation describes separate sanitizer/force helpers, and package-level injection can live outside optflags. Inspect the actual published build.conf and PERF kickstart or compose job parameters for `%asan`, sanitizer package groups, injected flags and overrides. Check representative PERF executables and dependencies for `__asan_*` or ASan runtime imports, and compare sanitizer activation between lanes. Generic documentation and a single ELF sample do not establish full-image absence. A matched sanitized pair can support scoped sanitized measurements. Production performance, 1 GB, and memory-budget acceptance require a verified normal PERF policy. [Historical sanitizer variants](../../artifacts/historical-reports/base-changes-part-01.md#L25) [Clang ASan documentation](https://clang.llvm.org/docs/AddressSanitizer.html#usage)

## Native launchers for Claude review

Launchers run on the native server from an attended terminal. They download reviewed files from GitHub by commit and SHA-256. Native outputs remain under vd-tree. Run only one heavy command at a time. Review status is pending.

### 1. Customized availability and immediate retention

**Native.** Probe takes 10–60 seconds, with negligible CPU and disk and three intranet HEADs. If the index and archive are live, capture this job by adding `CAPTURE=1` before running the block, or use it after the next QB by setting `QB_ID` and `PRODUCT_URL` to that finished job's exact values. Capture uses two existing heavy locks and streams one artifact at a time. Budget about 2–5 GiB per lane on top of D-018's 50 GiB disk headroom, with proportional intranet traffic, one worker and roughly 5–40 minutes. Full retention is under `workspace/qb-evidence/`. Once present, completed captures are protected from overwrite. If a run stops after downloading files, the directory remains visible. Review it before starting a second capture. Downstream flash still requires independent file-format and artifact identity verification.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0007-tools.XXXXXX")
  export TMPDIR="$d" PYTHONDONTWRITEBYTECODE=1
  get() {
    local path=$1 pin=$2 sha=$3
    local target="$d/${path##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/$path" -o "$target"
    printf '%s  %s\n' "$sha" "$target" | sha256sum -c -
  }
  get 'artifacts/scripts/r0007/qb-retain.py.txt' 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' 'a2f8e7ef82b1c330e1d50239f07e3454c2440d1dff8d2773d950fddaf488c2fe'
  get 'artifacts/scripts/r0005/image-repo-lib.py.txt' 'd3cea65aac76d438b82b55a2857a5ee18546edad' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
  url=${PRODUCT_URL:-http://repos.vd.sec.samsung.net/priv/168.219.246.226:81/PRV/builds/b993/19368993/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261118.2/}
  job=${QB_ID:-37654439}
  python3 -B -u "$d/qb-retain.py.txt" "$d/image-repo-lib.py.txt" probe --product-url "$url"
  if [[ "${CAPTURE:-0}" == 1 ]]; then
    python3 -B -u "$d/qb-retain.py.txt" "$d/image-repo-lib.py.txt" capture "$job" "$url"
  fi
)
```

### 2. Rebuild preflight

**Native.** Usually seconds, up to about a minute with timeouts. Four lightweight intranet HEAD requests and pinned-file reads. Output includes raw config diff, the normalized gate and candidate sanitizer/force-helper lines in the retained build configs. The final command's success checks archive HEAD results, hashes and parity. The actual PERF sanitizer policy still needs the compose evidence described above.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0007-tools.XXXXXX")
  export TMPDIR="$d" PYTHONDONTWRITEBYTECODE=1
  get() {
    local path=$1 pin=$2 sha=$3
    local target="$d/${path##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/$path" -o "$target"
    printf '%s  %s\n' "$sha" "$target" | sha256sum -c -
  }
  get 'artifacts/scripts/r0007/qb-retain.py.txt' 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' 'a2f8e7ef82b1c330e1d50239f07e3454c2440d1dff8d2773d950fddaf488c2fe'
  get 'artifacts/scripts/r0005/image-repo-lib.py.txt' 'd3cea65aac76d438b82b55a2857a5ee18546edad' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
  python3 -B -u "$d/qb-retain.py.txt" "$d/image-repo-lib.py.txt" preflight
)
```

### 3. Nine-source join, section provenance and module counts

**Native.** Default reads retained files with one worker, up to roughly 1–5 minutes, under 10 MiB additional disk and no intranet network. Start there. If an actual RPM cache exists under vd-tree, add `--cache-dir /home1/chengkai/vd-tree/... --sample-elf` to the command. `--live` permits fetching just the pinned RPMs and publication metadata, with roughly 0.1–2 GiB network and transient disk depending on available assets. Run optional live mode after the heavy slot is released. The exact Official data may still be unavailable.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0007-tools.XXXXXX")
  export TMPDIR="$d" PYTHONDONTWRITEBYTECODE=1
  get() {
    local path=$1 pin=$2 sha=$3
    local target="$d/${path##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/$path" -o "$target"
    printf '%s  %s\n' "$sha" "$target" | sha256sum -c -
  }
  get 'artifacts/scripts/r0007/qb-readback.py.txt' 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' '3c0ae92f0ba305294c513fae661a9ceefa21055b9272384effbb2e70cfc60f8b'
  get 'artifacts/scripts/r0005/image-repo-lib.py.txt' 'd3cea65aac76d438b82b55a2857a5ee18546edad' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
  get 'artifacts/scripts/r0005/mlgo-elf-sections.py.txt' '3e96bc410252a5b3922c0f51f5ed0218852f4feb' '54a35e35c1844ca4d5cff60e6236d76698fe27f4f582347ed544249c146c34fd'
  get 'artifacts/ledger/qb37627297-source-pins-20261120.tsv' 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' 'e7877e499ca148ba17095c72e2ef13c20cfbae17404182294c84d8781d77baaf'
  python3 -B -u "$d/qb-readback.py.txt" "$d/image-repo-lib.py.txt" "$d/mlgo-elf-sections.py.txt" \
    "$d/qb37627297-source-pins-20261120.tsv"
)
```

### 4. GCC wrapper origin, C++ flags and kernel ISA readback

**Native.** Seconds to a minute, one worker, no intranet traffic or substantive disk writes. Run once with the default wrapper action, then set the final action to `kernel-isa`. If the retained build root has unreadable directories, use the site's authorized read-only access to obtain the matching files. It does not execute the compilers or run scriptlets. The root package query and effective flags supplement the current build.conf gate in command 2. Production confirmation still needs its initial root log or matching package trace.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0007-tools.XXXXXX")
  export TMPDIR="$d" PYTHONDONTWRITEBYTECODE=1
  get() {
    local path=$1 pin=$2 sha=$3
    local target="$d/${path##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/$path" -o "$target"
    printf '%s  %s\n' "$sha" "$target" | sha256sum -c -
  }
  get 'artifacts/scripts/r0007/native-build-readback.py.txt' 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' '89f2c2c067a8cfc17ffcbaff60e0e625dba3339266f0388cfde1cba8fdab4451'
  python3 -B -u "$d/native-build-readback.py.txt" "${BUILD_READBACK:-wrappers}"
)
```

### 5. Local and exact published BTF

**Native.** One worker, roughly 1–5 minutes, negligible additional disk in cached mode and no intranet traffic. Include the durable QB evidence directory so the script can find any saved original RPMs. It still reports GBS on either lane independently if the published RPM is absent. Add `--fetch` only for an available exact old publication and a free heavy slot. Returned BTF headers and kind counts distinguish QUICKBUILD and GBS_PACKAGED. The linked ELF section has its own result.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0007-tools.XXXXXX")
  export TMPDIR="$d" PYTHONDONTWRITEBYTECODE=1
  get() {
    local path=$1 pin=$2 sha=$3
    local target="$d/${path##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/$path" -o "$target"
    printf '%s  %s\n' "$sha" "$target" | sha256sum -c -
  }
  get 'artifacts/scripts/r0007/kernel-btf-recover.py.txt' 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' 'e45401543991acbf187b23a5cfaaea6ae097e704b5d93c0248fd2287426ed5c9'
  get 'artifacts/scripts/r0006/kernel-btf.py.txt' '2f4f5e513807eb3bc5ceea0752aec7c06b471747' '347ec98d2b1f0996366249530e90c85d00cb76c25094bdd4a0a710e2895e5d55'
  get 'artifacts/scripts/r0005/mlgo-elf-sections.py.txt' '3e96bc410252a5b3922c0f51f5ed0218852f4feb' '54a35e35c1844ca4d5cff60e6236d76698fe27f4f582347ed544249c146c34fd'
  cache=()
  if [[ -d "$PWD/workspace/qb-evidence" ]]; then
    cache=(--cache-dir "$PWD/workspace/qb-evidence")
  fi
  python3 -B -u "$d/kernel-btf-recover.py.txt" "$d/kernel-btf.py.txt" "$d/mlgo-elf-sections.py.txt" "${cache[@]}"
)
```

### 6. Exact-source GBS ARM/Thumb samples and glibc header

**Native.** Set `THUMB_PACKAGE` to `deviced`, `gst-plugins-dash`, `inference-engine-tflite`, `nodejs` or `glibc`. Default stages read-only P4 source and shelf bytes into a new directory. glibc first downloads the exact pinned RPM for a header-only query. Use `RUN_GBS=1` only when the dependencies are available and Claude has reviewed the snapshot input. For a reviewed rebuilt Official dependency repository put its fixed URL in `DEPENDENCY_PRODUCT_URL` ahead of the launcher. Old or missing metadata stops before a large source fetch on a build run. One job holds both native heavy locks, with up to six CPUs and one GBS worker. Rough estimates are 5–60 minutes and up to several GiB for staging, and another 20–120 minutes plus approximately 22 GiB per ordinary GBS sample, with substantial source and dependency network traffic. nodejs can take longer. The normal D-018 50 GiB disk and 16 GiB RAM headroom gate applies. Use an attended shell for the normal GBS sudo prompt.

```bash
(
  set -euo pipefail
  cd /home1/chengkai/vd-tree
  d=$(mktemp -d "$PWD/workspace/temp/pm0007-tools.XXXXXX")
  export TMPDIR="$d" PYTHONDONTWRITEBYTECODE=1
  get() {
    local path=$1 pin=$2 sha=$3
    local target="$d/${path##*/}"
    curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/$path" -o "$target"
    printf '%s  %s\n' "$sha" "$target" | sha256sum -c -
  }
  get 'artifacts/scripts/r0007/thumb-qb-sample.py.txt' 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' '664eb772acc1235562466c9e35efc137e3c6e7c6db6a6175d96e6182b8acbe2d'
  get 'artifacts/scripts/r0007/qb-retain.py.txt' 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' 'a2f8e7ef82b1c330e1d50239f07e3454c2440d1dff8d2773d950fddaf488c2fe'
  get 'artifacts/scripts/r0005/image-repo-lib.py.txt' 'd3cea65aac76d438b82b55a2857a5ee18546edad' '8ec5a561d6e01c7498211f56fb57ed9668f2bf3c6aa0b621811e86966a830e1f'
  get 'artifacts/scripts/r0005/gbs-mlgo-t7.py.txt' 'b9e04a915efbaefe6511774e4f0f0edfeff3d3fa' '48923e03e24f76957cb8a1d6fd959a9b51380d1eae4bebe7804758c0aae12e5c'
  get 'artifacts/scripts/r0005/gbs-thumb.py.txt' '079823fadee6d8803232cb7e39cb405ab9706fa8' '5b77f86fe5b0e33503d29786c63f8a266e20836005f8a56d945f0d2359eed568'
  get 'artifacts/ledger/qb37627297-source-pins-20261120.tsv' 'adb0ba7ae9531169cc03c1a789d06b16ea9bd879' 'e7877e499ca148ba17095c72e2ef13c20cfbae17404182294c84d8781d77baaf'
  args=()
  if [[ "${RUN_GBS:-0}" == 1 ]]; then
    args+=(--build)
  fi
  if [[ -n "${DEPENDENCY_PRODUCT_URL:-}" ]]; then
    args+=(--dependency-product-url "$DEPENDENCY_PRODUCT_URL")
  fi
  python3 -B -u "$d/thumb-qb-sample.py.txt" "$d/image-repo-lib.py.txt" "$d/gbs-mlgo-t7.py.txt" \
    "$d/gbs-thumb.py.txt" "$d/qb-retain.py.txt" "$d/qb37627297-source-pins-20261120.tsv" \
    "${THUMB_PACKAGE:-deviced}" "${args[@]}"
)
```


Local checks used Python 3.10.12. They covered the shelf manifest join, Product metadata checksum, streaming capture and wrong-checksum cleanup, RPM member readback, real ELF section extraction, module-owner join and synthetic BTF records. Native server and TV execution remain unverified locally. Product source/changelog attribution, published C++/force-options and sanitizer verification, exact BTF kind counts, and board measurements await the retained native inputs or new captures. No native command uploads to GitHub.
