# Decision register

Checkpoint: 2026-11-17. Request 0002 records Claude’s acceptance of the initial handover. Prior user directions remain authoritative. “Agreed” historical entries mean an established user direction or implemented historical configuration, **not** that the new Claude PM has already reviewed it. Claude’s positions on D-001 through D-010 are recorded below. D-011 through D-014 remain Proposed as requested in review 0002. Exact historical decision dates are unknown where noted.

## D-001 — Coordination and storage

- Date: 2026-11-17.
- Topic/options: shared GitHub review vs scattered chat; central workspace vs dispersed outputs.
- Codex position: use public `lhmax2010/analysis` main for readable review; preserve raw inputs locally with hashes. All local generated files under `/home/toolchain/Desktop/temp`; native task files under `/home1/chengkai/vd-tree`; board additions under `/root`.
- Claude position: Agrees. D-015 extends the board rules. HQ-facing English documents omit internal tooling, review and repository references.
- Final decision: follow these boundaries; preserve prior evidence and every review/decision, update status/tracker each round. User is final authority.
- Status: **Agreed** (user-relayed workflow).

## D-002 — Compiler and standard-library baseline

- Date: historical; confirmed in retained Nov 16–17 evidence.
- Topic/options: LLVM22 Clang migration with existing GNU C++ runtime vs simultaneous libc++ migration.
- Codex position: retain current LLVM22.1.8/GCC14.2 baseline and GNU C++ interoperability until a separately reviewed runtime transition. GCC remains for approved components and native consumers.
- Claude position: Agrees. Keep GNU C++ interoperability for existing vendor libraries and TPKs. A libc++ transition requires a separate compatibility study and measured benefit.
- Final decision: existing baseline retained for handover; a global libc++ switch is not evidenced or authorized by the request.
- Status: **Agreed** (retained configuration; reviewed by Claude in request 0002).
- Evidence: [sources](../handover/03_sources_rpms_image.md), [bootstrap](../artifacts/evidence/llvm101-bootstrap.txt), [C++ smoke](../artifacts/evidence/llvm101-smoke.txt).

## D-003 — Compiler injection and linker route

- Date: historical; exact original decision date unknown.
- Topic/options: RPM compiler/macros plus package corrections vs replacing every compiler invocation; GNU linker/plugin vs global lld.
- Codex position: preserve existing Clang macros/driver GNU-plugin integration and audit actual commands. Hard-coded GCC, configure overrides and package exceptions need explicit treatment. Evaluate lld separately.
- Claude position: Agrees. GNU ld and LLVMgold remain the baseline. lld is optimization candidate O7.
- Final decision: report implemented configuration; do not claim all packages obey macros or production 10.1 acceleration is validated.
- Status: **Agreed** (existing baseline only).
- Evidence: [sources/macros](../handover/03_sources_rpms_image.md), [patch index](../artifacts/patch-index.csv).

## D-004 — Parallel 10.1 adaptation

- Date: retained user direction, Nov 16–17; exact message time unknown.
- Topic/options: sequential after10.0 vs parallel independent adaptation.
- Codex position: parallel workstreams, separate provenance and acceptance; schedule heavy jobs within confirmed capacity.
- Claude position: Agrees. 10.0 product work gets contested heavy-build slots unless the user overrides.
- Final decision: user selected parallel10.1; do not block it on10.0 or treat private ARM smoke as production acceptance.
- Status: **Agreed** (user direction).
- Evidence: [master plan](../artifacts/progress_tracker.csv), [10.1 results](../handover/05_build_status.md).

## D-005 — Customized MLGO experiment and complete SR runtime

- Date: 2026-11-17.
- Topic/options: 10.0 vs10.1 starting Base; model-only transfer vs full SR runtime adaptation.
- Codex position: 10.0 starting Base as selected by user. Full SR runtime is required by the branch adaptation; freeze the same runtime for Official/Customized comparison.
- Claude position: Agrees. Kernel MLGO remains a separate experiment and can inform kernel Clang feasibility.
- Final decision: revision12 supersedes incomplete model-only revision11. Preserve independent model/runtime switches. Wait for build/advisor/Base evidence before kernel claims.
- Status: **Agreed** (user direction and implemented source update; acceptance pending).
- Evidence: [submission](../artifacts/evidence/mlgo-source-submit.txt), [pin](../artifacts/evidence/mlgo-input-pin.txt), [latest status](../artifacts/evidence/mlgo-latest-status.txt).

## D-006 — Fat objects and native PIC coverage

