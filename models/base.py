# -*- coding: utf-8 -*-
"""
基础响应模型
成功时: {Result_Code, Result_Desc, Result_Data}
失败时: {Result_Code, Result_Desc, Result_Data, Message}
"""
from typing import Any, Optional
from pydantic import BaseModel


class Result:
    """
    统一响应工具类
    success/fail 返回 dict，FastAPI 直接序列化
    支持 Result(Result_Code=200, Result_Desc="xxx") 构造调用
    """
    def __new__(cls, Result_Code: int = 999, Result_Desc: str = "失败", Result_Data: Any = None, **kwargs):
        """兼容 Result(Result_Code=200, Result_Desc="xxx") 构造方式"""
        return {"Result_Code": Result_Code, "Result_Desc": Result_Desc, "Result_Data": Result_Data}

    @staticmethod
    def success(data: Any = None, code: int = 100, msg: str = "成功") -> dict:
        return {"Result_Code": code, "Result_Desc": msg, "Result_Data": data}

    @staticmethod
    def fail(code: int = 999, msg: str = "失败") -> dict:
        return {"Result_Code": code, "Result_Desc": msg, "Result_Data": None}


class JsonListData(BaseModel):
    """
    分页列表响应数据
    对应原 JsonList<T>
    """
    PageIndex: int = 1
    PageSize: int = 10
    TotalCount: int = 0
    List: list = []
    StaticsModel: Optional[dict] = None

    def model_dump(self, **kwargs):
        """重写 model_dump：默认排除 None 字段（StaticsModel=None 时不输出）"""
        kwargs.setdefault('exclude_none', True)
        return super().model_dump(**kwargs)

    def to_dict(self) -> dict:
        """转为 dict，排除 None 字段（StaticsModel=None 时不输出）"""
        d = {"PageIndex": self.PageIndex, "PageSize": self.PageSize,
             "TotalCount": self.TotalCount, "List": self.List}
        if self.StaticsModel is not None:
            d["StaticsModel"] = self.StaticsModel
        return d

    @staticmethod
    def create(data_list: list, total: int, page_index: int = 1, page_size: int = 10,
               statics_model: dict = None) -> "JsonListData":
        return JsonListData(
            List=data_list,
            TotalCount=total,
            PageIndex=page_index,
            PageSize=page_size,
            StaticsModel=statics_model
        )
