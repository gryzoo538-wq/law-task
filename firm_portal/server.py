#!/usr/bin/env python3
"""Hartwell & Osei firm portal (mock). Delivers partner review questions and office memos in sequence,
and receives filing submissions. Run: python3 firm_portal/server.py  (http://127.0.0.1:8790)
Treat as a black box: use it over HTTP only."""
import json, zlib, base64, csv, io, re, os, argparse, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
HERE=os.path.dirname(os.path.abspath(__file__)); SF=os.path.join(HERE,"state.json")
FX=json.loads(zlib.decompress(base64.b64decode(open(os.path.join(HERE,"fixtures.bin")).read())))
ap=argparse.ArgumentParser(); ap.add_argument("--port",type=int,default=8790); A=ap.parse_args()
STAGES=["phase1","partner_answers","memo_01","memo_02","memo_03","memo_04","complete"]
RELEASE={"phase1":"partner_review","partner_answers":"memo_01","memo_01":"memo_02","memo_02":"memo_03","memo_03":"memo_04"}
LOCK=threading.Lock()
def load():
    try: return json.load(open(SF))
    except Exception: return {"stage":"phase1","released":[],"receipts":[]}
def save(s): json.dump(s,open(SF,"w"),indent=1)
CATS={"matter","needs_review","firm_admin","non_matter","duplicate"}
FLAGS={"hold","post-closing","ethical-wall","potential-conflict","new-matter-request","misdirected","phishing","delivery-failure","restricted","duplicate-retained","attorney-action"}
HDR=["email_file","received","sender","subject","category","primary_matter","xref_matters","privilege","flags","box_path","attachments_saved"]
NAME=re.compile(r"^\d{4}-\d{2}-\d{2}_\d{4}_[a-z0-9]+_[a-z0-9-]+(_dup)?\.eml$")
def check_log(b,stage,errs):
    try: rows=list(csv.DictReader(io.StringIO(b.get("filing_log_csv",""))))
    except Exception as e: errs.append(f"filing_log_csv is not valid CSV: {e}"); return []
    if not rows: errs.append("filing_log_csv is empty"); return []
    if list(rows[0].keys())!=HDR: errs.append("filing_log_csv header must be exactly: "+",".join(HDR))
    names=[r.get("email_file") for r in rows]
    if len(rows)!=64: errs.append(f"filing_log_csv must have 64 rows (got {len(rows)})")
    miss=set(FX["mailbox"])-set(names); extra=set(names)-set(FX["mailbox"])
    if miss: errs.append(f"{len(miss)} mailbox emails missing from the log, e.g. {sorted(miss)[:3]}")
    if extra: errs.append(f"unknown email_file values: {sorted(extra)[:3]}")
    if len(set(names))!=len(names): errs.append("email_file values must be unique")
    matters=set(FX["matters"])|({"1002-003"} if STAGES.index(stage)>=2 else set())|({"1007-002"} if STAGES.index(stage)>=3 else set())
    flags=FLAGS|({"declined-intake"} if STAGES.index(stage)>=3 else set())
    pre={"needs_review":"box/_Needs_Review/","firm_admin":"box/Firm_Admin/","non_matter":"box/_Non_Matter/","duplicate":"box/_Duplicates/"}
    for r in rows:
        c=r.get("category",""); f=r.get("email_file"); p=r.get("box_path","")
        if c not in CATS: errs.append(f"{f}: unknown category '{c}'"); continue
        if c=="matter" and r.get("primary_matter") not in matters: errs.append(f"{f}: primary_matter '{r.get('primary_matter')}' is not an open matter at this stage")
        if c!="matter" and r.get("primary_matter"): errs.append(f"{f}: primary_matter must be blank for category {c}")
        if c=="matter" and not (p.startswith("box/Clients/") or p.startswith("box/Restricted/")): errs.append(f"{f}: matter emails belong under box/Clients/ or box/Restricted/")
        if c in pre and not p.startswith(pre[c]): errs.append(f"{f}: {c} emails belong under {pre[c]}")
        if not NAME.match(p.split("/")[-1]): errs.append(f"{f}: file name '{p.split('/')[-1]}' does not follow the naming rule")
        bad=[x for x in (r.get("flags") or "").split(";") if x and x not in flags]
        if bad: errs.append(f"{f}: unknown flags {bad}")
        if (c=="matter")!=(r.get("privilege") in ("AC","WP","none")): errs.append(f"{f}: privilege must be AC/WP/none for matter emails and n/a otherwise")
    cc=b.get("summary",{}).get("category_counts")
    real={k:sum(1 for r in rows if r.get("category")==k) for k in CATS}
    if not isinstance(cc,dict): errs.append("summary.category_counts is required")
    elif {k:int(cc.get(k,0)) for k in CATS}!=real: errs.append("summary.category_counts does not match the filing log")
    if not isinstance(b.get("summary",{}).get("box_file_count"),int): errs.append("summary.box_file_count (integer) is required")
    if "wall_incidents_csv" not in b: errs.append("wall_incidents_csv is required")
    return rows