- Date: 2026-11-17 proposal; historical fat-object rationale predates this date.
- Topic/options: remove fat objects; rely solely on IR fallback; validate both consumption paths and repair producers; attempt arbitrary native-code rewriting.
- Codex position: retain fat objects for GNU/native consumption; IR fallback handles only claimed bitcode. Validate native reuse separately and fix producer PIC settings where required. No demonstrated safe generic machine-code PIC repair exists in our evidence.
- Claude position: Agrees with producer-side PIC and keeping generic native rewriting out of scope. D-014 adds the review scope and the 92-RPM screening plan.
- Final decision: keep IR handling and producer-side PIC validation. D-014 records the implementation proposal. No promise that every non-PIC native object fails to link; probe-specific rejection is all the matrix proves.
- Status: **Agreed** on the core position. Follow-up policy details remain in D-012 through D-014.
- Evidence: [matrix](../artifacts/evidence/arm-pic-matrix.txt), [first acceptance batch](../artifacts/pic-next-phase.csv).

## D-007 — Optimization acceptance on KantSU2E

- Date: user direction retained Nov17; historical experiment protocol predates it.
- Topic/options: adopt based on static estimates vs module target tests followed by combined image tests.
- Codex position: separate compiler, Thumb, LTO and MLGO effects; record control/candidate identities and repeated runs, then test interactions. Argot/media candidates may be bounded locally; global effects are not independently attributable to every module.
- Claude position: Agrees. Retain target measurements and single-variable comparisons.
- Final decision: user requires actual KantSU2E results for every accepted optimization. No performance claim from static size alone.
- Status: **Agreed** (user direction).
- Evidence: [measurement boundaries](../handover/07_perf_memory.md), [scope](../handover/01_goal_and_scope.md).

## D-008 — Definition of done and completion percentages

- Date: 2026-11-17.
- Topic/options: infer completion from action counts vs agree eligible package/experiment scope and independent gates.
- Codex position: no defensible overall percentage today. Adopt [proposed DoD](../handover/01_goal_and_scope.md), explicit GCC/prebuilt exceptions, current build ledger, product suites and numerical measurement margins.
- Claude position: Agrees. The coverage denominator comes from D-012 and the acceptance rules from D-013 and D-017.
- Final decision: report Unknown until the D-012 coverage denominator and scope are supported. Milestone100% only means that bounded milestone.
- Status: **Agreed** on the core position. Follow-up policy details remain in D-012 through D-014.

## D-009 — Native/ABI inventory classification

- Date: 2026-11-17.
- Topic/options: count every GCC binary/static path as incompatible vs qualify source, ABI boundary and actual consumers.
- Codex position: 6770 repository RPM identities, 866 discovery candidates and nine first-phase acceptance rows are distinct from defects. Five historical ABI/export cases are documented; one explicitly concerns GCC prebuilt/Clang trivial ABI. Do not turn this into a full current affected-package count.
- Claude position: Agrees. Call the 56 cases synthetic test fixtures in the HQ draft.
- Final decision: use qualified wording in draft HQ response; Claude approved the wording change in request 0002.
- Status: **Agreed** on the core position. Follow-up policy details remain in D-012 through D-014.
- Evidence: [case ledger](../artifacts/shelf-cases.csv), [risks](../handover/08_issues_risks.md).

## D-010 — First handover execution scope

- Date: 2026-11-17.
- Topic/options: start new execution vs information gathering only.
- Codex position: export/review existing records with lightweight local checks and Git publication.
- Claude position: Agrees. The first handover round is closed.
- Final decision: no new build/benchmark/OBS mutation/device change in this round; next execution follows reviewed priorities.
- Status: **Agreed**.


## D-011 — Priorities for 18–20 November

- Date: 2026-11-17.
- Options: follow the proposed priority order or divert capacity to unrelated work.
- Claude position: finish the HQ PIC draft first, then refresh MLGO, capacity and coverage inputs. Progress memory, Thumb and 10.1 in parallel within capacity.
- Codex position: agree. Read-only evidence collection and the draft can overlap. Keep fixed-image identity ahead of compiler attribution.
- Final decision: proposed schedule retained. HQ draft is ready for PM review. User controls its external delivery.
- Status: **Proposed**.

## D-012 — Current image compiler coverage

- Date: 2026-11-17.
- Options: infer compiler from dependency metadata or inspect pinned payloads and source package provenance.
- Claude position: inspect installed NEVRA and ARM ELF, use DWARF when available, and count eligible source packages. Track QB health separately.
- Codex position: agree. Keep `UNKNOWN` when marker or producer coverage is incomplete. A GCC-only marker can come from CRT. Report denominator completeness and preserve multiple installed SRPM versions.
- Final decision: proposed. Observed 2,342 installed identities with exact repository metadata matches. Payload and compiler coverage are pending.
- Status: **Proposed**.

## D-013 — Scenario protocol and test margins

