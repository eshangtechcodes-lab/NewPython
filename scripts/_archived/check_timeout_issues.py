# -*- coding: utf-8 -*-
"""
检查旧API超时接口中新API有问题的 5 个
"""
import requests, json, os

os.environ["NO_PROXY"] = "localhost,127.0.0.1,10.*,192.168.*"
NEW = "http://127.0.0.1:8080/CommercialApi"

TESTS = [
    # #21 GetServerpartList - TODO 占位
    ("GET", "/BaseInfo/GetServerpartList",
     {"Province_Code": "340000"},
     "服务区列表(TODO)"),
    
    # #67 GetPATROLDetail - 测试ID问题
    ("GET", "/Examine/GetPATROLDetail",
     {"PATROLId": 10},
     "巡检明细(ID=10)"),
    # 换个更大的ID试试
    ("GET", "/Examine/GetPATROLDetail",
     {"PATROLId": 100},
     "巡检明细(ID=100)"),

    # #69 WeChat_GetExamineDetail - 422
    ("GET", "/Examine/WeChat_GetExamineDetail",
     {"ExamineId": 10},
     "微信考核明细"),

    # #84 Revenue/GetBudgetExpenseList POST - T=0
    ("POST", "/Revenue/GetBudgetExpenseList",
     {"PageIndex": 1, "PageSize": 5},
     "预算费用列表(POST)"),

    # #114 Revenue/GetTransactionDetailList - 422
    ("GET", "/Revenue/GetTransactionDetailList",
     {"ProvinceCode": "340000", "Serverpart_ID": "416"},
     "交易明细列表"),
]

for method, path, params, desc in TESTS:
    print(f"\n--- {desc}: [{method}] {path} ---")
    print(f"  传参: {json.dumps(params, ensure_ascii=False)}")
    try:
        if method == "GET":
            r = requests.get(NEW + path, params=params, timeout=10)
        else:
            r = requests.post(NEW + path, json=params, timeout=10)
        print(f"  HTTP: {r.status_code}")
        if r.status_code == 200:
            body = r.json()
            code = body.get("Result_Code")
            msg = body.get("Result_Msg", "")[:80]
            rd = body.get("Result_Data")
            if isinstance(rd, dict):
                total = rd.get("TotalCount")
                print(f"  Code={code}, Msg={msg}, TotalCount={total}")
            else:
                print(f"  Code={code}, Msg={msg}")
        elif r.status_code == 422:
            for d in r.json().get("detail", [])[:5]:
                print(f"  422: 缺少 {d.get('loc',[])} - {d.get('msg','')}")
    except Exception as e:
        print(f"  异常: {e}")
