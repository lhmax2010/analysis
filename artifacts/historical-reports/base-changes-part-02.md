-       --enable-targets=aarch64-tizen-linux,armv7l-tizen-linux,armv7hl-tizen-linux,armv8l-tizen-linux,i686-tizen-linux,x86_64-tizen-linux,riscv64-tizen-linux \
+       --enable-targets=aarch64-tizen-linux,armv7l-tizen-linux,armv7hl-tizen-linux,armv8l-tizen-linux,i686-tizen-linux,x86_64-tizen-linux,riscv64-tizen-linux,arm-none-eabi \
 } \
        --enable-plugins \
 %ifnarch riscv64
```

### A.5 binutils-armv7l r2 (committed 10-10, from snapshot 20261010.1)

```diff
Index: binutils-armv7l.spec
===================================================================
--- binutils-armv7l.spec (revision 1)
+++ binutils-armv7l.spec (revision 2)
@@ -150,7 +150,7 @@
        --build=%{_build} --host=%{_host} \
        --target=%{target_arch} \
 %{?cross: \
-       --enable-targets=%{target_arch} \
+       --enable-targets=%{target_arch},arm-none-eabi \
        --enable-64-bit-bfd \
 } \
 %{!?cross: \
```

### A.6 gcc-contrib r2 (committed 10-06, from snapshot 20261010.1)

```diff
Index: macros.gcc_warning_force
===================================================================
--- macros.gcc_warning_force (revision 1)
+++ macros.gcc_warning_force (revision 2)
@@ -26,7 +26,9 @@

 %__spec_build_pre \
   %{___build_pre} \
+  %{set_build_flags}; \
   %{gcc_warning_incompatible} \
+  %{?clang_force_incompatible} \
 %{nil}

 %__spec_prep_pre \
```

### A.7 llvm r5 (committed 10-08, from snapshot 20261010.1)

```diff
Index: llvm.spec
===================================================================
--- llvm.spec (revision 4)
+++ llvm.spec (revision 5)
@@ -103,6 +103,11 @@
 Summary: Clang %{version} (C Language family frontend for LLVM)
 License: NCSA
 Requires: llvm = %{version}-%{release}
+# compiler-rt holds the clang runtimes (profile runtime for --coverage/-fprofile-arcs, builtins, sanitizers);
+# without it a chroot that only has clang cannot link instrumented binaries (TSYSTEM: analog-input-control-impl UT).
+Requires: compiler-rt = %{version}-%{release}
+# libomp is the OpenMP runtime clang links for -fopenmp; without it any -fopenmp package fails at link time.
+Requires: libomp = %{version}-%{release}
 Provides: libclang.so.%{version}

 %description -n clang
```

### A.8 gcc-contrib r3 (committed 10-09, from snapshot 20261010.1)

```diff
Index: macros.gcc_warning_force
===================================================================
--- macros.gcc_warning_force (revision 2)
+++ macros.gcc_warning_force (revision 3)
@@ -24,9 +24,17 @@
   }              \


+# r3 (2026-10-09): export CFLAGS/CXXFLAGS/FFLAGS/FCFLAGS the way rpm's %set_build_flags does, but NOT LDFLAGS.
+# The GCC product never exports LDFLAGS (its macros.gcc_warning_force has no set_build_flags at all), and
+# 56 VD specs append to it without a leading space ('LDFLAGS+="-Wl,..."'); with LDFLAGS pre-set that
+# becomes '--hash-style=gnu-Wl,...' and every link fails (QB b943: capi-tv-control, libmm-imgp-gstcs,
+# libnet-clock-vd, libav-common, vc-webview-js).
 %__spec_build_pre \
   %{___build_pre} \
-  %{set_build_flags}; \
+  CFLAGS="${CFLAGS:-%{?build_cflags}}" ; export CFLAGS ; \
+  CXXFLAGS="${CXXFLAGS:-%{?build_cxxflags}}" ; export CXXFLAGS ; \
+  FFLAGS="${FFLAGS:-%{?build_fflags}}" ; export FFLAGS ; \
+  FCFLAGS="${FCFLAGS:-%{?build_fflags}}" ; export FCFLAGS ; \
   %{gcc_warning_incompatible} \
   %{?clang_force_incompatible} \
 %{nil}
