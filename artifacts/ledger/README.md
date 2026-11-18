# Installed compiler ledger

[Verified] The board reports 2,342 installed RPM identities and 1,839 distinct source RPM strings. Product-first lookup found 2,342 exact NEVRA metadata matches. The board release and raw capture digest are recorded in [board identity](../evidence/board-readonly-20261117.txt). Package release metadata still needs a QB build-to-image proof and payload/Build-ID corroboration. The match percentage is 100% for installed metadata. Compiler coverage is **unknown**.

- [Installed identities](installed-rpms-20261117.csv) and numbered parts 02–08 preserve all rows.
- [RPM metadata match](rpm-metadata-match-20261117.csv) and numbered parts 02–08 show repository lookup.
- [Native payload plan](rpm-payload-plan.csv) and numbered parts 02–08 include repository checksum and location.
- [Exception review](exceptions.csv), [firmware feasibility](firmware-feasibility.csv) and [QB gap](qb-build-results.md).

## Compiler attribution

Download one checksummed RPM at a time. Inventory its ARM ELF, including extensionless ELF, and retain its Build ID and compiler markers. Where retained debug payloads exist, join by Build ID and inspect DW_AT_producer for the real translation units. Mark GNU crt/startup CUs separately and check runtime/linker provenance. An ELF may contain both Clang and GCC markers through startup files. A bare GCC marker is ambiguous. Clang marker identifies some Clang contribution. Rust markers indicate a Rust contribution. Resolve assemblies and mixed source types with the source/build record. Embedded TPK files and vendor contents need their own provenance.

Roll up to source RPM with CLANG, MIXED, GCC, PREBUILT/VENDOR, NON-C/C++, NO-ELF or UNKNOWN. NO-ELF requires complete payload coverage of applicable contents. Denominator is eligible C/C++ source packages after justified exceptions. Numerator is eligible CLANG source packages supported by the full shipped-code review. Keep MIXED and GCC in the queue and report all unknowns.

Run the marker stage described in [reply 0002](../../comms/codex_to_claude/0002_reply.md) before a producer rollup. A first filesystem/transport sample and available-size check are needed to bound total runtime. One RPM is cached at a time, capped at 1 GiB. Archive/debuginfo and current source reconciliation remain further work. For planning, budget a native task slot for several hours, with output/throughput re-estimated from the first 30 RPMs.

## CSV parts

- installed-rpms-20261117: [01](installed-rpms-20261117.csv), [02](installed-rpms-20261117-part-02.csv), [03](installed-rpms-20261117-part-03.csv), [04](installed-rpms-20261117-part-04.csv), [05](installed-rpms-20261117-part-05.csv), [06](installed-rpms-20261117-part-06.csv), [07](installed-rpms-20261117-part-07.csv), [08](installed-rpms-20261117-part-08.csv)
- rpm-metadata-match-20261117: [01](rpm-metadata-match-20261117.csv), [02](rpm-metadata-match-20261117-part-02.csv), [03](rpm-metadata-match-20261117-part-03.csv), [04](rpm-metadata-match-20261117-part-04.csv), [05](rpm-metadata-match-20261117-part-05.csv), [06](rpm-metadata-match-20261117-part-06.csv), [07](rpm-metadata-match-20261117-part-07.csv), [08](rpm-metadata-match-20261117-part-08.csv)
- rpm-payload-plan: [01](rpm-payload-plan.csv), [02](rpm-payload-plan-part-02.csv), [03](rpm-payload-plan-part-03.csv), [04](rpm-payload-plan-part-04.csv), [05](rpm-payload-plan-part-05.csv), [06](rpm-payload-plan-part-06.csv), [07](rpm-payload-plan-part-07.csv), [08](rpm-payload-plan-part-08.csv)
