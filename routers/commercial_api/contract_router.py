# -*- coding: utf-8 -*-
"""
CommercialApi - Contract 路由
对应原 CommercialApi/Controllers/ContractController.cs
经营合同分析相关接口
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result
from routers.deps import get_db

router = APIRouter()


# ===== 1. GetContractAnalysis =====
@router.get("/Contract/GetContractAnalysis")
async def get_contract_analysis(
    statisticsDate: Optional[str] = Query(None, description="统计日期，格式：yyyy-MM-dd"),
    provinceCode: Optional[str] = Query(None, description="省份编码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取经营合同分析
    原路由: [Route("Contract/GetContractAnalysis")] GET
    原注释: 显示在驿达数智化小程序-经营画像：营收分析板块，显示当月经营合同相关数据
    原 Helper: ContractAnalysisHelper.GetContractAnalysis
    依赖表: CONTRACT_STORAGE.T_REGISTERCOMPACT, T_REGISTERCOMPACTSUB, T_PAYMENTCONFIRM,
            HIGHWAY_STORAGE.T_SERVERPART
    返回: ContractAnalysisModel（ContractProfitLoss/ShopCount/SalesPerSquareMeter/
          ExpiredShopCount/ContractList/ContractCompletionDegree/ConvertRate）
    """
    try:
        # TODO: 实现完整的合同分析逻辑（涉及3张跨schema表关联+聚合计算）
        # 原始返回模型字段：
        result_data = {
            "ContractProfitLoss": 0,        # 合同总金额
            "ShopCount": 0,                  # 在营门店数量
            "SalesPerSquareMeter": 0,        # 欠款总金额（万元）
            "ExpiredShopCount": 0,           # 半年内到期合同数量
            "ContractList": [],              # 到期合同列表 [{name, value}]
            "ContractCompletionDegree": 67.1,  # 合同完成度（原代码写死67.1）
            "ConvertRate": 50.5,             # 转化率（原代码写死50.5）
        }
        logger.warning(f"GetContractAnalysis 复杂查询暂未完整实现（需同步 CONTRACT_STORAGE 表）")
        return Result.success(data=result_data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetContractAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 2. GetMerchantAccountSplit =====
@router.get("/Contract/GetMerchantAccountSplit")
async def get_merchant_account_split(
    StatisticsMonth: Optional[str] = Query(None, description="统计结束月份，格式：yyyy-MM"),
    StatisticsStartMonth: Optional[str] = Query("", description="统计开始月份"),
    calcType: int = Query(1, description="计算方式：1=当月，2=累计"),
    CompactTypes: str = Query("340001", description="合同类型"),
    BusinessTypes: Optional[str] = Query("", description="经营模式"),
    SettlementMods: Optional[str] = Query("", description="结算模式"),
    MerchantIds: Optional[str] = Query("", description="经营商户"),
    SortStr: Optional[str] = Query("", description="排序字段"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取经营商户应收拆分数据
    原路由: [Route("Contract/GetMerchantAccountSplit")] GET
    原 Helper: AccountHelper.GetMerchantAccountSplit
    依赖表: CONTRACT_STORAGE 相关表
    返回: MerchantAccountSummaryModel
    """
    try:
        # 构建查询条件
        where_parts = ['"MERCHANTSPLIT_STATE" = 1']
        params = []

        if CompactTypes:
            where_parts.append(f'"COMPACT_TYPE" IN ({CompactTypes})')
        if BusinessTypes:
            where_parts.append(f'"BUSINESS_TYPE" IN ({BusinessTypes})')
        if SettlementMods:
            where_parts.append(f'"SETTLEMENT_MODES" IN ({SettlementMods})')
        if MerchantIds:
            where_parts.append(f'"MERCHANTS_ID" IN ({MerchantIds})')

        # 处理统计月份（去掉横杠）
        month_str = StatisticsMonth.replace("-", "") if StatisticsMonth else ""
        start_month_str = StatisticsStartMonth.replace("-", "") if StatisticsStartMonth else ""

        if calcType == 1:
            where_parts.append(f'"STATISTICS_MONTH" = ?')
            params.append(int(month_str))
        else:
            where_parts.append(f'"STATISTICS_MONTH" >= ? AND "STATISTICS_MONTH" <= ?')
            params.append(int(start_month_str))
            params.append(int(month_str))

        where_sql = " AND ".join(where_parts)

        # 按商户分组查询
        sql = f"""SELECT "MERCHANTS_ID", COUNT("BUSINESSPROJECT_ID") AS "PROJECT_COUNT",
            SUM("REVENUEDAILY_AMOUNT") AS "REVENUE_AMOUNT",
            SUM("ROYALTYDAILY_PRICE") AS "ROYALTY_PRICE",
            SUM("SUBROYALTYDAILY_PRICE") AS "SUBROYALTY_PRICE",
            SUM("TICKETDAILY_FEE") AS "TICKET_FEE",
            SUM("ROYALTYDAILY_THEORY") AS "ROYALTY_THEORY",
            SUM("SUBROYALTYDAILY_THEORY") AS "SUBROYALTY_THEORY"
        FROM "T_MERCHANTSPLIT"
        WHERE {where_sql}
        GROUP BY "MERCHANTS_ID" """
        rows = db.execute_query(sql, params)

        if not rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        # 汇总统计
        total_project = sum(r.get("PROJECT_COUNT", 0) or 0 for r in rows)
        total_sub_royalty_price = sum(float(r.get("SUBROYALTY_PRICE", 0) or 0) for r in rows)
        total_sub_royalty_theory = sum(float(r.get("SUBROYALTY_THEORY", 0) or 0) for r in rows)

        # 获取商户名称
        merchant_names = {}
        try:
            merchant_rows = db.execute_query('SELECT "COOPMERCHANTS_ID", "COOPMERCHANTS_NAME" FROM "T_COOPMERCHANTS"')
            merchant_names = {r["COOPMERCHANTS_ID"]: r["COOPMERCHANTS_NAME"] for r in merchant_rows}
        except:
            pass

        # 构建商户列表
        merchant_list = []
        for r in rows:
            mid = r.get("MERCHANTS_ID")
            sub_price = float(r.get("SUBROYALTY_PRICE", 0) or 0)
            sub_theory = float(r.get("SUBROYALTY_THEORY", 0) or 0)
            merchant_list.append({
                "MerchantId": int(mid) if mid else 0,
                "MerchantName": merchant_names.get(mid, "") if mid else "",
                "ProjectCount": int(r.get("PROJECT_COUNT", 0) or 0),
                "SubRoyaltyPrice": round(sub_price, 2),
                "SubRoyaltyTheory": round(sub_theory, 2),
                "ReceivableAmount": round(sub_price - sub_theory, 2),
                "ProjectDetailList": None,
            })

        # 排序
        if SortStr:
            sort_field = SortStr.split(' ')[0] if SortStr else ""
            desc = SortStr.lower().endswith(" desc")
            field_map = {"SubRoyaltyPrice": "SubRoyaltyPrice", "SubRoyaltyTheory": "SubRoyaltyTheory",
                         "ReceivableAmount": "ReceivableAmount"}
            if sort_field in field_map:
                merchant_list.sort(key=lambda x: x[field_map[sort_field]], reverse=desc)
            else:
                merchant_list.sort(key=lambda x: x.get("ProjectCount", 0), reverse=True)
        else:
            merchant_list.sort(key=lambda x: x.get("ProjectCount", 0), reverse=True)

        data = {
            "ProjectCount": total_project,
            "SubRoyaltyPrice": round(total_sub_royalty_price, 2),
            "SubRoyaltyTheory": round(total_sub_royalty_theory, 2),
            "ReceivableAmount": round(total_sub_royalty_price - total_sub_royalty_theory, 2),
            "MerchantAccountList": merchant_list,
            "ProjectDetailList": None,
        }
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMerchantAccountSplit 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 3. GetMerchantAccountDetail =====
@router.get("/Contract/GetMerchantAccountDetail")
async def get_merchant_account_detail(
    MerchantId: int = Query(..., description="经营商户内码"),
    StatisticsMonth: str = Query(..., description="统计结束月份，格式yyyyMM"),
    StatisticsStartMonth: Optional[str] = Query("", description="统计开始月份"),
    calcType: int = Query(1, description="计算方式：1=当月，2=累计"),
    CompactTypes: str = Query("340001", description="合同类型"),
    BusinessTypes: Optional[str] = Query("", description="经营模式"),
    SettlementMods: Optional[str] = Query("", description="结算模式"),
    SortStr: Optional[str] = Query("", description="排序字段"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取经营商户应收拆分明细数据
    对齐 C# AccountHelper.GetMerchantAccountDetail
    依赖表: T_MERCHANTSPLIT, T_COOPMERCHANTS, T_SERVERPARTSHOP, T_BRAND
    返回: MerchantAccountModel
    """
    try:
        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0
        def safe_int(v):
            try: return int(v) if v is not None else 0
            except: return 0

        # 构建 WHERE 条件 (对齐 C#)
        where_sql = f" AND MERCHANTS_ID = {MerchantId}"
        if CompactTypes:
            where_sql += f" AND COMPACT_TYPE IN ({CompactTypes})"
        if BusinessTypes:
            where_sql += f" AND BUSINESS_TYPE IN ({BusinessTypes})"
        if SettlementMods:
            where_sql += f" AND SETTLEMENT_MODES IN ({SettlementMods})"
        if calcType == 1:
            where_sql += f" AND STATISTICS_MONTH = {StatisticsMonth}"
        else:
            where_sql += f" AND STATISTICS_MONTH >= {StatisticsStartMonth} AND STATISTICS_MONTH <= {StatisticsMonth}"

        # 查询 T_MERCHANTSPLIT 全部明细
        sql = f"""SELECT * FROM "T_MERCHANTSPLIT"
            WHERE "MERCHANTSPLIT_STATE" = 1{where_sql}"""
        rows = db.execute_query(sql) or []

        if not rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        # 汇总商户级数据
        total_sub_royalty_price = sum(safe_dec(r.get("SUBROYALTY_PRICE")) for r in rows)
        total_sub_royalty_theory = sum(safe_dec(r.get("SUBROYALTY_THEORY")) for r in rows)
        total_receivable = round(total_sub_royalty_price - total_sub_royalty_theory, 2)

        # 查询商户名称
        merchant_name = ""
        m_rows = db.execute_query(f"""SELECT "COOPMERCHANTS_NAME" FROM "T_COOPMERCHANTS"
            WHERE "COOPMERCHANTS_ID" = {MerchantId}""") or []
        if m_rows:
            merchant_name = m_rows[0].get("COOPMERCHANTS_NAME", "")

        # 查询品牌信息（带省份过滤）
        brand_rows = db.execute_query("""SELECT "BRAND_ID","BRAND_NAME","BRAND_INTRO"
            FROM "T_BRAND" WHERE "PROVINCE_CODE" = 340000""") or []
        brand_map = {}
        for b in brand_rows:
            bid = str(b.get("BRAND_ID", ""))
            brand_map[bid] = {
                "BrandId": safe_int(b.get("BRAND_ID")),
                "BrandName": b.get("BRAND_NAME", ""),
                "BrandICO": b.get("BRAND_INTRO", ""),
            }

        # 按 SERVERPART_ID 分组
        from collections import defaultdict
        sp_groups = defaultdict(list)
        for r in rows:
            sp_id = str(r.get("SERVERPART_ID", ""))
            sp_groups[sp_id].append(r)

        project_detail_list = []
        for sp_id, sp_rows in sp_groups.items():
            sp_name = sp_rows[0].get("SERVERPART_NAME", "")
            sp_sub_price = sum(safe_dec(r.get("SUBROYALTY_PRICE")) for r in sp_rows)
            sp_sub_theory = sum(safe_dec(r.get("SUBROYALTY_THEORY")) for r in sp_rows)
            sp_receivable = round(sp_sub_price - sp_sub_theory, 2)

            # 遍历每个项目，构建 BrandAccountList
            brand_account_list = []
            for dr in sp_rows:
                brand_model = {
                    "BusinessType": safe_int(dr.get("BUSINESS_TYPE")),
                    "SettlementMods": safe_int(dr.get("SETTLEMENT_MODES")),
                    "SubRoyaltyPrice": safe_dec(dr.get("SUBROYALTY_PRICE")),
                    "SubRoyaltyTheory": safe_dec(dr.get("SUBROYALTY_THEORY")),
                    "ReceivableAmount": round(safe_dec(dr.get("SUBROYALTY_PRICE")) - safe_dec(dr.get("SUBROYALTY_THEORY")), 2),
                    "BrandId": None,
                    "BrandName": None,
                    "BrandICO": None,
                }
                # 查品牌信息（通过门店表中间跳转）
                shop_id = str(dr.get("SERVERPARTSHOP_ID", ""))
                if shop_id:
                    shop_rows = db.execute_query(f"""SELECT "BUSINESS_BRAND","BRAND_NAME"
                        FROM "T_SERVERPARTSHOP"
                        WHERE "SERVERPARTSHOP_ID" IN ({shop_id}) AND "BUSINESS_BRAND" IS NOT NULL""") or []
                    if shop_rows:
                        b_id = str(shop_rows[0].get("BUSINESS_BRAND", ""))
                        if b_id in brand_map:
                            brand_model["BrandId"] = brand_map[b_id]["BrandId"]
                            brand_model["BrandName"] = brand_map[b_id]["BrandName"]
                            brand_model["BrandICO"] = brand_map[b_id]["BrandICO"]
                            if brand_model["BrandICO"] and brand_model["BrandICO"].startswith("/"):
                                brand_model["BrandICO"] = "http://yida.anhighway.cn" + brand_model["BrandICO"]
                        else:
                            brand_model["BrandId"] = safe_int(b_id)
                            brand_model["BrandName"] = shop_rows[0].get("BRAND_NAME", "")

                brand_account_list.append(brand_model)

            # 对品牌列表排序
            if SortStr:
                sort_key = SortStr.split(" ")[0]
                is_desc = SortStr.lower().endswith(" desc")
                sort_fn = {
                    "SubRoyaltyPrice": lambda x: x.get("SubRoyaltyPrice", 0),
                    "SubRoyaltyTheory": lambda x: x.get("SubRoyaltyTheory", 0),
                    "ReceivableAmount": lambda x: x.get("ReceivableAmount", 0),
                }.get(sort_key, None)
                if sort_fn:
                    brand_account_list.sort(key=sort_fn, reverse=is_desc)

            detail_model = {
                "ServerpartId": sp_id,
                "ServerpartName": sp_name,
                "BrandCount": len(sp_rows),
                "SubRoyaltyPrice": round(sp_sub_price, 2),
                "SubRoyaltyTheory": round(sp_sub_theory, 2),
                "ReceivableAmount": sp_receivable,
                "BrandAccountList": brand_account_list,
            }
            project_detail_list.append(detail_model)

        # 对服务区列表排序
        if SortStr:
            sort_key = SortStr.split(" ")[0]
            is_desc = SortStr.lower().endswith(" desc")
            sort_fn_map = {
                "SubRoyaltyPrice": lambda x: x.get("SubRoyaltyPrice", 0),
                "SubRoyaltyTheory": lambda x: x.get("SubRoyaltyTheory", 0),
                "ReceivableAmount": lambda x: x.get("ReceivableAmount", 0),
            }
            sort_fn = sort_fn_map.get(sort_key, lambda x: x.get("ServerpartName", ""))
            project_detail_list.sort(key=sort_fn, reverse=is_desc)

        account_model = {
            "MerchantId": MerchantId,
            "MerchantName": merchant_name,
            "ProjectCount": len(rows),
            "SubRoyaltyPrice": round(total_sub_royalty_price, 2),
            "SubRoyaltyTheory": round(total_sub_royalty_theory, 2),
            "ReceivableAmount": total_receivable,
            "ProjectDetailList": project_detail_list,
        }

        return Result.success(data=account_model, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMerchantAccountDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")
