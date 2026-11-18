# Decision register

Checkpoint: 2026-11-17. Prior user directions remain authoritative. “Agreed” historical entries mean an established user direction or implemented historical configuration, **not** that the new Claude PM has already reviewed it. Claude positions below are unknown unless supplied in request0001. New proposals remain Proposed until feedback. Exact historical decision dates are unknown where noted.

## D-001 — Coordination and storage

- Date: 2026-11-17.
- Topic/options: shared GitHub review vs scattered chat; central workspace vs dispersed outputs.
- Codex position: use public `lhmax2010/analysis` main for readable review; preserve raw inputs locally with hashes. All local generated files under `/home/toolchain/Desktop/temp`; native task files under `/home1/chengkai/vd-tree`; board additions under `/root`.
- Claude position: specified repository-only communication and workspace storage in [request0001](../comms/claude_to_codex/0001_handover_request.md).
- Final decision: follow these boundaries; preserve prior evidence and every review/decision, update status/tracker each round. User is final authority.
- Status: **Agreed** (user-relayed workflow).

## D-002 — Compiler and standard-library baseline

- Date: historical; confirmed in retained Nov 16–17 evidence.
- Topic/options: LLVM22 Clang migration with existing GNU C++ runtime vs simultaneous libc++ migration.
- Codex position: retain current LLVM22.1.8/GCC14.2 baseline and GNU C++ interoperability until a separately reviewed runtime transition. GCC remains for approved components and native consumers.
- Claude position: not yet received.
- Final decision: existing baseline retained for handover; a global libc++ switch is not evidenced or authorized by the request.
- Status: **Agreed** (retained configuration; fresh PM review pending).
- Evidence: [sources](../handover/03_sources_rpms_image.md), [bootstrap](../artifacts/evidence/llvm101-bootstrap.txt), [C++ smoke](../artifacts/evidence/llvm101-smoke.txt).

## D-003 — Compiler injection and linker route

- Date: historical; exact original decision date unknown.
- Topic/options: RPM compiler/macros plus package corrections vs replacing every compiler invocation; GNU linker/plugin vs global lld.
- Codex position: preserve existing Clang macros/driver GNU-plugin integration and audit actual commands. Hard-coded GCC, configure overrides and package exceptions need explicit treatment. Evaluate lld separately.
- Claude position: not yet received.
- Final decision: report implemented configuration; do not claim all packages obey macros or production 10.1 acceleration is validated.
- Status: **Agreed** (existing baseline only).
- Evidence: [sources/macros](../handover/03_sources_rpms_image.md), [patch index](../artifacts/patch-index.csv).

## D-004 — Parallel 10.1 adaptation

- Date: retained user direction, Nov 16–17; exact message time unknown.
- Topic/options: sequential after10.0 vs parallel independent adaptation.
- Codex position: parallel workstreams, separate provenance and acceptance; schedule heavy jobs within confirmed capacity.
- Claude position: not yet received.
- Final decision: user selected parallel10.1; do not block it on10.0 or treat private ARM smoke as production acceptance.
- Status: **Agreed** (user direction).
- Evidence: [master plan](../artifacts/progress_tracker.csv), [10.1 results](../handover/05_build_status.md).

## D-005 — Customized MLGO experiment and complete SR runtime

- Date: 2026-11-17.
- Topic/options: 10.0 vs10.1 starting Base; model-only transfer vs full SR runtime adaptation.
- Codex position: 10.0 starting Base as selected by user. Full SR runtime is required by the branch adaptation; freeze the same runtime for Official/Customized comparison.
- Claude position: not yet received.
- Final decision: revision12 supersedes incomplete model-only revision11. Preserve independent model/runtime switches. Wait for build/advisor/Base evidence before kernel claims.
- Status: **Agreed** (user direction and implemented source update; acceptance pending).
- Evidence: [submission](../artifacts/evidence/mlgo-source-submit.txt), [pin](../artifacts/evidence/mlgo-input-pin.txt), [latest status](../artifacts/evidence/mlgo-latest-status.txt).

## D-006 — Fat objects and native PIC coverage

- Date: 2026-11-17 proposal; historical fat-object rationale predates this date.
- Topic/options: remove fat objects; rely solely on IR fallback; validate both consumption paths and repair producers; attempt arbitrary native-code rewriting.
- Codex position: retain fat objects for GNU/native consumption; IR fallback handles only claimed bitcode. Validate native reuse separately and fix producer PIC settings where required. No demonstrated safe generic machine-code PIC repair exists in our evidence.
- Claude position: current PM review pending; [internal review prompt](../artifacts/evidence/dual-path-review-prompt.txt) awaits feedback.
- Final decision: not yet agreed. User requested a two-path design and review before implementation. No promise that every non-PIC native object fails to link; probe-specific rejection is all the matrix proves.
- Status: **Proposed**.
- Evidence: [matrix](../artifacts/evidence/arm-pic-matrix.txt), [first acceptance batch](../artifacts/pic-next-phase.csv).

## D-007 — Optimization acceptance on KantSU2E

- Date: user direction retained Nov17; historical experiment protocol predates it.
- Topic/options: adopt based on static estimates vs module target tests followed by combined image tests.
- Codex position: separate compiler, Thumb, LTO and MLGO effects; record control/candidate identities and repeated runs, then test interactions. Argot/media candidates may be bounded locally; global effects are not independently attributable to every module.
- Claude position: not yet received.
- Final decision: user requires actual KantSU2E results for every accepted optimization. No performance claim from static size alone.
- Status: **Agreed** (user direction).
- Evidence: [measurement boundaries](../handover/07_perf_memory.md), [scope](../handover/01_goal_and_scope.md).

## D-008 — Definition of done and completion percentages

- Date: 2026-11-17.
- Topic/options: infer completion from action counts vs agree eligible package/experiment scope and independent gates.
- Codex position: no defensible overall percentage today. Adopt [proposed DoD](../handover/01_goal_and_scope.md), explicit GCC/prebuilt exceptions, current build ledger, product suites and numerical measurement margins.
- Claude position: requested completion estimates; denominator/acceptance thresholds not supplied.
- Final decision: pending; report Unknown instead of invented progress. Milestone100% only means that bounded milestone.
- Status: **Proposed**.

## D-009 — Native/ABI inventory classification

- Date: 2026-11-17.
- Topic/options: count every GCC binary/static path as incompatible vs qualify source, ABI boundary and actual consumers.
- Codex position: 6770 repository RPM identities, 866 discovery candidates and nine first-phase acceptance rows are distinct from defects. Five historical ABI/export cases are documented; one explicitly concerns GCC prebuilt/Clang trivial ABI. Do not turn this into a full current affected-package count.
- Claude position: not yet received.
- Final decision: use qualified wording in draft HQ response; PM review of final wording remains pending.
- Status: **Proposed**.
- Evidence: [case ledger](../artifacts/shelf-cases.csv), [risks](../handover/08_issues_risks.md).

## D-010 — First handover execution scope

- Date: 2026-11-17.
- Topic/options: start new execution vs information gathering only.
- Codex position: export/review existing records with lightweight local checks and Git publication.
- Claude position: explicitly requested no new builds/heavy jobs in request0001.
- Final decision: no new build/benchmark/OBS mutation/device change in this round; next execution follows reviewed priorities.
- Status: **Agreed**.
