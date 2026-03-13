"""测试散装接口的 C# 端和 Python 端响应对比"""
import requests

apis = [
    ("GetInvestmentReport", {"ContainHoliday": 0, "ServerpartId": "416"}),
    ("GetNestingIAReport", {"ContainHoliday": 0, "ServerpartId": "416"}),
    ("GetPeriodMonthlyList", {"StatisticsMonth": "202501", "ServerpartId": "416"}),
    ("GetRevenueEstimateList", {"StatisticsMonth": "202501", "ServerpartId": "416"}),
    ("GetShopSABFIList", {"ServerpartId": "416", "StatisticsMonth": "202501", "calcSelf": "true"}),
]
headers = {"ProvinceCode": "340000"}
for name, params in apis:
    try:
        r1 = requests.get(
            f"http://192.168.1.99:8900/EShangApiMain/Analysis/{name}",
            params=params, headers=headers, timeout=15
        )
        r2 = requests.get(
            f"http://localhost:8080/EShangApiMain/Analysis/{name}",
            params=params, headers=headers, timeout=15
        )
        d1, d2 = r1.json(), r2.json()
        rd1 = d1.get("Result_Data")
        rd2 = d2.get("Result_Data")
        l1 = len(rd1) if isinstance(rd1, list) else ("dict" if isinstance(rd1, dict) else str(type(rd1).__name__))
        l2 = len(rd2) if isinstance(rd2, list) else ("dict" if isinstance(rd2, dict) else str(type(rd2).__name__))
        c1 = d1.get("Result_Code")
        c2 = d2.get("Result_Code")
        print(f"{name}: OLD code={c1} data={l1} | NEW code={c2} data={l2}")
    except Exception as e:
        print(f"{name}: ERROR {e}")
