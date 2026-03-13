# -*- coding: utf-8 -*-
"""
CommercialApi - 节日/INC分析/SABFI Service
从 revenue_router.py 中抽取（框架声明，后续逐步迁移业务逻辑）

路由清单（共 20 个）:
  L3170  GetHolidayCompare          — 节日同比
  L3273  GetAccountReceivable       — 应收账款
  L3455  GetCurRevenue              — 当日实时营收
  L3509  GetShopCurRevenue          — 门店当日实时营收
  L3567  GetLastSyncDateTime        — 最后同步时间
  L3706  GetHolidayAnalysis         — 节日分析
  L3907  GetHolidayAnalysisBatch    — 节日批次分析
  L3976  GetServerpartINCAnalysis   — 服务区 INC 分析
  L4294  GetShopINCAnalysis         — 门店 INC 分析
  L4631  GetMonthlyBusinessAnalysis — 月度经营分析
  L4833  GetMonthlySPINCAnalysis    — 月度 SP INC 分析
  L4997  GetTransactionDetailList   — 交易明细列表
  L5109  GetHolidayRevenueRatio     — 节日营收占比
  L5135  GetBusinessRevenueList (POST) — 业态营收列表
  L5161  GetMonthlyBusinessRevenue (POST) — 月度业态营收
  L5185  GetCompanyRevenueReport    — 公司营收报表
  L5525  GetRevenueCompare          — 营收对比
  L5837  GetHolidaySPRAnalysis      — 节日 SPR 分析
  L6110  GetHolidayDailyAnalysis    — 节日逐日分析
  L6238  GetMonthINCAnalysis        — 月度 INC 分析
  L6972  GetMonthINCAnalysisSummary — 月度 INC 汇总
  L7054  StorageMonthINCAnalysis    — 月度 INC 存储
  L7073  GetShopSABFIList           — 门店 SABFI 列表
  L7841  GetShopMonthSABFIList      — 门店月度 SABFI

上述路由逻辑体量巨大（合计约 4,800 行），且多数含复杂的多表 JOIN、
日期遍历、树形聚合等逻辑，与 Router 层深度耦合。
当前阶段以声明式框架建立索引，后续重写 Router 时按功能子组逐步迁移。

建议拆分方向:
  - holiday_core: GetHolidayCompare, GetHolidayAnalysis, GetHolidayAnalysisBatch,
                  GetHolidayRevenueRatio, GetHolidaySPRAnalysis, GetHolidayDailyAnalysis
  - inc_analysis: GetServerpartINCAnalysis, GetShopINCAnalysis, GetMonthINCAnalysis,
                  GetMonthINCAnalysisSummary, GetMonthlySPINCAnalysis, StorageMonthINCAnalysis
  - account_realtime: GetAccountReceivable, GetCurRevenue, GetShopCurRevenue,
                      GetLastSyncDateTime
  - monthly_business: GetMonthlyBusinessAnalysis, GetTransactionDetailList,
                      GetBusinessRevenueList, GetMonthlyBusinessRevenue,
                      GetCompanyRevenueReport, GetRevenueCompare
  - sabfi: GetShopSABFIList, GetShopMonthSABFIList
"""


# ===== 以下路由暂保留在 Router 层，待后续按子组逐步迁移 =====
# 每个路由保持在 Router 原始位置，不做任何修改
# 本文件作为后续迁移的索引和拆分规划参考


# ===== 1. GetCurRevenue / GetShopCurRevenue =====
# 实时营收查询，查 T_ENDACCOUNT_TEMP 汇总
# 逻辑相对简洁，优先迁移


# ===== 2. GetLastSyncDateTime =====
# 查最后同步时间，逻辑简单
# 优先迁移


# ===== 3. GetAccountReceivable =====
# 应收账款查询，约 180 行
# 含复杂的租金/提成计算和年度累计


# ===== 4. GetHolidayCompare =====
# 节日同比，约 100 行


# ===== 5-6. GetHolidayAnalysis / GetHolidayAnalysisBatch =====
# 节日分析主逻辑，约 200+70 行


# ===== 7-8. GetServerpartINCAnalysis / GetShopINCAnalysis =====
# INC 分析核心，各约 300 行，含复杂的多维度聚合


# ===== 9-10. GetMonthlyBusinessAnalysis / GetMonthlySPINCAnalysis =====
# 月度经营分析，各约 200 行


# ===== 11. GetCompanyRevenueReport =====
# 公司营收报表，约 340 行，含多层嵌套


# ===== 12. GetRevenueCompare =====
# 营收对比，约 310 行


# ===== 13-14. GetHolidaySPRAnalysis / GetHolidayDailyAnalysis =====
# 节日 SPR 和逐日分析，各约 270/130 行


# ===== 15. GetMonthINCAnalysis =====
# 月度 INC 分析，约 730 行（最大单路由）


# ===== 16-17. GetShopSABFIList / GetShopMonthSABFIList =====
# SABFI 门店列表，各约 770/120 行
