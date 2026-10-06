# Verification log

All outputs below are from runs made at the end of the job, after the last rebuild.

## 1. Input confirmation (before filing)
- `sha256sum -c MANIFEST.sha256`: 72 files OK, 0 failures.
- Folder vs INPUTS.md: 64 mailbox/*.eml, matters.csv, staff.csv, filing_rules.md and 4 memos = 71 input files, all present and non-empty; INPUTS.md is also present. The manifest lists those 72 files (the 71 plus INPUTS.md) and not itself.
- Extra file not in the manifest or INPUTS.md: `count_steps.py` (an unrelated step-counting script). Not used and not an input. Reported, nothing else done with it.
- All 64 .eml parse (Python email parser, no defects); they carry 24 attachments, all `application/pdf`, and all 24 open (`pdfinfo`). 9 have a text layer and 15 are image-only (0 words from `pdftotext`).
- Memos were not opened until Part 3 (only checksummed).

## 2. Scans re-opened as images (final check)
Rendered again from the extracted copies in `output/final/box/**/Documents/` (so this also proves the saved file is the scan), cropped to the text and viewed.

| email | saved file | orientation seen | what the image shows | matter in final log | matches? |
|---|---|---|---|---|---|
| AAMk0de90794df | 2026-08-28_IMG_2211.pdf | upright | Specimen of use, mark SUNHARVEST, retail packaging label | 1001-002 | yes |
| AAMk15a9964aef | 2026-08-18_coi.pdf | rotated 90 | Certificate of liability insurance, holder Blue Heron Marina LLC, Re: Slip C lease | 1007-001 | yes |
| AAMk30965eda32 | 2026-08-05_landlord_letter.pdf | upside down (180) | Harborview Properties, Dock 7 lease renewal counter-proposal, 4% escalator, tenant Northpoint Logistics LLC | 1003-002 | yes |
| AAMk360023b682 | 2026-08-27_scan0047.pdf | upright | Letters testamentary, Estate of Ricardo Delgado, executor Maria Delgado | 1002-001 | yes |
| AAMk6078511608 | 2026-08-28_doc_0828.pdf | upside down (180) | Confidential, Calloway Medical Group PC, risk assessment of July access incident | 1004-001 | yes |
| AAMk6b65bd9acb | 2026-09-01_statement_jul.pdf | upright, slightly skewed | First Harbor Bank statement, Paul Ostrander, July 2026 | 1005-001 | yes |
| AAMk7218187993 | 2026-08-06_sigpage.pdf | upright | Blue Heron Marina LLC, Slip C lease signature page, signed S. Pryce | 1007-001 | yes |
| AAMk737734d7c1 | 2026-08-04_scan_0812.pdf | rotated 90 | Appraisal report, 88 Alder Street, Estate of Ricardo Delgado, $412,000 | 1002-001 | yes |
| AAMk8917362f25 | 2026-08-06_ledger.pdf | upright | Fenwick Lane HOA owner ledger, unit 22 (K. Albright), $1,860.00 | 1006-001 | yes |
| AAMk9012b2a414 | 2026-09-02_receipt.pdf | upright | Blue Heron Marina LLC, Slip C first month rent receipt no. 0091 | 1007-001 | yes |
| AAMk9f28518867 | 2026-08-11_personnel_excerpt.pdf | upright | Northpoint Logistics personnel file, employee Jessica Tran | 1003-001 | yes |
| AAMkb5faf8cda9 | 2026-08-31_scan_lien.pdf | upright | Notice of mechanic's lien, Rivera & Sons Roofing, 210 Mill Street | 1008-001 | yes |
| AAMkc250b601fc | 2026-08-21_parenting_plan.pdf | upright | Proposed parenting plan, In re the Marriage of Ostrander | 1005-001 | yes |
| AAMke3cf44dd3f | 2026-08-07_hoa_letter.pdf | upright, slightly skewed | Fenwick Lane HOA letter to Maria Delgado, 14 Fenwick Lane, transfer fee $750 | 1002-002 | yes |
| AAMked35b00a54 | 2026-08-27_scan0103.pdf | rotated 90 | Lease Amendment No. 3, Dock 7, Harborview Properties / Northpoint Logistics, EXECUTED | 1003-002 | yes |

No scan changed matter. Note: the brief said one scan is rotated; I found five (coi, landlord_letter, doc_0828, scan_0812, scan0103). All were read in their correct orientation.

## 3. Re-read of flagged, needs_review and sensitive-name emails
I listed every email whose headers, subject or body mention Heron, Fenwick, Kestrel, Tran, Anika/abrandt or Tom/tweller together with its final category, matter, cross-reference, privilege and flags, and checked each against the rules:
- **Heron**: Project Heron (Calloway, 1004-002) = escrow instructions, diligence responses, board-approved checklist, plus the Board update (primary 1004-001 restricted, stub in 1004-002). Blue Heron Marina (1007) = insurance certificate scan, signature page scan, receipt scan (1007-001) and the fuel dock email (1007-002 after memo 02). Paul Ostrander's brother's slip request stays in 1005-001 with potential-conflict;new-matter-request. No cross-client stub exists.
- **Fenwick**: HOA client 1006 (unit 22 ledger, unit 14 transfer fee) vs Delgado purchase 1002-002 (HOA letter, post-closing, conflict). The unit 14 email is in 1006-001 with potential-conflict and no stub in any Delgado folder.
- **Kestrel**: 11 emails mention it; the deposition notices, the FRE 408 note and Dana's "Old April mailbox" email do not contain the word in text but are filed in 1001-001 by sender and context. Hold flag only on or after 2026-08-10 (10 log rows: 9 originals incl. the hold notice itself on the start date, plus the retained duplicate); 08-03, 08-04 and 08-07 emails correctly have none; 08-07 duplicate goes to _Duplicates; 08-14 duplicate retained as _dup with hold;duplicate-retained. Kestrel's CEO request: needs_review in phase 1, firm_admin/Declined_Intake in final.
- **Tran / screened people**: five Tran emails; Anika Brandt is on three (sender 08-05, cc 08-11, cc 08-18 via the stub); Tom Weller (screen from 2026-08-15) is on one qualifying email (cc 08-26); his 08-05 cc predates the screen. Anika's 09-08 Dock 7 email (1003-002) is not an incident because she is screened only from 1003-001. Q3 billing notice (all staff) is not matter content.
- **needs_review**: phase 1 five (fuel dock, Martinez misdirected, two bakery, Kestrel request); final one (Martinez). Each has reason, decision needed and decider in needs_review.md.

## 4. Cross-file agreement (computed)
- phase1: triage_notes.md vs filing_log.csv (category, matter, xref, privilege, flags, path exists): 64 triage entries, 64 log rows, 0 mismatches.
- final: triage_notes.md vs filing_log.csv (category, matter, xref, privilege, flags, path exists): 64 triage entries, 64 log rows, 0 mismatches.
- Log vs box/ (every box_path exists, no extra or missing file, byte-identical copies, attachments and stubs, wall incidents and privilege log recomputed from the inputs, summary counts): done by `tools/check_filing.py`, see section 6.
- changes_report.md vs a fresh phase1/final comparison: 22 emails differ; 22 listed in the report; sets equal: True.
- Emails named in memo_reply_01..04 together = 22; equal to the changes_report set: True.
- Wall incidents 3 -> 4; privilege log 7 -> 7 (identical files: True).

## 5. Mistakes found and what I changed
- Phase 1 data: I had given Hank Moreau's "Dock 7 - and one more thing" email the `attorney-action` flag. Rule 5 reserves it for client requests the hold forbids; the Tran question is an action-list item only. Removed before the first build.
- Checker v1 failed on the two duplicate pairs: it demanded exactly one file per content hash, but a duplicate is byte-identical to its original. The checker was wrong, not the data. It now compares per-hash file counts with the number of mailbox emails sharing that content.
- After memo 02 the checker reported that the Kestrel intake email (flags declined-intake;new-matter-request) was not on attorney_actions.md, because I had removed its old conflict entries. Added a closing action for Jonah Hartwell.
- My first attachment-rename break test did not run (shell word-splitting on folder names with spaces), so its "PASS" was meaningless. Redone in Python; the rename is caught (section 7).
- memo_reply_04 first claimed paths in wall_incidents.csv and needs_review.md had been rebuilt; they contain no client 1001 paths. Corrected to say exactly which files contain the old name and which do not (verified by grep: the old folder name now appears only inside the two report files that quote it as the "old path" and in document titles quoted in triage_notes).
- Memo 03 action for Mira wrongly implied she had copied Tom; the client did. Reworded.
- Brief said one scan is rotated; there are five. Triage notes describe each scan in its true orientation.
- Re-reading the decisions at the end found no further mistake in categories, matters, flags or privilege. No unresolved mistake remains.

## 6. Final checker output
### python3 tools/check_filing.py output/phase1
```
checked 64 log rows, 64 .eml, 3 stubs, 91 files in box/
PASS: all checks passed
exit code 0
```
### python3 tools/check_filing.py output/final
```
checked 64 log rows, 64 .eml, 3 stubs, 91 files in box/
PASS: all checks passed
exit code 0
```

## 7. Deliberate-break test (copy of each output folder in a scratch dir)
### output/phase1
```
## break_move: moved 2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml out of its matter Correspondence folder into box/Firm_Admin/
exit code 1 (CAUGHT)
    checked 64 log rows, 64 .eml, 3 stubs, 91 files in box/
    FAIL: 3 problem(s)
     - AAMk03552454f1.eml: box_path does not exist: box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml
     - unexpected/unlogged file in box/: box/Firm_Admin/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml
     - unexpected/unlogged file in box/: box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-09-14_production_vol2_index.pdf
