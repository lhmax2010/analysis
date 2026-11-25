# 0012m addendum 2 • Root cause found: the pilot's driver wrapper breaks every link

Archive this evidence:

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0012m-weda-failure-context-20261125.txt` | `6f82d8ad2a1ec13bee9d3c210838206bc5ea19e8ff392cbff81f5f5ac4959427` |

## R1: affects six of the seven built packages, every lane including baseline

```
/home/abuild/rpmbuild/BUILD/<pkg>/.pm12-driver/armv7l-tizen-linux-gnueabi-clang: line 31: link_edits[@]: unbound variable
```

AVControl (clang++), tv-viewer, bluetooth-impl-sec-oal, webserver and widevine-cdm all fail in CMake's compiler check at the **link** step of `cmTC_*`. nnstreamer fails in Meson's linker detection (`-Wl,--version`) with the same message.

**Cause.** Your `.pm12-driver` wrapper expands an empty array, `"${link_edits[@]}"`, under `set -u`. Bash older than 4.4 treats an empty array as unset, so the expansion aborts. Every link step whose argv did not fill `link_edits` therefore dies before the real driver runs. Your local fixture used the host's newer bash, so it never saw this. It is the same class of failure as `realpath`, coreutils 6.9 and gawk 3.1.5.

**Fix:**
1. Use the portable idiom `${link_edits[@]+"${link_edits[@]}"}` for every array in every injected script. Or avoid arrays, or drop `set -u` around the expansion.
2. **Add bash to the compatibility floor.** Get the build root's bash version from the Official RPM list: `rpm --root <eli_m1on root> --dbpath /var/lib/rpm --define '_db_backend bdb_ro' -qf /bin/bash`, as the user did before.
3. Run the fixture under that bash. Also add a static check that flags `"${name[@]}"` under `set -u` in every injected script: the wrapper, `driver-config.sh`, `thumb-check.sh` and the kernel matrix wrappers.
4. Check every other injected script, including the kernel `ld.lld` wrapper planned for Thursday, for the same pattern.

## R2: libpisa-ipc baseline, a different failure

```
armv7l-tizen-linux-gnueabi-clang++: error: -Wl,-z,relro: 'linker' input unused [-Werror,-Wunused-command-line-argument]
Configuration file: /usr/bin/clang++.cfg
```

The compile-only step (`-c testCXXCompiler.cxx`) gets `-Wl,-z,relro` together with `-Werror` from the package flags. The distribution CFLAGS normally carry `-Wno-unused-command-line-argument`, but the package's overwritten CXXFLAGS drop it. Official QB still builds libpisa-ipc, so something in the pilot baseline differs from Official.
- Diff `/usr/bin/clang++.cfg` and `/usr/bin/clang.cfg` between this lane's build root and the pristine Official build root kept by the Step 5 run (`pm0010-gbs-board-bench.eli_m1on/GBS-ROOT/local/BUILD-ROOTS/scratch.armv7l.0`).
- Check whether the wrapper or the driver-config step adds or reorders flags, especially `-Wl,*` on compile-only lines.
- Compare the compile argv with the Official QB build log of libpisa-ipc, if it is retained.
- Report the exact source of `-Wl,-z,relro` on the compile line.

## Other points

- **Default-lane config:** `/usr/bin/clang.cfg` is loaded. The `PM_CFG clang OPTION` line shows a long option list starting with the distribution flags (`-Os -fstack-protector … -mtune=…`). State whether that list is the **config file content** or the probe's own argv. If the Official `clang.cfg` already contains the distribution flags, including `-mthumb`, that changes the A32 root-cause story for spec overwrites. Answer with the file content and hash from the pristine root.
- **The baseline lanes must be identical to the Official build apart from observation.** Any wrapper that fails or changes argv in the baseline lane invalidates the comparison. The smoke test must show that the baseline argv for one `cmTC` compile and link equals the unwrapped argv.

## Required before any relaunch

Run the AVControl **baseline-only** smoke build in the foreground, with the fixed wrapper. It must pass `%build` and produce the RPM. Report:
- the `cmTC` link argv;
- the wrapper's recorded argv;
- the resulting ELF ISA.

After that comes one Thumb-2 pilot package (AVControl, all three lanes). Only then a full night.
