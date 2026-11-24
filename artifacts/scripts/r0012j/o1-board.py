"""Read O1 measurements via a single designated SDB serial. All output is host-side."""
import argparse
import base64
import gzip
from pathlib import Path
import re
import subprocess
import time

SERIAL = "192.168.108.25:26101"
BASE = ["sdb", "-s", SERIAL]
def call(cmd, timeout=90):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    return p.returncode, p.stdout.replace(b"\r\n", b"\n")

def shell(command, timeout=90):
    # Send one shell argument, including on clients whose SDB shell uses a pty.
    end = "PM_O1_REMOTE_STATUS"
    rc, data = call(BASE+["shell","(\n"+command+"\n)"+'\nr=$?; printf "\\n'+end+' %s\\n" "$r"'], timeout)
    body, sep, status = data.rpartition(("\n"+end+" ").encode())
    if rc or not sep:
        raise RuntimeError("SDB transport: "+repr(data[-300:]))
    return int(status.strip()), body

def write(out, name, data):
    path = out/name
    with path.open("xb") as f: f.write(data)

def read(out, name, command, timeout=90):
    rc, data = shell(command, timeout)
    write(out,name,data)
    with (out/"returncodes.tsv").open("a") as f: print(name,rc,sep="\t",file=f)
    return rc,data

DT = r'''
t=/proc/device-tree
for n in "$t" "$t"/memory* "$t"/reserved-memory "$t"/reserved-memory/*; do
    test -d "$n" || continue
    printf 'NODE\t%s\n' "$n"
    for k in '#address-cells' '#size-cells' device_type reg size alignment alloc-ranges no-map reusable compatible status; do
        test -e "$n/$k" || continue
        printf 'PROP\t%s\t' "$k"
        od -An -v -tx1 "$n/$k" | tr -d ' \n'
        printf '\n'
    done
done
'''
TARGET = r'''
rpm -qa --qf '%{NAME}\n' | grep -Ei 'avcontrol|tv-viewer|libpisa-ipc|webserver|libgcrypt|^rpm($|-)|nnstreamer' |
while IFS= read -r pkg; do
    printf 'PACKAGE\t%s\n' "$pkg"
    rpm -ql "$pkg" | while IFS= read -r f; do
        test -f "$f" || continue
        case "$f" in /usr/lib/debug/*) continue;; esac
        hdr=$(od -An -tx1 -N20 "$f" 2>/dev/null | tr -d ' \n')
        case "$hdr" in 7f454c46* ) ;; *) continue;; esac
        size=$(stat -Lc %s "$f") || continue
        h=$(sha256sum "$f") || { echo "HASH_ERROR $f"; continue; }
        printf 'ELF\t%s\t%s\t%s\t%s\t%s\n' "$pkg" "$f" "$size" "${h%% *}" "$hdr"
    done
done
'''
PROC = r'''
for f in /proc/[0-9]*/stat; do
    case "${f#/proc/}" in *[!0-9]*/stat) continue;; esac
    test -r "$f" || continue
    IFS= read -r st <"$f" 2>/dev/null || continue
    tail=${st##*) }; set -- $tail
    p=${f#/proc/}; p=${p%/stat}
    cn=${st#*(}; cn=${cn%)*}
    if test -r "/proc/$p/smaps_rollup"; then
        kb=$(awk '$1=="Pss:" {print $2}' "/proc/$p/smaps_rollup" 2>/dev/null)
    else kb=; fi
    printf '%s\t%s\t%s\t%s\n' "$p" "${kb:--}" "${20}" "$cn"
done
'''
def root_mode(enable):
    rc,data=call(BASE+["root","on" if enable else "off"],20)
    for _ in range(15):
        try:
            status,value=shell("id -u",5)
            if not status and value.strip().isdigit() and ((value.strip()==b"0")==enable): return
        except (RuntimeError,subprocess.TimeoutExpired): pass
        time.sleep(1)
    raise RuntimeError("root transition did not verify "+str(rc)+" "+repr(data[-200:]))

def privileged(function):
    rc,uid=shell("id -u")
    if rc: raise RuntimeError("identity unavailable")
    try:
        if uid.strip()!=b"0": root_mode(True)
        function()
    finally:
        root_mode(False)

