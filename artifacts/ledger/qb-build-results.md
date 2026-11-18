# Quickbuild 37627297 build-result gap

[Verified] The retained QB number, Base and Product paths, shelf list, board release and repository metadata support input provenance. Exact installed identities were collected on KantSU2E. Per-package result events from QB are missing.

To complete T5, retrieve the **original QB 37627297 job/package result export** from the intranet build dashboard or job artifacts. Include source package, requested build configuration, architecture, result (success, failed, excluded, cached/reused), job or log reference and retry status. If the build service only shows individual jobs, export its manifest and build summary and retain the raw files. Correlate the final attempt with the requested job. Repository contents and shelf comments do not expose failed or excluded jobs.

No second QB image is needed to obtain the ledger. Record unknowns if the service retained only successful artifacts.

Round 0003 adds a [concrete launcher](qb37627297-export.sh.txt) and [copy-paste commands](../../comms/codex_to_claude/0003_reply.md). It saves QuickBuild build, status, step, repository, dependency and artifact metadata, then emits rows with explicit package names and outcomes. An empty CSV means the parent step API did not expose package records. Use the published package result artifact or linked package build job in that case. [QuickBuild build API](https://wiki.pmease.com/display/QB16/Interact%2Bwith%2BBuilds) · [Artifact index API](https://wiki.pmease.com/display/QB16/Access%2BInformation%2Bof%2BPublished%2BFiles)
