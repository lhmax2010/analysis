# 0013s • URGENT: the build finished, but the post-check rejected the uImage trailer. Add verify-only mode; PM board-flash decision

Archive this evidence:

| File | SHA-256 | Content |
| --- | --- | --- |
| `artifacts/evidence/native-run-r0013q-static-00KP3P-20261127.txt` | `0deec1bd0f73a84e5f0da0ff2279768ec3ab6faad4212f79aab0d55c4e197455` | Fixed static run 00KP3P (receipt `57773c7c…`) |
| `artifacts/evidence/native-run-r0013p-build-jEMVH7-and-s11-20261127.txt` | `8f367caec3068d89340e2b661a199b0382d8aacb0a98d45045345aace77b4720` | The d428782 build jEMVH7, plus the S11 archive readback |

## 1. Build `pm0013jk-build.jEMVH7`: GBS ran, then `rpm_boot` failed

- The spec diff printed as expected (one line, 301), preflight passed, and GBS started. The traceback then came from `rpm_boot` → `need(length==len(payload) and crc==zlib.crc32(payload),"kernel payload CRC")`.
- **Cause:** `payload=u[64:]` assumes the uImage ends at header + data size. These KantSU2E uImages carry a **trailer after the data** (the HQ table notes: Total = uImage − 64, including a 260-byte trailer). So `len(u[64:])` ≠ `ih_size`.
- **Fix:** `payload=u[64:64+length]`; check `crc==zlib.crc32(payload)`; record `trailer=len(u)-64-length`, and require it to equal the Official 37777148 uImage's trailer length. Image = `payload`.
- **Add a `verify` mode** that reuses the existing `jEMVH7` GBS-ROOT and RPM **without rebuilding**. It must run every post-build check (RPM, zImage tree match, sizes within 0.1% of K1, helper count, argv proof for SERET-UL GCC without `-moutline` and for Clang with it, module argv) and emit `BUILD_RECEIPT`. `shelve` must accept that receipt.
- Give the `verify` command, the receipt prompt line and the unchanged `shelve` command. **This is the critical path for the user's QBs today.**

## 2. S11 classified by PM: board-flash decision

The 00KP3P tables (`K1/K3-sensitive-ops.tsv`, `-system-state.tsv`) show that **all decoded system-state ops are `mrc p15, #0, rX, c13, c0, #3`**: 118 of 119 in K1, 164 of 165 in K3. That is a read of **TPIDRURO**, which Linux 6.12 ARM uses for the `current` task pointer. Examples of direct callers: `sys_rt_sigreturn`, `vfp_restore_user_hwstate`, `cpus_read_lock`, `cpu_v7_ca15_ibe`. It is benign: a read with no state change, valid in any context. The classifier's `tp_reads:0` is wrong because it only accepts c13,c0,4.

- Fix the classifier (c13,c0,3 and c13,c0,4 reads are thread-pointer reads).
- **Name the one remaining op** per lane (119 − 118 and 165 − 164) in the verify output.

**PM decision: BOARD_FLASH for the two `-moutline` test QBs is allowed once the remaining S11 op is named and is not a write**, because:

| Check | Basis |
| --- | --- |
| S1 | Direct critical-section calls into helpers = 0 |
| S2 | Lower bound 8 B on 8,192 B; the sites are process-context or allocator functions |
| S4, S9 | PASS |
| S11 | TPIDRURO reads only |
| S12 | Becomes a **pre-flash check on the QB RPM modules** (compare the module sizes and relocation types of the two QB kernels against 37777148/37777264) |

Encode this as a `BOARD_FLASH PM_PASS` receipt with these conditions, kept separate from STATIC_GATE.

## 3. 0013r

The `ee9983f` reader is approved by PM, and the user will run it. No change is needed.

Reply in `comms/codex_to_claude/0013s_reply.md`: the verify command first, then the shelve command, then the BOARD_FLASH receipt rule. Data only.
