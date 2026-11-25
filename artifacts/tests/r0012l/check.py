"""Exercise the native analysis against a small ARM ELF constructed without a host compiler."""
import base64
import contextlib
import hashlib
import io
import os
from pathlib import Path
import runpy
import struct
import subprocess
import tempfile
import zlib

root=Path(__file__).resolve().parents[3]
scripts=root/'artifacts/scripts'
def load(path): return runpy.run_path(str(scripts/path))
q=load('r0012l/kernel-qualification.py.txt')
audit=load('r0012f/kernel-audit.py.txt')
scan=load('r0004/image_mode_scan.py.txt')['secs_of']
trace=load('r0012l/trace-symbolize.py.txt')
sha=lambda b:hashlib.sha256(b).hexdigest()

def elf():
    text=struct.pack('<4I',0xeb000000,0xe12fff1e,0xe1a00000,0xe12fff1e)
    names=b'\0meminfo_proc_show\0OUTLINED_FUNCTION_0\0$a\0'
    syms=bytes(16)+struct.pack('<IIIBBH',names.index(b'$a'),0x1000,0,0,0,1)
    for name,va in ((b'meminfo',0x1000),(b'OUTLINED',0x1008)):
        syms+=struct.pack('<IIIBBH',names.index(name),va,8,2,0,1)
    note=struct.pack('<III',4,20,3)+b'GNU\0'+bytes(range(20))
    ex=struct.pack('<IIII',(0x1008-0x2000)&0x7fffffff,0x80b0b0b0,(0x1010-0x2008)&0x7fffffff,1)
    sections=[('',0,0,b'',0,0,0),('.text',1,6,text,0x1000,0,0),('.strtab',3,0,names,0,0,0),
              ('.symtab',2,0,syms,0,2,16),('.note.gnu.build-id',7,2,note,0x1800,0,0),
              ('.rodata',1,2,b'abc',0x1900,0,0),('.data',1,3,b'ab',0x1910,0,0),
              ('.bss',8,3,bytes(8),0x1920,0,0),('.init.text',1,6,bytes(8),0x1980,0,0),
              ('.ARM.exidx',0x70000001,0x82,ex,0x2000,1,8)]
    attrs=b"\x06\x0a\x08\x01\x09\x02"  # CPU_arch=v7; ARM_ISA_use; THUMB_ISA_use
    sub=b"\x01"+struct.pack("<I",5+len(attrs))+attrs
    vendor=b"aeabi\0"+sub
    sections.append((".ARM.attributes",0x70000003,0,b"A"+struct.pack("<I",4+len(vendor))+vendor,0,0,0))
    tab='\0'.join(x[0] for x in sections)+'\0.shstrtab\0'
    sections.append(('.shstrtab',3,0,tab.encode(),0,0,0))
    data=bytearray(52); data[:7]=b'\x7fELF\x01\x01\x01'
    struct.pack_into('<HHI',data,16,2,40,1)
    struct.pack_into('<IHHHHHH',data,36,0x05000000,52,0,0,40,len(sections),len(sections)-1)
    headers=bytearray()
    for name,kind,flags,b,va,link,ent in sections:
        data+=bytes((-len(data))%4)
        headers+=struct.pack('<10I',tab.index(name+'\0'),kind,flags,va,len(data),len(b),link,4 if kind==2 else 0,4,ent)
        data.extend(b)
    data+=bytes((-len(data))%4)
    struct.pack_into('<I',data,32,len(data))
    return bytes(data+headers),text

