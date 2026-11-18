# LLVM memory, performance and size: handover and execution plan

Prepared 14 November 2026. Planned next-week window:16–20 November. Scope: Tizen 10.0 KantSU2e LLVM migration. This plan adopts the previous investigation as evidence and work items; it does not automatically enable its proposed defaults.

## 1. Source and baseline interpretation

Primary source: [VD LLVM LTO Image 20261111.1: Full Analysis Report](optimization-analysis-part-01.md). It compares GCC 20261001.3, LLVM 20261103.1 and LLVM 20261111.1. The latter uses Base 20261105.1 and build.conf 14431365. It includes 22 sample packages and 151 builds (126 successes,25 failures), with documented failures and limitations.

Our current Base is 20261113.1 (r10); next-QB config is 14452507 and disables the five previous LTO exclusions. prelinksh 14327923 is in the next Base list. The already-built Product 20261114.1 still records 14431365. Keep these four facts separate: planned input, published package, built image, and measured runtime.

### Historical findings to carry forward

All numbers below are reported historical results. They are not estimates of savings on the new image and must not be added together across different sample sets.

| Topic | Historical evidence | How it will be used |
|---|---|---|
| Whole-image static comparison | Common 4778 ELF set: total files LLVM 1638.76 MB versus GCC 1647.38 MB; .text difference−39.93 MB; runtime symbol metadata+4.68 MB | Archive the original file set and units; recount the new common-file set and whole-image inventories independently. |
| Loaded sections versus memory | The report sums allocated sections as an approximation; .symtab/.strtab adds 22.42 MB but is not runtime-loaded | Track file size, PT_LOAD file/memory spans and actual PSS/RSS/private memory separately. Static bytes are not measured resident memory savings. |
| LTO gap |21 files/13 packages identified with missing final-link-flto behavior; source filenames in .symtab were used as a heuristic | Verify actual compile/link/plugin evidence and fat-object fallback; missing source symbols alone does not prove LTO. Respect explicit-fno-lto exceptions. |
| GCC forced options |1269 of 2245 historical source packages get a GCC wrapper-appended option set; Clang lacked equivalent behavior | Recheck current lists, wrappers/hooks, final flag ordering and real producer data before reusing this count or patch. |
| Forced-option samples | Four packages: loaded-section sum−25.9%, .text−36.2%; signed-char and hardening differences also addressed | Strong candidate for current-baseline evaluation; it changes current LLVM behavior and needs functional validation. |
| Inline visibility | Six effective, non-excluded samples: dynamic metadata−43.9%, loaded-section sum−11.4%; libgrpc metadata−49.2% | Re-evaluate with exclusions openusd, tvs-si, aurum and an image/TPK consumer export audit. |
| ThinLTO | Four affected samples: loaded-section sum+0.5%, .text−0.1%; build time improved. Earlier two-library timing 245s versus full-LTO 393s | Measure dedicated build times without conflating setup, cache or parallel load. Do not extrapolate sample timing to QB. |
| Inlining threshold | Affected samples: threshold 50 loaded-section sum−14.3%; threshold 25−23.3% | Test each threshold independently; performance-sensitive paths and final link-stage settings determine acceptance. |
| MachineOutliner | Two effective packages: .text−16.5%, loaded-section sum−8.1%, unwind tables+21.6% | Measure hot-path cost and unwind/stack-trace behavior as well as size. |
| lld/ICF | lld alone roughly similar; lld+safe ICF loaded-section sum−2.3% on the measured sample set | Separate linker change from ICF so results can be attributed and reverted. |
| RELR | Historical encoding calculation estimates 18.83 MB file saving; several largest providers are GCC-built/prebuilt | Recompute eligible current files; loader/packaging/boot support must be tested. Fewer relocation bytes does not mean fewer relocated dirty pages. |
| Unwind growth | .ARM.exidx+.ARM.extab about 5.10 MB above GCC in the historical comparison | Compare function/record counts and actual mapping residency; do not disable unwind tables or assume a fixed PSS impact. |

