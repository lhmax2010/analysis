# Native compiler evidence and terminal transport

- [Compile evidence collector](collect-compile-evidence.py.txt) reads selected logs, compile databases, kbuild command sidecars, source files, debuginfo and shipped/vendor ELF paths. Output is a compressed terminal packet.
- [Rust mode probe](rust-thumb-probe.sh.txt) compares the existing target, its Thumb-mode feature and the alternate hard-float target using the same Tizen rustc.
- [Terminal packet launcher](print-terminal-packet.py.txt) emits one numbered part with up to 160 base64 lines. It takes named text results and preserves their bytes and hashes.
- [Round 0004 commands](../../comms/codex_to_claude/0004_reply.md) give the order and evidence rules.

Treat the reported expected QB ID as a label until the build manifest and log establish provenance. Match the shipped ELF or member to that build by path and Build ID or SHA-256. Keep source rules, effective compiler arguments, DWARF producers and byte-identical source assets as distinct fields. A missing rule or a stripped binary leaves causation unresolved.
