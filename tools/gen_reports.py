#!/usr/bin/env python3
"""Generate memo_reply_01..04.md and changes_report.md by diffing the real stage outputs.
usage: gen_reports.py <phase1_dir> <stage1> <stage2> <stage3> <final_dir>"""
import csv, os, re, sys
from collections import Counter

FIELDS = ['category', 'primary_matter', 'xref_matters', 'privilege', 'flags', 'box_path', 'attachments_saved']


def rd(p):
    return list(csv.DictReader(open(p, newline='', encoding='utf-8')))


def load(d):
    log = {r['email_file']: r for r in rd(f'{d}/filing_log.csv')}
    wall = {(r['email_file'], r['screened_person'], r['role'], r['matter']) for r in rd(f'{d}/wall_incidents.csv')}
    priv = Counter((r['date'], r['subject'], r['privilege']) for r in rd(f'{d}/privilege_log.csv'))
    nr = {e for e, r in log.items() if r['category'] == 'needs_review'}
    aa = set()
    cur = None
    for line in open(f'{d}/attorney_actions.md', encoding='utf-8'):
        if line.startswith('## '):
            cur = line[3:].strip()
        m = re.match(r'- \*\*(\S+)\*\*', line)
        if m and cur:
            aa.add((cur, m.group(1)))
    files = set()
    for dp, _, fs in os.walk(f'{d}/box'):
        for f in fs:
            files.add(os.path.relpath(os.path.join(dp, f), d))
    return dict(log=log, wall=wall, priv=priv, nr=nr, aa=aa, files=files, dir=d)


def counts(s):
    L = s['log'].values()
    mats = {}
    for r in L:
        mats[r['primary_matter']] = mats.get(r['primary_matter'], 0) + 1
    return dict(cat=Counter(r['category'] for r in L), mat=Counter(r['primary_matter'] for r in L if r['primary_matter']), files=len(s['files']))


def attorney_counts(d):
    t = open(f'{d}/filing_summary.md').read()
    sec = t.split('## By responsible attorney')[1].split('##')[0]
    return {m.group(1).strip(): int(m.group(2)) for m in re.finditer(r'^\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|$', sec, re.M) if m.group(1) != 'attorney'}


def diff_logs(a, b):
    out = []
    for e in sorted(b['log']):
        ra, rb = a['log'][e], b['log'][e]
        ch = {f: (ra[f], rb[f]) for f in FIELDS if ra[f] != rb[f]}
        if ch:
            out.append((e, rb['subject'], ch))
    return out


def fmt_changes(ch):
    return '; '.join(f'{f}: `{x or "-"}` -> `{y or "-"}`' for f, (x, y) in ch.items())


def setdiff(a, b):
    return sorted(b - a), sorted(a - b)


def section_state(a, b):
    L = []
    ca, cb = counts(a), counts(b)
    aa, ab = attorney_counts(a['dir']), attorney_counts(b['dir'])
    L.append('Counts after the change (before in brackets):')
    L.append('')
    for c in ['matter', 'needs_review', 'firm_admin', 'non_matter', 'duplicate']:
        L.append(f"- {c}: {cb['cat'].get(c, 0)} [{ca['cat'].get(c, 0)}]")
    mm = sorted(set(ca['mat']) | set(cb['mat']))
    L.append('- by matter (changed only): ' + (', '.join(f"{m} {cb['mat'].get(m, 0)} [{ca['mat'].get(m, 0)}]" for m in mm if ca['mat'].get(m, 0) != cb['mat'].get(m, 0)) or 'none'))
    L.append('- by attorney (changed only): ' + (', '.join(f"{p} {aa_} [{aa.get(p, 0)}]" for p, aa_ in sorted(ab.items()) if aa.get(p, 0) != aa_) or 'none'))
    L.append(f"- files in box/: {cb['files']} [{ca['files']}]")
    L.append(f"- wall incidents: {len(b['wall'])} [{len(a['wall'])}]; privilege log entries: {sum(b['priv'].values())} [{sum(a['priv'].values())}]; needs_review emails: {len(b['nr'])} [{len(a['nr'])}]")
    return L