def check(b,stage):
    errs=[]
    if stage=="partner_answers":
        ans=b.get("answers")
        if not isinstance(ans,dict): return ["answers object is required"]
        for q in FX["questions"]:
            a=ans.get(q["id"])
            if not isinstance(a,dict): errs.append(f"{q['id']}: answer missing"); continue
            if len(a.get("answer","").strip())<60: errs.append(f"{q['id']}: answer is too short to be reviewed (60+ characters)")
            ev=a.get("evidence_email_files") or []
            if not ev or any(e not in FX["mailbox"] for e in ev): errs.append(f"{q['id']}: evidence_email_files must list mailbox file names")
        return errs
    rows=check_log(b,stage,errs)
    if errs: return errs
    if stage=="memo_01" and not any(r["primary_matter"]=="1002-003" for r in rows): errs.append("memo_01 has not been applied: nothing is filed in 1002-003")
    if stage=="memo_02":
        if not any(r["primary_matter"]=="1007-002" for r in rows): errs.append("memo_02 has not been applied: nothing is filed in 1007-002")
        if not any("declined-intake" in r["flags"] and r["box_path"].startswith("box/Firm_Admin/Declined_Intake/") for r in rows): errs.append("memo_02 has not been applied: no declined intake filed under box/Firm_Admin/Declined_Intake/")
    if stage=="memo_03":
        w=list(csv.DictReader(io.StringIO(b["wall_incidents_csv"])))
        tom=[x for x in w if "Weller" in (x.get("screened_person") or "")]
        if not tom: errs.append("memo_03 has not been applied: no incidents for Tom Weller")
        if any((x.get("received") or "")[:10]<"2026-08-15" for x in tom): errs.append("memo_03: Tom Weller's screen starts on 2026-08-15")
    if stage=="memo_04":
        if any("Brightwater Foods" in r["box_path"] for r in rows): errs.append("memo_04 has not been applied: paths still use '1001 Brightwater Foods'")
    return errs
class H(BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def send(self,code,obj):
        b=json.dumps(obj,indent=1).encode(); self.send_response(code); self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def ok(self):
        if self.headers.get("Authorization")!="Bearer ho-portal-token": self.send(401,{"error":"unauthorized"}); return False
        return True
    def do_GET(self):
        if not self.ok(): return
        s=load()
        if self.path=="/portal/status":
            return self.send(200,{"stage_expected":s["stage"],"released_messages":s["released"],"receipts":s["receipts"]})
        if self.path=="/portal/inbox":
            msgs=[]
            for m in s["released"]:
                if m=="partner_review": msgs.append({"id":m,"date":"2026-09-27","from":"Mira Osei (partner)","subject":"Questions on your first filing pass","questions":FX["questions"]})
                else: msgs.append({"id":m,**FX["memos"][m]})
            return self.send(200,{"messages":msgs})
        self.send(404,{"error":"not found"})
    def do_POST(self):
        if not self.ok(): return
        if self.path!="/portal/submissions": return self.send(404,{"error":"not found"})
        try: b=json.loads(self.rfile.read(int(self.headers.get("Content-Length",0))))
        except Exception: return self.send(400,{"error":"body must be JSON"})
        with LOCK:
            s=load(); st=s["stage"]
            if st=="complete": return self.send(409,{"error":"all stages are complete"})
            if b.get("stage")!=st: return self.send(409,{"error":f"expected a submission for stage '{st}'"})
            errs=check(b,st)
            if errs: return self.send(422,{"accepted":False,"stage":st,"errors":errs[:40]})
            rid=f"HO-{len(s['receipts'])+1:03d}"; s["receipts"].append({"receipt":rid,"stage":st,"at":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())})
            nxt=RELEASE.get(st); s["stage"]=STAGES[STAGES.index(st)+1]
            if nxt: s["released"].append(nxt)
            save(s)
            return self.send(200,{"accepted":True,"receipt":rid,"released":nxt,"stage_expected_next":s["stage"]})
print(f"Firm portal on http://127.0.0.1:{A.port}",flush=True)
ThreadingHTTPServer(("127.0.0.1",A.port),H).serve_forever()
