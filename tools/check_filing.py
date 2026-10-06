#!/usr/bin/env python3
"""Validate a filing output folder against the filing rules and the input mailbox.

usage: check_filing.py <output_folder> [--inputs <folder with mailbox/, matters.csv, staff.csv>]
                                       [--matters <matters.csv override>]
Exit status 0 = all checks pass, 1 = at least one failure.
Independent of build_filing.py: names, flags, duplicates and counts are re-derived from the inputs.
"""
import argparse, csv, email, hashlib, os, re, sys
from collections import Counter
from email import policy
from email.utils import getaddresses, parsedate_to_datetime

FLAG_ORDER = ['hold', 'post-closing', 'ethical-wall', 'declined-intake', 'potential-conflict', 'new-matter-request', 'misdirected',
              'phishing', 'delivery-failure', 'restricted', 'duplicate-retained', 'attorney-action']
CATS = {'matter', 'needs_review', 'firm_admin', 'non_matter', 'duplicate'}
CAT_DIR = {'needs_review': '_Needs_Review', 'firm_admin': 'Firm_Admin', 'non_matter': '_Non_Matter', 'duplicate': '_Duplicates'}
PRIV = {'AC', 'WP', 'none', 'n/a'}
errors = []


def err(msg):
    errors.append(msg)


