# 0012o · Official O1 PC visit

KantSU2E ran Official QB 37736448, Product `20261123.2`, on boot `45fac48b-bc2b-4ba9-9b98-a75d0b5f3bf0`. SDB connected to `192.168.108.25:26101`. The tools archive was pulled from the TV’s exFAT mount `/opt/media/USBDriveA1` and verified on the PC. The USB stick is safe to eject. [USB transfer receipt](../../artifacts/evidence/board/o1-37736448/0012o/usb-pull.json)

| Boot-route field | Measured evidence |
|---|---|
| Active slot | `partition_ab=a` on the live kernel command line. |
| Running GNU build ID | `419813f26f2d03bee00bde1d7173b0c2fd887530` matches the Official kernel. |
| Kernel partitions | `/dev/mmcblk0p5` and `/dev/mmcblk0p6` both have GPT name `uImage`, the legacy uImage header and the same 11,348,968-byte prefix as the Official uImage (SHA-256 `eb458b69e99ce1976f8fc8013fa797c9f4734b8b8643854167d04a859f60a6d6`). |
| zImage comparison | The first 5,326,504 bytes on each partition hash to `54929820e8eeb4c1004c5500e28bea4cceb4f8c1a1c50536ebe1f3a1c5950f7d`. Official zImage hashes to `f8530555d4a0e30141e9c11c6c85655a0efe19866f0307c98bd9ceef5d24fcab`. |
| Bootloader interpretation | uImage is verified on both kernel partitions and is the supported boot-container inference for slot A. The identical contents and unavailable bootloader environment leave the physical device read on this boot unconfirmed. |
| Early `Memory: … kernel code` | 8,363 KiB kernel code. Cold-boot capture at uptime 0.046730 s has the same boot ID as this visit. The live ring had already rolled over. |

`[    0.046730] Memory: 1279556K/1631488K available (8363K kernel code, 666K rwdata, 1640K rodata, 404K init, 4024K bss, 29920K reserved, 311296K cma-reserved, 726272K highmem)` [Cold-boot dmesg](../../artifacts/evidence/board/o1-37736448/cold/early-memory-log.txt) · [Matching boot ID](../../artifacts/evidence/board/o1-37736448/cold/confirmed-boot.txt)

The boot capture used `r0012n/boot-proof.py.txt` at `88c6d9e` with PC-side staging and the verified Official image copies. After the SDK user could not read the partition devices, protected reads were taken under temporary SDB root. The SDK uid was restored to 5001. [Partition hashes and kernel log](../../artifacts/evidence/board/o1-37736448/0012o/boot-readback.txt) · [Boot receipt](../../artifacts/evidence/board/o1-37736448/0012o/boot-protected.json)

The 312,298-byte kit SHA-256 is `ee1e42701592082d2a02e44be35df2e34155940ce0a45c08706eb32f28063e33`. Its A32 static benchmark hashes to `372945183c355de1919f97b039c1f898fea0818c32025cae16cd8eb864b9b5fd`. The input manifest and Official Base 20261113.1 build receipt were verified. [Board tools provenance](../../artifacts/evidence/board/o1-37736448/0012o/board-tools.json)

## O1 timed trials

Home (`TA_native-home`, PID 486) retained focus at all 16 checks, 20 seconds apart, over 302.68 seconds of board uptime. The USB mount stayed present during this interval. The verified PC kit is retained independently of USB. [Focus](../../artifacts/evidence/board/o1-37736448/0012o/focus.txt) · [Idle window](../../artifacts/evidence/board/o1-37736448/0012o/idle.tsv)

| Attempt as SDK uid 5001 | Board result |
|---|---|
| Pinned PC launcher `c56e4ab`, CPU 0, Official | SDB pushed 559,212 bytes. SMACK denied the shell’s `chmod` metadata read on the object labeled `System`. The launcher stopped before running a trial. |
| SDK-owned file in the same private scratch directory | An ordinary shell read the archive member into the authorized path. The resulting file had mode 0700 and the expected SHA-256. Its `--clk-tck` execution check returned 126. The kernel recorded `[Verification fail] file /tmp/pm0012m/microbench is not signed. Sign it.` |
| Trials 1–5, median, spread | 0 of 5 executed. All four timing metrics are unavailable. |
| Exit state | Scratch directory absent, SDK uid 5001, original boot ID and Home focus verified. The TV remains on Official. |

The second attempt established a separate signature requirement after the checksum succeeded. A platform-approved signed benchmark common to both lanes is needed to retry with the PERF image’s execution policy. Pin its delivered hash and verify it on O1 and C1. The C1 flash awaits PM review. [Pinned run output](../../artifacts/evidence/board/o1-37736448/0012o/launcher-output.txt) · [Target hash and execution result](../../artifacts/evidence/board/o1-37736448/0012o/sdk-stage.txt) · [Kernel denial and final state](../../artifacts/evidence/board/o1-37736448/0012o/post-sdk.txt) · [Evidence checksums](../../artifacts/evidence/board/o1-37736448/0012o/SHA256SUMS)

**Native results accepted by PM.** The verbatim archive SHA-256 is `b4d21db681ace51224ff2229bff7471393f9fa299e16527fb094eca6f5a8e157`. The two root configs are byte-identical. libpisa-ipc’s compile flags come from spec lines 95–96. Cleanup pruned 19 GBS roots whose recorded sizes total 61,202,427,904 bytes. AVControl baseline smoke `pm0012-smoke.neJb0i` passed with rc=0. Received and executed cmTC argv match for both compile and link. The ARM baseline ELF SHA-256 is `97e5d0b429bc6160b98d7de9317bbadafddfece6f7460019ad0fc3af000f9a32`. Accepted order is Thumb pilot, image scan, then kernel matrix. [Native terminal evidence](../../artifacts/evidence/native-run-r0012m-inventory-cleanup-smoke-20261125.txt) · [PM review](../claude_to_codex/0012o_codex_pc_board_o1.md)
