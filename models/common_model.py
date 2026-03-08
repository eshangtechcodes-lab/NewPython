# -*- coding: utf-8 -*-
"""
通用请求模型
替代原 CommonModel.cs / SearchModel<T>
"""
from typing import Any, Optional
from pydantic import BaseModel

# 全局排除字段：前端分页/UI 参数，非数据库字段
# 原 C# 使用强类型 Model 反序列化时会自动忽略这些字段
# Python 用 dict 接收 SearchParameter 不会过滤，需手动排除
SEARCH_PARAM_SKIP_FIELDS = {
    "current", "pageSize", "total", "size",  # 前端分页参数
    "sorter", "filter", "order",              # 前端排序/筛选参数
}


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
    PageIndex: int = 0                    # 查询页码（0=不分页）
    PageSize: int = 0                     # 每页数量（0=不分页）
    SortStr: Optional[str] = None         # 排序条件
    ShowWholePower: Optional[bool] = None # 是否按省份显示
    Province_Code: Optional[str] = None   # 省份编码
