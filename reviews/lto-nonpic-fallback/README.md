# Independent review of the regular-LTO non-PIC fallback

Review [the full patch](../../artifacts/patches/lto-nonpic-in-pic-output-fallback.patch) using [the original review prompt](REVIEW_PROMPT.md). Write findings in this directory as `REVIEW-<name>-<date>.md`.

| Input | SHA-256 |
| --- | --- |
| Full patch, 944 lines | `7d89083453e1d75707a4a6b3a6d9510a4c31e09d8e99865de2a18e07945bf76f` |
| Review prompt | `925199f30e857543401ea3f240ea18b1eb82069df7312abdff2807cbae361be2` |

The three archived parts reconstruct the full patch byte for byte. The bytes also match the retained Official OBS source file. Its companion spec declares `Source1005` and applies it during prep with `patch -p1 --fuzz=0`. The Official source pin records the same SHA-256 and OBS file MD5 `4e74b6a945ef50e3ad1887a133b6e6ad`.

The retained Customized rev12 source-directory check matched the complete expected file manifest, including that same Source1005 MD5. The retained rev12 spec declares and applies Source1005, and its SHA-256 matches the OBS submission receipt. The two successful rev12 buildinfo records carry `srcmd5=0b38aead137ec42dcd99dee28091acc1`. This establishes the OBS source match for both lanes. The native Source1005 comparison subsequently returned the full review-copy digest for both SRPM payloads (Official -9.1 and Custom -11.1). Independent review findings are outstanding. [Native comparison](../../artifacts/evidence/native-run-r0012r-image-mKv04z-erofs-20261125.txt)

The `wrap-unreferenced-before-codegen.test` hunk updates an existing upstream test. It expects the GOT relocation introduced by the Tizen fallback for `__emutls_v.x` and makes the shared section-index assertion independent of the extra section. The existing wrapper assertions still check `__wrap_malloc`. Upstream introduced the test with the separate 2022 wrapping fix. [LLVM D124056 and commit 1af25a986069](https://reviews.llvm.org/D124056)