MEMOS = [
    ('01', 'Carla Ruiz (office manager)', '2026-09-28', 'New matter opened - Delgado'),
    ('02', 'Carla Ruiz (office manager)', '2026-09-29', 'Intake decisions'),
    ('03', 'Jonah Hartwell (ethics partner)', '2026-09-30', 'Tran ethical wall - expanded'),
    ('04', 'Carla Ruiz (office manager)', '2026-10-01', 'Client name change'),
]
NOTES = {
    '01': ['Matter 1002-003 "Formation of Delgado Bakery LLC" (folder `1002-003 Delgado Bakery LLC Formation`, Ravi Iyer, open) was added to the matter list for client 1002.',
           'Both bakery emails were waiting in `_Needs_Review`; both moved into the new matter and were filed as ordinary matter emails. The new-matter-request flag was removed from both, as instructed. The earlier one (2026-08-19) predates the matter opening; I filed it there anyway because it is the request the matter covers.',
           'Privilege is AC (only Maria Delgado and Ravi Iyer). No attachments, no stubs, no hold or wall effects.'],
    '02': ['Kestrel (Robert Baines, 2026-08-13): moved from `_Needs_Review` to `box/Firm_Admin/Declined_Intake/`, category firm_admin, privilege n/a. Flag potential-conflict was replaced by declined-intake. I kept new-matter-request because the memo replaces only potential-conflict and the email still asks for services outside every matter. Tell me if you want that flag dropped too.',
           'Matter 1007-002 "Fuel dock damage claim" (folder `1007-002 Fuel Dock Damage Claim`, Jonah Hartwell, open) was added for client 1007. The Blue Heron fuel dock email (2026-08-25) moved from `_Needs_Review` into it; its new-matter-request flag was removed because the matter now exists. Privilege AC.',
           'Nothing else in `_Needs_Review` belonged to either decision. Paul Ostrander\'s brother\'s slip contract request (filed in 1005-001, flags potential-conflict;new-matter-request) is untouched because the memo does not mention it.'],
    '03': ['Tom Weller is now screened from 1003-001 from 2026-08-15 (added to the matter\'s wall list next to Anika Brandt; Anika\'s start date 2026-07-01 is unchanged).',
           'I checked every email filed in or cross-referenced to 1003-001 for Tom as sender, to or cc on or after 2026-08-15. There is one: the 2026-08-26 "Tran mediation - authority" email (Hank Moreau to Mira Osei, cc Tom). It now carries the ethical-wall flag and a new row in wall_incidents.csv (role cc). The ethics partner (you) is on the action list for it.',
           'Not counted: Tom was also copied on Anika Brandt\'s 2026-08-05 deposition outline email, but that predates 2026-08-15. Emails Tom handles on other matters (for example the Kestrel and Rivera emails) are not in 1003-001 and are not incidents. The existing three Anika incidents are unchanged.'],
    '04': ['Client 1001 is now "Brightwater Brands Inc." and its client folder is `1001 Brightwater Brands` (was `1001 Brightwater Foods`). Matter numbers and matter folder names are unchanged.',
           'Every file under the old client folder moved to the new one (emails, extracted Documents and the cross-reference stub for 1001-002). Every `box_path` in filing_log.csv, the stub\'s "Filed at:" line (the 1001-002 stub is the only stub touching client 1001; it points into 1001-001), the paths quoted in triage_notes.md and attorney_actions.md, and the client name and folder in matters_current.csv were rebuilt from the new name. wall_incidents.csv, needs_review.md and privilege_log.csv quote no client 1001 path, so they are unchanged (checked).',
           'Left alone on purpose: file names (they contain no client name), sender addresses such as @brightwaterfoods.test (the memo gives no new domain), and document titles in the triage notes that quote what the scans or PDFs actually say ("Brightwater Foods Inc.").'],
}


