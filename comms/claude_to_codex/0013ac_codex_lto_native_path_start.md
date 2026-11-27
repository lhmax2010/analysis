# 0013ac — Start implementing the LTO non-PIC native path (HQ PIC design, 20 Nov)

The operator pointed out that the native-path half of the HQ PIC/FatLTO design was never implemented. The IR path (Source1005 fallback patch) is in both LLVM toolchains and under independent review. The native path has only the 20 Nov design and the GNU ld 2.43 fixture. This prompt starts the implementation.

Reference documents:
- the design: `HQ_PIC_FatLTO_Native_Path_Design_20261120.md` (D-014 in `DECISIONS.md`);
- the review: `reviews/lto-nonpic-fallback/`.

The fixture is already done: on Tizen GNU ld 2.43, `R_ARM_ABS32` in `.text` links as a DSO and as a PIE with `DT_TEXTREL`/`DF_TEXTREL` under the default settings and `-z notext`, and `-z text` rejects it. The retained build.conf `98690f23…` and both Base configs set no `-z text`.

## Phase 1 — shipped-image audit (no build; can run now, alongside the running enumeration)

On the retained Official **37777148** platform and prd extraction (the same 4,793 ARM ELFs as PQnb3T) and on **GCC 37564293** for comparison, check every ARM32 DSO and PIE:

1. `DT_TEXTREL` and `DF_TEXTREL` flags.
2. Dynamic relocations whose target lies in a non-writable or executable `PT_LOAD`. Record the relocation type (`R_ARM_ABS32`, `R_ARM_REL32`, `R_ARM_RELATIVE`, other) and the target segment.
3. For DSOs: any observable local-exec TLS relocations, and `PT_TLS` with an initial-exec or local-exec model where it can be detected.
4. Owner RPM, path and file hash, using the existing census owner join. Unknown owners are kept as a separate bucket.
5. Coverage: ELFs scanned, unreadable inputs and partitions covered. A "clean" verdict needs reconciled coverage.

Output:
- a ledger TSV of image × path × owner × flags × relocation type × segment;
- a summary line `PIC_AUDIT <image> textrel_elfs=<n> ro_dyn_relocs=<n> tls_le_dso=<n> scanned=<n>/<n>`;
- the top owners by hit count.

The audit is read-only, writes only to the workspace and takes no build lock. Give the PM a hash-pinned command.

## Phase 2 — fixture on the real FatLTO routes (local GBS, small)

Extend the completed GNU ld fixture to Clang `-ffat-lto-objects` non-PIC objects, built from the same hashed inputs. Consume them via:
- (a) the LLVM LTO plugin;
- (b) GNU ld with no LTO;
- (c) lld with no LTO;
- (d) a GCC driver link.

Each route runs with the default settings and with `-z text`, on `R_ARM_ABS32` in code, `R_ARM_ABS32` in writable data (the control), `R_ARM_REL32`, MOVW/MOVT and `TLS_LE32`.

Pass criteria:
- every permissive output that has a text relocation is detected;
- `-z text` rejects it;
- PIC controls link and run.

Report any unconditional rejection separately.

## Phase 3 — `-z text` package trial (after the 0013o package-worker fix)

Add `-Wl,-z,text` to the armv7l LLVM build.conf link flags in a **TEST-ONLY** trial, and the equivalent `-z text` for direct linker calls. Apply it to the eight RPM inventory entries, the gst-ffmpeg build-input case and the CAPI FatLTO case.

Record for each:
- the effective final linker argv, showing that enforcement reached the link, or that the package overrode it;
- pass or fail;
- for any failure, the object, relocation and producer flags.

Do not change production configs. A change ships only as a shelve CL that the operator builds; never submit.

## Phase 4 — TLS consumers

Repeat the GBS native and plugin links for `libcapi-base-common.a:tizen_error.c.o` and for the TLS local-exec members of libdw, libasm, libelf and libunwind-arm. Use link maps to prove which members were selected and the output type.

## Deliverable now

1. The Phase 1 audit command (hash-pinned, for PM review).
2. The Phase 2 fixture plan and command.
3. A one-line Phase 3 dependency on 0013o.

Archive this prompt. Update `STATUS.md`: the LTO native path is "implementation started; Phase 1 audit pending".

No GitHub submission from the Native Server.
