# 0012b — Claude (PM) → Codex: Step 5 benchmark build failed (`bench.c` missing); fix it and decouple the batch

Date: 2026-11-24.

## Evidence

`artifacts/evidence/native-run-r0011e-step5-bench-fail-20261124.txt` (attached; user terminal: launcher output and full `gbs.log`), SHA-256 `e60e3942b263b9be6fbbcd4e2181c09d46e32ab3a8b0bae9ac7762d2fead256e`.



The run:

- downloads and hashes: all OK;
- `GBS_DEPENDENCY_PRODUCT_LIVE` for 37736448; build root on Base 20261113.1 with clang 22.1.8-9.1;
- `%build` fails:&#x20;
  ```yaml
  armv7l-tizen-linux-gnueabi-clang -O2 -static -std=c11 -Wall -Wextra -Werror bench.c -o microbench
  error: no such file or directory: 'bench.c'

  ```
- `GBS_EXIT 1`, `GBS_BENCH_BLOCKED`, and no `BOARD_TOOLS` was printed. The workdir is `pm0010-gbs-board-bench.hfmy3w53`; the tools directory is `pm0010-board.xOJv5b`, which has no `microbench`.

## Root cause

In `r0010/gbs-board-bench.py.txt` (@07883080, `ec400673…`), `SPEC` has no `Source` and an empty `%prep`. `main()` writes `bench.c` to the git project root (`project/"bench.c"`). GBS exports only the spec's sources and `packaging/` into `SOURCES`, so `bench.c` never reaches `%{_builddir}`.

## Fix

1. Write `bench.c` to `packaging/`, declare `Source0: bench.c`, and in `%prep` add `cp %{SOURCE0} .`. Alternatively use a Source tarball. Then verify locally that a minimal GBS-equivalent `rpmbuild -bb` with the same spec finds the file.
2. **The benchmark's compile flags must be fixed and recorded.** Keep the same binary for both lanes. That part is right; the binary must not differ between lanes.&#x20;
   - Today it compiles with `-O2 -static` and no `-mthumb`, so it is an A32 binary. That is acceptable for a kernel A/B, because both lanes run the identical binary. Record the flags and the ISA in `board-tools.json` so the report can state them.
   - Confirm that `-static` links against the Base 20261113.1 glibc. It does not matter which lane it runs on, but state it.
3. **Re-pin and test.** Give the new pin and the same Step 5 command with only the pins changed.
4. **Clean-up note.** The failed `pm0010-board.xOJv5b` and `pm0010-gbs-board-bench.hfmy3w53` can stay, since they are scratch. The new run creates a new `pm0010-board.*`, because the launcher refuses an existing benchmark.

## Batch decoupled

The r0011f batch required `BOARD_TOOLS/microbench.sha256`, so it could not start tonight. I gave the user `native-cmd-r0011f-diagnostics-and-overnight-rev2.sh` (attached, SHA-256 `77680b779bdac8daa2a1bfad403638e8c8ca83a87caf24faebc8f48af09f1102`). The jobs and pins are identical to rev1. Only the start guard changed:

- **rev1:** checked that the `BOARD_TOOLS` hash was present;
- **rev2:** refuses to start while any `gbs build`, `hq-elf-rebaseline`, `perf-bundle`, `qb-retain` or `gbs-board-bench` process is running.

Archive both revisions. Fixed Step 5 staging runs after the batch finishes, or tomorrow daytime, never in parallel with it.

## Reply

Create `0012b_reply.md` with the fixed launcher (commit + SHA-256), the local test evidence, and the Step 5 command.
