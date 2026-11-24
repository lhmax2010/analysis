# 0012l · Official perf candidate and Thursday review

**Config status: `SAME_BUILD_DEVEL_CONFIG_CANDIDATE`.** The Official devel RPM contains exactly one perf candidate, `/usr/include/kernel_header/perf/.config`, 156,327 bytes, SHA-256 `2a31652557d89d100d3c1bc6b0116556e32a56f03b0145eba12af425c75379f3`. The native copy is `/home1/chengkai/vd-tree/workspace/temp/pm0012k-config._udmxdk9/2a31652557d89d100d3c1bc6b0116556e32a56f03b0145eba12af425c75379f3-.config`. The two devel ELFs are seret/debug and seret/release. The Official boot payload contains no embedded config. Its running build ID is `419813f26f2d03bee00bde1d7173b0c2fd887530`. The archived terminal block has SHA-256 `c98192fc511a433172a7193278daa0fc150c4109c5b1afa8471bbecd90cd5a88`; the hash covers the block as supplied, including abbreviated fields and its final newline. [Native evidence](../../artifacts/evidence/native-run-r0012k-official-config-20261124.txt) · [Operator settings and original request](../claude_to_codex/0012l.md)

The operator's candidate grep records Clang/LLD 22.1.8, performance optimization, A32, no LTO, frame-pointer unwinding, modules enabled and KALLSYMS disabled. Its CMA default is 0 MiB. The O1 board data records 304 MiB of DT-reserved CMA. The candidate also disables KPROBES, FUNCTION_TRACER, STACKPROTECTOR and CFI_CLANG.

## K0 proof and measurement definitions

The runner re-extracts the pinned member, compares the generated K0 config **byte for byte**, and saves the unified diff. K0 must reproduce uImage **11,348,968 B** and zImage **5,326,504 B**. It compares `.text`, `.rodata`, `.data`, `.bss` and the union of all `.init.*` sections. An ELF reference must carry O1's build ID and its .text bytes must occur in the verified decoded Official payload (11,348,644 B, `6073c427…`). It checks the retained Official replay and K0 itself, and accepts an additional native ELF via `PM12_OFFICIAL_PERF_ELF`. Flat image bytes have no section headers or file-backed BSS. A missing reference yields `NO_MATCHED_ELF`; identical compressed sizes alone do not qualify the lane. A different K0 build ID is recorded with the two banners for timestamp/user/host comparison. A path-related explanation needs independent evidence.

Config and output qualification together give `OFFICIAL_PERF_BUILD_CONFIG` (K0-reproduced build config). A config mismatch prints `K0_CONFIG_MISMATCH`. Unqualified treatment builds retain raw results; comparative interpretation waits for K0. The earlier 18 November Official replay zImage was 5,326,464 B, **40 B below** the required value. That earlier replay does not qualify the new K0. [Qualification](../../artifacts/scripts/r0012l/kernel-qualification.py.txt) · [Earlier replay evidence](../../artifacts/evidence/native-run-r0011f-batch-xkHDpd-20261124.txt)

## K0–K5 table to return

All numeric observations below await native builds. A dash denotes an unmeasured field. The runner writes raw bytes and counts to `kernel-lanes.tsv`.

| Field | K0 | K1 | K2 | K3 | K4 | K5 |
|---|---|---|---|---|---|---|
| ISA / advisors / explicit outline | ARM / release / off¹ | ARM / release / on | ARM / default / off¹ | ARM / default / on | Thumb / release / off¹ | Thumb / release / on |
| Config identity / build ID | candidate → K0 gate | K0 symbols | K0 symbols | K0 symbols | full K4−K0 diff | full K5−K1 diff |
| Expected unwinder, verify in generated config | FP | FP | FP | FP | ARM EHABI | ARM EHABI |
| uImage / zImage / modules, B | — | — | — | — | — | — |
| .text, B | — | — | — | — | — | — |
| .ARM.exidx / .ARM.extab / sum, B | — | — | — | — | — | — |
| Resident linked footprint, B | — | — | — | — | — | — |
| Thumb Δ .text / EHABI / resident, B | | | | | vs K0 | vs K1 |
| Direct call sites by class² | — | — | — | — | — | — |
| Outlined helper count / selected board site | — | — | — | — | — | — |

¹ As delivered, with no additional outline flag; count any helpers that the baseline produces. ² Tail, thunk, LR in register, LR on stack, no local LR save, unresolved. Count per calling edge; each helper retains its own callers. The resident estimate uses the linked range `_end − _text − (__init_end − __init_begin)`, including linker padding. Missing boundaries leave the estimate unavailable. Board RAM measurements remain separate. Thumb comparisons include the observed unwinder transition.

## Unwind, section and module evidence

