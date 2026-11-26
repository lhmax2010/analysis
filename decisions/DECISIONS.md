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
- Codex position: agree. Keep `UNKNOWN` when marker or producer coverage is incomplete. A GCC-only marker can come from CRT. Report denominator completeness and preserve multiple installed SRPM versions. Publish the lower bound CLANG / eligible and upper bound (CLANG + UNKNOWN) / eligible with explicit Unknown and the eligible denominator. If package eligibility is also unknown, report counts and the unresolved denominator.
- Final decision: proposed. Observed 2,342 installed identities with exact repository metadata matches. Payload and compiler coverage are pending.
- Status: **Proposed**.

## D-013 — Scenario protocol and test margins

- Date: 2026-11-17.
- Options: fixed-board repeated scenarios or ad hoc observations.
- Claude position: fixed conditions and repetitions, case-specific metrics, median/IQR/CI, proposed 2% margin.
- Codex position: agree, with separate absolute criteria for zero or rare events such as OOM and stalls. Use paired or blocked CIs and mark wide intervals inconclusive. Lack of statistical significance alone provides insufficient evidence for adoption.
- Absolute event rule agreed in 0003: a new crash, LMK/OOM kill, ANR or audio/video underrun signature in the scenario is a regression independent of CI. Record per-zone free/min watermarks during playback.
- Final decision: proposed. App list, workloads and margins are reviewed before scored runs.
- Status: **Proposed**.

## D-014 — Producer PIC and two-path validation

- Date: 2026-11-17.
- Options: targeted producer packaging flags, global ARM32 PIC, or an additional compiler option.
- Claude position: targeted packaging rule and a relocation screen validated on the 56 matrix cases, followed by the 92 pinned RPMs.
- Codex position: agree. The listed relocations are a screening signal. Record their executable target section and the real consumer. A link can fail for other relocations or ABI conditions. Keep allowlisting bound to an intended use.
- Final decision: proposed. Local ARM assembler fixtures verified the basic classifier. The complete matrix and pinned RPM check run in the native environment before counting affected packages. Claude schedules T7 review for Thursday, with refresh after T6.
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
- Final decision: capture current memory and reservations first. Method A is a pressure approximation. Method B needs exact address ranges, a saved boot environment and a verified reflash/restore path. Compare three matched runs per method before selecting routine use. In the attended session ramp through 16, 64, 256 MiB and the validated target as applicable. Skip increments above the target. Monitor dmesg/LMK, MemAvailable, LowFree/HighFree, per-zone free/min and 4K playback. Release the holder immediately after a system-process LMK kill, watchdog warning or playback failure. Verify the actual lowmem/highmem split rather than inferring it from allocation flags.
- Status: **Agreed — user direction**.


## D-021 — Official versus Customized kernel MLGO this week

- Date: 2026-11-17. Round 0004 updates scope and submission conditions. Due Friday 20 November.
- Options: frozen image Base substitution with kernel measurements, user-space identity control, and future same-toolchain model attribution.
- Claude position: use 1113.1 as Official and 1118.1 as Customized. The historical report identifies Linux kernel as the MLGO consumer and user space as the identity control. Submit after both binary pins and the expected Base-list diff. The kernel gate determines interpretation.
- Codex position: agree. Current TV boot confirms Clang/LLD-built Linux 6.12.60 with tztv-kernel-perf. The pinned shelf 14427407 describes both release switches in Kbuild. Check pinned sources and recover effective command and Base clang provenance in each job.
- Final decision: keep Product, build.conf, shelves and saved QB inputs fixed. Prioritize the native preflight. Verify rebuilt kernel artifacts, Image/vmlinux/modules, five boots, kernel microbenchmarks and three 4K runs per lane. Compare user-space ELF hashes and list every confounder. Defer global release flags and same-rev12 macro 0/1 rebuilds.
- Status: **Agreed — user direction**. This replaces the earlier advisor-as-submission-gate interpretation.

## D-022 — ARM-mode evidence and Thumb transition

- Date: 2026-11-17. Requested HQ follow-up by Wednesday 25 November.
- Options: mapping-symbol baseline, coverage-weighted dynamic function symbols, matched debuginfo and retained build-tree objects.
- Claude position: combine methods per file, identify ARM-mode causes, measure paired size results and run Bluetooth and DRM regressions.
- Codex position: agree. Sized dynamic symbols establish lower bounds. Use a conservative threshold with unknown bytes, union aliases, and verify debuginfo by Build ID and actual section/symbol evidence.
- Final decision: proposed. Round 0004 withdraws the unsent Appendix A. The forthcoming user scan over 2,342 installed RPMs supplies the working cohort using mapping symbols and a labelled condition-field heuristic. Keep prior dynsym output as historical. Recover actual per-file invocations and source evidence. Verify argot target and candidate ABI before any one-change board experiment.
- Status: **Proposed**.


## D-023 — Terminal text transport for native and TV work

