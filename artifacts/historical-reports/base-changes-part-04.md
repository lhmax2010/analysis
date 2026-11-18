@@ -131,18 +186,82 @@
 cp %{SOURCE1001} .
 %{?asan:%gcc_unforce_options}

+%if 0%{llvm_release_build}
+filter_lto_flags() {
+    filtered_flags=
+    for flag in "$@"; do
+        case "$flag" in
+            -flto|-flto=*|-ffat-lto-objects|-fuse-linker-plugin) ;;
+            *) filtered_flags="${filtered_flags:+$filtered_flags }$flag" ;;
+        esac
+    done
+    echo "$filtered_flags"
+}
+
+export CFLAGS="$(filter_lto_flags $CFLAGS)"
+export CXXFLAGS="$(filter_lto_flags $CXXFLAGS)"
+export FFLAGS="$(filter_lto_flags $FFLAGS)"
+export LDFLAGS="$(filter_lto_flags $LDFLAGS)"
+%endif
+
+%ifarch armv7l
+export QEMU_RESERVED_VA=0x70000000
+%endif
+
+# Set up MLGO AOT model paths from bundled verify assets
+%if %{with mlgo}
+MLGO_AOT_DIR="$PWD/mlgo_verify_assets"
+MLGO_BUILD_DIR="$PWD/build"
+MLGO_RUNTIME_OBJECTS="${MLGO_AOT_DIR}/xla_runtime_objects/xla_compiled_cpu_function.cc.o;${MLGO_AOT_DIR}/xla_runtime_objects/cpu_function_runtime.cc.o;${MLGO_AOT_DIR}/xla_runtime_objects/custom_call_status.cc.o;${MLGO_AOT_DIR}/xla_runtime_objects/executable_run_options.cc.o;${MLGO_AOT_DIR}/xla_runtime_objects/runtime_single_threaded_matmul_f32.cc.o"
+MLGO_REQUIRED_RUNTIME_OBJECTS="xla_compiled_cpu_function.cc.o cpu_function_runtime.cc.o custom_call_status.cc.o executable_run_options.cc.o runtime_single_threaded_matmul_f32.cc.o"
+%endif
+
 mkdir -p build
 cd build
 cmake \
+    -G Ninja \
+    -DTIZEN=1 \
     -DCMAKE_C_COMPILER=%__cc \
     -DCMAKE_CXX_COMPILER=%__cxx \
     -DLLVM_HOST_TRIPLE=%{_host} \
+    -DLLVM_DEFAULT_TARGET_TRIPLE=%{_host} \
+    -DLLVM_TARGET_TRIPLE_ENV=%{_host} \
     -DCMAKE_ASM_FLAGS="$CFLAGS" \
-    -DCMAKE_BUILD_TYPE=Release \
+    -DCMAKE_C_FLAGS="$CFLAGS" \
+    -DCMAKE_CXX_FLAGS="$CXXFLAGS" \
+%if %{defined _toolchain}
+    -DCMAKE_SHARED_LINKER_FLAGS="-ffunction-sections -fdata-sections -Wl,--gc-sections" \
+    -DCMAKE_EXE_LINKER_FLAGS="-ffunction-sections -fdata-sections -Wl,--gc-sections" \
+%endif
     -DLLVM_ENABLE_ASSERTIONS=No \
