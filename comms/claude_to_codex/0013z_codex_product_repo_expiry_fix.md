# 0013z — The K4 product repo expired: use the new LLVM Official QB product (PM decision)

**Evidence (archive under `artifacts/evidence/`):**

| File | SHA-256 |
|---|---|
| `native-run-r0013y-source-4y1y4P-r0013x-enum-7Za3F6-20261127.txt` | `afda4c91bab6166318d920ff78d02688fc4665ddf08c9e8c7dd0de9849861766` |
| `native-run-r0013x-repo-probe-v1-lzma-20261127.txt` | `13a15f0640b58cbe998758a9136a378e93406ef7c9c63fe6860d69dc6771698a` |
| `native-run-r0013x-repo-probe-20261127.txt` | `fb49327b18d50fcb46f939dbb1503cf3cf7cf4da049d1f63cc9354995c309bb2` |

The v1 probe failed because the native pyenv 3.10.12 has no `_lzma`. Keep that in mind for any script that imports `lzma`: use an `xz` subprocess instead. The v2 probe is the PM's read-only probe.

## Results

1. **0013y source check: `SOURCE_EQUIV PASS scope=seven-files`.** K1 `9066e12a…` and jEMVH7 `8b0eec57…` both hold the 14427407 bytes for all 7 files, so CL 14507546 is the measured source. Record this and close section 2b.

2. **r0013x enumeration `7Za3F6`: `SETUP_FAILED deps HTTP Error 404`.** It stopped in the pre-flight check, with no locks and no sudo, as designed. `ENUM_INPUT` confirms that the K4 config used product `b776/19414776 …RELEASE_20261123.2`, which is the old Official QB 37736448.
   - **PM correction to 0013x:** "TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE" is the naming of every KantSU2e product artifact. It is not an ASAN-instrumented build, and r0013n did use K4's own repo, as you suspected.
   - **Root cause:** private QB (PRV) artifacts expire after a few days.

3. **Repo probe (v2):**

| Product repo | Origin | root / repodata | secureboot-signer | vd-kernel-dtb-devel |
|---|---|---|---|---|
| 20261123.2 `b776/19414776` (used by K4) | old Official 37736448 | 404 / 404 | — | — |
| 20261123.1 `b755/19414755` | old Custom 37736427 | 404 / 404 | — | — |
| 20261118.2 `b993/19368993` | — | 404 / 404 | — | — |
| DO_NOT_DELETE 20261113.1 | permanent daily product (**GCC-built, not usable**) | 200 / 200 | pkg | pkg |
| **20261125.1 `b567/19437567`** | **new Official 37777148 (use this)** | 200 / 200 | pkg | pkg |
| 20261125.2 `b655/19437655` | **new Custom 37777264** | 200 / 200 | pkg | pkg |
| base 20261113.1 | base | 200 / 200 | MISSING | MISSING |

These two packages come only from the product repo.

## PM decision (operator-confirmed)

The DO_NOT_DELETE 20261113.1 product is a **GCC-built** daily product, so it is **not** acceptable for LLVM kernel work, even though it provides both packages. Product repos must come from the current LLVM QBs. The old pair (37736448 / 37736427) is retired; ignore it. The current pair uses the same base URL, base CL and shelf as the old one.

| Lanes built on | Product repo to use |
|---|---|
| Official base 20261113.1 (K0–K5, the r0013x enumeration, the Thumb-2 patch builds) | **new Official 37777148:** `http://repos.vd.sec.samsung.net/priv/168.219.236.43:81/PRV/builds/b567/19437567/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261125.1/` |
| Custom base 20261118.1 (if ever needed) | **new Custom 37777264:** `http://repos.vd.sec.samsung.net/priv/168.219.236.55:81/PRV/builds/b655/19437655/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261125.2/` |

**When a QB product expires (404), the operator will build a new LLVM QB and give the PM its URL.** Do not hard-wire a single URL forever.

Implementation:
1. Keep the K4 provenance trace, but **substitute only `repo.product_NikeM`**. The substitute comes from a launcher argument, `PRODUCT_URL`. Default it to the 20261125.1 URL above.
   - Validate the host and the `…/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_<date>.<n>/` form.
   - Reject the DO_NOT_DELETE path and any product that is not an LLVM QB.
   - Print `PRODUCT_SUBSTITUTED <old> -> <new>` in `ENUM_INPUT`.
2. The pre-flight check must pass with the substitute. If it returns 404, stop with `ENUM_RESULT SETUP_FAILED product-expired <url>` and the line `NEED new LLVM Official QB product URL`, then exit. Never fall back to a GCC or daily product.
3. Everything else stays as at `3a1362f`: the base 20261113.1, the locks, the resource checks, the keep-going wrapper and the packet format.
4. **A32 control (required with the patch later):** before you claim that any Thumb-2 patch leaves A32 byte-identical, rebuild K1 (A32) once with the substituted product. Show that its `.text` is still 8,214,312 and its Image is 10,996,388. This proves that the product swap alone does not change the kernel. It can run in the same session as the post-patch K4 build. You don't need it for the error inventory.

## S12 consequence

PRV artifacts disappear within about 2–4 days. `qb-evidence/` already keeps `tztv-kernel`, `-devel`, `-perf` and `-release` RPMs for the S12 baselines **37777148** and **37777264**; ignore the old pair. Confirm that, or make it so:

- S12 reads the **baselines from those retained, checksum-verified RPMs** when the URL is gone, and only falls back to the network if they are missing.
- On its first successful read of each **new outline QB**, S12 retains that QB's RPMs into `qb-evidence/<QB>-<release>/`, the same way. If any module RPM S12 needs is not among the four retained packages, retain it too.
- `S12 PASS|FAIL` semantics stay unchanged.

## Deliverable

- A new pin.
- The hash-pinned launch commands for (a) the r0013x enumeration, with an optional `PRODUCT_URL` argument, and (b) S12, if its script changes.
- A note in `STATUS.md` that PRV QB artifacts expire, so S12 must run within a day of the QBs finishing.

No GitHub submission from the Native Server.
