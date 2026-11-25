# 0012r • C1 Memory line (warm reboot), image partition fix, LTO delivery rule, kernel ELF sizes, replay cause, disk

Work in this order. §1 is urgent (it needs the board); §2–§6 need no board. Re-pin everything that changes and send it to me for review. Tonight's image re-run and kernel batch wait for that review.

## §1 (now, board): C1 `Memory:` line via one software reboot

You may reboot the TV yourself this once: `reboot` over SDB. It stays on Custom 37736427; no flash.

1. Wait until SDB reconnects, and record the new boot ID and the uptime at first connection.
2. **Immediately** read the full `Memory:` boot line from `dmesg`, before the ring buffer rolls over. Complete Table A: Data (rwdata), BSS and init for C1, next to the O1 cold-boot values. State the measurement method in each row. Keep the `/proc/iomem` Text rows you already have (Official 8,564,632, Custom 8,315,864, −248,768 B, −2.90%).
3. Wait until Home is ready (record how you detected it). Then take 3 `MemAvailable` samples 60 s apart, starting about 6 minutes after boot. Label this boot **warm (software reboot)**; O1 was a cold boot. Do not mix the earlier C1 samples (taken at about 117 min) into any comparison.
4. Without the board: classify the **178 package differences** between the O1 and C1 rosters as same version with a different release (rebuild) or a real version change. Name every toolchain or runtime-library package among them (glibc, libstdc++, compiler-rt, zlib, xz/liblzma, gzip, openssl, etc.). This decides how far whole-board results (gzip/xz timing, idle memory) can be attributed to MLGO.

No other board changes. Leave the TV on Custom at Home.

## §2 Image scan (`pm0012-image.6nhIbn`, `DONE image rc=1`)

The first job, `platform`, failed after 9 s. Every dependent job (base-proof, hq, roster-gcc/official, audit-gcc/official) stopped with rc=2. From `jobs/platform/job.log`:

```
File ".../image-tree.py.txt", line 70, in partition
ValueError: ambiguous GPT partition layout: {'label': 'gpt', ... 'firstlba': 34, 'lastlba': 2408414, 'sectorsize': 512,
 'partitions': [{'node': '.../platform.img1', 'start': 2048, 'size': 2322432, 'type': '0FC63DAF-8483-4772-8E79-3D69D8477DE4', 'name': 'pltf_t.img'},
                {'node': '.../platform.img2', 'start': 2324480, 'size': 81920, 'type': '0FC63DAF-8483-4772-8E79-3D69D8477DE4', 'name': 'prd_t.img'}]}
```

- `platform.img` holds **two GPT partitions**: `pltf_t.img` (about 1.1 GiB) and `prd_t.img` (40 MiB). Select each by its **GPT name** and verify the EROFS magic in each. Use `pltf_t` as the platform tree. Also extract and roster `prd_t`: report its filesystem type and what it contains, and whether installed RPM files live there. Add a two-partition fixture.
- Say whether tonight's kernel batch needs a clean image run. If it does, give the corrected `pm12m image` command first.
- Explain `KERNEL_SRPM_CONTENT_MATCH UNAVAILABLE`.
- Positive results from that run, to keep: Source1005 is byte-equal in Official and Custom (`7d890834…`). The GCC kernel SRPM label is `vbs-vdlinux-20260929.194254-0-14293732`, the **same CL 14293732** as both LLVM kernels.

## §3 AVControl delivery: LTO-aware rule

The 0012q readback shows that both built lanes fail only on **"DWARF producer/options"**: 28 compile calls but only **2 DWARF CUs**, `dwarf_option_proof false`. The default lane also fails on "config gate" (`driver_mode_gaps`: all four drivers load `/usr/bin/clang.cfg` / `clang++.cfg`). AVControl is an **LTO** build, so the CUs are merged and per-file options never appear in DWARF; this predicate cannot pass for LTO packages.

For LTO packages, replace it with:
- wrapper receipts for every compile and for the LTO link argv;
- Thumb mode in the bitcode function attributes of the fat objects (`target-features` / `"thumb-mode"`);
- mapping-symbol ISA in the final ELF (default lane: A32 share 0.95%; baseline: 99.98%).

Also fix the "config gate". The Official `clang.cfg` has no `-mthumb` (`2ec8547a…`: target, resource-dir and `-D_FILE_OFFSET_BITS=64` only), so in the default lane, check that the scoped block is present in the cfg the driver actually loaded. Re-evaluate the retained default lane (`pm0012-pilot.FejM73`) with the new rule and report T1–T8, giving the specific reason for each REVIEW item (T1 lists 28 unmatched inputs; T2, T4, T6 REVIEW; T5 CHECK_NOT_OBSERVED; T7 REVIEW_GENERATED_SOURCES). Then give the re-run command for the package lane with the `cf4e0e9` wrapper fix.

## §4 Kernel ELF sizes from debuginfo

The listing shows that `tztv-kernel-perf-debuginfo-1-1.armv7l.rpm` **is published** in `repos/product/armv7l/debug/` for both QBs (and `tztv-kernel-debuginfo`, `-debugsource`). The 0012p failure was a timeout. Download both perf debuginfo RPMs, match the build IDs `419813f2…` (Official) and `4d95bb9e…` (Custom), and report Berkeley text/data/bss/dec plus per-section `.text`, `.rodata`, `.data`, `.bss` and `.init.*`, as Table B next to the board values. Give one read-only native command with longer timeouts and retries.

## §5 Replay cause (before Thursday's K0)

The pm0005 replay payloads have the same length as the QB payloads, but 7.72 MB (Official) and 7.52 MB (Custom) of about 11.3 MB differ, starting in `.text` at 0x594 with a 4-byte stride. Find the cause: link order, a different toolchain build, embedded paths shifting literal addresses, a config difference, or something else. Say how K0 will be qualified if a GBS rebuild is not byte-reproducible: for example, the same `.config`, the same section sizes, and only explained differences.

## §6 Disk

`/home1` is at 93% (135G free) after removing two failed benchmark GBS roots (`pm0010-gbs-board-bench.hadnvlae`, `.hfmy3w53`). The disk is shared; most of its use is outside `vd-tree`.

List every directory under `workspace/` and `workspace/temp/` that our work created, with its size, purpose, whether any pending task or report still needs it, and a keep/prune verdict. Include the older `vd-gbs-applied-full-build-r3-*`, `manifest_state` (23G), `z901` (17G), `s895c` (12G), `llvm22_bootstrap101_*` (10G), `o*`, `core*`, `ctx*` and similar. Keep, for now:
- `pm0005-gbs-kernel.mtob625f` (needed for §5);
- `pm0010-gbs-board-bench.eli_m1on` (pristine root);
- `pm0012-smoke.neJb0i`, `pm0012-pilot.FejM73`, `pm0012-wed-a.M5knpj`;
- `qb-evidence`, `usb`.

Give a prune command limited to the confirmed entries. It must keep logs and JSON, refuse mounts and running builds, and touch nothing outside `workspace/`.

Reply in `comms/codex_to_claude/0012r_reply.md`, with §1 first. Data only.
