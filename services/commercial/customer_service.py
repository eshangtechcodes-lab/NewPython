# -*- coding: utf-8 -*-
from __future__ import annotations
# -*- coding: utf-8 -*-
"""
CommercialApi - 客群分析业务服务
从 customer_router.py 中抽取的 SQL 和业务逻辑
"""
from typing import Optional
from core.database import DatabaseHelper


def get_customer_ratio(db: DatabaseHelper, serverpart_id: Optional[int],
                       statistics_month: Optional[str]) -> list[dict]:
    """获取客群分析占比（男/女/年龄层次）"""
    conditions, params = [], {}
    if serverpart_id:
        conditions.append("SERVERPART_ID = :serverpartId")
        params["serverpartId"] = serverpart_id
    if statistics_month:
        conditions.append("STATISTICS_MONTH = :statisticsMonth")
        params["statisticsMonth"] = statistics_month
    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""

    sql = f"SELECT COUNT_MALE, COUNT_FEMALE, COUNT_00, COUNT_90, COUNT_80, COUNT_70 FROM T_CUSTOMERGROUP{where_sql}"
    data = db.execute_query(sql, params)

    if not data:
        return []
    row = data[0]
    return [
        {"name": "男性", "data": [float(row["COUNT_MALE"])]},
        {"name": "女性", "data": [float(row["COUNT_FEMALE"])]},
        {"name": "年龄", "data": [
            float(row["COUNT_00"]), float(row["COUNT_90"]),
            float(row["COUNT_80"]), float(row["COUNT_70"])
        ]},
    ]


def get_customer_consume_ratio(db: DatabaseHelper, serverpart_id: Optional[int],
                               statistics_month: Optional[str]) -> list[dict]:
    """获取客群消费能力占比"""
    conditions, params = [], {}
    if serverpart_id:
        conditions.append("SERVERPART_ID = :serverpartId")
        params["serverpartId"] = serverpart_id
    if statistics_month:
        conditions.append("STATISTICS_MONTH = :statisticsMonth")
        params["statisticsMonth"] = statistics_month
    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""

    sql = f"SELECT COUNT_MALE_30, COUNT_MALE_60, COUNT_MALE_90, COUNT_MALE_90U, COUNT_FEMALE_30, COUNT_FEMALE_60, COUNT_FEMALE_90, COUNT_FEMALE_90U FROM T_CUSTOMER_CONSUME{where_sql}"
    data = db.execute_query(sql, params)

    if not data:
        return []
    row = data[0]
    return [
        {"name": "男性", "data": [
            float(row["COUNT_MALE_30"]), float(row["COUNT_MALE_60"]),
            float(row["COUNT_MALE_90"]), float(row["COUNT_MALE_90U"])
        ]},
        {"name": "女性", "data": [
            float(row["COUNT_FEMALE_30"]), float(row["COUNT_FEMALE_60"]),
            float(row["COUNT_FEMALE_90"]), float(row["COUNT_FEMALE_90U"])
        ]},
    ]


def get_customer_age_ratio(db: DatabaseHelper, serverpart_id: Optional[int],
                           statistics_month: Optional[str]) -> list[dict]:
    """获取客群年龄层次占比"""
    conditions, params = [], {}
    if serverpart_id:
        conditions.append("SERVERPART_ID = :serverpartId")
        params["serverpartId"] = serverpart_id
    if statistics_month:
        conditions.append("STATISTICS_MONTH = :statisticsMonth")
        params["statisticsMonth"] = statistics_month
    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""

    sql = f"SELECT COUNT_MALE_00, COUNT_MALE_90, COUNT_MALE_80, COUNT_MALE_70, COUNT_FEMALE_00, COUNT_FEMALE_90, COUNT_FEMALE_80, COUNT_FEMALE_70 FROM T_CUSTOMER_AGE{where_sql}"
    data = db.execute_query(sql, params)

    if not data:
        return []
    row = data[0]
    return [
        {"name": "男性", "data": [
            float(row["COUNT_MALE_00"]), float(row["COUNT_MALE_90"]),
            float(row["COUNT_MALE_80"]), float(row["COUNT_MALE_70"])
        ]},
        {"name": "女性", "data": [
            float(row["COUNT_FEMALE_00"]), float(row["COUNT_FEMALE_90"]),
            float(row["COUNT_FEMALE_80"]), float(row["COUNT_FEMALE_70"])
        ]},
    ]


