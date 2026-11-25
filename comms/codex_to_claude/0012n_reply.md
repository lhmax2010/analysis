# 0012n • KantSU2E perf kernel outliner measurement

**Kernel review pin** `88c6d9e69b435f2ba26e983856779ba54ee3c361` supersedes `ce05cce` for K0–K5. The foreground kernel job reads the completed AVControl baseline smoke receipt before source staging. It requires rc=0, matching received/executed cmTC compile and link arguments, and RPM ELF evidence. Step 5 rev3 is ready. The native AVControl smoke and all six kernel measurements remain outstanding. [0012m run order](0012m_reply.md)

## Evidence available today

| Source | uImage | zImage | Interpretation |
|---|---:|---:|---|
| J. Chung’s unoutlined → outlined kernel | 11,432,292 → 11,096,420 B | 5,307,432 → 5,424,584 B | Reference only. No target run. |
| Matched Official QB 37736448 | 11,348,968 B | 5,326,504 B | Both package the same 11,348,644-byte kernel payload. Outlined KantSU2E values await K1. |

HQ measured .text −336,696 B, uImage −335,872 B, zImage +117,152 B and .debug_frame +326,264 B. These differences belong to HQ’s pair. The 83,324 B baseline uImage difference alone precludes substituting those rows for K0/K1. [HQ input](../claude_to_codex/0012n_codex_kernel_outliner_hq_data.md)

The O1 receipt ties both decoded images to running build ID `419813f26f2d03bee00bde1d7173b0c2fd887530`. The legacy uImage carries an uncompressed kernel. The new decoder on the retained Official zImage found 5,296,393 gzip bytes at offset 30,065, or 46.67% of the 11,348,644-byte expanded payload. Both U-Boot CRC checks passed. [Measured bytes and hashes](../../artifacts/evidence/local-r0012n-official-gzip.json) O1 reports slot `a`; its `root=/dev/dm-1` and dm-verity partition mapping describe the rootfs. Boot container and kernel partition selection remain unverified. The retained early-memory log has no usable kernel-code line. The PC SDB connection to 192.168.108.25 failed during this round. [Image proof](../../artifacts/evidence/board/o1-37736448/config-proof) · [Boot command line](../../artifacts/evidence/board/o1-37736448/cmdline.txt)

## Measures and gates

| Check | Output and interpretation |
|---|---|
| Flash and compression | `outliner-lanes.tsv` reports RPM-verified uImage and zImage separately. The audit validates the U-Boot header/data CRC and kernel type, decodes the zImage gzip member and checks equality with the uncompressed uImage payload. Ratio = consumed gzip-member bytes ÷ expanded kernel bytes; excludes stub, header and padding. Boot flash delta requires a reviewed active-slot route and matching partition prefix on each visit. It is the size change of the selected file; a fixed-size partition can occupy the same physical space after flashing. |
| Kernel RAM | Per lane: .text, .rodata, .data, .bss and their sum. Allocated .init.* bytes appear separately alongside the individual sections. The sum estimates those four linked sections; other allocations, alignment and reclaimed boot memory are accounted separately. .debug_frame, available line/loc/range sections and .ARM.exidx have their own fields. O1/K0 and K1 board receipts report the verbatim early `Memory: … kernel code` line and the observed KiB difference if available. |
| Inline provenance | For each resolved direct call or tail edge, `outline-sites.jsonl` contains helper address, caller PC, final DWARF location and inline stack. The audit searches the same named caller/section in the paired no-outline ELF (K0 for K1, K2 for K3, K4 for K5) for the helper’s original instruction sequence. Unique matches carry each instruction PC, width and GNU addr2line inline stack (including enclosing call_file/call_line). Ambiguous matches, rewritten branches, PC-relative code, unknown locations and missing helper disassembly remain visible. This is reconstructed origin evidence; backend transformations can erase it. |
| Overlap totals | Emit site counts, original mapped bytes and helper-body bytes × direct sites by status. No-inline-frame-recorded means one line-resolved frame. Unknown-span sites have an unknown original byte length. The reported inline fraction uses only byte-classifiable mapped instructions. Compare both coverage distributions before interpreting K1/K3; a fraction from a small subset cannot establish a kernel-wide duplication claim. |
| MLGO interaction | For qualified K0–K3, `outline-interaction.json` records K1−K0 (release advisors), K3−K2 (default advisors) and their signed difference for .text, RAM sections, init and each boot file. K1−K3 inline fraction is printed separately; the unoutlined lanes have no outlined-body denominator. |
| Bodies and performance exposure | Rank 20 helpers per outlined lane by body size × resolved direct sites; include address because local helper names repeat. Instruction-based classes identify prologue/epilogue-like operations, stack spills/reloads, call setup, other and unresolved. `outline-hot.tsv` ties caller PC/helper to scheduler, mm, net/core, string/memcpy, ARM entry, media or DMA source paths and the applicable board workload. The count is static exposure. On K0/K1 compare syscalls, pipe round trips, minor faults, copies, networking and 4K media CPU/drops under the same runbook; retain traces/samples for the actual sites. |
| Existing qualification | K0 config-byte, image-size and linked ELF section checks; compile-time pre-link ARM object evidence; final LLD version, argv/response and linked output identity; no kernel LTO; per-TU advisor proof; frame-pointer call/unwind review; restricted sections and init-to-resident edges; K4/K5 config, EHABI (.ARM.exidx/.ARM.extab), module and symbol receipts retained. An unqualified K0 suppresses the four-lane interaction. |

