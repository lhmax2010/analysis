# Performance, memory and size evidence

[Verified: retained reports] There are historical static comparisons and candidate experiments. A controlled current-image GCC-versus-LLVM target performance/memory result set with run-level samples and variance is **not available**. Do not report static loaded-section savings as measured PSS or a historical different-source image comparison as compiler-only causality.

[Measurements CSV](../artifacts/measurements.csv) exports exact retained aggregate numbers. It is **not raw benchmark runs**; no run-level data is invented. The [historical analysis](../artifacts/historical-reports/optimization-analysis-part-01.md) and [optimization plan](../artifacts/historical-reports/optimization-plan.md) retain more detailed tables and their limitations.

| Evidence | Result | Interpretation |
|---|---|---|
| Historical common 4,778 ELF set | LLVM file sum 1638.76 MB vs GCC 1647.38 MB; text delta -39.93 MB | [Verified: historical report] report units retained; source/date and file-set controls matter |
| AVControl inherited-flags candidate | File 2,386,562 -> 680,730 bytes; executable sections 740,764 -> 183,324 | [Verified](../artifacts/evidence/avcontrol-size.txt); both Clang, combined flags/LTO policy change, not compiler-only or LTO-only gain |
| AVControl dependencies | NEEDED 108 -> 34; 782 weak exports removed, no strong definitions removed | [Verified] static strong imports covered in retained closure; dynamic consumers/target not cleared |
| Historical forced-option samples | Loaded-section sum -25.9%, text -36.2% | [Verified: report] four packages; no global runtime claim |
| Historical inline visibility | Loaded-section sum -11.4%, dynamic metadata -43.9% | [Verified: report] six effective samples with exclusions |
| Historical ThinLTO | Loaded sum +0.5%, text -0.1%; two-library timing 245s vs393s | [Verified: report] setup/load/parallelism must be controlled before extrapolation |
| Inlining threshold 50/25 | Loaded sum -14.3% / -23.3% | [Verified: report] selected samples; target cost unknown |
| MachineOutliner | Text -16.5%, loaded sum -8.1%, unwind +21.6% | [Verified: report] two effective samples; target/unwind gates open |
| lld + safe ICF | Loaded sum approximately -2.3% | [Verified: report] sample result, separate linker and ICF changes |
| RELR | Estimated 18.83 MB file opportunity | [Verified: report] encoding calculation, not measured deployment/PSS saving |

## Measurement requirements

| Metric | Method / tool | Current runs and variance |
|---|---|---|
| Boot / application launch | Fixed boot ID, log milestones and scenario timing; TPMS where applicable | No complete paired current dataset |
| Media throughput / responsiveness | Same stream/device/thermal state; frame/drop/latency and CPU counters | Targeted functional seek checks only; performance runs absent |
| ELF size | Section inventory, executable sections, allocated file/NOBITS and PT_LOAD file/memory | Deterministic retained artifact comparison; not repeated target measurements |
| RPM / TPK / image size | Exact byte sums on consistent package and compression scope | Full current matched sets/total image bytes unavailable |
| RSS/PSS/USS/private dirty | `/proc` smaps or smaps_rollup with fixed process set and scenario phase | Some prior observation medians exist; no qualified matched current pair/variance |
| Page cache / free memory / slab | meminfo and workload phase, separating file cache from working set | Matched repeated samples unavailable |
| Build time / peak memory | Per-stage wall time and resource metrics with fixed parallelism/cache | Historical sample timings only |

[Assumption/Memory: proposed protocol] Predefine repetitions, warm/cold cache policy, thermal state, workloads and acceptable regression margins with Claude/user. Retain each run rather than just medians. Begin with independent compiler/Thumb/LTO/MLGO module experiments; then validate the selected combination because modules interact. All optimization acceptance requires KantSU2E results.

`-O2/-Os/-Oz`, Full/ThinLTO, visibility, threshold, Outliner, lld, ICF, RELR and unwind analysis are explicitly tracked. PGO/AutoFDO/BOLT, global `-fno-plt`, or a machine-tuning change have no current accepted experiment/result established in this export. Hash style, hardening and garbage collection flags can already exist in platform/package commands; their presence is not a measured optimization experiment.

Customized versus Official MLGO kernel study is pending build/publication and actual advisor invocation checks. Hold source, runtime, kernel configuration, flags and link mode constant; first isolate inliner and regalloc if attribution is needed. A standalone model inference pass does not prove the kernel used it.
