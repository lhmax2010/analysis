# 0012o · Official O1 PC visit

**USB status: keep it in the TV.** The PC has not pulled the archive. The final direct TCP check to `192.168.108.25:26101` timed out; `sdb devices` returned an empty list. `sdb connect` printed an error despite process exit 0. The PC selected its wired interface (192.168.107.10 via 192.168.107.1). This establishes a connection failure from this PC; the location of the fault is undetermined. [Connection receipt](../../artifacts/evidence/board/o1-37736448/0012o/pc-connection.json) · [SHA-256](../../artifacts/evidence/board/o1-37736448/0012o/SHA256SUMS)

| Boot-route field | This visit |
|---|---|
| Product / active slot | No current board read. Earlier O1 evidence identifies Official QB 37736448 and slot a. |
| Loaded image, partition, prefix digest | Unresolved. The earlier build ID matches the payload in both containers. |
| Early `Memory: … kernel code` line | No current board read. |
| USB tar and binary | Awaiting pull and local verification. Expected archive 312,298 B, SHA-256 `ee1e42701592082d2a02e44be35df2e34155940ce0a45c08706eb32f28063e33`. Expected microbench SHA-256 `372945183c355de1919f97b039c1f898fea0818c32025cae16cd8eb864b9b5fd`. |

| O1 microbenchmark | Result |
|---|---|
| Trials 1–5 | 0 of 5 acquired |
| Median / spread | Unavailable |

No board shell, root, benchmark staging, reboot or USB write occurred in this attempt. Resume at the USB mount/pull step when the specified board is reachable. Release the stick following complete PC-side validation of the archive, microbench, input manifest and board-tools provenance, then start the idle measurement after USB handling and Home readiness. [Earlier O1 identity](../../artifacts/evidence/board/o1-37736448/kernel-receipt.txt)

**Native results accepted by PM.** The verbatim archive SHA-256 is `b4d21db681ace51224ff2229bff7471393f9fa299e16527fb094eca6f5a8e157`. The two root configs are byte-identical. libpisa-ipc’s compile flags come from spec lines 95–96. Cleanup pruned 19 GBS roots whose recorded sizes total 61,202,427,904 bytes. AVControl baseline smoke `pm0012-smoke.neJb0i` passed with rc=0. Received and executed cmTC argv match for both compile and link. The ARM baseline ELF SHA-256 is `97e5d0b429bc6160b98d7de9317bbadafddfece6f7460019ad0fc3af000f9a32`. Accepted order is Thumb pilot, image scan, then kernel matrix. [Native terminal evidence](../../artifacts/evidence/native-run-r0012m-inventory-cleanup-smoke-20261125.txt) · [PM review](../claude_to_codex/0012o_codex_pc_board_o1.md)