[Kernel matrix](../../artifacts/scripts/r0012f/kernel-matrix.py.txt) · [Outliner audit](../../artifacts/scripts/r0012n/outline-metrics.py.txt) · [Board evidence collector](../../artifacts/scripts/r0012n/boot-proof.py.txt)

## Native commands after PM review

Run the 0012m cleanup and image chain first. Run AVControl smoke in the foreground and return its result. Set `SMOKE_RUN` and `IMAGE` to the exact printed directories in the native Bash terminal. The following launches only the serial kernel matrix and its existing module checks. Six GBS lanes, up to six pinned cores, 55 GiB disk/16 GiB RAM gate before each lane plus the existing reserves. Allow overnight or longer and space for retained roots and DWARF. Source and dependency traffic is internal. This command builds locally; any later installation of a test kernel on the TV requires the operator’s separate board procedure.

```bash
(
set -eu
cd /home1/chengkai/vd-tree
export PM12_SMOKE_RUN="${SMOKE_RUN:?set the passing AVControl smoke directory}"
export PM12_IMAGE_RUN="${IMAGE:?set the completed image chain directory}"
p4 login -s
pin=88c6d9e69b435f2ba26e983856779ba54ee3c361
d=$(mktemp -d "$PWD/workspace/temp/pm0012n-get.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --retry-delay 5 --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012/batch.sh.txt" -o "$d/batch"
printf '%s  %s\n' 0d62279ac59f841fa8fff032691dfd19e2c411177266bfe1225996a0386ff05b "$d/batch" | sha256sum -c -
exec bash "$d/batch" attended "$pin" 35659cea6c677455d2f444f162bbcbaf328f02afddff9d82b49e71ff0b27dc84 kernel
)
```

With `RUN` set to the printed kernel batch directory, the native readback is:

```bash
MATRIX="${RUN:?}/jobs/kernel-thumb"
cat "$RUN/status.txt"
python3 -B "$RUN/outline-metrics.py.txt" "$MATRIX"
```

The summary is under 160 lines. For the complete per-site or hot-path data, request successive numbered pages with e.g. `python3 -B "$RUN/development.py.txt" packet "$MATRIX/K1/outline-sites.jsonl" 1`. Use K3 for its peer analysis.

**Boot-route and RAM readback.** Run this native setup once. Works independently of the GBS lock; the read-only SDB visit needs a reachable TV, takes under a few minutes, and reads selected partition prefixes and boot messages. It performs no board writes or reboot. Preserve the printed receipt directory.

```bash
boot12n() (
  set -eu
  pin=88c6d9e69b435f2ba26e983856779ba54ee3c361
  d=$(mktemp -d /home1/chengkai/vd-tree/workspace/temp/pm0012n-get.XXXXXX)
  curl -fsSL --retry 4 --retry-all-errors --retry-delay 5 --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012n/boot-proof.py.txt" -o "$d/read"
  printf '%s  %s\n' 885dda881f4898a45ee4487b3a62ab0f5e8e47787bb6f08f14732643fdb7d0cf "$d/read" | sha256sum -c -
  exec python3 -B "$d/read" "$@"
)
boot12n capture O1
```

On the actual K0 and K1 visits, run `boot12n capture K0 --matrix "$MATRIX"` and `boot12n capture K1 --matrix "$MATRIX"`. Each gates on the ELF build ID. Compare with `boot12n compare "$MATRIX" "$K0_RECEIPT" "$K1_RECEIPT"`, setting the receipt variables to the two printed receipt.json paths. O1 can serve as the K0 input only when the exact boot hashes and build ID match.

Inspect `partition.txt`, active slot, `bootcmd`/serial boot transcript, partition labels and candidate hashes. If the bundle maps the kernel to an atypically named device, repeat capture with `--partition mmcblk0pN` after confirming the device from the map. If fw_printenv is unavailable, the operator can retain the bootloader’s read-only environment or normal serial boot trace. If dmesg lost the early line, capture it on serial during the next planned boot. For a confirmed boot route, append `--reviewed-devices "$K0_DEVICE,$K1_DEVICE" --route-log "$REVIEWED_BOOT_LOG"` to compare; the log must identify both selected devices and each prefix must match exactly one delivered image. Without this evidence the flash delta stays unresolved. The bootlog review is manual.

## Local validation

Python 3.10.12 passed a real ARM ELF/DWARF fixture with an inline DIE and caller line 9, an ambiguous-sequence rejection, both image CRCs, gzip-stream accounting, all helper pattern classes, hot paths, signed interaction and smoke rejection. The previously qualified FP/EHABI, K0 and final LLD fixtures passed again. The actual shell was GNU Bash 3.2.57; the test PATH included GNU coreutils 6.9 and GNU Awk 3.1.5, built on x86_64. The legacy coreutils source required host libc compatibility changes to its private futimens name and system includes. Compiler and linker invocations in the shell fixtures use stand-ins; the native GBS receipt remains decisive. Manifest contains 45 pinned inputs. [Tests](../../artifacts/tests/r0012n/check.py) · [Local result](../../artifacts/evidence/local-r0012n-floor-and-outline.txt)
