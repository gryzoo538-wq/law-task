"""Stage after memo 01 (2026-09-28): matter 1002-003 opened; the two bakery emails leave needs_review."""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data_phase1 as base

CLIENT_PEOPLE = base.CLIENT_PEOPLE
D = copy.deepcopy(base.D)
ACTIONS = list(base.ACTIONS)


def patch_rows(rows):
    rows.append(dict(matter_no='1002-003', client_no='1002', client_name='Maria Delgado', client_folder='1002 Delgado Maria',
                     matter_name='Formation of Delgado Bakery LLC', matter_folder='1002-003 Delgado Bakery LLC Formation',
                     responsible_attorney='Ravi Iyer', status='open', closed_date='', notes=''))


for _id, extra in [('AAMk8dff666589', 'Original ask: LLC for her daughter\'s bakery.'), ('AAMk68f6cdb2f8', 'Follow-up on the name for the bakery LLC.')]:
    d = D[_id]
    d.update(cat='matter', m='1002-003', f=[])
    d.pop('nr', None)
    d['why'] = ('Memo 01 (2026-09-28): matter 1002-003 "Formation of Delgado Bakery LLC" is open (conflicts cleared), so this email is no longer a new-matter '
                'request and moves from _Needs_Review into that matter. ' + extra + ' Maria Delgado and Ravi Iyer only, so attorney-client.')
ACTIONS = [a for a in ACTIONS if a[1] not in ('AAMk8dff666589', 'AAMk68f6cdb2f8')]
