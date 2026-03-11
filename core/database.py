# -*- coding: utf-8 -*-
from __future__ import annotations
"""
数据库连接管理
支持 Oracle（oracledb Thick 模式）和 达梦（dmPython）双数据源

PKG-TIMEOUT-INFRA-01 整改:
- 增加连接池 (pool_size=5, max_overflow=10)
- SQL 执行超时控制 (默认 30s)
- 慢查询日志 (>5s 记录 WARNING)
- 每次查询记录执行时间
"""
import os
import time
import threading
from contextlib import contextmanager
from loguru import logger
from config import settings

# ============================================================
# Oracle Instant Client 初始化
# ============================================================
ORACLE_CLIENT_PATH = r"C:\Users\YSKJ02\instantclient_21_3"

try:
    import oracledb
    oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)
    logger.info(f"Oracle Thick 模式初始化成功: {ORACLE_CLIENT_PATH}")
except Exception as ex:
    logger.warning(f"Oracle Thick 模式初始化跳过: {ex}")


# ============================================================
# 达梦连接池实现（dmPython 原生不提供连接池，手动实现简单池）
# ============================================================
class SimpleConnectionPool:
    """
    简单连接池：维护一组复用连接，避免每次请求都新建
    适用于 dmPython 等不自带连接池的驱动
    """

    def __init__(self, creator_func, pool_size=5, max_overflow=10):
        self._creator = creator_func
        self._pool_size = pool_size
        self._max_overflow = max_overflow
        self._pool = []           # 空闲连接
        self._in_use = 0          # 正在使用的连接数
        self._lock = threading.Lock()
        # 预创建连接
        for _ in range(min(2, pool_size)):
            try:
                conn = self._creator()
                self._pool.append(conn)
            except Exception as ex:
                logger.warning(f"连接池预创建连接失败: {ex}")

    def get_connection(self):
        """从池中获取连接"""
        with self._lock:
            # 优先从空闲池取
            while self._pool:
                conn = self._pool.pop()
                try:
                    # 测试连接是否仍然有效
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1")
                    cursor.close()
                    self._in_use += 1
                    return conn
                except Exception:
                    # 连接已失效，丢弃
                    try:
                        conn.close()
                    except Exception:
                        pass

            # 池空了，检查是否可以新建
            total = self._in_use + len(self._pool)
            if total < self._pool_size + self._max_overflow:
                conn = self._creator()
                self._in_use += 1
                return conn
            else:
                # 超出上限，仍然新建但记录警告
                logger.warning(f"连接池已满 (in_use={self._in_use}, pool={len(self._pool)}), 强制新建")
                conn = self._creator()
                self._in_use += 1
                return conn

    def return_connection(self, conn):
        """归还连接到池中"""
        with self._lock:
            self._in_use = max(0, self._in_use - 1)
            if len(self._pool) < self._pool_size:
                self._pool.append(conn)
            else:
                # 池满了，关闭多余连接
                try:
                    conn.close()
                except Exception:
                    pass

    def discard_connection(self, conn):
        """丢弃一个有问题的连接"""
        with self._lock:
            self._in_use = max(0, self._in_use - 1)
        try:
            conn.close()
        except Exception:
            pass

    @property
    def status(self):
        return f"pool={len(self._pool)}, in_use={self._in_use}"


# ============================================================
# 慢查询阈值和超时配置
# ============================================================
SLOW_QUERY_THRESHOLD = 5.0    # 秒，超过此值记录 WARNING
DEFAULT_QUERY_TIMEOUT = 30    # 秒，SQL 执行超时


