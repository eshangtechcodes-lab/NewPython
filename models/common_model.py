# -*- coding: utf-8 -*-
"""
通用请求模型
替代原 CommonModel.cs / SearchModel<T>
"""
from typing import Any, Optional
from pydantic import BaseModel, model_validator

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

    @model_validator(mode='before')
    @classmethod
    def _case_insensitive_fields(cls, values):
        """
        模拟 C# Newtonsoft.Json 的大小写不敏感反序列化。
        前端可能传 pagesize/pageindex（全小写）或其他大小写变体，
        需要映射到正确的字段名（PageSize/PageIndex 等）。
        """
        if not isinstance(values, dict):
            return values
        # 构建已知字段名的小写→原名映射
        field_map = {}
        for field_name in cls.model_fields:
            field_map[field_name.lower()] = field_name
        # 遍历传入值，做大小写不敏感匹配
        normalized = {}
        for key, val in values.items():
            key_lower = key.lower()
            if key_lower in field_map:
                canonical = field_map[key_lower]
                # 优先保留精确匹配（如已有 PageSize 则不用 pagesize 覆盖）
                if canonical not in normalized:
                    normalized[canonical] = val
            else:
                # 未知字段原样保留
                normalized[key] = val
        return normalized
