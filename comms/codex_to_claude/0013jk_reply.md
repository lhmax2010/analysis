```bash
(
set -eu -o pipefail
p=1a9d27cfef4549c14a74a951c8ba18f77f9270f6
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013jk-launch.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0013jk/run.sh.txt" -o "$d/run"
printf '%s  %s\n' a8361cce5c35db157f82b13d77eb1d62117101d43b374ab12fde055dc4890ee9 "$d/run" | sha256sum -c -
bash "$d/run" "$p" static | tee "$d/combined.txt"
)
```

### Release gates

| Gate | K1/K0 | K3/K2 | Evidence required for PASS |
|---|---|---|---|
| S1 boot-critical paths | Await static receipt | Await static receipt | Helper and caller sections, critical ranges, direct paths and coverage of unresolved edges |
| S4 exception/bug tables | Await static receipt | Await static receipt | Decoded fault and fixup PCs, paired counts, zero helper hits |
| S9 branch veneers | Await static receipt | Await static receipt | Counts, bytes and placement; zero veneers in critical sections |
| S11 system state | Await static receipt | Await static receipt | Complete helper disassembly and disposition of system-state instructions |
| S12 in-tree modules | Await static receipt | Await static receipt | Full paired module roster, size/helper/relocation/PLT comparison with ARM loader |

**QB release is on hold.** K1 and K3 perf ELFs are complete with ARGV PASS. K1 contains 20,324 helpers covering 316,380 B, K3 contains 26,020 covering 411,200 B. The original package jobs subsequently failed in SERET-UL/GCC. Their measurements can be reused. The clean verification build below qualifies the proposed spec through the GCC step.

Native host after Claude review. One idle-I/O worker, no build lock, GBS or sudo. Allow 30–150 minutes plus the installed Thumb scan and several GiB of scratch. Reads use the explicit dkyJ0S matrix, a0Pmc0 measurement receipt and HgSjf0 partitions. Network use is limited to pinned analyzer downloads. Paste the gate rows and final archive and receipt lines. The archive includes per-PC calls and input sections, LR variants and frames, fixups, sensitive instructions, hot-path source joins, module comparisons and known/unknown Thumb bytes. Static helper-site share and maximum observed nested LR saves have different units from measured profile time and actual worst-case kernel stack depth. Missing caller attribution, ambiguous table encoding, incomplete module trees or unexplained state instructions keep the affected release gate open.

To export the complete static archive by terminal, run this block once per numbered part. Each part contains 12 KiB of the compressed archive.

```bash
read -r -p 'Paste TABLES line: ' tag digest file
read -r -p 'Part number starting at 1: ' part
python3 -B - "$tag" "$digest" "$file" "$part" <<'PY'
import base64, hashlib, math, sys
from pathlib import Path
tag,h,name,n=sys.argv[1:];p=Path(name).resolve(strict=True)
assert tag=="TABLES" and p.name=="side-effects.tar.gz" and p.parent.parent==Path("/home1/chengkai/vd-tree/workspace/temp")
g=hashlib.sha256()
with p.open("rb") as f:
    for block in iter(lambda:f.read(1<<20),b""):g.update(block)
    assert g.hexdigest()==h
    total=math.ceil(f.tell()/12288);i=int(n);assert 1<=i<=total
    f.seek((i-1)*12288);print(h,f"{i}/{total}",base64.b64encode(f.read(12288)).decode())
PY
```

### Proposed spec

Base spec after shelf 14427407 on CL 14293732 has SHA-256 `5663f9c9c074f74e69a57bec9fb3dcc595512985a778814e311e0658e2b12cc5`. RPM expands `%%` to `%`. Shell quoting preserves the expression for make to evaluate with the actual CC. The separate SERET-UL invocation retains its original environment.

```diff
--- a/packaging/tztv-kernel.spec
+++ b/packaging/tztv-kernel.spec
@@ -301 +301 @@
-    env $KERNEL_TOOLCHAIN_ENV ./BUILD.sh "$PROJECT" "$RELEASE_MODE" "$SIGN_CHIP" "$VERIFIER" "$SANITIZER"
+    env $KERNEL_TOOLCHAIN_ENV KCFLAGS="${KCFLAGS:+$KCFLAGS }"'$(if $(filter clang clang-%% %%-clang,$(notdir $(lastword $(CC)))),-moutline)' ./BUILD.sh "$PROJECT" "$RELEASE_MODE" "$SIGN_CHIP" "$VERIFIER" "$SANITIZER"
```

### Clean Official verification

```bash
(
set -eu -o pipefail
p=1a9d27cfef4549c14a74a951c8ba18f77f9270f6
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013jk-launch.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0013jk/run.sh.txt" -o "$d/run"
printf '%s  %s\n' a8361cce5c35db157f82b13d77eb1d62117101d43b374ab12fde055dc4890ee9 "$d/run" | sha256sum -c -
bash "$d/run" "$p" build | tee "$d/combined.txt"
)
```

