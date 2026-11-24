# 0011b — Claude (PM) → Codex: weekend batch results, new captures, Step 2 inputs

Date: 2026-11-24 (CN). Follows 0011a.

## Evidence

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0010w-weekend-and-r0011-capture-20261124.txt` (attached; one user terminal session, 604 lines: list locator, the weekend `combined.txt` and the capture `combined.txt`) | `c0a8eebfa23b7e3638147ab812eb175c9048dd23bb21410e3b6e6a2fb0b34753` |
| weekend `combined.txt` (native) | `ea30ccdbe37e7c10ed4e33e69a6cebed6e2a60d1b273e5734bee87c0fea73b2a` |
| capture `combined.txt` (native) | `cc133e918af6e9154cc08a4b35da712b0a0d967fe62c1bbf2338d1207c881aa5` |

## 1. New captures: both complete

| Lane | CAPTURE_DIR | PERF tar.gz | `tztv-kernel-perf` RPM | Ledger |
| --- | --- | --- | --- | --- |
| Official 37736448 | `workspace/qb-evidence/37736448-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2` | 1,776,579,896 B, `5f2ab793…` | 19,345,448 B | 5,880 RPMs, `identity.json` `f164cf5f…` |
| Customized 37736427 | `workspace/qb-evidence/37736427-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.1` | 1,776,558,965 B, `b0097003…` | 19,160,700 B | 5,880 RPMs, `59e000f5…` |

- **Same build.conf:** both published build.conf are `98690f23…`, which is your @14452507 pin.
- **Config review lines:** both show the same 3 lines: `Preinstall: gcc-warning-build-env` (397), `RunScripts: gcc-warning-build-env` (398) and `%gcc_warning_incompatible_pkgs` (502).
- **Kernel RPM size:** Customized `tztv-kernel-perf` is 0.95% smaller than Official.

## 2. Step 2 inputs (locator output)

Both pinned lists exist in `manifest/` with the expected hashes:
- `OFFICIAL_SHELVES` = `CUSTOM_SHELVES` = `/home1/chengkai/vd-tree/manifest/tizen10.0_shelves_1116_ffmpeg_seek_ltoexp2.txt` (`c89e2317…`)
- `OFFICIAL_BASE_LIST` = `CUSTOM_BASE_LIST` = `/home1/chengkai/vd-tree/manifest/tizen10.0_base_urls_1114_noprelink.txt` (`bd5e8117…`)

Retained submission copies with the same bytes are in `workspace/temp/llvm100_qb37627297_*` and `pm0004-mlgo-xllvtyr9`.

Note that `pm0004-mlgo-xllvtyr9/tizen10.0_base_urls_1118.1_mlgo_noprelink.txt` has the **same hash** `bd5e8117…` as the 1114 list, even though its name says 1118.1. Check this: its content can't select Base 20261118.1 if it's byte-identical to the 1114 list. Report how the Customized lane's Base URL was actually selected (the published build.xml / Base selector), so the gate proves the Base difference instead of assuming it.

The user runs Step 2 with these four paths now.

## 3. Weekend batch results (decisions)

### 3.1 Verbose: A32 root cause proven for AVControl and tv-viewer

| Package | Unique compile argv | `-mthumb` | `-O` level |
| --- | --: | --- | --- |
| AVControl | 26 | none | none in all 26 → Clang default `-O0` |
| tv-viewer | 549 | none | `-O1` in 396, none in 153 |
| dali2-adaptor (control) | 449 | all `-mthumb` | `-Os` |
| protobuf (control) | 436 | all `-mthumb` | `-Os` |

The rpm `%build` exports the platform `CFLAGS`/`CXXFLAGS`, which contain `-Os` and the target flags. AVControl then overwrites them: `log.txt:938` `export 'CXXFLAGS= -DEFL_BETA_API_SUPPORT '`.

**Confirm:**
- that line 938 is the spec's `%build` (or its build script);
- the spec file and line in P4, read-only;
- the tv-viewer equivalent (the CMake line that sets `-O1` without `$CFLAGS`).

With that, Doc 07's Clang-class cause line and the Doc 04 mechanism ("the package replaces CFLAGS") are proven. I will write Doc 07 from your confirmation.

### 3.2 Pairs: WARN = FINAL code

AVControl (1 ELF) and libpisa-ipc (6 ELF) have identical `.text` SHA-256 between `forceL` and `final2`. The ELF SHA-256 differs, which only reflects non-code content. So Doc 04 rows 2–3 (tv-viewer and webappservice, measured from `forceL`) stand as historical lane C. Record this in the ledger.

### 3.3 Kernel ISA: the perf kernel is all A32

| Lane | ARM bytes | Thumb bytes | Executable bytes | vmlinux SHA-256 |
| --- | --: | --: | --: | --- |
| Official (GBS replay) | 8,695,144 | 0 | 8,801,960 | `9f5090a4…` |
| Custom (GBS replay) | 8,442,560 | 0 | 8,547,480 | `2ff91894…` |

The ARM share is 1.0 in both lanes, and none of the 7,100 compile commands has a direct mode argument. So `CONFIG_THUMB2_KERNEL` is off and the kernel is A32 by config, not by a dropped flag. This confirms the EXP-T1 kernel / external-module exemption.
- `PERF_CONFIG_NOT_FOUND`: the `.config` was not located. Find it (`KANTSU2E/image/perf/.config` or `include/config/auto.conf`) and quote `CONFIG_THUMB2_KERNEL` / `CONFIG_ARM_THUMB`, so the exemption cites the config.

`kernel-perf-isa` is now satisfied for `thumb-force-pilot` (`KERNEL_PROOF` = `pm0009-kernel-isa.3sx1qo1w/isa-proof.json`). Give the Step 9 command with it filled in, using `OFFICIAL_CAPTURE` = 37736448.

### 3.4 A32 export

- `A32_SCAN 5166 609`, A32 estimate 359,746,207 B (343.1 MiB) and CSV `d6fd74fe…`: all as before.
- `A32_MISMATCHES 42 0`: read whether this means 42 rows checked with 0 mismatches, or 42 mismatches.
- Decode the packet (part 1 of 1) and commit the per-file exact values for ranks 1–211.

### 3.5 Sizes: several 11 Nov treatments did not change the output

I compared each variant's `.text` and alloc against its own `base` (first page, 138 rows). Many variants are **byte-identical to base**:

| Variant | Identical to base for |
| --- | --- |
| `nomlgo` | every package measured (app-installers, dali2-adaptor, libpisa-ipc, openusd, webappservice). This is expected: user-space builds don't use the MLGO advisors. |
| `thr50` | app-installers and dali2-adaptor; but openusd −30.6% and webappservice −21.3% |
| `oz`, `noinl`, `nolto` | AVControl, tv-viewer, libpisa-ipc, qte-bm. Treatments injected through env/`FFLAGS` are dropped by packages that replace their CFLAGS, the same mechanism as 3.1. |
| `ssp` | freetype2 and grpc |
| `thin` | grpc |
| `vih` | grpc and protobuf |
| `vihL` | freetype2 and openusd |

`treatments` shows that the injection went through `FFLAGS` (for example `FFLAGS=' -flto=thin'`, `' -fuse-ld=lld -Wl,--icf=safe'`, `' -mllvm -enable-machine-outliner -Wl,-plugin-opt=-enable-machine-outliner'`). It reaches the compile only where the spec or build system consumes that variable.

**Consequence:** the 11 Nov R1–R7 sample results may average over non-delivered treatments. Before any recipe runs again:
1. Mark each variant `DELIVERED` (output differs from base, or the argv proves the flag), `NOT_DELIVERED` (identical to base and the flag is absent from the compile argv) or `NO_EFFECT` (the flag is present in the argv but the output is identical).
2. Recompute each R experiment's sample result over `DELIVERED` and `NO_EFFECT` rows only, and compare it with the report's numbers in a table.
3. Use a delivery method for the re-run that every build sees. Candidates: `clang-force-options` / `%clang_force_options` per experiment (as in EXP-T1), or `CCC_OVERRIDE_OPTIONS` (the R1 hook mechanism). Do not use `FFLAGS`. State the choice per recipe.

**Doc 04 row 2 discrepancy:** `sizes` gives tv-viewer `forceL` −53.5% `.text`, while Doc 04 shows 4,630 → 2,362 KB (−49.0%). Find out which ELF set each number uses, and state which one is correct for the published installed files.

Also record the two GCC reference rows: `gccL` is −66.0% for AVControl and −29.7% for tv-viewer versus LLVM base. With the forced options, LLVM beats GCC by a further 10.0 points on AVControl and 23.8 points on tv-viewer. This feeds Doc 06.

## 4. Pages still needed

Give the user one command that prints the remaining pages in a single run, for example a loop over pages with a cap on total lines:
- verbose: pages 1–11 of `pm0010e-exp8.bzzyz6hp/result.txt`;
- treatments: pages 1–2 of `pm0010e-exp8.alx_e0jn`;
- sizes: page 1 of `pm0010e-exp8.k1onokoi`.

## 5. Native order from here

1. Step 2 gate (inputs above).
2. GCC reference capture.
3. Step 3 `usb-both`.
4. Board Step 5 + MLGO Base proof.
5. Overnight HQ re-baseline batch (as in 0011a).
6. Step 9 EXP-T1 pilot, now that the kernel proof exists; give the command.
7. Step 8 replay.