-    -DLLVM_TARGETS_TO_BUILD='X86;ARM;AArch64;BPF;RISCV' \
-    -DLLVM_BUILD_LLVM_DYLIB=1 \
-    -DLLVM_ENABLE_PROJECTS="clang;lldb;clang-tools-extra;compiler-rt" \
+    -DLLVM_ENABLE_RTTI=ON \
+%ifarch x86_64 i686
+    -DCMAKE_BUILD_TYPE=Release \
+    -DLLVM_TARGETS_TO_BUILD='X86;ARM;AArch64;BPF' \
+%endif
+%ifarch armv7l
+    -DCMAKE_BUILD_TYPE=MinSizeRel \
+    -DLLVM_TARGETS_TO_BUILD='ARM;BPF' \
+    -DLLVM_TARGET_ARCH="ARM" \
+%endif
+%ifarch aarch64
+    -DCMAKE_BUILD_TYPE=Release \
+    -DLLVM_TARGETS_TO_BUILD='AArch64;BPF' \
+    -DLLVM_TARGET_ARCH="AArch64" \
+%endif
+%ifarch riscv64
+    -DCMAKE_BUILD_TYPE=Release \
+    -DLLVM_TARGETS_TO_BUILD='RISCV;BPF' \
+%endif
+    -DCLANG_ENABLE_ARCMT=OFF \
+    -DLLVM_BUILD_LLVM_DYLIB=ON \
+    -DCLANG_BUILD_CLANG_DYLIB=ON \
+%if %{defined _toolchain}
+    -DLLVM_LINK_LLVM_DYLIB=ON \
+    -DCLANG_LINK_CLANG_DYLIB=ON \
+%endif
+    -DLLVM_ENABLE_PROJECTS="clang;lldb;clang-tools-extra;lld;compiler-rt;openmp" \
+    -DLLVM_ENABLE_PER_TARGET_RUNTIME_DIR=OFF \
     -DLLVM_BUILD_EXAMPLES=OFF \
     -DLLVM_INCLUDE_EXAMPLES=OFF \
     -DLLVM_BUILD_TESTS=OFF \
@@ -153,21 +272,110 @@
     -DLLVM_OPTIMIZED_TABLEGEN=ON \
     -DCMAKE_INSTALL_PREFIX=%{_prefix} \
     -DLLVM_LIBDIR_SUFFIX=`echo %{_lib} | sed s/lib//g` \
+    -DCLANG_RESOURCE_DIR="../%{_lib}/clang/%{llvm_version}" \
     -DLLVM_BINUTILS_INCDIR=/usr/include \
+    -DLLVM_PARALLEL_COMPILE_JOBS=6 \
+    -DLLVM_PARALLEL_LINK_JOBS=2 \
+%if %{with mlgo}
+%ifarch armv7l aarch64 x86_64
+    -DTENSORFLOW_AOT_PATH="${MLGO_AOT_DIR}/mlgo_sysroot" \
+    -DLLVM_MLGO_EXPORT_TF_XLA_RUNTIME=OFF \
+    -DLLVM_MLGO_EMBED_TF_XLA_RUNTIME_OBJECTS="${MLGO_RUNTIME_OBJECTS}" \
+    -DLLVM_OVERRIDE_MODEL_HEADER_INLINERSIZEMODEL="${MLGO_AOT_DIR}/InlinerSizeModel.h" \
+    -DLLVM_OVERRIDE_MODEL_OBJECT_INLINERSIZEMODEL="${MLGO_AOT_DIR}/InlinerSizeModel.o" \
+    -DLLVM_OVERRIDE_MODEL_HEADER_REGALLOCEVICTMODEL="${MLGO_AOT_DIR}/RegAllocEvictModel.h" \
+    -DLLVM_OVERRIDE_MODEL_OBJECT_REGALLOCEVICTMODEL="${MLGO_AOT_DIR}/RegAllocEvictModel.o" \
+%else
+    -DLLVM_INLINER_MODEL_PATH=none \
+    -DLLVM_RAEVICT_MODEL_PATH=none \
+%endif
+%else
+    -DLLVM_INLINER_MODEL_PATH=none \
+    -DLLVM_RAEVICT_MODEL_PATH=none \
+%endif
     ../llvm

