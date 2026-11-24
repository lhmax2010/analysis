"""Local evidence gates. No host-side target compilation or link."""
from pathlib import Path
import hashlib
import os
import runpy
import shutil
import struct
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
scripts = root / 'artifacts/scripts'
patch = root / 'artifacts/patches/kernel/perf-machine-outliner.spec.patch'
cfg = runpy.run_path(str(scripts / 'r0012k/official-config.py.txt'))
sha = cfg['file_sha']


def reject(message, fn):
    try:
        fn()
    except ValueError as e:
        assert message in str(e), e
    else:
        raise AssertionError(message)


with tempfile.TemporaryDirectory() as folder:
    work = Path(folder)
    spec = work/'spec'
    instrument = runpy.run_path(str(scripts/'r0008a/gbs-mlgo-t7.py.txt'))['INSTRUMENT']
    spec.write_text('%build\n'+instrument+'echo original body\n')
    subprocess.run(['patch','--fuzz=0','--batch',spec,patch],check=True)
    shell = spec.read_text().partition('%build\n')[2].replace('%%','%')
    subprocess.run(['sh','-n'],input=shell,text=True,check=True)
    wrapper = work/'capture'
    wrapper.write_text(shell.partition("<<'PMLLD'\n")[2].partition('\nPMLLD\n')[0])
    fake = work/'ld.lld'
    fake.write_text('#!/bin/sh\nif [ "$1" = --version ]; then echo "LLD 22.1.8"; else cp /bin/sh vmlinux; fi\n')
    fake.chmod(0o755)
    (work/'link inputs').write_text('"some file.o" vmlinux.a')
    subprocess.run(['sh',wrapper,'@link inputs','-o','vmlinux'],cwd=work,
                   env={**os.environ,'PM_REAL_LLD':str(fake)},check=True)
    for src in ('r0012k/outliner-phase.py.txt','r0012f/kernel-audit.py.txt'):
        shutil.copyfile(scripts/src,work/Path(src).name)
    phase = runpy.run_path(str(work/'outliner-phase.py.txt'))
    link = phase['final_link'](work,sha)
    assert link['argv'] == [str(fake),'@link inputs','-o','vmlinux']
    assert link['response_files']['0'] == '"some file.o" vmlinux.a'
    assert link['retained_match'] == 'SHA256'
    with (work/'vmlinux').open('ab') as f:
        f.write(b'post-link fixture')
    assert phase['final_link'](work,sha)['retained_match'].startswith('GNU_BUILD_ID ')
    note = work/'vmlinux.pm0012k-link/output.notes'
    original = note.read_bytes()
    note.write_text('Build ID: 1234')
    reject('cannot join',lambda:phase['final_link'](work,sha))
    note.write_bytes(original)

    # ELF32 ARM ET_REL with a defined function in .text and a real symbol table layout.
    data=bytearray(320)
    data[:6]=b'\x7fELF\x01\x01'
    struct.pack_into('<HH',data,16,1,40)
    strings=b'\0.text\0.strtab\0.symtab\0OUTLINED_FUNCTION_0\0'
    data[52:52+len(strings)]=strings
    struct.pack_into('<IIIBBH',data,112,strings.index(b'OUTLINED'),0,4,2,0,1)
    struct.pack_into('<I',data,32,152)
    struct.pack_into('<HHH',data,46,40,4,2)
    for i,sec in enumerate([(0,0,0,0,0,0,0,0,0,0),(1,1,6,0,128,4,0,0,4,0),
                            (7,3,0,0,52,len(strings),0,0,1,0),(15,2,0,0,112,16,2,0,4,16)]):
        struct.pack_into('<10I',data,152+40*i,*sec)
    (work/'example.o').write_bytes(data)
    cmd = work/'.example.o.cmd'
    argv = 'clang -D__KERNEL__ -c example.c -moutline -o example.o'
    cmd.write_text('savedcmd_example.o := '+argv+'\n')
    secs=runpy.run_path(str(scripts/'r0004/image_mode_scan.py.txt'))['secs_of']
    verify=lambda:phase['verify'](work,{'CONFIG_LTO_NONE':'y'},secs,sha)
    assert verify()['helper']=='OUTLINED_FUNCTION_0'
    cmd.write_text('savedcmd_example.o := '+argv+' -flto=thin\n')
    reject('LTO or unexpanded',verify)
    cmd.write_text('savedcmd_example.o := '+argv+' -mno-outline\n')
    reject('no compiled native',verify)
    reject('config enables LTO',lambda:phase['verify'](work,{'CONFIG_LTO_CLANG':'y'},secs,sha))

    raw=b'CONFIG_ARM=y\n'+b''.join(f'CONFIG_STUB_{i}=y\n'.encode() for i in range(1000))
    digest=hashlib.sha256(raw).hexdigest()
    bins=('tztv-kernel-perf','tztv-kernel-devel')
    keys=('name','epoch','version','release','arch','srpm')
    rows={name:dict(zip(keys,(name,'0','1','1','armv7l','tztv-kernel-1-1.src.rpm')),sha256=name) for name in bins}
    members={'/perf/.config':(len(raw),digest),'/perf/zImage':(1,cfg['PINS']['zImage'])}
    q={'retained':lambda *_:(work,None,rows),'matched_payload':lambda c,r,p,lib:p['name'],
       'query':lambda pkg,fmt:'\t'.join(rows[pkg][k] for k in keys),
       'member_checksums':lambda rpm:members,
       'extract_member':lambda rpm,name,path,digest,lib:path.write_bytes(raw)}
    assert cfg['devel_config'](work,q)==raw
    members['/perf/zImage']=(1,'0'*64)
    reject('UNVERIFIED',lambda:cfg['devel_config'](work,q))
    rows[bins[1]]['release']='2'
    reject('identity mismatch',lambda:cfg['devel_config'](work,q))
print('PASS spec wrapper, response argv, linked output identity, compile-phase ELF helper, LTO exclusions, devel identity gates')