- Date: 2026-11-17, round 0004.
- Topic: return evidence as terminal text because the operator cannot transfer files from native.
- Codex position: prefer compact result lines within 300 lines. Encode longer structured outputs as zlib+base64 with SHA-256, using numbered parts when needed. Retain the original native artifacts within vd-tree and give explicit terminal print commands.
- Final decision: apply to all new native/TV commands. Earlier file-return instructions are historical where superseded.
- Status: **Agreed — user direction**.

## D-024 — Review and pin native and TV launchers

- Date: 2026-11-17, round 0004 addendum.
- Final decision: commit scripts under `artifacts/scripts/r0004/`. Claude reviews the script commit before sending native launchers. Use full commit pins and SHA-256 verification, compact terminal output, native Python 3.10 and retained results under vd-tree. Apply this to A and B as well as the new tasks.
- MLGO: use the repaired preflight with `xz -dc`. The two binary pins and expected Base-list diff govern QuickBuild submission. Kernel source and actual job evidence govern interpretation.
- ARM scan: stage the two PM inputs byte-identically and run a single background job with eight downloads when the operator launches it. Codex accepts the scan for candidate discovery. Build IDs, mapping coverage, extractor status and effective compile commands are needed for HQ attribution.
- Status: **Agreed — user direction**. Scan methodology counter-position and native results are pending review.

## D-025 — Friday kernel MLGO model identity replay

- Date: 2026-11-17, round 0004 model-identity addendum.
- Final decision: compare both fixed Base compiler payloads on selected pinned kernel TUs and the shared probe. Use release/release, release/default, default/release and default/default. Report every unexpected outcome, along with compiler and object hashes and optimization-record counts.
- Verify Customized clang RPMs against the preflight pins and identify the actual kernel job's x86_64 executable by hash. Keep the ARM compiler under QEMU as a separate role. Preserve LTO IR evidence and identify separate native codegen replays.
- Status: **Agreed — user direction**. Native launchers use GitHub downloads only. Friday results and Claude review are pending.

## D-026 — Standalone replay, Product comparison and attended board runs

- Date: 2026-11-18, round 0004 replacement for G discovery.
- Final decision: stage vdlinux 14293732 with shelf 14427407 using read-only Perforce. Use pinned Base RPM payloads and a fresh perf defconfig plus Kbuild prepare. Replay fixed kernel TUs and the probe in all four modes. Run native heavy work serially.
- The candidate QuickBuild has started using 20261118.1 and the other QB 37627297 inputs per the operator. Capture its ID and candidate Product URL once available. Compare the 2,342 baseline-installed package identities, preserving all changed ELF paths and confounders.
- Prepare reviewable KantSU2E boot, microbench and 4K collectors. Follow the attended flash and rollback checklist after verifying the approved board-specific procedure and known-good bundle. Keep measurements pending until collected.
- Status: **Agreed — user direction**. Native GitHub access is download-only.

## D-027 — Round 0005 evidence gates

- Date: 2026-11-18.
- Resume OBS binary pinning using the successful read-only Python transport and exact published RPM digests. Keep validated Base-list and source status evidence separate from binary equality.
- Pair non-LLVM before/after rows and join the exact installed roster. Use the resulting categories in the image ELF comparison. Preserve all unresolved package and payload evidence.
- Close the T5 REST route after the account's HTTP 403 responses. Accept a web UI export if provided.
- Qualify PIC members by bytes and consumer. Start the full compiler-marker proposal after review and after the running ARM/Thumb scan finishes. Continue per-file cause attribution once its complete roster arrives.
- Status: **Agreed — user direction**. Live readbacks and candidate QB artifacts are pending.

## D-028 — Source-level kernel gate and argot Thumb attribution

- Date: 2026-11-18, round 0005 addendum.
- Record the passed MLGO source gate on pending shelf 14427407. With the QB log unavailable, use the changed kernel payload and the user-space ELF comparison against the item 2 Base delta for Base-swap attribution. Retain the limits on effective compiler and model-only evidence.
- Trace cargo-tizen from the actual selected argot build sources. Preserve the resolved target, ABI and linker. Prefer the same-target Thumb feature if the baseline emits A32 and the candidate preserves the ABI. Use a supported same-ABI Thumb target only after isolating the instruction-mode difference.
- Status: **Agreed — user direction**. Config resolution, image comparison and native results are pending.

## D-029 — KantSU2E board-day gates

- Date 2026-11-18, round 0005 section I addendum.
- The operator supplied the full USB flash sequence for KantSU2E. Confirm the artifact and USB hashes, exact running image identity and recovery access. Review the captured output before proceeding from each step or trial.
- Preserve Official results on the native host before changing the image. Reuse the benchmark binary and verified media clip across lanes. Report frame drops as unavailable until the active stream counter is proven.
- Interpret the 1113.1/1118.1 Base swap with the source gate, exact artifacts, workload dependencies and the observed confounder ledger. A controlled model-only build pair is a separate experiment.
- Claude review and live execution are pending. [Board-day checklist](../reports/KantSU2E_MLGO_Board_Day_0005.md)


## D-030 — Verified Base pins and native consumer classification

