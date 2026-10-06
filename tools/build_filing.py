#!/usr/bin/env python3
"""Build a filing output folder from the mailbox, matters.csv, staff.csv and a decisions module.

usage: build_filing.py <root> <data_module.py> <out_dir> [phase_label]
Judgments live in the data module; hold, post-closing, ethical-wall, restricted,
duplicate handling, privilege, names and paths are derived here from the rules.
"""
import csv, email, importlib.util, os, re, shutil, sys
from collections import Counter, OrderedDict
from datetime import datetime
from email import policy
from email.utils import getaddresses, parsedate_to_datetime

FLAG_ORDER = ['hold', 'post-closing', 'ethical-wall', 'declined-intake', 'potential-conflict', 'new-matter-request', 'misdirected',
              'phishing', 'delivery-failure', 'restricted', 'duplicate-retained', 'attorney-action']
CAT_DIR = {'needs_review': '_Needs_Review', 'firm_admin': 'Firm_Admin', 'non_matter': '_Non_Matter', 'duplicate': '_Duplicates'}


def slug(subject):
    s = subject.strip()
    while True:
        n = re.sub(r'^(re|fw|fwd):\s*', '', s, flags=re.I)
        if n == s:
            break
        s = n
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40].rstrip('-')
    return s or 'no-subject'


def last_name(name, addr):
    if name.strip():
        w = name.strip().split()[-1]
    else:
        w = addr.split('@')[0]
    return re.sub(r'[^a-z0-9]', '', w.lower())


