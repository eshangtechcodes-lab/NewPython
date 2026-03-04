# -*- coding: utf-8 -*-
"""
业主单位管理表数据模型
对应原 OWNERUNITModel.cs
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class OWNERUNITModel(BaseModel):
    """
    业主单位管理表数据模型
    对应 T_OWNERUNIT 表 18 个字段
    """
    OWNERUNIT_ID: Optional[int] = None          # 业主内码
    OWNERUNIT_PID: Optional[int] = None         # 父级内码
    PROVINCE_CODE: Optional[int] = None         # 省份标识
    PROVINCE_BUSINESSCODE: Optional[int] = None # 业务省份标识
    OWNERUNIT_NAME: Optional[str] = None        # 业主单位
    OWNERUNIT_EN: Optional[str] = None          # 业主简称
    OWNERUNIT_NATURE: Optional[int] = None      # 业主单位性质(1000:管理单位;2000:经营单位)
    OWNERUNIT_GUID: Optional[str] = None        # 业主标识
    OWNERUNIT_INDEX: Optional[int] = None       # 排序字段
    OWNERUNIT_ICO: Optional[str] = None         # 业主图标
    OWNERUNIT_STATE: Optional[int] = None       # 有效状态
    STAFF_ID: Optional[int] = None              # 操作人员内码
    STAFF_NAME: Optional[str] = None            # 操作人员名称
    OPERATE_DATE: Optional[datetime] = None     # 操作时间
    OWNERUNIT_DESC: Optional[str] = None        # 备注
    ISSUPPORTPOINT: Optional[int] = None        # 是否支持积分功能
    DOWNLOAD_DATE: Optional[datetime] = None    # 下载时间
    WECHATPUBLICSIGN_ID: Optional[int] = None   # 公众号ID
