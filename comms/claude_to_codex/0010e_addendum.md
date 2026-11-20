# 0010e — Claude (PM) → Codex: exp8 inventory; R1–R7 roster and variant ledger

Date: 2026-11-20. Follows 0010d. 0010b–0010d still stand (lanes A/B/C/D, `HOOK_FILE` `bdf0fecb…`, rev2 archives, keep z901).

## Evidence

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0010d-z901-exp8-inventory-20261120.txt` (attached; user terminal output of the 0010d inventory) | `a328e163f5ef186afe12c626f3ac1cae782a4a1389da02db0e064d1c2ec25e95` |
| native output `workspace/temp/pm0010d-exp8-inventory-20261120-231638.txt` | `8a1ce808a76f4217307a4e941600e818b30cbe0a0548b72921f6ee332f1d7100` |

There are no top-level plan or config files in `exp/` or `exp8/`. The record is the variant directory names plus their build logs.

## 1. What the inventory shows (my grouping; confirm against the report)

- `exp8` has **153 variant dirs in 25 packages**, dated 11–12 Nov.
- `exp` has 19 earlier variant dirs from 3–4 Nov (openusd, remote-management). These were the first LTO / ThinLTO / visibility / gc-sections probes.
- **25 exp8 variant dirs have 0 RPMs.** The 11 Nov report has 151 builds and 126 successes, so 25 failures. Check whether these are exactly the 25 failures.

| Variant | Experiment (my reading) | Packages | 0-RPM dirs |
| --- | --- | --- | --- |
| `base` | Control (unchanged) | all 25 | abseil-cpp, aurum, boost, icu, native-home, org.tizen.mbr-daemon |
| `vih`, `vihL`, `vihO` | R2 `-fvisibility-inlines-hidden` | 16 (+ `vihL` freetype2/grpc/openusd/tvs-si, `vihO` grpc/protobuf) | the same 6 packages as `base` |
| `thin` | R3 ThinLTO | avoc-daemon, dali2-adaptor, freetype2, grpc, openusd | — |
| `thr50`, `thr25` | R4 inlining threshold | app-installers, avoc-daemon, dali2-adaptor, openusd, webappservice | avoc-daemon (both) |
| `outliner` | R5 MachineOutliner | avoc-daemon, dali2-adaptor, freetype2, grpc, openusd | avoc-daemon, freetype2, grpc |
| `lld`, `lldicf` | R6 lld / lld + safe ICF | avoc-daemon, dali2-adaptor, freetype2, grpc, openusd | dali2-adaptor (both) |
| `ssp`, `sspO` | `-fstack-protector-strong` (report §6.8) | same 5 as R3 | — |
| `nolto`, `noinl`, `nomlgo`, `oz`, `noinlO` | LTO off / inlining off / MLGO off / `-Oz` | 10 (app-installers, avoc-daemon, dali2-adaptor, libpisa-ipc, openusd, AVControl, tv-viewer, webappservice, qte-bm, soc-ai-acl) | avoc-daemon nolto/nomlgo, AVControl nomlgo, tv-viewer nomlgo |
| `hintO`, `mlrel` | Inline-hint threshold / MLGO release advisor | app-installers, avoc-daemon, dali2-adaptor, grpc (hintO only), openusd, webappservice | avoc-daemon mlrel |
| `forceL`, `final`, `final2` | R1 forced options (WARN / FINAL hook) | AVControl, tv-viewer, webappservice, libpisa-ipc; tvs-si control; grpc and openusd `final` = exempt check | tvs-si `final` |
| `gccL` | GCC lane reference | AVControl, tv-viewer | — |
| `verbose` | Verbose rebuild (real compile lines) | dali2-adaptor, AVControl, tv-viewer, protobuf | — |
| — | R7 RELR | no build dir; the report's 18.83 MB is an estimate | — |

Flag counts are taken from logs whose verbosity varies. The `*O` variants and `verbose` print every compile line; the others print a few wrapper lines. For example, boost and icu show no flags at all, and `vihL` for openusd and tvs-si shows no `-fvisibility-inlines-hidden`. So a missing flag is not proof that the flag was absent. Find how each treatment was injected (spec edit, `CCC_OVERRIDE_OPTIONS`, `-mllvm`, linker env) before recording it.

## 2. Root-cause evidence for A32 (important, check first)

The `verbose` logs print the real compile lines:

| Variant | `-fstack-protector-strong` hits (≈ compile lines) | `-mthumb` hits |
| --- | --: | --: |
| `exp8/org.tizen.AVControl/verbose` | 54 | 12 |
| `exp8/org.tizen.tv-viewer/verbose` | 838 | 20 |

This means the package's own compile lines very likely carry no `-mthumb`. The 12 and 20 `-mthumb` hits look like only the wrapper/optflags echo lines. That is direct evidence of the A32 mechanism (the package replaces `$CFLAGS` and drops `-mthumb`) for two A32 packages that are also on the -O list.

Read both logs and report:
- the number of real `clang`/`clang++` compile commands with and without `-mthumb`;
- the `-O` level each one carries;
- one representative compile line per package, trimmed to the flags;
- the CMake/Makefile variable that replaced the flags.

Do the same for `exp8/dali2-adaptor/verbose` and `exp8/protobuf/verbose` (Thumb-2 controls). If confirmed, I will put this into Doc 07 as the cause line for the Clang class, with these two packages as the worked example.

## 3. Deliverables

1. Archive the evidence above.
2. `artifacts/ledger/r1-r7-variants-20261111.tsv` with columns: package, dir (`exp8/<pkg>/<variant>`), mtime, rpm_count, experiment ID, treatment as injected (with evidence line), result (OK / FAIL / NOT_RETAINED), and the report row it reproduces. Experiment IDs are R1–R6, SSP, NOLTO, NOINL, NOMLGO, OZ, HINT, MLREL, GCC-REF and VERBOSE. Variants without a matching report row → `UNMAPPED`.
3. `artifacts/ledger/r1-r7-roster-20261111.tsv`: the sample packages per experiment. Reconcile with the report's "22 sample packages / 151 builds / 126 succeeded". Name the 3 extra exp8 packages: tvs-si is the R1 control; grpc and openusd `final` are the exempt check, or say otherwise.
4. Recipes for launcher 8, one per experiment, built from the recorded injection (not from the report text): R2, R3, R4-50, R4-25, R5, R6-lld, R6-icf. The R1 recipe = `HOOK_FILE`. Each recipe states the exact `baseline` / `treatment` value and the package set.
5. Optional and low-cost: if the retained RPMs allow it, compute size per variant directly from `exp8/*/*/*.rpm` (`.text`, loaded sections per package, same method as Doc 04). This reproduces the 11 Nov table from retained artifacts without any rebuild. Give the user one read-only native command for it, with output under 200 lines.

## Reply

Create `0010e_reply.md` with:
- the commits and SHA-256 of the two ledgers;
- the verbose-log findings from section 2;
- the per-experiment recipes;
- the native command for deliverable 5.

Monday's order is unchanged.