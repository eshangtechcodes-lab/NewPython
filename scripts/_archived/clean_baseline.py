
import json

BASELINE_PATH = r"D:\Projects\Python\eshang_api\scripts\test_results\baseline_cache.json"

TO_DELETE = [
    "POST:/BaseInfo/GetShopCountList",
    "GET:/BaseInfo/GetShopCountList",
    "GET:/BaseInfo/RecordShopCount",
    "POST:/BaseInfo/RecordShopCount",
    "GET:/BaseInfo/RecordProvinceShopCount",
    "POST:/BaseInfo/RecordProvinceShopCount",
    "GET:/Budget/DeleteBUDGETPROJECT_AH",
    "POST:/Budget/SynchroBUDGETPROJECT_AH",
    "POST:/Analysis/SynchroANALYSISINS",
    "GET:/Analysis/verifyWXCode",
    "POST:/Analysis/respTencentMsg",
    "GET:/Analysis/GetShopRevenue"
]

def main():
    with open(BASELINE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    results = data.get("results", {})
    deleted_count = 0
    for key in TO_DELETE:
        if key in results:
            del results[key]
            deleted_count += 1
            print(f"Deleted: {key}")
        else:
            print(f"Not found in baseline: {key}")
            
    # Update meta count if possible
    if "meta" in data:
        data["meta"]["total_routes"] = len(results)
        
    with open(BASELINE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Total deleted from baseline: {deleted_count}")
    print(f"Remaining routes in baseline: {len(results)}")

if __name__ == "__main__":
    main()