## break_stub: overwrote stub 2026-08-10_1430_whitcomb_two-things.eml.xref.txt with a path that does not exist
exit code 1 (CAUGHT)
    checked 64 log rows, 64 .eml, 3 stubs, 91 files in box/
    FAIL: 1 problem(s)
     - stub box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-10_1430_whitcomb_two-things.eml.xref.txt: "Filed at" path does not exist: box/Clients/1009 Nowhere/missing.eml
## break_attachment: renamed extracted attachment 2026-08-03_delivery_logs_mar-may.pdf to renamed_delivery_logs.pdf
exit code 1 (CAUGHT)
    checked 64 log rows, 64 .eml, 3 stubs, 91 files in box/
    FAIL: 2 problem(s)
     - AAMkdd73cf256d.eml: extracted attachment missing: box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-08-03_delivery_logs_mar-may.pdf
     - unexpected/unlogged file in box/: box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/renamed_delivery_logs.pdf
## break_all_three: moved 2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml out of its matter Correspondence folder into box/Firm_Admin/ + overwrote stub 2026-08-10_1430_whitcomb_two-things.eml.xref.txt with a path that does not exist + renamed extracted attachment 2026-08-03_delivery_logs_mar-may.pdf to renamed_delivery_logs.pdf
exit code 1 (CAUGHT)
    checked 64 log rows, 64 .eml, 3 stubs, 91 files in box/
    FAIL: 6 problem(s)
     - AAMk03552454f1.eml: box_path does not exist: box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml
     - AAMkdd73cf256d.eml: extracted attachment missing: box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-08-03_delivery_logs_mar-may.pdf
     - stub box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-10_1430_whitcomb_two-things.eml.xref.txt: "Filed at" path does not exist: box/Clients/1009 Nowhere/missing.eml
     - unexpected/unlogged file in box/: box/Firm_Admin/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml
     - unexpected/unlogged file in box/: box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/renamed_delivery_logs.pdf
     - unexpected/unlogged file in box/: box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-09-14_production_vol2_index.pdf
