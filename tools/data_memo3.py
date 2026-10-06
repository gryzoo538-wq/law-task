"""Stage after memo 03 (2026-09-30): Tom Weller also screened from 1003-001 since 2026-08-15."""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data_memo2 as prev

CLIENT_PEOPLE = prev.CLIENT_PEOPLE
D = copy.deepcopy(prev.D)
ACTIONS = list(prev.ACTIONS)


def patch_rows(rows):
    prev.patch_rows(rows)
    for r in rows:
        if r['matter_no'] == '1003-001':
            r['notes'] = r['notes'] + ' ETHICAL WALL: Tom Weller is screened from this matter (since 2026-08-15).'


D['AAMk04f542441d']['why'] += (' Memo 03 (2026-09-30): Tom Weller is screened from 1003-001 since 2026-08-15 and is copied on this 2026-08-26 email, so it is a wall incident (cc).'
                                ' Earlier Tom emails on this matter (2026-08-05, copied on the Anika Brandt deposition email) predate the screen and do not count.')
D['AAMkcd2f45e678']['why'] += ' Tom Weller is also copied, but this is dated 2026-08-05, before his screen starts (2026-08-15), so no incident for Tom (memo 03).'
ACTIONS += [
 ('Jonah Hartwell (ethics partner)', 'AAMk04f542441d', 'Wall incident (memo 03): Tom Weller (screened from 1003-001 since 2026-08-15) was copied on the client\'s Tran mediation authority email of 2026-08-26.'),
 ('Mira Osei', 'AAMk04f542441d', 'The client copied Tom Weller on a Tran matter email (2026-08-26) after his screen began (2026-08-15). Make sure Tom is removed from the Tran distribution and tell the client contact not to copy him.'),
]
