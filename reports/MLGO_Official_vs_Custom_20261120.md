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
| Kernel and modules | Same perf variant; compare Image, published zImage/uImage where present, vmlinux section bytes and installed .ko counts/sizes. Separate stripped/unstripped and compressed/uncompressed sizes. | uImage −2.32%, zImage −1.96%, modules −0.29%. Rootfs vmlinux is raw BTF, +3.37%. Local ELF .text −2.90%. |
| Boot | Five matched cold boots per lane; same board, firmware and Home-ready marker | Pending |
| Kernel microbenchmarks | Preselect runnable syscall, scheduling/context-switch and memory probes; five blocked runs per lane after a warm-up, fixed CPU affinity, frequency policy and load | Pending |
| Normal-memory 4K | Three matched runs per lane; identical stream/player/firmware, CPU and dropped or late frames, stalls and new regression signatures | Pending |
| User-space identity | SHA-256 by installed path and package owner on identical scope; list added, removed and byte-different ELF, with Build IDs for triage. Correlate with non-LLVM inventory delta and rebuilt package records. Treat every unexplained difference as a confounder. | 2,289 RPMs differ, 50 match, 3 unresolved. ELF section qualification pending. |

Keep each run and both exact artifacts. Preserve rollback before flashing. Report median, IQR, interval and all absolute regression events. Capture compiler/version, model evidence and any kernel source/config/link-mode difference alongside the result. User-space identity concerns file bytes. It does not imply equal runtime behavior after a kernel change.

## Supporting GBS compiler command evidence

