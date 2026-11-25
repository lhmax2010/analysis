| VDLinux PERF (bytes) | GCC 37564293 | Official MLGO 37736448 | Custom MLGO 37736427 | Official − GCC | Custom − GCC | Custom − Official |
|---|---:|---:|---:|---:|---:|---:|
| Text | 9,364,188 | 8,564,632 | 8,315,864 | −799,556 | −1,048,324 | −248,768 |
| Data¹ | 683,008 | 681,984 | 680,960 | −1,024 | −2,048 | −1,024 |
| BSS¹ | 4,117,504 | 4,120,576 | 4,121,600 | +3,072 | +4,096 | +1,024 |
| Total | 12,218,544 | 11,348,904 | 11,085,176 | −869,640 | −1,133,368 | −263,728 |
| uImage | 12,218,608 | 11,348,968 | 11,085,240 | −869,640 | −1,133,368 | −263,728 |
| zImage | 5,664,248 | 5,326,504 | 5,222,032 | −337,744 | −442,216 | −104,472 |
| rodata | 1,740,800 | 1,679,360 | 1,675,264 | −61,440 | −65,536 | −4,096 |
| init¹ | 421,888 | 413,696 | 405,504 | −8,192 | −16,384 | −8,192 |
| tztv-kernel-perf RPM | 20,018,029 | 19,345,448 | 19,160,700 | −672,581 | −857,329 | −184,748 |

¹ **GCC Data/BSS/init: derived from the kernel image (mem_init formula), method validated on Official and Custom.** G1’s first successful SDB read came at uptime 266.88 s after the authorized warm reboot. Its ring buffer had already advanced to 4.334774 s. The operator confirmed there is no UART capture. The full early `Memory:` line could not be recovered from the ring, journal or vendor log reads. The exact GCC kernel that ran gives 667 KiB rwdata, 4,021 KiB BSS and 412 KiB init at its boot-print call site. O1 and C1 values come directly from their boot logs. G1 available/reserved memory and the timestamp of the original line remain unobserved. [G1 first read](../../artifacts/evidence/board/g1-37564293/first-connection.txt) · [G1 log retention](../../artifacts/evidence/board/g1-37564293/boot-log-sources.txt) · [O1 boot log](../../artifacts/evidence/board/o1-37736448/cold/early-memory-log.txt) · [C1 boot log](../../artifacts/evidence/board/c1-37736427/warm/early-memory.txt)

**Measurement.** Text and rodata use inclusive physical resource ranges from each board visit. Data, BSS and init use whole KiB from the kernel’s boot accounting, converted to bytes. Total is the complete uImage file minus its 64-byte header and includes the 260-byte trailer on every lane. HQ’s Linux-RPI Total definition is unverified. The first four rows follow its presentation. [Raw byte table](../../artifacts/evidence/board/g1-37564293/hq-size-bytes.tsv) · [LLVM board ranges](../../artifacts/evidence/board/c1-37736427/kernel-resource-sizes.tsv)

**Comparison scope.** All three lanes share kernel source CL 14293732. The Official/Custom pair matches across all 5,880 Product source/VCS rows and differs in LLVM Base. GCC uses Product 20261113.1 and Base `tizen-10.1-base-standard_20260919.1`; Official/Custom use Products 20261123.2/20261123.1 and LLVM Bases 20261113.1/20261118.1. The GCC deltas describe shipped images. Isolating a compiler effect requires controlling the other inputs. The GCC perf config comparison against Official `2a31652557d89d100d3c1bc6b0116556e32a56f03b0145eba12af425c75379f3` is scheduled under `pm12t gcc`. [Matched-pair gate](../../artifacts/evidence/native-run-r0011-step2-pair-gate-20261124.txt) · [GCC capture](../../artifacts/evidence/native-run-r0011c-chain-AFkXQV-20261124.txt)

## Validation against the two LLVM board boots

| Lane | Image-derived rwdata / BSS / init (KiB) | Observed boot-line rwdata / BSS / init (KiB) | Result |
|---|---|---|---|
| Official 37736448 | 666 / 4,024 / 404 | 666 / 4,024 / 404 | 3/3 exact |
| Custom 37736427 | 665 / 4,025 / 396 | 665 / 4,025 / 396 | 3/3 exact |
| GCC 37564293 | 667 / 4,021 / 412 | Unavailable | Image-derived |

One collector verifies the pinned uImage SHA-256 and legacy data CRC, locates the unique ARM load of the `Memory:` format address, and extracts 1,152 bytes around it. The same offline evaluator follows the linked arithmetic, overlap adjustments and KiB shifts up to the print call. Loads of live counters and function returns remain unknown. All five fixed arguments, including the two extra checks (code and rodata), reproduced the archived boot line independently on each LLVM lane. [Three-lane validation receipt](../../artifacts/evidence/board/g1-37564293/method-validation.json) · [Image collector](../../artifacts/scripts/r0012u/memory-site.py.txt) · [Constant evaluator](../../artifacts/scripts/r0012u/verify-print-fields.py.txt)

## G1 identity and boot route