def load_data(path):
    spec = importlib.util.spec_from_file_location('data', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_emails(root):
    out = OrderedDict()
    d = os.path.join(root, 'mailbox')
    for fn in sorted(os.listdir(d)):
        raw = open(os.path.join(d, fn), 'rb').read()
        m = email.message_from_bytes(raw, policy=policy.default)
        name, addr = getaddresses([str(m['From'])])[0]
        dt = parsedate_to_datetime(str(m['Date']))
        atts = [(p.get_filename(), p.get_payload(decode=True)) for p in m.iter_attachments()]
        body = m.get_body(preferencelist=('plain',))
        out[fn[:-4]] = dict(
            id=fn[:-4], raw=raw, from_name=name, from_addr=addr.lower(), subject=str(m['Subject']),
            to=[(n, a.lower()) for n, a in getaddresses([str(x) for x in m.get_all('To', [])])],
            cc=[(n, a.lower()) for n, a in getaddresses([str(x) for x in m.get_all('Cc', [])])],
            date_hdr=str(m['Date']), dt=dt.replace(tzinfo=None), msgid=str(m['Message-ID']).strip(), atts=atts,
            body=body.get_content().strip() if body else '')
    return out


def load_matters(root, patch=None):
    """Read matters.csv, apply the data module's patch_rows (memo changes), parse hold / wall / restricted notes."""
    path = os.path.join(root, 'matters.csv')
    rdr = csv.DictReader(open(path, encoding='utf-8'))
    fields = rdr.fieldnames
    rows = list(rdr)
    if patch:
        patch(rows)
    ms = OrderedDict()
    for r in rows:
        n = r['notes']
        r['restricted'] = 'RESTRICTED' in n
        h = re.search(r'Litigation hold from (\d{4}-\d{2}-\d{2})', n)
        r['hold'] = h.group(1) if h else ''
        r['walls'] = re.findall(r'ETHICAL WALL: (.+?) is screened from this matter \(since (\d{4}-\d{2}-\d{2})\)', n)
        ms[r['matter_no']] = r
    return ms, fields


def load_staff(root):
    return {r['email'].lower(): r['name'] for r in csv.DictReader(open(os.path.join(root, 'staff.csv'), encoding='utf-8'))}


def build(root, data_path, out, phase):
    data = load_data(data_path)
    E = load_emails(root)
    M, mfields = load_matters(root, getattr(data, 'patch_rows', None))
    S = load_staff(root)
    people_name = {}
    for e in E.values():
        for n, a in [(e['from_name'], e['from_addr'])] + e['to'] + e['cc']:
            people_name.setdefault(a, n)

    def mdir(mn):
        m = M[mn]
        return ('Restricted' if m['restricted'] else 'Clients'), m['client_folder'], m['matter_folder']

    def mbase(mn):
        top, c, mf = mdir(mn)
        return f'box/{top}/{c}/{mf}'

    def is_client_person(addr, client_no):
        for c in data.CLIENT_PEOPLE.get(client_no, []):
            if addr == c or ('@' not in c and addr.endswith('@' + c)):
                return True
        return False

    # ---- duplicates
    first = {}
    dupof = {}
    for e in sorted(E.values(), key=lambda e: (e['dt'], e['id'])):
        if e['msgid'] in first:
            dupof[e['id']] = first[e['msgid']]
        else:
            first[e['msgid']] = e['id']

    rows = []
    stubs = []   # (path, content)
    wall = []
    info = {}
    for eid, e in E.items():
        dec = dict(data.D[eid])
        cat = dec['cat']
        if eid in dupof:
            orig = data.D[dupof[eid]]
            assert cat == 'duplicate', eid
        fname = f"{e['dt']:%Y-%m-%d}_{e['dt']:%H%M}_{last_name(e['from_name'], e['from_addr'])}_{slug(e['subject'])}.eml"
        flags = set(dec.get('f', []))
        pm = dec.get('m', '')
        xr = list(dec.get('x', []))
        retained = False
        if cat == 'duplicate':
            o = data.D[dupof[eid]]
            om = o.get('m', '')
            if o['cat'] == 'matter' and M[om]['hold'] and e['dt'].date().isoformat() >= M[om]['hold']:
                retained = True
                pm = om
                fname = fname[:-4] + '_dup.eml'
                flags |= {'hold', 'duplicate-retained'}
        if cat == 'matter' or retained:
            path = f'{mbase(pm)}/Correspondence/{fname}'
            client = pm[:4]
            m = M[pm]
            if cat == 'matter':
                if m['hold'] and e['dt'].date().isoformat() >= m['hold']:
                    flags.add('hold')
                if m['status'] == 'closed' and m['closed_date'] and e['dt'].date().isoformat() > m['closed_date']:
                    flags.add('post-closing')
                if m['restricted']:
                    flags.add('restricted')
            for x in xr:
                assert x[:4] == client, (eid, 'stub crosses clients')
        elif cat == 'firm_admin' and 'declined-intake' in flags:
            path = f'box/Firm_Admin/Declined_Intake/{fname}'
        else:
            path = f'box/{CAT_DIR[cat]}/{fname}'
        # privilege
        if cat == 'matter':
            if 'priv' in dec:
                priv = dec['priv']
            else:
                parts = [e['from_addr']] + [a for _, a in e['to']] + [a for _, a in e['cc']]
                nonstaff = [a for a in parts if a not in S]
                if not nonstaff:
                    priv = 'WP'
                elif all(is_client_person(a, pm[:4]) for a in nonstaff):
                    priv = 'AC'
                else:
                    priv = 'none'
        else:
            priv = 'n/a'
        # walls (primary or cross-referenced matters)
        for mn in ([pm] + xr) if pm else []:
            if not (cat == 'matter' or retained):
                continue
            for pname, start in M[mn]['walls']:
                if e['dt'].date().isoformat() < start:
                    continue
                paddr = [a for a, n in S.items() if n == pname][0]
                roles = []
                if e['from_addr'] == paddr:
                    roles.append('sender')
                if paddr in [a for _, a in e['to']]:
                    roles.append('to')
                if paddr in [a for _, a in e['cc']]:
                    roles.append('cc')
                for r in roles:
                    flags.add('ethical-wall')
                    act = ('Flagged ethical-wall in the filing log; filed at ' + path +
                           ('' if mn == pm else ' with a cross-reference stub in ' + mbase(mn) + '/Correspondence') +
                           '; reported to Jonah Hartwell (ethics partner).')
                    wall.append(dict(email_file=eid + '.eml', received=f"{e['dt']:%Y-%m-%d %H:%M}", screened_person=pname,
                                     role=r, matter=mn, action=act))
        atts_saved = []
        if cat == 'matter':
            for fn, payload in e['atts']:
                atts_saved.append((f"{e['dt']:%Y-%m-%d}_{fn}", payload))
        fl = [f for f in FLAG_ORDER if f in flags]
        assert flags <= set(FLAG_ORDER), flags
        sender = f"{e['from_name']} <{e['from_addr']}>" if e['from_name'] else e['from_addr']
        rows.append(dict(email_file=eid + '.eml', received=f"{e['dt']:%Y-%m-%d %H:%M}", sender=sender, subject=e['subject'],
                         category=cat, primary_matter=pm if (cat == 'matter' or retained) else '',
                         xref_matters=';'.join(xr), privilege=priv, flags=';'.join(fl), box_path=path,
                         attachments_saved=';'.join(n for n, _ in atts_saved)))
        info[eid] = dict(e=e, dec=dec, path=path, priv=priv, flags=fl, pm=pm, xr=xr, fname=fname, atts=atts_saved, retained=retained,
                         dup=dupof.get(eid))
        for x in xr:
            stubs.append((f'{mbase(x)}/Correspondence/{fname}.xref.txt', f'Filed at: {path}\n'))

    # ---- write box
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    for eid, i in info.items():
        p = os.path.join(out, i['path'])
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'wb').write(i['e']['raw'])
        if i['atts']:
            dd = os.path.join(out, os.path.dirname(os.path.dirname(i['path'])), 'Documents')
            os.makedirs(dd, exist_ok=True)
            for n, payload in i['atts']:
                open(os.path.join(dd, n), 'wb').write(payload)
    for p, c in stubs:
        fp = os.path.join(out, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, 'w').write(c)

    # ---- csv outputs
    with open(os.path.join(out, 'matters_current.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, mfields, extrasaction='ignore')
        w.writeheader()
        for r in M.values():
            w.writerow(r)
    cols = ['email_file', 'received', 'sender', 'subject', 'category', 'primary_matter', 'xref_matters', 'privilege', 'flags', 'box_path', 'attachments_saved']
    with open(os.path.join(out, 'filing_log.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    wall.sort(key=lambda r: (r['received'], r['email_file'], r['matter'], r['role']))
    with open(os.path.join(out, 'wall_incidents.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, ['email_file', 'received', 'screened_person', 'role', 'matter', 'action'])
        w.writeheader()
        for r in wall:
            w.writerow(r)
    # privilege log: AC/WP emails filed in 1001-001 (hold matter)
    hold_matters = [mn for mn, m in M.items() if m['hold']]
    plog = []
    for r in sorted(rows, key=lambda r: (r['received'], r['email_file'])):
        if r['primary_matter'] in hold_matters and r['privilege'] in ('AC', 'WP'):
            i = info[r['email_file'][:-4]]
            e = i['e']
            if r['privilege'] == 'AC':
                desc = 'Confidential communication between firm attorney(s) and the client\'s representative made for the purpose of legal advice in the matter.'
            else:
                desc = 'Internal firm communication among firm personnel prepared in connection with the pending litigation.'
            if e['atts']:
                desc += ' Includes an attachment.'
            def nm(l):
                return '; '.join(f'{n} <{a}>' if n else a for n, a in l)
            plog.append(dict(date=r['received'], **{'from': r['sender']}, to=nm(e['to']), cc=nm(e['cc']), subject=r['subject'],
                             privilege=r['privilege'], description=desc))
    with open(os.path.join(out, 'privilege_log.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, ['date', 'from', 'to', 'cc', 'subject', 'privilege', 'description'])
        w.writeheader()
        for r in plog:
            w.writerow(r)

    # ---- markdown outputs
    def fmt(l):
        return ', '.join(f'{n} <{a}>' if n else a for n, a in l) or '(none)'

    t = [f'# Triage notes ({phase})', '',
         f'{len(rows)} emails. Judgments are explained per entry; rule-derived flags, privilege and paths are computed from the rules.', '']
    for r in rows:
        i = info[r['email_file'][:-4]]
        e = i['e']
        t += [f"## {r['email_file']}", f"- **From:** {r['sender']}", f"- **To:** {fmt(e['to'])}", f"- **Cc:** {fmt(e['cc'])}",
              f"- **Date:** {e['date_hdr']}", f"- **Message-ID:** {e['msgid']}", f"- **Subject:** {e['subject']}",
              f"- **Body:** {i['dec']['sum']}"]
        if e['atts']:
            for fn, _ in e['atts']:
                t.append(f"- **Attachment {fn}:** {i['dec'].get('att', {}).get(fn, '??')}")
        else:
            t.append('- **Attachments:** none')
        mm = f", matter {i['pm']}" if i['pm'] else ''
        xx = f", cross-reference to {';'.join(i['xr'])}" if i['xr'] else ''
        t += [f"- **Decision:** category `{r['category']}`{mm}{xx}; privilege `{r['privilege']}`; flags `{r['flags'] or '-'}`",
              f"- **Filed at:** `{r['box_path']}`", f"- **Why:** {i['dec']['why']}"]
        if i['dup']:
            t.append(f"- **Duplicate of:** {i['dup']}.eml")
        t.append('')
    open(os.path.join(out, 'triage_notes.md'), 'w').write('\n'.join(t))

    nr = [r for r in rows if r['category'] == 'needs_review']
    t = [f'# needs_review ({phase})', '', f'{len(nr)} emails.', '']
    for r in nr:
        i = info[r['email_file'][:-4]]
        reason, decide, who = i['dec']['nr']
        t += [f"## {r['email_file']} - {r['subject']}", f"- Received: {r['received']}; from {r['sender']}", f"- Flags: {r['flags']}",
              f"- Reason: {reason}", f"- What the firm must decide: {decide}", f"- Who should decide: {who}", f"- Filed at: `{r['box_path']}`", '']
    open(os.path.join(out, 'needs_review.md'), 'w').write('\n'.join(t))

    t = [f'# Attorney actions ({phase})', '']
    people = OrderedDict()
    for p, eid, why in data.ACTIONS:
        people.setdefault(p, []).append((eid, why))
    for p, items in people.items():
        t += [f'## {p}', '']
        for eid, why in items:
            r = next(r for r in rows if r['email_file'] == eid + '.eml')
            t.append(f"- **{r['email_file']}** ({r['received']}, \"{r['subject']}\", flags: {r['flags'] or '-'}; `{r['box_path']}`): {why}")
        t.append('')
    open(os.path.join(out, 'attorney_actions.md'), 'w').write('\n'.join(t))

    # summary
    nfiles = sum(len(fs) for _, _, fs in os.walk(os.path.join(out, 'box')))
    n_eml = sum(1 for _, _, fs in os.walk(os.path.join(out, 'box')) for f in fs if f.endswith('.eml'))
    n_stub = sum(1 for _, _, fs in os.walk(os.path.join(out, 'box')) for f in fs if f.endswith('.xref.txt'))
    n_att = nfiles - n_eml - n_stub
    cats = Counter(r['category'] for r in rows)
    mats = Counter(r['primary_matter'] for r in rows if r['primary_matter'])
    atty = Counter(M[r['primary_matter']]['responsible_attorney'] for r in rows if r['primary_matter'])
    t = [f'# Filing summary ({phase})', '', f'Emails in filing_log.csv: {len(rows)}', '', '## By category', '', '| category | emails |', '|---|---|']
    for c in ['matter', 'needs_review', 'firm_admin', 'non_matter', 'duplicate']:
        t.append(f'| {c} | {cats.get(c, 0)} |')
    t += ['', 'Note: the duplicate row includes retained duplicates that sit in a matter folder (counted below by matter as well).', '',
          '## By matter', '', '| matter | emails |', '|---|---|']
    for mn in M:
        if mats.get(mn):
            t.append(f'| {mn} | {mats[mn]} |')
    t += ['', '## By responsible attorney', '', '| attorney | emails |', '|---|---|']
    for a, n in sorted(atty.items()):
        t.append(f'| {a} | {n} |')
    t += ['', '## Files in box/', '', f'- Files in box/: {nfiles}', f'- Email copies (.eml): {n_eml}', f'- Cross-reference stubs: {n_stub}',
          f'- Extracted attachments: {n_att}', '', '## Other counts', '',
          f"- Wall incidents: {len(wall)}", f"- Privilege log entries: {len(plog)}", f"- needs_review emails: {len(nr)}", '',
          '## Open issues', '']
    for p, items in people.items():
        for eid, why in items:
            t.append(f'- [{p}] {eid}.eml: {why}')
    open(os.path.join(out, 'filing_summary.md'), 'w').write('\n'.join(t) + '\n')
    return rows


if __name__ == '__main__':
    root, data_path, out = sys.argv[1:4]
    phase = sys.argv[4] if len(sys.argv) > 4 else os.path.basename(out)
    rows = build(root, data_path, out, phase)
    print('built', len(rows), 'rows into', out)
