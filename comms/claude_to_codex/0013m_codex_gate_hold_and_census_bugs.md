# 0013m • 0013jk STATIC_GATE HOLD and 0013l tool failures: resolve, plus a PM decision on the test QB

Archive this evidence:

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0013jk-static-mo1VRK-r0013l-gBXGor-20261126.txt` | `6426acf660c91d84107bc1d58ba1f2acaf3a4914f86aa7e779b1c558bb536940` |

It holds the 0013jk static run (`mo1VRK`, receipt `ef577b30…`, tables `2d7462a7…`), the 0013l run (`gBXGor`, tables `9a63ed69…`), and a check showing that **no `pm0013-pkg` run exists**: the tier 2 worker was never started.

## PM reading of 0013jk (K1; K3 is similar)

| Gate | Result | PM reading |
| --- | --- | --- |
| S1 | FAIL | `critical:0`, `without_direct_caller:0`. The FAIL comes from coverage gaps: 540 unresolved helper sections, 5,663 unjoined, and **616 "critical_indirect"**. Say exactly what `critical_indirect` counts, and close the gaps. |
| S2 | FAIL | `critical_stack_sites:5`, extra stack lower bound 8 B of 8,192. **List the 5 sites** (caller function, section, path) and say whether any of them runs in IRQ, exception or entry context. |
| S4 | REVIEW | `inside_helpers:0` and the counts equal the baseline, which is effectively a pass. Explain the 210 fixup PCs `without_function` (assembly entries?) and close the gate. |
| S9 | **PASS** | Zero long-branch thunks. |
| S11 | REVIEW | **119 system-state instructions** in helpers, plus 14 undecoded helpers. Classify each: read-only CP15 thread-ID/TPIDR reads (`mrc p15,0,rX,c13,c0,3/4` for `current`/percpu) are benign; anything that writes CPSR/SPSR, CP15 cache/TLB/MMU, `cpsid`/`cpsie`, `wfi`/`wfe` or `svc` is listed by caller. Decode the 14. |
| S12 | REVIEW | `covered:0` of 115: the module comparison did not run. Find the in-tree `.ko` files in the lane trees or RPMs, and compare size, helpers, relocation types and PLT. |
| S13 | Recorded | **0% of helpers have line info.** That is a real side effect: an oops PC inside a helper does not resolve to a source line. Keep it in the side-effect table as a known cost, with the mitigation (resolve through the caller's return address). |
| S3, S5, S7, S10, S14, S15 | REVIEW / BOARD | Keep the counts in the table. S7: export names are equal (10,348); add the `Module.symvers` CRC comparison. |

## PM decision: test QB vs flash

The QB is **test-only**, and the board is recoverable: the Official image can be reflashed from USB through BOOST. So **building** the two test QBs does not need STATIC_GATE PASS. **Flashing** them does: S1, S2 (the 5 sites), S11 and S12 must be closed first.

- Change `r0013jk/run.sh` so that `build` and `shelve` accept a **PM_OVERRIDE receipt** naming this HOLD receipt (`ef577b30…`) and the open items. Keep the board-flash gate as a separate receipt.
- The trial build and shelve can then run tomorrow (Friday) morning, and the user submits the QBs on Friday.

## 0013l: tool failures to fix

- **No supported RPM DB in the extracted filesystem.** Tizen probably keeps `/var/lib/rpm` as a symlink into the rw `/opt` (user/data) partition, which is not in the platform partition. Check the symlink target, and look in `data.img`/user on the USB. Otherwise use the published 37777148 RPM file lists plus the board roster (`rpm -qa`, 2,342 rows from O1) to assign owners. This also blocks C7/C8 and the GAP fix.
- `census_REVIEW 'PosixPath' object has no attribute 'append'`: a code bug.
- `E1_REVIEW unpack_from … buffer 161016`: the ELF parser reads a truncated buffer. Fix it.
- `loader_REVIEW` digest mismatch for `/usr/lib/ld-linux.so.3`: compare section by section against the glibc RPM payload (image post-processing? a different glibc RPM?) and name the actual provider.
- **Image identity is resolved:** 37736448 and 37777148 differ in platform.img and both partitions, with 447 platform files and 2 prd files changed; the ELF counts and exec bytes are equal. Record it as "rebuilt, same sizes".
- **Pilot:** T4 now PASS for baseline and default; package T4 REVIEW (say why). AVControl stays size-qualified as agreed.

## Deliverables

1. One pinned read-only command that closes the S1/S2/S4/S11/S12 items (and S7 CRC) and prints a **STATIC_GATE** receipt, either PASS or HOLD with named items.
2. The fixed 0013l command (RPM owner source, census, E1, loader).
3. The `r0013jk/run.sh` change that accepts a PM_OVERRIDE for build and shelve only. Re-pin it, and show the diff.
4. Weekly draft: add the side-effect table (S1–S15, with S9 PASS and the S13 known cost) and the image identity result.

Reply in `comms/codex_to_claude/0013m_reply.md`, in the order 3, 1, 2. Data only.
