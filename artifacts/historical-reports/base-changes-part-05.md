-PROJECT: //TIZEN/[MAIN]/[BASE2026_Prj]/[INT]/platform/upstream/llvm
-CHANGELIST: 13118253
\ No newline at end of file
Index: llvm-19.1.4.tar.gz
===================================================================
Binary files llvm-19.1.4.tar.gz (revision 1) deleted
Index: llvm.changes
===================================================================
--- llvm.changes (revision 1)
+++ llvm.changes (deleted)
@@ -1,9 +0,0 @@
-* Tue Sep 30 2025 vd_tizen_autosync <samjy.kim@samsung.com> - vbs-llvm-20250930.131421
-- [COSMOS] https://vdcosmos-hub.sec.samsung.net/build/31095544
-
-* Thu Jul 10 2025 vd_tizen_autosync <samjy.kim@samsung.com> - vbs-llvm-20250710.205040
-- [COSMOS] https://vdcosmos-hub.sec.samsung.net/build/29673608
-
-* Sun May 04 2025 vd_tizen_autosync <deokyang.jin@samsung.com> - vbs-llvm-20250504.102509
-- [COSMOS] https://vdcosmos-hub.sec.samsung.net/build/28620020
-
```

### C.2 llvm r3 (08-31)

```diff
Index: llvm.spec
===================================================================
--- llvm.spec (revision 2)
+++ llvm.spec (revision 3)
@@ -205,7 +205,7 @@
 %endif

 %ifarch armv7l
-export QEMU_RESERVED_VA=0x70000000
+export QEMU_RESERVED_VA=0x40000000
 %endif

 # Set up MLGO AOT model paths from bundled verify assets
```

### C.3 llvm r4 (08-31)

```diff
Index: llvm.spec
===================================================================
--- llvm.spec (revision 3)
+++ llvm.spec (revision 4)
@@ -204,9 +204,9 @@
 export LDFLAGS="$(filter_lto_flags $LDFLAGS)"
 %endif

-%ifarch armv7l
-export QEMU_RESERVED_VA=0x40000000
-%endif
+#%ifarch armv7l
+#export QEMU_RESERVED_VA=0x70000000
+#%endif

 # Set up MLGO AOT model paths from bundled verify assets
 %if %{with mlgo}
@@ -220,6 +220,7 @@
 cd build
 cmake \
     -G Ninja \
+       -DCMAKE_MAKE_PROGRAM=/usr/bin/ninja \
     -DTIZEN=1 \
     -DCMAKE_C_COMPILER=%__cc \
     -DCMAKE_CXX_COMPILER=%__cxx \
```

### C.4 qemu_aggregate r2 (08-19)

```diff
Index: _aggregate
===================================================================
--- _aggregate (revision 1)
+++ _aggregate (revision 2)
@@ -1,11 +1,11 @@
 <aggregatelist>
-  <aggregate project="Tools-qemu5.2.x:20250521">
+  <aggregate project="Tools-qemu9.2.x:20250819">
     <package>qemu</package>
     <binary>qemu-tools</binary>
     <repository source="standard" target="standard"/>
     <repository source="standard" target="emulator"/>
   </aggregate>
-  <aggregate project="Tools-qemu5.2.x:20250521">
+  <aggregate project="Tools-qemu9.2.x:20250819">
     <package>qemu-linux-user</package>
     <binary>qemu-linux-user-cross</binary>
     <binary>qemu-linux-user-x86-cross</binary>
```

## Appendix D　Project config: `Tizen:10.0:Base` against `Tizen:10.0:Base:Dev:LLVM`

```diff
--- Tizen:10.0:Base/_config
+++ Tizen:10.0:Base:Dev:LLVM/_config
@@ -100,6 +100,65 @@
 %gcc_version 140
 :Macros

