# -*- coding: utf-8 -*-
"""
数据库连接管理
支持 Oracle（oracledb Thick 模式）和 达梦（dmPython）双数据源
"""
import os
from contextlib import contextmanager
from loguru import logger
from config import settings

# Oracle Instant Client 路径
ORACLE_CLIENT_PATH = r"C:\Users\YSKJ02\instantclient_21_3"

# 模块加载时初始化 Oracle Thick 模式
try:
    import oracledb
    oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)
    logger.info(f"Oracle Thick 模式初始化成功: {ORACLE_CLIENT_PATH}")
except Exception as ex:
    logger.warning(f"Oracle Thick 模式初始化跳过: {ex}")


class DatabaseHelper:
    """通用数据库操作辅助类，支持 Oracle 和达梦"""

    def __init__(self, db_type="oracle"):
        """
        db_type: "oracle" 或 "dm"
        """
        self.db_type = db_type

    def _get_connection(self):
        """获取数据库连接"""
        if self.db_type == "oracle":
            import oracledb
            return oracledb.connect(
                user=settings.ORA_USER,
                password=settings.ORA_PASSWORD,
                dsn=settings.ORA_DSN,
            )
        else:
            import dmPython
            return dmPython.connect(
                user=settings.DM_USER,
                password=settings.DM_PASSWORD,
                server=settings.DM_HOST,
                port=settings.DM_PORT,
            )

    @contextmanager
    def get_conn(self):
        """上下文管理器：自动管理连接生命周期"""
        conn = self._get_connection()
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(self, sql: str, params: dict = None) -> list[dict]:
        """
        执行 SQL 查询，返回字典列表
        """
        with self.get_conn() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows]
            finally:
                cursor.close()

    def execute_non_query(self, sql: str, params: dict = None) -> int:
        """
        执行 SQL（INSERT/UPDATE/DELETE），返回受影响行数
        """
        with self.get_conn() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                conn.commit()
                return cursor.rowcount
            except Exception:
                conn.rollback()
                raise
            finally:
                cursor.close()

    def execute_scalar(self, sql: str, params: dict = None):
        """执行 SQL，返回单个值"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                row = cursor.fetchone()
                return row[0] if row else None
            finally:
                cursor.close()

    def test_connection(self) -> bool:
        """测试数据库连通性"""
        try:
            test_sql = "SELECT 1 FROM DUAL" if self.db_type == "oracle" else "SELECT 1"
            result = self.execute_scalar(test_sql)
            db_name = "Oracle" if self.db_type == "oracle" else "达梦"
            logger.info(f"{db_name}数据库连接成功")
            return result == 1
        except Exception as ex:
            logger.error(f"数据库连接失败: {ex}")
            return False


# 全局数据库实例——使用达梦连接
db_helper = DatabaseHelper(db_type="dm")
