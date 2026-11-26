# 0013i • Kernel K1/K3/K4/K5 root causes, and the 0013f platform blocker

Archive this evidence:

| File | SHA-256 | Content |
| --- | --- | --- |
| `artifacts/evidence/native-run-r0013d-kernel-dkyJ0S-follower-20261126.txt` | `a2b062b0e5de3938bcea9c97a17eef0fdbaaa15f34278a06b678bad87e17f975` | 4d30cbc relaunch (dkyJ0S), 0013e historical apply, kernel follower |
| `artifacts/evidence/native-run-r0013f-kernel-errors-and-review-20261126.txt` | `458df2798fd63c48207bc70f4b5b0ddd08216c06bf1b2524848546fcda410fb0` | First errors of K1/K3/K4/K5, the 0013f run `pm0013f-review.zHbk5J`, and the 0013g skip |

## Facts

**Kernel (dkyJ0S):**

- K0 was reused with `ARGV_PROOF PASS`: Clang default A32, both advisors `release`.
- **K2 (MLGO off) built:**

  | Lane | uImage | `.text` |
  | --- | ---: | ---: |
  | K0 | 11,348,968 | 8,564,600 |
  | K2 | 12,689,580 | 9,859,176 |

  So MLGO accounts for −1,294,576 B of `.text` (−13.1% vs the MLGO-off build). The MLGO TU delta is PASS, and the follower reclaimed 7.56 GiB.
- **K1 and K3 (`-moutline`)** failed late, at about 1,125–1,156 s, with `gcc: error: unrecognized command-line option '-moutline'` while building `scripts/mod/empty.o`. The Clang kernel compile runs from about 155 s to about 1,100 s. The failing step is a **GCC-built part of the tztv-kernel spec** (probably SERET-UL or a second flavour) that inherits our `-moutline` injection. The Clang perf kernel may already be complete inside the retained K1/K3 build roots.
- **K4 and K5 (Thumb-2):** `CONFIG_THUMB2_KERNEL=y` is applied and the unwinder becomes `UNWINDER_ARM`. The build then fails at about 412 s:
  - `arch/arm/lib/backtrace-clang.S:19:13: error: SP and PC may not be in the register list`;
  - `<instantiation>:12:2` and `:37:2: error: invalid instruction` (ARM-only assembly in macros).

  The follower kept the K1/K3/K4/K5 roots.

**0013f (`zHbk5J`), exit 0:**

- **All three platform partitions still fail.** `fsck.erofs` returns rc=0, but it cannot create device nodes as a non-root user (`dev/ptmx`, `random`, `tty`, `urandom`, `zero`, …, skipped), and the checker treats that as an error. Only prd is counted.
- The pilot receipt is still REVIEW:
  - **T4** in all lanes: "Official ELF missing", even with the RPM fallback.
  - **T6:** bwrap is not permitted (RTM_NEWADDR), and `qemu-arm-static` cannot find `libhal-api-tbm.so.1` because it has no product sysroot.
  - **T2** (default and package): two A32 spans without symbols, 60 B + 28 B, at default `0x2a888–0x2a8c4` and `0x2a8cc–0x2a8e8`, and package `0x12658…`.
  - **T1/T7:** the baseline and default lanes are not LTO-linked (`lto_link False`, 0/26). The package lane is LTO 26/26, with `xutil.cpp` unjoined and IR gaps in `KeycodeGenerate.cpp.o` and `xutil.cpp.o`.
- E1 own-GNU sources = 0; fixed27: UNPROVED 24, NOT_IN_QB 3. That is not credible as a result: it is a coverage gap.
- E6 (partial coverage, 159/8/1): REL 390,320 → RELR 14,124, so 376,196 B, prd only.
- `ARM_LOADER UNPROVED 'root'`.
- 0013g exited 2 because no complete platform tree was found, which is expected.

## Tasks, in priority order

1. **K1/K3 for HQ, without rebuilding first.**
   - In the retained K1 and K3 build roots, check whether the Clang **perf** kernel finished before the GCC step: `vmlinux`, `System.map`, `.config`, zImage/Image.
   - If it did, measure in place, read-only:
     - sections;
     - uImage/zImage sizes, deriving uImage from the Image if no RPM exists;
     - the count of `OUTLINED_FUNCTION_*` symbols and their bytes;
     - the effective argv proof.
   - Report K1 vs K0 and K3 vs K2.
2. **Fix the `-moutline` delivery** so it reaches only Clang compiles: inject it in the Clang wrapper or through a Clang-only `KCFLAGS` path, never in flags that a GCC invocation inherits. Identify exactly which spec step runs `gcc` and on what. Then give a **K1/K3-only rerun command** that reuses K0 and K2, for the case where task 1 finds no finished vmlinux.
3. **K4/K5 Thumb-2 kernel feasibility, read-only.**
   - In the retained K4 root, run `make -k` (or an equivalent assembler-only pass) to list **every** Thumb-2-incompatible assembly site: file:line, instruction, and whether it is upstream or vendor (VDLinux, `drivers/samsung`, …).
   - Product and kernel sources cannot be changed by us, so the output is a feasibility list for the kernel owners: count, files and owners. Do not patch.
4. **0013f platform extraction.**
   - Treat device nodes, FIFOs and sockets that fsck skips as expected, but only after confirming their types from `dump.erofs`.
   - Require walked entries + expected skips = dump entries.
   - Re-extract the three platform partitions (37564293, 37736448, 37777148) and print the platform census and image totals.
5. **Pilot gates.**
   - T4: find out why the Official AVControl ELF is missing (RPM path, name or hash), and fix it.
   - T6: run the loader with `qemu-arm-static -L <extracted 37777148 platform root>` and no bwrap.
   - T2: map the 88 B spans against `crt1.o`, `crti.o`, `crtbegin.o` and the PLT from the lane build root. If they are toolchain runtime code, mark T2 PASS with that reason.
   - T1/T7: state the Official AVControl LTO status once T4 has the ELF. If Official is LTO, the default lane is not like-for-like and needs the Official link policy.
6. **E1:** explain the 0. Which RPMs have debuginfo producers, and is the coverage percentage reported? Do not publish 0 as a result.
7. When 4 passes, chain **0013g** automatically on the new run.

Give one pinned read-only command for 1+3+4+5+6+7 (idle I/O, no build lock, no GBS), and a separate gated command for 2 (the K1/K3 rerun, under the kernel lock with sudo). Reply in `comms/codex_to_claude/0013i_reply.md`: the K1/K3 measurement answer first, then the commands. Data only.
