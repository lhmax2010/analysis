# Open issues and risks

| ID | Severity | Evidence and risk | Next step |
|---|---|---|---|
| R01 | High | [Verified] MLGO rev12 last observed building; no successful published Base | Status-only check, then verify RPM/model identity and published snapshot |
| R02 | High | [Verified] 10.1 x86 accelerated ld versus ARM LLVMgold payload mismatch | Prepare architecture-matched host compiler/plugin/runtime path; preserve passed private-ARM evidence |
| R03 | High | [Verified] full current build/test ledger missing | Reconcile fixed build jobs and source identities; do not use shelf counts as passes |
| R04 | High | [Verified] native fat-object path outside regular-LTO fallback | Qualify actual selected inputs/consumers; repair PIC at producer where applicable; no generic binary repair assumed |
| R05 | High | [Verified] AVControl removes 782 weak exports | Target functional/dynamic-consumer regression before adoption despite static import closure |
| R06 | Medium | [Verified] historical106 Thumb roster not recovered locally | Search original Claude/source analysis; current89 set is not replacement; get actual compile-command deltas only |
| R07 | High | [Verified] optimization samples lack matched current target measurements | Freeze baseline and run independent experiments plus combined regression |
| R08 | Medium | [Verified] playback dimming recurred; IoTivity lifetime candidate undelivered | Resume separately after priority work, do not report resolved |
| R09 | Medium | [Verified] debug paste changed whitespace; 23,456 CU rows lack producer | Preserve raw input and structural reconciliation; do not claim original TSV byte hash or full compiler attribution |
| R10 | Medium | [Assumption/Memory] server resource sharing/current disk unknown | Read-only capacity review before heavy jobs; retain evidence, avoid broad cleanup |
| R11 | Medium | [Verified] multiple historical launchers/checkpoints contain superseded status | Use latest rev12 runtime status-only command; don't re-upload rev11 or overwrite concurrent source changes |
| R12 | Medium | [Verified] public GitHub is the agreed collaboration channel | Publish reviewed text/metadata only, redact credentials, retain large/private raw payloads locally; no automated raw directory upload |

Current affected-production native-PIC count is **unknown**, not zero. The 18 synthetic negative tests are not package defects. Two RPM families/seven explicit-marm ELF candidates are not confirmed performance regressions or ABI failures.

Before acceptance, bind every result to its source/flags/toolchain/build root/image/device/scenario. Historical report statuses remain dated. No silent inference from missing evidence to either success or failure.