-make %{?_smp_mflags}
+%if 0%{mlgo_verify_configure_only}
+  # ---- configure-only probe: guard against §0 traps; check sentinels, GBS exit code non-0 is expected ----
+  # Note: %%build does not guarantee set -e, so each assertion explicitly uses '|| { ...; exit 1; }'
+  # Assertion 0: MLGO_BUILD_DIR is correct (fail immediately with clear error if wrong)
+  test -f CMakeCache.txt || \
+    { echo "FATAL: MLGO_BUILD_DIR wrong (CMakeCache.txt not found in $(pwd))"; exit 1; }
+%if %{with mlgo}
+  # Assertion 1: override actually took effect (COPYONLY artifacts exist from configure stage)
+  test -f lib/Analysis/InlinerSizeModel.h || \
+    { echo "FATAL: Missing InlinerSizeModel.h (override not effective, likely trap 1: silent fallback to none)"; exit 1; }
+  test -f lib/Analysis/InlinerSizeModel.o || \
+    { echo "FATAL: Missing InlinerSizeModel.o (override not effective)"; exit 1; }
+  test -f lib/CodeGen/RegAllocEvictModel.h || \
+    { echo "FATAL: Missing RegAllocEvictModel.h(regalloc override not effective)"; exit 1; }
+  test -f lib/CodeGen/RegAllocEvictModel.o || \
+    { echo "FATAL: Missing RegAllocEvictModel.o(regalloc override not effective)"; exit 1; }
+  for mlgo_runtime_object in ${MLGO_REQUIRED_RUNTIME_OBJECTS}; do
+    test -f "${MLGO_AOT_DIR}/xla_runtime_objects/${mlgo_runtime_object}" || \
+        { echo "FATAL: missing MLGO runtime object: ${mlgo_runtime_object}"; exit 1; }
+  done
+  # Assertion 1b: bundled objects must match the target arch.
+%ifarch armv7l
+  MLGO_EXPECT_MACHINE="ARM"
+%endif
+%ifarch aarch64
+  MLGO_EXPECT_MACHINE="AArch64"
+%endif
+%ifarch x86_64
+  MLGO_EXPECT_MACHINE="X86-64"
+%endif
+  for mlgo_obj in lib/Analysis/InlinerSizeModel.o lib/CodeGen/RegAllocEvictModel.o; do
+    readelf -h "${mlgo_obj}" | grep -q "Machine:.*${MLGO_EXPECT_MACHINE}" || \
+      { echo "FATAL: ${mlgo_obj} arch mismatch (expected ${MLGO_EXPECT_MACHINE})"; exit 1; }
+  done
+  for mlgo_runtime_object in ${MLGO_REQUIRED_RUNTIME_OBJECTS}; do
+    mlgo_obj="${MLGO_AOT_DIR}/xla_runtime_objects/${mlgo_runtime_object}"
+    readelf -h "${mlgo_obj}" | grep -q "Machine:.*${MLGO_EXPECT_MACHINE}" || \
+      { echo "FATAL: ${mlgo_obj} arch mismatch (expected ${MLGO_EXPECT_MACHINE})"; exit 1; }
+  done
+  # Assertion 2: did not fall into autogenerate mock. Use && short-circuit: file missing => FATAL, don't let '! grep' pass
+  test -f CMakeCache.txt && \
+    ! grep -qE 'LLVM_INLINER_MODEL_PATH(:[^=]+)?=autogenerate' CMakeCache.txt || \
+    { echo "FATAL: Fell into autogenerate mock or CMakeCache missing (trap 2)"; exit 1; }
+  test -f CMakeCache.txt && \
+    ! grep -qE 'LLVM_RAEVICT_MODEL_PATH(:[^=]+)?=autogenerate' CMakeCache.txt || \
+    { echo "FATAL: regalloc fell into autogenerate mock"; exit 1; }
+  # Assertion 3: MLGO runtime is embedded and tf_xla_runtime is not exported.
+  grep -q '^LLVM_MLGO_EXPORT_TF_XLA_RUNTIME:BOOL=OFF$' "${MLGO_BUILD_DIR}/CMakeCache.txt" || \
+    { echo "FATAL: MLGO TensorFlow runtime export is not disabled"; exit 1; }
+  for mlgo_runtime_object in ${MLGO_REQUIRED_RUNTIME_OBJECTS}; do
+    grep -q "xla_runtime_objects/${mlgo_runtime_object}" "${MLGO_BUILD_DIR}/CMakeCache.txt" || \
+      { echo "FATAL: MLGO runtime object is not embedded: ${mlgo_runtime_object}"; exit 1; }
+  done
+  cmake --build . --target tf_xla_runtime || \
+    { echo "FATAL: tf_xla_runtime build failed"; exit 1; }
+  MLGO_PROBE_ROOT="$PWD/mlgo_probe_root"
+  rm -rf "${MLGO_PROBE_ROOT}"
+  mkdir -p "${MLGO_PROBE_ROOT}"
+  DESTDIR="${MLGO_PROBE_ROOT}" cmake --install . \
+    --prefix /usr --component tf_xla_runtime --verbose
+  ! find "${MLGO_PROBE_ROOT}" -name libtf_xla_runtime.a | grep -q . || \
+    { echo "FATAL: tf_xla_runtime archive should not be installed"; exit 1; }
+%endif
+  echo MLGO_VERIFY_CONFIGURE_PASS
+  exit 86
+%endif
+
+# Full build using ninja (already in build/ directory after cd build)
+ninja -j %{mlgo_build_jobs}

 %install
 cd build