The source report uses 4778 common ELF files for cross-image comparisons and 4780 for some single-image analyses. Retain the relevant denominator in every new table. Some earlier size percentages compare different ELF inventories and must not be treated as compiler-only gains.

## 2. Current adoption status and required verification

| Proposal / prerequisite | Status at handover | Next action |
|---|---|---|
| r10 driver behavior | Source behavior recorded; repository published; current-image complete behavior/coverage audit open | Probe default plugin use, explicit-fno-lto, linker choice, actual PIE and effective LTO with fixed artifacts. |
| Drop vdprelink | HQ source adopted locally; prelink package builds and lists are empty | Confirm next-image lists/boot behavior; an empty target does not prove no process invocation. |
| Forced Clang option hook | Previous report says final-form local validation; no deployment proof recovered for current inputs | Recover original patch/results; inspect current 14452507 and Base macros for the hook, then reproduce under current conditions. |
| Inline visibility | Previous sample validation and three exclusions; no current deployment proof | Recover exact option/list change; use a separate experiment and preserve public symbol/ABI behavior. |
| Default ThinLTO | Previous recommendation and samples; current default not established here | Inspect active toolchain; prepare an isolated candidate only if still needed. Verify both compile and final-link mode. |
| Threshold / Outliner defaults | Historical candidates; no release or TPMS acceptance evidence here | Separate candidates with compiler and LTO-backend coverage; retain full measurements for failed or ineffective options too. |
| lld acceleration / dali2-adaptor dependency | Historical ARM-emulated lld and unresolved provider-link issues | Identify current ld.lld provider, host/target architecture and invocation; recover/fix the exact missing dependency, then remeasure. |
| RELR | Historical calculated opportunity; deployment and loader compatibility unverified on current product | Check target loader/ABI, complete ELF consumers including TPKs, packaging and no-prelink baseline; test actual output. |
| Base-package visibility | boost/abseil/icu experiments previously failed in Product environment | Rebuild in their proper fixed Base environment; product build.conf changes are not evidence of Base behavior. |

## 3. Baseline and experiment protocol

### 3.1 Freeze reproducible inputs

Record source Base CL list and unique-path shelf list with hashes; full build.conf and Base/Product URLs; OBS source revision/digest and binary package versions; compiler, linker, runtime library and SDK plugin identities; package inventory, build.xml, build logs and original/stripped ELF hashes. Archive existing historical reports and reachable artifacts before they expire. Historical artifact retention duration must be rechecked rather than assumed from the old report.

Use the latest stable no-prelink r10 image as control after current correctness work is validated. First establish whether the control can be rebuilt with matching code-section output. Keep safety fixes common across control and candidate. Same-source Clang option A/B is the primary optimization comparison; a GCC image with different sources/Base is context only. If a GCC comparator is needed for attribution, build the same package revision and dependencies with an explicit recorded GCC configuration.

One change per initial experiment: forced options, visibility, ThinLTO, threshold, Outliner, lld, ICF, RELR. Combine only accepted candidates, then run an interaction regression. Keep full-LTO and ThinLTO modes, compilation caches, host-job count and warm/cold build state explicit.

### 3.2 Device and scenario controls

- Use the same physical board for A/B, with board ID/device tree/RAM layout recorded. The earlier 192.168.108.25 and current 192.168.108.26 boards are different and are not a matched pair.
- Keep firmware/MICOM, thermal state, power mode, network, account state, application versions and peripherals fixed. Record SSO auto-update events; do not silently compare different downloaded applications.
- Proposed scenarios: cold boot to usable UI; idle after a defined settling period; Wizard/account flow; TV/broadcast and channel change; representative media playback; app launch; profile lifecycle; HbbTV and USB/media scenarios relevant to the build.
- Plan repeated measurements, initially at least five comparable runs per scenario/variant where practical. Report median and spread, startup/peak/steady-state values and individual failures. Increase repetition if noise prevents a decision; do not declare improvement from one run.
- The user operates flashing/TPMS where access requires it; migration engineering prepares candidates, collection commands, analysis and rollback artifacts. No board reset/flash is implied by this documentation update.

### 3.3 Metrics and evidence

