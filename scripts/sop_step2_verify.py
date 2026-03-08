# -*- coding: utf-8 -*-
"""
SOP 步骤 2: 用真实入参调原 API 获取基准响应
SynchroSERVERPART: 用一条已有记录的 ID 做"无变化更新"验证响应格式
SolidServerpartWeather: 传一个服务区 ID 列表验证响应格式
"""
import sys, json, requests, dmPython
sys.stdout.reconfigure(encoding='utf-8')

OLD_API = "http://192.168.1.99:8900/EShangApiMain"

# 1. 先从达梦查一条已有的服务区记录
conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='192.168.1.99', port=5236)
cur = conn.cursor()
cur.execute("SELECT SERVERPART_ID, SERVERPART_NAME, SERVERPART_CODE, PROVINCE_CODE FROM T_SERVERPART WHERE ROWNUM <= 1")
row = cur.fetchone()
cols = [desc[0] for desc in cur.description]
sp_data = dict(zip(cols, row))
print(f"=== 测试服务区 ===")
print(json.dumps(sp_data, ensure_ascii=False, default=str))
conn.close()

# 2. 用这条记录调原 SynchroSERVERPART（只传 ID + NAME 做无变化更新）
print(f"\n=== 步骤 2.1: 调原 SynchroSERVERPART ===")
synchro_body = {
    "SERVERPART_ID": sp_data["SERVERPART_ID"],
    "SERVERPART_NAME": sp_data["SERVERPART_NAME"],
}
try:
    r = requests.post(
        f"{OLD_API}/BaseInfo/SynchroSERVERPART",
        json=synchro_body,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    print(f"状态码: {r.status_code}")
    print(json.dumps(r.json(), ensure_ascii=False, indent=2)[:1000])
except Exception as e:
    print(f"请求失败: {e}")

# 3. 调原 SolidServerpartWeather
print(f"\n=== 步骤 2.2: 调原 SolidServerpartWeather ===")
weather_body = [{"value": str(sp_data["SERVERPART_ID"])}]
try:
    r = requests.post(
        f"{OLD_API}/BaseInfo/SolidServerpartWeather",
        json=weather_body,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    print(f"状态码: {r.status_code}")
    print(json.dumps(r.json(), ensure_ascii=False, indent=2)[:1000])
except Exception as e:
    print(f"请求失败: {e}")
