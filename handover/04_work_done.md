# Completed work and retained implementation

| Milestone | Evidence and completion boundary |
|---|---|
| Historical Base/toolchain integration, Aug–Oct | [Verified] [Base changes](../artifacts/historical-reports/base-changes-part-01.md): original project inventory 447 packages; 12 changed packages/16 commits since Sep 1 in that report, plus separately documented creation/comment commits. Historical count, not current totals. |
| Historical SDK migration | [Verified] [SDK report](../artifacts/historical-reports/sdk-changes-part-01.md): toolchain selection and output comparisons. Current remaining SDK coverage is still tracked. |
| Compiler/options/LTO planning, Nov 12–17 | [Verified] complete 986-row historical action ledger exported with all fields; categories 101 compiler, 199 options, 146 LTO and 540 other-toolchain/SDK entries. |
| Seek correctness fix, Nov 16–17 | [Verified] [crash report](../artifacts/historical-reports/usb-thumbnail-crash.md): initialize indeterminate seek bounds; GCC/Clang ARM builds, ABI checks, host regression and scoped Clang TV checks passed. CL14466526 shelved. |
| AVControl Global Options candidate, Nov 17 | [Verified] Clang control/candidate and GCC candidate built; static size/ELF checks and retained strong-import closure passed. No target acceptance/shelf adoption. |
| 10.1 bootstrap and probes, Nov 16–17 | [Verified] 12 LLVM RPMs built with GCC bootstrap; eight scoped smoke groups and selected RPM-layout review completed. Production accelerated path open. |
| FatLTO/PIC, Nov 17 | [Verified] 56 ARM mechanism cases reviewed; 38 positive outcomes, 18 expected native relocation rejections. Full production affected count still unknown. |
| Customized MLGO, Nov 17 | [Verified] complete SR runtime correction committed as OBS rev12 after 512 standalone model probes. Build/publication still pending. |
| Thumb and ABI evidence, Nov 17 | [Verified] 930 shelf comments reconciled; target mapping scan and 28,004 debug CU rows reviewed. Seven explicit-marm ELF candidates in two RPM families; historical106 roster missing locally. |

[Patch index](../artifacts/patch-index.csv) contains **six selected retained patch files**, not a claim that the whole project has six patches. The historical Base/SDK reports include further diffs. The complete action tracker contains shelf references; one shelf may change multiple files/packages and one package may have multiple shelves. A deduplicated global patch-file count with upstream status is not established.

The selected patches cover the regular-LTO PIC fallback, default LLVMgold handoff, O4 compatibility, complete MLGO runtime integration, AVControl flags and MAPI migration. Text snapshots are supplied for review; split pieces reconstruct in numeric order. Their original hashes are indexed.

[Script index](../artifacts/script-index.csv) lists 58 top-level retained automation files in the selected workstream directories, with path, size and hash. This is a bounded index, excluding generated fixtures and caches. Filename-derived purpose is labeled. Active MLGO submission/input-verification scripts are included as readable snapshots under [scripts](../artifacts/scripts/README.md).

No new build/test workload was executed for this PM handover. Current-source compilations, target runtime tests, package installation and further OBS operations require a subsequent execution task.
