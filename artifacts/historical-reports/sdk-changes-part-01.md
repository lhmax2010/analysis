# Tizen SDK (Tizen Studio) Changes and Packages: Summary (up to 2026-10-30)

> Scope: all the work to move the packages built by Tizen Studio in the product build (specs that produce a TPK with `tizen build-native`) to LLVM: the problem, the sdk-core change in Base, the spec change of each package, the handling of Clang errors, the verification, and the list of all packages with their CLs.
> The detection method and the per-package records are in "Packages Built by Tizen Studio — Detection, List and Progress", version 2 (10-28).

---

## 1. Problem

| Item | Situation |
|---|---|
| Packages | **296** of the 2244 packages of the product build call `tizen build-native` in their spec, all with `-c gcc` |
| Compiler actually used | Tizen Studio's own `arm-linux-gnueabi-gcc-14.2`, installed by Base's sdk-core package |
| Why LLVM was not possible | The SDK supports `-c llvm`, but sdk-core installed only the GCC 14.2 toolchain plug-in and the rootstrap listed only `gcc 14.2`; the internal SDK server only has LLVM 10.0 and older |
| Effect | ① the LLVM image is incomplete: the native code of these packages is still GCC-built, which skews the performance and size comparison of the GCC and LLVM images; ② mixing GCC- and Clang-built C++ libraries risks symbol mismatches; ③ the options of the Clang build.conf were passed as they are to the SDK GCC, mixing the options of two compilers |
| "Can only be built with GCC"? | No: the code can be built with Clang; only the LLVM toolchain of the SDK was missing |

Two ways of counting:

- **In the image**: image 20261027.1 has 65 RPMs built by Tizen Studio with native files compiled by the SDK GCC (230 files in total) — this is what the LLVM coverage of the image is measured on; list in 5.1.
- **The other 232**: also compiled by the SDK GCC, but not part of the image coverage — 203 `*-mapi` (gtest apps for the Managed API, installed on the TV by TOMATO, not in the product image) and 29 other packages; lists in 5.2 and 5.3.
- Note: 65 + 232 = 297, one more than 296, because one source package is counted on both sides: ta-sta2 produces the RPM com.samsung.tv.sta2, which is in the image (5.1, row 38), and the source package ta-sta2 is listed in 5.2 - both rows are the same CL 14383270.

---

## 2. Changes

### 2.1 Base: sdk-core (OBS `Tizen:10.0:Base:Dev:LLVM`)

| Revision | Change | Snapshot |
|---|---|---|
| r2 → 6.5.0-3.1 | New LLVM 22 toolchain plug-in `llvm22.armel`: the compiler is the platform's clang / clang++ 22 (the same compiler as for the other platform packages), with `--gcc-toolchain=/usr/tizen-studio/tools/arm-linux-gnueabi-gcc-14.2 --gcc-triple=arm-tizen-linux-gnueabi`, so the sysroot, C++ headers, as / ar / strip, the C++ library and the C run-time stay those of the SDK's GCC 14.2; compile options only the common `-fstack-protector-strong -Wno-comment -fcommon`; every rootstrap plug-in that lists `gcc 14.2` also lists `llvm 22` | 20261024.1 |
| r3 → 6.5.0-4.2 | The plug-in links with `--build-id=sha1` and gets the GDB tool entry, so TPK binaries carry `.note.gnu.build-id` like the rest of the platform | 20261028.1 |

The patches of both revisions are in "Tizen Base Changes", Appendix A.12 (r2) and A.13 (r3); the jsoncpp header fix is Appendix A.15.

Design choices:

- Not the LLVM 10 of the SDK server: too old, the same problem might have to be fixed twice; with the platform's Clang 22, the Clang fixes already made apply to the TPKs too.
- `--gcc-triple` is needed: the SDK's GCC 14.2 is installed as `arm-tizen-linux-gnueabi`, the platform clang targets `armv7l-tizen-linux-gnueabi`; with `--gcc-toolchain` alone, clang does not find the C++ standard headers.
- The GCC-14-only `-Wno-error=...` of the GCC plug-in are not carried over: the problems they would hide are fixed in the code.
- The GCC toolchain itself is unchanged.

### 2.2 The spec of each TPK package (one form for all)

```spec
# tizen build-native: LLVM (the Clang of the platform, through the LLVM plugin of sdk-core) when the package is built with
# the Clang toolchain, the SDK GCC 14.2 otherwise - PLEASE CHECK
%if "%{?_toolchain}" == "clang"
%define tpk_compiler llvm
%else
%define tpk_compiler gcc
%endif
...
tizen build-native -a arm -C Release -c %{tpk_compiler} -r tv-samsung-7.0-device.core ...   # was: -c gcc
```

`_toolchain` is a build.conf macro of Quickbuild / GBS (`clang` for Clang builds), so one spec works for both; GCC builds are not affected.

### 2.3 Directory permissions