The foreground replay completed both lanes from the same vdlinux input (14293732 + 14427407, 24 overlays), same Product URL and `published-build.conf` (P4 14452507). The launcher compared the two staged GBS configs after normalizing the Base URL and buildroot. Each local lane retained 7,100 command entries containing both release advisors. The sampled compiler driver target is `arm-linux-gnueabi`. Installed Clang and LLVM moved from `22.1.8-9.1` to `22.1.8-11.1` and `clang-accel-x86_64-armv7l` from `0.4-2.4` to `0.4-2.5`. The trace identifies both ARM and x86-64 compiler files by owner and hash. The full installed dependency set was not diffed. Production QB argv remains unavailable under REST HTTP 403. [GBS evidence](../artifacts/evidence/native-run-r0005-gbs-kernel-thumb-20261118.txt#L68)

**Official model.** Base 20261113.1 provides Clang `22.1.8-9.1`, from `llvm-22.1.8-9.1.src.rpm`. The retained Official OBS revision 10 spec enables MLGO by default for armv7l, aarch64 and x86-64. It selects the corresponding VD model archive and explicitly overrides both AOT model headers and objects. “Official” means the VD baseline's bundled release inliner and register-allocation eviction models. The capture does not establish that the weights are the upstream stock artifacts. Customized is the pinned rev12 package with the SR models/runtime inputs. [Pinned Official OBS source](../artifacts/evidence/official-mlgo-obs-source-excerpt-20261119.txt) [Customized input pin](../artifacts/evidence/mlgo-source-submit.txt)

Upstream LLVM 22.1.8 raises an error when the requested inliner cannot be initialized. The regalloc legacy path can construct a default provider while emitting an error for the unavailable requested advisor. A successful compile with both release options is consistent with the Official spec's embedded models. [LLVM inliner](https://github.com/llvm/llvm-project/blob/llvmorg-22.1.8/llvm/lib/Transforms/IPO/Inliner.cpp) [LLVM eviction advisor](https://github.com/llvm/llvm-project/blob/llvmorg-22.1.8/llvm/lib/CodeGen/RegAllocEvictionAdvisor.cpp)

### Local GBS reproduction against QuickBuild

| Payload | Official GBS | Official QB | QB − GBS | Customized GBS | Customized QB | QB − GBS | GBS custom − official |
|---|---:|---:|---:|---:|---:|---:|---:|
| uImage | 11,348,968 | 11,348,968 | 0 | 11,085,240 | 11,085,240 | 0 | −263,728 (−2.32%) |
| zImage | 5,326,464 | 5,326,496 | +32 | 5,222,304 | 5,222,024 | −280 | −104,160 (−1.96%) |
| 115 modules | 6,507,334 | 6,567,110 | +59,776 | 6,487,666 | 6,547,762 | +60,096 | −19,668 (−0.30%) |

Equal uImage lengths await the local SHA-256 join to the published member. In the 12 module paths present in both previews, the Official QB offset is +512 bytes for nine and +576 bytes for three, while the Customized offset is +512 bytes for all twelve. That pattern is consistent with fixed-size packaging additions such as signatures. Strip or signing details and the full 115-path distribution require inspection of the packaged bytes or sign step. The published module delta is 320 bytes smaller in magnitude than the local delta. [GBS module rows](../artifacts/evidence/native-run-r0005-gbs-kernel-thumb-20261118.txt#L145) [Published module rows](../artifacts/evidence/native-run-r0005-image-compare-20261118.txt#L17)

### Local GBS linked vmlinux sections

| Section | Official bytes | Customized bytes | Delta bytes | Delta |
|---|---:|---:|---:|---:|
| .text | 8,564,600 | 8,315,832 | −248,768 | −2.90% |
| .init.text | 225,372 | 220,192 | −5,180 | −2.30% |
| .exit.text | 10,392 | 9,860 | −532 | −5.12% |
| .rodata | 1,334,714 | 1,333,098 | −1,616 | −0.12% |
| .data | 666,016 | 666,112 | +96 | +0.014% |
| __bug_table | 16,644 | 14,964 | −1,680 | −10.09% |
| .init.smpalt | 30,448 | 24,832 | −5,616 | −18.45% |
| .symtab | 1,763,968 | 1,801,488 | +37,520 | +2.13% |
| .strtab | 2,456,712 | 2,523,959 | +67,247 | +2.74% |
| .debug_frame | 1,373,692 | 1,487,400 | +113,708 | +8.28% |
| Sum of reported ELF section sizes | 152,432,813 | 149,949,301 | −2,483,512 | −1.63% |

The selected code and data sections (.text, .init.text, .exit.text, .rodata and .data) total **10,801,094 → 10,545,094 bytes, −256,000 (−2.37%)**. This sum excludes .bss, BTF and other allocatable sections and does not measure resident memory. The pattern is consistent with changed inlining and out-of-line function retention. Inlining decisions, symbol kinds, and the number of unwind FDEs require their own evidence. The size changes also combine input-package and register-allocation effects. [Linked ELF section sizes](../artifacts/evidence/native-run-r0005-gbs-kernel-thumb-20261118.txt#L161)

## Round 0005 preflight and confounders

Native preflight verified identical Base and shelf lists and counted 3,000 delta rows, 2,952 outside LLVM. The direct OBS replay proved the following published Base 20261118.1 Clang RPM bytes correspond to OBS revision 12, source digest `0b38aead137ec42dcd99dee28091acc1`. The hashes identify the published RPMs. The local replay independently records compiler identity and both advisor flags. [Native binary pin](../artifacts/evidence/native-run-r0005-20261118.txt#L3)

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

**Source-level gate passed.** The pending vdlinux shelf 14427407 selects Base Clang and LLVM under `_toolchain clang`, sets `LLVM=1 LLVM_IAS=1`, and enables `CONFIG_MLGO=y` in the KantSU2E perf defconfig. Makefile lines 1065–1070 add `-mllvm -enable-ml-inliner=release` and `-mllvm -regalloc-enable-advisor=release` to `KBUILD_CFLAGS` under `CONFIG_MLGO_INLINER` and `CONFIG_MLGO_REGALLOC`, respectively. The QuickBuild kernel log remains unavailable after REST HTTP 403. The local two-root GBS replay verifies advisor argv and records the resolved tool files. The actual QB invocation remains unavailable. [Native source gate](../artifacts/evidence/native-run-r0005-20261118.txt#L22)

**The user-space byte-identity criterion failed for this image pair.** Of 2,342 Official installed package identities resolved against the published repositories, 2,289 RPMs differed, 50 were identical and 3 were unresolved. The comparer flagged 2,279 package rows as potential user-space confounders. The flags include ELF changes, other payload changes and differences outside the expected Base delta. This screening establishes which packages need review. The ELF-section audit will quantify how often executable bytes and other runtime sections changed. If there are broad code changes or unresolved differences in workload dependencies, report board measurements as whole-image A/B observations. The data currently support that qualified interpretation. [Native image comparison](../artifacts/evidence/native-run-r0005-image-compare-20261118.txt)

Reconcile candidate-only and removed packages against the actual board inventories. Verify workload-relevant non-ELF inputs and dependencies even when changed packages are in the expected Base delta. Use local compiler argv as supporting provenance. Keep model-only causal claims contingent on controlling other build inputs, dependencies and the effective compiler/linker path. [Round 0005 independent review](KantSU2E_MLGO_Board_Day_0005.md#independent-review-of-mlgo-attribution)


## Published kernel payload sizes

| Payload | Official bytes | Customized bytes | Delta |
|---|---:|---:|---:|
| uImage | 11,348,968 | 11,085,240 | −263,728 (−2.32%) |
| zImage | 5,326,496 | 5,222,024 | −104,472 (−1.96%) |
| 115 modules | 6,567,110 | 6,547,762 | −19,348 (−0.29%) |
| `/lib/modules/perf/6.12.60/kernel/vmlinux` | 3,696,242 | 3,820,867 | +124,625 (+3.37%) |

Individual modules changed in both directions. The QuickBuild `tztv-kernel-perf` payload owns the rootfs file named `vmlinux`. Its validated header describes an independent raw BTF v1 blob. This file holds type metadata and a string table. The entire increase is explained by their stored lengths. [Native kernel-only capture](../artifacts/evidence/native-run-r0006-causes-kernel-sections-20261119.txt#L244) [BTF format](https://docs.kernel.org/bpf/btf.html)

| Packaged BTF component | Official bytes | Customized bytes | Delta |
|---|---:|---:|---:|
| Header | 24 | 24 | 0 |
| BTF type records | 2,207,044 | 2,282,972 | +75,928 (+3.44%) |
| BTF strings | 1,489,174 | 1,537,871 | +48,697 (+3.27%) |
| Total | 3,696,242 | 3,820,867 | +124,625 (+3.37%) |

**BTF kind counts pending.** More FUNC/FUNC_PROTO records could explain some growth, but the header lengths alone do not establish record counts or their cause. The local ELF's .symtab, .strtab and .debug_frame increased separately. Those sections are absent from the raw BTF file. The kernel boot image can shrink while rootfs metadata grows. Upstream 6.12 also links allocatable .BTF into the running kernel image when CONFIG_DEBUG_INFO_BTF is enabled. Confirm that option, the local .BTF size delta and any exact blob match through the pinned native decoder. The published rootfs file's size does not establish resident RAM or whether a tool opens that file versus reading kernel-exported BTF. Actual VD tooling load and lifetime remain unmeasured. [Kernel v6.12 link procedure](https://github.com/torvalds/linux/blob/v6.12/scripts/link-vmlinux.sh#L100-L123) [Native decoder](../comms/codex_to_claude/0006_reply.md#packaged-btf)
