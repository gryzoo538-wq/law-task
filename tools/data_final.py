"""Final state after memo 04 (2026-10-01): client 1001 renamed to Brightwater Brands Inc., folder '1001 Brightwater Brands'."""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data_memo3 as prev

CLIENT_PEOPLE = prev.CLIENT_PEOPLE
D = copy.deepcopy(prev.D)
ACTIONS = list(prev.ACTIONS)


def patch_rows(rows):
    prev.patch_rows(rows)
    for r in rows:
        if r['client_no'] == '1001':
            r['client_name'] = 'Brightwater Brands Inc.'
            r['client_folder'] = '1001 Brightwater Brands'