RESULT: all breaks caught
```
### output/final
```
## break_move: moved 2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml out of its matter Correspondence folder into box/Firm_Admin/
exit code 1 (CAUGHT)
    checked 64 log rows, 64 .eml, 3 stubs, 91 files in box/
    FAIL: 3 problem(s)
     - AAMk03552454f1.eml: box_path does not exist: box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml
     - unexpected/unlogged file in box/: box/Firm_Admin/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml
     - unexpected/unlogged file in box/: box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-09-14_production_vol2_index.pdf
## break_stub: overwrote stub 2026-08-10_1430_whitcomb_two-things.eml.xref.txt with a path that does not exist
exit code 1 (CAUGHT)
    checked 64 log rows, 64 .eml, 3 stubs, 91 files in box/
    FAIL: 1 problem(s)
     - stub box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-10_1430_whitcomb_two-things.eml.xref.txt: "Filed at" path does not exist: box/Clients/1009 Nowhere/missing.eml
## break_attachment: renamed extracted attachment 2026-08-03_delivery_logs_mar-may.pdf to renamed_delivery_logs.pdf
exit code 1 (CAUGHT)
    checked 64 log rows, 64 .eml, 3 stubs, 91 files in box/
    FAIL: 2 problem(s)
     - AAMkdd73cf256d.eml: extracted attachment missing: box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-08-03_delivery_logs_mar-may.pdf
     - unexpected/unlogged file in box/: box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/renamed_delivery_logs.pdf