- Date: 2026-11-17.
- Options: fixed-board repeated scenarios or ad hoc observations.
- Claude position: fixed conditions and repetitions, case-specific metrics, median/IQR/CI, proposed 2% margin.
- Codex position: agree, with separate absolute criteria for zero or rare events such as OOM and stalls. Use paired or blocked CIs and mark wide intervals inconclusive. Lack of statistical significance alone provides insufficient evidence for adoption.
- Final decision: proposed. App list, workloads and margins are reviewed before scored runs.
- Status: **Proposed**.

## D-014 — Producer PIC and two-path validation

- Date: 2026-11-17.
- Options: targeted producer packaging flags, global ARM32 PIC, or an additional compiler option.
- Claude position: targeted packaging rule and a relocation screen validated on the 56 matrix cases, followed by the 92 pinned RPMs.
- Codex position: agree. The listed relocations are a screening signal. Record their executable target section and the real consumer. A link can fail for other relocations or ABI conditions. Keep allowlisting bound to an intended use.
- Final decision: proposed. Local ARM assembler fixtures verified the basic classifier. The complete matrix and pinned RPM check run in the native environment before counting affected packages.
- Status: **Proposed**.

## D-015 — TV board use

- Date: 2026-11-17.
- Options: use the current board under bounded tasks or require a separate device.
- Claude position: records the user's permission to test on KantSU2E, with an inventory and rollback documentation.
- Codex position: agree. New test files go under `/root/llvm-pm/<task>/`. Keep the prior test inventory and restore the original boot configuration and temporary SDB privilege.
- Final decision: board testing allowed. System partitions and package installation need D-020 scope or a separate recorded decision. Record exact rollback before image or boot changes.
- Status: **Agreed — user direction**.

## D-016 — GCC replacement scope

- Date: 2026-11-17.
- Options: explicit package evidence or historical blanket exceptions.
- Claude position: records the user's two allowed categories, GNU GCC-only or content outside the GCC/Clang build.
- Codex position: agree. Include kernel, modules, bootloader, TEE and drivers when built as RPMs and technically Clang-feasible. Record compiler, source support, risks and effort for each. Distinguish vendor prebuilts for memory attribution.
- Final decision: apply per-package evidence. MLGO kernel evidence informs feasibility while its experiment remains separate.
- Status: **Agreed — user direction**.

## D-017 — Ongoing optimization and benchmark scope

- Date: 2026-11-17.
- Options: ongoing improvement with measured gates or a fixed aggregate end target.
- Claude position: records the user's ongoing goal and the five standard scenarios, including smooth 4K under the physical 1 GB budget.
- Codex position: agree. Rank memory candidates after attributing file-backed code and rodata, relocation-dirty pages, anonymous memory and kernel/slab/media buffers. Compare prelink variants only on matched controls.
- Final decision: require improvement in at least one scenario with regressions within agreed margins elsewhere. Treat 4K at 1 GB as a stress benchmark and continue ranked work after passing.
- Status: **Agreed — user direction**.

## D-018 — Native capacity and mutation boundaries

- Date: 2026-11-17.
- Options: 4–8 tasks with measured capacity or unconstrained parallel runs.
- Claude position: records the user's 4–8 task envelope and asks for a concrete capacity rule after a read-only refresh.
- Codex position: agree. Until refresh, start the proposed four-slot tier with at most one heavy and one package build concurrently when headroom allows. Count scans among tasks. Confirm actual limits using the capture.
- Final decision: agreed package builds, scans and measurements may proceed within capacity. OBS mutations, shelf/CL submission and formal manifest changes require a recorded decision.
- Status: **Agreed — user direction**.

## D-019 — Earlier-account results

- Date: 2026-11-17.
- Options: reproduce from retained inputs or carry forward unverifiable results.
- Claude position: records that the earlier account records cannot be retrieved and requests reproduction.
- Codex position: agree. Use the 27-file retained scan as its own labelled baseline. Preserve the original 106 as an unverified historical reference where image, threshold and inputs cannot be pinned.
- Final decision: reproduce before using any result unique to those lost records. Redo against current scope if original inputs are unavailable.
- Status: **Agreed — user direction**.

## D-020 — 1 GB condition on KantSU2E

- Date: 2026-11-17.
- Options: reversible reservation first, then a boot-map limit with proven rollback.
- Claude position: records the user's physical budget, Method A first and matched A/B comparison.
- Codex position: agree with ordering. Map the relevant carveouts and verify which pools are needed for the actual 4K path before calculating the target. Start with a bounded reservation pilot. Require a free-memory floor, predictable teardown and a tested root execution path before issuing a large lock.
- Final decision: capture current memory and reservations first. Method A is a pressure approximation. Method B needs exact address ranges, a saved boot environment and a verified reflash/restore path. Compare three matched runs per method before selecting routine use.
- Status: **Agreed — user direction**.
