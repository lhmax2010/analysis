# Clang migration: change list for review, increment of 14 Nov 2026

As of 14 November 2026. This increment consolidates work after the 11 November increment, including late-11-November work and the 12–13 November backfill. It does not assert that all entries were implemented today.

The local documentation contains the 11 November evaluation/review increments and the final 13 November HQ decision tables, but no separate 12/13 November evaluation or review increment. Remote publication status has not been verified. Twenty product CLs recorded in the HQ tables and project memory are absent from both 11 November increments; they are included below. Two later shelves are added separately. The 986-row HQ table is retained as a historical baseline, not silently rewritten.

Evidence labels: **historical record** = carried from the existing report/log; **verified artifact/build** = supported by a supplied result or locally inspected artifact; **candidate** = not in the formal shelf list; **runtime pending** = no complete target acceptance evidence. A successful build does not establish ABI compatibility, performance or runtime stability.

## 1. Product shelves: 20 backfilled rows and two later shelves

The columns follow the previous review list. Rows 927–948 continue its product numbering; they are independent of the HQ four-table row numbers. REVIEW does not mean submitted or runtime-approved. Dates marked backfill identify the available evidence window, not a newly asserted P4 creation date.

| No | type | package | summary | review URL | rbs / sbs | Snapshot | TASK owner | Remark | Date |
|---|---|---|---|---|---|---|---|---|---|
| 927 | product | org.tizen.UsbSyncDisplay | CMake compiler selection; migration also exposed an errno declaration conflict. Use the build-selected compiler. Recover the exact errno diff before treating its source review as complete. Base CL 14262074. | shelve CL 14448681 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: not found under this name → Clang build (local, Quickbuild conditions): 9 ELF (all clang), .text 1048 KB. Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 928 | product | capi-mva-contextfw | CMake compiler selection. Use the build-selected compiler; the earlier script had falsely classified text inside a sed command as a build error. Base CL 13738558. | shelve CL 14448652 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: not found under this name → Clang build (local, Quickbuild conditions): 2 ELF (all clang), .text 40 KB. Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 929 | product | capi-stt-wrapper-tv | CMake compiler selection; a pointer printed with %x was reported. Use the build-selected compiler; use a pointer-compatible format rather than suppressing the diagnostic. Exact historical diff is not reproduced here. Base CL 14231451. | shelve CL 14448672 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: not found under this name → Clang build (local, Quickbuild conditions): 2 ELF (all clang), .text 84 KB. Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 930 | product | capi-va-policy-tv | CMake compiler selection. Use the build-selected compiler; distinguish actual compiler errors from error text inside shell commands. Base CL 14157547. | shelve CL 14448655 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: not found under this name → Clang build (local, Quickbuild conditions): 1 ELF (all clang), .text 38 KB. Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 931 | product | capi-voice-source-manager-tv | CMake compiler selection; an unused test variable was reported. Use the build-selected compiler. Source-cleanup details remain subject to the archived diff. Base CL 13738558. | shelve CL 14448674 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: not found under this name → Clang build (local, Quickbuild conditions): 2 ELF (all clang), .text 40 KB. Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 932 | product | SZDrv_tools | Makefile compiler selection. Propagate the selected CC/CXX through the package build rather than fixing the compiler name to GCC. Base CL 11438397. | shelve CL 14448692 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 2 ELF, .text 370 KB → Clang build (local, Quickbuild conditions): 2 ELF (all clang), .text 389 KB (+5.1%). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 933 | product | nvt-pba-interface | Makefile compiler selection. Propagate the selected CC/CXX; do not attribute the USB enumeration failure to this change without a controlled reproduction. Base CL 14268942. | shelve CL 14448696 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 1 ELF, .text 77 KB → Clang build (local, Quickbuild conditions): 1 ELF (all clang), .text 76 KB (-1.3%). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 934 | product | vdlinux-usb-modules | User-space USB-module package compiler selection. Propagate the selected compiler; this CL is not evidence that a USB -71 kernel enumeration failure is fixed. Base CL 14267825. | shelve CL 14448698 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 2 ELF, .text 1 KB → Clang build (local, Quickbuild conditions): 1 ELF (all clang), .text 1 KB (+0.0%) (ELF count differs: not all sub-packages in the local build; to be compared again on the image). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 935 | product | streaming-accelerator | Makefile compiler selection. Propagate selected CC/CXX, including the stage that produces the shipped binary. Base CL 13165389. | shelve CL 14448705 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 3 ELF, .text 525 KB → Clang build (local, Quickbuild conditions): 3 ELF (all clang), .text 516 KB (-1.7%). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 936 | product | feature-config-daemon | Compiler name fixed in a build script. Use the selected C++ compiler; analyse the recorded size increase separately. Base CL 13733507. | shelve CL 14448709 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 3 ELF, .text 182 KB → Clang build (local, Quickbuild conditions): 3 ELF (all clang), .text 213 KB (+17.0%). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 937 | product | mdnsresponder | Makefile compiler selection. Use the selected compiler; do not accept or reject the migration from size alone. Base CL 13747715. | shelve CL 14450591 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 3 ELF, .text 198 KB → Clang build (local, Quickbuild conditions): 3 ELF (all clang), .text 254 KB (+28.3%). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 938 | product | libav-common | FFmpeg configure/compiler selection. Pass the platform compiler through the package configure path; retain package-specific semantics. Base CL 14062264. | shelve CL 14450650 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 3 ELF, .text 5586 KB → Clang build (local, Quickbuild conditions): 3 ELF (all clang), .text 5547 KB (-0.7%). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 939 | product | gst-plugins-httpdemux | FFmpeg configure/compiler selection. Pass the selected compiler. Reconcile the differing ELF inventory before claiming size savings. Base CL 14085831. | shelve CL 14451112 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 5 ELF, .text 764 KB → Clang build (local, Quickbuild conditions): 3 ELF (all clang), .text 388 KB (-49.2%) (ELF count differs: not all sub-packages in the local build; to be compared again on the image). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 940 | product | luabind | bjam toolset selection. Follow the platform toolchain rather than forcing the GCC toolset. Base CL 12912787. | shelve CL 14452018 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 2 ELF, .text 328 KB → Clang build (local, Quickbuild conditions): 2 ELF (all clang), .text 275 KB (-16.2%). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 941 | product | soc-ir-interface | Makefile compiler selection. Follow the platform compiler; prioritise a controlled analysis of the recorded .text increase. Base CL 13688992. | shelve CL 14452133 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 2 ELF, .text 26 KB → Clang build (local, Quickbuild conditions): 2 ELF (all clang), .text 63 KB (+142.3%). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 942 | product | lib-ndp-pq-interface-tv | Recorded compiler adaptation; detailed archived diff not available in this reporting pass. Retain the existing shelf and recover its detailed diff before adding source-level claims. Base CL 14258004. | shelve CL 14452243 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 1 ELF, .text 79 KB → Clang build (local, Quickbuild conditions): 1 ELF (all clang), .text 89 KB (+12.7%). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 943 | product | soc_vendor-user-bins | Compiler adaptation and dropctr-related work; a GCC prebuilt remains in the package. Keep the prebuilt classification separate from source compilation. The pkt_Err reporting item remains open. Base CL 12927034. | shelve CL 14452503 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 7 ELF, .text 147 KB → Clang build (local, Quickbuild conditions): 7 ELF (6 clang, 1 GCC-only), .text 126 KB (-14.3%) (the GCC-only ELF is a prebuilt binary shipped from the source tree). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 944 | product | gst-plugins-dash | Compiler/FFmpeg adaptation and source fixes; supersedes 14452527. Recorded fixes: flag logical-AND to bitwise-AND, avoid 32-bit truncation of clock differences, and retain a fractional buffer target; FFmpeg warning ordering and upstream 2705c0bd81e7 are recorded separately. Base CL 14274649. | shelve CL 14452597 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 9 ELF, .text 3737 KB → Clang build (local, Quickbuild conditions): 5 ELF (all clang), .text 1866 KB (-50.1%) (ELF count differs: not all sub-packages in the local build; to be compared again on the image). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 945 | product | iotivity | SCons/compiler adaptation, AtomicHelper and callback signature. Recorded Clang std::atomic path and confirmCB_thread signature repair. Does not contain the later ResourceInitException lifetime repair. Base CL 12913071. | shelve CL 14452627 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 20 ELF, .text 2133 KB → Clang build (local, Quickbuild conditions): 20 ELF (all clang), .text 1750 KB (-18.0%). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 946 | product | org.tizen.webserver | Tizen.mk compiler selection and GCC-specific fcgi diagnostic options. Follow CC/CXX; keep GCC-only options out of Clang. Judge the final installed build, while retaining the known failed earlier build stage as an open build-script issue. Base CL 14131900. | shelve CL 14452802 | Historical HQ record: Build OK (Quickbuild conditions); runtime test pending. GCC image: 4 ELF, .text 1,691,076 B → Clang build (local, Quickbuild conditions): 4 ELF (all clang), .text 1,694,168 B (+0.2%); all binaries are -O0 in both builds (definitions.mk always adds DEBUG_FLAGS). Separate matched GCC verification not recovered here. | Historical local Quickbuild-condition build; current-image package contents not independently rechecked in this reporting pass. | Migration team | REVIEW; backfill | Late 11–12 Nov; documented 14 Nov |
| 947 | product | capi-multiprofile-tv | Repair callback/lifecycle mutex reentry; queue profile notifications and track subscribers. Retain previous build adaptations; base 14298993. | shelve CL 14457173; replaces 14337555 without overwriting it | Host reentry cases and ARM Clang builds passed; new-config targeted rebuild passed. Runtime/ordering regression remains open. | Product 20261114.1 repository contains the fix marker symbols; different-board smoke check only. | Migration team | REVIEW; shelved, not submitted | 13–14 Nov session |
| 948 | product | libtv-element / gst-plugins-atsc3 | Respect selected compiler; repair literal/macro spacing and ten pointer-format sites in Proidiom. Four files; base 14297461. | shelve CL 14459110 | ARM Clang 22.1.8 and GCC 14.2 full package builds passed; source/format checks passed. Runtime and changed address-log consumers pending. | Included in next-QB 932-entry list; not claimed present in Product 20261114.1. | Migration team | REVIEW; shelved, not submitted | 14 Nov |

