# -*- coding: utf-8 -*-
"""
达梦数据库连接管理
替代原 OracleHelper.cs
"""
import dmPython
from contextlib import contextmanager
from loguru import logger
from config import settings


class DatabaseHelper:
    """达梦数据库操作辅助类"""

    def __init__(self, host=None, port=None, user=None, password=None):
        self.host = host or settings.DM_HOST
        self.port = port or settings.DM_PORT
        self.user = user or settings.DM_USER
        self.password = password or settings.DM_PASSWORD

    def _get_connection(self):
        """获取数据库连接"""
        return dmPython.connect(
            user=self.user,
            password=self.password,
            server=self.host,
            port=self.port,
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
        替代原 ExcuteSqlGetDataSet / ExecuteDataTable
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
        替代原 ExcuteSql
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

    def execute_transaction(self, sql_list: list[str]) -> bool:
        """
        事务批量执行 SQL
        替代原 ExecuteSqlTran
        """
        with self.get_conn() as conn:
            cursor = conn.cursor()
            try:
                for sql in sql_list:
                    cursor.execute(sql)
                conn.commit()
                return True
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
            result = self.execute_scalar("SELECT 1")
            logger.info(f"达梦数据库连接成功: {self.host}:{self.port}")
            return result == 1
        except Exception as ex:
            logger.error(f"达梦数据库连接失败: {ex}")
            return False


# 全局数据库实例
db_helper = DatabaseHelper()
