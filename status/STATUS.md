# Status — 2026-11-20, round 0008

## Round 0008

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