- Date 2026-11-18, Round 0005 results.
- Accept the published 1118.1 Clang RPM byte pins on armv7l and x86_64 at OBS rev12. Source lines 1065–1070 confirm both conditional release-advisor assignments in `KBUILD_CFLAGS`. Actual QB compiler/argv and image-level attribution remain open.
- Use the 177-of-2,342 installed name/arch overlap to prioritize the image check. Keep ambiguous pairs and same-NEVRA payload changes visible. The classifier found zero resolved version or epoch changes.
- Supersede D-028's platform-build assumption for the argot client and TPK. Classify their ARM-mode cause as PREBUILT. Change instruction mode in the artifact owner's cargo-tizen build after verifying the exact Rust target, build job and ownership. The Meson `argot-platform` library remains a separate build lane.
- Track the Clang FatLTO/native relocation hit and the four TLS-local-exec static archives in T7 with their final-link consumers. Classify kernel modules separately in T4 and keep the marker evidence within that class.
- Kernel replay is running at the P4 print stage. [Native evidence](../artifacts/evidence/native-run-r0005-20261118.txt)


## D-031 — Run build and link validation in GBS roots

- The user requires compiler and linker execution inside GBS. The host replay is superseded. Its unpublished accelerator patch remains outside the published branch.
- Reproduce the pinned VD kernel package in two serial, isolated GBS roots with the same QB 37627297 Product configuration and source shelf. Capture effective local Kbuild argv, root compiler binary and RPM identities and derived artifact sizes. Preserve the distinction between local GBS evidence and the unavailable production QB log.
- T7 links the byte-identified CAPI member and the four other TLS archives inside a GBS probe package. Compare native GNU ld, Gold/LLVMgold and the CAPI runtime thread checks. Consumer link maps and actual outputs determine impact.
- Argot ownership is the CODEOWNERS team `@AGENTIC/argo-tizen-maintainers`. The retained submitter is `youngb.shin`. Run the pinned CI/config readback before declaring the ARM triple or Thumb setting. [Native input](../artifacts/evidence/native-run-r0005-pic-accel-argot-20261118.txt)


## D-032 — Resume the GBS kernel and verify Thumb causes

- Resume the retained pre-build vdlinux workdir with the recorded spec and defconfig hashes and 24 shelf actions. Write-enable only the staged spec before applying the existing trace. Run GBS in an attended foreground terminal.
- The completed scan is the 609-file ARM-predominant roster. Treat GCC/Clang/Rust marker strings as screening evidence. Test compiler defaults with the effective GBS flags/config and match the actual compilation and linked artifact before assigning each cause.
- Require three paired, cause-(i) GBS measurements before a code-size extrapolation. Keep estimated executable bytes distinct from resident memory. [Native evidence](../artifacts/evidence/native-run-r0005-argot-scan-gbs-20261118.txt)


## D-033 — Report the real QuickBuild pair