def main():
    p1, s1, s2, s3, fin = sys.argv[1:6]
    stages = [load(p1), load(s1), load(s2), load(s3), load(fin)]
    # ---- memo replies
    per_email = {}
    for i, (num, who, date, subj) in enumerate(MEMOS):
        a, b = stages[i], stages[i + 1]
        L = [f'# Reply to memo {num}', '', f'To: {who}', f'Re: {subj} ({date})', '', 'Thank you. Here is exactly what changed in the filing.', '']
        for n in NOTES[num]:
            L.append(f'- {n}')
        L += ['', '## Emails changed', '']
        d = diff_logs(a, b)
        if not d:
            L.append('None.')
        for e, s, ch in d:
            L.append(f'- **{e}** ("{s}"): {fmt_changes(ch)}')
            per_email.setdefault(e, []).append((num, ch))
        w_add, w_del = setdiff(a['wall'], b['wall'])
        L += ['', '## Wall incidents', '']
        L.append('Added: ' + ('; '.join(f'{e} / {p} / {r} / {m}' for e, p, r, m in w_add) or 'none'))
        L.append('Removed: ' + ('; '.join(f'{e} / {p} / {r} / {m}' for e, p, r, m in w_del) or 'none'))
        n_add, n_del = setdiff(a['nr'], b['nr'])
        L += ['', '## needs_review', '', 'Removed: ' + (', '.join(n_del) or 'none'), 'Added: ' + (', '.join(n_add) or 'none'), '',
              '## Attorney actions', '']
        a_add, a_del = setdiff(a['aa'], b['aa'])
        L.append('Added: ' + ('; '.join(f'{p}: {e}' for p, e in a_add) or 'none'))
        L.append('Removed: ' + ('; '.join(f'{p}: {e}' for p, e in a_del) or 'none'))
        f_add, f_del = setdiff(a['files'], b['files'])
        L += ['', '## Files in box/', '', f'{len(f_del)} paths removed, {len(f_add)} paths added.', '']
        if num == '04':
            L += ['Old path -> new path (every renamed file):', '']
            for x in f_del:
                y = x.replace('1001 Brightwater Foods', '1001 Brightwater Brands')
                L.append(f'- `{x}` -> `{y}`' + ('' if y in f_add else '  (NOT FOUND)'))
            L.append('')
        else:
            for x in f_del:
                L.append(f'- removed: `{x}`')
            for x in f_add:
                L.append(f'- added: `{x}`')
            L.append('')
        L += section_state(a, b) + ['']
        open(f'{fin}/memo_reply_{num}.md', 'w').write('\n'.join(L))
    # ---- changes report
    a, b = stages[0], stages[-1]
    L = ['# Changes report: output/phase1 -> output/final', '',
         'Compared field by field: filing_log.csv (category, primary_matter, xref_matters, privilege, flags, box_path, attachments_saved), then wall incidents, privilege log, needs_review, attorney actions and counts.', '',
         '## Emails whose category, matter, flags, privilege or path differs', '']
    d = diff_logs(a, b)
    L.append(f'{len(d)} of {len(b["log"])} emails differ.')
    L.append('')
    L.append('| email_file | subject | change | caused by |')
    L.append('|---|---|---|---|')
    for e, s, ch in d:
        cause = ', '.join(f'memo {n}' for n, _ in per_email[e])
        L.append(f'| {e} | {s} | {fmt_changes(ch)} | {cause} |')
    L += ['', '## Wall incidents', '']
    w_add, w_del = setdiff(a['wall'], b['wall'])
    L.append(f'Phase 1: {len(a["wall"])}; final: {len(b["wall"])}.')
    for x in w_add:
        L.append(f'- added (memo 03): {x[0]} / {x[1]} / {x[2]} / {x[3]}')
    for x in w_del:
        L.append(f'- removed: {x}')
    same = [r for r in rd(f'{fin}/wall_incidents.csv') if (r['email_file'], r['screened_person'], r['role'], r['matter']) in a['wall']]
    old = {(r['email_file'], r['screened_person'], r['role'], r['matter']): r['action'] for r in rd(f'{p1}/wall_incidents.csv')}
    chg = [r['email_file'] for r in same if old[(r['email_file'], r['screened_person'], r['role'], r['matter'])] != r['action']]
    L.append(f'- The {len(same)} incidents that existed in phase 1 are unchanged' + (' except the action text of ' + ', '.join(chg) if chg else ' (identical rows)') + '.')
    L += ['', '## Privilege log', '']
    L.append(f'Phase 1: {sum(a["priv"].values())} entries; final: {sum(b["priv"].values())} entries; ' + ('identical rows (no memo changed an AC/WP email in 1001-001; the Kestrel/hold matter is untouched, only its client folder was renamed, and the log carries no paths).' if a['priv'] == b['priv'] else 'DIFFERENT: ' + str(a['priv'] ^ b['priv'])))
    L += ['', '## needs_review', '']
    n_add, n_del = setdiff(a['nr'], b['nr'])
    L.append(f'Phase 1: {len(a["nr"])}; final: {len(b["nr"])}.')
    for e in n_del:
        r = b['log'][e]
        L.append(f'- left needs_review: {e} -> {r["category"]} {r["primary_matter"]} ({", ".join(f"memo {n}" for n, _ in per_email.get(e, []))})')
    for e in n_add:
        L.append(f'- entered needs_review: {e}')
    L += ['', '## Attorney actions', '']
    a_add, a_del = setdiff(a['aa'], b['aa'])
    for p, e in a_del:
        L.append(f'- removed: {p}: {e}')
    for p, e in a_add:
        L.append(f'- added: {p}: {e}')
    f_add, f_del = setdiff(a['files'], b['files'])
    L += ['', '## Files in box/', '', f'{len(f_del)} phase-1 paths no longer exist and {len(f_add)} new paths exist in final (91 files in each; each memo-04 rename moves the email, Documents file or stub with the folder).',
          f'Of these, {sum(1 for x in f_del if "1001 Brightwater Foods" in x)} are memo 04 renames (including {sum(1 for x in f_del if x.endswith(".xref.txt"))} stub and {sum(1 for x in f_del if "/Documents/" in x)} extracted attachments).']
    L += ['', '## Counts', ''] + section_state(a, b) + ['']
    open(f'{fin}/changes_report.md', 'w').write('\n'.join(L))
    print('wrote', fin)


main()
