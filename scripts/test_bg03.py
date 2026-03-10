# -*- coding: utf-8 -*-
import requests
BASE = "http://localhost:8080/EShangApiMain"
tests = [
    ("POST", "/BigData/GetBAYONETWARNINGList", {}),
    ("GET",  "/BigData/GetBAYONETWARNINGDetail?BAYONETWARNINGId=1", None),
    ("POST", "/BigData/SynchroBAYONETWARNING", {"BAYONETWARNING_STATE": "1"}),
    ("GET",  "/BigData/DeleteBAYONETWARNING?BAYONETWARNINGId=99999", None),
]
print("=== BG-03 BAYONETWARNING 4 routes ===")
ok = 0
for m, p, b in tests:
    url = BASE + p
    try:
        r = requests.post(url, json=b, timeout=10) if m == "POST" else requests.get(url, timeout=10)
        d = r.json()
        code = d.get("Result_Code", "?")
        desc = str(d.get("Result_Desc", ""))[:50]
        if r.status_code == 200:
            ok += 1
        tag = p.split("?")[0]
        print(f"  [OK] {m:4s} {tag:45s} HTTP={r.status_code} Code={code} {desc}")
    except Exception as e:
        tag = p.split("?")[0]
        print(f"  [FAIL] {m:4s} {tag:45s} {e}")
print(f"\n=== {ok}/4 passed ===")
