# Hartwell & Osei firm portal (mock)

Run `python3 firm_portal/server.py` (http://127.0.0.1:8790). Treat it as a black box. Use it over HTTP only, and do not read or edit its other files. State persists in firm_portal/state.json.
Auth header on every request: `Authorization: Bearer ho-portal-token`

| Method | Path | What it does |
|---|---|---|
| GET | /portal/status | which submission stage is expected next; messages released so far; receipts |
| GET | /portal/inbox | the partner's questions and office memos released so far (full text) |
| POST | /portal/submissions | submit work for the current stage (JSON, see below) |

Stages, in order: `phase1` → `partner_answers` → `memo_01` → `memo_02` → `memo_03` → `memo_04` → complete. An accepted submission releases the next message to the inbox. A rejected one returns 422 with the problems found; fix them and resubmit.

Submission body for a filing stage (`phase1` and `memo_01` to `memo_04`):
```json
{"stage": "phase1",
 "filing_log_csv": "<full text of filing_log.csv>",
 "wall_incidents_csv": "<full text of wall_incidents.csv>",
 "summary": {"category_counts": {"matter": 0, "needs_review": 0, "firm_admin": 0, "non_matter": 0, "duplicate": 0}, "box_file_count": 0}}
```
Submission body for `partner_answers`:
```json
{"stage": "partner_answers",
 "answers": {"Q1": {"answer": "...", "evidence_email_files": ["AAMk....eml"]}, "Q2": {...}}}
```
The portal checks a submission's format and internal consistency, and that the memo it responds to was applied. It does not tell you whether your filing decisions are right.
