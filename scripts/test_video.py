# -*- coding: utf-8 -*-
"""Video 模块接口验证脚本"""
import requests

BASE = "http://localhost:8080/EShangApiMain"

tests = [
    ("POST", "/ShopVideo/GetEXTRANETList", {}),
    ("GET",  "/ShopVideo/GetEXTRANETDetail?EXTRANETId=1", None),
    ("POST", "/ShopVideo/SynchroEXTRANET", {"SERVERPART_ID": 1, "EXTRANET_IP": "test"}),
    ("GET",  "/ShopVideo/DeleteEXTRANET?EXTRANETId=99999", None),
    ("POST", "/ShopVideo/GetEXTRANETDETAILList", {}),
    ("GET",  "/ShopVideo/GetEXTRANETDETAILDetail?EXTRANETDETAILId=1", None),
    ("POST", "/ShopVideo/SynchroEXTRANETDETAIL", {"EXTRANET_ID": 1, "VIDEOIP": "test"}),
    ("GET",  "/ShopVideo/DeleteEXTRANETDETAIL?EXTRANETDETAILId=99999", None),
    ("POST", "/ShopVideo/GetSHOPVIDEOList", {}),
    ("GET",  "/ShopVideo/GetSHOPVIDEODetail?SHOPVIDEOId=1", None),
    ("POST", "/ShopVideo/SynchroSHOPVIDEO", {"SERVERPARTCODE": "test"}),
    ("GET",  "/ShopVideo/DeleteSHOPVIDEO?SHOPVIDEOId=99999", None),
    ("POST", "/ShopVideo/GetVIDEOLOGList", {}),
    ("POST", "/ShopVideo/SynchroVIDEOLOG", {"VIDEOLOG_TYPE": 1000, "USER_NAME": "test"}),
    ("GET",  "/ShopVideo/GetShopVideoInfo?ServerpartCode=test&ServerpartShopCode=test", None),
    ("GET",  "/ShopVideo/GetYSShopVideoInfo?ServerpartCode=test&ServerpartShopCode=test", None),
]

print("=== Video 模块 16 条接口验证 ===")
ok_count = 0
fail_count = 0
for method, path, body in tests:
    url = BASE + path
    try:
        if method == "POST":
            r = requests.post(url, json=body, timeout=10)
        else:
            r = requests.get(url, timeout=10)
        data = r.json()
        code = data.get("Result_Code", "?")
        desc = str(data.get("Result_Desc", "?"))[:50]
        status = "OK" if r.status_code == 200 else "FAIL"
        if r.status_code == 200:
            ok_count += 1
        else:
            fail_count += 1
        print(f"  [{status}] {method:4s} {path:55s} HTTP={r.status_code} Code={code} {desc}")
    except Exception as e:
        fail_count += 1
        print(f"  [FAIL] {method:4s} {path:55s} ERROR: {e}")

print(f"\n=== 结果: {ok_count} 成功, {fail_count} 失败 (共 {ok_count + fail_count} 条) ===")
