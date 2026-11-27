# 0013x — r0013n Thumb-2 enumeration never compiled: wrong product repo (PM review)

**Evidence (archive both under `artifacts/evidence/`):**
- `native-run-r0013n-enum-DsfXAe-20261127.txt`, sha256 `2f03badb43703faeca9fc45aeec72c664931f0d45530daba20c264b36c7dee73`
- `native-run-r0013n-prebuild-DsfXAe-20261127.txt`, sha256 `2cd7d1f1e4bf92c6e196bd049287a4b17d995362c51e24847021b7246dfea14b`

## What happened

Run `pm0013n-enum.DsfXAe` was launched from pin `9e8886d8`, with `enumerate.sh.txt` sha `967b647b…`. It reported `ENUM_RESULT INCOMPLETE 1 diagnostics 1 known_errors 0 config []` and `make_k_seen false`.

It did not reach the kernel. In `gbs.log`, GBS refused the kernel package at dependency resolution:

```
=== the following packages failed to build due to missing build dependencies (1) ===
  nothing provides secureboot-signer
  nothing provides vd-kernel-dtb-devel
=== Total succeeded built packages: (0) ===
```

As a result:
- `logs/fail/` and `logs/success/` are empty;
- no `BUILD-ROOTS/` directory was created;
- nothing was compiled.

**Root cause: the generated `gbs.conf` used a different product repo from the one the working K-lanes used:**

```
[repo.product_NikeM]
url = http://repos.vd.sec.samsung.net/priv/168.219.246.226:81/PRV/builds/b776/19414776/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2/
```

This is an **ASAN** artifact from a different build (19414776, 20261123.2). It does not publish `secureboot-signer` or `vd-kernel-dtb-devel`.

The base repo (`tizen-10.0-base-dev-llvm-standard_20261113.1`) is correct. The K4/K5 lanes in `pm0012-kernel.dkyJ0S` got past dependency resolution and failed in the Thumb-2 assembler, so their product repo was correct.

## Required fixes (`enumerate.sh` / `enumerate.py`)

1. **Repo provenance.** Take the product (and base) repo URLs **verbatim from the gbs config that the K4 lane of `pm0012-kernel.dkyJ0S` actually used**. Do not take them from a "latest KantSU2e artifact" lookup or any other discovery. Print them in `ENUM_INPUT` along with the source file and its sha256. If the K4 config can't be found, stop with `ENUM_RESULT SETUP_FAILED repo-provenance`. Do not guess.

2. **Classify setup failures correctly.** If `gbs.log` contains `missing build dependencies`, `nothing provides`, `have choice` or `unresolvable`, emit `ENUM_RESULT SETUP_FAILED deps` and list the missing names. Do not emit `INCOMPLETE`. Likewise, if no build root exists or `make_k_seen` is false, the result must be `SETUP_FAILED`, never a diagnostics count.

3. **Pre-flight check (cheap, before the long GBS run).** Resolve the build dependencies against the configured repos. A dependency query that does not start a build, or a repodata grep for `secureboot-signer` and `vd-kernel-dtb-devel`, is fine. Stop in under a minute if any is missing.

4. **Keep everything else unchanged.** That covers source revision `fae92f99…`, the sources and pins, the locks (`pm0012-queue.lock` and the `heavy.lock` pair, `LOCK_NB`), the per-lane follower, packet format, and the workspace-only writes.

## What the PM expects the real enumeration to show

This is not a gate; it is a prediction for you to confirm or refute. The source context your packet already captured shows ARM-only (A32) instructions in VDLinux-modified files, with no `ARM()`/`THUMB()` alternatives:

| File | Code | Why Thumb-2 rejects it |
|---|---|---|
| `arch/arm/lib/backtrace-clang.S:19` | `stmia r0, {r0 - r15}` | T32 STM cannot include SP or PC |
| `arch/arm/kernel/entry-armv.S` `check_extension`/`check_overflow` (≈225, 303) | `mov r8, sp, lsr #PAGE_SHIFT` | T32 does not allow SP as a shifted register operand |
| `entry-armv.S` ≈365 | `ldmia sp, {r0 - pc}^` | no exception-return LDM in T32 |
| `entry-armv.S` ≈301, 226 | `lsr r7, #PAGE_SHIFT` / `lsl r8, #…` (two-operand shift aliases) | check the UAL form under Clang IAS in T32 |

The enumeration must report **every** error with file, line and macro-expansion origin (`make -k`, the full error list, not just the first). Then, as a separate deliverable, propose a **minimal patch**, kept in the workspace and not applied to P4 yet:
- mainline-style `ARM()`/`THUMB()` variants, or an explicit `.arm` section for these VDLinux handlers;
- ARM behaviour must stay byte-identical: prove that the K1 (A32) `.text` and `.o` hashes for the touched objects are unchanged.

## Deliverable

1. A new pin and the hash-pinned `enumerate.sh` launch command for the PM to review.
2. After the run, a packet with `ENUM_RESULT COMPLETE n diagnostics …` and `make_k_seen true`.

Do not submit anything to GitHub from the Native Server.