### Product baseline alignment supplied by HQ

| No | type | package | summary | review URL | rbs / sbs | Snapshot | TASK owner | Remark | Date |
|---|---|---|---|---|---|---|---|---|---|
| HQ-P1 | product Base CL | prelinksh | Use submitted 14327923 instead of 13003472; empty TV prelink lists. | //TIZEN/[MAIN]/[TIZENPROD_Prj]/[INT]/PLATFORM/SYSTEM/Bootservice/prelinksh/...@14327923 | Local target package build passed; installed list files empty. Tool invocation with an empty target may remain. | Prepared for next image via noprelink Base list. | HQ / migration integration | Baseline alignment, not a new shelf | Adopted 14 Nov |

### Candidate deliberately excluded from the formal list

IoTivity ResourceInitException lifetime repair has no new CL. The first candidate added a string member and passed ARM builds, but was withheld for public layout/allocation changes. The new fixed-message-table candidate preserves class declarations and has host GCC/Clang/cross-DSO test evidence; it costs approximately 20.4 KiB per retained table. ARM Clang/GCC package builds now pass. Clang candidate versus Product: no removed exports or changed export contracts across eight libraries; NEEDED, SONAME and ARM flags match. liboc.so .bss adds 20,936 bytes, including the 20,928-byte message table; this is not measured PSS. GCC versus the Clang Product has export differences and is not a matched GCC before/after ABI test. ARM runtime/ABI checks remain open. Its tests do not repair or execute old inlined dangling what() bodies. Keep 14452627. See the [evaluation](Clang_Fix_Evaluation_Daily_Increment_1114.md).

