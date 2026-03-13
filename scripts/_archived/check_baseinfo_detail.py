# -*- coding: utf-8 -*-
"""
列出 BaseInfo 每个接口的【测试传参】、【新API路由定义的参数】和【响应】
只查新 API（旧API结果已在compare_all.json中）
"""
import requests, json

NEW = "http://127.0.0.1:8080/CommercialApi"

# 全量对比测试时 compare_all.py 中 get_test_params 传的参数
TESTS = [
    ("GET",  "/BaseInfo/GetSPRegionList",
     {"Province_Code": "340000"},
     "片区列表"),
    ("GET",  "/BaseInfo/GetBusinessTradeList",
     {"pushProvinceCode": "340000"},
     "业态列表(GET)"),
    ("POST", "/BaseInfo/GetBusinessTradeList",
     {"PageIndex": 1, "PageSize": 3},
     "业态列表(POST)"),
    ("POST", "/BaseInfo/GetShopCountList",
     {"PageIndex": 1, "PageSize": 3},
     "门店数量(POST)"),
    ("GET",  "/BaseInfo/GetShopCountList",
     {"Province_Code": "340000"},
     "门店数量(GET)"),
    ("GET",  "/BaseInfo/GetBrandAnalysis",
     {"ProvinceCode": "340000", "Serverpart_ID": "416"},
     "品牌分析"),
    ("GET",  "/BaseInfo/GetServerpartList",
     {"Province_Code": "340000"},
     "服务区列表"),
    ("GET",  "/BaseInfo/GetServerpartInfo",
     {"ProvinceCode": "340000", "Serverpart_ID": "416"},
     "服务区信息"),
    ("GET",  "/BaseInfo/GetServerInfoTree",
     {"Province_Code": "340000"},
     "服务区树"),
    ("POST", "/BaseInfo/GetServerpartServiceSummary",
     {"name": "", "value": ""},
     "基础设施汇总"),
    ("POST", "/BaseInfo/GetBrandStructureAnalysis",
     {"name": "", "value": ""},
     "品牌结构分析"),
]

# 旧API对比测试结果（来自 compare_all.json）
OLD_RESULTS = {
    "/BaseInfo/GetSPRegionList": "C=100,T=7",
    "/BaseInfo/GetBusinessTradeList_GET": "C=100,T=35",
    "/BaseInfo/GetBusinessTradeList_POST": "C=100,T=230",
    "/BaseInfo/GetShopCountList_POST": "TIMEOUT",
    "/BaseInfo/GetShopCountList_GET": "HTTP405",
    "/BaseInfo/GetBrandAnalysis": "C=100(有数据)",
    "/BaseInfo/GetServerpartList": "TIMEOUT",
    "/BaseInfo/GetServerpartInfo": "HTTP404",
    "/BaseInfo/GetServerInfoTree": "HTTP404",
    "/BaseInfo/GetServerpartServiceSummary": "C=999",
    "/BaseInfo/GetBrandStructureAnalysis": "C=999",
}

print("BaseInfo 接口测试传参与响应详情")
print("=" * 100)

for i, (method, path, params, desc) in enumerate(TESTS, 1):
    # 构造旧API结果key
    if "GetBusinessTradeList" in path:
        old_key = path + "_" + method
    elif "GetShopCountList" in path:
        old_key = path + "_" + method
    else:
        old_key = path
    old_result = OLD_RESULTS.get(old_key, "?")

    print(f"\n{i:2d}. [{method}] {path}  ({desc})")
    print(f"    测试传参: {json.dumps(params, ensure_ascii=False)}")
    print(f"    旧API结果: {old_result}")

    try:
        if method == "GET":
            r = requests.get(NEW + path, params=params, timeout=10)
        else:
            r = requests.post(NEW + path, json=params, timeout=10)
        
        print(f"    新API HTTP: {r.status_code}")
        if r.status_code == 200:
            body = r.json()
            code = body.get("Result_Code")
            msg = body.get("Result_Msg", "")[:60]
            rd = body.get("Result_Data")
            if isinstance(rd, dict):
                total = rd.get("TotalCount")
                items = rd.get("Items")
                item_cnt = len(items) if isinstance(items, list) else None
                print(f"    新API响应: Code={code}, Msg={msg}")
                if total is not None:
                    print(f"               TotalCount={total}, Items数量={item_cnt}")
                else:
                    keys = list(rd.keys())[:8]
                    print(f"               Data字段: {keys}")
            else:
                print(f"    新API响应: Code={code}, Msg={msg}")
        elif r.status_code == 422:
            detail = r.json().get("detail", [])
            for d in detail[:3]:
                print(f"    422错误: 缺少参数 {d.get('loc',[])} - {d.get('msg','')}")
        elif r.status_code == 404:
            print(f"    404: 路由不存在")
    except Exception as e:
        print(f"    异常: {e}")

print("\n" + "=" * 100)