The team has read-only access to the `//TIZEN_APP/.../[INT]` directories, so the CLs of the TPKs there are made on the identical `[FET]/[COSMOS]` directories (compared file by file: no difference from [INT] @ the base CL; HomeVersion is the exception and is built from the FET content). 47 lines of the Quickbuild base list switched from [INT] to [FET]/[COSMOS] accordingly.

---

## 3. Handling of Clang errors

### 3.1 Rules

- Change only the code, no `-Wno-*` / `-Wno-error` workarounds; every change carries a comment (what it was, why it changed) and PLEASE CHECK for the owner.
- Standard forms that do not change behaviour.
- A CL is made only after the Clang build passes, every TPK binary in the output is confirmed as built by clang 22.1.8, executables have a program interpreter and a GNU_RELRO segment, and — if code changed — a GCC build passes too.

### 3.2 Common error types and fixes

| Error type (Clang) | Fix |
|---|---|
| Link options inside the compile flags (`-Wl,-z,relro`, `-pie`), "argument unused" | Moved out of the compile flags |
| `-shared` in the link flags of an app project (GCC's driver lets `-pie` win; Clang's lets `-shared` win, the output dies with SIGILL at start) | `-shared` removed from the executable's link flags; GCC output unchanged |
| `-flto` only in the compile flags, not the link flags (including `*.prop.in` templates) | `-flto` added to the link flags (Clang's link line needs it to use LLVMgold); GCC output unchanged |
| `std::string` passed directly to a printf-like variadic function | `.c_str()` |
| Format and argument type mismatch; text used as the format (`-Wformat-security`); placeholder missing (`-Wformat-extra-args`); pointer printed with `%x` | Fix the format / `"%s"` / add the placeholder / `%p` |
| Variable-length arrays (including initialised ones, a GCC extension) | `std::vector` |
| Default argument repeated in a redeclaration; missing `override`; derived class hides a base overload | Moved to the first declaration; `override`; `using Base::f;` |
| `std::result_of`, `static_assert` without message, unqualified `move` | `invoke_result`, message added, `std::move` |
| class/struct forward declaration or header guard inconsistent | Made consistent with the definition |
| Callback pointer type does not match the API | Callback fixed to the API type or explicit cast, PLEASE CHECK |
| Unused constant / private member / internal function | Commented out; deletion is the owner's decision |
| Enum out of range in an embedded old Boost (hard error from Clang 16) | Boost upstream's fix |
| Third-party sub-project uses the build host's `/usr/include` | Removed (TPKs build against the SDK rootstrap) |
| Member template of a nested class uses non-static members of the outer class and is never instantiated (GCC does not check it without instantiation) | Dead code, `#if 0` with a note, PLEASE CHECK |
| `volatile` parameter of jsoncpp 1.9.2 in the rootstrap (C++20) | Header fixed in Base (jsoncpp r2). The rootstrap is produced at build time by the VD package sdk-rootstraps from jsoncpp-devel, so it follows Base; in the meantime mcp-server adds the Clang spelling of its existing GCC waiver |

### 3.3 Real bugs found on the way (fixed in the code, PLEASE CHECK)

| Package | Problem |
|---|---|
| mde-framework | Abstract class without a virtual destructor deleted through `unique_ptr`; member self-assignment |
| pisa-service | Wrong header guard; wrong `snprintf` size argument (crashed at boot on the LLVM image, see issue 9 of the stability report) |
| org.tizen.dseal | The same wrong `snprintf` size argument as pisa-service, in a copy of the same code (found by the whole-tree scan, fixed in advance on 10-30) |
| screenmirroring-app | Log format missing `%d` |
| voice-client | Null pointer passed to `%s` |
| easysetup-daemon, samsunghealth-service-tv, contentservicemanager, screenmirroring-app, etc. | `-shared` in the link flags of an executable (easysetup-daemon crashed 31 times on the image; the others were caught at build time) |

---

## 4. Verification

| Check | Result |
|---|---|
| First local run (10-24) | context-aware and accessory-mapi built with `-c llvm`; clang picks the SDK's GCC 14.2 installation, and the header search path, the libraries the linked output depends on and the CPU architecture attributes match g++; the GCC side passes its regression |
| File-by-file comparison of GCC and LLVM output | 195 ELF files; every difference is in the expected class: compiler string and build-id, code size, TPK signature xml, EXEC / DYN and 64-bit file interfaces (defaults of the platform Clang); NEEDED differences come from the `--as-needed` link order and do not affect run time; Clang's exports are a superset of GCC's (two complete-object constructors and one libstdc++ internal symbol more, harmless). Nothing needed a code or option change |
| Quickbuild 37271875 | 59 TPK packages built with LLVM |
| Quickbuild 37293671 | All 296 included; produced image 20261029.1 |
| Image 20261029.1 | easysetup-daemon 0 crashes (fix verified); the FORTIFY crash of pisa-service fixed (in 37318590) |
| Quickbuild 37318590 | Running (Base 20261029.1, with jsoncpp r2) |
| The 232 packages outside the image | Quickbuild can only check "built + ELF check of the output"; the run-time check needs TOMATO |

---

## 5. Packages and CLs (what each CL changes, for the review of each CL)

Progress: **all 296 packages done, each with a shelved CL**, all in the shelve list (891 lines). One row per package below, with what its CL changes.

Kinds of change:

| Kind | Meaning |
|---|---|
| spec only | Only the spec change of 2.2 (`-c gcc` → `-c %{tpk_compiler}`); no source or build file touched; 227 packages |
| build file | Besides the spec, build files changed (flags.mk, CMakeLists, `*.prop`; typically link options moved out of the compile flags, `-shared` removed from an executable, `-flto` added to the link flags) |
| code | Besides the spec, source changed in the forms of 3.2; every change commented in place and marked PLEASE CHECK |
| (real bug) | The change also fixes a real bug; the owner should know what it means for behaviour |
| temporary option | mcp-server only: removed once the rootstrap is confirmed to carry the new jsoncpp header |

"First Quickbuild" is the round that first built the CL; it stays in the list for every later round.

### 5.1 The 65 RPMs in the image

59 were verified in Quickbuild 37271875; 6 got their CL later (adagent, mde-framework, slive-daemon, pisa-service, targeted-ad-service, NetworkSetting-Tizen). NetworkSetting-Tizen mixes C# and native code; its native part (3 sub-projects) is switched as well.

| # | Package | CL | In the image | What changed | Kind of change | First Quickbuild |
|---|---|---|---|---|---|---|
| 1 | account-extra-service | 14395447 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 2 | canalysis-service | 14396811 | in the image (native files built by the SDK GCC before) | the bundled tiny-dnn / cereal: `::template apply` written as `::apply` (the only form Clang accepts) | code | 37271875 |
| 3 | cms-service | 14396973 | in the image (native files built by the SDK GCC before) | linker options removed from the compile flags; `std::result_of` → `std::invoke_result` (removed in C++20 mode) in the thread pool; std::string arguments as `.c_str()`; two unused constants commented out | code + build file | 37271875 |
| 4 | com.samsung.ep-plateau-agent-service | 14383261 | in the image (native files built by the SDK GCC before) | unused private fields ×2, missing `override` ×49 | code | 37219576 |
| 5 | com.samsung.rdm.b2b.general | 14395448 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 6 | com.samsung.rdm.tv.handler-sdm | 14396808 | in the image (native files built by the SDK GCC before) | unqualified `move` → `std::move`; `typeid` expression hoisted out of a potentially-evaluated context; a virtual destructor added to the abstract `SDMCommand` (deleted through a base pointer - a real bug) | code (real bug) | 37271875 |
| 7 | com.samsung.tizen.contextengine | 14391011 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37245097 |
| 8 | com.samsung.tizen.perception-engine | 14391012 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37245097 |
| 9 | com.samsung.tv.accf-service | 14395449 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 10 | com.samsung.tv.billing-helper | 14395450 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 11 | com.samsung.tv.bixby-context-client | 14395451 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 12 | com.samsung.tv.bixbycapsuleviewer | 14395453 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 13 | com.samsung.tv.bmp | 14395455 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 14 | com.samsung.tv.coba-aitech-native | 14391341 | in the image (native files built by the SDK GCC before) | CommonUtil.cpp: std::string passed to printf-style log calls → `.c_str()` (2 places; undefined behaviour before); spec switched to the LLVM plug-in | code | 37245097 |
| 15 | com.samsung.tv.coba-bluetooth-native | 14391346 | in the image (native files built by the SDK GCC before) | coba-component-capi.cpp: a pointer printed with `%u` → `%p`; a log call with an argument but no conversion for it → `%s` added; spec switched to the LLVM plug-in | code | 37245097 |
| 16 | com.samsung.tv.coba-multiscreen-native | 14391349 | in the image (native files built by the SDK GCC before) | EventManager.h: the `std::mutex` member locked in const methods made `mutable`; spec switched to the LLVM plug-in | code | 37245097 |
| 17 | com.samsung.tv.coba.adagent | 14397070 | in the image (native files built by the SDK GCC before) | linker options (`-Wl,-z,relro`, `-pie`) moved out of the compile flags; `override` added where a declaration overrides a virtual function; `using ComponentInterface::t_OnCommand;` keeps the base overloads visible next to an override | code + build file | 37293671 |
| 18 | com.samsung.tv.coba.homeversion | 14396721 | in the image (native files built by the SDK GCC before) | spec only. The exception: this FET directory differs from [INT] in 2 files; the hub builds the FET content @14350794 | spec only | 37271875 |
| 19 | com.samsung.tv.coba.mobilebff.native | 14391344 | in the image (native files built by the SDK GCC before) | MobileBFFStub.cpp: std::string passed to a printf-style log call → `.c_str()` (1 place); spec switched to the LLVM plug-in | code | 37245097 |
| 20 | com.samsung.tv.coba.native.epg | 14391005 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37245097 |
| 21 | com.samsung.tv.coba.nativesamsungaccount | 14396803 | in the image (native files built by the SDK GCC before) | AccountMenuItem.cpp:70: std::string passed to a printf-style function → `.c_str()`; spec switched to the LLVM plug-in | code | 37271875 |
| 22 | com.samsung.tv.coba.newhome.native | 14396804 | in the image (native files built by the SDK GCC before) | std::string arguments of printf-style calls as `.c_str()`; format specifiers matched to the argument types | code | 37271875 |
| 23 | com.samsung.tv.coba.usbcam.native | 14395456 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 24 | com.samsung.tv.contents-recognition-dbmgr | 14391006 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37245097 |
| 25 | com.samsung.tv.ContentsBrowser | 14396806 | in the image (native files built by the SDK GCC before) | std::string arguments of printf-style calls as `.c_str()`; a format mismatch; `"..."PRId64` literal concatenation | code | 37271875 |
| 26 | com.samsung.tv.contentservicemanager | 14396890 | in the image (native files built by the SDK GCC before) | callback types made to match their APIs (`g_timeout_add` callback returns gboolean, `vconf_notify_key_changed` callbacks return void); `static` removed from out-of-class member definitions; `-shared -Wl,--copy-dt-needed-entries` removed from the executable's link flags (the easysetup pattern) | code + build file (real bug, caught at build time) | 37271875 |
| 27 | com.samsung.tv.fuzzy-search-engine | 14396894 | in the image (native files built by the SDK GCC before) | the test runner's `using namespace ReportBuilder;` (a namespace and a class of the same name) written as an explicit namespace block | code | 37271875 |
| 28 | com.samsung.tv.ghdaemon | 14391013 | in the image (native files built by the SDK GCC before) | replaces the team CL 14298008 (its change kept): `-Xlinker -rpath-link=/usr/lib/hal:/usr/lib` in the link options of project_def.prop, so that indirect dependencies under the hal directory are found at link time; spec switched to the LLVM plug-in | build file | 37245097 |
| 29 | com.samsung.tv.ghservice | 14397000 | in the image (native files built by the SDK GCC before) | a default argument repeated on the constructor's definition moved to its declaration in the header | code | 37271875 |
| 30 | com.samsung.tv.home.apps | 14395457 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 31 | com.samsung.tv.home.mainhub | 14396805 | in the image (native files built by the SDK GCC before) | CategoryListManager.cpp:140, BixbyHandler.cpp:189 / 199: std::string passed to printf-style functions → `.c_str()` (3 places); spec switched to the LLVM plug-in | code | 37271875 |
| 32 | com.samsung.tv.iacr | 14395458 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 33 | com.samsung.tv.kmx-setting-app | 14395459 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 34 | com.samsung.tv.mde-framework | 14397100 | in the image (native files built by the SDK GCC before) | abstract classes deleted through `unique_ptr` got virtual destructors and a member self-assignment was fixed (real bugs); limits converted explicitly to the compared type; `friend struct` matching the definition; unused lambda captures removed; `-shared` removed from the test executables | code + build file (real bug) | 37293671 |
| 35 | com.samsung.tv.multiprofile-coba | 14395461 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 36 | com.samsung.tv.photo-analysis-datamgr | 14391007 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37245097 |
| 37 | com.samsung.tv.slive-daemon | 14397097 | in the image (native files built by the SDK GCC before) | `-shared` removed from the executables' link flags (the Clang output had no interpreter); pointer arguments cast to the parameter type (`void **`); format specifiers matched to the argument types (`%lld`) | code + build file (real bug, caught at build time) | 37293671 |
| 38 | com.samsung.tv.sta2 | 14383270 | in the image (native files built by the SDK GCC before) | linker options out of the compile flags; the Clang errors of the two DctSectionsHash headers fixed (`constexpr` initialised with a non-constant expression → `const`, same values); spec switched to the LLVM plug-in | code + build file | 37219576 |
| 39 | com.samsung.tv.subm-service | 14395462 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 40 | com.samsung.tv.targeted-ad-service | 14401447 | in the image (native files built by the SDK GCC before) | `-flto` added to the link options (the compile options ask for LTO; Clang needs it on the link line to use LLVMgold) | build file | 37293671 |
| 41 | com.samsung.tv.termsclient | 14396893 | in the image (native files built by the SDK GCC before) | a default argument repeated on the constructor's definition moved to its declaration in the header | code | 37271875 |
| 42 | com.samsung.tv.uem-client | 14395463 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 43 | com.samsung.tv.ug-res-mgr | 14391008 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37245097 |
| 44 | com.samsung.tv.utterance-recommender-service | 14392185 | in the image (native files built by the SDK GCC before) | 17 files. build_def.prop: `-Wl,-z,relro` taken out of the compile options (a linker option, USER_LINK_OPTS already has it; Clang rejects it on a compile line under -Werror); `-Wno-unknown-warning-option` in front of the GCC-only `-Wno-stringop-*` options. Code (all PLEASE CHECK): 4 methods overriding base methods marked `override`; a counter, 6 private fields and 2 constants defined and never read removed; 6 unqualified `move(hint)` calls written `std::move`; `StubIpcFactory` (virtual functions, no virtual destructor, deleted through `shared_ptr`) marked `final`; double literals (38.88, 122.88 ...) assigned to `int` in the gui: the implicit truncation made explicit with `static_cast<int>` (value unchanged — owner to decide whether rounding was intended) | code + build file | 37245097 |
| 45 | com.samsung.tv.vif | 14396809 | in the image (native files built by the SDK GCC before) | out-of-class definitions added for `static constexpr` members whose address is taken (undefined reference under C++14) | code | 37271875 |
| 46 | contextengine-plugin-smartthings | 14396920 | in the image (native files built by the SDK GCC before) | spec only (the earlier local failures came from a stale signing profile in the reused build environment, not from the code) | spec only | 37271875 |
| 47 | csft-service | 14396999 | in the image (native files built by the SDK GCC before) | linker options removed from the compile flags (every `Build/tizen_v*/.../flags.mk`); 4 variable-length arrays with initializers → `std::vector` (`.data()` where a pointer is needed); `std::result_of` → `std::invoke_result` | code + build file | 37271875 |
| 48 | mbr-downloadable-feature | 14395465 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 49 | multiprofile-service | 14396974 | in the image (native files built by the SDK GCC before) | linker options removed from the compile flags; a GCC-only `#pragma GCC diagnostic` group guarded by `#ifndef __clang__`; 7 unused lambda captures removed | code + build file | 37271875 |
| 50 | org.tizen.askuser-privacy-popup | 14395466 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 51 | org.tizen.dseal | 14395467 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); added on 10-30: in `src/service/SEALAuthChecker.cpp`, `snprintf(&mdString[i * 2], sizeof(mdString), …)` now passes the space left, `sizeof(mdString) - i * 2` (the same error as pisa-service; names and output unchanged; PLEASE CHECK) | spec + code (real bug) | 37271875; the 10-30 addition goes into the next round |
| 52 | org.tizen.easysetup-daemon | 14391347 | in the image (native files built by the SDK GCC before) | First LLVM build of this TPK. Its own `Build/flags.mk` (and `ut/Build/flags.mk`) links the executable with `-shared -pie`: GCC's driver lets `-pie` win (a PIE executable with interpreter), Clang's driver lets `-shared` win (a shared object: no interpreter, entry 0) - the kernel executed the ELF header. Fix: `-shared` removed from the executable's LINK_FLAGS (PLEASE CHECK). Clang output now a PIE executable with interpreter; the GCC output's `.text` is byte-for-byte identical to before | code + build file (real bug) | 37271875 |
| 53 | org.tizen.NetworkSetting-Tizen | 14401507 | in the image (native files built by the SDK GCC before) | mixed C# / native package: the 3 build-native sub-projects switched; linker options out of the compile flags; one std::string passed to a printf-style function → `.c_str()` | code | 37293671 |
| 54 | org.tizen.ScreenMirroring-app-tv | 14397044 | in the image (native files built by the SDK GCC before) | the bundled old Boost (libmm-common/include_embeded): `boost::integral_constant` instead of `mpl::integral_c` in numeric/conversion, the upstream Boost fix (mpl's `static_cast<enum>(value - 1)` is an out-of-range enum value and no constant expression any more); two `SM_ERROR` formats got their missing `%d`; a callback retyped to its API; `-shared` removed from the app's LINK_FLAGS (the easysetup pattern - the Clang output had no interpreter) | code + build file (real bug) | 37271875 |
| 55 | org.tizen.ssoservice | 14391345 | in the image (native files built by the SDK GCC before) | replaces the team CL 14298009 (its change kept): std::string passed to log calls → `.c_str()` in 3 sources (6 places); the initialised variable-length array of SSOSignatureProvider.cpp without the initializer (a memset below zeroes it); `-rpath-link=/usr/lib/hal:/usr/lib` in two project_def.prop; spec switched to the LLVM plug-in | code + build file | 37245097 |
| 56 | org.tizen.tts-engine-neural | 14396892 | in the image (native files built by the SDK GCC before) | `USER_LINK_OPTS=-z,relro` → `-Wl,-z,relro` (GCC passed `-z ,relro`, which ld silently ignored; Clang rejects the unknown argument) - the executables now really get GNU_RELRO | build file (real bug) | 37271875 |
| 57 | org.tizen.tts-resource | 14395468 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37271875 |
| 58 | org.tizen.voice-app | 14395469 | in the image (native files built by the SDK GCC before) | spec only, plus one icon file | spec only | 37271875 |
| 59 | org.tizen.voice-client | 14384878 | in the image (native files built by the SDK GCC before) | GCC: null pointer passed to `%s` (-Wformat-overflow). The message is printed only when command or result is null, i.e. exactly when `%s` gets NULL; now prints `"(null)"`, normal path unchanged | code (real bug) | 37219576 |
| 60 | pisa-service | 14398961 | in the image (native files built by the SDK GCC before) | many sub-projects: `std::result_of` → `std::invoke_result` (deprecated in C++17, an error under -Werror), unused private fields commented out, a mistyped header guard (real bug), format specifiers fitting both rootstraps | code (real bug) | 37293671 |
| 61 | samsunghealth-service-tv | 14396660 | in the image (native files built by the SDK GCC before) | the linker options `-Wl,-z,relro` / `-pie` removed from the compile flags (Clang: "argument unused" under -Werror); `-shared` removed from the executable's LINK_FLAGS (the easysetup pattern - the Clang output had no interpreter) | build file (real bug, caught at build time) | 37271875 |
| 62 | SmartControlService | 14391004 | in the image (native files built by the SDK GCC before) | replaces the team CL 14296679 (its change kept): the initialised variable-length array `char dest2[len + 1] = { "" }` in VirtualGamepadHandler.cpp declared without the initializer and zeroed by `memset`; spec switched to the LLVM plug-in | code | 37245097 |
| 63 | ug-unifiedauthentication-tv-native | 14391009 | in the image (native files built by the SDK GCC before) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37245097 |
| 64 | unifiedAuthenticationDN | 14391010 | in the image (native files built by the SDK GCC before) | replaces the team CL 14298176 (its change kept): the two authenticator CMakeLists.txt list the libraries the code really uses in their pkg-config dependencies (openssl3, capi-network-connection, capi-register-device, capi-system-info, capi-system-system-settings, system-type; one also capi-appfw-app-manager); spec switched to the LLVM plug-in | build file | 37245097 |
| 65 | vd-sc-client | 14396807 | in the image (native files built by the SDK GCC before) | a variable-length array with an initializer (not valid C++) rewritten | code | 37271875 |

### 5.2 The other 29 (not `*-mapi`)

ta-sta2 is the same source package and CL as com.samsung.tv.sta2 in 5.1.

| # | Package | CL | In the image | What changed | Kind of change | First Quickbuild |
|---|---|---|---|---|---|---|
| 1 | aifw-data-manager | 14399034 | in the image, native files already built by the platform LLVM | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 2 | aisound-app-engine | 14399632 | not in the image | spec only (replaces the earlier 14298307) | spec only | 37293671 |
| 3 | avsdk-lib-releaser | 14401393 | not in the image | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 4 | coba-component-verifier | 14399128 | not in the image | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 5 | coba-privacychoice | 14401395 | not in the image | linker options moved out of the compile flags (`Build/flags.mk`) | build file | 37293671 |
| 6 | com.samsung.tv.custom-picture-resource | 14401398 | not in the image | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 7 | context-aware-framework | 14386572 | in the image, native files already built by the platform LLVM | replaces 14383160. `%lu` printed the 64-bit `rlim_t` (2 sites, -Wformat): `%llu` + `(unsigned long long)` — the quick fix's `(unsigned long)` cast cut the value to 32 bits (`RLIM_INFINITY` printed as 4294967295). TPK: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (llvm when the package is built with the Clang toolchain, gcc otherwise); Clang build: all TPK objects compiled by clang 22.1.8 | code (real bug) | 37221304 |
| 8 | contextengine-plugin-perception | 14399135 | not in the image | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 9 | contextengine-plugin-systeminfo | 14400894 | in the image, no native ELF | `-flto` added to the link options | build file | 37293671 |
| 10 | contextengine-plugin-userdetection | 14399137 | in the image, no native ELF | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 11 | easysetup-mediator | 14401399 | not in the image | `-shared` removed from the executable's LINK_FLAGS (the easysetup-daemon pattern) | build file | 37293671 |
| 12 | globoplay-tpk | 14384479 | not in the image | function pointer cast to an incompatible type (-Wcast-function-type-strict) → small forwarding functions with the correct parameter types; the earlier option removed | code | 37219576 |
| 13 | LibAriaFW_TPK | 14399186 | not in the image | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 14 | manage-terms-platform-api | 14399191 | not in the image | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 15 | mcp-server | 14401311 | not in the image | `Server::~Server() noexcept {}` - the definition repeats the declaration's exception specification; `-flto` on the link line (cmake template `.prop.in` included); `-Wno-deprecated-volatile` next to the package's own `-Wno-error=volatile` - the Clang spelling of the same waiver, for the jsoncpp 1.9.2 header of the rootstrap (removed once Base has jsoncpp r2) | code + build file + temporary option | 37293671 |
| 16 | netflix-launcher | 14401400 | in the image, no native ELF | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 17 | sboard | 14371382 | in the image, native files already built by the platform LLVM | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | code | 37293671 |
| 18 | screen-analysis-dbmgr | 14399217 | not in the image | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 19 | ta-sta2 | 14383270 | not in the image | linker options out of the compile flags; the Clang errors of the two DctSectionsHash headers fixed (`constexpr` initialised with a non-constant expression → `const`, same values); spec switched to the LLVM plug-in | code + build file | 37219576 |
| 20 | tizen-actions | 14401012 | not in the image | `-flto` added to the link options; `struct Property;` matching the definition | code + build file | 37293671 |
| 21 | tizen-sandbox-runtime | 14399236 | not in the image | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 22 | tizen-tools | 14384480 | in the image, native files already built by the platform LLVM | incomplete type in a template: special members declared in `JsonValue` and defaulted after it (`std::pair<std::string, JsonValue>` no longer instantiated while JsonValue is incomplete); spec switched to the LLVM plug-in | code | 37219576 |
| 23 | tizensdk-simple-nativeapp | 14399365 | not in the image | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 24 | tvcamera-iot-service | 14401552 | not in the image | a variable-length array with an initializer (`int distance[len1 + 1][len2 + 1] = { 0, };`) → `std::vector` of the same name, every use unchanged; linker options moved out of the compile flags | code + build file | 37293671 |
| 25 | tvs-api | 14356149 | in the image, native files already built by the platform LLVM | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 26 | unified-drm | 14399384 | in the image, no native ELF | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 27 | vd-webapi | 14399392 | in the image, native files already built by the platform LLVM | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 28 | VisionAIRow_26 | 14401402 | not in the image | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 29 | webapi-avplay-xwalk-plugin | 14401616 | not in the image | 21 files in gst-plugins-dash / hls / subtitleparser: GLib callback casts (`GDestroyNotify`), pointer-type casts, a status text passed as the format of `g_error_new` → `"%s"`, `HLS_LOG` texts without the conversion for their argument, pointers printed with `%x` → `%p`; in dashplusplayer two never-instantiated member templates of a nested class that use the enclosing class's members without an object disabled (`#if 0`) with a note | code | 37293671 |

### 5.3 The 203 `*-mapi` packages

gtest apps for the Managed API, not in the product image; their run-time check is TOMATO.

| # | Package | CL | In the image | What changed | Kind of change | First Quickbuild |
|---|---|---|---|---|---|---|
| 1 | accessory-mapi | 14386718 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37221304 |
| 2 | acm-api-mapi | 14401403 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 3 | action-planner-api-mapi | 14399029 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 4 | adinfo-mapi | 14399030 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 5 | aifw-api-mapi | 14399031 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 6 | aifw-backend-mapi | 14399032 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 7 | aifw-core-mapi | 14399033 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 8 | ais-control-settings-mapi | 14399035 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 9 | aisound-app-api-mapi | 14399036 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 10 | aitech-api-mapi | 14400477 | not in the product image (TOMATO test app) | linker options out of the compile flags; `-shared` removed from the executable's LINK_FLAGS | build file | 37293671 |
| 11 | alarm-extension-tv-mapi | 14399038 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 12 | api-connection-mapi | 14399039 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 13 | api-p2p-legacy-mapi | 14399040 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 14 | api-rdm-handler-manager-mapi | 14399041 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 15 | api-rdm-handler-mapi | 14399042 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 16 | api-wifi-direct-mapi | 14399043 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 17 | api-wifi-mapi | 14399044 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 18 | app-core-extension-mapi | 14399047 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 19 | appbinarymanager-mapi | 14399046 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 20 | appdrm-mapi | 14399048 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 21 | apputil-mapi | 14399049 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 22 | audio-capture-mapi | 14399050 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 23 | audio-share-api-mapi | 14399052 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 24 | audiosync-api-mapi | 14399053 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 25 | aul-extension-mapi | 14399054 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 26 | autoInput-mapi | 14399055 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 27 | billing-api-internal-mapi | 14399056 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 28 | billing-api-mapi | 14399057 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 29 | bms-api-mapi | 14399058 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 30 | bnr-mapi | 14399059 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 31 | broadcast-time-mapi | 14399062 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 32 | broadcastapp-util-mapi | 14399061 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 33 | bt-settings-api-mapi | 14399063 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 34 | ca-api-mapi | 14399064 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 35 | capi-accf-tv-mapi | 14399065 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 36 | capi-ai-interpreter-tv-mapi | 14399066 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 37 | capi-android-utils-tv-mapi | 14399067 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 38 | capi-aov-tv-mapi | 14399068 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 39 | capi-appfw-app-operation-tv-mapi | 14399069 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 40 | capi-bmplayer-tv-mapi | 14399070 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 41 | capi-boost-tv-mapi | 14399071 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 42 | capi-bt-hfp-agent-tv-mapi | 14399072 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 43 | capi-bt-le-extended-tv-mapi | 14399074 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 44 | capi-cis-api-tv-mapi | 14399075 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 45 | capi-coba-core-tv-mapi | 14399077 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 46 | capi-csa-api-tv-mapi | 14399078 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 47 | capi-hdmi-infoframe-tv-mapi | 14399079 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 48 | capi-mde-framework-tv-mapi | 14399081 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 49 | capi-media-iot-player-tv-mapi | 14399084 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 50 | capi-minimusicplayer-tv-mapi | 14399085 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 51 | capi-multi-assistant-wrapper-tv-mapi | 14399088 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 52 | capi-multiprofile-tv-mapi | 14400496 | not in the product image (TOMATO test app) | linker options (`-Wl,-z,relro`, `-pie`) moved out of the compile flags | build file | 37293671 |
| 53 | capi-multiview-tv-mapi | 14399089 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 54 | capi-mva-tv-mapi | 14399090 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 55 | capi-network-bluetooth-tv-mapi | 14399091 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 56 | capi-parental-control-tv-mapi | 14399092 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 57 | capi-pisa-ipc-mapi | 14400498 | not in the product image (TOMATO test app) | linker options (`-Wl,-z,relro`, `-pie`) moved out of the compile flags | build file | 37293671 |
| 58 | capi-rm-video-capture-mapi | 14400479 | not in the product image (TOMATO test app) | `-shared` removed from the executable's LINK_FLAGS (the easysetup-daemon pattern) | build file | 37293671 |
| 59 | capi-screen-mapi | 14399094 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 60 | capi-screensaver-mapi | 14399096 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 61 | capi-sessiond-tv-mapi | 14399098 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 62 | capi-sound-sensor-tv-mapi | 14399099 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 63 | capi-sso-service-tv-mapi | 14400499 | not in the product image (TOMATO test app) | linker options (`-Wl,-z,relro`, `-pie`) moved out of the compile flags | build file | 37293671 |
| 64 | capi-stt-wrapper-tv-mapi | 14399101 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 65 | capi-sys-event-mapi | 14399102 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 66 | capi-system-display-rotator-mapi | 14399104 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 67 | capi-system-info-mapi | 14399105 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 68 | capi-system-input-key-mapi | 14399107 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 69 | capi-system-runtime-info-mapi | 14399109 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 70 | capi-system-sensor-mapi | 14401008 | not in the product image (TOMATO test app) | negative tests: an int passed as `sensor_type_e` → `static_cast<sensor_type_e>(-1)`, a string literal passed as `void *` user data → explicit cast (GCC `-fpermissive` converted both), two callbacks corrected to the API callback types | code | 37293671 |
| 71 | capi-system-system-settings-mapi | 14399110 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 72 | capi-system-usbdevice-mapi | 14399111 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 73 | capi-tim-service-tv-mapi | 14399112 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 74 | capi-trackrenderer-tv-mapi | 14400481 | not in the product image (TOMATO test app) | `-shared` removed from the executable's LINK_FLAGS (the easysetup-daemon pattern) | build file | 37293671 |
| 75 | capi-tts-wrapper-tv-mapi | 14399113 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 76 | capi-tvsensor-tv-mapi | 14399114 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 77 | capi-ui-config-manager-tv-mapi | 14399115 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 78 | capi-upgradable-webapi-tv-mapi | 14399116 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 79 | capi-utterance-recommender-tv-mapi | 14400501 | not in the product image (TOMATO test app) | unused constants / file-scope statics commented out (PLEASE CHECK, the owner deletes them) | code | 37293671 |
| 80 | capi-va-policy-tv-mapi | 14399117 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 81 | capi-vc-wrapper-tv-mapi | 14399118 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 82 | capi-vd-connectivity-data-mgr-tv-mapi | 14399120 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 83 | capi-voice-interaction-tv-mapi | 14399121 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 84 | capi-window-tv-mapi | 14399122 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 85 | cc-parser-mapi | 14399124 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 86 | chromium-efl-mapi | 14399125 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 87 | clearkey-mapi | 14399126 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 88 | com.samsung.tv.oobep-api-mapi | 14399129 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 89 | com.samsung.tv.slive-daemon-mapi | 14401009 | not in the product image (TOMATO test app) | std::string passed to a printf-style macro → `.c_str()`; format specifiers matched to the argument type (`%llu` for TCServiceId); an FCVirtualProgramId object passed to a printf-style function → its `GetServiceId()` cast | code | 37293671 |
| 90 | comss-api-mapi | 14399130 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 91 | content-db-api-mapi | 14399131 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 92 | content-service-framework-mapi | 14399132 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 93 | contents-recognition-api-mapi | 14399133 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 94 | context-aware-api-mapi | 14399134 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 95 | coreapp-fw-mapi | 14399138 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 96 | cryptocore-mapi | 14399139 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 97 | dapi-provider-mapi | 14399140 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 98 | data-service-api-mapi | 14399141 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 99 | dcm-mapi | 14399142 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
| 100 | deviced-mapi | 14399143 | not in the product image (TOMATO test app) | spec: `tizen build-native -c gcc` → `-c %{tpk_compiler}` (LLVM plug-in for Clang builds, GCC builds unchanged); no source change | spec only | 37293671 |