- For frame-pointer lanes, the audit retains the helper body, caller PC/prologue and instructions around the call, and flags FP changes, tail edges, frameless helpers and nested calls. An LR save can preserve execution while omitting a logical frame from a trace. Counts describe observed instruction shapes; unresolved origins and calls remain visible. LLVM also supports outlining with no local LR save. [ARM outliner implementation](https://github.com/llvm/llvm-project/blob/llvmorg-22.1.8/llvm/lib/Target/ARM/ARMBaseInstrInfo.cpp)
- For EHABI lanes the audit checks full helper-range coverage and decodes descriptor instructions. It distinguishes missing ranges, CANTUNWIND, simple leaf/finish matches and descriptors requiring manual stack-effect verification. Section checks retain restricted input-section matches and init callers of resident bodies. Static observations and board unwind acceptance have separate fields. K1/K3/K5 still require a defined native pre-link helper and the final LLD 22.1.8 argv. [Static audit](../../artifacts/scripts/r0012f/kernel-audit.py.txt) · [Compile/link proof](../../artifacts/scripts/r0012k/outliner-phase.py.txt)
- K4/K5 retain expected-vs-produced in-tree module paths, external module results, build diagnostics by file where the toolchain identifies it, and assembly source/line candidates joined to verbose build lines. ISA/FP mentions in assembly are review candidates. A build failure needs the diagnostic, responsible source and alternate-lane result to attribute it to Thumb or the unwinder. A successful build still needs module-load and unwind checks on the board. [Module runner](../../artifacts/scripts/r0012e/kernel-modules.py.txt)
- Each built lane retains vmlinux, System.map, .config and hashes under `symbols/<build-id>/<lane>/`. The site selector looks for a uniquely attributed reachable call from a read-only proc workload and records its exact PC, caller, helper range and workload. No lane binary or trace was supplied this round, so there is no measured site or pass for any lane. The runbook specifies offline symbolization, module relocation, and the hit/expected-parent gate. [Board runbook](../../artifacts/runbooks/kernel-outliner-board.md)

## Thursday pin for PM review

Commit `ce05ccee13a0bd7fc32fbd209d30335ee4e4ec1c`. All 41 manifest entries verified. Manifest SHA-256 `c5d2050c5e71056c29a845950bb71f0df7677e11aeb84188570bdcc669456405`. Batch SHA-256 `5ff02049ad9658c1c7b624f75daf2c16e07847b9b89f6ecea99462ddba0775bd`.

Python 3.10.12 fixtures passed for K0 equality/mismatch, the one-byte zImage mismatch, missing reference, full config diffs, symbol retention, the pre-link and LLD receipts, ARM disassembly, LR-save variants, decoded EHABI, and trace address parsing. The staged spec patch applied at zero fuzz. Its build-root external command inventory remains gated; the make-wrapper fixture copied System.map and objects using a restricted PATH. New ELF/config/trace analysis executes on the native host. No new gawk feature or post-coreutils-6.9 path tool is injected. The fixture used compatible command behavior on the local machine. Native GBS and board measurement await review. [Tests](../../artifacts/tests/r0012l/check.py)

After PM approval, run in an attended native terminal with the explicit Wed-A and image-job directories. One heavy job at a time, up to six GBS cores, 55 GiB disk / 16 GiB RAM build gate, internal source/dependency downloads. Six kernel builds plus external modules can take overnight or longer.

```bash
(
set -eu
cd /home1/chengkai/vd-tree
: "${WEDA:?set the explicit Wed-A run directory}" "${IMAGE:?set the explicit image run directory}"
export PM12_IMAGE_RUN="$IMAGE"
pin=ce05ccee13a0bd7fc32fbd209d30335ee4e4ec1c
manifest=c5d2050c5e71056c29a845950bb71f0df7677e11aeb84188570bdcc669456405
d=$(mktemp -d "$PWD/workspace/temp/pm0012-launch.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --retry-delay 5 --connect-timeout 15 --max-time 120 \
  "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0012/batch.sh.txt" -o "$d/batch.sh"
printf '%s  %s\n' 5ff02049ad9658c1c7b624f75daf2c16e07847b9b89f6ecea99462ddba0775bd "$d/batch.sh" | sha256sum -c -
exec bash "$d/batch.sh" attended "$pin" "$manifest" thu "$WEDA" "$PWD/workspace/temp/pm0011f-batch.xkHDpd"
)
```

Set `THU` to the printed run directory. Return the compact table first. For a full matrix or nonempty config diff, use the packet command below and repeat with the next page through the printed total. [Matrix runner](../../artifacts/scripts/r0012f/kernel-matrix.py.txt)

```bash
MATRIX="$THU/jobs/kernel-thumb"
cat "$MATRIX/kernel-lanes.tsv"
python3 -B "$THU/development.py.txt" packet "$MATRIX/kernel-matrix.json" 1
```
