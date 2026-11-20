# PM → Codex, round 0007b: the GCC "Thumb default" is a force-options wrapper

Evidence file (in ~/Downloads, copied from the user's terminal paste): `native-run-r0007-gcc-force-wrapper-20261120.txt`, 24 lines, sha256 `de598a7a5ca7a896052e80f41d23c166c28b00e4835948023c77b0aaee3908c9`.

## What the build root shows (official GBS root, published build.conf@14452507)

These four are Tizen "force options" shell wrappers created at build-root setup:

- `/usr/bin/gcc` and `/usr/bin/armv7l-tizen-linux-gnueabi-gcc` (identical, 1684 B);
- `/usr/bin/g++` and `/usr/bin/c++` (1622 B).

`cc` is a symlink to `gcc`. The wrappers call `$(readlink -f $0)-real`.

For every invocation **without** `__KERNEL__` or `-nostdlib`, the wrapper **appends** this list after the package's own arguments:
```diff
-Wmissing-parameter-type -Wold-style-declaration -Wsign-compare -Woverride-init
-O2 -g2 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong
-Wformat-security -Wformat -fmessage-length=0 -Wno-implicit-fallthrough --param=ssp-buffer-size=4
-mcpu=cortex-a53 -mtune=cortex-a53 -march=armv8-a+crc -mlittle-endian -mfpu=neon-vfpv4
-mfloat-abi=softfp -mthumb -Wp,-D__SOFTFP__ -Wa,-mimplicit-it=thumb
-Wshadow -fno-common -fsigned-char -Wclobbered -Wcast-function-type
-Wmissing-field-initializers -Wshift-negative-value -Werror

```

(The g++ list may differ slightly in its leading C-only warnings. Check it.)

For `__KERNEL__` or `-nostdlib` invocations, the wrapper adds only `-Wl,--tizen-no-force-options`.

## Consequences. Verify each, then use them in the ledger and reports

1. **Mechanism for HQ.** Under GCC, every non-kernel, non-`-nostdlib` compile was forced to `-mthumb`, **appended last**. So it overrode both a package's own explicit `-marm` and any missing CFLAGS.
   - Clang has no such wrapper, and `clang.cfg` has no `-mthumb`.
   - So under Clang a file becomes A32 whenever its build drops `$CFLAGS`, passes `-marm`, or uses `.arm`/`target("arm")`/A32 asm.
   - This explains why the ARM-predominant count is high only in the Clang image.
   - `GCC_DEFAULT_C → $t` in the probe is the wrapper, not GCC itself. **Correct 0007 §2 and the ledger accordingly.**
2. **The 157 GCC-only-marker A32 files.** Under the wrapper, a GCC compile cannot produce A32 code. So GCC-marked A32 code must come from one of these. Classify the 157 on that basis:
   - asm;
   - `__KERNEL__`/`-nostdlib` builds (glibc builds parts with `-nostdlib`; check that);
   - objects built outside this environment (prebuilt/bundled);
   - packages whose build bypasses `/usr/bin/gcc` by an absolute `*-gcc-real`/accelerator path.
3. **Optimization level confound.** The wrapper also forces `-O2` (appended last). So **historical GCC builds were effectively `-O2` and `-fstack-protector-strong`**, while the Clang optflags are `-Os -fstack-protector`. Every GCC-vs-LLVM size or performance comparison in the reports must state this. Check the historical reports for claims that assumed `-Os` for GCC.
4. **Is this wrapper active in the real QB/OBS builds?** Identify:
   - the package that installs it (a `gcc-force-options` style package?) and its version;
   - which `build.conf` line pulls it in (Preinstall/Support/Required);
   - whether QB product builds and the 1113.1/1118.1 Base OBS builds get the same wrapper.
   Also explain `-Werror` plus `-Wshadow` being forced on every GCC compile. Is that really the production setting, or a GBS-only artefact? Do not state the mechanism to HQ until this is proven for QB/OBS.
5. **Fix design (update 0007 §2.3).** Two candidates for the Clang side:
   - (a) `-mthumb` in `clang.cfg`. The config options come first, so an explicit package `-marm` still wins. This fixes only the "CFLAGS dropped" class.
   - (b) a force-options equivalent for Clang that appends `-mthumb` (and only the ISA option; do not copy `-O2`/`-Werror`). It fully mirrors the GCC behaviour, including overriding explicit `-marm`.
   Every package that now builds A32 under Clang built Thumb under the forced GCC and worked on the board. That is strong evidence that (b) is safe for C/C++; asm `.S` files are unaffected either way. Recommend one, with the measurement plan (size, code memory, KantSU2E check, one change per experiment).

## Deliverables

- Commit the evidence.
- Answer items 1–5 with evidence.
- Fold the corrections into the reply for 0007 / 0007a. Do not send a separate thread.
