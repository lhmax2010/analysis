# Official versus Customized MLGO — kernel comparison record

The Friday, 20 November report uses the completed KantSU2E QuickBuild pair. The native Product RPM comparison is complete. ELF section qualification and board measurements remain pending.

The 11 November image report recorded release MLGO in the Linux kernel and byte-identical outputs in the sampled user-space control after disabling ML inlining. For this image pair the kernel is the primary measurement and user space is the identity control. The current board boots Linux 6.12.60 built by Clang/LLD 22.1.8, with tztv-kernel-perf installed. The planned shelf list selects the vdlinux change that records both advisor switches. The post-login source gate passed. Actual QB argv and compiler-install records remain unavailable through the current REST account. Use the source and image criteria below to interpret the Base comparison. [Kernel evidence](../artifacts/evidence/kernel-mlgo-source-chain-20261117.txt)

| Lane | QuickBuild | Base | Published Product |
|---|---|---|---|
| Official | `37627297` | `20261113.1` | `TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261117.2` |
| Customized | `37654439` | `20261118.1`, pinned LLVM rev12 | `TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261118.2` |

The operator reported QB 37654439 finished and completed the pinned Product comparison using its fixed repository. These results are the primary Friday evidence for kernel, modules and user-space payloads. The approved board measurements use the full flash images from these same two QuickBuild runs. Compare the two actual GBS config files separately to confirm input parity outside the two repository URLs and local buildroot. [Fixed repositories and config check](../comms/codex_to_claude/0005_reply.md#published-quickbuild-pair)

| Metric | Procedure | Result |
|---|---|---|
| Kernel and modules | Same perf variant; compare Image, published zImage/uImage where present, vmlinux section bytes and installed .ko counts/sizes. Separate stripped/unstripped and compressed/uncompressed sizes. | uImage −2.32%, zImage −1.96%, modules −0.29%, packaged vmlinux +3.37%. Section sizes pending. |
| Boot | Five matched cold boots per lane; same board, firmware and Home-ready marker | Pending |
| Kernel microbenchmarks | Preselect runnable syscall, scheduling/context-switch and memory probes; five blocked runs per lane after a warm-up, fixed CPU affinity, frequency policy and load | Pending |
| Normal-memory 4K | Three matched runs per lane; identical stream/player/firmware, CPU and dropped or late frames, stalls and new regression signatures | Pending |
| User-space identity | SHA-256 by installed path and package owner on identical scope; list added, removed and byte-different ELF, with Build IDs for triage. Correlate with non-LLVM inventory delta and rebuilt package records. Treat every unexplained difference as a confounder. | 2,289 RPMs differ, 50 match, 3 unresolved. ELF section qualification pending. |

Keep each run and both exact artifacts. Preserve rollback before flashing. Report median, IQR, interval and all absolute regression events. Capture compiler/version, model evidence and any kernel source/config/link-mode difference alongside the result. User-space identity concerns file bytes. It does not imply equal runtime behavior after a kernel change.

## Supporting GBS compiler command evidence

The QB kernel build log remains unavailable under HTTP 403. Use the retained two-root GBS build only for effective local compiler argv and accelerator identity. The launcher holds the Product inputs and build.conf fixed and changes the Base in the reproduction. This is a local reconstruction of the compiler commands. Report the real QB image's size and module results from the published artifacts. [Foreground GBS resume](../comms/codex_to_claude/0005_reply.md#foreground-kernel-resume)

The first GBS attempt verified the configs, build.conf 14452507 and 24 vdlinux overlays before stopping at the read-only spec. Keep the owner-write resume and run it only after the Product comparison releases the heavy lock. Full flash-image downloads use that same lock. [Native GBS log](../artifacts/evidence/native-run-r0005-argot-scan-gbs-20261118.txt#L432) [Board-day procedure](KantSU2E_MLGO_Board_Day_0005.md)

## Round 0005 preflight and confounders

Native preflight verified identical Base and shelf lists and counted 3,000 delta rows, 2,952 outside LLVM. The direct OBS replay proved the following published Base 20261118.1 Clang RPM bytes correspond to OBS revision 12, source digest `0b38aead137ec42dcd99dee28091acc1`. The hashes identify the published RPMs. The kernel compile command and resolved executable remain open. [Native binary pin](../artifacts/evidence/native-run-r0005-20261118.txt#L3)

| Architecture | Published Clang RPM | SHA-256 |
|---|---|---|
| armv7l | `clang-22.1.8-11.1.armv7l.rpm` | `6e692d5fb4f372c9e8d8f969b5171ce73275a7f613ae1f9694797758cf66b1a9` |
| x86_64 | `clang-22.1.8-11.1.x86_64.rpm` | `ed6db88c182662fb81007ffe4589c49792970e14d110b95ebf6744de2949a3d2` |

| Non-LLVM category | Classified events | Unique name/arch | Board name/arch | Board exact Official NEVRA |
|---|---:|---:|---:|---:|
| Release only | 1,363 | 1,354 | 175 | 174 |
| Ambiguous multi-version | 52 | 26 | 2 | 2 |
| Same NEVRA with payload difference | 18 | 9 | 1 | 1 |
| Version or epoch change | 0 | 0 | 0 | 0 |

The deduplicated name/arch overlap is **177 of 2,342**. Category counts overlap. Zero version changes describes the resolved version/epoch pairs. The 52 ambiguous events still require reconciliation. This is a repository-to-installed-inventory join. Compare actual image payloads, including the same-NEVRA case and workload-relevant release bumps, before attributing observed differences. QB IDs and Product URLs are fixed. The Product compare output is archived. TV measurements remain pending. [Native Base delta](../artifacts/evidence/native-run-r0005-20261118.txt#L11)

## Source gate and image attribution

**Source-level gate passed.** The pending vdlinux shelf 14427407 selects Base Clang and LLVM under `_toolchain clang`, sets `LLVM=1 LLVM_IAS=1`, and enables `CONFIG_MLGO=y` in the KantSU2E perf defconfig. Makefile lines 1065–1070 add `-mllvm -enable-ml-inliner=release` and `-mllvm -regalloc-enable-advisor=release` to `KBUILD_CFLAGS` under `CONFIG_MLGO_INLINER` and `CONFIG_MLGO_REGALLOC`, respectively. The QuickBuild kernel log remains unavailable after REST HTTP 403. Effective argv and the exact executing compiler remain unverified. [Native source gate](../artifacts/evidence/native-run-r0005-20261118.txt#L22)

**The user-space byte-identity criterion failed for this image pair.** Of 2,342 Official installed package identities resolved against the published repositories, 2,289 RPMs differed, 50 were identical and 3 were unresolved. The comparer flagged 2,279 package rows as potential user-space confounders. The flags include ELF changes, other payload changes and differences outside the expected Base delta. This screening establishes which packages need review. The ELF-section audit will quantify how often executable bytes and other runtime sections changed. If there are broad code changes or unresolved differences in workload dependencies, report board measurements as whole-image A/B observations. The data currently support that qualified interpretation. [Native image comparison](../artifacts/evidence/native-run-r0005-image-compare-20261118.txt)

Reconcile candidate-only and removed packages against the actual board inventories. Verify workload-relevant non-ELF inputs and dependencies even when changed packages are in the expected Base delta. Use local compiler argv as supporting provenance. Keep model-only causal claims contingent on controlling other build inputs, dependencies and the effective compiler/linker path. [Round 0005 independent review](KantSU2E_MLGO_Board_Day_0005.md#independent-review-of-mlgo-attribution)


## Published kernel payload sizes

| Payload | Official bytes | Customized bytes | Delta |
|---|---:|---:|---:|
| uImage | 11,348,968 | 11,085,240 | −263,728 (−2.32%) |
| zImage | 5,326,496 | 5,222,024 | −104,472 (−1.96%) |
| 115 modules | 6,567,110 | 6,547,762 | −19,348 (−0.29%) |
| `/lib/modules/perf/6.12.60/kernel/vmlinux` | 3,696,242 | 3,820,867 | +124,625 (+3.37%) |

Individual modules changed in both directions. The native run emitted no `VMLINUX_SECTION` rows. File size and pathname alone cannot establish the file format, stripping status, or which sections contributed to the increase. A packaged `vmlinux` and compressed boot images can vary independently because packaging, included material and compression affect those sizes. Identifying the actual increase requires inspecting the verified RPM members. [Native kernel output](../artifacts/evidence/native-run-r0005-image-compare-20261118.txt#L15) [Section-audit launcher](../comms/codex_to_claude/0005_reply.md#published-image-comparison-and-attribution)