def inventory(out):
    for name,args in (("devices.txt",["sdb","devices"]),("capability.txt",BASE+["capability"])):
        rc,data=call(args)
        if rc: raise RuntimeError(name)
        write(out,name,data)
    read(out,"identity.txt",'''cat /proc/version; uname -a; cat /proc/sys/kernel/random/boot_id
for f in /etc/info.ini /etc/tizen-release /etc/os-release; do echo FILE "$f"; cat "$f"; done
for f in /lib/modules/perf/*/kernel/vmlinux /perf/zImage /perf/uImage /sys/kernel/btf/vmlinux; do test -f "$f" && sha256sum "$f"; done
if test -r /sys/kernel/notes; then echo KERNEL_ELF_NOTES; od -An -tx1 -v /sys/kernel/notes; fi
rpm -q tztv-kernel-perf''')
    rc,data=read(out,"rpm-query.txt",r"""rpm -qa --qf '%{NAME}\t%{EPOCHNUM}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{SOURCERPM}\n'""")
    rows=data.splitlines()
    if rc==0 and rows and all(len(r.split(b'\t'))==6 for r in rows):
        write(out,"installed-rpms.tsv",b'\n'.join(sorted(rows))+b'\n')
    read(out,"targets.tsv",TARGET,420)
    read(out,"meminfo.txt","cat /proc/meminfo")
    read(out,"cmdline.txt","cat /proc/cmdline")
    read(out,"zoneinfo.txt","cat /proc/zoneinfo")
    read(out,"vmstat.txt","cat /proc/vmstat")
    read(out,"swap.txt",'''cat /proc/swaps; for d in /sys/block/zram*; do test -d "$d" || continue; for n in disksize mm_stat compr_data_size orig_data_size mem_used_total; do test -r "$d/$n" || continue; printf '%s ' "$d/$n"; cat "$d/$n"; done; done''')
    def protected():
        read(out,"iomem.txt","cat /proc/iomem")
        read(out,"device-tree.tsv",DT)
        read(out,"dmesg-memory.txt",r"""dmesg | grep -iE 'Memory:|cma:|reserved.memory|reserved mem|carve.?out|zone ranges|early memory node'""")
        rc,compressed=shell('if test -r /proc/config.gz; then base64 /proc/config.gz; else exit 44; fi')
        if rc==0: write(out,"effective.config",gzip.decompress(base64.b64decode(b"".join(compressed.split()),validate=True)))
        write(out,"config-status.txt",("PROC_CONFIG_READ\n" if rc==0 else "PROC_CONFIG_ABSENT_OR_UNREADABLE "+str(rc)+"\n").encode())
        read(out,"process-candidates.tsv",r'''getconf CLK_TCK; for d in /proc/[0-9]*; do IFS= read -r c < "$d/comm" 2>/dev/null || continue; first=$(tr '\000' '\n' <"$d/cmdline" 2>/dev/null | head -1); case "$c $first" in *[Hh][Oo][Mm][Ee]*|*auncher*) printf '%s\t%s\t%s\n' "${d#/proc/}" "$c" "$first";; esac; done''')
    privileged(protected)
    read(out,"root-restored.txt","id -u")

def followup(out):
    def protected():
        read(out,"kernel-receipt.txt", """rpm -q --dump tztv-kernel-perf | grep -E '/(vmlinux|[uz]Image) '
rpm -ql org.tizen.tv-viewer org.tizen.AVControl | grep -E '/bin/|[.]tpk$'
ls -ld /lib/modules/* /sys/kernel/btf /proc/config.gz
for x in /prd/prd_info.ini /etc/prd_info.ini /prd/info.ini /mnt/prd/prd_info.ini; do
    if test -r "$x"; then sha256sum "$x"; cat "$x"; fi
done""")
        read(out,"target-apps.tsv", "printf '%s\\n' org.tizen.AVControl org.tizen.tv-viewer | "+
             TARGET[TARGET.index("while IFS="):])
        read(out,"boot-memory-log.txt", """if command -v journalctl >/dev/null; then journalctl -b -k --no-pager | grep -iE 'Memory:|cma:|reserved mem|carve.?out' | head -100; fi
for f in /var/log/dmesg /proc/bootkpi; do if test -r "$f"; then grep -iE 'Memory:|cma:' "$f"; fi; done
ls -l /proc/device-tree/memory_tbl/ | head -60
cat /proc/sys/kernel/random/boot_id; getconf PAGESIZE""")
    privileged(protected)
    read(out,"followup-uid.txt","id -u")

def sample(out, number, boot):
    rc,observed=shell("cat /proc/sys/kernel/random/boot_id")
    if rc or observed.strip().decode()!=boot: raise ValueError("boot ID changed")
    prefix=f"idle-{number}-"
    read(out,prefix+"clock.txt","cat /proc/sys/kernel/random/boot_id /proc/uptime; getconf CLK_TCK; date -u")
    read(out,prefix+"meminfo.txt","cat /proc/meminfo")
    privileged(lambda: read(out,prefix+"pss.tsv",PROC,120))
    read(out,prefix+"end.txt","cat /proc/sys/kernel/random/boot_id /proc/uptime; id -u")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("mode",choices=["inventory","sample","followup"])
    ap.add_argument("out",type=Path)
    ap.add_argument("--number",type=int,choices=range(1,4))
    ap.add_argument("--boot")
    a=ap.parse_args()
    if a.mode=="inventory": inventory(a.out)
    elif a.mode=="followup": followup(a.out)
    else: sample(a.out,a.number,a.boot)