-%make_install
+cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/usr -P cmake_install.cmake
 ln -sf %{_prefix}/bin/clang++ %{buildroot}%{_prefix}/bin/clang++-%{llvm_version}

 ln -sf clang %{buildroot}%{_prefix}/bin/%{_host}-clang
 ln -sf clang++ %{buildroot}%{_prefix}/bin/%{_host}-clang++
-# Use host triple by default via <lang>.cfg
+# Use host triple and resource dir by default via <lang>.cfg
 cat >> %{buildroot}/%{_prefix}/bin/clang.cfg << EOF
 -target %{_host}
+-resource-dir %{_prefix}/%{_lib}/clang/%{llvm_version}
 EOF
 ln -sf clang.cfg %{buildroot}/%{_prefix}/bin/clang++.cfg

@@ -204,10 +412,14 @@
 %{_prefix}/bin/bugpoint
 %{_prefix}/bin/clang-linker-wrapper
 %{_prefix}/bin/clang-offload-packager
-%{_prefix}/bin/clang-pseudo
 %{_prefix}/bin/clang-repl
 %{_prefix}/bin/intercept-build
 %{_prefix}/bin/llc
+%{_prefix}/bin/lld
+%{_prefix}/bin/ld.lld
+%{_prefix}/bin/ld64.lld
+%{_prefix}/bin/lld-link
+%{_prefix}/bin/wasm-ld
 %{_prefix}/bin/lli
 %{_prefix}/bin/llvm-ar
 %{_prefix}/bin/llvm-as
@@ -215,6 +427,8 @@
 %{_prefix}/bin/llvm-bitcode-strip
 %{_prefix}/bin/llvm-c-test
 %{_prefix}/bin/llvm-cat
+%{_prefix}/bin/llvm-cgdata
+%{_prefix}/bin/llvm-ctxprof-util
 %{_prefix}/bin/llvm-config
 %{_prefix}/bin/llvm-cov
 %{_prefix}/bin/llvm-cvtres
@@ -238,6 +452,7 @@
 %{_prefix}/bin/llvm-lto2
 %{_prefix}/bin/llvm-mc
 %{_prefix}/bin/llvm-ml
+%{_prefix}/bin/llvm-ml64
 %{_prefix}/bin/llvm-modextract
 %{_prefix}/bin/llvm-mt
 %{_prefix}/bin/llvm-nm
@@ -263,6 +478,7 @@
 %{_prefix}/bin/llvm-tli-checker
 %{_prefix}/bin/llvm-windres
 %{_prefix}/bin/llvm-xray
+%{_prefix}/bin/offload-arch
 %{_prefix}/bin/opt
 %{_prefix}/bin/run-clang-tidy
 %{_prefix}/bin/sancov
@@ -292,13 +508,20 @@
 %{_prefix}/bin/llvm-undname
 %{_prefix}/bin/pp-trace
 %{_prefix}/bin/reduce-chunk-list
+%{_prefix}/bin/llvm-cas
+%{_prefix}/bin/llvm-ir2vec
+%{_prefix}/bin/llvm-offload-binary
+%{_prefix}/bin/llvm-offload-wrapper
+%{_prefix}/bin/yaml2macho-core

 %files devel
 %manifest %{name}.manifest
 %defattr(-,root,root,-)
