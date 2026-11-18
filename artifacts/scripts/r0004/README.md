# Round 0004 native scripts

The revision-pinned launchers and their SHA-256 checks are in [reply 0004](../../../comms/codex_to_claude/0004_reply.md). Review the script commit before forwarding a launcher to the operator. The two image-mode inputs are byte-identical copies of the PM's files.

The preflight reads the published Base and Product snapshots and OBS binary evidence. QB export uses the existing native authentication path. The RPM scan uses the pinned installed-image payload plan, reads RPMs over the VD network and keeps its records under the native vd-tree. The other scripts inspect retained artifacts or run isolated compiler probes.
