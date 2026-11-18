# Official versus Customized MLGO — comparison record

This draft records the planned comparison on KantSU2E. Run-level results and an outcome are pending.

| Lane | Pinned input | Evidence needed |
|---|---|---|
| Official snapshot | Base 20261113.1 and current KantSU2E image | Image checksum, QB inputs, RPM SHA-256 and Build-ID chain, effective advisor selection |
| Customized snapshot | Base 20261118.1, expected LLVM rev12 srcmd5 `0b38aead137ec42dcd99dee28091acc1` | New QB input proof, architecture binary hashes, effective advisor selection |
| Attribution control | Same rev12 toolchain sources and SR runtime, VD reference models and custom models selected independently | Per-build model digests and advisor-use evidence |

Hold Product, build.conf, shelf list and workload constant for the snapshot comparison. List every added, removed or changed non-LLVM package. Attribute the whole snapshot delta separately from model-only effects. Record compiler wrappers and LTO link commands. If one lane uses heuristics, label it explicitly and use a pair with effective release advisors for model-only claims.

| Measurement | Repetitions and scope | Result |
|---|---|---|
| Image/installed size | Exact bytes and same-package intersection, report scope differences separately | Pending |
| ELF sections | Total .text and PT_LOAD file/memory, top 50 libraries | Pending |
| Boot | Five cold boots per lane with the same ready marker | Pending |
| Settled idle | Three boots per lane, PSS/USS and memory counters after ten minutes | Pending |
| Application launch | Five launches per app and lane, fixed list of five apps | Pending |
| Normal-memory 4K | Three runs, CPU, frame drops, stalls, private/system memory and zone counters | Pending |
| Constrained 4K | Three runs if the 1 GB approximation is qualified | Pending |
| Kernel | Conditional on Clang-built, bootable exact kernel. Two builds per variant. vmlinux, Image, modules, build time, peak memory and microbenchmarks | Pending |

Keep each run with input hashes, board and firmware identifiers, run ID, observation interval and paired lane. Report median, IQR, confidence interval and new crash, LMK/OOM, ANR or audio/video underrun events. The deadline run counts are smaller than the full protocol. Interpret wide intervals accordingly.