| Area | Collect | Interpretation |
|---|---|---|
| Distribution size | RPM/TPK/image bytes; unstripped and consistently stripped ELF sizes; section inventory | Packaging, debug symbols and compression changes must not be labelled executable-code savings. |
| Runtime-related ELF size | PT_LOAD p_filesz/p_memsz, .text/.rodata/.data/.bss, dynamic symbols/strings/hashes, relocations, GOT, unwind | Zero-fill .bss and shared mappings differ from file bytes and resident memory. |
| Device memory | Per-process PSS/RSS/USS or equivalent private/shared breakdown, anonymous/file-backed dirty pages, startup peaks, system available memory and kernel/slab where relevant | Avoid summing RSS as system consumption; retain the process set and sampling phase. Attribute new IoTivity table storage separately if present. |
| Performance | TPMS results, boot/app-start latency, media/broadcast responsiveness, CPU time/utilization, frame/drop or latency counters relevant to each workload | Keep workload/version/temperature comparable; build-time acceleration is not target runtime acceleration. |
| Build performance | Per-package compile/link wall time, peak memory, parallelism/cache/setup costs, image/QB duration | Do not extrapolate emulated-linker or setup-dominated timings. |
| Correctness/compatibility | Core count/signature, loader errors, undefined symbols, versioned exports, exception/unwind behavior, old GCC/prebuilt/TPK consumers and dlsym/plugin paths | ELF symbol checks cannot prove callback ordering, pointer identity or all dynamic consumers; add targeted runtime cases. |

Acceptance: no new functional/ABI regression; no demonstrated memory increase in the agreed critical scenarios; no material performance regression outside measured run-to-run noise or the existing product/TPMS acceptance limits. Numerical product limits have not been provided here, so no arbitrary percentage is labelled approved. Report every tradeoff explicitly; hold a candidate whose measurements cannot distinguish gain from regression. A size-only gain is insufficient for a global default change.

## 4. Prioritized experiments and release gates

| ID / priority | Experiment | Initial scope | Completion / decision gate |
|---|---|---|---|
| O1 / P0 | Recover old scripts/results and capture current control | Historical 22-package/151-build set plus current inputs; export baseline and actual LTO/flag coverage | Reproducible control, archived inventory and stable same-board scenarios. Missing raw data is explicitly marked, not reconstructed as measured results. |
| O2 / P1 | Forced-option behavior | org.tizen.AVControl, org.tizen.tv-viewer, libpisa-ipc, org.tizen.webappservice; openusd/grpc exempt controls; tvs-si compatibility check | Final options and hook expansion verified; cover %prep/%build/%install, environment-clearing build systems and nostdlib rules. Preserve GCC exclusions, Clang-specific mapping and SDK target mode. Validate signed-char/hardening effects before a wider image. |
| O3 / P1 | Inline visibility | libgrpc, trustzone-nwd, security-manager, tee_test_suite, pkgmgr-info, libwebauthn-common; retain openusd/tvs-si/aurum exclusions | No newly unresolved/version-incompatible symbols in actual consumer scope. Include dlopen/dlsym, prebuilt GCC code and TPKs. Check cross-DSO function-address and inline/static/exception interactions at runtime. |
| O4 / P1 | ThinLTO versus full LTO | openusd, avoc-daemon, dali2-adaptor, freetype and representative current-LTO packages | Effective mode proved at both stages, size/unwind/code correctness retained, dedicated build-time and runtime results; no bypass of package-fno-lto exceptions. |
| O5 / P2 | Threshold 50/25 individually | openusd, app-installers, dali2-adaptor and webappservice; avocd after resolving test-option injection | Target performance/TPMS meets acceptance; final compile and LLVMgold/LTO backend behavior is confirmed. Do not simply copy GCC-fno-inline-functions. |
| O6 / P2 | MachineOutliner independently | openusd/dali2-adaptor first; expand only after initial proof | Performance benefit/cost, increased unwind data and backtrace behavior measured; supported ARM and LTO/non-LTO option delivery. |
| O7 / P2 | lld prerequisite repair and linker-only comparison | Native accelerated linker provider, dali2-adaptor dependencies, representative links | No global allow-shlib-undefined workaround; correct host acceleration, successful links and loading, then a linker-only control. |
| O8 / staged | Safe ICF, then RELR | Start with O7-passing source-built packages; prebuilt/GCC providers separately | ICF address/ABI correctness and performance; RELR target-loader/packaging support and boot results; record actual eligible bytes, not the whole historical 18.83 MB as guaranteed. |
| O9 / parallel | Enlarged-package cause analysis | soc-ir-interface, mdnsresponder, feature-config-daemon, ppi-display-control, lib-ndp-pq-interface-tv plus historical top-size outliers | Separate source/ELF-inventory changes, final optimization flags, wrappers, LTO, inlining and prebuilt contents before choosing a package fix. |
| O10 / parallel | Unwind table analysis | tee_test_suite, native-home, web-engine, SWU, openusd, libgrpc | Function/record counts, coverage and resident/file impact; preserve exceptions and crash backtraces. |
| O11 / follow-up | Base visibility and formerly failed samples | boost/abseil/icu in Base; aurum, mbr-daemon, native-home after baseline failures resolved | An unchanged control must build before an option-failure/gain claim. No global visibility extension from Product-only data. |
| O12 / follow-up | SDK coverage, MLGO/user-space and debug-symbol policy | Remaining mixed SDK/content cases; selected hot user-space code; release/debug artifacts | Proven source ownership and reproducible profiles; preserve GCC consumers and crash-debug capability. Not a promise to complete custom LLVM passes next week. |

