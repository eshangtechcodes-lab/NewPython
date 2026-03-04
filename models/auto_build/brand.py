# -*- coding: utf-8 -*-
"""
品牌表数据模型
对应原 BRANDModel.cs，保持原字段名
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class BRANDModel(BaseModel):
    """品牌表（T_BRAND）"""
    BRAND_ID: Optional[int] = None            # 内码
    BRAND_PID: Optional[int] = None           # 上级内码
    BRAND_INDEX: Optional[int] = None         # 品牌索引
    BRAND_NAME: Optional[str] = None          # 品牌名称
    BRAND_CATEGORY: Optional[int] = None      # 品牌分类（1000：经营品牌；2000：商城品牌）
    BRAND_INDUSTRY: Optional[str] = None      # 经营业态
    BRAND_TYPE: Optional[int] = None          # 品牌类型
    BRAND_INTRO: Optional[str] = None         # 品牌图标
    BRAND_STATE: Optional[int] = None         # 有效状态
    WECHATAPPSIGN_ID: Optional[int] = None    # 小程序内码
    WECHATAPPSIGN_NAME: Optional[str] = None  # 小程序名字
    WECHATAPP_APPID: Optional[str] = None     # 小程序APPID
    OWNERUNIT_ID: Optional[int] = None        # 业主内码
    OWNERUNIT_NAME: Optional[str] = None      # 业主单位
    PROVINCE_CODE: Optional[int] = None       # 省份标识
    STAFF_ID: Optional[int] = None            # 人员内码
    STAFF_NAME: Optional[str] = None          # 配置人员
    OPERATE_DATE: Optional[datetime] = None   # 配置时间
    BRAND_DESC: Optional[str] = None          # 品牌介绍
    COMMISSION_RATIO: Optional[str] = None    # 建议提成比例

    class Config:
        # 允许从 ORM / dict 创建
        from_attributes = True