```

### A.9 llvm r6 (committed 10-14, from snapshot 20261015.1)

```diff
Index: llvm.spec
===================================================================
--- llvm.spec (revision 5)
+++ llvm.spec (revision 6)
@@ -379,9 +379,14 @@
 ln -sf clang %{buildroot}%{_prefix}/bin/%{_host}-clang
 ln -sf clang++ %{buildroot}%{_prefix}/bin/%{_host}-clang++
 # Use host triple and resource dir by default via <lang>.cfg
+# _FILE_OFFSET_BITS=64: Tizen gcc predefines it inside cc1, so every gcc compile uses the 64-bit file API whatever the
+# package does with $CFLAGS; clang gets the same default here. Config-file options come before the command line, so a
+# package that sets or undefines the macro itself still wins. Without this a package that drops the project optflags
+# is built against the 32-bit file API (cert-svc, MIC signature check, 2026-10).
 cat >> %{buildroot}/%{_prefix}/bin/clang.cfg << EOF
 -target %{_host}
 -resource-dir %{_prefix}/%{_lib}/clang/%{llvm_version}
+-D_FILE_OFFSET_BITS=64
 EOF
 ln -sf clang.cfg %{buildroot}/%{_prefix}/bin/clang++.cfg
```

### A.10 python3 r2 (committed 10-19, from snapshot 20261020.1)

```diff
Index: python3-base.spec
===================================================================
--- python3-base.spec (revision 1)
+++ python3-base.spec (revision 2)
@@ -229,7 +229,6 @@
 other applications.

 %prep
-%define _toolchain_override gcc
 %setup -q -n %{tarname}
 %{__patch} -p1 < %{SOURCE11}
 %{__patch} -p1 < %{SOURCE12}
@@ -261,6 +260,16 @@
 ### COMMON-PREP-END ###

 %build
+%if %{toolchain_is clang}
+%ifarch %{arm}
+# clang: compile in ARM (A32) mode. The build runs the freshly built interpreter under qemu user-mode emulation (OBS / gbs
+# qemu-accel), and that qemu rejects the T32 STREXD/STLEXD encoding with Rt == Rt2 which clang emits for 64-bit atomic stores
+# (SIGILL in _PyRecursiveMutex_Unlock). The encoding is valid on real hardware; A32 cannot express it, so the problem is
+# avoided at the cost of some code size. Remove once the qemu of the build service accepts it. GCC does not emit it.
+export CFLAGS="$CFLAGS -marm"
+export CXXFLAGS="$CXXFLAGS -marm"
+%endif
+%endif
 export CFLAGS+=" -w"
 export CXXFLAGS+=" -w"
 ### COMMON-CONFIG-BEGIN ###
Index: python3.spec
===================================================================
--- python3.spec (revision 1)
+++ python3.spec (revision 2)
@@ -141,7 +141,6 @@
 Console User Interface.

 %prep
-%define _toolchain_override gcc
 %setup -q -n %{tarname}
 %{__patch} -p1 < %{SOURCE11}
 %{__patch} -p1 < %{SOURCE12}
@@ -173,6 +172,16 @@
 ### COMMON-PREP-END ###

 %build
+%if %{toolchain_is clang}
+%ifarch %{arm}
+# clang: compile in ARM (A32) mode. The build runs the freshly built interpreter under qemu user-mode emulation (OBS / gbs
+# qemu-accel), and that qemu rejects the T32 STREXD/STLEXD encoding with Rt == Rt2 which clang emits for 64-bit atomic stores
+# (SIGILL in _PyRecursiveMutex_Unlock). The encoding is valid on real hardware; A32 cannot express it, so the problem is
+# avoided at the cost of some code size. Remove once the qemu of the build service accepts it. GCC does not emit it.
+export CFLAGS="$CFLAGS -marm"
+export CXXFLAGS="$CXXFLAGS -marm"
+%endif
+%endif
 ### COMMON-CONFIG-BEGIN ###
 # use rpm_opt_flags
 export OPT="%{optflags} -DOPENSSL_LOAD_CONF $(pkg-config --cflags-only-I libffi)"
