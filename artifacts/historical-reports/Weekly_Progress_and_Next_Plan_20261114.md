# Tizen LLVM migration: weekly progress and next plan

Reporting period: 9–14 November 2026. Status cut-off: the latest supplied results on 14 November; the layout-preserving IoTivity ARM Clang/GCC package build results have been received; Clang artifact checks have also been received; target runtime/ABI checks remain open.

## 1. Executive progress

The work has moved from producing an LLVM image to closing runtime defects, completing compiler coverage and preparing a measured optimization baseline. The r10-based Product 20261114.1 image exists and completed an initial smoke check on a different board. The next-QB no-prelink/LTO configuration has passed seven targeted package builds. ATSC3 now has a new shelf with both ARM Clang and GCC package validation. IoTivity still needs an ABI-preserving lifetime fix to finish target validation before release.

Twenty post-11-November compiler-adaptation CLs were missing from the local daily evaluation and review increments. They are consolidated in today's documents together with the later multiprofile and ATSC3 shelves. This is a documentation backfill, not a claim of twenty new changes made today. Remote publication status is not established.

## 2. Weekly milestones

| Stream | Progress this week | Evidence / remaining boundary |
|---|---|---|
| Image generation | Historical 20261111.1 image built with LTO; subsequent 20261112.1,20261113.2 and r10-based 20261114.1 images supplied for investigation | Different Base/config/source/package-update states must remain explicit; these images are not interchangeable performance controls. |
| Build-time and runtime correctness | Earlier pkgmgr-info alignment and prd-factory uninitialized-read fixes documented; subsequent SSO/Wizard and multiprofile reentry issues investigated | Do not state all historical 30 cores are closed without corresponding runtime evidence. SSO rollback is a workaround; multiprofile now has a shelf and initial image evidence. |
| Compiler migration | Twenty additional adaptation CLs consolidated after the 11-Nov increment; historical HQ four-table review covers 986 rows | Historical build/size results retained with their limitations. Prebuilt libraries and intentionally GCC-built toolchain components are not automatically migration defects. |
| SDK coverage | Historical 313 SDK packages reconciled by RPM names and TPK contents; latest VIF/TTS target provenance supported by code/data/Build-ID matches | Historical 37 mixed and two content-difference cases remain; current VIF main and TTS language-library coverage not fully resolved. |
| Base/configuration source review | B.30 now documents exact r10 spec/driver diffs; C14-2 documents GCC #2-to-#3 LTO exclusions and the wider baseline/feature refresh | Source/configuration evidence; no additional build or runtime validation claimed. |
| HQ baseline integration | prelinksh 14327923 and Clang build.conf 14452507 integrated into local next-QB inputs | Seven targeted builds passed: prelinksh, five newly LTO-eligible packages, multiprofile. Full image and runtime acceptance pending. |
| ATSC3 | Respect platform compiler, correct token spacing and pointer formats; shelf 14459110 created and workspace restored | ARM Clang/GCC full builds passed; runtime and diagnostic-output consumers pending. |
| IoTivity | Confirmed dangling what() return; rejected release of layout-changing member-string candidate; implemented a layout-preserving alternative | New candidate host tests and ARM Clang/GCC package builds passed; Clang artifact exports/dependencies checked; liboc.so .bss +20,936 bytes (table20,928 bytes); target ABI/runtime review and new shelf pending. Existing 14452627 retained. |
| Optimization handover | 11-Nov full LTO analysis reviewed and incorporated into next-week work plan | Historical 151 builds across 22 samples are prior evidence, not new r10 measurements. No optimization defaults changed by this reporting task. |

## 3. Current plan status

| Task | State | Next completion criterion |
|---|---|---|
| Canonical manifests and configuration | Prepared and checked | Next image's build.xml and package artifacts match the recorded inputs. |
| ATSC3 code / shelf | Build-complete, shelved | Target functional regression, including the relevant Proidiom/TA execution path and address-log consumers. |
| Multiprofile reentry | Shelved; artifact markers and initial smoke evidence | Target lifecycle/callback regression, repeated boot and soak; record any remaining core signatures. |
| IoTivity lifetime repair | Host verification and ARM Clang/GCC package builds complete; target ABI/runtime pending | Target cross-library/runtime checks, then a new shelf replacing the package's single manifest entry; Clang artifact footprint/exports already checked. |
| SSO automatic updates | Open | Compatible updated application or a durable agreed version/update strategy; rollback alone is not closure. |
| USB -71 / later TV restart | Awaiting reproduction per current request | Capture failure/reboot timeline and board evidence; do not infer causation from SSO recovery. |
| SDK residual coverage | In progress | Classify each remaining ELF by fixed-source/prebuilt provenance, actual compiler evidence and current image inventory. |
| Missing historical source-review details | Backfilled as open items | Recover pkt_Err, DashCurl/ICurl and enum-assignment diffs; retain klay va_start UB/ABI tradeoff. |
| Memory/performance/size | Accepted as a next-week workstream | Current baseline, controlled experiments and a measured go/hold/rollback decision for each candidate. |

