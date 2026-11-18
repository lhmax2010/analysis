# Artifact locations and provenance

- [All repository artifacts](../artifacts/README.md), including every split-file directory index.
- [Original source manifest](../artifacts/source-manifest.csv): exact local path, byte count and SHA256, with transformation/scope notes.
- [Progress tracker](../artifacts/progress_tracker.csv): current master milestones and evidence.
- [Complete historical action tracker](../artifacts/historical-tracker/README.md): all986 rows, all original columns.
- [Current build-status label universe](05_build_status.md): all942 distinct historical labels across three CSV parts; current results explicitly unknown.
- [Scoped build results](../artifacts/scoped-build-results.csv), [aggregate measurements](../artifacts/measurements.csv), [shelf cases](../artifacts/shelf-cases.csv), [PIC first batch](../artifacts/pic-next-phase.csv).
- [Patch index](../artifacts/patch-index.csv), [script index](../artifacts/script-index.csv) and readable selected snapshots.
- [Server artifact metadata](../artifacts/server-artifacts.csv): known path/size/hash; missing values explicit. Directory hashes are not invented. Packet digests are not silently treated as original report-file hashes.

Local repo: `/home/toolchain/Desktop/temp/analysis`. Preparation/check outputs: `/home/toolchain/Desktop/temp/analysis-work`. Original prompt backup: `/home/toolchain/Desktop/temp/input-backups/20261117/claude-pm-handover-0001/request-original.txt`.

Other raw evidence remains under `/home/toolchain/Desktop/temp/tizen-llvm-handover`, with maintained memory in `/home/toolchain/Desktop/temp/claude_mem`. Historical paths inside evidence are preserved. Consult local `project-file-relocation.json` for relocated files; do not recreate old locations or forwarding symlinks.

Native files remain under `/home1/chengkai/vd-tree`, including retained builds, models, RPMs, logs and debug details. No native directory is copied wholesale into this repository. The three SR runtime archives alone are approximately22MB each and are represented by exact pin hashes, not committed binaries.

The debug CU paste was structurally reconciled by package/file/BuildID and producer counts, but tabs/trailing whitespace changed. See [validation](../artifacts/evidence/thumb-paste-validation.txt). Exact original hashes reported by the native collector are provenance claims, not byte-verified local TSV hashes.

Split `.txt` source/patch snapshots can be concatenated in numeric order; directory indexes explain scope. CSV chunks repeat headers and are combined by parsed rows. Historical Markdown fragments are for web review, not executable files.

Round 0002 adds the [board inventory](../artifacts/board-inventory.md), [installed ledger](../artifacts/ledger/README.md), [PIC audit](../artifacts/pic-audit/README.md), [memory attribution](../artifacts/memory-attribution/README.md), [Thumb reproduction](../artifacts/thumb-repro/README.md) and [HQ drafts](../hq/README.md).
