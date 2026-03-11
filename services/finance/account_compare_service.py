# -*- coding: utf-8 -*-
"""
经营数据对比分析表 — GetAccountCompare
完整实现 C# AccountHelper.GetAccountCompare + BindSPAccountCompare + calcGuaranteeIncome
"""
import logging
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

logger = logging.getLogger(__name__)


# ====================== 数据模型 ======================

def _ccm(cur=None, compare=None, cur_intro=None, compare_intro=None,
         increase=None, rate=None):
    """构造 CommonCompareModel dict"""
    return {
        "curData": cur,
        "compareData": compare,
        "increaseData": increase,
        "increaseRate": rate,
        "curIntro": cur_intro,
        "compareIntro": compare_intro,
    }


def _node(node_data: dict, children: list = None):
    """构造 NestingModel<AccountCompareModel>"""
    return {"node": node_data, "children": children or []}


def _d(v, default=0):
    """安全转 Decimal"""
    if v is None:
        return Decimal(0)
    try:
        return Decimal(str(v))
    except Exception:
        return Decimal(default)


def _round2(v):
    """保留两位小数"""
    return float(Decimal(str(v)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _try_int(v, default=0):
    """安全转 int"""
    if v is None:
        return default
    try:
        return int(v)
    except (ValueError, TypeError):
        return default


def _try_date(v):
    """安全解析日期"""
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d %H:%M:%S",
                "%Y/%m/%d", "%Y%m%d"):
        try:
            return datetime.strptime(s[:len(fmt.replace('%', '').replace('-', '').replace('/', '').replace(':', '').replace(' ', '')) + s.count('-') + s.count('/') + s.count(':') + s.count(' ')], fmt)
        except Exception:
            continue
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d")
    except Exception:
        try:
            return datetime.strptime(s[:10], "%Y/%m/%d")
        except Exception:
            return None


def _parse_date(s: str) -> datetime:
    """解析日期字符串"""
    if not s:
        return None
    s = s.strip().split(' ')[0]  # 只取日期部分
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def _join_distinct(rows, field):
    """从行列表中提取某字段去重拼接"""
    seen = set()
    result = []
    for r in rows:
        v = str(r.get(field, "") or "")
        if v and v not in seen:
            seen.add(v)
            result.append(v)
    return ",".join(result)


# ====================== 保底/提成计算 ======================

def _calc_guarantee_income(shop_node, dr_project, start_date, end_date,
                           compare_start, compare_end,
                           shoproyalty_list, royalty_detail_list):
    """
    C# calcGuaranteeIncome — 计算保底租金、提成比例、保底收入
    返回 (guarantee_price, guarantee_ratio, guarantee_income, income_str, data_type)
    """
    data_type = _try_int(dr_project.get("DATATYPE"))
    cur_start = start_date if data_type == 1 else compare_start
    cur_end = end_date if data_type == 1 else compare_end

    sr_id = _try_int(dr_project.get("SHOPROYALTY_ID"))
    sr_model = None
    for s in shoproyalty_list:
        if _try_int(s.get("SHOPROYALTY_ID")) == sr_id:
            sr_model = s
            break

    guarantee_price = Decimal(0)
    guarantee_ratio = None
    guarantee_income = Decimal(0)
    income_str = ""

    if sr_model is None:
        return guarantee_price, guarantee_ratio, guarantee_income, income_str, data_type

    # 判断当前是第几期
    sr_end = _try_date(sr_model.get("ENDDATE"))
    bp_id = _try_int(sr_model.get("BUSINESSPROJECT_ID"))
    period_index = sum(1 for s in shoproyalty_list
                       if _try_int(s.get("BUSINESSPROJECT_ID")) == bp_id
                       and _try_date(s.get("ENDDATE")) is not None
                       and sr_end is not None
                       and _try_date(s.get("ENDDATE")) <= sr_end)

    # 撤场日期
    period_end = sr_end
    closed_date_val = dr_project.get("CLOSED_DATE")
    if closed_date_val is not None and str(closed_date_val).strip():
        cd = _try_date(closed_date_val)
        if cd and period_end and cd <= period_end:
            period_end = cd - timedelta(days=1)

    biz_type = _try_int(shop_node["node"].get("BusinessType"))
    tax_rate = _d(shop_node["node"].get("TaxRate", 9))

    sr_start = _try_date(sr_model.get("STARTDATE"))
    nature_day = _try_int(sr_model.get("NATUREDAY"), 1)
    if nature_day == 0:
        nature_day = 1

    # 根据经营模式确定保底租金和提成比例
    if biz_type == 3000:
        # 保底采购
        detail = None
        for d in royalty_detail_list:
            if _try_int(d.get("SHOPROYALTY_ID")) == _try_int(sr_model.get("SHOPROYALTY_ID")):
                detail = d
                break
        if detail:
            guarantee_ratio = Decimal(100) - _d(detail.get("GUARANTEERATIO"))
            guarantee_price = _d(detail.get("MINTURNOVER")) * guarantee_ratio * Decimal(100)
        else:
            guarantee_price = _d(sr_model.get("MINTURNOVER")) * Decimal(10000)
            guarantee_ratio = _d(sr_model.get("GUARANTEERATIO"))
    elif biz_type == 1000:
        # 合作经营
        guarantee_price = _d(sr_model.get("MINTURNOVER")) * Decimal(10000)
        guarantee_ratio = _d(sr_model.get("GUARANTEERATIO"))
    else:
        # 固定租金等
        guarantee_price = _d(sr_model.get("RENTFEE")) * Decimal(10000)

    # 日均保底收入（除税）
    avg_gp = _round2(guarantee_price / Decimal(nature_day) / (1 + tax_rate / Decimal(100)))

    # 装修期天数
    decorate_s = _try_date(dr_project.get("DECORATE_STARTDATE"))
    decorate_e = _try_date(dr_project.get("DECORATE_ENDDATE"))
    decorate_days = 0
    act_start = max(cur_start, sr_start) if sr_start else cur_start

    if decorate_s and decorate_e and act_start and act_start <= decorate_e and act_start >= decorate_s:
        if cur_start > decorate_s:
            end_ref = min(cur_end, decorate_e) if cur_end and decorate_e else (cur_end or decorate_e)
            decorate_days = (end_ref - cur_start).days + 1
        else:
            if cur_end and decorate_e and cur_end < decorate_e:
                decorate_days = (cur_end - decorate_s).days + 1
            elif decorate_e and decorate_s:
                decorate_days = (decorate_e - decorate_s).days + 1

    decorate_str = f",不含装修期{decorate_days}天" if decorate_days > 0 else ""

    if period_end and cur_start and period_end < cur_start:
        # 已撤场
        guarantee_income = Decimal(0)
        income_str = f"第{period_index}期已撤场(0)"
    elif sr_start and cur_start and cur_start > sr_start:
        end_ref = min(cur_end, period_end) if cur_end and period_end else (cur_end or period_end)
        if end_ref and cur_start:
            execute_days = (end_ref - cur_start).days + 1
        else:
            execute_days = 0
        guarantee_income = _round2(Decimal(str(avg_gp)) * (execute_days - decorate_days))
        income_str = (f"第{period_index}期保底租金({guarantee_price})/周期天数({nature_day})/"
                      f"税(1 + {tax_rate}%)*执行天数({execute_days}{decorate_str})")
    else:
        sr_end_val = _try_date(sr_model.get("ENDDATE"))
        if (cur_end and period_end and (cur_end < period_end or period_end != sr_end_val)):
            end_ref = min(cur_end, period_end) if cur_end and period_end else (cur_end or period_end)
            if end_ref and sr_start:
                execute_days = (end_ref - sr_start).days + 1
            else:
                execute_days = 0
            guarantee_income = _round2(Decimal(str(avg_gp)) * (execute_days - decorate_days))
            income_str = (f"第{period_index}期保底租金({guarantee_price})/周期天数({nature_day})/"
                          f"税(1 + {tax_rate}%)*执行天数({execute_days}{decorate_str})")
        else:
            # 整个周期
            guarantee_income = _round2(guarantee_price / (1 + tax_rate / Decimal(100)))
            income_str = f"第{period_index}期保底租金({guarantee_price})/税(1 + {tax_rate}%)"

    # 保底租金 / 保底收入说明
    node = shop_node["node"]
    gp = node.get("GuaranteePrice", {})
    gi = node.get("GuaranteeIncome", {})

    if data_type == 1:
        old_intro = gp.get("curIntro") or ""
        gp["curIntro"] = f"第{period_index}期保底租金({guarantee_price})" + \
                         ("" if not old_intro else "+" + old_intro)
        if income_str:
            old_gi = gi.get("curIntro") or ""
            gi["curIntro"] = income_str + ("" if not old_gi else "+" + old_gi)
    else:
        old_intro = gp.get("compareIntro") or ""
        gp["compareIntro"] = f"第{period_index}期保底租金({guarantee_price})" + \
                             ("" if not old_intro else "+" + old_intro)
        if income_str:
            old_gi = gi.get("compareIntro") or ""
            gi["compareIntro"] = income_str + ("" if not old_gi else "+" + old_gi)

    return float(guarantee_price), guarantee_ratio, float(guarantee_income), income_str, data_type


# ====================== 绑定服务区数据 ======================

def _bind_sp_account_compare(sp_node, start_date, end_date, compare_start, compare_end,
                             revenue_data, project_data, shop_list,
                             shoproyalty_list, royalty_detail_list):
    """
    C# BindSPAccountCompare — 绑定服务区经营数据对比分析
    """
    sp_id = sp_node["node"].get("ServerpartId")
    project_ids_used = set()

    # ---- 1. 绑定有营收的经营项目 ----
    # 找出属于该服务区且有 BUSINESSPROJECT_ID 的营收数据
    sp_revenue = [r for r in revenue_data
                  if _try_int(r.get("SERVERPART_ID")) == sp_id
                  and r.get("BUSINESSPROJECT_ID")]

    # 按 BUSINESSPROJECT_ID 分组
    bp_ids_in_revenue = list({str(r.get("BUSINESSPROJECT_ID")) for r in sp_revenue})

    shop_id_list = set()       # 本期已处理的门店
    compare_shop_id_list = set()  # 对比期已处理的门店

    for bp_id_str in bp_ids_in_revenue:
        rev_rows = [r for r in sp_revenue if str(r.get("BUSINESSPROJECT_ID")) == bp_id_str]
        if not rev_rows:
            continue

        # 本期 / 对比期营收汇总
        cur_revenue = sum(_d(r.get("REVENUE_AMOUNT")) for r in rev_rows if _try_int(r.get("DATATYPE")) == 1)
        cmp_revenue = sum(_d(r.get("REVENUE_AMOUNT")) for r in rev_rows if _try_int(r.get("DATATYPE")) == 2)

        shop_node = _node({
            "SPRegionTypeId": sp_node["node"].get("SPRegionTypeId"),
            "SPRegionTypeName": sp_node["node"].get("SPRegionTypeName"),
            "ServerpartId": sp_id,
            "ServerpartName": sp_node["node"].get("ServerpartName"),
            "ServerpartShopId": _join_distinct(rev_rows, "SERVERPARTSHOP_ID"),
            "ServerpartShopName": _join_distinct(rev_rows, "SHOPSHORTNAME"),
            "Brand_Id": None,
            "Brand_Name": None,
            "Brand_ICO": None,
            "MerchantsId": _try_int(rev_rows[0].get("SELLER_ID")),
            "MerchantsName": str(rev_rows[0].get("SELLER_NAME") or ""),
            "BusinessTradeType": 3,
            "BusinessProjectId": bp_id_str,
            "BusinessType": _try_int(rev_rows[0].get("BUSINESS_TYPE")),
            "TaxRate": sp_node["node"].get("TaxRate"),
            "GuaranteePrice": _ccm(cur=0, compare=0, cur_intro="", compare_intro=""),
            "GuaranteeRatio": _ccm(),
            "RevenueAmount": _ccm(cur=float(cur_revenue), compare=float(cmp_revenue)),
            "GuaranteeIncome": _ccm(cur=0, compare=0, cur_intro="", compare_intro=""),
            "RoyaltyIncome": _ccm(cur=0, compare=0),
            "ConfirmIncome": _ccm(cur=0, compare=0),
        })

        # 计算保底提成
        proj_rows = [p for p in project_data
                     if str(p.get("BUSINESSPROJECT_ID")) == bp_id_str]
        # 按 DATATYPE, ENDDATE desc 排序
        proj_rows.sort(key=lambda x: (
            _try_int(x.get("DATATYPE")),
            -((_try_date(x.get("ENDDATE")) or datetime(2000, 1, 1)).timestamp())
        ))

        for pr in proj_rows:
            gp, gr, gi, income_str, dt = _calc_guarantee_income(
                shop_node, pr, start_date, end_date, compare_start, compare_end,
                shoproyalty_list, royalty_detail_list)
            n = shop_node["node"]
            if dt == 1:
                n["GuaranteePrice"]["curData"] = (n["GuaranteePrice"]["curData"] or 0) + gp
                n["GuaranteeIncome"]["curData"] = (n["GuaranteeIncome"]["curData"] or 0) + gi
                if n["GuaranteeRatio"]["curData"] is None and gr is not None:
                    n["GuaranteeRatio"]["curData"] = float(gr)
                    ra = n["RevenueAmount"]["curData"] or 0
                    tax = _d(n.get("TaxRate", 9))
                    n["RoyaltyIncome"]["curData"] = _round2(
                        Decimal(str(ra)) * gr / Decimal(100) / (1 + tax / Decimal(100)))
                    n["RoyaltyIncome"]["curIntro"] = (
                        f"营业额({ra})*提成比例({gr}%)/税(1 + {tax}%)")
            else:
                n["GuaranteePrice"]["compareData"] = (n["GuaranteePrice"]["compareData"] or 0) + gp
                n["GuaranteeIncome"]["compareData"] = (n["GuaranteeIncome"]["compareData"] or 0) + gi
                if n["GuaranteeRatio"]["compareData"] is None and gr is not None:
                    n["GuaranteeRatio"]["compareData"] = float(gr)
                    ra = n["RevenueAmount"]["compareData"] or 0
                    tax = _d(n.get("TaxRate", 9))
                    n["RoyaltyIncome"]["compareData"] = _round2(
                        Decimal(str(ra)) * gr / Decimal(100) / (1 + tax / Decimal(100)))
                    n["RoyaltyIncome"]["compareIntro"] = (
                        f"营业额({ra})*提成比例({gr}%)/税(1 + {tax}%)")

            # 应确认收入 = max(保底, 提成)
            _update_confirm_income(n)

        sp_node["children"].append(shop_node)
        project_ids_used.add(bp_id_str)

    # ---- 2. 绑定有营收但无合同的门店 ----
    sp_revenue_no_bp = [r for r in revenue_data
                        if _try_int(r.get("SERVERPART_ID")) == sp_id
                        and not r.get("BUSINESSPROJECT_ID")]
    shop_names = list({str(r.get("SHOPSHORTNAME") or "") for r in sp_revenue_no_bp})

    for sn in shop_names:
        rev_rows = [r for r in sp_revenue_no_bp if str(r.get("SHOPSHORTNAME") or "") == sn]
        if not rev_rows:
            continue

        cur_rev = sum(_d(r.get("REVENUE_AMOUNT")) for r in rev_rows if _try_int(r.get("DATATYPE")) == 1)
        cmp_rev = sum(_d(r.get("REVENUE_AMOUNT")) for r in rev_rows if _try_int(r.get("DATATYPE")) == 2)

        biz_type = _try_int(rev_rows[0].get("BUSINESS_TYPE"))
        trade_type = 3
        if biz_type == 4000:
            if sn in ("自营商超", "自营超市", "加油站便利店"):
                trade_type = 1
            else:
                trade_type = 2

        shop_node = _node({
            "SPRegionTypeId": sp_node["node"].get("SPRegionTypeId"),
            "SPRegionTypeName": sp_node["node"].get("SPRegionTypeName"),
            "ServerpartId": sp_id,
            "ServerpartName": sp_node["node"].get("ServerpartName"),
            "ServerpartShopId": _join_distinct(rev_rows, "SERVERPARTSHOP_ID"),
            "ServerpartShopName": _join_distinct(rev_rows, "SHOPSHORTNAME"),
            "Brand_Id": None,
            "Brand_Name": None,
            "Brand_ICO": None,
            "MerchantsId": _try_int(rev_rows[0].get("SELLER_ID")),
            "MerchantsName": str(rev_rows[0].get("SELLER_NAME") or ""),
            "BusinessTradeType": trade_type,
            "BusinessType": biz_type,
            "TaxRate": sp_node["node"].get("TaxRate"),
            "GuaranteePrice": _ccm(cur=0, compare=0),
            "GuaranteeRatio": _ccm(),
            "RevenueAmount": _ccm(cur=float(cur_rev), compare=float(cmp_rev)),
            "GuaranteeIncome": _ccm(cur=0, compare=0),
            "RoyaltyIncome": _ccm(cur=0, compare=0),
            "ConfirmIncome": _ccm(cur=0, compare=0),
        })
        sp_node["children"].append(shop_node)

    # ---- 3. 绑定无营收的经营项目 ----
    sp_projects = [p for p in project_data
                   if _try_int(p.get("SERVERPART_ID")) == sp_id
                   and str(p.get("BUSINESSPROJECT_ID")) not in project_ids_used]
    no_rev_bp_ids = list({str(p.get("BUSINESSPROJECT_ID")) for p in sp_projects})

    for bp_id_str in no_rev_bp_ids:
        proj_rows = [p for p in sp_projects if str(p.get("BUSINESSPROJECT_ID")) == bp_id_str]
        if not proj_rows:
            continue
        proj_rows.sort(key=lambda x: (
            _try_int(x.get("DATATYPE")),
            -((_try_date(x.get("ENDDATE")) or datetime(2000, 1, 1)).timestamp())
        ))
        first = proj_rows[0]
        shop_id_val = str(first.get("SERVERPARTSHOP_ID") or "")
        # 查门店名
        shop_name_parts = []
        for sid in shop_id_val.split(","):
            sid = sid.strip()
            if not sid:
                continue
            for sl in shop_list:
                if str(sl.get("SERVERPARTSHOP_ID")) == sid:
                    sn = str(sl.get("SHOPSHORTNAME") or "")
                    if sn and sn not in shop_name_parts:
                        shop_name_parts.append(sn)
                    break
        shop_name = ",".join(shop_name_parts)

        shop_node = _node({
            "SPRegionTypeId": sp_node["node"].get("SPRegionTypeId"),
            "SPRegionTypeName": sp_node["node"].get("SPRegionTypeName"),
            "ServerpartId": sp_id,
            "ServerpartName": sp_node["node"].get("ServerpartName"),
            "ServerpartShopId": shop_id_val,
            "ServerpartShopName": shop_name,
            "Brand_Id": None,
            "Brand_Name": None,
            "Brand_ICO": None,
            "MerchantsId": _try_int(first.get("MERCHANTS_ID")),
            "MerchantsName": str(first.get("MERCHANTS_NAME") or ""),
            "BusinessTradeType": 3,
            "BusinessProjectId": bp_id_str,
            "BusinessType": _try_int(first.get("BUSINESS_TYPE")),
            "TaxRate": sp_node["node"].get("TaxRate"),
            "GuaranteePrice": _ccm(cur=0, compare=0, cur_intro="", compare_intro=""),
            "GuaranteeRatio": _ccm(),
            "RevenueAmount": _ccm(cur=0, compare=0),
            "GuaranteeIncome": _ccm(cur=0, compare=0, cur_intro="", compare_intro=""),
            "RoyaltyIncome": _ccm(cur=0, compare=0),
            "ConfirmIncome": _ccm(cur=0, compare=0),
        })

        for pr in proj_rows:
            gp, gr, gi, _, dt = _calc_guarantee_income(
                shop_node, pr, start_date, end_date, compare_start, compare_end,
                shoproyalty_list, royalty_detail_list)
            n = shop_node["node"]
            if dt == 1:
                n["GuaranteePrice"]["curData"] = (n["GuaranteePrice"]["curData"] or 0) + gp
                n["GuaranteeIncome"]["curData"] = (n["GuaranteeIncome"]["curData"] or 0) + gi
                if n["GuaranteeRatio"]["curData"] is None and gr is not None:
                    n["GuaranteeRatio"]["curData"] = float(gr)
            else:
                n["GuaranteePrice"]["compareData"] = (n["GuaranteePrice"]["compareData"] or 0) + gp
                n["GuaranteeIncome"]["compareData"] = (n["GuaranteeIncome"]["compareData"] or 0) + gi
                if n["GuaranteeRatio"]["compareData"] is None and gr is not None:
                    n["GuaranteeRatio"]["compareData"] = float(gr)

            # 无营收→应确认收入 = 保底收入
            n["ConfirmIncome"]["curData"] = n["GuaranteeIncome"]["curData"]
            n["ConfirmIncome"]["curIntro"] = (
                f"保底收入({n['GuaranteeIncome']['curData']})>"
                f"提成收入(0)=保底收入({n['GuaranteeIncome']['curData']})")
            n["ConfirmIncome"]["compareData"] = n["GuaranteeIncome"]["compareData"]
            n["ConfirmIncome"]["compareIntro"] = (
                f"保底收入({n['GuaranteeIncome']['compareData']})>"
                f"提成收入(0)=保底收入({n['GuaranteeIncome']['compareData']})")

        sp_node["children"].append(shop_node)

    if not sp_node["children"]:
        return

    # 按门店名排序
    sp_node["children"].sort(key=lambda x: str(x["node"].get("ServerpartShopName") or ""))

    # 累计汇总
    _aggregate_node(sp_node)


def _update_confirm_income(n):
    """更新应确认收入 = max(保底, 提成)"""
    gi_cur = n["GuaranteeIncome"]["curData"] or 0
    ri_cur = n["RoyaltyIncome"]["curData"] or 0
    if gi_cur < ri_cur:
        n["ConfirmIncome"]["curData"] = ri_cur
        n["ConfirmIncome"]["curIntro"] = (
            f"提成收入({ri_cur})>保底收入({gi_cur})=提成收入({ri_cur})")
    else:
        n["ConfirmIncome"]["curData"] = gi_cur
        n["ConfirmIncome"]["curIntro"] = (
            f"保底收入({gi_cur})>提成收入({ri_cur})=保底收入({gi_cur})")

    gi_cmp = n["GuaranteeIncome"]["compareData"] or 0
    ri_cmp = n["RoyaltyIncome"]["compareData"] or 0
    if gi_cmp < ri_cmp:
        n["ConfirmIncome"]["compareData"] = ri_cmp
        n["ConfirmIncome"]["compareIntro"] = (
            f"提成收入({ri_cmp})>保底收入({gi_cmp})=提成收入({ri_cmp})")
    else:
        n["ConfirmIncome"]["compareData"] = gi_cmp
        n["ConfirmIncome"]["compareIntro"] = (
            f"保底收入({gi_cmp})>提成收入({ri_cmp})=保底收入({gi_cmp})")


def _aggregate_node(parent):
    """汇总子节点到父节点"""
    children = parent["children"]
    if not children:
        return
    n = parent["node"]
    n["GuaranteePrice"] = _ccm(
        cur=sum(c["node"]["GuaranteePrice"]["curData"] or 0 for c in children),
        compare=sum(c["node"]["GuaranteePrice"]["compareData"] or 0 for c in children))
    n["RevenueAmount"] = _ccm(
        cur=sum(c["node"]["RevenueAmount"]["curData"] or 0 for c in children),
        compare=sum(c["node"]["RevenueAmount"]["compareData"] or 0 for c in children))
    n["GuaranteeIncome"] = _ccm(
        cur=sum(c["node"]["GuaranteeIncome"]["curData"] or 0 for c in children),
        compare=sum(c["node"]["GuaranteeIncome"]["compareData"] or 0 for c in children))
    n["RoyaltyIncome"] = _ccm(
        cur=sum(c["node"]["RoyaltyIncome"]["curData"] or 0 for c in children),
        compare=sum(c["node"]["RoyaltyIncome"]["compareData"] or 0 for c in children))
    cur_ci = sum(c["node"]["ConfirmIncome"]["curData"] or 0 for c in children)
    cmp_ci = sum(c["node"]["ConfirmIncome"]["compareData"] or 0 for c in children)
    inc = cur_ci - cmp_ci
    rate = None
    if cur_ci and cmp_ci:
        rate = _round2(Decimal(str(inc)) / Decimal(str(cmp_ci)) * Decimal(100))
    n["ConfirmIncome"] = _ccm(cur=cur_ci, compare=cmp_ci, increase=inc, rate=rate)


# ====================== 主函数 ======================

def get_account_compare(db, start_date: str, end_date: str, serverpart_id: str,
                        compare_start_date: str = "", compare_end_date: str = "",
                        compare_year: int = None, business_type: str = "") -> list:
    """
    C# AccountHelper.GetAccountCompare 完整实现
    返回 List[NestingModel[AccountCompareModel]]
    """
    if not start_date or not end_date or not serverpart_id:
        return []

    # ---- 处理对比日期 ----
    sd = _parse_date(start_date)
    ed = _parse_date(end_date)
    if not sd or not ed:
        return []

    if not compare_start_date or not compare_end_date:
        if compare_year is None:
            return []
        if not compare_start_date:
            compare_start_date = f"{compare_year}/{sd.month:02d}/{sd.day:02d}"
        if not compare_end_date:
            try:
                cmp_ed = ed.replace(year=compare_year)
            except ValueError:
                cmp_ed = ed.replace(year=compare_year, day=28)
            compare_end_date = cmp_ed.strftime("%Y/%m/%d")

    csd = _parse_date(compare_start_date)
    ced = _parse_date(compare_end_date)
    if not csd or not ced:
        return []

    start_ym = sd.strftime("%Y%m")
    end_ym = ed.strftime("%Y%m")
    cmp_start_ym = csd.strftime("%Y%m")
    cmp_end_ym = ced.strftime("%Y%m")

    # ---- 1. 获取服务区列表 ----
    sp_sql = f"""SELECT * FROM T_SERVERPART
        WHERE SERVERPART_ID IN ({serverpart_id})
        ORDER BY SPREGIONTYPE_INDEX, SPREGIONTYPE_ID, SERVERPART_INDEX, SERVERPART_CODE"""
    sp_list = db.execute_query(sp_sql) or []

    # ---- 2. 获取门店列表 ----
    shop_sql = f"""SELECT * FROM T_SERVERPARTSHOP
        WHERE SERVERPART_ID IN ({serverpart_id}) AND ISVALID = 1"""
    shop_list = db.execute_query(shop_sql) or []

    # ---- 3. 获取成本税率 ----
    crt_sql = f"""SELECT * FROM T_SERVERPARTCRT
        WHERE SERVERPART_ID IN ({serverpart_id})"""
    crt_list = db.execute_query(crt_sql) or []

    # ---- 4. 营收数据（两期 UNION ALL）----
    revenue_sql = f"""SELECT
            A.SERVERPART_ID, B.SERVERPARTSHOP_ID, B.SHOPSHORTNAME, B.SELLER_ID, B.SELLER_NAME,
            CASE B.BUSINESS_TYPE WHEN 1000 THEN 4000 WHEN 2000 THEN 1000
                WHEN 3000 THEN 2000 WHEN 4000 THEN 5000 END AS BUSINESS_TYPE,
            SUM(A.CASHPAY) AS REVENUE_AMOUNT, NULL AS BUSINESSPROJECT_ID, 1 AS DATATYPE
        FROM T_ENDACCOUNT_DAILY A, T_SERVERPARTSHOP B
        WHERE A.SERVERPART_ID = B.SERVERPART_ID AND A.SHOPCODE = B.SHOPCODE
            AND A.VALID = 1 AND A.SERVERPART_ID IN ({serverpart_id})
            AND A.STATISTICS_DATE >= TO_DATE('{sd.strftime("%Y/%m/%d")}','YYYY/MM/DD')
            AND A.STATISTICS_DATE < TO_DATE('{ed.strftime("%Y/%m/%d")}','YYYY/MM/DD') + 1
        GROUP BY A.SERVERPART_ID, B.SERVERPARTSHOP_ID, B.SHOPSHORTNAME, B.SELLER_ID, B.SELLER_NAME,
            CASE B.BUSINESS_TYPE WHEN 1000 THEN 4000 WHEN 2000 THEN 1000
                WHEN 3000 THEN 2000 WHEN 4000 THEN 5000 END
        UNION ALL
        SELECT
            A.SERVERPART_ID, B.SERVERPARTSHOP_ID, B.SHOPSHORTNAME, B.SELLER_ID, B.SELLER_NAME,
            CASE B.BUSINESS_TYPE WHEN 1000 THEN 4000 WHEN 2000 THEN 1000
                WHEN 3000 THEN 2000 WHEN 4000 THEN 5000 END AS BUSINESS_TYPE,
            SUM(A.CASHPAY) AS REVENUE_AMOUNT, NULL AS BUSINESSPROJECT_ID, 2 AS DATATYPE
        FROM T_ENDACCOUNT_DAILY A, T_SERVERPARTSHOP B
        WHERE A.SERVERPART_ID = B.SERVERPART_ID AND A.SHOPCODE = B.SHOPCODE
            AND A.VALID = 1 AND A.SERVERPART_ID IN ({serverpart_id})
            AND A.STATISTICS_DATE >= TO_DATE('{csd.strftime("%Y/%m/%d")}','YYYY/MM/DD')
            AND A.STATISTICS_DATE < TO_DATE('{ced.strftime("%Y/%m/%d")}','YYYY/MM/DD') + 1
        GROUP BY A.SERVERPART_ID, B.SERVERPARTSHOP_ID, B.SHOPSHORTNAME, B.SELLER_ID, B.SELLER_NAME,
            CASE B.BUSINESS_TYPE WHEN 1000 THEN 4000 WHEN 2000 THEN 1000
                WHEN 3000 THEN 2000 WHEN 4000 THEN 5000 END"""
    revenue_data = db.execute_query(revenue_sql) or []

    # ---- 5. 经营项目数据（两期 UNION ALL）----
    project_sql = f"""SELECT
            A.BUSINESSPROJECT_ID, A.BUSINESSPROJECT_NAME, A.SERVERPARTSHOP_ID, A.SERVERPARTSHOP_NAME,
            A.BUSINESS_TYPE, A.MERCHANTS_ID, A.MERCHANTS_NAME, B.SHOPROYALTY_ID, D.SERVERPART_ID,
            A.CLOSED_DATE, E.DECORATE_STARTDATE, E.DECORATE_ENDDATE,
            MIN(B.STARTDATE) AS STARTDATE, MAX(B.ENDDATE) AS ENDDATE, 1 AS DATATYPE
        FROM T_BUSINESSPROJECT A, T_BIZPSPLITMONTH B, T_REGISTERCOMPACT C,
             T_RTREGISTERCOMPACT D, T_REGISTERCOMPACTSUB E
        WHERE A.BUSINESSPROJECT_ID = B.BUSINESSPROJECT_ID
            AND B.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
            AND B.REGISTERCOMPACT_ID = D.REGISTERCOMPACT_ID
            AND B.REGISTERCOMPACT_ID = E.REGISTERCOMPACT_ID
            AND A.PROJECT_VALID = 1 AND C.COMPACT_TYPE IN (340001)
            AND B.BIZPSPLITMONTH_STATE = 1 AND B.ACCOUNT_TYPE = 1000
            AND A.SERVERPARTSHOP_ID IS NOT NULL AND D.SERVERPART_ID IN ({serverpart_id})
            AND B.STATISTICS_MONTH BETWEEN {start_ym} AND {end_ym}
        GROUP BY A.BUSINESSPROJECT_ID, A.BUSINESSPROJECT_NAME, A.SERVERPARTSHOP_ID, A.SERVERPARTSHOP_NAME,
            A.MERCHANTS_ID, A.MERCHANTS_NAME, A.BUSINESS_TYPE, A.CLOSED_DATE,
            B.SHOPROYALTY_ID, E.DECORATE_STARTDATE, E.DECORATE_ENDDATE, D.SERVERPART_ID
        UNION ALL
        SELECT
            A.BUSINESSPROJECT_ID, A.BUSINESSPROJECT_NAME, A.SERVERPARTSHOP_ID, A.SERVERPARTSHOP_NAME,
            A.BUSINESS_TYPE, A.MERCHANTS_ID, A.MERCHANTS_NAME, B.SHOPROYALTY_ID, D.SERVERPART_ID,
            A.CLOSED_DATE, E.DECORATE_STARTDATE, E.DECORATE_ENDDATE,
            MIN(B.STARTDATE) AS STARTDATE, MAX(B.ENDDATE) AS ENDDATE, 2 AS DATATYPE
        FROM T_BUSINESSPROJECT A, T_BIZPSPLITMONTH B, T_REGISTERCOMPACT C,
             T_RTREGISTERCOMPACT D, T_REGISTERCOMPACTSUB E
        WHERE A.BUSINESSPROJECT_ID = B.BUSINESSPROJECT_ID
            AND B.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
            AND B.REGISTERCOMPACT_ID = D.REGISTERCOMPACT_ID
            AND B.REGISTERCOMPACT_ID = E.REGISTERCOMPACT_ID
            AND A.PROJECT_VALID = 1 AND C.COMPACT_TYPE IN (340001)
            AND B.BIZPSPLITMONTH_STATE = 1 AND B.ACCOUNT_TYPE = 1000
            AND A.SERVERPARTSHOP_ID IS NOT NULL AND D.SERVERPART_ID IN ({serverpart_id})
            AND B.STATISTICS_MONTH BETWEEN {cmp_start_ym} AND {cmp_end_ym}
        GROUP BY A.BUSINESSPROJECT_ID, A.BUSINESSPROJECT_NAME, A.SERVERPARTSHOP_ID, A.SERVERPARTSHOP_NAME,
            A.MERCHANTS_ID, A.MERCHANTS_NAME, A.BUSINESS_TYPE, A.CLOSED_DATE,
            B.SHOPROYALTY_ID, E.DECORATE_STARTDATE, E.DECORATE_ENDDATE, D.SERVERPART_ID"""
    project_data = db.execute_query(project_sql) or []

    # ---- 6. 遍历营收数据，更新门店所属经营项目 ----
    # C# 逻辑: 按项目分组遍历，给每条营收记录标记 BUSINESSPROJECT_ID
    shop_id_used = set()
    compare_shop_id_used = set()
    proj_bp_ids = list({str(p.get("BUSINESSPROJECT_ID"))
                        for p in project_data})

    for bp_id_str in proj_bp_ids:
        proj_rows = [p for p in project_data if str(p.get("BUSINESSPROJECT_ID")) == bp_id_str]
        if not proj_rows:
            continue
        # 取最新 ENDDATE 的那条
        proj_rows.sort(key=lambda x: -((_try_date(x.get("ENDDATE")) or datetime(2000, 1, 1)).timestamp()))

        for dt_val in [1, 2]:
            dt_proj = [p for p in proj_rows if _try_int(p.get("DATATYPE")) == dt_val]
            if not dt_proj:
                continue
            dr_project = dt_proj[0]
            shop_ids_in_proj = str(dr_project.get("SERVERPARTSHOP_ID") or "")

            for rev in revenue_data:
                rev_shop = str(rev.get("SERVERPARTSHOP_ID") or "")
                rev_dt = _try_int(rev.get("DATATYPE"))
                if rev_shop not in shop_ids_in_proj.split(","):
                    continue
                if rev_dt != dt_val:
                    continue

                used_set = shop_id_used if dt_val == 1 else compare_shop_id_used
                if rev_shop not in used_set:
                    used_set.add(rev_shop)
                    rev["BUSINESS_TYPE"] = dr_project.get("BUSINESS_TYPE")
                    rev["SELLER_ID"] = dr_project.get("MERCHANTS_ID")
                    rev["SELLER_NAME"] = dr_project.get("MERCHANTS_NAME")
                    rev["BUSINESSPROJECT_ID"] = dr_project.get("BUSINESSPROJECT_ID")
                else:
                    existing = str(rev.get("BUSINESSPROJECT_ID") or "")
                    if existing:
                        rev["BUSINESSPROJECT_ID"] = existing + "," + str(dr_project.get("BUSINESSPROJECT_ID"))
                    else:
                        rev["BUSINESSPROJECT_ID"] = dr_project.get("BUSINESSPROJECT_ID")

    # ---- 6b. 获取应收拆分数据 ----
    all_bp_ids = list({str(p.get("BUSINESSPROJECT_ID")) for p in project_data})
    shoproyalty_list = []
    if all_bp_ids:
        bp_str = ",".join(all_bp_ids)
        sr_sql = f"""SELECT * FROM T_SHOPROYALTY
            WHERE BUSINESSPROJECT_ID IN ({bp_str})"""
        shoproyalty_list = db.execute_query(sr_sql) or []

    royalty_detail_list = []
    all_sr_ids = list({str(p.get("SHOPROYALTY_ID")) for p in project_data
                       if p.get("SHOPROYALTY_ID")})
    if all_sr_ids:
        sr_str = ",".join(all_sr_ids)
        rd_sql = f"""SELECT * FROM T_SHOPROYALTYDETAIL
            WHERE SHOPROYALTY_ID IN ({sr_str})"""
        royalty_detail_list = db.execute_query(rd_sql) or []

    # ---- 7. 经营模式过滤 ----
    if business_type:
        bt_set = set(business_type.split(","))
        revenue_data = [r for r in revenue_data if str(r.get("BUSINESS_TYPE")) in bt_set]
        project_data = [p for p in project_data if str(p.get("BUSINESS_TYPE")) in bt_set]

    if not revenue_data and not project_data:
        return []

    # ---- 8. 构建树形结构 ----
    summary_node = _node({"SPRegionTypeName": "总计"})

    # 按片区分组（排除 SPREGIONTYPE_ID=89）
    region_ids = []
    seen_regions = set()
    for sp in sp_list:
        rid = sp.get("SPREGIONTYPE_ID")
        if rid is not None and _try_int(rid) != 89 and rid not in seen_regions:
            seen_regions.add(rid)
            region_ids.append(rid)

    for region_id in region_ids:
        region_sps = [sp for sp in sp_list if sp.get("SPREGIONTYPE_ID") == region_id]
        if not region_sps:
            continue
        region_name = str(region_sps[0].get("SPREGIONTYPE_NAME") or "")

        region_node = _node({
            "SPRegionTypeId": region_id,
            "SPRegionTypeName": region_name,
        })

        for sp in region_sps:
            sp_id = _try_int(sp.get("SERVERPART_ID"))
            # 查税率
            tax_rate = 9
            for crt in crt_list:
                if _try_int(crt.get("SERVERPART_ID")) == sp_id and crt.get("ACCOUNTTAX") is not None:
                    tax_rate = crt.get("ACCOUNTTAX")
                    break

            sp_node = _node({
                "SPRegionTypeId": region_id,
                "SPRegionTypeName": region_name,
                "ServerpartId": sp_id,
                "ServerpartName": str(sp.get("SERVERPART_NAME") or ""),
                "TaxRate": tax_rate,
            })

            _bind_sp_account_compare(
                sp_node, sd, ed, csd, ced,
                revenue_data, project_data, shop_list,
                shoproyalty_list, royalty_detail_list)

            if sp_node["children"]:
                region_node["children"].append(sp_node)

        if region_node["children"]:
            _aggregate_node(region_node)
            summary_node["children"].append(region_node)

    # 无片区的服务区
    null_region_sps = [sp for sp in sp_list if sp.get("SPREGIONTYPE_ID") is None]
    for sp in null_region_sps:
        sp_id = _try_int(sp.get("SERVERPART_ID"))
        tax_rate = 9
        for crt in crt_list:
            if _try_int(crt.get("SERVERPART_ID")) == sp_id and crt.get("ACCOUNTTAX") is not None:
                tax_rate = crt.get("ACCOUNTTAX")
                break

        sp_node = _node({
            "ServerpartId": sp_id,
            "ServerpartName": str(sp.get("SERVERPART_NAME") or ""),
            "TaxRate": tax_rate,
        })

        _bind_sp_account_compare(
            sp_node, sd, ed, csd, ced,
            revenue_data, project_data, shop_list,
            shoproyalty_list, royalty_detail_list)

        if sp_node["children"]:
            summary_node["children"].append(sp_node)

    # ---- 9. 汇总根节点 ----
    _aggregate_node(summary_node)

    return [summary_node]