+
+########## compilers and utils ##########
+
+%ifarch armv7l armv7hl
+Macros:
+%___optflags_toolchain_gcc --param=ssp-buffer-size=4
+:Macros
+%endif
+%ifarch aarch64 riscv64
+Macros:
+%___optflags_toolchain_gcc -feliminate-unused-debug-types
+:Macros
+%endif
+%ifarch i686 x86_64
+Macros:
+%___optflags_toolchain_gcc --param=ssp-buffer-size=4 -feliminate-unused-debug-types
+%___optflags_toolchain_clang -momit-leaf-frame-pointer
+:Macros
+%endif
+
+Macros:
+# clang utils
+%__ar_clang llvm-ar
+%__ranlib_clang llvm-ranlib
+%__cc_clang %{_host}-clang
+%__cxx_clang %{_host}-clang++
+%__optflags_toolchain_clang -Os -fstack-protector -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument %{?___optflags_toolchain_clang:%{___optflags_toolchain_clang}}
+
+# gcc utils
+%__ar_gcc gcc-ar
+%__ranlib_gcc gcc-ranlib
+%__cc_gcc %{_host}-gcc
+%__cxx_gcc %{_host}-g++
+%__optflags_toolchain_gcc -O2 -fno-inline-functions -fstack-protector-strong %{?___optflags_toolchain_gcc:%{___optflags_toolchain_gcc}}
+
+%_toolchain %{?_toolchain_override}%{!?_toolchain_override:clang}
+%toolchain_is() %((echo "%_toolchain" | %{__grep} -qE "%{1}") && echo 1 || echo 0)
+
+%__ar %{expand:%%{__ar_%{_toolchain}}}
+%__ranlib %{expand:%%{__ranlib_%{_toolchain}}}
+%__cc %{expand:%%{__cc_%{_toolchain}}}
+%__cxx %{expand:%%{__cxx_%{_toolchain}}}
+%__optflags_toolchain %{expand:%%{__optflags_toolchain_%{_toolchain}}}
+
+%prep %%prep\
+export AR=%{__ar} RANLIB=%{__ranlib};\
+%{nil}
+
+%build %%build\
+export AR=%{__ar} RANLIB=%{__ranlib};\
+export CC=%{__cc} CXX=%{__cxx};\
+%{nil}
+
+%install %{?_enable_debug_packages:%{?buildsubdir:%{debug_package}}}\
+%%install\
+export AR=%{__ar} RANLIB=%{__ranlib};\
+export CC=%{__cc} CXX=%{__cxx};\
+%{nil}
+:Macros
 ################################### targets ####################################

 %ifarch i586
@@ -139,24 +198,32 @@
 %ifarch armv7l
 Preinstall: qemu-accel-%{build_hostarch}-armv7l
 Runscripts: qemu-accel-%{build_hostarch}-armv7l
+Preinstall: clang-accel-%{build_hostarch}-armv7l
+Runscripts: clang-accel-%{build_hostarch}-armv7l
 Preinstall: libmount libblkid libuuid
 %endif

 %ifarch armv7hl
 Preinstall: qemu-accel-%{build_hostarch}-armv7hl
 Runscripts: qemu-accel-%{build_hostarch}-armv7hl
+Preinstall: clang-accel-%{build_hostarch}-armv7hl
+Runscripts: clang-accel-%{build_hostarch}-armv7hl
 Preinstall: libmount libblkid libuuid
 %endif

 %ifarch aarch64
 Preinstall: qemu-accel-%{build_hostarch}-aarch64
 Runscripts: qemu-accel-%{build_hostarch}-aarch64
+Preinstall: clang-accel-%{build_hostarch}-aarch64
+Runscripts: clang-accel-%{build_hostarch}-aarch64
 Preinstall: libmount libblkid libuuid
 %endif

 %ifarch riscv64
 Preinstall: qemu-accel-%{build_hostarch}-riscv64
 Runscripts: qemu-accel-%{build_hostarch}-riscv64
+Preinstall: clang-accel-%{build_hostarch}-riscv64
+Runscripts: clang-accel-%{build_hostarch}-riscv64
 Preinstall: libmount libblkid libuuid
 %endif

@@ -202,9 +269,10 @@

 VMinstall: perl libmount libblkid libext2fs libuuid  grep libpcre util-linux libsmartcols procps-ng

-Required: binutils gcc glibc rpm-build libtool
-Required: gcc-c++
-
+Required: binutils glibc rpm-build libtool
+
+Support: gcc gcc-c++
+Support: clang llvm-devel
 Support: glibc-locale
 Support: perl
 Support: hostname
