# armv7l Thumb-2 trial patches

The package hunks retain the EFL define and restore the distribution flags at two recorded assignments. The matched sources and actual command counts are in [the flag-origin ledger](../../ledger/thumb-flag-origins-20261124.tsv). The tv-viewer CMake file still selects -O1 for a subset of its C++ sources. A size change in either spec lane includes all restored options.

The independent default lane uses the clang-force-options RPM from clang-contrib. Its build macro adds the marked block in [scoped-clang.cfg.diff](scoped-clang.cfg.diff) to the build root's /usr/bin/clang.cfg. The observed /usr/bin/clang++.cfg is a symlink to that file. The script saves the complete per-lane build.conf diff and the effective driver command. The macro removes the block after the build. The policy supplies -mthumb and -mimplicit-it=thumb, with the helper's exemption lists and the kernel and module owner list. Apply the package and default layers in separate fresh roots.

Review additional source hunks against the exact source RPM and VCS in the Official roster. Record the image path, ELF hash, byte range and cause evidence in [the reviewed range ledger](../../ledger/official-37736448-thumb-reviewed.tsv). Group (c) entries need a documented reason for -marm. Group (b) entries need a source location and assembly evidence. Missing evidence keeps the range unresolved.
