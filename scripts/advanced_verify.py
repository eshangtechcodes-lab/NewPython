"""
修正后的验证脚本：使用 (门店名, 项目ID) 作为唯一键，避免同名门店覆盖
"""
import requests, json

OLD = "http://192.168.1.99:8900/CommercialApi/Revenue/GetShopSABFIList"
NEW = "http://127.0.0.1:8080/CommercialApi/Revenue/GetShopSABFIList"

def get_shops_advanced(data):
    shops = {}
    for region in (data.get("Result_Data", {}).get("List", [{}])[0].get("children") or []):
        for sp in (region.get("children") or []):
            for shop in (sp["node"].get("ShopSABFIList") or []):
                # 使用 (门店名, 项目ID) 作为唯一键
                key = (shop["ServerpartShopName"], shop.get("BusinessProjectId"))
                shops[key] = shop
    return shops

test_sps = ["378","416","417","419","420","435","433","421"]
all_results = []

for sp_id in test_sps:
    params = {"pushProvinceCode": "340000", "StatisticsMonth": "202602",
              "ServerpartId": sp_id, "BusinessTradeType": "", "BusinessTrade": ""}
    try:
        r_old = requests.get(OLD, params=params, timeout=30)
        r_new = requests.get(NEW, params=params, timeout=30)
        
        olds = get_shops_advanced(r_old.json())
        news = get_shops_advanced(r_new.json())
        
        common_keys = set(olds.keys()) & set(news.keys())
        diffs_in_sp = []
        
        for key in sorted(common_keys):
            o, n = olds[key], news[key]
            # 基础字段对比
            mismatches = [k for k in o.keys() if k in n and o[k] != n[k]]
            if mismatches:
                diffs_in_sp.append({"name": key[0], "bp": key[1], "diffs": mismatches, "old": o, "new": n})
        
        all_results.append({
            "sp_id": sp_id,
            "total": len(news),
            "consistent": len(news) - len(diffs_in_sp),
            "diffs": diffs_in_sp
        })
    except Exception as e:
        print(f"Error checking SP {sp_id}: {e}")

# 输出审计结果
print("\n" + "="*60)
total_shops = 0
total_consistent = 0
for res in all_results:
    total_shops += res["total"]
    total_consistent += res["consistent"]
    status = "✅" if res["total"] == res["consistent"] else "⚠️"
    print(f"{status} SP={res['sp_id']}: {res['total']}门店, {res['consistent']}一致, {len(res['diffs'])}差异")
    for d in res["diffs"]:
        print(f"  ❌ {d['name']} (BP={d['bp']}): {d['diffs']}")
        # 详细打印差异
        for f in d['diffs']:
            if isinstance(d['old'][f], dict):
                print(f"    - {f}: 旧={json.dumps(d['old'][f], ensure_ascii=False)} 新={json.dumps(d['new'][f], ensure_ascii=False)}")
            else:
                print(f"    - {f}: 旧={d['old'][f]} 新={d['new'][f]}")

print("="*60)
print(f"最终统计: {total_shops}门店, {total_consistent}一致")
print(f"一致率: {total_consistent/total_shops*100:.2f}%")