## 4. Current build inputs

| Input | Current value / evidence |
|---|---|
| Base repository | `http://repos.vd.sec.samsung.net/obs220/tizen-rsa/tizen-10.0-base-dev-llvm/standard/tizen-10.0-base-dev-llvm-standard_20261113.1/` (r10 baseline) |
| Product repository used for current local dependencies | `http://repos.vd.sec.samsung.net/priv/168.219.246.243:81/PRV/builds/b259/19330259/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261114.1/` |
| Next-QB Base CL list | `/home1/chengkai/vd-tree/manifest/tizen10.0_base_urls_1114_noprelink.txt`; 2245 entries, no duplicate paths; SHA256 `bd5e81179eae1367b083fa77b701322b115e2214a862bf073e3063e8a04aa1f3` |
| Next-QB shelf list | `/home1/chengkai/vd-tree/manifest/tizen10.0_shelves_1114_atsc3.txt`; 932 entries, no duplicate paths; SHA256 `86bfbf724745a99914be5e991f7ae4caac015702cff657666428ef3a333e467c` |
| Next-QB Clang configuration | `/home1/chengkai/vd-tree/config/TIZEN_KantSU2E_Clang_14452507.conf`; SHA256 `98690f234ec8b79c728ae624f3ea91b12e6db5d918c70cfacb277d798dc95e03` |
| Important package entries | multiprofile `14457173`; ATSC3 `14459110`; IoTivity remains `14452627` |
| Already-built 20261114.1 image | Artifact `19330259`; its build.xml records build.conf **14431365**, not 14452507. The new configuration/ATSC3 shelf are prepared for the next image, not proven present in this one. |
| GCC validation configuration | Temporary GCC override using the existing build.conf mechanism and the same r10/Product dependencies; validation-only, not the formal QB configuration and not an exact reconstruction of the older GCC image. |

The new board is 192.168.108.26; it is not the earlier 192.168.108.25 board. Its initial no-core observation lasted approximately 412 seconds. The currently inserted Kingston device is not proof of behavior with the original failing USB device. Board/model/memory layout, peripherals and automatic application updates must be fixed before performance comparisons.

The formal PIC-fix list remains in use. The historical ltoexp2 list is an experiment, not the current recommended production input. The next full QB has not been reported complete in this status.

## 5. Immediate actions before and after the next QB

1. Execute the prepared ARM QEMU cross-library and actual packaged-body tests, then complete runtime/compatibility review before adding the IoTivity candidate. Clang artifact checks passed the inspected export/dependency contracts; the GCC-versus-Clang export difference is not a matched GCC regression test.
2. If a QB starts before that review finishes, retain 14452627 and explicitly carry the lifetime defect as open. Do not label the image as containing its fix.
3. Build from the canonical 932-entry list, r10 Base, noprelink Base list and 14452507 configuration; archive input hashes, build.xml, package inventories and logs.
4. Validate startup, Wizard/SSO versions, profile lifecycle, core counts and key media/broadcast/USB scenarios. Observe actual prelink behavior and PIE/LTO output before claiming alignment is complete.
5. Use the resulting stable image as the current optimization control; keep the safety and correctness fixes common to all experiment variants.

## 6. Next week: 16–20 November

| Priority | Work | Deliverable |
|---|---|---|
| P0 | Close target-validation gaps and freeze the measurement baseline | Reproducible image/input/source/package manifest, same-board scenario protocol and current size/memory/performance data. |
| P1 | Recheck effective compiler options and LTO coverage on r10; evaluate the missing forced-option behavior | Per-package evidence, unchanged-control rebuilds, isolated build.conf candidate and functional checks for char signedness/hardening. |
| P1 | Re-evaluate inline visibility with existing exclusions; measure ThinLTO separately | Export/consumer compatibility report and independent full-LTO versus ThinLTO build-time/size/runtime comparison. |
| P2 | Inlining thresholds and MachineOutliner | Controlled sample results with TPMS and unwind-table costs; only then choose candidate defaults. |
| P2 / staged | Native accelerated lld and package link dependencies, then ICF/RELR | Host-tool and target-loader verification, explicit dependency fixes and one-candidate-at-a-time measurements. Full rollout is not promised within one week. |
| Parallel | SDK provenance, enlarged-package causes and unwind growth | Updated per-package decisions; no blanket compiler/optimization switch based on a historical percentage. |

See [LLVM optimization execution plan](optimization-plan.md) for experiment ordering, metrics and release gates. There is no new memory-saving or performance-gain claim until these measurements exist.

## 7. Reporting package

- [Daily evaluation including 12–13 Nov backfill](Clang_Fix_Evaluation_Daily_Increment_1114.md)
- [Product / Base / build.conf review increment](Clang_Review_List_1114_Increment.md)
- [Optimization handover and next-week plan](optimization-plan.md)
- [Historical 11-Nov optimization report](optimization-analysis-part-01.md)

Documents are prepared locally for review/publication. No remote upload, submitted CL, completed next QB or full runtime acceptance is implied.


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
