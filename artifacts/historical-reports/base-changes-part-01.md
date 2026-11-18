# Tizen Base Changes: Summary (up to 2026-10-30)

> Scope: every change made to the LLVM Base (OBS project `Tizen:10.0:Base:Dev:LLVM`) and to the build configuration while moving the VD product (armv7l) from GCC to LLVM; the items evaluated and deliberately left unchanged; and the open items.
> Product-package changes all have shelve CLs (see "Change Evaluation List"); Base changes have none, so this file carries the patch of every OBS commit in Appendix A, for review one by one.
> The list comes from the OBS commit history: the revision history of all 447 packages of the project was checked. The 12 packages with commits since 2026-09-01 (16 commits) are in 2.1 (plus one comment-only commit each for gdb and vdcoreclr-diagnostics on 10-30, see Appendix A.2 and A.3); the 4 commits made when the project was set up (before 09-01) and the project config are in 2.2. Compared with `Tizen:10.0:Base` the project has one package more (clang-contrib) and none less.

---

## 1. Principles

1. Every package is built with LLVM except those that can only be built with GCC (such as glibc, binutils), in Base as in the product packages.
2. A problem whose root cause is in Base is fixed in Base, not worked around in each affected package.
3. A Base change is first verified locally under the Quickbuild conditions (Clang and GCC), then submitted to OBS for a new snapshot, and only then discussed with the owner for merging.
4. Compile and link options have the same effect as on the GCC line; problems that the GCC line hides with options are not hidden on the LLVM line.
5. When a Base root fix takes long, the affected packages first get a temporary solution so that Quickbuild can run; the root fix continues in parallel.

---

## 2. All Base changes (by commit date)

### 2.1 Commits since 2026-09-01

"First snapshot" is derived from the commit date: the first LLVM Base snapshot after the commit.