- The operator reports Customized QB 37654439 completed on Base 20261118.1. Official QB 37627297 on Base 20261113.1 remains the control.
- Friday prioritizes the published Product comparison and matched full-image board measurements. The local GBS resume supplies effective local compiler argv after the comparison releases the heavy lock. Its spec-permission fix remains in scope.
- Compare the two QB-specific GBS configs exactly after substituting the expected Base and Product URLs and local buildroot. Record any unexpected change.
- Obtain the versioned KantSU2e full-image download link for each QB. Download Official for rollback first, under the same heavy lock. [Fixed inputs and read-only check](../comms/codex_to_claude/0005_reply.md#published-quickbuild-pair)


## D-034 — Qualify the published image differences before attributing performance

- Use the retained 2,342-package comparison as the fixed scope for section qualification. Preserve the three unresolved RPM identities. Verify every re-read RPM and ELF against its recorded SHA-256. Existing local RPM caches are read-only. Re-fetch only missing matched RPMs, serially, after the heavy slot is free.
- Record the four published kernel sizes. Inspect the exact packaged vmlinux before inferring section composition. Report board metrics as whole-image observations while user-space parity and production inputs are unresolved.
- Stream the pinned PERF inner tar inventory. Confirm the genuine full flash artifact before applying the USB/BOOST procedure. [Native comparison result](../artifacts/evidence/native-run-r0005-image-compare-20261118.txt)

## D-035 — Qualify kernel replay and packaged BTF

- Count the completed local GBS builds as supporting argv, tool and linked-ELF evidence. Preserve the distinction between same-size local/QB uImage files and any later SHA match. Require a model-only controlled comparison before attributing causality to changed advisors.
- Record the Official pair as the VD-bundled reference AOT inliner and eviction models. Keep content identity with upstream weights unresolved. Record raw BTF type and string byte growth separately from linked code and device memory. [Friday report](../reports/MLGO_Official_vs_Custom_20261120.md)

## D-036 — Join Thumb evidence by exact packaged members

- Preserve the 609-file cohort and keep ELF producer markers, packaging origin and ISA cause separate. Collect exact historical logs before serial GBS sample builds. Log failures per action, and use the actual prefixed Clang driver and effective mode order. Keep the full ELF section scan in its existing heavy slot. [Origin ledger](../artifacts/ledger/thumb-producer-origin-20261119.md) [Round 0006](../comms/codex_to_claude/0006_reply.md)

## D-037 — Retain QuickBuild artifacts on completion

- For every QB the project depends on, immediately save the immutable Product and Base identities, submitted configuration and source manifests, checksummed repository metadata and package ledger, and the exact KantSU2E PERF image under `vd-tree/workspace`. Retain the exact kernel RPMs and any priority comparison payloads while the publication still exists. Record SHA-256, size, source URL, QB ID and whether each digest was supplied or computed at download. Keep the prepared `updateSU2E/` and its file-level manifest separately under the QB ID for rollback. D-041 records the flat-bundle procedure.
- The 20261117.2 Official Product root, PERF tar and kernel RPM returned HTTP 404. Complete the scoped static comparison from the retained ledgers. Matched board work requires the exact archived pair or a newly captured pair. [Availability evidence](../artifacts/evidence/native-run-r0007-clangcfg-gccwrapper-qb404-20261120.txt#L24)
- Status **Agreed — user direction**.

## D-038 — Rebuild the matched MLGO image pair

- Keep build.conf 14452507, the unchanged no-prelink Base list and the 930-entry ltoexp2 shelf list. Product (GCC) sources are fixed for this work and can only be adapted through LLVM-side shelves. QuickBuild exposes no Product changelist pin. Submit both LLVM jobs at the same time with identical inputs except the Base URL (Official 20261113.1 and Customized 20261118.1). Save the effective publication identities and package-source join to detect any drift.
- Round 0008a confirms that the historical pair also changed the published Product build.conf. Official used `@14452507`, and the Customized publication matches the older `@14431365` digest. Round 0009 binds both revisions to the published build records and confirms the single LTO-exclusion line. It adds five Customized exclusions. Four correspond to 45 of 50 changed ELF rows and all +1,379,302 bytes of positive .text growth. Both new submissions use `@14452507` and the same shelf list. Verify the published build.conf bytes before interpreting the results. Published source identities match for those nine packages. Remaining Base-driven differences may still appear in the replacement pair.
- The operator confirmed that ASAN is part of the job name and the PERF image is uninstrumented. Close the sanitizer gate on that statement. Spot-check up to ten ELF files from the completed Customized capture. The check does not block submission.
- Status **Agreed — updated by user direction in round 0008**. Retain the earlier input comparison as a historical reference. Capture both new jobs under D-037. [Round 0008 handoff](../comms/claude_to_codex/0008_pm_review.md)


## D-039 — Measure a scoped Clang Thumb default first

- The observed GCC wrapper appends ISA, optimization, hardening and warning options in the tested GBS root subject to its exemption/escape paths. Separate this from historical production configuration evidence and the unwrapped compiler default. The Clang probe confirms A32 without the ISA flag and Thumb with platform flags.
- First test a one-option armv7l Clang config experiment on source-verified C/C++ samples, preserving any explicit `-marm`. Keep assembly and kernel controls. Evaluate per-package ISA-only propagation where appropriate. Keep an appended ISA force rule as a separately reviewed experiment because it would override explicit package mode selections.
- Status **Proposed for Claude review**. No global policy or OBS change authorized by this record. [Wrapper evidence](../artifacts/evidence/native-run-r0007-gcc-force-wrapper-20261120.txt) [Measurement plan](../comms/codex_to_claude/0007_reply.md#thumb-experiment)


## D-040 — Trial and enforce native shared/PIE PIC policy

- Keep the tagged regular-LTO IR fallback. Use LLVM migration shelves to repair reusable native objects. Baseline PERF for dynamic text relocations and observable DSO local-exec TLS before trialing armv7l `-z text`. Qualify the actual native or plugin consumer, require narrowly documented exceptions and verify the final image.
- Status **Proposed for Claude review**. The GBS GNU ld 2.43 native fixture verified successful TEXTREL output under default and rejection under strict mode. The design is ready for HQ review while the flat-PERF baseline remains the first acceptance gate. [HQ design](../hq/PIC_FatLTO_Dual_Path_Design.md)


## D-041 — Prepare KantSU2E USB from flat PERF captures

- Verify the captured archive and stage its regular flat files under `workspace/usb/<QB_ID>/updateSU2E/`. Use `do_not_use.img` as `data.img` and use `dtb_RW.bin` as `dtb.bin`. Retain a per-file SHA-256 manifest beside the folder and recheck the copied USB contents.
- Retain and verify Official rollback before any flash. Pause at the BOOST `mmc` menu before choosing `a`.
- Status **Operator procedure confirmed**. Native preparation and board acceptance pending. This supersedes the earlier nested-tar assumption and single-file lookup. [Operator procedure](../artifacts/evidence/native-run-r0008-ldprobe-forensics-usbmethod-20261120.txt#L1)

## D-042 — Pilot Thumb via the existing Clang config hook

- The exact `clang-force-options-1.0.0-1.1` armv7l RPM matches across both Bases. Use the same preinstall/run hooks in both EXP-T1 lanes and change the helper option list from empty to `-mthumb`. Explicit `-marm` keeps precedence. Run only the three pinned user-space sources against one live reviewed Product and Official Base 1113.1.
- Verify the PERF kernel mappings and argv, then run the serial pilot. Keep the kernel and external-module sources out of both builds and out of any later QB rollout through a complete source-package exclusion list. Treat SERET-UL as a distinct GCC-built migration candidate.
- Run the separate EXP-Z1 strict-link option later, with baseline and actual final linker argv. Capture bypasses and overrides.
- Status **Proposed for Claude review**, supplementing D-039 and D-040. [Trial design and evidence](../comms/codex_to_claude/0009_reply.md#exp-t1-clang-thumb-default)


## D-043 — Preserve weekly reports verbatim

- Put the supplied originals and checksum manifest under `reports/weekly/<YYYY-MM-DD>/`. Verify all manifest entries before commit, and index the directory in the reports README. Evidence-based corrections belong in working or follow-up reports.
- Status **Agreed**. The 20 November archive is complete. [Archived report](../reports/weekly/2026-11-20/README.md)

## D-044 — Attribute optimization level and ISA separately

- Map Doc 04 by installed RPM header SOURCERPM. Use the same sources and locked Official environment for A/B/C. A is unchanged, B only appends `-Os`, and C replays the verified historical hook when available. Compare ELF sizes and DWARF producer flags, and maintain libgcrypt's intentional low-level production cases. Default Thumb remains the separate EXP-T1 measurement.
- Keep the top-211 historical report values traceable and qualify remaining evidence with the exact native scan. Treat family-wide causes and measurements as pending until verified.
- Status **Accepted for round 0010**. [Round 0010 reply](../comms/codex_to_claude/0010_reply.md)

## D-045 — Attribute the matched MLGO run to the Base swap until the package proof returns

- Preserve the original weekly archive and add approved corrections as separately hashed revisions. Use the installed NEVRA comparison, same-NEVRA candidate digest differences, the exact LLVM SRPM contents, accelerator changes and user-space ELF evidence to qualify attribution. Archive the next report under the 27 November date.
- Status **Agreed on attribution and archive scope**. Claude approved the native proof after both Step 1 captures in round 0010f. [Round 0010b reply](../comms/codex_to_claude/0010b_reply.md#matched-qb-mlgo-base-package-proof)

## D-046 — Reuse the recovered historical hook and preserve its build evidence

- Keep the recovered single-line expanded hook as the historical lane C input. It carries Thumb and other policy changes alongside -Os. Continue using separately controlled runs for the individual effects. Require the reconciled 22-source roster before R1–R7. Preserve the z901 experiment directories and GBS package logs in storage cleanup.
- Confirm the tvs-core alias with the matching shelved or submitted spec in Monday step 8. Keep the exact A32 rank/basis and retail inclusion pending their respective evidence. Test the two selected Crosswalk packages independently before assigning a common build-rule cause.
- Status **Historical hook recovered**. Native alias scan and launcher review pending. [Round 0010b reply](../comms/codex_to_claude/0010b_reply.md)

## D-047 — Measure the Thumb option separately from the complete hook

- Use the verified native hook for C. For the seven A32 sources, compare unchanged A, -Os B, complete hook C and -Os plus Thumb D. Record effective flags and four A32 shares. Treat historical WARN results as such until the paired ELF readback and FINAL builds qualify them.
- Record exp8's 25 candidate sources and 153 variants. Keep the exact 22-source historical scope and the original treatment injection open until proved. Retain the exp8 paths, RPMs and GBS logs.
- Status **Claude approved the pinned Step 8 launcher in round 0010f**. [Step 8](../comms/codex_to_claude/0010c_reply.md) [Exp8 evidence](../comms/codex_to_claude/0010e_reply.md)


## D-048 — Apply the 0010f report gates

- Run the approved exp8 modes in order: verbose, pairs, treatments, and optional sizes after heavy jobs. Tie each result to its variant and report row. Leave unproved injection strings unset.
- Require a named source variable and actual argv for the Doc 07 CFLAGS attribution. Keep Doc 04 rows 2–3 labeled WARN until complete matching experimental pairs establish parity or FINAL lane results replace them.
- Use “Installed in the PERF image (debug tooling)” only for an installed identity in Doc 05. Keep retail coverage in the internal ledger.
- Status **PM review received and recorded**. [Review and report gates](../comms/codex_to_claude/0010f_reply.md)


## D-049 — Use the published GCC no-prelink reference for new HQ comparisons

- Use QB 37564293 with LLVM Official QB 37736448 for Docs 04–07. Keep the GCC and LLVM Base-series difference and ten-day Product separation in the report. Display source-different or unproved package rows with raw measures and exclude them from matched totals.
- Use new Official 37736448 and Customized 37736427 for the MLGO chain. Require submitted manifest evidence, matching published build config and Product source review before a source-matched claim.
- For a future GCC build, validate that every local repository resolves to a dedicated empty path under the GCC run workspace. Reject LLVM buildroot paths. The historical gccL configuration remains unproved.
- **PM decision recorded**. New tools await review and native input. [Round 0011](../comms/codex_to_claude/0011_reply.md)


## D-050 — Keep the HQ comparison off the board critical path

- After the reference capture and USB staging, run a serial overnight GCC scan, LLVM scan and comparison. Schedule Step 8 after that batch exits. Keep the Base proof in its own heavy-job slot.
- Use only MATCHED rows for HQ totals. Report raw bytes in TSVs and bytes/KiB in the comparison summary. Report both image prelink counts and any paths that carry a marker.
- Keep FILE-symbol-supported LTO review candidates separate from stripped and inconclusive pairs. Verified build-log evidence may qualify a candidate for manual review.
- **PM order recorded**. The updated HQ launcher and output rules await Claude review. [Round 0011a](../comms/codex_to_claude/0011a_reply.md)

## D-051 — Use the captured pair and qualify historical treatment delivery

- Record Official 37736448 and Customized 37736427 as captured. Use the published `build.xml` Base selectors and Product source ledger for Step 2, with the separate MLGO Base proof before a model-only claim.
- Use the measured PERF vmlinux ISA and retained compile argv for the EXP-T1 pilot gate. Keep the kernel and external-module exclusion. Record config symbols separately when the generated config is recovered.
- Keep Doc 04 rows 2–3 as historical lane C with WARN provenance. Their supporting check covers seven matching `.text` hashes from AVControl and libpisa-ipc. Retain the eight-ELF tv-viewer payload scope separately from the historic installed scope.
- Qualify R1–R7 by effective compile/link evidence and measured output on the same ELF scope. A size match alone leaves the effect and delivery unresolved. Preserve the R2–R6 execution gate and the exact historical hooks. Submit the scoped replay delivery routes for review.
- **PM instructions recorded and interpreted against native evidence.** The new evidence readback and proposed recipe routes await Claude review. [Round 0011b reply](../comms/codex_to_claude/0011b_reply.md)

## D-052 — Accept the Step 2 source match and finish the native chain first

- Step 2 passed for Official QB 37736448 and Customized QB 37736427. Accept the published Base selectors and all 5,880 same-source Product identities. The parallel build-input comparison is now a source-matched LLVM Base swap. Model-only attribution awaits the Base payload and dependency evidence.
- Record Claude's acceptance of 0011a and 0011b. Keep the operator's running chain intact and verify each job's completion signal. Use the two verified USB stages for board Step 5. Schedule the approved overnight batch after the chain and board slot. Run Steps 9 and 8 after the batch exits. [PM review](../comms/claude_to_codex/0011c_review.md) [Step 2 evidence](../artifacts/evidence/native-run-r0011-step2-pair-gate-20261124.txt)

## D-053 — Archive live HQ exports and use verified download retries

- Claude authors and updates the live HQ docs. Put proposed wording in round replies. Archive each supplied live export verbatim with its checksum. Retain repo-authored Doc 02 rev3 as superseded by the live rev4 export.
- In native launcher `get()`, allow up to five attempts, with a 15-second connection timeout, a 120-second transfer timeout and 10 seconds between failed attempts. Require SHA-256 verification before using a downloaded file. Record failures with the attempt and filename.
- Read status from the exact launch directory. When a lookup is unavoidable, select by modification time. The active chain for 0011c is `pm0011c-chain.AFkXQV`. [PM review](../comms/claude_to_codex/0011d_review.md) [Current reply](../comms/codex_to_claude/0011d_reply.md)

## D-054 — Use both staged USBs and keep within-Base attribution open

- Use the verified staging manifests for Official QB 37736448 and Customized QB 37736427. Keep an alternating per-lane board schedule and preserve native copies of each visit, both board RPM rosters and one combined measurement file per lane.
- Keep the source-matched Base-swap attribution. Exact historical LLVM SRPMs, same-QB RPM rosters and executed Clang/libLLVM provenance qualify the comparison inside the Base. Compare verified linked ELF sections before carrying replay results into the matched QB table.
- Capture GCC reference 37564293 as the overnight input. Hold its kernel RPM comparison for a source-identity check. Run the overnight batch after Step 5 staging releases the shared lock, then Steps 9 and 8. [Round 0011e results and runbook](../comms/codex_to_claude/0011e_reply.md)

## D-055 — Run board-free development in one heavy slot

- Use Official 37736448 and GCC no-prelink 37564293 for the static baseline. Keep the kernel and external-module exemptions for T1. Require observed compiler and linker delivery and exact output scope before a no-effect result.
- Trial strict final links before any production rollout. Identify a failing object and its producer before proposing a shelf. Retain native and plugin link maps, ABI source status and runtime gaps. Keep the gating order for R2, R6 and the link-only R3 diagnostic.
- Run the r0011f rev2 diagnostics independently of board staging. Use the fixed Step 5 source package after the heavy slot is clear. Reuse one hashed benchmark binary in both board lanes.
- Archive Source1005 and the independent review request. Treat the retained OBS source match and direct SRPM member verification as separate evidence.
- **PM direction recorded.** Implementation and local tests complete for the staged entry points. Claude review and native results are pending. [Development queue](../comms/codex_to_claude/0012_reply.md) [Independent review](../comms/codex_to_claude/0012a_reply.md) [Step 5 repair](../comms/codex_to_claude/0012b_reply.md)

## D-056 — Qualify Thumb-2 on the complete Official image

- Use a fresh Official 37736448 baseline, one package-fix lane preserving package flags, and an independent scoped default lane. Keep explicit A32 controls, kernel and external-module exemptions. For A32 cause shares record verified mapped ranges, source owner and unknown bytes. Gate each proposed package on T1–T8. Measure runtime and soak when boards return. Keep this week's kernel trial local. PM decides on any future QB. [Scope and decisions](../comms/claude_to_codex/0012e.md)
- Share checksum- and filesystem-verified image extraction across roster, ABI, TEXTREL and compiler audits. Keep the within-Base model attribution open until direct package evidence returns. [Batch evidence and updated review](../comms/codex_to_claude/0012c_reply.md)

## D-057 — Require actual driver, LTO and kernel evidence before reporting the scoped Thumb trial

- Adopt Claude’s run order and preserve the earlier approved pin for Step 5 and Wed-A. Gate the next Wed-night pin on the verified Official image cause ledger. Classify applicable old assembler failures as F1.
- Pair the scoped Thumb default with driver-level implicit IT, verify actual driver selection, preserve explicit ARM overrides, and qualify newly enabled LTO under the ABI rule. Maintain libpisa’s -Werror. Trace tv-viewer C and C++ separately.
- Test machine outlining with the Official kernel advisors in the existing Thursday job. Require the matched source and full effective perf config, real TU advisor diagnostics and observed output before drawing a conclusion. Preserve linked ELF and BTF provenance separately. [PM instructions](../comms/claude_to_codex/0012g.md) · [Review handoff](../comms/codex_to_claude/0012g_reply.md)

## D-058 — Stage one verified benchmark and qualify the build-root probes

- Use coreutils 6.9 and gawk 3.1.5 as the compatibility floor for injected commands. Gate on the commands in the real build root. Verify an owner before relying on mktemp. Record both Base RPM and linked archive digests and the actual CRT search paths. One accepted binary serves both board lanes. [Step 5 review](../comms/codex_to_claude/0012h_reply.md)
- PM’s Wed-A approval for b048780 supersedes the earlier 0a4e9ec pilot. Run the matched image readback after Wed-A exits. Capture each observed GCC-family compile line under T1 and F2. A scoped Clang lane with a loaded config missing either marked ISA option requires a targeted F6 rerun. Await matched causes before a Wed-night pin and separate PM approval before Thursday’s kernel trial. [PM decision and operation order](../comms/claude_to_codex/0012i.md)

## D-059 — Official O1 board visit

Keep Official QB 37736448 flashed for Step 5. The operator performs the cold boot and times Home readiness. Accept the three idle readings at Home +5/+6/+7 minutes on that boot. Retain the post-flash sample separately. [Operator instruction](../comms/claude_to_codex/0012j.md) · [O1 measurements](../comms/codex_to_claude/0012j_reply.md)

## D-060 — Official config provenance and kernel outlining

PM accepted 0012j. Check the published boot images for IKCONFIG first. Accept a same-build perf devel config only with the package identity and corroborating kernel build identity, and label its provenance. For K1, K3 and K5, require native pre-link machine outlining evidence, check kernel LTO and retain the final LLD argument vector. [Direction](../comms/claude_to_codex/0012k.md) · [Evidence](../comms/codex_to_claude/0012k_reply.md)

## D-061 — K0 qualifies the same-build perf candidate

0012l extends D-060: use the exact perf header config in the pinned devel RPM as a candidate. Promote it to the Official perf build config only after K0 reproduces its bytes and the required outputs. Report Thumb/unwinder changes together, retain each lane’s symbol files by GNU build ID, and require a symbolized on-target trace through an observed site. The new Thursday pin is submitted for review. [PM decision](../comms/claude_to_codex/0012l.md) · [Review packet](../comms/codex_to_claude/0012l_reply.md)

## D-062 — Build-root shell floor and baseline qualification

Apply Bash 3.2.57, coreutils 6.9 and gawk 3.1.5 compatibility to injected shell. Require foreground AVControl baseline compile/link forwarding proof and a built RPM before expanding to three lanes or starting K0–K5. Step 5 rev3 supplies one immutable benchmark for both board lanes. [0012m](../comms/codex_to_claude/0012m_reply.md)

## D-063 — Matched outliner comparison and measured boot artifact

The HQ kernel is a reference. Use qualified KantSU2E K0–K3 for the advisor interaction, report compressed and uncompressed images independently, and require an active boot route joined to bytes on the board for flash attribution. Keep uncovered DWARF origins and unavailable live memory observations explicit. [0012n](../comms/codex_to_claude/0012n_reply.md)

## D-064 — Custom warm-boot observation and 0012r native gates

Record the authorized single software reboot as C1 warm. Keep the O1 cold and earlier 117-minute C1 idle observations distinguishable. The 178 installed release changes limit interpretation of board timings to the Base swap. PM review precedes the new image run and kernel batch. [Request](../comms/claude_to_codex/0012r_codex_c1_reboot_image_lto_kernel_disk.md) · [Reply](../comms/codex_to_claude/0012r_reply.md)

## D-065 — 0012s/t kernel and image sequencing, 25 Nov

Run the six GBS kernel lanes against the successful standalone source record from pm0012-image.mKv04z. Retain the image-dependent external-module membership gate. Audit both platform partitions with pinned 1.9.4 host binaries and a metabox inline-byte fixture before AVControl acceptance. The Official/Custom board readings remain Table A. Use GNU build-ID-matched kernel ELFs for the independent section cross-check. GCC values require the corresponding GCC sources of evidence. [Review and commands](../comms/codex_to_claude/0012t_reply.md)

## 0012u · GCC board-reference provenance

User-approved method: admit GCC image-derived Data, BSS and init only after the same print-site procedure reproduces the observed Official and Custom triplets exactly. Both controls passed. Text and rodata retain the live inclusive physical-range definition. The GCC comparison spans different Product and Base snapshots at the same kernel source CL. [Instruction](../comms/claude_to_codex/0012u_method_validation.md) · [Result](../comms/codex_to_claude/0012u_reply.md)

## 0012v · G1 whole-board comparison and upstream extractor

User requested a single warm series and the same C1 signed workload on GCC, with the native kernel batch left independent. C1/G1 values describe complete images. For tomorrow's review, the EROFS launcher uses upstream dev 7e52cbf including b9dd73fb, with the existing exact-byte fixture and tool-hash receipt. The order after kernel completion is gcc, erofs, image, pilot with a fresh free-space gate at each step. [Inputs](../comms/claude_to_codex/0012v.md) · [Measurements and review command](../comms/codex_to_claude/0012v_reply.md)

### 0012w/x/y · baseline and trial controls

The user designated 37777148/37777264 for the next MLGO image comparison. Preserve 37736448/37736427 for in-flight jobs and existing board results. Kernel table transfer is conditional on per-lane artifact identity. In local K2/K3 change the perf Kconfig parent MLGO to n; disallow unrelated generated config drift and verify both advisor pairs disappear on the same TU. [0012x](../comms/codex_to_claude/0012x_reply.md) · [0012y](../comms/codex_to_claude/0012y_reply.md)

### 0012z · sequence and decoder

Run the three AVControl lanes from the qualified smoke and retain the shared locks. Defer image-to-RPM matches until the reader is qualified. Preserve the reviewed kernel pin. Prefer the vendor SRPM reader, then a separately reviewed decoder port, then board file reads. [0012z](../comms/codex_to_claude/0012z_reply.md)

### 0013a/b · board pair and overnight capacity

PM accepted 37777148/37777264 for the board comparison. Both have matching Product sources across 5,880 rows. Two submitted manifests are unavailable and two published metadata fields differ. Keep the sent kernel table on 37736448/37736427. Reassess the pilot using retained artifacts. Prefer the snapshot-matched vendor reader. Run published-RPM scans independently, and use the separate pkg lock for ranked GBS package work with a Friday 09:30 CST stop. The full installed A32 roster retains its pilot PASS and shared-lock requirements. [Decision](../comms/claude_to_codex/0013a_codex_pilot_fix_pair_gate_vendor_erofs.md) · [Capacity and scope](../comms/claude_to_codex/0013b_codex_optimization_tracks_tonight.md)

### 0013d · reuse K0 for tonight's kernel matrix

Use the retained RhOLRN K0 receipt and RPMs. Build K1–K5 and give each lane an independent flag-proof verdict. Keep raw measurements when argv evidence is incomplete. Cross-image attribution still requires the existing reproduction gates. [Decision and evidence](../comms/codex_to_claude/0013d_reply.md)

### 0013c · package work alongside the kernel

Keep commands 1 and 3 at 9047570. Run the revised package worker in a separate attended terminal under the pkg lock. Give the kernel scheduling priority, wait on RAM-only shortfall, and end the package run on expired credentials or a disk-floor breach. [PM review](../comms/claude_to_codex/0013c_codex_pkg_sudo_p4_fix.md) · [Implementation](../comms/codex_to_claude/0013c_reply.md)

### 0013e · 26 November · reclaim measured scratch on /home1

The operator released the 35 GiB target as a prerequisite. Keep evidence and all generated files within the workspace. Gate RPM-original deletion on a retained URL/SHA manifest, a matching published primary entry and an exact redownload. Reclaim measured kernel and package roots independently. Resume only disk-refused K4/K5 lanes. [Operator decision](../artifacts/evidence/native-input-r0013e-scope-20261126.txt) · [Commands](../comms/codex_to_claude/0013e_reply.md)
