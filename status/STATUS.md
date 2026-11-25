# Status

## 0012u · GCC board reference

G1 Product, running kernel, USB pair, both slot prefixes and BTF match QB 37564293. G1 Text is 9,364,188 B. The two LLVM image-to-boot checks passed for all five fixed fields. G1 Data/BSS/init use that verified derivation. The original G1 boot line is unavailable. TV left on GCC at Home, SDB uid 5001. GCC perf config comparison awaits the native readback. Claude review pending. [HQ table and evidence](../comms/codex_to_claude/0012u_reply.md)

## 0012s/t · native launch and inventory

K0–K5 can run tonight using the completed source job. External-module ownership waits for the image scan. The private erofs-utils 1.9.4 build passed local 48-bit metabox content tests. Actual partition receipts, four debug inventories, GCC performance config/image values and AVControl pilot results await native readback. Submitted for Claude review. [Pinned commands, evidence and gates](../comms/codex_to_claude/0012t_reply.md)

## 0012r · Custom warm-boot measurements and native review

C1 returned the full kernel Memory line at 27.15 s and Home focus at 28.48 s. Against cold O1, kernel code changes by −248,768 B, boot rwdata by −1 KiB, BSS by +1 KiB and init by −8 KiB. The 178 installed package changes are release-only, including gzip, xz and their libraries. Three warm idle observations are archived. Native pin 3660bfe addresses the two-partition image, AVControl LTO receipts, matched debug ELF, replay diagnosis and disk census. The earlier image run ended with rc=1. Requalification and ELF measurements await native evidence and PM review. [Results and commands](../comms/codex_to_claude/0012r_reply.md)

## 0012q · AVControl pilot and C1 staging

AVControl baseline/default built with provisional .text delta −295,582 B. Both report NOT_DELIVERED. The package failed at the %install link. Wrapper fix cf4e0e9 passed the local four-stage RPM test and awaits review. Image job pm0012-image.6nhIbn was reported running. The matched QB file sizes and full Official boot Memory line are verified. C1 Custom verified by running ID and BTF. Three idle samples, both kernel partitions and five gzip/xz trials per tool returned. Same-boot early dmesg rolled over. Live kernel resource bytes changed by −248,768 code and −4,096 rodata. C1 rwdata/BSS split requires the same-boot console record or independent matched evidence. Native gate and replay readback is pinned at 684b7c0. [Evidence, Table A and launchers](../comms/codex_to_claude/0012q_reply.md)

## 0012o · O1 visit and native smoke

PM accepted the passing AVControl baseline smoke and cleanup of 19 lane roots. Pilot, image scan and kernel follow in that order. PC-to-TV connectivity recovered. The kit and target binary hashes match. Slot A is active and both kernel partitions match Official uImage. The same-boot early log reports 8,363 KiB of kernel code. After the 302.68-second Home idle window, O1 produced 0/5 trials. The SDK-owned executable passed its on-board hash check and the PERF kernel rejected its missing signature. The board remains on Official for PM review. [Visit status](../comms/codex_to_claude/0012o_reply.md)

## 0012p · Matched PERF kernel sizes

Official → Custom reduces uImage by 263,728 B, zImage by 104,472 B and RPM size by 184,748 B. The two QB-linked ELF tables await the native readback. The RPI Total uses an unknown measure. [Size tables and native collection](../comms/codex_to_claude/0012p_reply.md)

## 0012m–n · Wed-A, Step 5 and kernel outliner

Official GBS produced the verified A32 Step 5 benchmark. Wed-A M5knpj yielded no qualifying Thumb comparison. The foreground AVControl smoke and O1 run are ready for PM review at c56e4ab. Kernel pin 88c6d9e requires the passing native smoke and adds paired inline/size/board evidence. Which boot container is active and K0–K5 measurements await native and board readback. [Wed-A and board commands](../comms/codex_to_claude/0012m_reply.md) · [Kernel measurements](../comms/codex_to_claude/0012n_reply.md)

## 0012l · Official config candidate and K0 qualification

