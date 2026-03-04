# -*- coding: utf-8 -*-
"""
通用请求模型
替代原 CommonModel.cs / SearchModel<T>
"""
from typing import Any, Optional
from pydantic import BaseModel


class CommonModel(BaseModel):
    """
    通用请求入参
    对应原 CommonModel（用于接收 AES 加密的 value）
    """
    label: Optional[str] = None
    value: Optional[str] = None


class KeyWord(BaseModel):
    """组合查询键值对"""
    Key: Optional[str] = None
    Value: Optional[str] = None


class SearchModel(BaseModel):
    """
    通用查询条件
    对应原 SearchModel<T>
    """
    QueryType: Optional[int] = None       # 查询方式: 0=模糊, 1=精确
    SearchParameter: Optional[dict] = None  # 查询参数（泛型 T 对应的字段）
    keyWord: Optional[KeyWord] = None     # 组合查询条件
    PageIndex: int = 1                    # 查询页码
    PageSize: int = 10                    # 每页数量
    SortStr: Optional[str] = None         # 排序条件
    ShowWholePower: Optional[bool] = None # 是否按省份显示
    Province_Code: Optional[str] = None   # 省份编码