def slug(subject):
    s = subject.strip()
    while True:
        n = re.sub(r'^(re|fw|fwd):\s*', '', s, flags=re.I)
        if n == s:
            break
        s = n
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40].rstrip('-')
    return s or 'no-subject'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_csv(p):
    with open(p, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--inputs', default=None)
    ap.add_argument('--matters', default=None)
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    root = os.path.abspath(a.inputs or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

    # ---------- inputs
    orig_path = os.path.join(root, 'matters.csv')
    cur_in_out = os.path.join(out, 'matters_current.csv')
    mpath = a.matters or (cur_in_out if os.path.isfile(cur_in_out) else orig_path)
    M = {}
    for r in read_csv(mpath):
        n = r['notes']
        r['restricted'] = 'RESTRICTED' in n
        h = re.search(r'Litigation hold from (\d{4}-\d{2}-\d{2})', n)
        r['hold'] = h.group(1) if h else ''
        r['walls'] = re.findall(r'ETHICAL WALL: (.+?) is screened from this matter \(since (\d{4}-\d{2}-\d{2})\)', n)
        M[r['matter_no']] = r
    # the facts in force may only differ from the original matters.csv by additions (new matters, extra walls) and a client rename
    for r in read_csv(orig_path):
        c = M.get(r['matter_no'])
        if not c:
            err(f'matters_current.csv lost matter {r["matter_no"]}')
            continue
        for k in ('client_no', 'matter_name', 'matter_folder', 'responsible_attorney', 'status', 'closed_date'):
            if c[k] != r[k]:
                err(f'matters_current.csv changes {k} of {r["matter_no"]}: {r[k]!r} -> {c[k]!r}')
        if not c['notes'].startswith(r['notes']):
            err(f'matters_current.csv changes the notes of {r["matter_no"]} beyond an addition')
    for mn, c in M.items():
        for mn2, c2 in M.items():
            if c['client_no'] == c2['client_no'] and c['client_folder'] != c2['client_folder']:
                err(f'client {c["client_no"]} has two folder names: {c["client_folder"]} / {c2["client_folder"]}')
    staff = {r['email'].lower(): r['name'] for r in read_csv(os.path.join(root, 'staff.csv'))}
    name_to_addr = {v: k for k, v in staff.items()}
    E = {}
    for fn in sorted(os.listdir(os.path.join(root, 'mailbox'))):
        raw = open(os.path.join(root, 'mailbox', fn), 'rb').read()
        m = email.message_from_bytes(raw, policy=policy.default)
        dn, da = getaddresses([str(m['From'])])[0]
        dt = parsedate_to_datetime(str(m['Date'])).replace(tzinfo=None)
        E[fn] = dict(raw=raw, dn=dn, da=da.lower(), dt=dt, msgid=str(m['Message-ID']).strip(), subject=str(m['Subject']),
                     to=[x[1].lower() for x in getaddresses([str(x) for x in m.get_all('To', [])])],
                     cc=[x[1].lower() for x in getaddresses([str(x) for x in m.get_all('Cc', [])])],
                     atts=[(p.get_filename(), p.get_payload(decode=True)) for p in m.iter_attachments()])
    first = {}
    dupof = {}
    for fn, e in sorted(E.items(), key=lambda kv: (kv[1]['dt'], kv[0])):
        if e['msgid'] in first:
            dupof[fn] = first[e['msgid']]
        else:
            first[e['msgid']] = fn

    def expected_name(e):
        ln = e['dn'].strip().split()[-1] if e['dn'].strip() else e['da'].split('@')[0]
        ln = re.sub(r'[^a-z0-9]', '', ln.lower())
        return f"{e['dt']:%Y-%m-%d}_{e['dt']:%H%M}_{ln}_{slug(e['subject'])}.eml"

    # ---------- output files
    for req in ['filing_log.csv', 'wall_incidents.csv', 'privilege_log.csv', 'needs_review.md', 'attorney_actions.md',
                'filing_summary.md', 'triage_notes.md']:
        if not os.path.isfile(os.path.join(out, req)):
            err(f'missing output file {req}')
    boxdir = os.path.join(out, 'box')
    if not os.path.isdir(boxdir):
        err('missing box/ folder')
        return finish()
    if not os.path.isfile(os.path.join(out, 'filing_log.csv')):
        return finish()
    log = read_csv(os.path.join(out, 'filing_log.csv'))
    cols = ['email_file', 'received', 'sender', 'subject', 'category', 'primary_matter', 'xref_matters', 'privilege', 'flags', 'box_path', 'attachments_saved']
    with open(os.path.join(out, 'filing_log.csv'), newline='', encoding='utf-8') as f:
        if next(csv.reader(f)) != cols:
            err('filing_log.csv columns differ from the required header')

    # ---------- every email exactly once
    names = [r['email_file'] for r in log]
    if len(log) != len(E):
        err(f'filing_log has {len(log)} rows, mailbox has {len(E)} emails')
    for fn in E:
        if names.count(fn) != 1:
            err(f'{fn}: appears {names.count(fn)} times in filing_log (expected exactly 1)')
    for n in set(names) - set(E):
        err(f'{n}: in filing_log but not in mailbox')
    all_files = []
    for d, _, fs in os.walk(boxdir):
        for f in fs:
            all_files.append(os.path.relpath(os.path.join(d, f), out).replace(os.sep, '/'))
    eml_files = [p for p in all_files if p.endswith('.eml')]
    stub_files = [p for p in all_files if p.endswith('.xref.txt')]
    other_files = [p for p in all_files if p not in set(eml_files) | set(stub_files)]
    if len(eml_files) != len(E):
        err(f'box/ holds {len(eml_files)} .eml files, expected {len(E)}')
    by_hash = Counter(sha(open(os.path.join(out, p), 'rb').read()) for p in eml_files)
    src_hash = Counter(sha(e['raw']) for e in E.values())
    for fn, e in E.items():
        h = sha(e['raw'])
        if by_hash.get(h, 0) != src_hash[h]:
            err(f'{fn}: box/ holds {by_hash.get(h, 0)} copies of this content, mailbox has {src_hash[h]} email(s) with it')

    claimed = set()
    logd = {}
    for r in log:
        fn = r['email_file']
        e = E.get(fn)
        if not e:
            continue
        logd[fn] = r
        p = r['box_path']
        if r['category'] not in CATS:
            err(f'{fn}: bad category {r["category"]}')
        if r['privilege'] not in PRIV:
            err(f'{fn}: bad privilege {r["privilege"]}')
        fl = [x for x in r['flags'].split(';') if x]
        if any(x not in FLAG_ORDER for x in fl) or fl != [x for x in FLAG_ORDER if x in fl]:
            err(f'{fn}: flags "{r["flags"]}" invalid or out of order')
        if r['received'] != f"{e['dt']:%Y-%m-%d %H:%M}":
            err(f'{fn}: received {r["received"]} != Date header {e["dt"]:%Y-%m-%d %H:%M}')
        fp = os.path.join(out, p)
        if not os.path.isfile(fp):
            err(f'{fn}: box_path does not exist: {p}')
            continue
        claimed.add(p)
        if sha(open(fp, 'rb').read()) != sha(e['raw']):
            err(f'{fn}: file at box_path is not a byte-identical copy of the original email')
        base = os.path.basename(p)
        exp = expected_name(e)
        is_dup_file = False
        if base != exp:
            if base == exp[:-4] + '_dup.eml':
                is_dup_file = True
            else:
                err(f'{fn}: file name "{base}" does not follow the naming rule (expected "{exp}")')
        cat = r['category']
        pm = r['primary_matter']
        xr = [x for x in r['xref_matters'].split(';') if x]
        # duplicate rules
        orig = dupof.get(fn)
        if orig and cat != 'duplicate':
            err(f'{fn}: same Message-ID as {orig}, must be category duplicate')
        if not orig and cat == 'duplicate':
            err(f'{fn}: category duplicate but Message-ID is not repeated')
        retained_expected = False
        if orig:
            orow = next((x for x in log if x['email_file'] == orig), None)
            if orow and orow['category'] == 'matter' and M.get(orow['primary_matter'], {}).get('hold') and \
                    e['dt'].date().isoformat() >= M[orow['primary_matter']]['hold']:
                retained_expected = True
        if orig:
            if retained_expected:
                if not is_dup_file:
                    err(f'{fn}: hold duplicate must be retained with _dup in the matter folder')
                if 'duplicate-retained' not in fl or 'hold' not in fl:
                    err(f'{fn}: retained duplicate needs flags hold;duplicate-retained')
                if orow and pm != orow['primary_matter']:
                    err(f'{fn}: retained duplicate must be in the original\'s matter {orow["primary_matter"]}')
                if '/Correspondence/' not in p:
                    err(f'{fn}: retained hold duplicate is not in a matter Correspondence folder')
            else:
                if not p.startswith('box/_Duplicates/'):
                    err(f'{fn}: non-hold duplicate must be in box/_Duplicates/')
                if is_dup_file:
                    err(f'{fn}: _dup suffix used outside the hold exception')
                if 'duplicate-retained' in fl:
                    err(f'{fn}: duplicate-retained flag without hold exception')
        else:
            if is_dup_file or 'duplicate-retained' in fl:
                err(f'{fn}: _dup / duplicate-retained on a non-duplicate')
        # location by category / matter
        if cat == 'matter' or (cat == 'duplicate' and retained_expected):
            if pm not in M:
                err(f'{fn}: primary_matter "{pm}" not in matters.csv')
                continue
            m = M[pm]
            top = 'Restricted' if m['restricted'] else 'Clients'
            expd = f"box/{top}/{m['client_folder']}/{m['matter_folder']}/Correspondence/{base}"
            if p != expd:
                err(f'{fn}: box_path "{p}" should be "{expd}"')
            for x in xr:
                if x not in M:
                    err(f'{fn}: xref matter {x} unknown')
                elif M[x]['client_no'] != m['client_no']:
                    err(f'{fn}: cross-reference to {x} crosses clients')
                elif x == pm:
                    err(f'{fn}: xref equals primary matter')
            # derived flags
            d = e['dt'].date().isoformat()
            want = set()
            if m['hold'] and d >= m['hold']:
                want.add('hold')
            if m['status'] == 'closed' and m['closed_date'] and d > m['closed_date'] and cat == 'matter':
                want.add('post-closing')
            if m['restricted'] and cat == 'matter':
                want.add('restricted')
            if retained_expected:
                want |= {'hold', 'duplicate-retained'}
            for mn in [pm] + xr:
                for wn, ws in M.get(mn, {}).get('walls', []):
                    if d >= ws:
                        wa = name_to_addr[wn]
                        if wa == e['da'] or wa in e['to'] or wa in e['cc']:
                            want.add('ethical-wall')
            for f in want:
                if f not in fl:
                    err(f'{fn}: missing derived flag {f}')
            for f in ('hold', 'post-closing', 'ethical-wall', 'restricted'):
                if f in fl and f not in want:
                    err(f'{fn}: flag {f} not justified by the rules')
            # privilege
            if cat == 'matter' and r['privilege'] not in ('AC', 'WP', 'none'):
                err(f'{fn}: matter email needs privilege AC/WP/none')
        else:
            if pm or xr:
                err(f'{fn}: non-matter category {cat} must not have a matter or cross-references')
            if r['privilege'] != 'n/a':
                err(f'{fn}: privilege must be n/a for {cat}')
            if cat in CAT_DIR:
                sub = 'Firm_Admin/Declined_Intake' if (cat == 'firm_admin' and 'declined-intake' in fl) else CAT_DIR[cat]
                expd = f'box/{sub}/{base}'
                if p != expd:
                    err(f'{fn}: box_path "{p}" should be "{expd}"')
            if r['attachments_saved']:
                err(f'{fn}: attachments must not be extracted for {cat}')
        if cat == 'matter' and r['privilege'] == 'n/a':
            err(f'{fn}: matter email has privilege n/a')
        if cat != 'matter' and not retained_expected and 'restricted' in fl:
            err(f'{fn}: restricted flag outside a restricted matter')
        if 'declined-intake' in fl and (cat != 'firm_admin' or 'potential-conflict' in fl):
            err(f'{fn}: declined-intake belongs on a firm_admin email and replaces potential-conflict')
        if 'phishing' in fl and cat != 'non_matter':
            err(f'{fn}: phishing should be non_matter')
        # restricted placement
        in_restricted_dir = p.startswith('box/Restricted/')
        if in_restricted_dir and not (pm in M and M[pm]['restricted']):
            err(f'{fn}: non-restricted item under box/Restricted/')
        if pm in M and M[pm]['restricted'] and not in_restricted_dir:
            err(f'{fn}: restricted matter item outside box/Restricted/')
        # attachments
        if cat == 'matter' and pm in M:
            m = M[pm]
            docdir = os.path.dirname(os.path.dirname(p)) + '/Documents'
            exp_att = [f"{e['dt']:%Y-%m-%d}_{n}" for n, _ in e['atts']]
            got = [x for x in r['attachments_saved'].split(';') if x]
            if got != exp_att:
                err(f'{fn}: attachments_saved {got} != expected {exp_att}')
            for (n, payload), en in zip(e['atts'], exp_att):
                ap_ = f'{docdir}/{en}'
                if not os.path.isfile(os.path.join(out, ap_)):
                    err(f'{fn}: extracted attachment missing: {ap_}')
                else:
                    claimed.add(ap_)
                    if sha(open(os.path.join(out, ap_), 'rb').read()) != sha(payload):
                        err(f'{fn}: attachment {en} content differs from the original')

    # ---------- stubs
    expected_stubs = {}
    for r in log:
        for x in [y for y in r['xref_matters'].split(';') if y]:
            if x in M and r['box_path']:
                m = M[x]
                sp = f"box/{'Restricted' if m['restricted'] else 'Clients'}/{m['client_folder']}/{m['matter_folder']}/Correspondence/{os.path.basename(r['box_path'])}.xref.txt"
                expected_stubs[sp] = r
    for sp, r in expected_stubs.items():
        if sp not in stub_files:
            err(f'{r["email_file"]}: stub missing: {sp}')
    for sp in stub_files:
        claimed.add(sp)
        txt = open(os.path.join(out, sp), encoding='utf-8').read()
        lines = txt.splitlines()
        if len(lines) != 1 or not lines[0].startswith('Filed at: '):
            err(f'stub {sp}: must contain exactly one line "Filed at: <path>"')
            continue
        tgt = lines[0][len('Filed at: '):]
        if not os.path.isfile(os.path.join(out, tgt)):
            err(f'stub {sp}: "Filed at" path does not exist: {tgt}')
            continue
        parts_s, parts_t = sp.split('/'), tgt.split('/')
        # client folder = path component after Clients/ or Restricted/
        if parts_s[2] != parts_t[2] or parts_s[1] != parts_t[1] and False:
            err(f'stub {sp}: crosses clients ({parts_s[2]} vs {parts_t[2]})')
        if sp not in expected_stubs:
            err(f'stub {sp}: not listed as a cross-reference in filing_log.csv')
        else:
            if expected_stubs[sp]['box_path'] != tgt:
                err(f'stub {sp}: points to {tgt}, log says primary copy is {expected_stubs[sp]["box_path"]}')

    # ---------- unclaimed files
    for p in all_files:
        if p not in claimed:
            err(f'unexpected/unlogged file in box/: {p}')
    for p in other_files:
        if '/Documents/' not in p:
            err(f'unexpected non-email file: {p}')
    # restricted matters only under Restricted
    for mn, m in M.items():
        if m['restricted']:
            if os.path.isdir(os.path.join(boxdir, 'Clients', m['client_folder'], m['matter_folder'])):
                err(f'restricted matter {mn} has a folder under box/Clients/')
    for p in all_files:
        if p.startswith('box/Restricted/'):
            mf = p.split('/')[3]
            if not any(m['restricted'] and m['matter_folder'] == mf for m in M.values()):
                err(f'non-restricted matter folder under Restricted: {p}')

    # ---------- wall incidents
    wpath = os.path.join(out, 'wall_incidents.csv')
    if os.path.isfile(wpath):
        wi = read_csv(wpath)
        want = set()
        for r in log:
            fn = r['email_file']
            if fn not in E:
                continue
            e = E[fn]
            pm = r['primary_matter']
            xr = [x for x in r['xref_matters'].split(';') if x]
            if not pm:
                continue
            for mn in [pm] + xr:
                for wn, ws in M.get(mn, {}).get('walls', []):
                    if e['dt'].date().isoformat() >= ws:
                        wa = name_to_addr[wn]
                        if wa == e['da']:
                            want.add((fn, wn, 'sender', mn))
                        if wa in e['to']:
                            want.add((fn, wn, 'to', mn))
                        if wa in e['cc']:
                            want.add((fn, wn, 'cc', mn))
        got = {(r['email_file'], r['screened_person'], r['role'], r['matter']) for r in wi}
        if len(got) != len(wi):
            err('wall_incidents.csv has duplicate rows')
        for x in want - got:
            err(f'wall incident missing: {x}')
        for x in got - want:
            err(f'wall incident not justified: {x}')
        for r in wi:
            if not r['action'].strip():
                err(f'wall incident {r["email_file"]}: empty action')
            lr = logd.get(r['email_file'])
            if lr and 'ethical-wall' not in lr['flags'].split(';'):
                err(f'wall incident {r["email_file"]}: log lacks ethical-wall flag')
        flagged = {r['email_file'] for r in log if 'ethical-wall' in r['flags'].split(';')}
        if flagged != {r['email_file'] for r in wi}:
            err('ethical-wall flags and wall_incidents.csv list different emails')

    # ---------- privilege log
    ppath = os.path.join(out, 'privilege_log.csv')
    if os.path.isfile(ppath):
        pl = read_csv(ppath)
        holdm = {mn for mn, m in M.items() if m['hold']}
        want = [r for r in log if r['primary_matter'] in holdm and r['privilege'] in ('AC', 'WP')]
        if len(pl) != len(want):
            err(f'privilege_log has {len(pl)} rows, expected {len(want)}')
        wk = Counter((r['received'], r['subject'], r['privilege']) for r in want)
        gk = Counter((r['date'], r['subject'], r['privilege']) for r in pl)
        if wk != gk:
            err('privilege_log.csv rows do not match the AC/WP emails filed in held matters')
        for r in pl:
            if not r['description'].strip():
                err('privilege_log: empty description')

    # ---------- needs_review / attorney actions
    nrp = os.path.join(out, 'needs_review.md')
    if os.path.isfile(nrp):
        txt = open(nrp, encoding='utf-8').read()
        for r in log:
            has = r['email_file'] in txt
            if (r['category'] == 'needs_review') != has:
                err(f'needs_review.md {"lacks" if not has else "wrongly lists"} {r["email_file"]}')
    triage = os.path.join(out, 'triage_notes.md')
    if os.path.isfile(triage):
        txt = open(triage, encoding='utf-8').read()
        for fn in E:
            if f'## {fn}' not in txt:
                err(f'triage_notes.md has no entry for {fn}')
    aap = os.path.join(out, 'attorney_actions.md')
    if os.path.isfile(aap):
        txt = open(aap, encoding='utf-8').read()
        must = [r for r in log if set(r['flags'].split(';')) & {'post-closing', 'potential-conflict', 'new-matter-request', 'ethical-wall',
                                                                'delivery-failure', 'phishing', 'attorney-action', 'misdirected'}]
        for r in must:
            if r['email_file'] not in txt:
                err(f'attorney_actions.md does not mention flagged email {r["email_file"]} ({r["flags"]})')

    # ---------- summary counts
    sp = os.path.join(out, 'filing_summary.md')
    if os.path.isfile(sp):
        txt = open(sp, encoding='utf-8').read()
        sections = {}
        cur = None
        for line in txt.splitlines():
            if line.startswith('## '):
                cur = line[3:].strip()
                sections[cur] = {}
            elif cur and re.match(r'^\|\s*[^|]+\|\s*\d+\s*\|$', line):
                k, v = [c.strip() for c in line.strip('|').split('|')]
                sections[cur][k] = int(v)
        cats = Counter(r['category'] for r in log)
        for c in CATS:
            if sections.get('By category', {}).get(c, 0) != cats.get(c, 0):
                err(f'filing_summary category {c}: {sections.get("By category", {}).get(c)} vs log {cats.get(c, 0)}')
        if sum(sections.get('By category', {}).values()) != len(log):
            err('filing_summary category counts do not add up to the number of log rows')
        mats = Counter(r['primary_matter'] for r in log if r['primary_matter'])
        if dict(sections.get('By matter', {})) != dict(mats):
            err(f'filing_summary by-matter {sections.get("By matter")} != log {dict(mats)}')
        att = Counter(M[r['primary_matter']]['responsible_attorney'] for r in log if r['primary_matter'] in M)
        if dict(sections.get('By responsible attorney', {})) != dict(att):
            err(f'filing_summary by-attorney {sections.get("By responsible attorney")} != log {dict(att)}')
        mm = re.search(r'Files in box/:\s*(\d+)', txt)
        if not mm or int(mm.group(1)) != len(all_files):
            err(f'filing_summary files in box/: {mm.group(1) if mm else None} vs actual {len(all_files)}')
        mm = re.search(r'Emails in filing_log.csv:\s*(\d+)', txt)
        if not mm or int(mm.group(1)) != len(log):
            err('filing_summary email count does not match the log')
        if os.path.isfile(wpath):
            mm = re.search(r'Wall incidents:\s*(\d+)', txt)
            if not mm or int(mm.group(1)) != len(read_csv(wpath)):
                err('filing_summary wall incident count does not match wall_incidents.csv')
        if os.path.isfile(ppath):
            mm = re.search(r'Privilege log entries:\s*(\d+)', txt)
            if not mm or int(mm.group(1)) != len(read_csv(ppath)):
                err('filing_summary privilege log count does not match privilege_log.csv')
        mm = re.search(r'needs_review emails:\s*(\d+)', txt)
        if not mm or int(mm.group(1)) != cats.get('needs_review', 0):
            err('filing_summary needs_review count does not match the log')
    print(f'checked {len(log)} log rows, {len(eml_files)} .eml, {len(stub_files)} stubs, {len(all_files)} files in box/')
    return finish()


def finish():
    if errors:
        print(f'FAIL: {len(errors)} problem(s)')
        for e in errors:
            print(' -', e)
        return 1
    print('PASS: all checks passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
