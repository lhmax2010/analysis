# Goal, scope and acceptance

[Verified: user-relayed request](../comms/claude_to_codex/0001_handover_request.md): migrate Tizen toolchain use from GCC to LLVM, then optimize performance and memory. Codex executes, develops and analyzes; Claude coordinates and reviews; the user retains final authority. Disagreements remain explicit.

[Verified: retained master plan](../artifacts/progress_tracker.csv): primary product is Tizen TV 10.0, ARMv7 `armv7l`, on KantSU2E. Tizen 10.1 adaptation proceeds **in parallel**, not after 10.0 completion. The 10.1 Base with 10.0 Product combination requires separate acceptance. It is not an approved interchangeable Base today.

[Verified: retained Base/SDK report](../artifacts/historical-reports/base-changes-part-01.md): intentional GCC toolchain components, vendor prebuilts, SDK/cross tools and other-language builds are distinct from source packages accidentally bypassing Clang. GCC-built code is not automatically an ABI defect. Kernel/TEE/driver builds use separate compiler mechanisms. Rust uses its own LLVM-based compiler and Go its own toolchain.

**Final exception register is not signed off.** The historical scope retains glibc, GCC/cross GCC and selected tools. Do not infer user approval to change kernel, bootloader, Fortran or all vendor binaries. The new Customized MLGO kernel study is a separate experimental workstream, not proof of a global kernel compiler transition.

| Architecture | Role | Evidence/status |
|---|---|---|
| armv7l | Primary TV product and package validation | [Verified] target capture and ARM package probes |
| x86_64 | Build acceleration, host toolchain/runtime models and OBS build | [Verified] production host/target matching remains a 10.1 gate |
| aarch64 | Model/runtime assets and cross components | [Verified] assets prepared; complete device acceptance unknown |
| riscv64 | Historical cross-toolchain configuration | [Verified] historical report; no active product acceptance evidence |

## Proposed definition of done

[Assumption/Memory: Codex proposal, D-008] Agree the exact source package universe and justified exceptions, then require:

1. Reproducible Base/Product inputs and an actual compiler/options/LTO ledger for each in-scope package.
2. Successful package and image builds, provenance-verified boot, ABI/SDK/vendor compatibility and required product tests.
3. Same-board, same-workload performance and PSS/private-memory measurements with repeated runs, plus long-term stability.
4. One-change module experiments followed by combined-image regression. Compiler, Thumb, LTO and MLGO effects must be separated.
5. Approved adoption/hold/rollback decision per candidate, with a recoverable control image and exception register.

[Verified: user direction retained in current checkpoint] All accepted optimizations must run on **KantSU2E** and produce measurements. Static savings and host/emulated tests cannot substitute for target acceptance. Global changes interact across modules; system changes cannot simply be assigned to one module.

Quantified performance/memory/size targets, required endurance duration and final completion date: **unknown/not recovered**. A historical next-week sequence covers Nov 16–20, but is a plan rather than an unconditional delivery promise. The user asked for a dual-path PIC proposal by Friday; Nov 20 is the calendar interpretation for this week, pending confirmation of HQ expectations.

Relation to `llvm-optimize` or `autofdo_bolt_agent`: **not established by reviewed evidence**. No shared branch, code or results are claimed. Existing LLVM optimization reports belong to this handover; similarly named external projects must be reconciled before reuse.
