# -*- coding: utf-8 -*-
"""PI-02 Picture 全量接口验证"""
import requests

BASE = "http://localhost:8080/EShangApiMain"

tests = [
    ("POST", "/Picture/GetPictureList", {}),
    ("GET",  "/Picture/GetPictureDetail?PictureId=1", None),
    ("POST", "/Picture/SynchroPicture", {"TABLE_NAME": "TEST"}),
    ("POST", "/Picture/DeletePicture?PictureId=99999", None),
    ("POST", "/Picture/UploadPicture", {"TABLE_NAME": "TEST"}),
    ("GET",  "/Picture/GetPictureTypeList", None),
    ("GET",  "/Picture/GetPictureByShop?ShopId=test", None),
    ("GET",  "/Picture/GetPictureCount", None),
    ("POST", "/Picture/BatchDeletePicture", []),
    # PI-02 新增 6 条
    ("GET",  "/Picture/GetEndaccountEvidence?EndaccountId=1", None),
    ("POST", "/Picture/UploadEndaccountEvidence", {"EndaccountId": 1, "ImageInfo": "test"}),
    ("GET",  "/Picture/GetAuditEvidence?AuditId=1", None),
    ("POST", "/Picture/UploadAuditEvidence", {"AuditId": 1, "ImageInfo": "test"}),
    ("POST", "/Picture/SaveImgFile", {"TableId": 1}),
    ("POST", "/Picture/DeleteMultiPicture", [{"ImageId": 99999}]),
]

print("=== Picture 全量接口验证 (15 条) ===")
ok_count = 0
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
        print(f"  [{status}] {method:4s} {path.split('?')[0]:45s} HTTP={r.status_code} Code={code} {desc}")
    except Exception as e:
        print(f"  [FAIL] {method:4s} {path.split('?')[0]:45s} ERROR: {e}")

print(f"\n=== {ok_count}/{len(tests)} 通过 ===")
