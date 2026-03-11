# -*- coding: utf-8 -*-
"""临时调试路由 - 查询数据库表信息"""
from fastapi import APIRouter, Query
from core.database import DatabaseHelper
from routers.deps import get_db
from fastapi import Depends

router = APIRouter(tags=["Debug"])

@router.get("/Debug/QuerySQL")
async def debug_query(sql: str = Query(...), db: DatabaseHelper = Depends(get_db)):
    """临时：执行SQL查询（仅限调试）"""
    try:
        rows = db.execute_query(sql)
        return {"ok": True, "count": len(rows) if rows else 0, "data": (rows or [])[:100]}
    except Exception as e:
        return {"ok": False, "error": str(e)[:300]}
