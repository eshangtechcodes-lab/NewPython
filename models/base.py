# -*- coding: utf-8 -*-
"""
基础响应模型
保持原有字段命名：Result_Code / Result_Desc / Result_Data
替代原 Result.cs / JsonMsg.cs / JsonList.cs
"""
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Result(BaseModel):
    """
    统一响应模型
    对应原 Result.cs 和 JsonMsg<T>
    状态码: 100=成功, 200=业务失败, 999=异常
    """
    Result_Code: int = 100
    Result_Desc: str = "Success"
    Result_Data: Any = None

    @staticmethod
    def success(data: Any = None, code: int = 100, msg: str = "成功") -> "Result":
        return Result(Result_Code=code, Result_Desc=msg, Result_Data=data)

    @staticmethod
    def fail(code: int = 999, msg: str = "失败") -> "Result":
        return Result(Result_Code=code, Result_Desc=msg, Result_Data=None)


class JsonListData(BaseModel):
    """
    分页列表响应数据
    对应原 JsonList<T> 和 JsonList<T1,T2>
    OtherData仅在有值时输出（对应JsonList<T1,T2>的OtherData字段）
    """
    PageIndex: int = 1
    PageSize: int = 0
    TotalCount: int = 0
    List: list = []
    OtherData: Any = None

    def model_dump(self, **kwargs):
        """C#对齐：OtherData为None时不输出该字段"""
        d = super().model_dump(**kwargs)
        if d.get("OtherData") is None:
            d.pop("OtherData", None)
        return d

    @staticmethod
    def create(data_list: list, total: int = None, page_index: int = 1, page_size: int = None,
               other_data=None) -> "JsonListData":
        if total is None:
            total = len(data_list)
        if page_size is None:
            page_size = total
        return JsonListData(
            List=data_list,
            TotalCount=total,
            PageIndex=page_index,
            PageSize=page_size,
            OtherData=other_data
        )
