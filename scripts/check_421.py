"""
查 SP=421 轻养社 (BP=1944) 的业务类型
"""
import requests
BASE = "http://127.0.0.1:8080/CommercialApi/Debug/QuerySQL"
def query(sql):
    r = requests.get(BASE, params={"sql": sql}, timeout=15).json()
    return r.get("data", []) if r.get("ok") else []

sql = "SELECT BUSINESSPROJECT_ID, BUSINESSPROJECT_NAME, BUSINESS_TYPE, SETTLEMENT_MODES FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID=1944"
print(query(sql))

sql2 = "SELECT DISTINCT SERVERPARTSHOP_NAME, BUSINESSTRADETYPE FROM T_BUSINESSWARNING WHERE SERVERPART_ID=421 AND BUSINESSPROJECT_ID=1944"
print(query(sql2))
