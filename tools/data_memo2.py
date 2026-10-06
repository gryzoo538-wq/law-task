"""Stage after memo 02 (2026-09-29): Kestrel engagement declined; matter 1007-002 opened."""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data_memo1 as prev

CLIENT_PEOPLE = prev.CLIENT_PEOPLE
D = copy.deepcopy(prev.D)
ACTIONS = list(prev.ACTIONS)


def patch_rows(rows):
    prev.patch_rows(rows)
    rows.append(dict(matter_no='1007-002', client_no='1007', client_name='Blue Heron Marina LLC', client_folder='1007 Blue Heron Marina',
                     matter_name='Fuel dock damage claim', matter_folder='1007-002 Fuel Dock Damage Claim',
                     responsible_attorney='Jonah Hartwell', status='open', closed_date='', notes=''))


d = D['AAMkc707b37e14']
d.update(cat='firm_admin', f=['declined-intake', 'new-matter-request'])
d.pop('nr', None)
d.pop('m', None)
d['why'] = ('Memo 02 (2026-09-29): the firm DECLINED the Kestrel engagement and sent a decline letter. Declined intake emails are firm_admin, filed in '
            'box/Firm_Admin/Declined_Intake/, privilege n/a. The flag declined-intake replaces potential-conflict for this email; new-matter-request stays because the '
            'email still asks for services outside every matter (the memo only replaces potential-conflict). Not filed in 1001-001: Kestrel is the adverse party.')
d = D['AAMk1b66809a11']
d.update(cat='matter', m='1007-002', f=[])
d.pop('nr', None)
d['why'] = ('Memo 02 (2026-09-29): matter 1007-002 "Fuel dock damage claim" is open for Blue Heron Marina (Jonah Hartwell), so this email is the request that the '
            'new matter covers and is filed there; new-matter-request removed. Blue Heron Marina (client 1007), not Project Heron (Calloway). Only the client and Jonah take part: attorney-client.')
ACTIONS = [a for a in ACTIONS if a[1] not in ('AAMkc707b37e14', 'AAMk1b66809a11')]
ACTIONS += [
 ('Jonah Hartwell (ethics partner)', 'AAMkc707b37e14', 'Declined intake (memo 02): keep the decline letter with this email in Firm_Admin/Declined_Intake. The email still asks for new services (new-matter-request stays); no further engagement work. Make sure nobody discusses Brightwater v. Kestrel with Kestrel directly (Kestrel is represented by Tolland Law).'),
]
