# Goal, scope and acceptance

[Verified: user-relayed request](../comms/claude_to_codex/0001_handover_request.md): migrate Tizen toolchain use from GCC to LLVM, then optimize performance and memory. Codex executes, develops and analyzes; Claude coordinates and reviews; the user retains final authority. Disagreements remain explicit.

[Verified: retained master plan](../artifacts/progress_tracker.csv): primary product is Tizen TV 10.0, ARMv7 `armv7l`, on KantSU2E. Tizen 10.1 adaptation proceeds **in parallel**, not after 10.0 completion. The 10.1 Base with 10.0 Product combination requires separate acceptance. It is not an approved interchangeable Base today.

[Verified: retained Base/SDK report](../artifacts/historical-reports/base-changes-part-01.md): intentional GCC toolchain components, vendor prebuilts, SDK/cross tools and other-language builds are distinct from source packages accidentally bypassing Clang. GCC-built code is not automatically an ABI defect. Kernel/TEE/driver builds use separate compiler mechanisms. Rust uses its own LLVM-based compiler and Go its own toolchain.

[Verified: D-016 user direction] The allowed categories are RPMs that require GNU GCC for a documented technical reason and RPMs whose content is outside our Clang/GCC compilation, such as Rust, Go, scripts, data or vendor prebuilts. Record the evidence per package. Track vendor prebuilts separately for memory studies. Assess kernel, modules, bootloader, TEE and drivers individually as in-scope candidates where shipped as RPMs. The MLGO kernel experiment can provide feasibility evidence. [Decision register](../decisions/DECISIONS.md)

| Architecture | Role | Evidence/status |
|---|---|---|
| armv7l | Primary TV product and package validation | [Verified] target capture and ARM package probes |
| x86_64 | Build acceleration, host toolchain/runtime models and OBS build | [Verified] production host/target matching remains a 10.1 gate |
| aarch64 | Model/runtime assets and cross components | [Verified] assets prepared; complete device acceptance unknown |
| riscv64 | Historical cross-toolchain configuration | [Verified] historical report; no active product acceptance evidence |

## Adaptation and optimization acceptance

D-012 proposes coverage across eligible installed source C/C++ packages after D-016 exceptions, backed by compiler provenance for shipped code. Keep build and runtime acceptance as separate gates. Adaptation requires a reproducible image, validated package outcomes and boot, compatibility, product suites and stability results.

[Verified: D-017 user direction] Improve performance and memory continuously. Cold boot, app launch, settled idle memory, media playback and smooth 4K playback on KantSU2E under a physical 1 GB budget are the standard scenarios. The 4K condition is a stress benchmark. Accept a candidate after measuring improvement in at least one scenario and meeting agreed regression margins across the others. Test each optimization on KantSU2E and verify combined changes after single-variable evaluations. D-013 proposes the repeat counts and comparison rules.

Relation to `llvm-optimize` or `autofdo_bolt_agent`: **not established by reviewed evidence**. No shared branch, code or results are claimed. Existing LLVM optimization reports belong to this handover; similarly named external projects must be reconciled before reuse.