### Directions kept out of the current rollout

- Relative vtables change the C++ ABI and conflict with retaining existing GCC consumers; keep as a separately gated long-term research item, not a next-week production change.
- No global-fvisibility=hidden or-Bsymbolic-functions shortcut, no global suppression of undefined shared-library symbols, and no removal of unwind information.
- No blanket-O2/-Oz switch, direct copy of Clang-fno-inline-functions, or generic gc-sections rollout based only on historical size data.
- Treat VD warning/-Werror policy and stronger stack protection for exempt packages as separate compatibility/security evaluations. Do not mix them into a size experiment or silently weaken existing hardening.
- MLGO/custom passes, hot/cold layout and ThinLTO global merging need source/version/profile evidence and isolated experiments before being scheduled as deliverables.

## 5. Proposed next-week sequence

| Day | Primary work | Expected artifact, not guaranteed rollout |
|---|---|---|
| Mon 16 Nov | O1, current correctness gates and unchanged sample rebuilds; recover historical patches/scripts | Baseline manifest, missing-evidence list, measurement protocol and current driver/coverage report. |
| Tue 17 Nov | O2 and O3 separately on representative packages | Two candidate diffs and package/ABI/export reports; preserve exclusions and rollback inputs. |
| Wed 18 Nov | O4; board/TPMS measurements for any accepted first candidates | Full-vs-ThinLTO size/build/runtime table; first measured memory/performance comparison. |
| Thu 19 Nov | O5/O6 only if earlier stability gates pass; begin O7 prerequisite verification independently | Threshold/Outliner tradeoff data and lld dependency/acceleration findings. |
| Fri 20 Nov | Repeated scenario checks, interaction regression for accepted candidates, next-QB selection | Updated evaluation/review increments and go/hold/rollback decisions with measured evidence. |

If correctness or compatibility remains unresolved, keep affected optimizations as experiments and carry them forward. Unrelated source/provenance/document recovery can continue. A single rushed image combining all candidates would prevent attribution and is not the planned comparison.

## 6. Ownership, artifacts and reporting

Migration engineering owns candidate preparation, source/ABI review, controlled builds and data analysis. Device/TPMS execution is coordinated with the board operator. Package-owner review is required for the technical meaning of changed behavior; no external messages or approval requests have been sent as part of this document.

Intranet artifacts stay under /home1/chengkai/vd-tree/: workspace for scripts/results, config for pinned experiments, manifest for unique-path lists. The maintained documentation is the local /home/toolchain/Desktop/temp/claude_mem copy. Preserve original shelves; create new shelves for accepted changes and replace the corresponding path once in a new list.

