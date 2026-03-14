-- ============================================
-- T_BRAND 品牌表建表脚本（达梦数据库）
-- 对应原 Oracle 表 COOP_MERCHANT.T_BRAND
-- ============================================

-- 创建序列
CREATE SEQUENCE SEQ_BRAND START WITH 1 INCREMENT BY 1;

-- 创建品牌表
CREATE TABLE T_BRAND (
    BRAND_ID          INT              PRIMARY KEY,    -- 内码
    BRAND_PID         INT,                             -- 上级内码
    BRAND_INDEX       INT,                             -- 品牌索引
    BRAND_NAME        VARCHAR(200),                    -- 品牌名称
    BRAND_CATEGORY    INT,                             -- 品牌分类（1000：经营品牌；2000：商城品牌）
    BRAND_INDUSTRY    VARCHAR(200),                    -- 经营业态
    BRAND_TYPE        INT,                             -- 品牌类型
    BRAND_INTRO       VARCHAR(500),                    -- 品牌图标
    BRAND_STATE       SMALLINT DEFAULT 1,              -- 有效状态（1=有效，0=已删除）
    WECHATAPPSIGN_ID  INT,                             -- 小程序内码
    WECHATAPPSIGN_NAME VARCHAR(200),                   -- 小程序名字
    WECHATAPP_APPID   VARCHAR(200),                    -- 小程序APPID
    OWNERUNIT_ID      INT,                             -- 业主内码
    OWNERUNIT_NAME    VARCHAR(200),                    -- 业主单位
    PROVINCE_CODE     INT,                             -- 省份标识
    STAFF_ID          INT,                             -- 人员内码
    STAFF_NAME        VARCHAR(100),                    -- 配置人员
    OPERATE_DATE      TIMESTAMP,                       -- 配置时间
    BRAND_DESC        VARCHAR(2000),                   -- 品牌介绍
    COMMISSION_RATIO  VARCHAR(50)                      -- 建议提成比例
);

-- 插入测试数据
INSERT INTO T_BRAND (BRAND_ID, BRAND_NAME, BRAND_CATEGORY, BRAND_INDUSTRY, BRAND_TYPE, BRAND_STATE, OWNERUNIT_ID, OWNERUNIT_NAME, STAFF_NAME, OPERATE_DATE)
VALUES (SEQ_BRAND.NEXTVAL, '星巴克', 1000, '餐饮', 1, 1, 1, '浙江高速服务区', '管理员', SYSDATE);

INSERT INTO T_BRAND (BRAND_ID, BRAND_NAME, BRAND_CATEGORY, BRAND_INDUSTRY, BRAND_TYPE, BRAND_STATE, OWNERUNIT_ID, OWNERUNIT_NAME, STAFF_NAME, OPERATE_DATE)
VALUES (SEQ_BRAND.NEXTVAL, '肯德基', 1000, '餐饮', 1, 1, 1, '浙江高速服务区', '管理员', SYSDATE);

INSERT INTO T_BRAND (BRAND_ID, BRAND_NAME, BRAND_CATEGORY, BRAND_INDUSTRY, BRAND_TYPE, BRAND_STATE, OWNERUNIT_ID, OWNERUNIT_NAME, STAFF_NAME, OPERATE_DATE)
VALUES (SEQ_BRAND.NEXTVAL, '全家便利店', 1000, '零售', 2, 1, 1, '浙江高速服务区', '管理员', SYSDATE);

INSERT INTO T_BRAND (BRAND_ID, BRAND_NAME, BRAND_CATEGORY, BRAND_INDUSTRY, BRAND_TYPE, BRAND_STATE, OWNERUNIT_ID, OWNERUNIT_NAME, STAFF_NAME, OPERATE_DATE)
VALUES (SEQ_BRAND.NEXTVAL, '天猫优选', 2000, '电商', 3, 1, 2, '杭州服务区', '操作员', SYSDATE);

INSERT INTO T_BRAND (BRAND_ID, BRAND_NAME, BRAND_CATEGORY, BRAND_INDUSTRY, BRAND_TYPE, BRAND_STATE, OWNERUNIT_ID, OWNERUNIT_NAME, STAFF_NAME, OPERATE_DATE)
VALUES (SEQ_BRAND.NEXTVAL, '中石化', 1000, '油品', 4, 1, 1, '浙江高速服务区', '管理员', SYSDATE);

COMMIT;
