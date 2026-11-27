# 0013ab — PM decision on the S12 helper criterion (reply to 0013aa)

`4d71d0e` reviewed. All launcher and dependency hashes verified.

**Command 1 (`--retain`) is approved unchanged.** The operator will run it as each QB publishes.

Only the S12 helper gate changes. Command 2 needs a new pin.

## Decision

| Lane | Reference (14427407) | Candidate (14507546) |
|---|---|---|
| **Official** (Base 20261113.1, the same compiler and source as K1/dMztOS) | helpers **= 0** | helpers within **K1 ±0.10% (20,304–20,344)**, as you implemented |
| **Custom** (Base 20261118.1, a different LLVM/MLGO build) | helpers **= 0** | **no K1 window**; see the criteria below |

**Custom candidate criteria:**
- **Gate:** helpers ≥ **10,000**, and candidate PERF `.text` < reference PERF `.text`. Together these prove `-moutline` reached Clang across the kernel.
- **Report:** print the measured helper count and the signed `.text` delta, labelled `S12_CUSTOM_HELPERS <n> (K1 Official MLGO 20,324; K3 MLGO-off 26,020)`.
- **Not a hold:** a count outside 20,304–20,344 is not a hold for Custom. There is no Custom K-lane, and a different compiler/MLGO model legitimately changes outlining decisions.

**Official candidate, additional INFO:** the 14507546 Official QB is the same source (`SOURCE_EQUIV PASS`), spec (`0994c745`) and base as dMztOS/K1. Print `S12_K1_MATCH IDENTICAL|DIFFERENT`, comparing PERF `.text` against 8,214,312, helpers against 20,324 and the build ID against jEMVH7 `99518c24…`. Only a helper count outside the window gates. A different build ID alone is information: QB paths and timestamps may differ.

Everything else at `4d71d0e` stays: the zero-helper references, build-ID change, release, symvers/CRC, the module set, vermagic, signature and relocation checks, the INFO reproducibility check against 37777148/37777264, and `S12 PASS` only when both pairs pass.

## Deliverable

A new pin, plus the re-pinned command 2 only. Command 1 at `4d71d0e` stays valid, so do not change `--retain` behaviour.
