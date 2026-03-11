"""通过 HTTP API 验证散装接口修复效果"""
import requests, json

OLD = "http://192.168.1.99:8900/EShangApiMain/Analysis"
NEW = "http://localhost:8080/EShangApiMain/Analysis"
H = {"ProvinceCode": "340000"}

apis = [
    ("GetPeriodMonthlyList", {"StatisticsMonth": "202501", "ServerpartId": "416"}),
    ("GetRevenueEstimateList", {"StatisticsMonth": "202501", "ServerpartId": "416"}),
    ("GetShopSABFIList", {"ServerpartId": "416", "StatisticsMonth": "202501", "calcSelf": "true"}),
]

for name, params in apis:
    print(f"\n=== {name} ===")
    try:
        r1 = requests.get(f"{OLD}/{name}", params=params, headers=H, timeout=15)
        r2 = requests.get(f"{NEW}/{name}", params=params, headers=H, timeout=15)
        d1, d2 = r1.json(), r2.json()
        rd1 = d1.get("Result_Data", {})
        rd2 = d2.get("Result_Data", {})
        l1 = rd1.get("List", []) if isinstance(rd1, dict) else []
        l2 = rd2.get("List", []) if isinstance(rd2, dict) else []
        print(f"  OLD: code={d1.get('Result_Code')}, List len={len(l1)}")
        desc2 = str(d2.get("Result_Desc", ""))[:200]
        print(f"  NEW: code={d2.get('Result_Code')}, desc={desc2}, List len={len(l2)}")
        if l1 and l2:
            n1 = l1[0]
            n2 = l2[0]
            if isinstance(n1, dict) and "node" in n1 and isinstance(n2, dict) and "node" in n2:
                ch1 = n1.get("children") or []
                ch2 = n2.get("children") or []
                nf1, nf2 = len(n1.get("node",{}).keys()), len(n2.get("node",{}).keys())
                print(f"  OLD[0]: node({nf1}), children({len(ch1)})")
                print(f"  NEW[0]: node({nf2}), children({len(ch2)})")
                if ch1 and ch2:
                    cn1, cn2 = ch1[0], ch2[0]
                    if isinstance(cn1, dict) and "node" in cn1:
                        cf1 = len(cn1.get("node",{}).keys())
                        cf2 = len(cn2.get("node",{}).keys()) if isinstance(cn2, dict) and "node" in cn2 else 0
                        cc1 = len(cn1.get("children") or [])
                        cc2 = len(cn2.get("children") or []) if isinstance(cn2, dict) else 0
                        print(f"  OLD child[0]: node({cf1}), children({cc1})")
                        print(f"  NEW child[0]: node({cf2}), children({cc2})")
    except Exception as e:
        print(f"  ERROR: {e}")
