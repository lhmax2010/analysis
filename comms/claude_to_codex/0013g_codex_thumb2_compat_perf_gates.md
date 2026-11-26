# 0013g • Thumb-2 rollout: compatibility and performance gates (user requirement)

The user requires that the Thumb-2 switch keep Tizen **compatible and performant**, not only smaller. Size is already measured: AVControl `.text` −40.1% with the toolchain default, and A32 693,820 → 88 bytes. Before the Thumb-2 QB is proposed, every item below needs an owner, a method and a pass rule. Static items run from RPMs and images now. Board items run on the Thumb-2 QB against Official 37777148.

Lower priority than 0013f. Use no build lock and no GBS. The static scans may reuse the `qp4O4m` RPM caches.

## A. Compatibility (static, before the QB)

| # | Check | Method | Pass rule |
| --- | --- | --- | --- |
| C1 | ARM-only source | Over the sources of the ARM-predominant cohort (the 609 set mapped to source packages): inline asm and `.S` with `.arm`/`.code 32`, ARM-only encodings, PC arithmetic or jump tables that assume 4-byte instructions, `mov pc, lr` returns | Every hit is classified as assembler-protected (an explicit `.arm` section stays A32), as a needed fix, or as a package exclusion |
| C2 | Interworking with prebuilt or vendor A32 code | Disassemble prebuilt ELFs (no Clang/GCC CU producer, or vendor-owned) for non-interworking returns (`mov pc, lr`, `ldm …, pc` without the `bx` pattern) and for exported functions that Thumb callers reach | No non-interworking return is reachable from Thumb code |
| C3 | ABI | Per package: dynsym (name, type, binding, version, size), SONAME, `DT_NEEDED` | Identical to the A32 build |
| C4 | **Frame pointer and unwinding** | Thumb uses **r7** as its frame pointer, while A32 uses **r11**. Find every consumer that unwinds by frame pointer: the crash reporter (crash-worker or equivalent), profilers, sanitizers, `backtrace()` users, and any code reading r11. Also check that `.ARM.exidx`/`.ARM.extab` are present where EHABI unwinding is used | Crash dumps and backtraces stay correct for Thumb code; this is proven on the board with a deliberate crash in a Thumb binary |
| C5 | JIT and self-generated code | Web engine (V8/Chromium), .NET runtime, any JS/Lua JIT, FFI trampolines (libffi) | Their own ISA settings are unchanged by the default switch, or they are listed as exclusions |
| C6 | Exclusions honoured | Kernel and external modules, bootloader, TEE, firmware, and packages with explicit `-marm` | The explicit `-marm` still wins: an argv proof per excluded package |

## B. Performance (board, Thumb-2 QB vs Official 37777148, same board, alternating boots)

| # | Workload | Repeats | Pass rule |
| --- | --- | --- | --- |
| P1 | Profile the hot paths during 4K playback and Home/UI navigation (perf top functions and owning packages, A32 vs T32 per function) | 3 | Names the packages whose hot code changed ISA |
| P2 | Microbenchmarks: gzip/xz/zstd, `openssl speed` (sha256, aes-cbc), JPEG/PNG decode, memcpy/memset, using in-image signed binaries | 5 each | Median regression ≤ 3%; otherwise per-package analysis |
| P3 | System: cold boot to Home, launch time of the top 5 apps, 4K playback (CPU load, dropped frames, A/V sync), seek/reopen | Boot ×5, apps ×5, playback ×3 | No regression beyond run-to-run noise (paired CI); zero new dropped-frame events |
| P4 | Memory: MemAvailable at Home, PSS of the top media and UI processes, at idle and during 4K | 3 | Report the saving; no increase |
| P5 | Stability: 24 h soak with playback and app cycling; check for SIGILL/SIGBUS/SIGSEGV and new crash dumps | 1 | Zero new crashes |

Regression policy: a package with a measured hot-path regression goes on a reviewed **per-package `-marm` opt-out list**. It is not reverted image-wide. Hand-written NEON and asm keep their authored mode.

## C. Deliverables

1. Add a **Thumb-2 acceptance plan** section to `reports/weekly/2026-11-27/draft-data.md`: the C1–C6 and P1–P5 tables with status.
2. One read-only native command for **C1, C2, C4 (static part) and C5** over the published 37777148 RPMs and the extracted image, using the `qp4O4m` caches after the 0013f fix. Give the counts and the top rows in at most 40 lines, with the full TSV in the USB export.
3. The **board runbook** for P1–P5 and the C4 crash test, ready for the Thumb-2 QB image next week.

Reply in `comms/codex_to_claude/0013g_reply.md`, after 0013f. Data only.