| # | Package | OBS revision | Committed | Change | Reason / effect | First snapshot | Patch |
|---|---|---|---|---|---|---|---|
| 1 | elfutils | r2 | 09-21 | `baseregs[][2]` → `[][3]` in the i386 / x86_64 backends (two patch files) | Clang 22 `-Wunterminated-string-initialization`: a two-character string literal in a `[2]` array has no room for the terminating `\0`, an error under -Werror. One more byte per entry; the code reads only the first two characters, behaviour unchanged | 20260929.1 | Appendix A.1 |
| 2 | gdb | r2 (r3: comments only, 10-30) | 09-21 | `gdbsupport/enum-flags.h`: signedness from `std::underlying_type`; `gdb/symtab.h`: `SEARCH_ALL_DOMAINS` built from the enumerators (two patch files) | Clang 22 makes the implicit int-to-enum conversion in a constant expression (`-Wenum-constexpr-conversion`) a hard error, so gdb 15.1 did not build (upstream report: GDB bug 31331). Same values as before | 20260929.1 | Appendix A.2 |
| 3 | vdcoreclr-diagnostics | r2 (r3: comments only, 10-30) | 09-21 | `dacprivate.h`, `disasm.h`: `memset` / `ZeroMemory` on objects of a non-trivial type take an explicit `void *` (two patch files) | Clang 22 `-Wnontrivial-memcall` (byte-wise zeroing of an object with non-trivial members), an error under -Werror. Same bytes zeroed | 20260929.1 | Appendix A.3 |
| 4 | binutils | r2 | 10-06 | the cross and native ld get `arm-none-eabi` in `--enable-targets` | trustzone-kldr is linked through Clang's BareMetal driver, which passes `-m armelf` to ld; the ld did not support that target | 20261010.1 | Appendix A.4 |
| 5 | binutils-armv7l | r2 | 10-10 | same (the ld that armv7l build roots use through qemu-accel) | same; the trustzone-kldr workaround shelve 14329022 was removed | 20261010.1 | Appendix A.5 |
| 6 | clang-contrib | r1 | 10-06 | new package: clang-force-options (forced clang options through clang.cfg at build time) | works with the hook of gcc-contrib r2. As agreed with HQ on 10-14, this set is for the public ASAN build and not for the regular image build; the clang_warning_force_options the regular build needs is an open item (section 6) | 20261010.1 | Appendix B |
| 7 | gcc-contrib | r2 | 10-06 | `%__spec_build_pre` of `macros.gcc_warning_force` gets `%{set_build_flags}` back and a `%{?clang_force_incompatible}` hook | Clang builds must receive the project's compile flags; the hook is for the forced-option layer of clang-contrib (empty when undefined). The LDFLAGS export was changed again in r3 | 20261010.1 | Appendix A.6 |
| 8 | llvm | r5 | 10-08 | clang sub-package `Requires: compiler-rt`, `libomp` | a build root with only clang cannot link `--coverage`, sanitizer or `-fopenmp` programs, so every package needed its own BuildRequires; 3 shelve CLs that only added `BuildRequires: libomp` were removed | 20261010.1 | Appendix A.7 |
| 9 | gcc-contrib | r3 | 10-09 | exports CFLAGS / CXXFLAGS / FFLAGS / FCFLAGS only, no longer LDFLAGS | the GCC product never exports LDFLAGS; 56 VD specs append with `LDFLAGS+="-Wl,..."` (no leading space), which with a preset LDFLAGS becomes `--hash-style=gnu-Wl,...` and every link fails | 20261010.1 | Appendix A.8 |
| 10 | llvm | r6 | 10-14 | `-D_FILE_OFFSET_BITS=64` in `clang.cfg` | Tizen GCC predefines the macro in cc1, so every GCC compile uses the 64-bit file API whatever the package does with CFLAGS; clang did not, and a package that drops the optflags was built against the 32-bit API (it broke the MIC signature check of cert-svc). Config-file options come before the command line, so a package that sets or undefines the macro still wins | 20261015.1 | Appendix A.9 |
| 11 | python3 | r2 | 10-19 | python3 and python3-base drop `%define _toolchain_override gcc` and use the project toolchain; `-marm` for Clang builds on ARM | "everything that can be built with LLVM is". `-marm` because the build runs the new interpreter under qemu user mode, and that qemu rejects the T32 STREXD/STLEXD encoding with Rt == Rt2 that Clang emits for 64-bit atomic stores (valid on real hardware); A32 has no such encoding. Removable once qemu accepts it | 20261020.1 | Appendix A.10 |
| 12 | unzip | r2 | 10-19 | `CC="$CC"` on the `make` command line | `unix/Makefile` hard-codes `CC = cc`, so the exported `$CC` was ignored and the package was always built by GCC. GCC builds unchanged, Clang builds now really use clang | 20261020.1 | Appendix A.11 |
| 13 | sdk-core | r2 | 10-24 | new LLVM 22 toolchain plug-in `llvm22.armel` for Tizen Studio; the rootstraps list `llvm 22` next to `gcc 14.2` | the 296 `tizen build-native` packages could only be built with the SDK's own GCC 14.2 (see "Tizen SDK Changes and Packages") | 20261024.1 | Appendix A.12 |
| 14 | sdk-core | r3 | 10-27 | the LLVM plug-in links with `-Wl,--build-id=sha1`; the debugger entry added | the SDK GCC is configured with `--enable-linker-build-id`, clang is not; Clang-built TPK binaries had no build-id, so crash reports and debuginfo did not match | 20261028.1 | Appendix A.13 |
| 15 | llvm | r7 | 10-27 | cmake `-DENABLE_LINKER_BUILD_ID=ON` | clang passes `--build-id` to the linker by default, as Tizen GCC does (`--enable-linker-build-id`); before, no Clang-built binary of the LLVM image had a build-id | 20261028.1 | Appendix A.14 |
| 16 | jsoncpp | r2 | 10-28 | `allocator.h`: the upstream C++20 fix backported (30170d6 / 1.9.5, #1478, #1709): no `volatile` on the parameter of `SecureAllocator::deallocate`, reliable zero fill | the jsoncpp 1.9.2 header fails under C++20 with GCC (`-Wvolatile`) and Clang (`-Wdeprecated-volatile`); header-only, `libjsoncpp.so` unchanged, no ABI effect | 20261029.1 | Appendix A.15 |

### 2.2 Commits made when the project was set up (before 2026-09-01)

These commits precede the first LLVM Base snapshot 20260929.1, which Quickbuild uses from the start.

| # | Item | OBS revision | Committed | Account | Change | Reason / note | Patch |
|---|---|---|---|---|---|---|---|
| 1 | project config | r1 | 08-19 | boolwhee | The project config at creation. Compared with `Tizen:10.0:Base`: clang is the default toolchain (`%_toolchain`; a package can go back to gcc with `_toolchain_override`); clang and gcc each have their own optflags (clang `-Os -fstack-protector`, gcc unchanged `-O2 -fno-inline-functions -fstack-protector-strong`); clang-accel preinstalled for armv7l and the others; gcc / gcc-c++ moved from Required to Support, `Support: clang llvm-devel` and `Keep: clang llvm libllvm llvm-devel` added; link options no longer in Optflags but in `%build_ldflags`; `-D_FILE_OFFSET_BITS=64` in the armv7l / armv7hl Optflags | One project that builds with Clang or GCC, Clang by default | Appendix D |
| 2 | qemu_aggregate | r2 | 08-19 | boolwhee | The qemu of the build changed from `Tools-qemu5.2.x:20250521` to `Tools-qemu9.2.x:20250819` | No commit message | Appendix C.4 |
| 3 | llvm | r2 | 08-28 | sdk | Copied from `home:prj_admin:LLVM-22` (revision 41): LLVM 19.1.4 → 22.1.8, with the MLGO AOT models (armv7l / aarch64 / x86_64) and openmp.patch; in a Clang build llvm itself is built with clang (`_toolchain_override clang`) | The LLVM 22 toolchain enters the LLVM Base | Appendix C.1 |
| 4 | llvm | r3 | 08-31 | prj_admin | `QEMU_RESERVED_VA` of armv7l from 0x70000000 to 0x40000000 | Build error fix | Appendix C.2 |
| 5 | llvm | r4 | 08-31 | prj_admin | The `QEMU_RESERVED_VA` setting commented out; cmake gets `-DCMAKE_MAKE_PROGRAM=/usr/bin/ninja` | Build error fix | Appendix C.3 |

---

## 3. Build configuration (maintained by HQ)

The Clang build.conf used by Quickbuild (`TIZEN_KantSU2E_Clang_build.conf`) is maintained by HQ; changes are handed to HQ as CLs. The same conf is used for GCC (switched by `_toolchain`), so it must work for both.

| Date | Change | Reason | Status |
|---|---|---|---|
| 10-09 | `CCC_OVERRIDE_OPTIONS` and the global warning-suppressing options removed, only the necessary `-Wno-` kept | `CCC_OVERRIDE_OPTIONS` is a Clang debugging switch, not for production builds; global suppression hides each package's problems | Merged by HQ |
| 10-19 | Link options back in `__optflags` / `Optflags` as in the GCC conf; the 3 `%build_ldflags` removed | Same link-option coverage as the GCC line | Merged by HQ as @14368686; used by every local verification and Quickbuild since |

The project config of the OBS project itself has not changed since 2026-09-01; its difference from `Tizen:10.0:Base` is in Appendix D.

---

## 4. Base snapshot timeline

| Snapshot | Changes included (numbers of 2.1) | Used by Quickbuild |
|---|---|---|
| 20260929.1 | all of 2.2 (LLVM 22.1.8, project config, qemu); 1–3 of 2.1 (elfutils, gdb, vdcoreclr-diagnostics) | Starting Base |
| 20261010.1 | 4–9 (binutils, gcc-contrib r2/r3, clang-contrib, the clang dependencies) | Yes |
| 20261015.1 | 10 (`_FILE_OFFSET_BITS=64` in clang.cfg) | Round 13 |
| 20261020.1 | 11–12 (python3 and unzip built with Clang) | From round 14 |
| 20261024.1 | 13 (sdk-core LLVM plug-in) | 37221304, 37245097 |
| 20261028.1 | 14–15 (build-id for TPK and platform binaries) | 37271875, 37293671 |
| 20261029.1 | 16 (jsoncpp C++20 header fix) | 37318590 (current) |

---

## 5. Evaluated and deliberately not changed in Base

| Item | Conclusion | Reason |
|---|---|---|
| vdprelink | Stays on GCC for now | An earlier ruling. Under the rule "GCC only for what cannot be built with LLVM" it is to be re-confirmed (section 6) |
| Message about findutils missing from the Base environment | Not changed | Adding it only removes the message and solves nothing; the pre-install stage has similar messages |
| Option order (build.conf's `-Wno-unused-parameter -Wno-ignored-qualifiers` turned on again by the package's own later `-Wextra`) | Neither Clang nor build.conf changed; handled in the package | GCC gives an explicit `-Wno-X` priority, Clang takes the last one — a rule difference. Three common-layer routes were checked and none fits: trailing options in the Clang config file act only at link time; changing the Clang driver changes Clang's own rules and upstream will not accept it; `CCC_OVERRIDE_OPTIONS` is a debugging switch. So the package repeats the two options after `-Wextra` for Clang only, with exactly the GCC result |
| Symbol mismatch between abseil (Base) and protobuf / grpc / re2 (product) | No Base change | GCC 14 and Clang 22 mangle functions with an `enable_if` default template argument differently (from Clang 18 the new Itanium C++ ABI rule adds a `Tn...` part). It appears only in local fix builds, which take the GCC-built protobuf from the official product; Quickbuild rebuilds the product with Clang every round. GCC- and Clang-built C++ libraries cannot be mixed freely |
| The GCC-14-only `-Wno-error=...` of the GCC plug-in, not in the LLVM plug-in | Not added | The problems they would hide are fixed in the code |
| Relaxing the FORTIFY check in glibc (evaluated after the pisa-service crash) | Not changed | The scan of the whole tree found only 4 real problems, fixed one by one in the code; relaxing the check would also silence real overflows |

---

## 6. Open items, and items verified but not landed

| # | Item | Status | Next step |
|---|---|---|---|
| 1 | The jsoncpp header in the Tizen Studio rootstrap | Source found on 10-30: the rootstrap is produced at build time by the VD package sdk-rootstraps (`PLATFORM/SDK/tizenappci/tizensdk-rootstraps`). Its spec requires more than 700 -devel packages, jsoncpp-devel among them; `make_rootstrap.sh` packs the headers of the build root into `rootstraps.zip`, which is unpacked into Tizen Studio at install time (so these files belong to no rpm). The rootstrap headers therefore follow Base's jsoncpp-devel, and neither Base nor the rootstrap package needs another change. The old header seen in the local build root comes from the sdk-rootstraps of the 10-01 product repository, built with the old jsoncpp | Confirm that the sdk-rootstraps built by Quickbuild 37318590 (Base 20261029.1, which has jsoncpp r2) carries the new header; if so, remove the temporary Clang waiver from mcp-server CL 14401311 |
| 2 | Clang forced-option layer for the regular build | clang-contrib (item 6) is for the public ASAN build; the regular build needs a `clang_warning_force_options` modelled on `gcc_warning_force_options`, for both the regular and the ASAN build | Verify locally, then submit |
| 3 | rpm macro (tizen_macros) patch | Waiting for the patch | New LLVM Base snapshot once it arrives |
| 4 | Base packages still built with GCC | One systematic review needed | Move everything to LLVM except what can only be built with GCC; re-confirm vdprelink |
| 5 | `-marm` of python3 | Works around the instruction-encoding problem of the build service's qemu (section 2, item 11) | Remove once qemu is fixed |
| 6 | libmnl / libnetfilter_queue lose their exported symbols | Found earlier on an LLVM image: the `EXPORT_SYMBOL` macro puts the visibility attribute after the function definition, Clang ignores it (`-Wignored-attributes`), almost all exports are lost; the fix "attribute moved onto the definition" is verified on both packages | Landing on hold; confirm whether the current VD image has the same problem, and submit if so |
| 7 | lld as the default linker | A separate work line: plan to make lld clang's own default linker; builds still use GNU ld | Follows that line's plan |

---

## 7. Suggested for HQ

| Item | Reason |
|---|---|
| Merge the jsoncpp patch into `Tizen:10.0:Base` of the GCC line | The GCC side is the same 1.9.2 with the same C++20 problem; the patch is header-only with no ABI effect |
| Merge the elfutils, gdb, vdcoreclr-diagnostics and unzip patches into `Tizen:10.0:Base` | Source-level corrections that leave the GCC build unchanged; no second fix when Base moves to Clang |

---

## Appendix A　All patches (diffs between OBS revisions)

Each patch is the output of `osc rdiff -r N-1:N Tizen:10.0:Base:Dev:LLVM <package>`; A.2 and A.3 are the output of `-r 1:3` (r3 changes comments only).

### A.1 elfutils r2 (committed 09-21, from snapshot 20260929.1)

```diff
Index: elfutils.spec
===================================================================
--- elfutils.spec (revision 1)
+++ elfutils.spec (revision 2)
@@ -10,6 +10,8 @@
 Source:         elfutils-%{version}.tar.bz2
 Source2:        baselibs.conf
 Source1001:     elfutils.manifest
+Patch1:         fix-clang22-i386-baseregs.patch
+Patch2:         fix-clang22-x86-64-baseregs.patch
 Requires:       libdw libelf
 BuildRequires:  automake
 BuildRequires:  bison
@@ -90,6 +92,8 @@

 %prep
 %setup -q -n elfutils-%{version}
+%patch1 -p1
+%patch2 -p1
 cp %{SOURCE1001} .

 %build
Index: fix-clang22-i386-baseregs.patch
===================================================================
--- fix-clang22-i386-baseregs.patch (added)
+++ fix-clang22-i386-baseregs.patch (revision 2)
@@ -0,0 +1,13 @@
+diff --git a/backends/i386_regs.c b/backends/i386_regs.c
+index 7ec93bb9fc13..4bca1b1a24d7 100644
+--- a/backends/i386_regs.c
++++ b/backends/i386_regs.c
+@@ -83,7 +83,7 @@ i386_register_info (Ebl *ebl __attribute__ ((unused)),
+
+   switch (regno)
+     {
+-      static const char baseregs[][2] =
++      static const char baseregs[][3] =
+       {
+         "ax", "cx", "dx", "bx", "sp", "bp", "si", "di", "ip"
+       };
Index: fix-clang22-x86-64-baseregs.patch
===================================================================
--- fix-clang22-x86-64-baseregs.patch (added)
+++ fix-clang22-x86-64-baseregs.patch (revision 2)
@@ -0,0 +1,13 @@
+diff --git a/backends/x86_64_regs.c b/backends/x86_64_regs.c
+index ef987daf43f0..c92c862a58c8 100644
+--- a/backends/x86_64_regs.c
++++ b/backends/x86_64_regs.c
+@@ -80,7 +80,7 @@ x86_64_register_info (Ebl *ebl __attribute__ ((unused)),
+
+   switch (regno)
+     {
+-      static const char baseregs[][2] =
++      static const char baseregs[][3] =
+       {
+         "ax", "dx", "cx", "bx", "si", "di", "bp", "sp"
+       };
```

### A.2 gdb r2 + r3 (committed 09-21; r3 on 10-30 only rewrites the patch headers, no code change; from snapshot 20260929.1)

```diff
Index: gdb.spec
===================================================================
--- gdb.spec (revision 1)
+++ gdb.spec (revision 3)
@@ -28,6 +28,8 @@
 Source10:       gmp-6.2.1.tar.bz2
 Source11:       mpfr-4.2.0.tar.bz2
 Source1001:     gdb.manifest
+Patch1:         enum-flags.patch
+Patch2:         symtab.patch
 %define gdb_src gdb-%{version}
 %define gdb_build build-%{_target_platform}
 Requires:       python3
@@ -81,6 +83,8 @@

 %prep
 %setup -q
+%patch1 -p1
+%patch2 -p1
 cp %{SOURCE1001} .
 tar xf %{SOURCE10}
 ln -sf gmp-6.2.1 gmp
Index: enum-flags.patch
===================================================================
--- enum-flags.patch (added)
+++ enum-flags.patch (revision 3)
@@ -0,0 +1,22 @@
+gdb 15.1: build fix for Clang 22 - gdbsupport/enum-flags.h
+Clang 22 makes the implicit int-to-enum conversion in a constant expression (-Wenum-constexpr-conversion) a hard
+error, so the DIAGNOSTIC_IGNORE around it no longer helps (upstream report: GDB bug 31331).
+Fix: the signedness probe T (-1) < T (0) is replaced by std::is_signed of std::underlying_type<T>, which gives the
+same result without converting an int to the enum type.
+
+diff --git a/gdbsupport/enum-flags.h b/gdbsupport/enum-flags.h
+--- a/gdbsupport/enum-flags.h
++++ b/gdbsupport/enum-flags.h
+@@ -91,10 +91,8 @@
+ template<typename T>
+ struct enum_underlying_type
+ {
+-  DIAGNOSTIC_PUSH
+-  DIAGNOSTIC_IGNORE_ENUM_CONSTEXPR_CONVERSION
+   typedef typename
+-    integer_for_size<sizeof (T), static_cast<bool>(T (-1) < T (0))>::type
++    integer_for_size<sizeof (T),
++                   std::is_signed<typename std::underlying_type<T>::type>::value>::type
+     type;
+-  DIAGNOSTIC_POP
+ };
Index: symtab.patch
===================================================================
--- symtab.patch (added)
+++ symtab.patch (revision 3)
@@ -0,0 +1,25 @@
+gdb 15.1: build fix for Clang 22 - gdb/symtab.h
+Clang 22 rejects "(domain_search_flags) 0" in the constexpr SEARCH_ALL_DOMAINS: the conversion goes through the
+non-constexpr enum_flags constructor.
+Fix: the value is built from the domain_search_flag enumerators, starting from SEARCH_UNDEF_DOMAIN (== 0), and the
+enum_flags constant is constructed from that value, so no int-to-enum conversion is left. Same value as before.
+
+diff --git a/gdb/symtab.h b/gdb/symtab.h
+--- a/gdb/symtab.h
++++ b/gdb/symtab.h
+@@ -917,11 +917,12 @@
+ DEF_ENUM_FLAGS_TYPE (enum domain_search_flag, domain_search_flags);
+
+ /* A convenience constant to search for any symbol.  */
+-constexpr domain_search_flags SEARCH_ALL_DOMAINS
+-    = ((domain_search_flags) 0
++constexpr domain_search_flag SEARCH_ALL_DOMAINS_ENUM
++    = (domain_search_flag) (SEARCH_UNDEF_DOMAIN
+ #define SYM_DOMAIN(X) | SEARCH_ ## X ## _DOMAIN
+ #include "sym-domains.def"
+ #undef SYM_DOMAIN
+        );
++constexpr domain_search_flags SEARCH_ALL_DOMAINS = SEARCH_ALL_DOMAINS_ENUM;
+
+ /* A convenience define for "C-like" name lookups, matching variables,
+    types, and functions.  */
```

### A.3 vdcoreclr-diagnostics r2 + r3 (committed 09-21; r3 on 10-30 only removes marker comments; from snapshot 20260929.1)

```diff
Index: vdcoreclr-diagnostics.spec
===================================================================
--- vdcoreclr-diagnostics.spec (revision 1)
+++ vdcoreclr-diagnostics.spec (revision 3)
@@ -11,6 +11,8 @@
 License:       MIT
 URL:           http://github.com/dotnet/diagnostics
 Source0: %{name}-%{version}.tar.gz
+Patch1:         fix-clang22-disasm-nontrivial-memcall.patch
+Patch2:         fix-clang22-dacprivate-nontrivial-memcall.patch

 BuildRequires:  python
 BuildRequires:  pkgconfig(libunwind)
@@ -81,6 +83,8 @@

 %prep
 %setup -q -n %{name}-%{version}
+%patch1 -p1
+%patch2 -p1

 %ifarch %{arm} %{ix86} aarch64
 %ifarch %{arm} aarch64
Index: fix-clang22-dacprivate-nontrivial-memcall.patch
===================================================================
--- fix-clang22-dacprivate-nontrivial-memcall.patch (added)
+++ fix-clang22-dacprivate-nontrivial-memcall.patch (revision 3)
@@ -0,0 +1,13 @@
+diff --git a/src/inc/dacprivate.h b/src/inc/dacprivate.h
+index 80a616630d4a..e08df5f5e662 100644
+--- a/src/inc/dacprivate.h
++++ b/src/inc/dacprivate.h
+@@ -53,7 +53,7 @@ template <class T>
+ struct ZeroInit
+ {
+     ZeroInit()
+-    { memset(static_cast<T*>(this), 0, sizeof(T)); }
++    { memset((void*)static_cast<T*>(this), 0, sizeof(T)); }
+ };
+
+
Index: fix-clang22-disasm-nontrivial-memcall.patch
===================================================================
--- fix-clang22-disasm-nontrivial-memcall.patch (added)
+++ fix-clang22-disasm-nontrivial-memcall.patch (revision 3)
@@ -0,0 +1,13 @@
+diff --git a/src/SOS/Strike/disasm.h b/src/SOS/Strike/disasm.h
+index 2a2d9f7779fc..ebb552651af7 100644
+--- a/src/SOS/Strike/disasm.h
++++ b/src/SOS/Strike/disasm.h
+@@ -58,7 +58,7 @@ struct SOSEHInfo
+     UINT        EHCount;
+     CLRDATA_ADDRESS methodStart;
+
+-    SOSEHInfo()   { ZeroMemory(this, sizeof(SOSEHInfo)); }
++    SOSEHInfo()   { ZeroMemory((void*)this, sizeof(SOSEHInfo)); }
+     ~SOSEHInfo()  { if (m_pInfos) { delete [] m_pInfos; } }
+
+     void FormatForDisassembly(CLRDATA_ADDRESS offSet);
```

### A.4 binutils r2 (committed 10-06, from snapshot 20261010.1)

```diff
Index: binutils.spec
===================================================================
--- binutils.spec (revision 1)
+++ binutils.spec (revision 2)
@@ -147,11 +147,11 @@
        --build=%{_build} --host=%{_host} \
        --target=%{target_arch} \
 %{?cross: \
-       --enable-targets=%{target_arch} \
+       --enable-targets=%{target_arch},arm-none-eabi \
        --enable-64-bit-bfd \
 } \
 %{!?cross: \
