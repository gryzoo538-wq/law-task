# Task inputs (complete set: 70 input files, plus this list and MANIFEST.sha256)

| Path | Count | What it is |
|---|---|---|
| mailbox/*.eml | 64 | Outlook export of the firm's mailbox (RFC 822 .eml files). Together they carry 24 PDF attachments, 15 of them image-only scans |
| matters.csv | 1 | Clients and matters: folder names, responsible attorney, status, closed dates, litigation hold, ethical wall, restricted flag |
| staff.csv | 1 | Firm staff and roles |
| filing_rules.md | 1 | The firm's filing rules |
| firm_portal/server.py, README.md, fixtures.bin | 3 | The firm's review portal (local mock). It delivers the partner's questions and four dated memos (2026-09-27 to 2026-10-01) one at a time, after each accepted submission |

MANIFEST.sha256 lists the SHA-256 checksum of every file. Check it with `sha256sum -c MANIFEST.sha256`.
All people, firms, clients, matters and addresses are fictional. The .test domains are reserved and do not exist.
