# -*- coding: utf-8 -*-
"""
应用配置管理
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """应用配置"""

    # === 应用设置 ===
    APP_NAME: str = "EShangApi"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # === 达梦数据库配置 ===
    DM_HOST: str = os.getenv("DM_HOST", "192.168.1.99")
    DM_PORT: int = int(os.getenv("DM_PORT", "5236"))
    DM_USER: str = os.getenv("DM_USER", "NEWPYTHON")
    DM_PASSWORD: str = os.getenv("DM_PASSWORD", "NewPython@2025")
    DM_DATABASE: str = os.getenv("DM_DATABASE", "DMNEW")

    # === Oracle 数据库配置（用于验证测试，与原 C# 项目共用） ===
    ORA_USER: str = os.getenv("ORA_USER", "highway_exchange")
    ORA_PASSWORD: str = os.getenv("ORA_PASSWORD", "qrwl")
    ORA_DSN: str = os.getenv("ORA_DSN", "127.0.0.1/orcl")

    # === Redis 配置 ===
    REDIS_HOST: str = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_REVENUE_TREND_DB: int = int(os.getenv("REDIS_REVENUE_TREND_DB", "1"))

    # === AES 加解密配置 ===
    AES_KEY: str = os.getenv("AES_KEY", "eshangapi2025key")  # 16字节密钥
    AES_IV: str = os.getenv("AES_IV", "eshangapi2025iv!")    # 16字节IV

    # === CORS 配置 ===
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True

    # === 日志配置 ===
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