Native readback found the 156,327-byte perf config (2a316525…) in the matched devel RPM. It remains a same-build candidate. A qualified K0 needs identical config bytes, both published image sizes and section sizes from a verified ELF. The Thursday review pin is ce05cce. No new kernel build or board trace has been run. [PM handoff](../comms/codex_to_claude/0012l_reply.md)

## Official kernel evidence · 24 November

PM accepted O1. The matched USB boot images contain no embedded config. Both yield the same kernel with the O1 GNU build ID and LLD 22.1.8 banner. Qualification of the devel perf config requires the native RPM. The Thursday phase and final-link checks await review and GBS runs. [Evidence and native command](../comms/codex_to_claude/0012k_reply.md)

## Board visit O1 · 24 November

Confirmed Official QB 37736448 on KantSU2E through the Product file and actual BTF hashes. Collected the 2,342-row board roster, 61 target paths and the RAM/CMA map. The kernel exposes no /proc/config.gz. Cold boot confirmed. Three PSS and memory samples completed at one-minute intervals after five minutes at Home. The native Official roster, replay ID and ELF joins await readback. [O1 data](../comms/codex_to_claude/0012j_reply.md)

## Rounds 0012h/i • 24 November

Step 5 rev2 linked on Official 37736448, then failed during evidence collection on missing realpath. The fixed builder is at 9c65ec5; await Claude review and a new native BOARD_TOOLS receipt before board measurements. PM approved b048780 for tonight’s Wed-A and the operator reports starting it. Read pm12read first, then run image with the same WEDA path after exit. F6 and the GCC-family argv readback at 199f5b5 await review. Wed-night selection needs the returned image cause ledger. [Step 5](../comms/codex_to_claude/0012h_reply.md) · [Wed-A and Thursday gates](../comms/codex_to_claude/0012i_reply.md)

## Round 0012f/g • 24 November

Claude approved Step 5 rev2 in the foreground and Wed-A under screen at the existing pin. Wednesday's image scan follows Wed-A. The new review pin `b048780` covers actual driver configs and implicit IT, per-language optimization/LTO and ABI checks, plus Thursday's integrated six-lane kernel job. Await the Wed-A logs and Official image roster before publishing the Wed-night package list. Kernel matrix status is blocked on an authenticated effective Official perf config. No new native sizes, ABI or board results were received. [PM review response](../comms/codex_to_claude/0012g_reply.md) · [Kernel prerequisites and board protocol](../comms/codex_to_claude/0012f_reply.md)

## Round 0012c+d / 0012e • 24 November

- The r0011f transcript and benchmark retry are archived byte-for-byte. Jobs 1–7 completed. Job 8 had zero installed headers on GPT/EROFS; source-attribution and real-image ownership checks remain open. The replacement EROFS reader passed local tests at two offsets and rejected corrupt superblocks. The Step 5 dependency gate now requires glibc-devel-static from Base 1113.1. No native benchmark artifact returned. [Measurements and launchers](../comms/codex_to_claude/0012c_reply.md)
- Three retained spec resets have zero-fuzz patches. Seven pilot packages and two controls are scheduled. Native acceptance T1–T8, the complete Official QB 37736448 roster and per-cause bytes await evidence. Four pilot packages need matched source/build evidence before a package patch. The perf kernel trial and its external modules use separate GBS roots. Board checks follow when KantSU2E is available. Claude review of the new pin is pending. [Thumb testing and schedule](../comms/codex_to_claude/0012e_reply.md)

## Rounds 0012–0012b — 24 November 2026

- The board is unavailable. Step 5 hit an RPM source-staging error before producing the benchmark. The replacement spec passed local RPM staging and build. Native ARM ISA, library provenance and benchmark handoff await a rerun. The revised board-free overnight batch supersedes the original start guard. Both originals and the failure transcript are retained. [Replacement pin and command](../comms/codex_to_claude/0012b_reply.md)
- The development queue is staged for Claude review. It covers EXP-T1, paired TEXTREL image audits, Step 8, strict-link trial, archive consumer checks, four ABI checks and prospective R4/R5. R2, R6 and the R3 diagnostic wait for their recorded gates. Board soak and matched kernel runtime measurements remain open. [Fixtures, limits and launchers](../comms/codex_to_claude/0012_reply.md)
- The full Source1005 patch matches the retained Official OBS bytes and the Customized rev12 source manifest. The independent review prompt is archived. Direct SRPM payload verification awaits the board-free diagnostics. [Patch provenance and launcher](../comms/codex_to_claude/0012a_reply.md)