On both sides of the reboot, `/etc/prd_info.ini` reported `TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261113.1`, type `perf`. The running kernel’s GNU build ID `137d01259d95739d5eb71e468bf289ee467a65b0` matches the note in the verified USB kernel. O1’s ID is `419813f26f2d03bee00bde1d7173b0c2fd887530` and C1’s is `4d95bb9eb9dc71983a87f90352fc8c2b7bd8a006`. The uncompressed zImage member equals the uImage’s declared payload byte for byte. [Board identity](../../artifacts/evidence/board/g1-37564293/identity-after.txt) · [USB header verification](../../artifacts/evidence/board/g1-37564293/legacy-header.json)

```text
Linux version 6.12.60 (abuild@A1502LMG) (gcc (Tizen GCC 14.2.0 20240801 1.3) 14.2.0, GNU ld (GNU Binutils) 2.43) #1 SMP PREEMPT Thu Nov 12 14:24:11 UTC 2026
```

The retained GCC `tztv-kernel-perf-1-1.armv7l.rpm` passed SHA-256 `e78789c2d95eb9a0e629646fad73e01d02a088ae470cce9e297ee8642b7399e5` on the native server. Its uImage/zImage sizes and digests match both the USB bytes and the installed RPM inventory. The SHA-256 of the board’s 3,630,143-byte raw BTF file `/lib/modules/6.12.60/kernel/vmlinux` matches the retained RPM member, `1a5ee77d0f3760df26546522966b0083a703343f1609b5d0decc473980ab979f`. [Native RPM readback](../../artifacts/evidence/board/g1-37564293/native-rpm-check.txt) · [Installed members and BTF](../../artifacts/evidence/board/g1-37564293/rpm-btf.txt)

`partition_ab=a`. The first 12,218,608 bytes of **both** `mmcblk0p5` and `mmcblk0p6` match the complete USB uImage by SHA-256. Both carry the GPT label `uImage`; their identical prefixes cannot distinguish them by content. The boot ID changed from `0c85ef71-b7d0-4634-a534-472a269b3956` to `156dc475-c1a0-4a45-a2f9-b377c22d0379`. The observed foreground process was `TA_native-home`, PID 444. SDB returned to uid 5001. USB reads are complete and the operator can safely eject the stick. [Route](../../artifacts/evidence/board/g1-37564293/route.txt) · [Home](../../artifacts/evidence/board/g1-37564293/focus.txt) · [Final SDB state](../../artifacts/evidence/board/g1-37564293/final-uid.txt)

## USB bundle

The TV mounted `/dev/sda1` at `/opt/media/USBDriveA1`. Inspection was read-only. The bundle is `updateSU2E/`. Its uImage header declares an uncompressed ARM Linux kernel, ih_size **12,218,284 B**. Both CRC32 checks passed: header `5201d896`, declared data `463c5f3e`. [All 26 directory entries and sizes](../../artifacts/evidence/board/g1-37564293/usb-inventory-and-hashes.txt) · [Mount and USB Product file](../../artifacts/evidence/board/g1-37564293/usb-mount.txt)

| File | Bytes | SHA-256 |
|---|---:|---|
| uImage | 12,218,608 | `f9bb12a1fa900c2dca61f15b86241f85724dd1a2caf4fbeeb9699cd061a9fe0e` |
| zImage | 5,664,248 | `161721c1f37e44f4a114849fba0dac95d73766a432a575365b602c8735e1f132` |
| dtb.bin | 1,564,672 | `1c7b8691089f690eab62a59773a21e38ba13ab3365304175019e2dea2191cdd6` |
| data.img | 1,118,674,944 | `f2a47268226802d80f716749a01a32983e50dcf53729374a705041cd5513c7a4` |

## Cross-check of G1 memory accounting

Root’s `/proc/iomem` returned code `040082c0–048f659b`, rodata `048f7000–04a9ffff` and data `04b08000–04f9c777`. The data resource spans both initialized writable data and BSS. [Board ranges](../../artifacts/evidence/board/g1-37564293/early-memory.txt)

In the verified USB payload the format string begins at offset `0x9aa140` including its two-byte log-level prefix. The ARM call site at `0xc0ab5da0` uses that string at `0xc09b2140`. The constant address pairs below are the actual linked operands feeding the size arguments. The compiler evaluates each field in KiB by shifting right ten bits. The init text lies within the init region and the printer accounts for it once. The printed code (9,144 KiB) and rodata (1,700 KiB) agree with the live resources after truncation; the raw writable data plus raw BSS cover the live data resource exactly. [Verified instruction words](../../artifacts/evidence/board/g1-37564293/memory-print-call.dis) · [Linked bounds and byte values](../../artifacts/evidence/board/g1-37564293/memory-print-bounds.tsv)

| GCC field | Linked range (exclusive end) | Bytes before rounding | Boot-format KiB |
|---|---|---:|---:|
| code | `c00082c0–c08f659c` | 9,364,188 | 9,144 |
| rwdata | `c0b08000–c0baefac` | 683,948 | 667 |
| rodata | `c08f7000–c0aa0000` | 1,740,800 | 1,700 |
| init | `c0aa1000–c0b08000` | 421,888 | 412 |
| bss | `c0baefac–c0f9c778` | 4,118,476 | 4,021 |
