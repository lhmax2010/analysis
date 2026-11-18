# Package build status and data gaps

[Verified: exported tracker] The maintained historical action tracker has **986 rows / 942 distinct package labels**. Labels include variants and are not normalized unique source RPM identities. It groups migration and optimization decisions rather than recording all build invocations.

**A comprehensive current GCC-versus-LLVM pass/fail/skip ledger was not recovered.** Reporting shelf presence as build success would be incorrect. Likewise, 6,770 repository RPM identities cannot be used as a build denominator. Current full-image pass/fail/skip totals and failure-category counts are unknown.

## Full label-universe table

To obey the ~400-line limit, the requested `build_status.csv` is the first part of one table. Read the union of these three files with the identical schema:

- [build_status.csv](../artifacts/build_status.csv): first 330 labels.
- [build_status-part-02.csv](../artifacts/build_status-part-02.csv): next 330 labels.
- [build_status-part-03.csv](../artifacts/build_status-part-03.csv): final 282 labels.

All 942 labels are retained. Current result cells are **Unknown**, rather than fabricated. Historical evidence, including historical Build OK claims, is preserved in the complete [historical tracker](../artifacts/historical-tracker/README.md). The [scoped build results](../artifacts/scoped-build-results.csv) separately records actual candidate/bootstrap results with their exact scope; these do not fill a current production-image matrix.

## Failure taxonomy for reconciliation

| Category | Current count | Representative retained evidence / next qualification |
|---|---|---|
| New diagnostics / Werror | Unknown | Historical per-package tracker; compare exact compiler invocation and log |
| GNU extensions / nested functions / VLAIS | Unknown | No current representative failure qualified in this round |
| Assembly / constraints / instruction mode | Unknown | dali-core CL14451023; libjxl CL14157988; distinguish runtime UB from build failure |
| Common symbols / symbol visibility | Unknown | key-manager CL14272968 export specialization |
| C++ ABI / ODR across DSO | Unknown | bluetooth-host-impl CL14392070; aul-1/coba layouts; historical cases, not current failure count |
| Versioned exports / linker dependencies | Unknown | cryptsetup CL14248929; broadcastapp-util CL14366057 |
| LTO / native PIC route | Unknown | 18 expected **synthetic** negative probes, not 18 package failures |
| Configure / macro compatibility | Unknown | 10.1 helper `rpm --load` and authentication issues were probe infrastructure stops; do not label compiler regressions |
| Flags propagation / compiler bypass | Unknown | AVControl inherited CXXFLAGS candidate; tvs-tpms-base flags |
| Test-suite failures | Unknown | No complete current product test log set available |

[Verified](../artifacts/evidence/llvm101-bootstrap.txt): bootstrap configure-probe exit1 is retained with a configure marker; subsequent full build exit0 and RPMs are recorded. Preserve both rather than flattening the whole bootstrap to either failure or unconditional release success.

[Assumption/Memory: proposed follow-up] Reconcile build service logs and source/RPM identities on the pinned configuration, then replace unknown entries with result, compiler command, job ID, failure signature and tested fix. This handover deliberately does not launch that collection or rebuild packages.