## 2. Base: Tizen:10.0:Base:Dev:LLVM

| No | type | package | summary | review URL | rbs / sbs | Snapshot | TASK owner | Remark | Date |
|---|---|---|---|---|---|---|---|---|---|
| 29 (update) | base | llvm r9 | Non-PIC LTO fallback already evaluated in the previous increment; published snapshot is now recorded. | OBS llvm revision 9; see prior B.29 | Historical v6 source/tests remain in 11-Nov report; no new test-suite run claimed. Four-package PIC-removal experiment has no accepted outcome in this update. | Base 20261112.1; formal PIC shelves retained | Toolchain team | Snapshot/status update | Backfilled 14 Nov |
| 30 | base | llvm r10 | Default LLVMgold selection for eligible GNU-ld links; -O4-to-O3 LTO-command fix; remove the forced default-PIE-off spec setting. See B.30 for exact diffs, cause, boundaries and test coverage. | OBS llvm revision 10, package Tizen:10.0:Base:Dev:LLVM/llvm | New repository version inspected; full image compiler-driver/LTO/PIE behavior check remains pending. Product package clang/llvm 22.1.8-9.1 does not identify the OBS source revision by release number alone. | Base 20261113.1; used by Product 20261114.1 | Toolchain team | REVIEW; deployment and measured-effect status distinguished | 13–14 Nov |

### B.30 llvm r10: preserve LTO at GNU-ld links, handle -O4 and remove the forced non-PIE default

**Files changed:** `llvm.spec`; `clang/lib/Driver/ToolChains/Gnu.cpp`; `clang/lib/Frontend/CompilerInvocation.cpp`; driver tests `tizen-default-lto-plugin.c` and `lto.c`. The existing non-PIC LTO fallback remains applied through `Source1005`.

The revision contains three changes. They address different behaviors and must be reviewed separately: selecting LLVMgold when the final link omits `-flto`, accepting `-O4` while constructing the LTO link command, and removing the spec override that forced Linux default PIE off.

**1. Spec integration — exact r9-to-r10 diff**

```diff
--- spec-r9
+++ spec-r10
@@ -50,6 +50,8 @@
 Source1003: mlgo_aarch_model.tar.gz
 Source1004: mlgo_x86_model.tar.gz
 Source1005: lto-nonpic-in-pic-output-fallback.patch
+Source1006: driver-pass-llvmgold-to-gnu-ld-by-default.patch
+Source1007: driver-O4-as-O3-upstream-85e76ec53ae4.patch

 %{!?mlgo_build_jobs: %define mlgo_build_jobs 6}
 %{!?mlgo_verify_configure_only: %define mlgo_verify_configure_only 0}
@@ -168,6 +170,11 @@
 # Tizen: regular LTO fallback for modules compiled without -fPIC/-fPIE that are
 # linked into a shared object or PIE (llvm/lib/LTO/LTO.cpp, LTO.h + tests).
 patch -p1 --fuzz=0 < %{SOURCE1005}
+# Tizen: like gcc, hand LLVMgold to GNU ld by default so -flto objects get LTO even
+# without -flto on the link line (clang/lib/Driver/ToolChains/Gnu.cpp + test).
+patch -p1 --fuzz=0 < %{SOURCE1006}
+# Backport of upstream 85e76ec53ae4: -O4 counted as -O3 when building the LTO link command.
+patch -p1 --fuzz=0 < %{SOURCE1007}
 %if %{with mlgo}
 mkdir -p mlgo_verify_assets
 %ifarch armv7l
@@ -229,14 +236,8 @@

 mkdir -p build
 cd build
-# CLANG_DEFAULT_PIE_ON_LINUX=OFF: clang does not build PIE executables by default on linux-gnu targets, the same default as
-# the Tizen GCC. With the upstream default (ON) every executable built by clang is PIE; the prelink step of the image skips
-# PIE executables, its list becomes empty and prelink fails for the whole image, so no library of the LLVM image is prelinked
-# (about 14 MB more private dirty memory on the TV board than the GCC image). Packages that ask for -fPIE/-pie themselves,
-# sanitizer builds that need PIE and musl targets stay PIE: PLEASE CHECK
 cmake \
     -DENABLE_LINKER_BUILD_ID=ON \
-    -DCLANG_DEFAULT_PIE_ON_LINUX=OFF \
     -G Ninja \
        -DCMAKE_MAKE_PROGRAM=/usr/bin/ninja \
     -DTIZEN=1 \
```