with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as tmp:
    w=Path(tmp); blob,txt=elf(); e=w/'vmlinux'; e.write_bytes(blob)
    buildid=q['build_id'](e)
    assert buildid==bytes(range(20)).hex()
    table=w/'System.map'
    table.write_text('1000 T _text\n1900 T __init_begin\n2000 T __init_end\n3000 B _end\n')
    assert q['resident'](table)==0x1900
    (w/'.config').write_text('CONFIG_A=y\n')
    assert q['keep_symbols'](w,w,'K0',lambda p:sha(p.read_bytes()))['build_id']==buildid
    raw=b'payload'+txt+bytes(64)
    (w/'uImage').write_bytes(bytes(12)+len(raw).to_bytes(4,'big')+bytes(48)+raw)
    qual=q['qualify']
    qual.__globals__['PAYLOAD']=sha(raw)
    rec={'symbols':{'build_id':buildid},'images':{'uImage':[11348968,''],'zImage':[5326504,'']}}
    cfg={'BUILD_ID':buildid,'IMAGES':w}
    def result(same=True):
        return qual(w,w,rec,cfg,{'local_paths':lambda _:('',w/'missing',[])},scan,same)
    assert result()['status']=='OFFICIAL_PERF_BUILD_CONFIG'
    assert result(False)['status']=='K0_CONFIG_MISMATCH'
    rec['images']['zImage'][0]-=1
    assert result()['status']=='K0_OUTPUT_UNQUALIFIED'
    cfg['BUILD_ID']='00'*20
    assert result()['section_comparison']=='NO_MATCHED_ELF'
    a=w/'a'; b=w/'b'
    a.write_text('CONFIG_A=y\n'); b.write_text('# note\nCONFIG_A=y\n')
    with contextlib.redirect_stdout(io.StringIO()) as s:
        assert not q['config_diff'](a,b,w/'diff')
    assert s.getvalue()==(w/'diff').read_text()
    b.write_text(''.join(f'# {i}\n' for i in range(120)))
    with contextlib.redirect_stdout(io.StringIO()) as s:
        assert not q['config_diff'](a,b,w/'diff')
    assert zlib.decompress(base64.b64decode(s.getvalue().split()[-1]))==(w/'diff').read_bytes()
    # Use real readelf and objdump on the fixture ELF.
    for k in ('CONFIG_UNWINDER_FRAME_POINTER','CONFIG_UNWINDER_ARM'):
        out=audit['audit'](w,e,scan,{k:'y','CONFIG_FRAME_POINTER':'y'})
        h=out['helpers'][0x1008]
        assert h['calls'][0]['caller']=='meminfo_proc_show' and h['body'],h
        if k.endswith('_ARM'):
            assert h['unwind']=='LEAF_FINISH_STATIC_MATCH',h
        else: assert 'frame_review' in h['calls'][0]
    def mode(op,prev='',after='',end='bx lr'):
        def ins(s): return (0x1000,*s.split(' ',1))
        return audit['classify']({'op':op,'addr':0x1000,'before':[ins(prev)] if prev else [],
                                'after':[ins(after)] if after else []},[ins(end)])
    assert mode('b')=='TAIL_CALL'
    assert mode('bl','mov r4, lr','mov lr, r4')=='LR_REGISTER'
    assert mode('bl','str lr, [sp, #-4]!','ldr lr, [sp], #4')=='LR_STACK'
    assert mode('bl','str lr, [sp, #-0x8]!','ldr lr, [sp], #8')=='LR_STACK'
    assert mode('bl',end='b 0x2340 <fn>')=='THUNK'
    assert mode('bl','nop x','add r0, r1')=='NO_LOCAL_LR_SAVE'
    assert mode('bne')=='UNRESOLVED'
    assert trace['frames']('[<c0001235>] from [<c0000010>]')==['c0001235','c0000010']
    assert trace['frames']('pc : c0001234 lr : 0xc0000020')==['c0001234','c0000020']
    patch=root/'artifacts/patches/kernel/perf-machine-outliner.spec.patch'
    spec=w/'spec';spec.write_text('%build\n'+load('r0008a/gbs-mlgo-t7.py.txt')['INSTRUMENT'])
    subprocess.run(['patch','--batch','--fuzz=0',spec,patch],check=True)
    section=spec.read_text()
    subprocess.run(['sh','-n'],input=section.partition('%build\n')[2],text=True,check=True)
    for forbidden in ('realpath','readlink -f','--reference','sort -V','timeout ','truncate ','--strict','--ignore-missing','PROCINFO','@include'):
        assert forbidden not in section,forbidden
    assert set(section.split('for pm_tool in ',1)[1].split(';')[0].split())==set(
        'mkdir cat clang ld.lld armv7l-tizen-linux-gnueabi-clang make grep sha256sum cut cp find xargs touch chmod sed rpm readelf'.split())
    # Exercise the exact injected make wrapper in a constrained buildroot-style PATH.
    tools=w/'allowed';tools.mkdir()
    import shutil
    for name in ('cp','find','xargs','grep','chmod','mkdir','sha256sum','cut','touch'):
        (tools/name).symlink_to(shutil.which(name))
    script=w/'make-wrapper';script.write_text(section.partition("<<'PMMAKE'\n")[2].partition('\nPMMAKE\n')[0].replace('%%','%'))
    for name in ('arch/arm/Makefile','scripts/Kbuild.include','arch/arm/boot/zImage','kernel/sched/core.o.pm0012f-options','.core.o.cmd','core.o'):
        f=w/name;f.parent.mkdir(exist_ok=True,parents=True);f.write_text('OUTLINED_FUNCTION_0')
    with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as receipt_dir:
        env={**os.environ,'PATH':str(tools),'PM_KERNEL_LANE':'K1','PM_REAL_MAKE':'/bin/true','PM_KERNEL_EVIDENCE':receipt_dir}
        for key in ('PM_REAL_MAKE','PM_KERNEL_LANE','PM_KERNEL_EVIDENCE'):
            (w/key).write_text(env.pop(key)+'\n')
        (w/'stage').write_text('install\n')
        subprocess.run(['/bin/sh',script],env=env,cwd=w,check=True)
        snapshot=Path(receipt_dir)/sha((w/'arch/arm/boot/zImage').read_bytes())
        assert (snapshot/'complete').exists() and (snapshot/'System.map').read_bytes()==table.read_bytes()
        assert (snapshot/'core.o').is_file()
print('PASS K0 identity and raw-only gates, config diff packet, retained symbols, static sizes, real ARM ELF direct edge and EHABI range, LR shapes, offline trace parser and buildroot command inventory')