def get_customer_group_ratio(db: DatabaseHelper, serverpart_id: Optional[int],
                             statistics_month: Optional[str]) -> list[dict]:
    """获取客群特征分析（散点图数据）"""
    conditions, params = [], {}
    if serverpart_id:
        conditions.append("SERVERPART_ID = :serverpartId")
        params["serverpartId"] = serverpart_id
    if statistics_month:
        conditions.append("STATISTICS_MONTH = :statisticsMonth")
        params["statisticsMonth"] = statistics_month
    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""

    sql = f"SELECT * FROM T_CUSTOMER_GAC{where_sql}"
    data = db.execute_query(sql, params)

    if not data:
        return []
    row = data[0]
    male_data = [[25, 50, float(row[col])] for col in row.keys() if "MALE" in col]
    female_data = [[25, 50, float(row[col])] for col in row.keys() if "FEMALE" in col]
    return [
        {"name": "男性", "data": male_data},
        {"name": "女性", "data": female_data},
    ]


def get_analysis_desc_list(db: DatabaseHelper, serverpart_id: Optional[int],
                           serverpart_code: Optional[str],
                           statistics_month: Optional[str],
                           statistics_type: Optional[int]) -> list[dict]:
    """获取客群分析说明表列表"""
    where_parts, params = [], {}
    if serverpart_id:
        where_parts.append("SERVERPART_ID = :serverpartId")
        params["serverpartId"] = serverpart_id
    elif serverpart_code:
        where_parts.append("SERVERPART_CODE = :serverpartCode")
        params["serverpartCode"] = serverpart_code
    else:
        where_parts.append("1 = 2")
    if statistics_type:
        where_parts.append("STATISTICS_TYPE = :statisticsType")
        params["statisticsType"] = statistics_type
    if statistics_month:
        where_parts.append("STATISTICS_MONTH = :statisticsMonth")
        params["statisticsMonth"] = statistics_month

    where_sql = " AND ".join(where_parts)
    sql = f"SELECT STATISTICS_TYPE, SERVERPART_NAME, ANALYSIS_CONTENT, KEY_CONTENT FROM T_CUSTOMER_ANALYSIS WHERE {where_sql} ORDER BY STATISTICS_TYPE"
    data_list = db.execute_query(sql, params)

    return [
        {
            "Statistics_Type": row["STATISTICS_TYPE"],
            "Serverpart_Name": row["SERVERPART_NAME"],
            "Analysis_Content": row["ANALYSIS_CONTENT"],
            "Key_Content": row["KEY_CONTENT"],
        }
        for row in data_list
    ]


def get_analysis_desc_detail(db: DatabaseHelper, serverpart_id: Optional[int],
                             serverpart_code: Optional[str],
                             province_code: Optional[str],
                             statistics_month: Optional[str],
                             statistics_type: Optional[int]) -> Optional[dict]:
    """获取客群分析说明表明细"""
    where_parts, params = [], {"statisticsType": statistics_type}
    if serverpart_id:
        where_parts.append("SERVERPART_ID = :serverpartId")
        params["serverpartId"] = serverpart_id
    elif serverpart_code:
        where_parts.append("SERVERPART_CODE = :serverpartCode")
        params["serverpartCode"] = serverpart_code
    elif province_code:
        where_parts.append("SERVERPART_CODE = :provinceCode")
        params["provinceCode"] = province_code
    else:
        where_parts.append("1 = 2")
    if statistics_month:
        where_parts.append("STATISTICS_MONTH = :statisticsMonth")
        params["statisticsMonth"] = statistics_month

    where_sql = " AND ".join(where_parts)
    sql = f"SELECT STATISTICS_TYPE, SERVERPART_NAME, ANALYSIS_CONTENT, KEY_CONTENT FROM T_CUSTOMER_ANALYSIS WHERE STATISTICS_TYPE = :statisticsType AND {where_sql}"
    data_list = db.execute_query(sql, params)

    if not data_list:
        return None
    row = data_list[0]
    return {
        "Statistics_Type": row["STATISTICS_TYPE"],
        "Serverpart_Name": row["SERVERPART_NAME"],
        "Analysis_Content": row["ANALYSIS_CONTENT"],
        "Key_Content": row["KEY_CONTENT"],
    }
