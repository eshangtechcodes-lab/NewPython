"""最终全面验证 - 多 SP 对比"""
import requests, json

OLD = "http://192.168.1.99:8900/CommercialApi/Revenue/GetShopSABFIList"
NEW = "http://127.0.0.1:8080/CommercialApi/Revenue/GetShopSABFIList"

def get_shops(data):
    shops = {}
    for region in (data.get("Result_Data", {}).get("List", [{}])[0].get("children") or []):
        for sp in (region.get("children") or []):
            for shop in (sp["node"].get("ShopSABFIList") or []):
                shops[shop["ServerpartShopName"]] = shop
    return shops

test_sps = ["378","416","417","419","420","435","433","421"]
total_common = 0
total_perfect = 0
total_diff = 0

for sp_id in test_sps:
    params = {"pushProvinceCode": "340000", "StatisticsMonth": "202602",
              "ServerpartId": sp_id, "BusinessTradeType": "", "BusinessTrade": ""}
    try:
        r_old = requests.get(OLD, params=params, timeout=30)
        r_new = requests.get(NEW, params=params, timeout=30)
        olds, news = get_shops(r_old.json()), get_shops(r_new.json())
        common = set(olds) & set(news)
        perfect = 0
        diffs_list = []
        for name in sorted(common):
            o, n = olds[name], news[name]
            diffs = [k for k in sorted(o.keys()) if o.get(k) != n.get(k)]
            if diffs:
                diffs_list.append(f"    ❌ {name}: {diffs}")
            else:
                perfect += 1
        
        total_common += len(common)
        total_perfect += perfect
        total_diff += len(diffs_list)
        
        status = "✅" if not diffs_list else "⚠️"
        print(f"{status} SP={sp_id}: {len(common)}门店, {perfect}一致, {len(diffs_list)}差异")
        for d in diffs_list:
            print(d)
    except Exception as e:
        print(f"❌ SP={sp_id}: {e}")

print(f"\n{'='*50}")
print(f"总计: {total_common}门店, {total_perfect}一致, {total_diff}差异")
print(f"一致率: {total_perfect/total_common*100:.1f}%")
