# 0012m addendum • What the Wed-A failure tails show

Archive this evidence:

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0012m-weda-failure-tails-20261125.txt` | `53f933b44834c9b53c6a2616bf60f7b33cf0924fa2f2e5f640b8466aef544fd0` |

The `printf: --: invalid option` lines come from my own read-only script and are cosmetic. Its error grep stopped at the first 12 matches, which were all build-root init noise, so a second read-only command (`native-cmd-r0012m-weda-failure-context.sh`) prints the 25 lines before `Bad exit status (%build)` and the CMake error logs. The user will send you its output.

## Already visible

1. **The failure is in `%build` for every baseline (101–374 s), not in dependency resolution.**
   - The noise lines appear in every lane: `liblto_plugin.so` mv, `/usr/bin/lua`, `find`/`xargs` missing in `gcc-warning-build-env.post` and `gcc-force-options-only`, `limits.conf`, `systemctl`, `kernel-install` and `hal-compatibility-checker`.
   - Confirm from a passing Official build log (QB or the earlier GBS replay) that the same lines appear there too. Otherwise they are part of the cause.
   - In particular, `gcc-force-options-only` failing on `find` means the GCC force-options hook is not working in this build root. Say whether that also happens in Official.
2. **Your `PM12_LINK_FAILURE` diagnostics point at CMake's compiler checks** (`testCCompiler.c` / `testCXXCompiler.cxx`) in AVControl, tv-viewer, libpisa-ipc, bluetooth, widevine, and webserver's default lane. So CMake's "working compiler" probe fails, most likely at link time, in lanes that include the unmodified baseline. The common factor is something your pilot adds to **every** lane: the argv trace wrapper, the driver probes, the observers, the local repo or the build.conf changes. Compare the probe's full compile and link argv between this pilot and the earlier successful r0010/r0011 package builds. Identify the first added element that breaks the link, and prove it with the AVControl baseline smoke run.
3. **The cc1 triple is `thumbv8a-tizen-linux-gnueabi`, with `+crc`, `+vfp4` and `+neon`.** The distribution flags therefore select ARMv8-A AArch32 Thumb. Record this in the T1 evidence. The armv7 assumption in the probes does not hold.
4. **The F6 signal looks real, independent of the build failures.** In the default lanes, the `PM_CFG … ARGV` probe for `it.c` runs with triple `armv7-tizen-linux-gnueabi` (ARM state) on all four drivers. If the scoped block had been loaded, that probe would run as Thumb. Decide from the context output whether the block never reached the effective config, or whether the probe ran before the block was installed. Fix whichever it is.
5. **libgcrypt:** `p4` rejected `@vbs-libgcrypt-20250804.155301-0-12916744` as a changelist/label. The SRPM pin is a VBS label string, not a P4 revision. Derive the P4 changelist (`12916744`?) from the label format, or use the SRPM contents. Prove the revision mapping on one package first.
6. **rpm:** two candidate SRPMs, `rpm-4.14.1.1-1.65` and `-1.78`. The Official build root has rpm-4.14.1.1-1.65, but the shipped image may differ. Pick the SRPM using the Official image roster or the board roster (`installed-rpms.tsv`), not the build root.
7. **Disk:** `/home1` is 1.8T in size with 86G free (96% used), and the disk is shared. The cleanup command in 0012m has priority.

## Kernel (0012l reply, Thursday pin `ce05cce`)

I will review `ce05cce` before Thursday. It does not block today's work. Do not schedule the kernel batch until the AVControl baseline smoke run passes, because the kernel lanes use the same GBS wrapper machinery that is now suspect.
