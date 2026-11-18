+  optimization", released in 1.9.5): the volatile qualifier is removed from the parameter - C++20 deprecates volatile-qualified
+  parameters (GCC -Wvolatile, Clang -Wdeprecated-volatile), and it never did what the comment says: a volatile POINTER parameter does
+  not make the memset through it non-removable, and std::memset cannot even take a volatile pointer, so this template could not be
+  instantiated at all. The zero fill became memset_s.
+- 07e3d1b (2024-09-12, #1478, in 1.9.7): memset_s only where it exists (HAVE_MEMSET_S), otherwise a byte fill through a
+  volatile unsigned char * (which the optimizer may not remove).
+- c6f68ac (2026-08-20, #1709): the fill covers n * sizeof(T) bytes, not n.
+This patch puts the resulting upstream body of deallocate() on 1.9.2 (plus #include <algorithm> for std::fill_n). Header-only
+(a class template), libjsoncpp.so is unchanged - no ABI change. Without it every C++20 translation unit that includes json/json.h
+gets the deprecation diagnostic, an error under -Werror (mcp-server had to add -Wno-error=volatile for GCC and
+-Wno-deprecated-volatile for Clang).
+
+diff --git a/include/json/allocator.h b/include/json/allocator.h
+index d5f987e..dbefacc 100644
+--- a/include/json/allocator.h
++++ b/include/json/allocator.h
+@@ -6,6 +6,7 @@
+ #ifndef CPPTL_JSON_ALLOCATOR_H_INCLUDED
+ #define CPPTL_JSON_ALLOCATOR_H_INCLUDED
+
++#include <algorithm>
+ #include <cstring>
+ #include <memory>
+
+@@ -35,11 +36,17 @@ public:
+    * Release memory which was allocated for N items at pointer P.
+    *
+    * The memory block is filled with zeroes before being released.
+-   * The pointer argument is tagged as "volatile" to prevent the
+-   * compiler optimizing out this critical step.
+    */
+-  void deallocate(volatile pointer p, size_type n) {
+-    std::memset(p, 0, n * sizeof(T));
++  void deallocate(pointer p, size_type n) {
++    // These constructs will not be removed by the compiler during optimization,
++    // unlike memset.
++#if defined(HAVE_MEMSET_S)
++    memset_s(p, n * sizeof(T), 0, n * sizeof(T));
++#else
++    std::fill_n(reinterpret_cast<volatile unsigned char*>(p), n * sizeof(T),
++                static_cast<unsigned char>(0));
++#endif
++
+     // free using "global operator delete"
+     ::operator delete(p);
+   }
```


## Appendix B　All files of clang-contrib (new package)

**clang-contrib.manifest**

```
<manifest>
 <request>
    <domain name="_"/>
 </request>
</manifest>
```

**clang-contrib.spec**

```
# Build-environment helpers for clang builds. The only binary package is clang-force-options, meant to be listed as
# Preinstall/RunScripts in the project config (like gcc-warning-build-env from gcc-contrib). Its %%post only registers
# rpm macros and makes /usr/bin writable; the forced options themselves are applied at %%build time by those macros
# (see macros.clang_force), because clang is not installed yet when the Preinstall %%post scripts run.
Name:           clang-contrib
Summary:        Build-environment helpers for clang builds
Version:        1.0.0
Release:        1
Group:          Development/Toolchain
License:        Apache-2.0
Source0:        clang-force-options
Source1:        clang-unforce-options
Source2:        macros.clang_force
Source3:        %{name}.manifest
# pure shell scripts and an rpm macro file: no debuginfo
%global debug_package %{nil}

%description
Helpers for building Tizen packages with clang. The source package itself
produces no binary; see clang-force-options.

%package -n clang-force-options
Summary:        Force the project's clang options on every package build
Group:          Development/Toolchain
# The package is Preinstall-ed (its init-time %%post runs before anything else is installed), but the build root is then
# populated for real and every package's %%post runs again in dependency order. rpm owns /usr/lib/rpm/tizen_macros and
# rewrites it when it is installed, so this package must be installed after rpm for the macros to survive. No other Requires:
# clang is deliberately not required here, the forcing happens at %%build time.
Requires:       rpm

%description -n clang-force-options
At the start of every %%build the project's compiler options (%%optflags plus
the forced linker options) are appended to /usr/bin/clang.cfg and
/usr/bin/clang++.cfg, and removed again at the end. clang reads these files
before the command line, so options passed by the package itself still take
precedence, while packages whose build system ignores CFLAGS/CXXFLAGS are
still built with the optimisation and hardening options of the project.
Blacklists: %%clang_force_incompatible_pkgs and the gcc warning blacklists
(%%gcc_warning_*_pkgs); %%clang_force_disable 1 switches the forcing off.

%prep
# nothing to unpack; the Tizen security manifest must sit in the build directory
cp %{SOURCE3} .

%build
# nothing to build

%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_rpmconfigdir}
install -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/clang-force-options
install -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/clang-unforce-options
install -m 0644 %{SOURCE2} %{buildroot}%{_rpmconfigdir}/macros.clang_force

%post -n clang-force-options
# Runs while the build root is initialised (Preinstall/RunScripts), before clang and findutils are installed:
# only bash, coreutils, grep and sed may be used here.
chmod a+w %{_bindir}
grep -q '^# /usr/lib/rpm/macros.clang_force$' %{_rpmconfigdir}/tizen_macros 2>/dev/null || cat %{_rpmconfigdir}/macros.clang_force >> %{_rpmconfigdir}/tizen_macros

%preun -n clang-force-options
sed -e '\|^# /usr/lib/rpm/macros.clang_force$|,\|^# /usr/lib/rpm/macros.clang_force ends here$|d' -i %{_rpmconfigdir}/tizen_macros

%files -n clang-force-options
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/clang-force-options
%{_bindir}/clang-unforce-options
%{_rpmconfigdir}/macros.clang_force
```

**clang-force-options**

```
#!/bin/bash
# clang-force-options <options...>
# Appends a marked block with <options> to /usr/bin/clang.cfg and /usr/bin/clang++.cfg (idempotent). clang reads these
# files before the command line, so the package's own options still take precedence. Run at the start of %build by the
# rpm macro %clang_force_incompatible (macros.clang_force); /usr/bin must be writable (done by the %post of this package).
OPTS="$*"
if [ -z "$OPTS" ]; then echo "clang-force-options: no options given, nothing done"; exit 0; fi
for f in /usr/bin/clang.cfg /usr/bin/clang++.cfg; do
  if [ -f "$f" ] && [ -w /usr/bin ]; then
    if grep -q '^# tizen-force-options begin$' "$f"; then
      echo "clang-force-options: already applied to $f"
    else
      cp "$f" "$f.force" && { echo '# tizen-force-options begin'; echo "$OPTS"; echo '# tizen-force-options end'; } >> "$f.force" && mv -f "$f.force" "$f" && echo "clang-force-options: applied to $f" || echo "clang-force-options: FAILED to rewrite $f"
    fi
    echo "clang-force-options: $f now reads:"; sed 's/^/clang-force-options:    /' "$f"
  else
    echo "clang-force-options: $f missing or /usr/bin not writable, nothing done"
  fi
done
exit 0
```

**clang-unforce-options**

```
#!/bin/bash
# clang-unforce-options
# Removes the block added by clang-force-options from /usr/bin/clang.cfg and /usr/bin/clang++.cfg (idempotent).
# Run when %build ends (%__spec_build_post), for blacklisted packages, and by %clang_unforce_options in a spec.
for f in /usr/bin/clang.cfg /usr/bin/clang++.cfg; do
  if [ -f "$f" ] && [ -w /usr/bin ] && grep -q '^# tizen-force-options begin$' "$f"; then
    sed '/^# tizen-force-options begin$/,/^# tizen-force-options end$/d' "$f" > "$f.force" && mv -f "$f.force" "$f" && echo "clang-unforce-options: removed the forced options from $f"
  fi
done
exit 0
```

**macros.clang_force**

```
# /usr/lib/rpm/macros.clang_force
#
# Forced compiler options for clang builds (package clang-force-options, source package clang-contrib).
#
# At the start of every %build (hook %__spec_build_pre, provided by macros.gcc_warning_force) the macro
# %clang_force_incompatible runs. Unless the package is blacklisted it executes
#     /usr/bin/clang-force-options <options>
# which appends a marked block with the options to /usr/bin/clang.cfg and /usr/bin/clang++.cfg. clang reads these
# files before the command line, so options given by the package itself still take precedence. When %build ends
# (%__spec_build_post) the block is removed again. Blacklisted packages get /usr/bin/clang-unforce-options instead.
# Nothing is done at install time: clang is not installed yet when the Preinstall %post scripts run.
#
# The option list defaults to the build root's own %optflags (project config: %__optflags_toolchain_clang and
# friends) plus the linker options gcc-contrib forces for gcc. In the project config:
#   %clang_force_options ...            replaces the list
#   %clang_force_disable 1              switches the forcing off
#   %clang_force_incompatible_pkgs a b  exempts packages (the %gcc_warning_*_pkgs blacklists are honoured as well)
# A spec that must not be forced calls %clang_unforce_options at the start of its %build.
#
# NOTE: rpm drops backslashes inside macro bodies, so no shell escape sequences may be used in them.

%clang_force_ldflags -Wl,-z,relro,--as-needed -Wl,-O1 -Wl,--hash-style=gnu
%clang_force_options %{optflags} %{clang_force_ldflags}

%clang_unforce_options %{lua: rpm.define("clang_force_unforced 1"); print("/usr/bin/clang-unforce-options")}

%clang_force_incompatible \
  %{lua: \
    if (rpm.expand("%{?clang_force_disable}") == "1") then \
      print("/usr/bin/clang-unforce-options") \
    elseif (nil ~= string.find( \
        " " .. rpm.expand("%{?clang_force_incompatible_pkgs}") .. \
        " " .. rpm.expand("%{?gcc_warning_incompatible_pkgs}") .. " " .. rpm.expand("%{?gcc_warning_kernel_pkgs}") .. \
        " " .. rpm.expand("%{?gcc_warning_opensource_pkgs}") .. " " .. rpm.expand("%{?gcc_warning_sr_pkgs}") .. \
        " " .. rpm.expand("%{?gcc_warning_thirdparty_pkgs}") .. \
        " " .. rpm.expand("%{?sec_buildconf_gcc_warning_incompatible_pkgs}") .. " " .. rpm.expand("%{?sec_buildconf_gcc_warning_kernel_pkgs}") .. \
        " " .. rpm.expand("%{?sec_buildconf_gcc_warning_opensource_pkgs}") .. " " .. rpm.expand("%{?sec_buildconf_gcc_warning_sr_pkgs}") .. \
        " " .. rpm.expand("%{?sec_buildconf_gcc_warning_thirdparty_pkgs}") .. " ", \
        " " .. rpm.expand("%{name}") .. " ", 1, true)) then \
      print("/usr/bin/clang-unforce-options") \
    else \
      print("/usr/bin/clang-force-options " .. rpm.expand("%{clang_force_options}")) \
    end \
  }

# remove the block when %build ends (keeps reused build roots clean); %___build_post needs the exit code of %build
%__spec_build_post \
  RPM_EC=$?; /usr/bin/clang-unforce-options; ( exit $RPM_EC ); \
  %{___build_post} \
%{nil}

# /usr/lib/rpm/macros.clang_force ends here
```


## Appendix C　llvm and qemu_aggregate at project set-up

Files of the llvm package on both sides:

- `Tizen:10.0:Base`: llvm-19.1.4.tar.gz (217 MB), llvm.spec, llvm.changes, llvm.manifest, _perforceinfo
- `Tizen:10.0:Base:Dev:LLVM`: llvm-22.1.8.tar.gz (353 MB), llvm.spec, llvm.manifest, mlgo_aarch_model.tar.gz / mlgo_arm_model.tar.gz / mlgo_x86_model.tar.gz (about 29 MB each), openmp.patch

### C.1 llvm r2 (08-28, copied from home:prj_admin:LLVM-22)

```diff
Index: llvm.spec
===================================================================
--- llvm.spec (revision 1)
+++ llvm.spec (revision 2)
@@ -1,7 +1,25 @@
 %define keepstatic 1
+
+# MLGO AOT support for LLVM MLGO (Ahead-of-Time compilation)
+# TODO: switch back to a project_config-controlled macro after MLGO is enabled
+# for all required arches.
+# %%bcond_with mlgo
+%ifarch armv7l aarch64 x86_64
+%bcond_without mlgo
+%endif
+
+%if %{defined _toolchain}
+%define _toolchain_override clang
+%define llvm_release_build 0
+%else
 %define llvm_release_build 1
+%endif
+
+%if 0%{llvm_release_build}
+%global _lto_cflags %{nil}
+%endif

-%define llvm_version 19
+%define llvm_version 22

 %define sdk_install_prefix /home/owner/share/tmp/sdk_tools/lldb
 %define sdk_bin_dir %{sdk_install_prefix}/bin
@@ -16,23 +34,36 @@
 %endif

 Name:      llvm
-VCS:           //TIZEN/[MAIN]/[BASE2026_Prj]/[INT]/platform/upstream/llvm#vbs-llvm-20250930.131421-0-13118253
 Summary:   The LLVM Project is a collection of modular and reusable compiler and toolchain technologies
-Version:   19.1.4
+Version:   22.1.8
 Release:   1
 Group:     Development/Toolchain
 License:   NCSA
 Source0:   %{name}-%{version}.tar.gz
+Source1000: openmp.patch
 Source1001: llvm.manifest

+# Bundled MLGO AOT assets for the inliner and regalloc models.
+# These override build-time AOT compilation, avoiding the need for TensorFlow
+# Python in GBS.
+Source1002: mlgo_arm_model.tar.gz
+Source1003: mlgo_aarch_model.tar.gz
+Source1004: mlgo_x86_model.tar.gz
+
+%{!?mlgo_build_jobs: %define mlgo_build_jobs 6}
+%{!?mlgo_verify_configure_only: %define mlgo_verify_configure_only 0}
+
 BuildRequires: cmake
 BuildRequires: python3
 BuildRequires: python3-devel
 BuildRequires: patchelf
 BuildRequires: binutils-devel
+BuildRequires: libxml2-devel
 %if 0%{llvm_release_build}
 BuildRequires: sed
 %endif
+BuildRequires: ninja
+

 Requires: libllvm = %{version}-%{release}

@@ -108,6 +139,18 @@
 %description -n compiler-rt
 Compiler runtime libraries

+%package -n libomp
+Summary:    OpenMP runtime
+
+%description -n libomp
+OpenMP runtime.
+
+%package -n libomp-devel
+Summary:    Development files for the OpenMP runtime
+
+%description -n libomp-devel
+Development files for the OpenMP runtime.
+
 %package -n python-clang
 Summary: Python bindings to parts of the Clang library

@@ -116,6 +159,18 @@

 %prep
 %setup -q
+%if %{with mlgo}
+mkdir -p mlgo_verify_assets
+%ifarch armv7l
+tar -C mlgo_verify_assets -xzf %{SOURCE1002}
+%endif
+%ifarch aarch64
+tar -C mlgo_verify_assets -xzf %{SOURCE1003}
+%endif
+%ifarch x86_64
+tar -C mlgo_verify_assets -xzf %{SOURCE1004}
+%endif
+%endif

 %build
 %if 0%{llvm_release_build}