## Round 0011e — 24 November 2026

- Native chain `pm0011c-chain.AFkXQV` finished at 16:13:39 CST. GCC reference 37564293 and both matched USB bundles are verified in the returned transcript. The Base proof exited normally and reported `REVIEW_STATUS INCOMPLETE`. Missing LLVM SRPMs, an unrecognized platform filesystem and executed compiler provenance remain open. [Chain evidence](../artifacts/evidence/native-run-r0011c-chain-AFkXQV-20261124.txt)
- The uImage sizes equal the retained GBS replay; the zImage sizes differ by +40 B Official and −272 B Customized. Linked vmlinux section equivalence requires the matched-QB artifact. GCC vs LLVM kernel RPM figures remain internal pending the kernel source-identity comparison. Doc 02 rev4 remains the verbatim live export. [Kernel readback and attribution](../comms/codex_to_claude/0011e_reply.md#close-the-base-proof-and-verify-the-kernel-table)
- Board Step 5 can start now with Official QB 37736448. Alternate Official and Customized visits on the same KantSU2E, archive per-lane board RPM rosters and return combined measurements by lane. Start HQ overnight after Step 5 staging releases the shared lock. The diagnostics and board runbook await native execution. [Board-day runbook](../comms/codex_to_claude/0011e_reply.md#board-day-runbook)

## Round 0011d — 24 November 2026

- Doc 02 rev4 is the verbatim live Claude export. It records the source-matched QuickBuild pair and the verified Base change. Rev3 remains in the archive as a superseded repo-authored version. Claude owns live HQ wording. [Doc 02 rev4](../reports/weekly/2026-11-20/02_MLGO_Kernel_Comparison_rev4.md) [Reports index](../reports/README.md)
- The active native chain is `/home1/chengkai/vd-tree/workspace/temp/pm0011c-chain.AFkXQV`. At 16:00 CST, the operator reported GCC reference 37564293 downloading, with 308 MB received and growing. The earlier `pm0011c-chain.xhVzT6` stopped during setup after a raw GitHub SSL timeout for `perf-bundle.py.txt`. The archived rev2 executable change adds five verified download attempts. Use the exact run directory for status and result readback. [Chain rev2](../artifacts/evidence/native-cmd-r0011c-gcc-ref-usb-baseproof-rev2.sh) [Current reply](../comms/codex_to_claude/0011d_reply.md)
- The sequence is chain result review, board Step 5, overnight HQ, then Steps 9 and 8. The chain's per-job receipts and results are still pending.

## Round 0011c — 24 November 2026

- Step 2 passed. Official QB 37736448 published LLVM Base 20261113.1 and Customized QB 37736427 published 20261118.1. The published `build.conf@14452507` and supplied shelf/Base lists matched their pins. All 5,880 Product rows matched source version and pinned VCS. Doc 02 rev3 records the source-matched Base comparison. Model attribution and board metrics remain pending. [Step 2 transcript](../artifacts/evidence/native-run-r0011-step2-pair-gate-20261124.txt) [Doc 02 rev3](../reports/weekly/2026-11-20/02_MLGO_Kernel_Comparison_rev3.md)
- Claude accepted 0011a and 0011b and verified the scanner, overnight and weekend launcher pins. The operator started a serial native chain under `workspace/temp/pm0011c-chain.*` for GCC reference 37564293, both USB staging jobs and the MLGO Base proof. The unchanged script and its four pins were verified locally. Await the per-job results. [Archived chain](../artifacts/evidence/native-cmd-r0011c-gcc-ref-usb-baseproof.sh)
- After the chain, verify both USB manifests and run board Step 5. Then start the overnight HQ batch, followed by Steps 9 and 8 once the batch exits. The approved weekend evidence export can run independently. [Readback and run order](../comms/codex_to_claude/0011c_reply.md)


## Round 0011a

- Claude accepted the original 0011 pins. The Official capture was reported running. Run the read-only manifest lookup in parallel and wait for both capture identities before Step 2.
- Keep GCC reference capture and USB staging ahead of extended HQ scans. The new serial overnight wrapper runs GCC then LLVM then compare. Run four-lane Step 8 after the batch. New HQ pins await review.
- HQ totals now use matched pinned VCS and source versions. Stripped or FILE-symbol-missing LTO pairs remain in a separate count. Readback includes prelink markers and bytes/KiB. The weekend transcript and new scans are pending. [Run order and commands](../comms/codex_to_claude/0011a_reply.md)

## Round 0011

- The operator supplied new Official QB 37736448 and Customized QB 37736427. Step 1 launcher hash verified. Native capture, submitted lists and effective Product source results are pending. Keep MLGO attribution at Base swap.
- Use GCC no-prelink QB 37564293 for new HQ comparisons. The native captures and two ELF scans are staged. GCC 10.1 and LLVM 10.0 are different Base series, and Product snapshots are ten days apart. Attribute only source-qualified rows to the matched subset and retain the rest as separate observations.
- GCC reference config names an LLVM local repository. Future GCC builds require a dedicated empty local repository and the path guard. Historical gccL configuration use remains unproved.
- The PM reports all six weekend jobs finished. The 517-line combined transcript and remaining pages have not returned. [Runbook and review inputs](../comms/codex_to_claude/0011_reply.md)

## Round 0010f

- Claude accepted the 0010b–0010e commits and the pinned Step 8 and MLGO Base proof commands. Run the proof after both Step 1 captures. Doc 02 keeps Base-swap attribution until evidence supports a narrower claim.
- Use exp8 verbose, pairs and treatments in that order. Sizes is optional after heavy jobs. Doc 07 source attribution, Doc 04 rows 2–3 and the R2–R6 injection values stay pending those returns.
- Doc 05 row 18 is verified on PERF. Row 17 awaits a matching installed identity for mic-bootstrap. Retail coverage stays an internal evidence gap. [Approved run order and report gates](../comms/codex_to_claude/0010f_reply.md)

## Rounds 0010c–0010e

- Lane C uses the byte-verified native hook. Step 8 adds the independent D lane for seven A32 sources and reports all four A32 shares. Doc 04 rev2 is archived alongside Doc 02 rev2. WARN versus FINAL ELF parity awaits retained-RPM readback.
- The exp8 inventory provides 25 candidate sources and 153 variant records. Historical 22/151 membership, exact injection recipes and the four verbose-log argv readbacks remain open. Preserve the z901 experiment directories, local build logs and retained variant RPMs. [Step 8](../comms/codex_to_claude/0010c_reply.md) [Exp8 reply](../comms/codex_to_claude/0010e_reply.md)

## Round 0010b

- Claude accepted round 0010 at 18e939a, verified its launcher pins and kept Monday steps 1–10 in order. Round 0010f records Claude’s acceptance of these pins.
- The original 20 November archive still verifies. Doc 02 rev2 records Base-swap attribution and has its own manifest. A compact proof for the matched captures is staged. The native SRPM/digest comparison and board A/B are pending.
- Lane C has the recovered expanded 11 November hook. It includes the Thumb and hardening flags. R1–R7 remains gated by the exact 22-source roster. Preserve the z901 experimental directories and GBS logs. Step 8 checks the tvs-core alias against the pinned P4 spec.
- The retained A32 cohort has seven DWARF-supported -marm rows and five Bluetooth candidates without matching -marm evidence. Crosswalk samples are pinned for two GBS captures. The exact rank 1–211 readback and retail-roster evidence remain open. [Round 0010b reply](../comms/codex_to_claude/0010b_reply.md)

## Round 0010 and 0010a

- Saved the 20 November weekly report verbatim with all eight manifest checks passing. The weekly archive path is fixed by D-043.
- Full 609-row A32 ledger joined to the installed RPM headers. The scan gives 343.1 MiB. The retained top-40 readback differed in 14 rounded estimates. Ranks 41–211 and exact per-file rootfs coverage await the native packet. The installed roster disproves the build-host-only characterization of sys-tools for this PERF image.
- Doc 04 resolves to 24 exact installed source names, nine unmatched and one alias pending. Packaged-code A/B replay, separate per-option recipes and the four-package ABI static check are staged. Round 0010b recovered the historical expanded hook for lane C. No new GBS result was inferred.
- Capture both new QBs when published, check the fixed lists and build.conf, audit Official, retain rollback, then run the board and Thumb gates. The updated board runner uses a GBS-only benchmark build. [Reply and Monday commands](../comms/codex_to_claude/0010_reply.md)


## Round 0009

- Tizen GNU ld 2.43 default links the ABS32-in-`.text` fixture as a DSO and PIE with TEXTREL. Strict mode rejects both. HQ design is ready for review with the shipped-image baseline pending.
- The captured PERF 37654439 bundle is flat. The patched audit reads it directly and reports coverage gaps. The USB helper stages the operator's `updateSU2E/` layout and writes a per-file manifest. Old Official publication returned 404. Secure the matched pair and rollback before board day.
- Both replacement QB lanes use `@14452507`. The old pair's LTO-exclusion mismatch is the leading explanation for all positive user-space .text growth. Four packages account for 45 of 50 changed ELF rows and +1,379,302 bytes. The other five remain unattributed.
- The 1,884 `-marm` lines are from GCC SERET-UL. The 302 `-mthumb` lines are RPM environment traces. PERF mapping, exact config and argv truncation readback are staged. External module comparison has 60 .text changes across 44 owners and two identical rows, 62 comparable rows across 45 owners.
- EXP-T1 uses the identical Base Clang helper with a single option delta across three local GBS source pairs. Complete the PERF ISA gate and review native launchers before execution. [Round 0009 reply](../comms/codex_to_claude/0009_reply.md)

## Round 0008a

- Customized PERF, four kernel RPMs and 5,880 Product identities are archived on the native server. The relocation scan and retained-root GNU ld probe were pending at this checkpoint. Round 0009 resolves the linker probe and bundle layout.
- Four Base metadata checks and five input pins passed. The old GBS input pair normalizes to Base-only. The published Product build.conf hashes differ. The older Customized configuration retains LTO exclusions for four of the nine changed-.text packages. Both new submissions use `@14452507`.
- All nine published NEVRA, SRPM and P4 identities match. Treat historical .text differences as a mixed build.conf and Base A/B. The 115 packaged kernel modules include 105 changed hashes. A separate scan found 60 changed external-module .text rows. Detached BTF kind deltas are verified for GBS.
- Both Product build.conf files enable the GCC force-options RPM scriptlets. The identical Base OBS configs omit them. New GBS launchers require and probe a live Product URL. [Round 0008a readbacks](../comms/codex_to_claude/0008_reply.md#round-0008a-native-results)

## Retained round 0008 update

- The operator confirmed that the PERF image is uninstrumented and ASAN is part of the QB job name. Close the gate on operator evidence. Use the ten-ELF spot check as corroboration when the image is available.
- The HQ PIC design covers producer PIC, strict native shared/PIE link enforcement and a release ELF audit. The retained old matrix explicitly used `-z text`. The current image's relocation counts and native GNU linker default require native readback. [HQ draft](../hq/PIC_FatLTO_Dual_Path_Design.md) [Native launchers](../comms/codex_to_claude/0008_reply.md)

## Retained round 0007 update

- Friday's static MLGO report records 4,784 of 4,834 comparable user-space ELFs with identical .text. Fifty changes across nine packages remain subject to the exact two-repository source join. The packaged kernel BTF and kernel image sizes are recorded separately. Local and published kernels reproduce size trends and have different hashes. Board measurements remain pending. [Friday report](../reports/MLGO_Official_vs_Custom_20261120.md)
- Official QB 37627297 Product 20261117.2 returned HTTP 404 for its root, PERF and kernel RPM. Customized QB 37654439 needs the native availability check now. D-037 requires immediate retention after each necessary QB. D-038 retains ltoexp2 and submits both lanes simultaneously with only the Base URL changed. QB has no Product changelist selector. [Combined reply](../comms/codex_to_claude/0007_reply.md)
- The GBS probe shows GCC's generated wrapper appends Thumb, optimization and warning policy. Clang without the mode option produced A32. The 609 roster is stable, and 603 packaging origins remain unverified. Current QB/OBS wrapper activation, four package compile traces and the matched Thumb measurements remain open. [Origin ledger](../artifacts/ledger/thumb-producer-origin-20261119.md)
- Round 0007 native launchers passed local Python 3.10.12 fixture checks. Claude review, operator execution and actual native or board results are pending.

## Retained 19 November checkpoint


- Customized QB 37654439 finished on Base 20261118.1, paired against Official QB 37627297 on Base 20261113.1. The Product RPM identity comparison completed. The per-ELF section pass is running. [Fixed inputs](../comms/codex_to_claude/0005_reply.md#published-quickbuild-pair)
- KantSU2E is running Linux 6.12.60 built with Clang/LLD 22.1.8. The pending kernel shelf passed the source gate with both release advisors and the perf defconfig. The QB kernel log remains unavailable under REST 403. Both local GBS builds completed, verified both release advisors in local argv and recorded tool-owner hashes. QB runtime metrics remain whole-image A/B.
- Friday's MLGO report measures the kernel. User-space ELF identity is the control, with every unexplained byte difference listed.
- The historical 106 lacks a recovered original image, report and method. Use the forthcoming user scan to assemble the command-backed roster. Appendix A was withdrawn. The new HQ response is a draft.
- Native preflight verified byte-identical Base and shelf lists. Base 20261118.1 Clang RPM pins are complete for both arches at OBS rev12. The non-LLVM delta overlaps 177 of 2,342 installed identities by name/arch. The host replay stopped after source staging. The user confirmed the ELF exists and requires the GBS build environment. The first GBS attempt verified both configs and 24 source overlays, then hit a read-only spec. The foreground kernel resume completed both lanes without repeating P4.
- ARM/Thumb scan completed with 2,342 RPMs and zero scan errors. It recorded 609 ARM-predominant loadable ELFs; cause attribution and the GBS default probes are open. T5 is blocked by QuickBuild REST 403. PIC matrix 56/56, RPM screen 78/92 scanned and 14 incomplete. Compiler sample 80/81 Clang-marked ELFs. Argot client and TPK are committed cargo-tizen prebuilts. Producer is argo-tizen CI using cargo-tizen v0.6.7. CODEOWNERS is @AGENTIC/argo-tizen-maintainers; youngb.shin submitted the artifacts. The pinned readback shows armv7l, no explicit Thumb override, and both Rust target variants installed in CI. The effective target/triple still requires producer argv or equivalent provenance. T4 separates `.ko` files after the lone unclassified sample proved to be `emdev.ko`. T7 identified the shipped FatLTO hit as capi-base-common-devel-static tizen_error.c.o with three TLS_LE32 relocations. Its link consumers and four other TLS-only archives await the GBS probe.

- Friday MLGO uses the real QB image pair. The Product run found 2,289 differing RPMs, 50 identical and 3 unresolved. The kernel payload sizes are recorded. The packaged vmlinux has been identified as raw BTF (+124,625 B). BTF kind counts, local ELF .BTF and user-space section classification are pending. The two-root GBS run supplies secondary effective-argv evidence. Resolve the two full flash artifacts serially. Both internal Product directories and their parents timed out here. Exact flash URLs, artifact-to-board identity, recovery prompts, 4K clip/counter qualification and measurements remain pending. [Board-day checklist](../reports/KantSU2E_MLGO_Board_Day_0005.md)

[Round 0005 native evidence and launchers](../comms/codex_to_claude/0005_reply.md)

| Workstream | Evidence-backed state | Next gate |
|---|---|---|
| 10.0 image/compiler ledger | T-KSU2EJAKUC-0101-PERF-202611171009, 2,342 installed RPMs, 1,839 source strings | Payload, DWARF/source attribution, in-scope coverage and exact QB job export |
| gst-ffmpeg and AVControl | Scoped TV seek regression and AVControl static closure still valid | Repeated current-image and dynamic consumer acceptance |
| Customized MLGO | Booted Clang/LLD kernel and pinned 14427407 source evidence. Published arch pins complete, both advisors confirmed in local GBS argv | QB pair compared; BTF kind counts, local .BTF, and user-space section counts pending; actual GBS config diff and flash paths pending |
| 10.1 parallel | Scoped bootstrap, smoke and RPM layout passed | Production accelerator compatibility, bounded by D-018 |
| HQ PIC/ABI | Producer policy drafted, 56 synthetic outcomes retained, basic ARM classifier exercised | Qualify unclassified members, intended consumers and release checks |
| Thumb | User scan replaces dynsym working cohort. Original 106 origin unverified | Join actual build commands, argot target/ABI proof and paired sizes |
| 1 GB / memory | Memory ranges and normal-board top-20 VMA evidence recorded | 4K pool mapping, attended Method A pilot, paired measurements |
| Capacity | Last available /home1 239.68 GiB, older vd-tree size 348.73 GiB | Live native capture and confirmed concurrency bounds |

[Tracker](../artifacts/progress_tracker.csv) records scoped completions and current dependencies. Overall adaptation coverage and performance/memory acceptance remain unknown.

[Verified 229-line Round 0005 result](../artifacts/evidence/native-run-r0005-20261118.txt) records the full pins, Base pair counts, Makefile, argot packaging, relocation and compiler sample evidence.

The Thumb cause ledger reads the completed scanner CSVs under `results/`. The GBS pair uses its explicit cause ledger and the newly built RPMs. The path fix passed a local Python 3.10.12 layout fixture and awaits native review. [Round 0005](../comms/codex_to_claude/0005_reply.md#thumb-scan-layout-fix)

The Thumb cause run verified two argot prebuilts and left 607 unresolved. The packaging-origin table records four additional bundled vd_memps paths supported by the retained same-NEVRA spec. The GCC query failure under RPM stopped the first defaults probe. A non-fatal, reviewed-run GBS resume is staged behind the full section scan. Kernel flag totals alone leave the generated config and mixed-flag classification open. [Round 0006](../comms/codex_to_claude/0006_reply.md) [Thumb provenance ledger](../artifacts/ledger/thumb-producer-origin-20261119.md)

### Round 0011b

Official QB 37736448 and Customized QB 37736427 captures completed with 5,880 Product identities and four kernel RPMs each. Customized `tztv-kernel-perf` archive size is 184,748 B smaller. Published Base selector and Product VCS validation, GCC reference capture, board A/B and model-only attribution remain open. [Step 2 and native order](../comms/codex_to_claude/0011b_reply.md)

The verbose AVControl and tv-viewer builds show package source replacing platform flags and 26 / 549 observed Clang invocations without `-mthumb`. WARN/FINAL `.text` matches for the seven verified comparator ELFs. The 609-file A32 cohort now has exact bytes and measurement basis for ranks 1–211. The previous `NOT_RETURNED` state for those rows is resolved. The PERF vmlinux maps to A32 in both retained GBS lanes and the pilot's ISA/argv gate is satisfied. Exact config values are pending. [Flag origins](../artifacts/ledger/thumb-flag-origins-20261124.tsv) [Exact A32 ledger](../artifacts/thumb-repro/a32-exact-top211-20261124.tsv)

R1 historical forced-option variants have delivery evidence for four measured packages. R2–R6 remain gated pending exact path-level deltas and verified effective flags. The continuation and comparison launchers await Claude review. [Delivery ledger](../artifacts/ledger/r1-r7-delivery-20261124.tsv)
