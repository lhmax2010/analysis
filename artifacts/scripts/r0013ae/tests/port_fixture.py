import hashlib, json, os, re, runpy, shutil, subprocess
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[4]
W=R.parent
S=R/'artifacts/scripts/r0013ae'
F=Path(sys.argv[1]).resolve()
if not F.is_relative_to(W):raise ValueError('fixture output outside workspace')
F.mkdir(parents=True,exist_ok=True)
os.environ.update(TMPDIR=str(F),PYTHONDONTWRITEBYTECODE='1',LC_ALL='C')
p=runpy.run_path(str(S/'port.py.txt'))
ev=json.loads((R/'artifacts/evidence/stooH5-enumeration-20261127.json').read_bytes())
src=ev['source_context']
lines=['\n']*395
for i,s in src[p['ENTRY']]:
 if i<=395:lines[i-1]=s+'\n'
for i in (258,335):
 lines[i-1]='\tmov r8,r7\n'; lines[i]='\teor r8,r8,sp\n'
lines[269]='\tsub sp,r7,#START_SP\n'
lines[345]='\tsub sp,r7,#(SVC_REGS_SIZE + 8)\n'
header=r""".macro svc_exit, rpsr, irq=0
@ Thumb mode SVC restore
 ldr lr,[sp,#S_SP]
 ldrd r0,r1,[sp,#S_LR]
 strex r2,r1,[sp,#S_LR]
 stmdb lr!,{r0,r1,\rpsr}
 ldmia sp,{r0-r12}
 mov sp,lr
 ldr lr,[sp],#4
 rfeia sp!
#endif
.endm
"""
src=p['edit_entry'](''.join(lines),header)
dump=p['edit_dump'](''.join(t+'\n' for i,t in ev['source_context'][p['DUMP']])) .split('/* fp')[0]
# Assemble the actual generated return block, page-boundary tests and dump island.
# Keep addressing directions and macro scope as in __dabt_svc.
start=src.index('#ifdef CONFIG_THUMB2_KERNEL\n        @ The IRQ-stack')
ret=src[start:src.index('#line 366',start)]
island=src[src.index('#if defined(CONFIG_THUMB2_KERNEL) &&'):src.index('#line 370')]
dump=dump[dump.index('THUMB(.arm;)'):]
asm=r"""
.syntax unified
.text
.macro ret reg
 bx \reg
.endm
#define S_SP 52
#define S_PSR 64
#define S_LR 56
#define PAGE_SIZE 4096
#define CONFIG_KERNEL_STACK_SMALL 1
#define disable_irq_notrace cpsid i
#define UNWIND(x...) x
#define ENTRY(x) .globl x; .p2align 2; x:
#define ENDPROC(x) .type x,%function; .size x,.-x
#ifdef CONFIG_THUMB2_KERNEL
.thumb
#define ARM(x...)
#define THUMB(x...) x
#else
.arm
#define ARM(x...) x
#define THUMB(x...)
#endif
"""+island+'\n.macro flow\n'+ret+'\n.endm\n.globl __dabt_svc\n__dabt_svc:\nflow\n'+dump
for mode in ('arm','thumb'):
 inp=subprocess.check_output(['cpp','-P','-undef','-x','assembler-with-cpp',*(['-DCONFIG_THUMB2_KERNEL'] if mode=='thumb' else []),'-'],input=asm.encode())
 f=F/(mode+'.o')
 subprocess.run(['llvm-mc','-triple=armv7-linux-gnueabi','-mcpu=cortex-a53','-filetype=obj','-o',f],input=inp,check=True)
 dis=subprocess.check_output(['llvm-objdump','--mcpu=cortex-a53','-d','--no-show-raw-insn',f],text=True)
 (F/(mode+'.dis')).write_text(dis)
 if mode=='thumb':
  assert 'rfeia' in dis and 'pm_small_stack_arm_return' in dis and 'bx\tlr' in dis and '^' in dis,dis
print('MC fixture ARM and Thumb mixed-state return, IRQ frame restore, EHABI and dump island assembled')
for i,original in ((225,225),(258,258),(259,259),(270,270),(303,303),(335,335),(336,336),(346,346)):
 line=next(l for l in src.splitlines() if 'ARM(' in l and p['normal'](lines[original-1]) in p['normal'](l))
 snippet=asm.split('#if defined(CONFIG_THUMB2_KERNEL) &&',1)[0]+'\n#define PAGE_SHIFT 12\n#define START_SP 8\n#define SVC_REGS_SIZE 80\n'+line+'\n'
 for mode in ('arm','thumb'):
  flags=['-DCONFIG_THUMB2_KERNEL'] if mode=='thumb' else []
  raw=subprocess.check_output(['cpp','-P','-undef','-x','assembler-with-cpp',*flags,'-'],input=snippet.encode())
  subprocess.run(['llvm-mc','-triple=armv7-linux-gnueabi','-mcpu=cortex-a53','-filetype=obj','-o',F/'instruction.o'],input=raw,check=True)
print('Eight site forms encoded; page bounds and stack metadata cases checked below')
for off,yes in [(0,False),(4,False),(12,False),(15,False),(16,True),(20,True),(21,False),(4096,True),(4100,False)]:
 take_thumb=(off%4==0 and 16<=off<=4096)
 assert take_thumb==yes
 if take_thumb:assert off-12>=4 and off<=4096
ov=S
for f in ov.glob('*.py.txt'):compile(f.read_bytes(),str(f),'exec')
print('Parser/transform syntax OK')
