# Round 0011d reply — live Doc 02 export and active chain

[Doc 02 rev4](../../reports/weekly/2026-11-20/02_MLGO_Kernel_Comparison_rev4.md) is the verbatim live export. Its SHA-256 matches `76563a70834a5a1632909678e0b24c387efb2a4e66579a398b778cd465e8f6e0`. The reports index marks the retained repo-authored rev3 as superseded. Future proposed HQ wording goes in these replies for Claude to apply to the live doc. [Reports index](../../reports/README.md) [Rev4 checksum](../../reports/weekly/2026-11-20/SHA256SUMS.rev4)

The active chain is `/home1/chengkai/vd-tree/workspace/temp/pm0011c-chain.AFkXQV`. At 16:00 CST, the operator reported the GCC reference download at 308 MB and growing. The earlier `pm0011c-chain.xhVzT6` stopped during the raw GitHub download of `perf-bundle.py.txt` with curl exit 28. Rev2 changes the download retry behavior and the header comment. Its job commands and pins match the original. The archived rev2 SHA-256 is `1a90387959e0cad9ec9002c622e7590ccfd2f3ef4a1ef3749031a542ec19f3cf`. [Archived rev2 script](../../artifacts/evidence/native-cmd-r0011c-gcc-ref-usb-baseproof-rev2.sh)

Use the [bounded chain readback](0011c_reply.md#return-the-existing-chain-results), which defaults to `AFkXQV`. The archived scripts retain their original status comments. The active launcher commands use the explicit run path and five download attempts, with 15 seconds to connect, 120 seconds per transfer and 10 seconds between failures. Every download still has to match its SHA-256 pin.

After the chain returns, verify the GCC receipt, both USB staging manifests and the Base proof. Run board Step 5, then the [overnight HQ batch](0011c_reply.md#overnight-hq-command-after-the-chain-and-board-slot), then Steps 9 and 8 after the batch exits.
