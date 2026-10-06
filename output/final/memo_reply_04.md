# Reply to memo 04

To: Carla Ruiz (office manager)
Re: Client name change (2026-10-01)

Thank you. Here is exactly what changed in the filing.

- Client 1001 is now "Brightwater Brands Inc." and its client folder is `1001 Brightwater Brands` (was `1001 Brightwater Foods`). Matter numbers and matter folder names are unchanged.
- Every file under the old client folder moved to the new one (emails, extracted Documents and the cross-reference stub for 1001-002). Every `box_path` in filing_log.csv, the stub's "Filed at:" line (the 1001-002 stub is the only stub touching client 1001; it points into 1001-001), the paths quoted in triage_notes.md and attorney_actions.md, and the client name and folder in matters_current.csv were rebuilt from the new name. wall_incidents.csv, needs_review.md and privilege_log.csv quote no client 1001 path, so they are unchanged (checked).
- Left alone on purpose: file names (they contain no client name), sender addresses such as @brightwaterfoods.test (the memo gives no new domain), and document titles in the triage notes that quote what the scans or PDFs actually say ("Brightwater Foods Inc.").

## Emails changed

- **AAMk03552454f1.eml** ("Kestrel - document production vol. 2"): box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml`
- **AAMk0de90794df.eml** ("photos"): box_path: `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-28_0900_whitcomb_photos.eml` -> `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-28_0900_whitcomb_photos.eml`
- **AAMk1162f28d1a.eml** ("Settlement strategy - privileged"): box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1530_osei_settlement-strategy-privileged.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1530_osei_settlement-strategy-privileged.eml`
- **AAMk15d7185dda.eml** ("April emails"): box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-20_1145_whitcomb_april-emails.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-20_1145_whitcomb_april-emails.eml`
- **AAMk32d7a94ded.eml** ("Deposition of D. Whitcomb"): box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb.eml`
- **AAMk41b53302fc.eml** ("SunHarvest response filed"): box_path: `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-20_1520_park_sunharvest-response-filed.eml` -> `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-20_1520_park_sunharvest-response-filed.eml`
- **AAMk4ad8b9b45c.eml** ("Settlement discussion (FRE 408)"): box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1100_tolland_settlement-discussion-fre-408.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1100_tolland_settlement-discussion-fre-408.eml`
- **AAMk5376c468ae.eml** ("Board minutes Q2"): box_path: `box/Clients/1001 Brightwater Foods/1001-003 General Corporate/Correspondence/2026-08-14_0905_whitcomb_board-minutes-q2.eml` -> `box/Clients/1001 Brightwater Brands/1001-003 General Corporate/Correspondence/2026-08-14_0905_whitcomb_board-minutes-q2.eml`
- **AAMk65fb710734.eml** ("Litigation hold notice - Kestrel dispute"): box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_0900_osei_litigation-hold-notice-kestrel-dispute.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_0900_osei_litigation-hold-notice-kestrel-dispute.eml`
- **AAMk73f6fa5db8.eml** ("Two things"): box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-things.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-things.eml`
- **AAMk9770c6a5b8.eml** ("Deposition of D. Whitcomb"): box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb_dup.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb_dup.eml`
- **AAMk980ab8ab67.eml** ("RE: Brightwater v. Kestrel - proposed protective order"): box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-07_1100_tolland_brightwater-v-kestrel-proposed-protectiv.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-07_1100_tolland_brightwater-v-kestrel-proposed-protectiv.eml`
- **AAMkbda7677796.eml** ("Kestrel production - Bates ranges"): box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-11_1010_weller_kestrel-production-bates-ranges.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-11_1010_weller_kestrel-production-bates-ranges.eml`
- **AAMkc7ec99108d.eml** ("Brightwater v. Kestrel - proposed protective order"): box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-04_1005_tolland_brightwater-v-kestrel-proposed-protectiv.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-04_1005_tolland_brightwater-v-kestrel-proposed-protectiv.eml`
- **AAMkdb8f4d3e27.eml** ("SunHarvest - USPTO office action"): box_path: `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-03_1440_park_sunharvest-uspto-office-action.eml` -> `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-03_1440_park_sunharvest-uspto-office-action.eml`
- **AAMkdd73cf256d.eml** ("Kestrel shipment records"): box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-03_0912_whitcomb_kestrel-shipment-records.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-03_0912_whitcomb_kestrel-shipment-records.eml`
- **AAMkecc20ef164.eml** ("Old April mailbox"): box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-25_1600_whitcomb_old-april-mailbox.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-25_1600_whitcomb_old-april-mailbox.eml`

## Wall incidents

Added: none
Removed: none

## needs_review

Removed: none
Added: none

## Attorney actions

Added: none
Removed: none

## Files in box/

25 paths removed, 25 paths added.

Old path -> new path (every renamed file):

- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-03_0912_whitcomb_kestrel-shipment-records.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-03_0912_whitcomb_kestrel-shipment-records.eml`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-04_1005_tolland_brightwater-v-kestrel-proposed-protectiv.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-04_1005_tolland_brightwater-v-kestrel-proposed-protectiv.eml`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-07_1100_tolland_brightwater-v-kestrel-proposed-protectiv.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-07_1100_tolland_brightwater-v-kestrel-proposed-protectiv.eml`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_0900_osei_litigation-hold-notice-kestrel-dispute.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_0900_osei_litigation-hold-notice-kestrel-dispute.eml`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-things.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-things.eml`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-11_1010_weller_kestrel-production-bates-ranges.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-11_1010_weller_kestrel-production-bates-ranges.eml`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb.eml`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb_dup.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb_dup.eml`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-20_1145_whitcomb_april-emails.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-20_1145_whitcomb_april-emails.eml`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1100_tolland_settlement-discussion-fre-408.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1100_tolland_settlement-discussion-fre-408.eml`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1530_osei_settlement-strategy-privileged.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1530_osei_settlement-strategy-privileged.eml`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-25_1600_whitcomb_old-april-mailbox.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-25_1600_whitcomb_old-april-mailbox.eml`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-08-03_delivery_logs_mar-may.pdf` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-08-03_delivery_logs_mar-may.pdf`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-08-04_proposed_protective_order.pdf` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-08-04_proposed_protective_order.pdf`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-08-10_litigation_hold_notice.pdf` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-08-10_litigation_hold_notice.pdf`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-08-20_april_emails.pdf` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-08-20_april_emails.pdf`
- `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-09-14_production_vol2_index.pdf` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-09-14_production_vol2_index.pdf`
- `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-03_1440_park_sunharvest-uspto-office-action.eml` -> `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-03_1440_park_sunharvest-uspto-office-action.eml`
- `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-10_1430_whitcomb_two-things.eml.xref.txt` -> `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-10_1430_whitcomb_two-things.eml.xref.txt`
- `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-20_1520_park_sunharvest-response-filed.eml` -> `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-20_1520_park_sunharvest-response-filed.eml`
- `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-28_0900_whitcomb_photos.eml` -> `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-28_0900_whitcomb_photos.eml`
- `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Documents/2026-08-28_IMG_2211.pdf` -> `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Documents/2026-08-28_IMG_2211.pdf`
- `box/Clients/1001 Brightwater Foods/1001-003 General Corporate/Correspondence/2026-08-14_0905_whitcomb_board-minutes-q2.eml` -> `box/Clients/1001 Brightwater Brands/1001-003 General Corporate/Correspondence/2026-08-14_0905_whitcomb_board-minutes-q2.eml`
- `box/Clients/1001 Brightwater Foods/1001-003 General Corporate/Documents/2026-08-14_q2_minutes.pdf` -> `box/Clients/1001 Brightwater Brands/1001-003 General Corporate/Documents/2026-08-14_q2_minutes.pdf`

Counts after the change (before in brackets):

- matter: 54 [54]
- needs_review: 1 [1]
- firm_admin: 3 [3]
- non_matter: 4 [4]
- duplicate: 2 [2]
- by matter (changed only): none
- by attorney (changed only): none
- files in box/: 91 [91]
- wall incidents: 4 [4]; privilege log entries: 7 [7]; needs_review emails: 1 [1]