**2. Default LLVMgold selection — cause and implementation**

Some packages compile with `-flto -ffat-lto-objects` but use a custom final link command without `-flto`. The old driver called `addLTOOptions()` only when `D.isUsingLTO()` was true. On the GNU-ld path, the linker could then consume the fat object's native code without running LTO. A successful link did not establish that the embedded bitcode was optimized at link time. The compiler/LTO comparison report identified this pattern in packages such as wpasupplicant, libdbuspolicy and freetype2; those historical observations are not measurements of the new snapshot's improvement.

`driver-pass-llvmgold-to-gnu-ld-by-default.patch` adds a conditional default-plugin path:

```diff
--- a/clang/lib/Driver/ToolChains/Gnu.cpp
+++ b/clang/lib/Driver/ToolChains/Gnu.cpp
@@ -439,9 +439,30 @@

   ToolChain.AddFilePathLibArgs(Args, CmdArgs);

-  if (D.isUsingLTO())
+  if (D.isUsingLTO()) {
     addLTOOptions(ToolChain, Args, CmdArgs, Output, Inputs,
                   D.getLTOMode() == LTOK_Thin);
+  } else if (!Args.hasArg(options::OPT_flto, options::OPT_flto_EQ,
+                          options::OPT_fno_lto, options::OPT_r)) {
+    // Tizen local change: behave like the gcc driver, whose link spec hands
+    // its LTO plugin to the linker unless -fno-lto is given. Objects compiled
+    // with -flto (Tizen builds them with -ffat-lto-objects) then get LTO even
+    // when the package does not repeat -flto on its link line; without this
+    // the fat objects were linked silently as ordinary machine code. The
+    // plugin only claims LLVM bitcode, so other inputs link as before. Only
+    // for GNU ld / gold (lld reads bitcode itself) and only if LLVMgold.so is
+    // installed; never for -r, and not when the link line says -flto or
+    // -fno-lto (handled above / left alone).
+    bool LinkerIsLLD = false;
+    (void)ToolChain.GetLinkerPath(&LinkerIsLLD);
+    SmallString<1024> GoldPlugin;
+    llvm::sys::path::native(Twine(D.Dir) + "/../" CLANG_INSTALL_LIBDIR_BASENAME
+                                "/LLVMgold.so",
+                            GoldPlugin);
+    if (!LinkerIsLLD && D.getVFS().exists(GoldPlugin))
+      addLTOOptions(ToolChain, Args, CmdArgs, Output, Inputs,
+                    /*IsThinLTO=*/false);
+  }

   if (Args.hasArg(options::OPT_Z_Xlinker__no_demangle))
     CmdArgs.push_back("--no-demangle");
```

The explicit-LTO path remains first. Only when it is inactive does the new branch check for explicit LTO flags or a relocatable link, identify lld, and check whether `LLVMgold.so` exists relative to the driver installation. It then calls the existing LTO-option builder with full-LTO mode for the default path.

| Link condition | Behavior of the added path |
|---|---|
| GNU ld/gold, LLVMgold installed, no explicit LTO option, not `-r` | Pass LLVMgold so eligible LLVM bitcode can be claimed even when the package omits link-time `-flto`. |
| Explicit effective `-flto` / `-flto=thin` | Existing `D.isUsingLTO()` path handles the requested mode; the new branch does not add a second plugin. |
| LTO inactive and command contains `-fno-lto` | Do not auto-enable the plugin. The new branch does not override the package's explicit opt-out. |
| `-r` with no explicit effective LTO | Do not add the default plugin. This guard is on the new branch; it is not a change to every explicit-LTO relocatable link. |
| lld | Do not inject LLVMgold through the added path; lld has its own bitcode handling. |
| LLVMgold absent at the checked installation path | Do not inject a missing plugin through the added path. |
| Native-only input | Passing a plugin does not turn native machine code into bitcode or prove that LTO ran. |

This is a driver default, not removal of package `-fno-lto` exceptions or a global full-LTO policy change. It can make previously inactive LTO effective, so code size, link time, symbol binding and runtime behavior require artifact and target checks; the presence of `LLVMgold` in a command alone is not an LTO result.

**3. -O4 handling — cause and implementation**

The supplied backport records a failure in `getOptimizationLevel()`: `-O4` is a distinct option without the value expected by the generic `OPT_O` path. Constructing the LTO command could hit an assertion in an assertions-enabled build or access the missing value otherwise. Default plugin selection would expose this path to more GNU-ld links, so it is paired with the upstream-style fix mapping `-O4` to optimization level 3.

`driver-O4-as-O3-upstream-85e76ec53ae4.patch` contains the following production change and regression test:

```diff
diff --git a/clang/lib/Frontend/CompilerInvocation.cpp b/clang/lib/Frontend/CompilerInvocation.cpp
--- a/clang/lib/Frontend/CompilerInvocation.cpp
+++ b/clang/lib/Frontend/CompilerInvocation.cpp
@@ -2732,7 +2732,8 @@
     if (A->getOption().matches(options::OPT_O0))
       return 0;

-    if (A->getOption().matches(options::OPT_Ofast))
+    if (A->getOption().matches(options::OPT_Ofast) ||
+        A->getOption().matches(options::OPT_O4))
       return 3;

     assert(A->getOption().matches(options::OPT_O));
diff --git a/clang/test/Driver/lto.c b/clang/test/Driver/lto.c
--- a/clang/test/Driver/lto.c
+++ b/clang/test/Driver/lto.c
@@ -66,6 +66,8 @@
 // RUN:   -fuse-ld=lld -flto -O3 -### 2>&1 | FileCheck --check-prefix=O3 %s
 // RUN: %clang --target=x86_64-unknown-linux-gnu --sysroot=%S/Inputs/basic_cross_linux_tree %s \
 // RUN:   -fuse-ld=lld -flto -Ofast -### 2>&1 | FileCheck --check-prefix=O3 %s
+// RUN: %clang --target=x86_64-unknown-linux-gnu --sysroot=%S/Inputs/basic_cross_linux_tree %s \
+// RUN:   -fuse-ld=lld -flto -O4 -### 2>&1 | FileCheck --check-prefix=O3 %s

 // O1: -plugin-opt=O1
 // O2: -plugin-opt=O2
```

The change recognizes `OPT_O4` before the generic `OPT_O` assertion and produces level 3, like the existing `-Ofast` case in this function. It does not introduce an optimization level 4 or change ordinary `-O0`/`-O1`/`-O2`/`-O3` handling. The supplied patch identifies upstream commit `85e76ec53ae4e5caea5a13b084c19ba4e2f3a6ce` as its source.

**4. PIE default — meaning and impact**

The spec deletes `-DCLANG_DEFAULT_PIE_ON_LINUX=OFF` and its explanatory comment. The concrete change is removal of that forced build-time override. The driver's effective default still depends on the resulting build configuration, target defaults and invocation; the spec deletion alone is not a measurement of every executable's output type.

This affects executable-default policy separately from the LLVMgold fix. It must be considered alongside the HQ no-prelink configuration. Existing package PIC fixes remain valid. Do not restore the deleted override merely to reproduce an older prelink workflow, and do not attribute a historical memory estimate from the removed comment to this revision without a controlled measurement.

**Validation evidence and limits**

| Evidence | What it establishes |
|---|---|
| Fixed OBS r9/r10 spec and patch contents | The exact source changes above, including the often-missed removal of the PIE-off override. |
| Added `tizen-default-lto-plugin.c` test | Defines `-###`/FileCheck cases for default GNU-ld plugin selection on x86_64 and ARM shared links, one plugin with explicit `-flto`, `-O4` producing `-plugin-opt=O3`, and no default plugin for `-fno-lto`, `-flto -fno-lto`, `-r`, lld or missing LLVMgold. Its fixture creates a placeholder plugin file: this tests driver command construction, not execution of an LTO link. |
| Added `lto.c` case | Defines an explicit lld `-flto -O4 -###` regression case using the existing O3 expectations. Test source is present; a new execution result is not asserted here. |
| Published Base 20261113.1 metadata | Lists clang/llvm 22.1.8-9.1; Product 20261114.1 build.xml selects that Base. RPM release 9.1 is not the OBS source revision number and cannot identify r9 versus r10 by itself. |
| Remaining acceptance evidence | Confirm the shipped driver/plugin behavior, effective PIE output, actual LTO use by affected package links and target runtime/size effects. Neither package publication nor a successful image build proves these properties. |

