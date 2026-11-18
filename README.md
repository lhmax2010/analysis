# Tizen LLVM adaptation and optimization

1. **[Overall progress and master tracker](handover/00_overall_progress.md)**
2. **[Current status](status/STATUS.md)** and [machine-readable progress](artifacts/progress_tracker.csv)
3. [Handover documents](handover/README.md)
4. [Decisions and proposals](decisions/DECISIONS.md)
5. [Claude/Codex correspondence](comms/README.md)
6. [Evidence, complete historical tracker, scripts and patches](artifacts/README.md)

This is the initial PM handover, prepared on 2026-11-17. No builds, target mutations or OBS changes were started for this round.

**Reading convention:** `[Verified]` means supported by the referenced retained evidence, within its recorded scope and date. A historical report verifies what was recorded; it does not independently revalidate a current image. `[Assumption/Memory]` identifies a proposal, estimate or unverified recollection. Unknown means the evidence is unavailable, not that the result is zero or failed.

The historical 986-row action tracker is exported in full. It is not a current-image build success ledger. Source package labels, RPM identities, ELF paths, compilation units and test cases are distinct counting units.

All local project files stay under `/home/toolchain/Desktop/temp`; native execution stays under `/home1/chengkai/vd-tree`. Raw inputs and their hashes remain archived locally. This repository carries readable evidence and metadata, not RPMs, binaries, images, credentials or build roots. See [source provenance](artifacts/source-manifest.csv).

Claude review status: **pending** for this handover. Historical reports are preserved under `artifacts/historical-reports`; their plans and recommendations can be superseded by current status and decision records.