## break_all_three: moved 2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml out of its matter Correspondence folder into box/Firm_Admin/ + overwrote stub 2026-08-10_1430_whitcomb_two-things.eml.xref.txt with a path that does not exist + renamed extracted attachment 2026-08-03_delivery_logs_mar-may.pdf to renamed_delivery_logs.pdf
exit code 1 (CAUGHT)
    checked 64 log rows, 64 .eml, 3 stubs, 91 files in box/
    FAIL: 6 problem(s)
     - AAMk03552454f1.eml: box_path does not exist: box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml
     - AAMkdd73cf256d.eml: extracted attachment missing: box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-08-03_delivery_logs_mar-may.pdf
     - stub box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-10_1430_whitcomb_two-things.eml.xref.txt: "Filed at" path does not exist: box/Clients/1009 Nowhere/missing.eml
     - unexpected/unlogged file in box/: box/Firm_Admin/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml
     - unexpected/unlogged file in box/: box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/renamed_delivery_logs.pdf
     - unexpected/unlogged file in box/: box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-09-14_production_vol2_index.pdf
RESULT: all breaks caught
```
Extra mutations on a copy of output/final (all caught): a stub pointing into another client's folder; a restricted email moved under box/Clients (file and log both moved, so only the rule can catch it); a file and its log row renamed to a wrong-case name; the retained hold duplicate deleted; a summary count edited; a wall incident row deleted.
```
CAUGHT      stub crosses clients | [' - stub box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-10_1430_whitcomb_two-things.eml.xref.txt: crosses clients (1001 Brightwater Brands vs 1002 Delgado Maria)']
CAUGHT      restricted item under Clients | [' - AAMk9da13ffe79.eml: box_path does not exist: box/Restricted/1004 Calloway Medical Group/1004-001 Privacy Investigation/Correspondence/2026-08-05_1502_varga_incident-timeline-draft.eml']
CAUGHT      wrong file name | [' - AAMk04f542441d.eml: box_path does not exist: box/Clients/1003 Northpoint Logistics/1003-001 Tran Employment Claim/Correspondence/2026-08-26_0945_moreau_tran-mediation-authority.eml']
CAUGHT      hold duplicate deleted | [' - box/ holds 63 .eml files, expected 64']
CAUGHT      summary count edited | [' - filing_summary category matter: 53 vs log 54']
CAUGHT      wall incident row deleted | [" - wall incident missing: ('AAMk04f542441d.eml', 'Tom Weller', 'cc', '1003-001')"]
naming rule (file+log both renamed): [' - AAMk04f542441d.eml: file name "2026-08-26_0945_Moreau_Tran-mediation-authority.eml" does not follow the naming rule (expected "2026-08-26_0945_moreau_tran-mediation-authority.eml")']
restricted rule (file+log both moved): [' - AAMk9da13ffe79.eml: box_path "box/Clients/1004 Calloway Medical Group/1004-001 Privacy Investigation/Correspondence/2026-08-05_1502_varga_incident-timeline-draft.eml" should be "box/Restricted/1004 Calloway Medical Group/1004-001 Privacy Investigation/Correspondence/2026-08-05_1502_varga_incident-timeline-draft.eml"', ' - AAMk9da13ffe79.eml: restricted matter item outside box/Restricted/', ' - AAMk9da13ffe79.eml: extracted attachment missing: box/Clients/1004 Calloway Medical Group/1004-001 Privacy Investigation/Documents/2026-08-05_incident_timeline_draft.pdf']
```

## 8. Judgment calls that remain open for the firm (not mistakes)
- Duplicate pairs have identical Date headers, so "earlier" is not defined by time; I used the lower file name as the original. Both pairs carry identical content, so nothing else differs.
- Paul Ostrander's brother (slip contract at Blue Heron Marina): flagged potential-conflict and new-matter-request and left in 1005-001; the memos do not mention it.
- Maria Delgado's HOA letter (08-07) carries potential-conflict as well as post-closing; the HOA email (08-21) carries potential-conflict. If the firm treats only one side as the conflict email, drop the flag on the other.
- Kestrel intake email keeps new-matter-request after memo 02 because the memo replaces only potential-conflict.
- Privilege for duplicates is n/a (they are not matter-category); neither duplicate is AC or WP, so the privilege log is unaffected.
- Client contacts were inferred from sender domains and content (client contacts are not listed): see CLIENT_PEOPLE in tools/data_phase1.py.
