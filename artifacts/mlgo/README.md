# MLGO Base comparison tools

- [Native Base preflight](preflight-base-qb.py.txt) collects the two published Base inventories for armv7l and x86_64 and diffs all NEVRAs, including checksum changes. It logs published configuration evidence, verifies OBS revision and matches the clang RPM binary bytes where available. Other LLVM RPMs carry metadata SHA-256 and source RPM in the CSV. Base inputs and shelves are digest checked before staging.
- [Target compiler probe](probe-effective-advisors.sh.txt) runs ambient, explicit release and heuristic modes through the same package compiler entry point with fixed translation-unit and flags. Record the compiler identity, invocation, diagnostics and actual optimization remarks or counters. Use a larger representative TU set when this lightweight sample has no discriminating output.
- [Reply 0003](../../comms/codex_to_claude/0003_reply.md) contains the review and copy-paste commands.

Staged inputs can be reviewed independently of build readiness. A generated configuration has an isolated GBS buildroot. The QuickBuild job itself must keep the saved Product, build.conf, shelves, job parameters and rebuild policy fixed.

The retained Official spec SHA-256 is `c3a1f3c4363683f6142678d60d6518c50c69dfc1ecd2a7fc0b4cbf3d708b9378`. It matches the source pin associated with the pre-Customized VD configuration. It enables MLGO packaging and wires both bundled model objects. Effective use by the installed release image still requires build evidence. The exact source carried by each subsequently published binary is checked separately.
