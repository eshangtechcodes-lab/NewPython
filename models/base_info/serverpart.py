from __future__ import annotations
# -*- coding: utf-8 -*-
"""
服务区站点数据模型
对应原 SERVERPARTModel.cs
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class SERVERPARTModel(BaseModel):
    """
    服务区站点数据模型
    对应 T_SERVERPART 表 42 个字段
    """
    SERVERPART_ID: Optional[int] = None             # 内码
    SERVERPART_NAME: Optional[str] = None           # 服务区名称
    SERVERPART_ADDRESS: Optional[str] = None        # 服务区地址
    SERVERPART_INDEX: Optional[int] = None          # 服务区索引
    EXPRESSWAY_NAME: Optional[str] = None           # 所在高速路
    SELLERCOUNT: Optional[int] = None               # 商家服务数
    SERVERPART_AREA: Optional[float] = None         # 服务区面积
    SERVERPART_X: Optional[float] = None            # 坐标X
    SERVERPART_Y: Optional[float] = None            # 坐标Y
    SERVERPART_TEL: Optional[str] = None            # 电话号码
    SERVERPART_INFO: Optional[str] = None           # 服务区说明
    PROVINCE_CODE: Optional[int] = None             # 省份编码
    CITY_CODE: Optional[int] = None                 # 城市编码
    COUNTY_CODE: Optional[int] = None               # 区县编码
    SERVERPART_CODE: Optional[str] = None           # 服务区编码
    FIELDENUM_ID: Optional[int] = None              # 枚举内码
    SERVERPART_IPADDRESS: Optional[str] = None      # IP地址描述
    SERVERPART_TYPE: Optional[int] = None           # 服务区类型
    DAYINCAR: Optional[float] = None                # 日均入区车辆
    HKBL: Optional[str] = None                      # 入区车辆客货比例
    STARTDATE: Optional[datetime] = None            # 开业时间
    OWNEDCOMPANY: Optional[str] = None              # 所属公司
    FLOORAREA: Optional[float] = None               # 占地面积
    BUSINESSAREA: Optional[float] = None            # 经营面积
    SHAREAREA: Optional[float] = None               # 公共区域面积
    TOTALPARKING: Optional[int] = None              # 车位数
    MANAGERCOMPANY: Optional[str] = None            # 管理公司
    SHORTNAME: Optional[str] = None                 # 服务区简称
    REGIONTYPE_ID: Optional[int] = None             # 附属管辖内码
    STATISTIC_TYPE: Optional[int] = None            # 统计类型(1000:正式;2000:测试;3000:替代)
    PROVINCE_NAME: Optional[str] = None             # 省份名称
    SPREGIONTYPE_ID: Optional[int] = None           # 归属区域内码
    SPREGIONTYPE_NAME: Optional[str] = None         # 归属区域名字
    SPREGIONTYPE_INDEX: Optional[int] = None        # 归属区域索引
    REGIONTYPE_NAME: Optional[str] = None           # 附属管辖名称
    STATISTICS_TYPE: Optional[str] = None           # 站点类型(服务区、加油站、单位部门)
    STAFF_ID: Optional[int] = None                  # 操作员内码
    STAFF_NAME: Optional[str] = None                # 操作人员
    OPERATE_DATE: Optional[datetime] = None         # 操作时间
    SERVERPART_DESC: Optional[str] = None           # 备注说明
    OWNERUNIT_ID: Optional[int] = None              # 业主单位内码
    OWNERUNIT_NAME: Optional[str] = None            # 业主单位名称
