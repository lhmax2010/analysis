# KantSU2E board test-file inventory

[Verified] Enumerated regular files under /root at Tue Nov 17 21:41:43 PST 2026. The known retained test directory is `/root/thumb-audit-20261117`. SDB root was temporary and the original shell account was restored. Root application state under `/root/share` is outside the task inventory.

| Board path | Bytes | Purpose |
|---|---:|---|
| `/root/thumb-audit-20261117/capture-board.sh` | 740 | Collection script |
| `/root/thumb-audit-20261117/collector-errors.txt` | 0 | Collector diagnostics |
| `/root/thumb-audit-20261117/complete.txt` | 17 | Completion marker |
| `/root/thumb-audit-20261117/elfmeta-arm` | 3792 | ARM ELF metadata reader |
| `/root/thumb-audit-20261117/elfmeta.bin` | 174495421 | Raw ELF metadata |
| `/root/thumb-audit-20261117/evidence.tar.gz` | 38378537 | Review bundle |
| `/root/thumb-audit-20261117/find-errors.txt` | 247 | Traversal diagnostics |
| `/root/thumb-audit-20261117/identity.txt` | 3230 | Board identity capture |
| `/root/thumb-audit-20261117/paths.bin` | 5905441 | Input path list |
| `/root/thumb-audit-20261117/rpm-errors.txt` | 0 | RPM diagnostics |
| `/root/thumb-audit-20261117/rpm-files.tsv` | 9538821 | Installed RPM ownership capture |
| `/root/thumb-audit-20261117/selftest.bin` | 1185 | Collector self-test data |

New test artifacts use `/root/llvm-pm/<task>/`. Add path, size and purpose after each session.
