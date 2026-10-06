#!/usr/bin/env python3
"""Deliberate-break test: copy an output folder to a scratch dir, break three things, run the checker on each break and on all three.
usage: break_test.py <output_folder> <scratch_dir>"""
import os, shutil, subprocess, sys

src, scratch = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
chk = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'check_filing.py')


def find(root, pat, ext=''):
    return sorted(os.path.join(d, f) for d, _, fs in os.walk(root) for f in fs if pat in f and f.endswith(ext))


def move_file(r):
    p = find(r + '/box/Clients', 'kestrel-document-production', '.eml')[0]
    os.makedirs(r + '/box/Firm_Admin', exist_ok=True)
    shutil.move(p, r + '/box/Firm_Admin/')
    return f'moved {os.path.basename(p)} out of its matter Correspondence folder into box/Firm_Admin/'


def corrupt_stub(r):
    p = find(r + '/box', '.xref.txt')[0]
    open(p, 'w').write('Filed at: box/Clients/1009 Nowhere/missing.eml\n')
    return f'overwrote stub {os.path.basename(p)} with a path that does not exist'


def rename_att(r):
    p = find(r + '/box', 'delivery_logs_mar-may.pdf')[0]
    os.rename(p, os.path.join(os.path.dirname(p), 'renamed_delivery_logs.pdf'))
    return 'renamed extracted attachment 2026-08-03_delivery_logs_mar-may.pdf to renamed_delivery_logs.pdf'


def run(d):
    p = subprocess.run([sys.executable, '-I', chk, d, '--inputs', os.path.join(os.path.dirname(chk), '..')], capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


shutil.rmtree(scratch, ignore_errors=True)
ok = True
for name, fns in [('break_move', [move_file]), ('break_stub', [corrupt_stub]), ('break_attachment', [rename_att]),
                  ('break_all_three', [move_file, corrupt_stub, rename_att])]:
    d = os.path.join(scratch, name)
    shutil.copytree(src, d)
    what = [f(d) for f in fns]
    rc, out = run(d)
    print(f'## {name}: ' + ' + '.join(what))
    print(f'exit code {rc} ({"CAUGHT" if rc else "NOT CAUGHT"})')
    print('\n'.join('    ' + l for l in out.splitlines()[:12]))
    ok &= rc != 0
print('RESULT: all breaks caught' if ok else 'RESULT: a break was NOT caught')
sys.exit(0 if ok else 1)