Each result records source/config/artifact hashes, control and candidate metric tables, actual option coverage, build/runtime/ABI status, known limitations and rollback inputs. Update the daily evaluation, review increment and weekly progress from these results. Historical reports remain unchanged as evidence.

Related: [weekly progress](Weekly_Progress_and_Next_Plan_20261114.md), [current evaluation](Clang_Fix_Evaluation_Daily_Increment_1114.md), [current review list](Clang_Review_List_1114_Increment.md).


## Resource constraint and Tizen 10.1 migration follow-up

The build host has limited free space, as reported by the operator. The prepared 12-package GCC/Clang comparison batch has no reported execution result and is held pending a disk inventory. First identify large build roots, download caches, active processes and nested mounts. Retain source snapshots, patches, RPMs/logs, rollback artifacts, shelve backups and the IoTivity ARM runtime-test root. A rebuildable directory is a cleanup candidate only after its current use and retained evidence are checked. Size listings include overlapping parent/child totals and must not be summed as reclaimable space.

Tizen 10.1 migration is an active parallel workstream. The last historical record found is `tizen10.1_shelves_1109g.txt` with 894 entries. Of the changes documented on 11 November, pkgmgr-info 14444254 and prd-factory-api 14445927 were included; the remaining later 10.0 changes are not established as migrated. This is historical evidence, not confirmation of the current intranet list.

| Priority | Work | Completion evidence |
|---|---|---|
| P0 | Inventory disk usage and existing 10.1 inputs | Measured available space, exact cleanup candidates, mount/process checks; current 10.1 Base/Product/config/base-list/shelf-list paths and hashes. |
| P0 | Reconcile 10.1 source and shelves against accepted 10.0 fixes | Per-path classification: already covered, reusable after source comparison, or requiring adaptation. Do not copy the entire 10.0 shelf list or treat the HQ GCC 10.1 configuration as a ready LLVM baseline. |
| P1 | Adapt high-priority correctness and compiler-selection fixes | New shelves carrying existing changes, preserved originals, no duplicate depot paths; package builds on the pinned 10.1 dependency set and targeted GCC/ABI checks. |
| P1 | Schedule builds within recovered capacity | Prioritize changed 10.1 packages and a reduced 10.0 comparison set; serialize resource-heavy work. Prepare the 10.1 Quickbuild only after its input and package gates are met. |

The existing 10.0 stability and optimization work continues. Measurements and release inputs remain separate by version. No actual cleanup, 10.1 migration completion or successful 10.1 LLVM build is claimed by this scheduling update.


### 15 November follow-up: measured storage and the 10.1 Base candidate

The operator returned the storage inventory: /home1 has 143 GiB shown as available by df, 92% block usage and 17% inode usage. vd-tree occupies about 348.73 GiB, including 205.16 GiB in workspace/temp. Ten identified old z901/sdkllvm4 download-cache directories total approximately 13.73 GiB; only their regular RPM payloads are proposed for deletion, subject to fresh process/mount checks. This is not a guaranteed reclaim estimate: metadata and hardlinked copies remain. Build roots, source, RPM outputs, logs, rollback packages and the pending IoTivity runtime environment are retained. Actual cleanup has not been reported.

The current intranet 10.1 base list has 2249 entries; shelf list1109g has894 entries with no duplicate paths. Relative to the accepted 10.0 shelf list,38 paths are absent from the 10.1 shelf list and274 shared paths select different CLs. These are source-review candidates, not proven missing fixes. Multiprofile is still14433454 on10.1 versus14457173 on10.0. The pinned Clang configuration itself already declares minor version1; this macro alone cannot identify the Base/Product/source baseline.

The operator confirmed that no new 10.1 LLVM Base snapshot is available and requested preparation of one, including evaluation of using it for10.0 Product source. First inspect the actual OBS project inheritance, package revisions, build macros and source differences. Prepare a10.1 LLVM candidate while preserving current10.0 inputs. Evaluate both source/build compatibility and binary/runtime compatibility for existing GCC applications, TPKs, SDK consumers and prebuilt libraries. Candidate package builds are followed by full image and same-board functional/ABI checks. Consolidation onto10.1 Base is conditional on this evidence; it is not an accepted default or a completed migration.