class DatabaseHelper:
    """
    通用数据库操作辅助类，支持 Oracle 和达梦
    PKG-TIMEOUT-INFRA-01: 增加连接池 + 慢查询日志 + 超时控制
    """

    def __init__(self, db_type="oracle"):
        """
        db_type: "oracle" 或 "dm"
        """
        self.db_type = db_type
        self._pool = None
        self._init_pool()

    def _create_dm_connection(self):
        """创建达梦连接"""
        import dmPython
        return dmPython.connect(
            user=settings.DM_USER,
            password=settings.DM_PASSWORD,
            server=settings.DM_HOST,
            port=settings.DM_PORT,
        )

    def _create_oracle_connection(self):
        """创建 Oracle 连接"""
        import oracledb
        return oracledb.connect(
            user=settings.ORA_USER,
            password=settings.ORA_PASSWORD,
            dsn=settings.ORA_DSN,
        )

    def _init_pool(self):
        """初始化连接池"""
        try:
            if self.db_type == "dm":
                self._pool = SimpleConnectionPool(
                    self._create_dm_connection,
                    pool_size=5,
                    max_overflow=10
                )
                logger.info(f"达梦连接池初始化成功 (pool_size=5, max_overflow=10)")
            else:
                # Oracle 使用 oracledb 自带的连接池（如果可用）
                self._pool = SimpleConnectionPool(
                    self._create_oracle_connection,
                    pool_size=3,
                    max_overflow=5
                )
                logger.info(f"Oracle 连接池初始化成功 (pool_size=3, max_overflow=5)")
        except Exception as ex:
            logger.warning(f"连接池初始化失败, 将使用逐次创建模式: {ex}")
            self._pool = None

    def _get_connection(self):
        """获取数据库连接（优先从池获取）"""
        if self._pool:
            return self._pool.get_connection()
        # 降级到直接创建
        if self.db_type == "oracle":
            return self._create_oracle_connection()
        else:
            return self._create_dm_connection()

    def _return_connection(self, conn, error=False):
        """归还连接到池（出错则丢弃）"""
        if self._pool:
            if error:
                self._pool.discard_connection(conn)
            else:
                self._pool.return_connection(conn)
        else:
            try:
                conn.close()
            except Exception:
                pass

    @contextmanager
    def get_conn(self):
        """上下文管理器：自动管理连接生命周期"""
        conn = self._get_connection()
        error = False
        try:
            yield conn
        except Exception:
            error = True
            raise
        finally:
            self._return_connection(conn, error=error)

    def execute_query(self, sql: str, params: dict = None, timeout: int = DEFAULT_QUERY_TIMEOUT, null_to_empty: bool = True) -> list[dict]:
        """
        执行 SQL 查询，返回字典列表
        PKG-TIMEOUT-INFRA-01: 增加执行时间日志 + 慢查询告警
        """
        start = time.time()
        conn = self._get_connection()
        error_occurred = False
        try:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = cursor.fetchall()
                result = [dict(zip(columns, row)) for row in rows]

                # 全局类型对齐：
                # 1. Decimal/float → int（当值为整数时）
                # 2. datetime → ISO 格式字符串（C# DateTime.ToString() 带 T 分隔符）
                # 3. 字符串列 NULL → ''（C# ToString() 对 DBNull 返回 ""）
                from decimal import Decimal
                from datetime import datetime as _dt, date as _date

                # 通过 cursor.description 推断字符串列
                # 策略: 先尝试 type_code 精确匹配，回退到采样法
                str_columns = set()
                if cursor.description:
                    # dmPython 字符串相关类型常量
                    _str_type_codes = set()
                    try:
                        import dmPython
                        # STRING 覆盖 CHAR/VARCHAR 等
                        _str_type_codes.add(dmPython.STRING)
                        # CLOB 也是字符串类型
                        if hasattr(dmPython, 'CLOB'):
                            _str_type_codes.add(dmPython.CLOB)
                    except ImportError:
                        pass

                    for desc in cursor.description:
                        col_name = desc[0]
                        type_code = desc[1]
                        # type_code 精确匹配字符串类型
                        if _str_type_codes and type_code in _str_type_codes:
                            str_columns.add(col_name)
                            continue
                        # 回退到采样法（扫描所有行的实际值类型）
                        if result:
                            for r in result:
                                v = r.get(col_name)
                                if v is not None:
                                    if isinstance(v, str):
                                        str_columns.add(col_name)
                                    break

                for row_dict in result:
                    for k, v in row_dict.items():
                        # Decimal → float（C# 中 NUMBER 列通过 TryParseToDouble() 绑定为 Double?
                        #   序列化时保留小数点，如 5518.0，不应转为 int）
                        if isinstance(v, Decimal):
                            row_dict[k] = float(v)
                            continue
                        # datetime → ISO 字符串（让 JSON 可序列化）
                        # C# 端的日期序列化实际输出 ISO 格式（如 2017-01-10T20:32:50）
                        # Python 保持一致，不做额外格式转换
                        if isinstance(v, _dt):
                            row_dict[k] = v.isoformat()
                        elif isinstance(v, _date):
                            row_dict[k] = f"{v.isoformat()}T00:00:00"
                    # 字符串列 NULL → ''（仅当 null_to_empty=True 时执行）
                    # C# List 用 .ToString()（DBNull→''），Detail 直接赋 entity 属性（null 保持 null）
                    if null_to_empty:
                        for col in str_columns:
                            if row_dict.get(col) is None:
                                row_dict[col] = ""

                elapsed = time.time() - start
                if elapsed > SLOW_QUERY_THRESHOLD:
                    logger.warning(f"[慢查询] {elapsed:.2f}s | SQL: {sql[:200]}...")
                elif elapsed > 1.0:
                    logger.info(f"[查询] {elapsed:.2f}s | rows={len(result)}")

                return result
            finally:
                cursor.close()
        except Exception as ex:
            error_occurred = True
            elapsed = time.time() - start
            logger.error(f"[查询失败] {elapsed:.2f}s | SQL: {sql[:200]}... | Error: {ex}")
            raise
        finally:
            self._return_connection(conn, error=error_occurred)

    def execute_non_query(self, sql: str, params: dict = None) -> int:
        """
        执行 SQL（INSERT/UPDATE/DELETE），返回受影响行数
        """
        start = time.time()
        conn = self._get_connection()
        error_occurred = False
        try:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                conn.commit()
                elapsed = time.time() - start
                if elapsed > SLOW_QUERY_THRESHOLD:
                    logger.warning(f"[慢写入] {elapsed:.2f}s | SQL: {sql[:200]}...")
                return cursor.rowcount
            except Exception:
                conn.rollback()
                raise
            finally:
                cursor.close()
        except Exception as ex:
            error_occurred = True
            elapsed = time.time() - start
            logger.error(f"[写入失败] {elapsed:.2f}s | SQL: {sql[:200]}... | Error: {ex}")
            raise
        finally:
            self._return_connection(conn, error=error_occurred)

    def execute_scalar(self, sql: str, params: dict = None):
        """执行 SQL，返回单个值"""
        start = time.time()
        conn = self._get_connection()
        error_occurred = False
        try:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                row = cursor.fetchone()
                elapsed = time.time() - start
                if elapsed > SLOW_QUERY_THRESHOLD:
                    logger.warning(f"[慢标量查询] {elapsed:.2f}s | SQL: {sql[:200]}...")
                return row[0] if row else None
            finally:
                cursor.close()
        except Exception as ex:
            error_occurred = True
            elapsed = time.time() - start
            logger.error(f"[标量查询失败] {elapsed:.2f}s | SQL: {sql[:200]}... | Error: {ex}")
            raise
        finally:
            self._return_connection(conn, error=error_occurred)

    def fetch_all(self, sql: str, params=None, null_to_empty: bool = True):
        """执行 SQL 返回所有行的 dict 列表（支持 list 位置参数）"""
        return self.execute_query(sql, params, null_to_empty=null_to_empty)

    def fetch_one(self, sql: str, params=None):
        """执行 SQL 返回单条 dict，无数据返回 None（支持 list 位置参数）"""
        rows = self.execute_query(sql, params, null_to_empty=False)
        return rows[0] if rows else None

    def fetch_scalar(self, sql: str, params=None):
        """执行 SQL 返回第一行第一列的值（支持 list 位置参数）"""
        start = time.time()
        conn = self._get_connection()
        error_occurred = False
        try:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                row = cursor.fetchone()
                elapsed = time.time() - start
                if elapsed > SLOW_QUERY_THRESHOLD:
                    logger.warning(f"[慢标量查询] {elapsed:.2f}s | SQL: {sql[:200]}...")
                return row[0] if row else None
            finally:
                cursor.close()
        except Exception as ex:
            error_occurred = True
            elapsed = time.time() - start
            logger.error(f"[标量查询失败] {elapsed:.2f}s | SQL: {sql[:200]}... | Error: {ex}")
            raise
        finally:
            self._return_connection(conn, error=error_occurred)

    def test_connection(self) -> bool:
        """测试数据库连通性"""
        try:
            test_sql = "SELECT 1 FROM DUAL" if self.db_type == "oracle" else "SELECT 1"
            result = self.execute_scalar(test_sql)
            db_name = "Oracle" if self.db_type == "oracle" else "达梦"
            pool_info = f" | 连接池: {self._pool.status}" if self._pool else ""
            logger.info(f"{db_name}数据库连接成功{pool_info}")
            return result == 1
        except Exception as ex:
            logger.error(f"数据库连接失败: {ex}")
            return False


# 全局数据库实例——使用达梦连接（带连接池）
db_helper = DatabaseHelper(db_type="dm")