+%{_prefix}/include/lld/*
 %{_prefix}/include/llvm/*
 %{_prefix}/include/llvm-c/*
 %{_prefix}/share/*
+%{_libdir}/cmake/lld/*
 %{_libdir}/cmake/llvm/*
 %{_libdir}/libLTO*.so*
 %{_libdir}/LLVMgold.so
@@ -319,7 +542,6 @@
 %files -n clang
 %manifest %{name}.manifest
 %defattr(-,root,root,-)
-%{_prefix}/bin/c-index-test
 %{_prefix}/bin/clang
 %{_prefix}/bin/clang++
 %{_prefix}/bin/%{_host}-clang
@@ -341,7 +563,7 @@
 %{_prefix}/bin/clang-include-fixer
 %{_prefix}/bin/clang-offload-bundler
 %{_prefix}/bin/clang-query
-%{_prefix}/bin/clang-rename
+%{_prefix}/bin/clang-sycl-linker
 %{_prefix}/bin/clang-reorder-fields
 %{_prefix}/bin/clang-tidy
 %{_prefix}/bin/clang-installapi
@@ -378,12 +600,14 @@
 %{sdk_bin_dir}/lldb-argdumper
 %{sdk_bin_dir}/lldb-server
 %{sdk_lib_dir}/liblldb*.so*
+%{_prefix}/bin/lldb-mcp

 %files -n lldb-devel
 %manifest %{name}.manifest
 %defattr(-,root,root,-)
 %{_prefix}/include/lldb/*
 %{_libdir}/liblldb*.so*
+%{_prefix}/bin/lldb-tblgen

 %files -n compiler-rt
 %manifest %{name}.manifest
@@ -391,5 +615,18 @@
 %{_libdir}/clang/%{llvm_version}/include/sanitizer/*
 %{_libdir}/clang/%{llvm_version}/*

+%files -n libomp
+%{_libdir}/libomp.so
+%ifnarch %arm
+%{_libdir}/libompd.so
+%{_libdir}/libarcher.so
+%endif
+
+%files -n libomp-devel
+%ifnarch %arm
+%{_libdir}/libarcher_static.a
+%endif
+%{_libdir}/cmake/openmp/FindOpenMPTarget.cmake
+
 %files -n python-clang
 %{python3_sitelib}/clang
Index: llvm-22.1.8.tar.gz
===================================================================
Binary files llvm-22.1.8.tar.gz (revision 2) added
Index: mlgo_aarch_model.tar.gz
===================================================================
Binary files mlgo_aarch_model.tar.gz (revision 2) added
Index: mlgo_arm_model.tar.gz
===================================================================
Binary files mlgo_arm_model.tar.gz (revision 2) added
Index: mlgo_x86_model.tar.gz
===================================================================
Binary files mlgo_x86_model.tar.gz (revision 2) added
Index: openmp.patch
===================================================================
--- openmp.patch (added)
+++ openmp.patch (revision 2)
@@ -0,0 +1,14 @@
+diff --git a/openmp/runtime/src/kmp_platform.h b/openmp/runtime/src/kmp_platform.h
+index 7d88c02e9cf3..90f2ff8eaacb 100644
+--- a/openmp/runtime/src/kmp_platform.h
++++ b/openmp/runtime/src/kmp_platform.h
+@@ -186,6 +186,9 @@
+ #elif defined __aarch64__
+ #undef KMP_ARCH_AARCH64
+ #define KMP_ARCH_AARCH64 1
++#elif defined(__arm__) || defined(_M_ARM) || defined(_ARM)
++#undef KMP_ARCH_ARM
++#define KMP_ARCH_ARM 1
+ #elif defined __mips__
+ #if defined __mips64
+ #undef KMP_ARCH_MIPS64
Index: _perforceinfo
===================================================================
--- _perforceinfo (revision 1)
+++ _perforceinfo (deleted)
@@ -1,2 +0,0 @@