### Updated Product source input: 20261116.2

The operator supplied the 10.1 Product manifest for TIZEN-ONEMAIN-KantSU2e-RELEASE_20261116.2. The inspected local copy has SHA256 `c22afe15b6dc3092906f11760dfb979e167cfab6c03f936e91f37178e1037b7d`, 2244 projects, no duplicate paths and no name/path mismatches. Of the revisions, 1112 are numeric and 1132 are VBS labels. Preserve the exact labels; their trailing numbers are CL hints until Perforce file identity is verified.

This manifest replaces the older 1101 source list as the candidate 10.1 Product source input. The 1101 list and 1109g shelves remain historical comparison inputs; the shelves require review against the updated source. Multiprofile now references the label ending14456146, libtv-element14343194, pkgmgr-info14451159 and prd-factory-api14427915. Do not apply older shelves as whole-file replacements without checking the new Product changes. prelinksh references a label ending14327923 and iotivity retains numeric12913071; neither observation alone establishes the final patched image contents.

The supplied GCC configuration is `/home1/chengkai/vd-tree/config/gbs_vd_gcc_11.16.conf`, with the official20261116.2 Product repository. Its Base URL still uses10.1 `latest`, and its local RPM repository precedes remote repositories. Keep the operator's configuration intact, but pin the actual Base snapshot and isolate candidate build roots/local outputs for comparative builds. The source manifest does not itself establish the publishing build.conf or resolved Base URL. The10.1 LLVM Base preparation and the10.1 Base with10.0 Product compatibility evaluation remain open, separate validation tasks.


### 16 November execution update

Cache cleanup completed successfully: 7641 downloaded RPMs removed, observed free space increased by13.48GiB to154.36GiB. The detailed deletion plan and log remain in `workspace/temp/disk_cleanup_8id333be`. No repeat cleanup is needed. The home-directory scan timed out and is partial; it identified whole_image225.25GiB, GBS-ROOT-hfy53.78GiB and .cache42.80GiB. Other extracted-package trees are only review candidates; corresponding RPMs and current use have not been verified sufficiently for deletion.

The complete312-row shelf comparison is against the historical1101 source baseline, not Product20261116.2. The first OBS query failed before returning project data because the hardcoded endpoint did not match a configured authentication entry. The probe now selects the exact endpoint from existing osc configuration, including explicit ports/aliases, and does not rewrite or print credentials. Local endpoint-selection checks passed; the corrected intranet query and the new Product manifest comparison remain pending. No10.1 LLVM Base build or compatibility pass is implied.


### Verified extraction cleanup completed; editor cache cleanup prepared

The operator returned a successful extraction-cleanup result: 6974 verified package directories removed, three entries retained, observed free-space increase47.59GiB and203.98GiB remaining. Together with the earlier cache cleanup, the observed increases total61.07GiB. Original RPMs remain available.

The directory named whole_image is a source checkout: its .repo directory alone occupies113.84GiB. It must not be treated as a disposable image download. Its45.77GiB temporary LLVM development tree and the46.45GiB GBS-ROOT-hfy scratch root require internal inspection before further deletion. Historical optimization source/scripts/results and manifest recovery records are retained.

The next prepared command removes only regenerable vscode-cpptools and pip cache contents, approximately42.4GiB reported. It requires the remote C/C++ indexing processes to exit and preserves the cache directory ownership and source workspaces. Four local tests passed; remote cleanup is pending. Additional source/build-tree inspection is included to continue identifying disposable intermediate data. The10.1 Base and updated Product migration tasks remain open.


### Scope correction: cleanup restricted to vd-tree

The operator clarified that cleanup is authorized only inside `/home1/chengkai/vd-tree`. External caches and workspaces, including `.cache`, whole_image and GBS-ROOT-hfy, are excluded from further cleanup. Earlier proposals to clean those external caches are withdrawn. Local entry points for editor-cache cleanup and index-process termination have been disabled; already copied intranet scripts must no longer be run.