Native host, attended. Paste the `STATIC_GATE PASS RECEIPT …` line. The build takes the queue and heavy locks, requires sudo, six pinned cores, 105 GiB free disk and 32 GiB available RAM. Estimate 30–90 minutes. It stages a private clone of OwlD9Q, a workspace buildroot, the 37777148 Official repos and the published build.conf. It checks exit 0, the perf RPM and config, the linked ELF build ID embedded in the checked uImage payload, actual Clang/module argv and the GCC SERET-UL argv. Incomplete surviving build evidence holds the shelf. Retain gbs.log, argv.json and the build receipt. Proposed repeatability limit for PM approval is 0.10% on each of .text 8,214,312 B, Image 10,996,388 B, zImage 5,449,312 B and 20,324 helpers. Report all observed values.

### Attended test shelf

```bash
(
set -eu -o pipefail
p=1a9d27cfef4549c14a74a951c8ba18f77f9270f6
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013jk-launch.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0013jk/run.sh.txt" -o "$d/run"
printf '%s  %s\n' a8361cce5c35db157f82b13d77eb1d62117101d43b374ab12fde055dc4890ee9 "$d/run" | sha256sum -c -
bash "$d/run" "$p" shelve | tee "$d/combined.txt"
)
```

P4 client `DEV-IPTV-VC_TOOLCHAIN`, root `/home1/chengkai/vd-tree`, expected depot file `//TIZEN/[MAIN]/[TIZENPROD_Prj]/[INT]/PRODUCT/SYSARCH/Sysarch/bsp/vdlinux/packaging/tztv-kernel.spec`. Paste the checksum-bearing static and build receipts. Confirm the depot path when prompted. A new pending CL opens only the spec, writes the build-verified bytes, checks the shelved content and restores the original working file. The CL number and describe output are the handoff. If P4 fails after allocating a CL, inspect that CL's opened/shelved state before retrying. Seconds, one spec and P4 metadata.

### Signed QB inputs

| Existing signed control | New signed treatment |
|---|---|
| Official 37777148, Product 20261125.1, Base 20261113.1 | Clone that job and append the verified test shelf |
| Custom 37777264, Product 20261125.2, Base 20261118.1 | Clone that job and append the same test shelf |

Recover the submitted shelf and Base lists from each control job and hash the ordered inputs. The controls have 5,880 matching Product VCS rows and published build.conf `98690f234ec8b79c728ae624f3ea91b12e6db5d918c70cfacb277d798dc95e03`. Their original submitted list copies were unavailable for independent comparison. Preserve shelf 14427407 and all other overlays. Verify the final appended CL wins for the spec and preserves the remaining overlay files. Hold Product source revisions, kernel config, packaging, signing profile and PERF image recipe fixed. Recheck the published source/package/VCS ledger and the built spec digest, capture both signed images and their manifests, and log every additional change as a confounder.

### Four-image board runbook

For each Base, alternate its signed control and treatment on the same KantSU2E. Counterbalance which Base is tested first. Match settings, thermal start, network, peripheral fixtures and media hash. Compute treatment minus control separately for each Base. Report the difference of those two effects separately. Local K2/K3 use MLGO off; a Custom-model QB runs with MLGO enabled.

| Order | Capture per image | Gate |
|---|---|---|
| 1 | Match signed USB manifest, Product, board boot ID and kernel build ID. Record active slot, early boot Memory line, /proc/iomem and separate uImage/zImage sizes. Stage verified rollback. | Stop on identity mismatch; preserve early console for boot failures. |
| 2 | Cold boot to responsive Home ×5. Match idle time and measure MemAvailable at minutes 6/7/8, top PSS and temperature. | Retain raw timings, medians and paired control spread. |
| 3 | Suspend/resume ×5 and instant-on/fast-boot ×5. Check picture, input, sound and new kernel messages each cycle. | Stop on failed wake, hang or loss of function. |
| 4 | Check remote/IR, HDMI-CEC, tuner/channel change, Wi-Fi, BT, USB and audio with the same equipment. | Record each result; unavailable peripherals remain open. |
| 5 | Five runs of each available signed hackbench/perf sched/perf mem workload. Keep argv and input fixed. | Compare dispersion and medians. Attribute helper samples using matched build IDs and caller stacks; record unresolved weight. |
| 6 | Three matched 4K playback/seek runs. Capture CPU, player drop counters, A/V sync and media PSS. | Establish counter source before comparing; inspect every new drop or sync failure. |
| 7 | Use an existing owner-approved benign QA warning path, when available. Symbolize helper and caller PCs with matching symbols. | Verify the expected frames; record skipped/unresolvable frames or an unavailable trigger. |
| 8 | Soak each +outline image for 24 h with the matched control workload/log window. Capture watchdog, soft/hard lockup, warning, oops, panic and device failures. | Stop on a new failure; retain evidence and restore the verified same-Base control using the operator's flash procedure. |

The separate Thumb QB run captures ITD via approved board diagnostics or verified effective CPU setup (C7), alignment counters and SIGBUS before/after equal-duration soaks (C8), signed mixed-mode exception, longjmp and Thumb signal/ucontext tests (C9), and a known QA core with expected mixed frames, CPSR.T, mapping symbols and matching debug data (C10).

Local checks passed for the launcher manifests, Python 3.10.12 modules, Thumb IT decoding and helper intervals. Bash 3.2.57 with GNU make selected the outliner for three Clang driver forms and omitted it for both GCC driver forms. The native S-gate receipt, clean GBS build and P4 shelf await execution and review.