Source review: [OBS LLVM package](http://168.219.245.220/package/show/Tizen:10.0:Base:Dev:LLVM/llvm). Published repository: [Base 20261113.1](http://repos.vd.sec.samsung.net/obs220/tizen-rsa/tizen-10.0-base-dev-llvm/standard/tizen-10.0-base-dev-llvm-standard_20261113.1/).

No new Base visibility, ThinLTO-default, inlining, MachineOutliner, lld or RELR optimization is claimed as delivered by this increment. Those are next-week candidates, subject to current-source and configuration checks.

## 3. build.conf

| No | type | package | summary | review URL | rbs / sbs | Snapshot | TASK owner | Remark | Date |
|---|---|---|---|---|---|---|---|---|---|
| C14-1 | build.conf | TIZEN_KantSU2E_Clang_build.conf | Submitted revision 12 / CL 14452507 removes five packages from lto_uncompatible_pkgs; previous revision 11 is 14431365. | //SHARED/[TizenBuild_Prj]/[INT]/buildconf/tizen/TEST/migration/10.0/TV/TIZEN_KantSU2E_Clang_build.conf@14452507 | ci-module, org.tizen.tv.swu, ug-hbbtv-efl, liballshare-core, nagsam-mw all build; multiprofile rebuilt too. HbbTV JavaScript/V8 retains local -fno-lto. | Local next-QB configuration; full new image pending. Already-built 20261114.1 still records 14431365. | HQ / migration integration | REVIEW; do not equate build success with effective whole-package LTO | Adopted 14 Nov |
| C14-2 | build.conf reference | TIZEN_KantSU2e_build.conf | HQ GCC baseline revision 3 / CL 14452502: remove five LTO exclusions and refresh platform/toolchain/architecture/feature settings. See C14-2 details below; this is not an LTO-only change. | //SHARED/[TizenBuild_Prj]/[INT]/buildconf/tizen/TEST/migration/10.0/TV/TIZEN_KantSU2e_build.conf@14452502 | GCC #2-to-#3 diff verified; Tizen minor0 to 1, GCC macros90 to 140, flag/dependency/product changes. Build.xml selects10.1 Base; no new GCC runtime/LTO acceptance claim. | Reference only for current LLVM 10.0 work | HQ | Reference, not a new local shelf | Inspected 14 Nov |

### C14-2 GCC build.conf: refresh the baseline and enable LTO eligibility for five packages

**File:** `//SHARED/[TizenBuild_Prj]/[INT]/buildconf/tizen/TEST/migration/10.0/TV/TIZEN_KantSU2e_build.conf`, revision `#2` to `#3`, submitted CL `14452502`. This is the GCC configuration; the Clang configuration has a separate path and CL `14452507`.

**Reason and scope.** HQ requests broader LTO support on the GCC baseline by revising `%lto_uncompatible_pkgs`. The supplied revision diff confirms that change, but also contains a substantial baseline refresh: Tizen version macros, GCC selection macros, architecture and compiler flags, build-root dependencies, warning-policy membership and product feature settings. Describing this CL as only a five-package LTO-list edit would omit changes that affect the build and invalidate a simple compiler-only comparison. The diff establishes those changes; it does not provide a separate owner rationale for every platform-feature choice.

**1. LTO eligibility — exact changed macro lines**

```diff
 # gcc lto (requested by hakbong5.lee)
 %_with_lto_full_build     1
 %_with_lto_partial_build  0
-%lto_uncompatible_pkgs    libtar acr ci-module gstreamer-atsc3-pvr-plugins libslive-dbus-proxy libslive-provider com.samsung.tv.slive-daemon tvs-parser tvs-udm acm-core tz-spassservice org.tizen.tv.swu com.samsung.tv.swu-ui ug-hbbtv-efl capi-appfw-app-context-manager capi-network-http isf iotivity pulseaudio com.samsung.tv.easysetup-client  gstreamer-plugins-muteplay gstreamer-plugins-smsrc vd-net-config liballshare-core context-aware-service tz-playservice dmp-manager libscl-ui-tv atsc3uhdcp marlin nagsam-mw nexguard tee_test_suite antimalware sdp secureime securestorage trustui-framework qte-bm gstreamer-plugins-tv avoc-daemon smart-deadlock org.tizen.RunningApps data-service-api logger webapi-antimalware-pepper-plugin webapi-contentsinfo-pepper-plugin tcmalloc resource-info data-provider-master libscreen_connector storaged rpc-port tts org.tizen.efreerdp isf libwidget_service logger libwidget_viewer com.samsung.ep-plateau-agent capi-ui-autofill ise-default-tv ug-ics-efl nettle libnettle libhogweed org.tizen.applist ug-rct alsa-lib com.samsung.audio.airplay-app com.samsung.tv.airplay-app-2
+%lto_uncompatible_pkgs    libtar acr gstreamer-atsc3-pvr-plugins libslive-dbus-proxy libslive-provider com.samsung.tv.slive-daemon tvs-parser tvs-udm acm-core tz-spassservice com.samsung.tv.swu-ui capi-appfw-app-context-manager capi-network-http isf iotivity pulseaudio com.samsung.tv.easysetup-client  gstreamer-plugins-muteplay gstreamer-plugins-smsrc vd-net-config context-aware-service tz-playservice dmp-manager libscl-ui-tv atsc3uhdcp marlin nexguard tee_test_suite antimalware sdp secureime securestorage trustui-framework qte-bm gstreamer-plugins-tv avoc-daemon smart-deadlock org.tizen.RunningApps data-service-api logger webapi-antimalware-pepper-plugin webapi-contentsinfo-pepper-plugin tcmalloc resource-info data-provider-master libscreen_connector storaged rpc-port tts org.tizen.efreerdp isf libwidget_service logger libwidget_viewer com.samsung.ep-plateau-agent capi-ui-autofill ise-default-tv ug-ics-efl nettle libnettle libhogweed org.tizen.applist ug-rct alsa-lib com.samsung.audio.airplay-app com.samsung.tv.airplay-app-2
```

The list removes exactly these five package names and adds none:

| Removed from `%lto_uncompatible_pkgs` | Configuration effect |
|---|---|
| `ci-module` | No longer excluded by this macro. |
| `org.tizen.tv.swu` | No longer excluded by this macro. |
| `ug-hbbtv-efl` | No longer excluded by this macro. |
| `liballshare-core` | No longer excluded by this macro. |
| `nagsam-mw` | No longer excluded by this macro. |

`%_with_lto_full_build` stays 1 and `%_with_lto_partial_build` stays 0. The displayed `%lto_armrel32_pkgs` and `%lto_pkgs` lines remain unchanged. Removing a package from one exclusion list makes it eligible through the common configuration; it does not prove that every compile/link stage actually uses LTO. Package-level flags and link commands still apply. In particular, the inspected HbbTV source explicitly retains `-fno-lto` for its JavaScript/V8 directory; this configuration change does not remove that local exception.

**2. Platform and GCC macros — exact excerpts**

```diff
@@ -49,7 +49,7 @@
 %release_name Tizen10/TV
 
 %tizen_version_major 10
-%tizen_version_minor 0
+%tizen_version_minor 1
 %tizen_version_patch 0
 
 %tizen_version %{tizen_version_major}.%{tizen_version_minor}
@@ -176,9 +176,9 @@
 
 ################################# build config #################################
 
-%define gcc_version 90
+%define gcc_version 140
 Macros:
-%gcc_version 90
+%gcc_version 140
 :Macros
 
 ################################### targets ####################################

```

The same diff changes the GCC feature define:

```diff
-%gcc_flag -DGCC90
+%gcc_flag -DGCC140
```

These macros update the configuration's platform/toolchain selection and any package conditionals that consume them. The actual compiler executable/version must still be checked in build output; a macro value alone is not binary compiler provenance. Although the depot path is under `migration/10.0`, the file now sets Tizen minor version 1.

**3. Compilation flags — exact excerpt**

```diff
@@ -359,13 +379,14 @@
 
 ############################## compilation flags ###############################
 
-%define __global_cflags -O2 -g2 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong -Wformat-security -Wformat -fmessage-length=0 -Wno-implicit-fallthrough -Wl,-z,relro,--as-needed
+%define __global_cflags -O2 -fno-inline-functions -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong -Wformat-security -Wformat -fmessage-length=0 -Wl,-z,relro,--as-needed
 
-Optflags: armv7l %{__global_cflags} --param=ssp-buffer-size=4 -mcpu=cortex-a53 -mtune=cortex-a53 -march=armv8-a+crc -mlittle-endian -mfpu=neon-vfpv4 -mfloat-abi=softfp -mthumb -Wp,-D__SOFTFP__ -Wl,-O1 -Wl,--hash-style=gnu -Wa,-mimplicit-it=thumb
+Optflags: armv7l %{__global_cflags} --param=ssp-buffer-size=4 -mtune=cortex-a53 -march=armv8-a+crc -mlittle-endian -mfpu=neon-vfpv4 -mfloat-abi=softfp -mthumb -Wp,-D__SOFTFP__ -Wl,-O1 -Wl,--hash-style=gnu -Wa,-mimplicit-it=thumb
 Optflags: armv7hl %{__global_cflags} --param=ssp-buffer-size=4 -mcpu=cortex-a53 -mtune=cortex-a53 -march=armv8-a+crc -mlittle-endian -mfpu=neon-vfpv4 -mfloat-abi=hard -mthumb -Wl,-O1 -Wl,--hash-style=gnu -Wa,-mimplicit-it=thumb
-Optflags: aarch64 %{__global_cflags} -feliminate-unused-debug-types -Wformat -march=armv8-a+fp+simd+crc+crypto -mtune=cortex-a57.cortex-a53
+Optflags: aarch64 %{__global_cflags} -feliminate-unused-debug-types -Wformat -march=armv8-a -Wl,-z,max-page-size=0x1000 -Wl,-O1 -Wl,--hash-style=gnu
 Optflags: i686 %{__global_cflags} -feliminate-unused-debug-types --param=ssp-buffer-size=4 -fdiagnostics-color=never -m32 -march=i686 -mtune=i686 -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables -fno-omit-frame-pointer -mstackrealign
-Optflags: x86_64 %{__global_cflags} -feliminate-unused-debug-types --param=ssp-buffer-size=4 -fdiagnostics-color=never -m64 -march=corei7 -msse4.2 -mtune=corei7-avx -mfpmath=sse -fasynchronous-unwind-tables -fno-omit-frame-pointer
+Optflags: x86_64 %{__global_cflags} -feliminate-unused-debug-types --param=ssp-buffer-size=4 -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables -fno-omit-frame-pointer
+Optflags: riscv64 %{__global_cflags} -feliminate-unused-debug-types -Wformat -mabi=lp64d -march=rv64gc -Wl,-O1 -Wl,--hash-style=gnu
 
 ###################### profile specific for normalization ######################

```

The global flag change adds `-fno-inline-functions` and `-gdwarf-4`, and removes `-Wno-implicit-fallthrough`, while retaining `-O2` and the shown hardening flags. The architecture lines also change: armv7l drops `-mcpu=cortex-a53` while keeping its explicit architecture/tuning/ABI options; aarch64 changes architecture/tuning selection and adds linker page-size/optimization/hash-style options; x86_64 changes its architecture/tuning selection; riscv64 gains its own ABI/ISA/linker flags. These are explicit configuration changes, not measured performance improvements. The shared global macro also affects architectures whose individual line is unchanged.

**4. Other changes present in the supplied revision diff**

| Area | Actual changes / review implication |
|---|---|
| riscv64 target and build support | Adds `Target: riscv64-tizen-linux`, includes riscv64 in the x86_64-host cross-build and speedpython conditions, adds qemu-accel preinstall/runscripts and Python/Clang accelerator substitutions, defines riscv64 speedpython requirements, and adds an RPM export filter. Architecture-conditional changes should not be described as an ARM-only LTO change. |
| Build-root dependency and ordering | Adds `libxcrypt` to Preinstall and declares `Order: sdk-rootstraps:sdk-core`. These affect build-root setup/ordering independently of the LTO list. |
| GCC warning policy | Adds onboot-aml/mtk/nvt/nxp/slsi to `%gcc_warning_kernel_pkgs` and refreshes the large opensource/SR/third-party package lists. Membership changes can affect which packages receive the associated policy; the supplied list diff alone is not a full expansion of warning flags. |
| Driver/product configuration | Changes `%_vd_cfg_driver_config` from 2025 to 2027. The commented product-year line also changes, but remains a comment. The configuration-item marker changes from 1.187.1 to 1.247.2. |
| Memory, filesystem and API settings | Sets optimized-memory to 1, rootfs type to erofs instead of vdfs, rootstrap API to 9.0 instead of 7.0, and adds kernel version 6.12. These are configuration values; runtime behavior requires their consuming code and resulting image. |
| Product features | Adds and changes multiple `%sec_buildconf_*` entries, including AI/color/style-transfer options, broadcast profiles, camera firmware, multicontrol, media streaming, security nagsam and sound support. These changes must remain visible as part of the baseline refresh, not be attributed to LTO or Clang. |

Selected feature-macro changes are reproduced below as **non-contiguous excerpts**; they are not a standalone applicable patch and do not enumerate the full feature list:

```diff
-%sec_buildconf_optimized_memory   0
+%sec_buildconf_optimized_memory   1
-%sec_buildconf_product_supported_rootfs_type   vdfs
+%sec_buildconf_product_supported_rootfs_type   erofs
-%sec_buildconf_rootstrap_api_version   7.0
+%sec_buildconf_rootstrap_api_version   9.0
+%sec_buildconf_kernel_version   6.12
-%sec_buildconf_multicontrol_support   1
-%sec_buildconf_multimedia_mediastreamer_supported   1
+%sec_buildconf_multicontrol_support   0
+%sec_buildconf_multimedia_mediastreamer_supported   0

```

**Validation evidence and comparison limits**

- The supplied `p4 diff2 -du` output directly compares GCC revisions `#2` and `#3`. It confirms the five removed LTO entries and the additional baseline changes above.
- The previously retrieved target configuration is submitted CL `14452502`, revision `#3`, with SHA256 `5e78db500271042c3d3d58c5f6933e6ef8365aaf1a039af45b9259bdbba20ba0`.
- HQ's GCC Product `TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261113.1` build.xml records this configuration and Base `tizen-10.1-base-standard_20260919.1`. This establishes the recorded build inputs, not full per-package LTO or runtime acceptance.
- The five targeted package builds already reported for the local LLVM environment used **Clang configuration `14452507`**. They are not new GCC package-validation results for this CL. Local GCC-override checks of ATSC3/IoTivity are also a different validation setup.
- GCC/LLVM image size or performance differences cannot be attributed solely to the compiler or the five LTO exclusions when Base, flags, filesystem/memory settings and product features differ. A controlled comparison must fix those conditions and verify the actual compile/link flags and artifacts.

**Local integration decision:** retain this file as the HQ GCC reference. The LLVM Quickbuild configuration remains `TIZEN_KantSU2E_Clang_build.conf@14452507`; do not copy the entire GCC refresh into it merely to reproduce the LTO-list change. Any further platform/feature alignment requires an explicit comparison of the corresponding LLVM settings.

## 4. Canonical inputs and publishing boundary

| Input | Current value / evidence |
|---|---|
| Base repository | `http://repos.vd.sec.samsung.net/obs220/tizen-rsa/tizen-10.0-base-dev-llvm/standard/tizen-10.0-base-dev-llvm-standard_20261113.1/` (r10 baseline) |
| Product repository used for current local dependencies | `http://repos.vd.sec.samsung.net/priv/168.219.246.243:81/PRV/builds/b259/19330259/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261114.1/` |
| Next-QB Base CL list | `/home1/chengkai/vd-tree/manifest/tizen10.0_base_urls_1114_noprelink.txt`; 2245 entries, no duplicate paths; SHA256 `bd5e81179eae1367b083fa77b701322b115e2214a862bf073e3063e8a04aa1f3` |
| Next-QB shelf list | `/home1/chengkai/vd-tree/manifest/tizen10.0_shelves_1114_atsc3.txt`; 932 entries, no duplicate paths; SHA256 `86bfbf724745a99914be5e991f7ae4caac015702cff657666428ef3a333e467c` |
| Next-QB Clang configuration | `/home1/chengkai/vd-tree/config/TIZEN_KantSU2E_Clang_14452507.conf`; SHA256 `98690f234ec8b79c728ae624f3ea91b12e6db5d918c70cfacb277d798dc95e03` |
| Important package entries | multiprofile `14457173`; ATSC3 `14459110`; IoTivity remains `14452627` |
| Already-built 20261114.1 image | Artifact `19330259`; its build.xml records build.conf **14431365**, not 14452507. The new configuration/ATSC3 shelf are prepared for the next image, not proven present in this one. |
| GCC validation configuration | Temporary GCC override using the existing build.conf mechanism and the same r10/Product dependencies; validation-only, not the formal QB configuration and not an exact reconstruction of the older GCC image. |

The 14-Nov documents are prepared locally. No upload to Confluence/GitHub and no P4 submit is asserted. Before merging into another master review list, reconcile report identifiers against that list; CL/path identities take precedence. One depot package path must have only one shelf entry.

Related: [detailed evaluation](Clang_Fix_Evaluation_Daily_Increment_1114.md), [weekly progress and plan](Weekly_Progress_and_Next_Plan_20261114.md), historical HQ decision table (original local reference: `HQ_Clang_Decision_Tables_1113.md`; not exported).