The two completed deletion stages were entirely inside vd-tree, with observed free-space increases totaling61.07GiB. External cache cleanup remained blocked before deletion in every reported attempt. Indexing processes belonging to chengkai were terminated during those attempts; this action is recorded and will not be repeated for cleanup. Subsequent cleanup candidates must be inside vd-tree and preserve current source, unique evidence, rollback inputs and pending test environments.


### Scoped scratch cleanup and return to migration work

The operator authorized removal of unused data inside vd-tree and explicitly retained the GCC20261001.3/Base20260916.1 reference data and the latest GCC20261116.2 reference data. Necessary LLVM stability, ABI and optimization evidence remains retained. External paths are excluded.

A combined command now targets15 explicitly named old build-root groups inside workspace/temp, preserves package outputs and selected build/dependency evidence, and removes their generated scratch environments. Local source exports, repositories, experimental reports, formal inputs and pending IoTivity runtime environments remain. Four local checks passed; intranet execution and actual reclaimed space are pending. The same command then performs the corrected read-only OBS probe and updated Product manifest comparison, returning directly to10.1 Base preparation and adaptation work. This is not a blanket deletion of GCC data or an additional broad filesystem scan.


### Scratch cleanup complete; active work returns to 10.1 inputs

All15 named old build-root groups were cleaned successfully, with an observed free-space increase30.19GiB and239.68GiB available. The three cleanup stages recorded increases totaling91.26GiB. Every completed deletion was inside vd-tree. Evidence and current control/test inputs were retained; further broad disk scanning is not scheduled now.

OSC authentication succeeded using the exact configured endpoint. That endpoint returned only Tizen:10.0:Base and Tizen:10.0:Base:Dev:LLVM; no matching10.1 project was listed there. This does not establish whether another OBS instance hosts10.1. The LLVM project reported llvm revision10 and a published armv7l state. These current-source results are not a substitute for immutable snapshot provenance.

The intranet Product20261116.2 manifest failed the raw-file hash check against the supplied local copy. Its cause is unresolved: formatting changes and changed source references must be distinguished. The next read-only command compares canonical path/revision references, exports complete references only if changed, and reads10.1 Base/Product publishing metadata and already-configured OBS endpoints. No10.1 project creation, candidate build or compatibility pass has occurred.


### 10.1 source references and publishing baseline resolved

The intranet and supplied local Product manifests contain exactly the same2244 path/revision references, with canonical hash `f17f710c7d7197fd5e9b337a92026844af6be4849d6c0b56d26d47f5b116434b`. Raw-file differences do not change those source references. Against the historical1101 list, there are70 added and75 removed source paths;71 old shelf paths are absent from the new manifest and require reconciliation.

Product20261116.2 explicitly publishes Base `tizen-10.1-base-standard_20261106.1` and the FMS GCC build configuration at14434440. Its configuration is distinct from the HQ migration GCC configuration. The Base configuration declares minor0 while the Product configuration declares minor1; repository and package identity must be measured rather than inferred from those macros. The next preparation command pins these inputs, creates an isolated GCC control configuration, compares Base package metadata and captures the exact new MAPI/ATSC3 source with prior migration shelves. Candidate builds, new LLVM Base publication and compatibility validation remain pending.


### First preparation attempt: control ready, source reads require correction

The isolated GCC control configuration was prepared in migration_101_prepare__w58_qu8. The Base configuration differs from the cached OBS configuration, and the Product-GCC versus existing-Clang configuration diff has226 lines. Both repository metadata reads failed because the script assumed an incorrect directory layout. Both source captures failed because the manifest VBS references are not valid labels on the configured Perforce server. This is not an authentication-expiry diagnosis. The returned bundle was decoded and contains zero source files.

The corrective command reuses the prepared control, discovers repository metadata through actual directory links, and resolves VBS numeric suffixes only after checking for submitted changes affecting the corresponding package. Original manifest references and resolution evidence are retained; label identity is not claimed. It then captures the MAPI/ATSC3 migration inputs and configuration diff. Local input/parser checks passed; remote capture, patch preparation and builds remain pending.