```

### A.11 unzip r2 (committed 10-19, from snapshot 20261020.1)

```diff
Index: unzip.spec
===================================================================
--- unzip.spec (revision 1)
+++ unzip.spec (revision 2)
@@ -33,7 +33,10 @@

 %build
 export LDFLAGS+=" -Wl,-z,relro -pie "
-make %{?_smp_mflags} LOCAL_UNZIP=-DIZ_HAVE_UXUIDGID generic
+# unix/Makefile hard-codes "CC = cc" (and LD = $(CC)), so the compiler the build environment exports in $CC was
+# ignored and the package was always built with the system cc (GCC). Hand it over on the make command line:
+# GCC builds are unchanged ($CC is gcc there), Clang builds now use clang.
+make %{?_smp_mflags} CC="$CC" LOCAL_UNZIP=-DIZ_HAVE_UXUIDGID generic

 %install
 make PREFIX=%{buildroot}%{_prefix} MANDIR=%{buildroot}/%{_mandir}/man1 INSTALL="cp -p" install
```

### A.12 sdk-core r2 (committed 10-24, from snapshot 20261024.1)

```diff
Index: sdk-core.spec
===================================================================
--- sdk-core.spec (revision 1)
+++ sdk-core.spec (revision 2)
@@ -1872,6 +1872,37 @@
 rm -v -rf %{buildroot}%{_prefix}/.package-manager/install-log/package-manager/*
 rm -v -rf %{buildroot}%{_prefix}/package-manager/package-manager_cli_*.txt

+%ifarch %{arm}
+# LLVM toolchain for "tizen build-native -c llvm" (armel), PLEASE CHECK: the compiler is the platform's Clang (the compiler of
+# the Clang build of the platform); the binutils, the C++ library and the C runtime come from the GCC 14.2 toolchain of this SDK
+# (--gcc-toolchain, with --gcc-triple: the SDK GCC is installed for arm-tizen-linux-gnueabi), as the SDK's own llvm-10 plugin used the GCC 9.2 toolchain. GCC-14-only relaxations (-Wno-error=...) are
+# not copied: what they would hide is fixed in the code. The rootstrap plugins list llvm 22 next to gcc 14.2.
+SBIP=%{buildroot}%{_prefix}/tizen-studio/tools/smart-build-interface/plugins
+GTC=%{_prefix}/tizen-studio/tools/arm-linux-gnueabi-gcc-14.2
+cat > $SBIP/llvm22.armel.core.app.xml <<EOF_LLVM
+<extension point="toolchainDefinition">
+    <toolchain id="llvm22.armel" name="LLVM-22" architecture="armel" path="#{SBI_HOME}/../arm-linux-gnueabi-gcc-14.2" toolchainType="tizen.core">
+        <property key="COMPILER_MISCELLANEOUS_OPTION" value="--gcc-toolchain=$GTC --gcc-triple=arm-tizen-linux-gnueabi -fstack-protector-strong -Wno-comment -fcommon"/>
+        <property key="LINKER_MISCELLANEOUS_OPTION" value="--gcc-toolchain=$GTC --gcc-triple=arm-tizen-linux-gnueabi -Wl,-z,relro,--as-needed"/>
+        <property key="TOOLCHAIN_PREFIX" value="arm-linux-gnueabi-"/>
+        <tool name="c_compiler" version="clang 22" path="%{_bindir}/clang"/>
+        <tool name="c++_compiler" version="clang 22" path="%{_bindir}/clang++"/>
+        <tool name="assembler" version="GNU as (GNU Binutils) 2.43" path="#{SBI_HOME}/../arm-linux-gnueabi-gcc-14.2/bin/arm-linux-gnueabi-as"/>
+        <tool name="strip" version="GNU strip (GNU Binutils) 2.43" path="#{SBI_HOME}/../arm-linux-gnueabi-gcc-14.2/bin/arm-linux-gnueabi-strip"/>
+        <tool name="archiver" version="GNU ar (GNU Binutils) 2.43" path="#{SBI_HOME}/../arm-linux-gnueabi-gcc-14.2/bin/arm-linux-gnueabi-ar"/>
+        <tool name="make" path="/usr/bin/make"/>
+        <tool name="msgfmt" path="/usr/bin/msgfmt"/>
+        <tool name="binutils" path="#{SBI_HOME}/../arm-linux-gnueabi-gcc-14.2/bin"/>
+    </toolchain>
+</extension>
+EOF_LLVM
+for rs in $SBIP/*.core.xml; do
+  grep -q '<toolchain name="gcc" version="14.2"/>' $rs || continue
+  grep -q '<toolchain name="llvm"' $rs || sed -i 's|^\( *\)<toolchain name="gcc" version="14.2"/>|&\n\1<toolchain name="llvm" version="22"/>|' $rs
+done
+grep -H '<toolchain name=' $SBIP/*.core.xml
+%endif
+
 %post
 /sbin/ldconfig
```

### A.13 sdk-core r3 (committed 10-27, from snapshot 20261028.1)

```diff
Index: sdk-core.spec
===================================================================
--- sdk-core.spec (revision 2)
+++ sdk-core.spec (revision 3)
@@ -1877,16 +1877,19 @@
 # the Clang build of the platform); the binutils, the C++ library and the C runtime come from the GCC 14.2 toolchain of this SDK
 # (--gcc-toolchain, with --gcc-triple: the SDK GCC is installed for arm-tizen-linux-gnueabi), as the SDK's own llvm-10 plugin used the GCC 9.2 toolchain. GCC-14-only relaxations (-Wno-error=...) are
 # not copied: what they would hide is fixed in the code. The rootstrap plugins list llvm 22 next to gcc 14.2.
+# -Wl,--build-id=sha1 (10-27): the SDK GCC is configured with --enable-linker-build-id, clang is not - without it no Clang-built TPK
+# binary carries a build-id note (crash reports and debuginfo matching need it). The debugger entry is the one of the GCC plugin.
 SBIP=%{buildroot}%{_prefix}/tizen-studio/tools/smart-build-interface/plugins
 GTC=%{_prefix}/tizen-studio/tools/arm-linux-gnueabi-gcc-14.2
 cat > $SBIP/llvm22.armel.core.app.xml <<EOF_LLVM
 <extension point="toolchainDefinition">
     <toolchain id="llvm22.armel" name="LLVM-22" architecture="armel" path="#{SBI_HOME}/../arm-linux-gnueabi-gcc-14.2" toolchainType="tizen.core">
         <property key="COMPILER_MISCELLANEOUS_OPTION" value="--gcc-toolchain=$GTC --gcc-triple=arm-tizen-linux-gnueabi -fstack-protector-strong -Wno-comment -fcommon"/>
-        <property key="LINKER_MISCELLANEOUS_OPTION" value="--gcc-toolchain=$GTC --gcc-triple=arm-tizen-linux-gnueabi -Wl,-z,relro,--as-needed"/>
+        <property key="LINKER_MISCELLANEOUS_OPTION" value="--gcc-toolchain=$GTC --gcc-triple=arm-tizen-linux-gnueabi -Wl,--build-id=sha1 -Wl,-z,relro,--as-needed"/>
         <property key="TOOLCHAIN_PREFIX" value="arm-linux-gnueabi-"/>
         <tool name="c_compiler" version="clang 22" path="%{_bindir}/clang"/>
         <tool name="c++_compiler" version="clang 22" path="%{_bindir}/clang++"/>
+        <tool name="debugger" version="GNU gdb 15.1" path="#{SBI_HOME}/../arm-linux-gnueabi-gdb-15.1/bin/arm-linux-gnueabi-gdb"/>
         <tool name="assembler" version="GNU as (GNU Binutils) 2.43" path="#{SBI_HOME}/../arm-linux-gnueabi-gcc-14.2/bin/arm-linux-gnueabi-as"/>
         <tool name="strip" version="GNU strip (GNU Binutils) 2.43" path="#{SBI_HOME}/../arm-linux-gnueabi-gcc-14.2/bin/arm-linux-gnueabi-strip"/>
         <tool name="archiver" version="GNU ar (GNU Binutils) 2.43" path="#{SBI_HOME}/../arm-linux-gnueabi-gcc-14.2/bin/arm-linux-gnueabi-ar"/>
```

### A.14 llvm r7 (committed 10-27, from snapshot 20261028.1)

```diff
Index: llvm.spec
===================================================================
--- llvm.spec (revision 6)
+++ llvm.spec (revision 7)
@@ -177,6 +177,8 @@
 %endif
 %endif

+# -DENABLE_LINKER_BUILD_ID=ON (10-27, PLEASE CHECK): clang passes --build-id to the linker by default, as the Tizen GCC does
+# (--enable-linker-build-id); without it no Clang-built binary of the image has a build-id note (crash reports, debuginfo matching).
 %build
 %if 0%{llvm_release_build}
 # Not to build debug info
@@ -224,6 +226,7 @@
 mkdir -p build
 cd build
 cmake \
+    -DENABLE_LINKER_BUILD_ID=ON \
     -G Ninja \
        -DCMAKE_MAKE_PROGRAM=/usr/bin/ninja \
     -DTIZEN=1 \
```

### A.15 jsoncpp r2 (committed 10-28, from snapshot 20261029.1)

```diff
Index: jsoncpp.changes
===================================================================
--- jsoncpp.changes (revision 1)
+++ jsoncpp.changes (revision 2)
@@ -1,3 +1,8 @@
+* Wed Oct 28 2026 Hao Lin <hao.lin@samsung.com> - 1.9.2
+- allocator.h: the upstream C++20 fix of SecureAllocator::deallocate backported (30170d6 of 1.9.5, #1478, #1709): the
+  volatile-qualified parameter (deprecated in C++20: GCC -Wvolatile, Clang -Wdeprecated-volatile) is gone, the zero fill
+  is a byte fill through a volatile unsigned char * (memset_s where available). Header-only, no ABI change.
+
 * Sat Apr 05 2025 seadmin <deokyang.jin@samsung.com> - vbs-jsoncpp-20250405.143508
 - [COSMOS] https://vdcosmos-hub.sec.samsung.net/build/28173964

Index: jsoncpp.spec
===================================================================
--- jsoncpp.spec (revision 1)
+++ jsoncpp.spec (revision 2)
@@ -9,6 +9,8 @@
 License:    Public-domain or MIT
 URL:        https://github.com/open-source-parsers/jsoncpp
 Source0:    https://github.com/open-source-parsers/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
+# upstream C++20 fix of SecureAllocator::deallocate (30170d6 / #1478 / #1709) backported - see the patch header
+Patch0:     jsoncpp-1.9.2-c++20-deallocate-volatile.patch
 Source1:    baselibs.conf
 Source1001: jsoncpp.manifest

@@ -33,6 +35,7 @@

 %prep
 %setup -q -n %{name}-%{version}
+%patch0 -p1
 cp %{SOURCE1001} .

 %build
Index: jsoncpp-1.9.2-c++20-deallocate-volatile.patch
===================================================================
--- jsoncpp-1.9.2-c++20-deallocate-volatile.patch (added)
+++ jsoncpp-1.9.2-c++20-deallocate-volatile.patch (revision 2)
@@ -0,0 +1,52 @@
+jsoncpp 1.9.2: SecureAllocator::deallocate - the upstream C++20 fix, backported
+
+Upstream history of include/json/allocator.h (github.com/open-source-parsers/jsoncpp):
+- f8674c6 (2016-03-06, "allocator.h"): SecureAllocator added with "void deallocate(volatile pointer p, size_type n)", the comment
+  saying the volatile tag keeps the compiler from optimizing the zero fill away.
+- 30170d6 (2020-10-13, Christian Ledergerber, "Fix c++20 compilation problem for clang10 and fix potential bug due to compiler