@@ -237,7 +305,7 @@
 Keep: nss-softokn-freebl libmagic libmagic-data
 Keep: setup
 Keep: update-alternatives
-Keep: cpp
+Keep: clang llvm libllvm llvm-devel
 Keep: gcc-c++
 Keep: libatomic
 Keep: libgomp
@@ -254,16 +322,30 @@

 ############################## compilation flags ###############################

-%define __global_cflags -O2 -fno-inline-functions -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong -Wformat-security -fmessage-length=0 -Wl,-z,relro,--as-needed
-
-Optflags: armv7l %{__global_cflags} --param=ssp-buffer-size=4 -mtune=cortex-a53 -march=armv8-a+crc -mlittle-endian -mfpu=neon-vfpv4 -mfloat-abi=softfp -mthumb -Wp,-D__SOFTFP__ -Wl,-O1 -Wl,--hash-style=gnu -Wa,-mimplicit-it=thumb
-Optflags: armv7hl %{__global_cflags} --param=ssp-buffer-size=4 -mcpu=cortex-a53 -mtune=cortex-a53 -march=armv8-a+crc -mlittle-endian -mfpu=neon-vfpv4 -mfloat-abi=hard -mthumb -Wl,-O1 -Wl,--hash-style=gnu -Wa,-mimplicit-it=thumb
-Optflags: aarch64 %{__global_cflags} -feliminate-unused-debug-types -Wformat -march=armv8-a -Wl,-z,max-page-size=0x1000 -Wl,-O1 -Wl,--hash-style=gnu
-Optflags: i686 %{__global_cflags} -feliminate-unused-debug-types --param=ssp-buffer-size=4 -fdiagnostics-color=never -m32 -march=i686 -mtune=i686 -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables -fno-omit-frame-pointer -mstackrealign
-Optflags: x86_64 %{__global_cflags} -feliminate-unused-debug-types --param=ssp-buffer-size=4 -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables -fno-omit-frame-pointer
-Optflags: riscv64 %{__global_cflags} -feliminate-unused-debug-types -Wformat -mabi=lp64d -march=rv64gc -Wl,-O1 -Wl,--hash-style=gnu
-
-####################### base specific for normalization ########################
+%define __optflags %{__optflags_toolchain} -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0
+
+Optflags: armv7l %{__optflags}  -mtune=cortex-a53 -march=armv8-a+crc -mlittle-endian -mfpu=neon-vfpv4 -mfloat-abi=softfp -mthumb -Wp,-D__SOFTFP__ -Wa,-mimplicit-it=thumb -D_FILE_OFFSET_BITS=64
+Optflags: armv7hl %{__optflags} -mcpu=cortex-a53 -mtune=cortex-a53 -march=armv8-a+crc -mlittle-endian -mfpu=neon -mfloat-abi=hard -mthumb -Wa,-mimplicit-it=thumb -D_FILE_OFFSET_BITS=64
+Optflags: aarch64 %{__optflags} -march=armv8-a
+Optflags: i686 %{__optflags} -fdiagnostics-color=never -m32 -march=i686 -mtune=i686 -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables -fno-omit-frame-pointer -mstackrealign
+Optflags: x86_64 %{__optflags} -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables -fno-omit-frame-pointer
+Optflags: riscv64 %{__optflags} -mabi=lp64d -march=rv64gc
+
+%ifarch armv7l armv7hl riscv64
+Macros:
+%build_ldflags -Wl,-z,relro,--as-needed,-O1,--hash-style=gnu
+:Macros
+%endif
+%ifarch aarch64
+Macros:
+%build_ldflags -Wl,-z,max-page-size=0x1000 -Wl,-O1 -Wl,--hash-style=gnu
+:Macros
+%endif
+%ifarch i686 x86_64
+Macros:
+%build_ldflags -Wl,-z,relro,--as-needed
+:Macros
+%endif

 Macros:
 %tizen_profile_name tv
@@ -271,5 +353,4 @@
 # Disable rpm strip for debug(Requested by jihun32.jung, 9th/MAY/16)
 %_rpm_strip_option --strip-debug

-:Macros
-
+
```