### Repository discovery and migration source capture succeeded

The actual Base repodata directory is under repos/base/armv7l/packages. The fixed10.1 GCC and10.0 LLVM repositories yielded851 and852 package names respectively. Submitted package CLs were verified and27 source variants captured for the five MAPI files and four ATSC3 files. The return packet exceeded the output limit; source remains available on the intranet and is being repackaged without full change descriptions. Local patch implementation still awaits those contents.

The10.1 Base contains OpenSSL3.0.23/1.1.1zj versus3.0.20/1.1.1zh in the current LLVM10.0 Base, and Clang19.1.4 versus22.1.8. Retain the10.1 system-library baseline and port reviewed LLVM/toolchain/SDK adaptations. Shared upstream version numbers for other packages do not prove binary identity or ABI compatibility. No wholesale replacement with the old LLVM repository or old OpenSSL synchronization downgrade is planned. The candidate plan is prepared locally; OBS creation, candidate builds and two-Product compatibility validation remain pending.


### MAPI migration candidate implemented and locally tested

The MAPI source packet was received and verified; the ATSC3 packet remains available on the intranet. Product1.4.7 already contains part of the initialization-lock fix. The new five-file candidate preserves its added APIs, verification bridge and TIDL namespace while porting lifecycle serialization, unlocked teardown and queued notification delivery, together with the existing Clang build adaptation. Initialization exception-to-error handling is retained.

GCC and Clang each passed14 targeted host cases. Patch application and all five output hashes were verified. These are instrumented-provider tests, not target package/runtime acceptance. The next command builds the candidate against the fixed10.1 GCC control and returns the actual provider methods plus the existing ATSC3 packet. ARM GCC/Clang validation, runtime acceptance and new shelves remain pending.


### MAPI target package build completed; compiler identity check pending

The isolated candidate package build exited0 and produced capi-multiprofile-tv1.4.7-1.armv7l.rpm, SHA256 `e5ee9da87d5dffbaae1f23e00851ec580c99837e106dfa3cbb07d2f99d4ad39d`. The script reported REVIEW_REQUIRED because neither compiler command pattern appeared in the log. This is a compiler-evidence gap, not a package build failure. Existing CMake compiler records and the packaged ELF will be inspected without rebuilding. The operator returned only the build tail; the earlier ATSC3 source packet and provider excerpt still need to be received and reviewed. Runtime/Clang/ABI acceptance and new shelves remain pending.


### ATSC3 source received: existing shelf is reusable

The complete ATSC3 packet was received and checksum-verified:12 file variants and8 unique blobs. All four affected files in the updated Product are byte-identical to the corresponding old Product files. Shelf14459110 can therefore be reused as the10.1 adaptation candidate without creating a duplicate change. This does not establish whole-package identity or target validation.

The next command builds the ATSC3 candidate against the fixed10.1 GCC control and prints compiler identity from CMake records. It also returns the still-unreceived MAPI compiler/provider evidence and existing Base source-package inventories for the LLVM Base preparation. No installation, new shelf or formal manifest change is included. MAPI package exit0 is confirmed; its compiler identity/provider review and both packages' target runtime acceptance remain pending.


### 10.1 GCC package gates confirmed and Base seed reviewed

Both target package builds exited0 and produced their expected RPMs. Actual CMake compiler records identify GNU14.2.0 for C and C++; the MAPI library also carries the GCC14.2.0 marker. The former REVIEW_REQUIRED labels were caused by hidden compile command lines. Actual provider setters store callback pointers and Disconnect calls/deletes the proxy, supporting the candidate's unlocked lifecycle design for the inspected paths. Target runtime and Clang10.1 validation remain pending.

The verified Base metadata groups to441 distinct source names per repository,442 in the union, within the armv7l/noarch scope. Ten source names have different upstream version sets. The seed worksheet preserves10.1 library versions and isolates LLVM/SDK/driver adaptations; equal version numbers do not establish identical patches. Current OBS packaging inputs and published source-RPM provenance will be pinned before any candidate project upload/build. The10.0 image-validation and new-QB work continue independently.
