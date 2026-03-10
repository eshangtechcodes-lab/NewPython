# 动态对比问题清单（最新四窗口联调结果）

- 生成时间：2026-03-10 15:30
- 数据来源：
  - [dynamic_compare_master_report_20260310.md](/E:/workfile/JAVA/NewAPI/docs/dynamic_compare_master_report_20260310.md)
  - [window_1_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_1_dynamic_compare_report.json)
  - [window_2_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_2_dynamic_compare_report.json)
  - [window_3_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_3_dynamic_compare_report.json)
  - [window_4_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_4_dynamic_compare_report.json)

## 1. 总体结果

- 总用例数：`329`
- 通过：`14`
- 失败：`315`
- 跳过：`0`

窗口分布：

| 窗口 | PASS | FAIL | TOTAL | 说明 |
| --- | --- | --- | --- | --- |
| `window_1` | 14 | 113 | 127 | BaseInfo / Merchants / Contract 主链仍是高风险区 |
| `window_2` | 0 | 115 | 115 | Finance / Revenue / BigData / MobilePay / Budget 全量失败 |
| `window_3` | 0 | 86 | 86 | Analysis / Audit / Verification 主体仍未打通 |
| `window_4` | 0 | 1 | 1 | Picture 当前唯一可执行接口仍失败 |

## 2. 问题分类总览

按失败首因归类后，当前问题清单如下：

| 问题分类 | 数量 | 说明 |
| --- | --- | --- |
| `新 API 超时` | 78 | Python 接口 20 秒内未返回，字段级对比无法进行 |
| `字段类型映射差异` | 60 | `float/int`、`空串/null`、日期格式等和 C# 不一致 |
| `HTTP 状态码不一致` | 57 | 常见于旧接口 `404/500`、新接口 `200/405` |
| `字段缺失` | 50 | 新接口缺少旧接口已返回字段 |
| `树结构/列表差异` | 41 | `children`、列表长度、树节点层级、递归装配不一致 |
| `响应包装漂移` | 16 | `Message` 与 `Result_Code/Result_Data/Result_Desc` 混用 |
| `空参/校验口径漂移` | 7 | 同样入参下，旧接口报错、新接口成功或报错原因不同 |
| `字段值映射差异` | 4 | 统计值、枚举值、日期值等结果不同 |
| `原 API 超时` | 2 | 旧接口基线不稳定，不能直接归咎于 Python |

高频差异字段/信号：

- `Result_Desc`：`80`
- `新 API 调用失败`：`78`
- `<root>.Result_Code`：`57`
- `<root>.Result_Desc`：`57`
- `Result_Data`：`57`
- `<root>.Result_Data`：`56`
- `<root>.Message`：`49`
- `Message`：`26`
- `Result_Data.List`：`21`
- `Result_Data.TotalCount`：`16`
- `Result_Data.StaticsModel`：`14`

## 3. 模块问题分布

按失败用例数看，当前最需要优先处理的模块是：

| 模块 | FAIL | 说明 |
| --- | --- | --- |
| `BusinessProject` | 48 | window_1 主体失败来源，状态码/缺字段/超时并存 |
| `BaseInfo` | 47 | 树结构、字段缺失、超时混杂 |
| `Revenue` | 43 | window_2 最大失败源，包装漂移与超时并存 |
| `Analysis` | 31 | window_3 最大失败源，超时和类型差异明显 |
| `Finance` | 26 | 404/200、包装漂移、字段差异并存 |
| `Audit` | 17 | window_3 主链尚未打通 |
| `Merchants` | 16 | window_1/3 都有问题，既有字段差异也有状态码问题 |
| `BigData` | 15 | 多为包装漂移、状态码不一致 |
| `MobilePay` | 14 | 参数校验和状态码口径差异明显 |
| `Budget` | 11 | window_2 新增高失败簇，当前全部失败 |

## 4. 各窗口问题清单

### 4.1 `window_1`

主问题：

- `新 API 超时`：`26`
- `字段缺失`：`36`
- `树结构/列表差异`：`22`
- `字段类型映射差异`：`19`

代表性问题：

- `BaseInfo/BindingOwnerUnitTree`
  - `children` 类型不一致，旧接口是空列表，新接口是 `None`
- `BaseInfo/GetAUTOSTATISTICSDetail`
  - 缺字段：`INELASTIC_DEMAND`
- `BaseInfo/GetBrandList`
  - 缺字段：`MerchantID_Encrypt`
- `BaseInfo/GetCASHWORKERDetail`
  - 新 API 超时
- `BaseInfo/GetSPRegionShopTree`
  - 树节点 `desc` 缺失
- `BaseInfo/GetServerPartShopNewDetail`
  - `BusinessEndDate` 值不一致
- `Commodity/GetCOMMODITYList`
  - `COMMODITY_CURRPRICE` 类型不一致
- `Merchants/GetRTCoopMerchantsList`
  - 顶层返回壳不一致，旧接口 `Message` 口径与新接口 `Result_*` 口径冲突
- `BusinessProject/GetAccountWarningListSummary`
  - 统计值不一致

结论：

- `window_1` 不是单一问题，已经分裂成 4 类问题并行存在：
  - 树接口回迁不完整
  - 详情/List 字段缺失
  - 类型/空值格式不一致
  - 大量详情/List 超时

### 4.2 `window_2`

主问题：

- `HTTP 状态码不一致`：`33`
- `新 API 超时`：`26`
- `字段类型映射差异`：`17`
- `字段缺失`：`14`
- `响应包装漂移`：`9`

代表性问题：

- `Finance/GetATTACHMENTDetail`
  - 旧接口 `404`，新接口 `200`
  - 旧接口仅 `Message`，新接口多出 `Result_Code/Result_Data/Result_Desc`
- `Revenue/GetBUSINESSANALYSISList`
  - 新接口多出 `Message`
  - `Result_Desc` 从旧接口的业务异常文案变成了“请求参数校验失败”
- `Budget/*`
  - 预算模块当前整簇失败，说明 Budget 路由链路还未对齐
- `Revenue/*`
  - 是当前 window_2 最大失败源，超时、缺字段、状态码漂移同时存在
- `BigData/*`
  - 主要是包装层和错误分支不一致
- `MobilePay/*`
  - 空参/缺参时新旧接口行为差异明显

结论：

- `window_2` 的第一优先级不是字段，而是：
  - 路由/状态码
  - 包装壳
  - 参数校验口径
  - Revenue 慢查询

### 4.3 `window_3`

主问题：

- `新 API 超时`：`26`
- `字段类型映射差异`：`24`
- `HTTP 状态码不一致`：`16`
- `响应包装漂移`：`7`
- `树结构/列表差异`：`8`
- `原 API 超时`：`2`

代表性问题：

- `Analysis/GetANALYSISINSDetail`
  - 已给真实入参 `ANALYSISINSId=1805`
  - 新 API 仍超时
- `Audit/*`
  - 前 8 条连续失败，说明 Audit 主链未打通
- `Verification/GetEndaccountList`
  - 原 API 超时，新 API 返回 `405`
  - 这是基线问题，不应直接算 Python 缺陷
- `Analysis/*`
  - 是 window_3 最大失败簇，超时和类型差异并存

结论：

- `window_3` 当前最应该先清 `Analysis + Audit`。
- `Verification` 里存在旧接口基线不稳定项，要隔离处理。

### 4.4 `window_4`

主问题：

- `Picture/GetPictureList`
  - 旧接口：`404`
  - 新接口：`405`
  - 旧接口顶层：`Message`
  - 新接口顶层：`detail`

结论：

- 这不是字段问题，是典型的“FastAPI 默认错误响应”未按旧接口契约包装。

## 5. 当前最明确的问题清单

可以直接作为整改入口的问题有这些：

1. 大量接口仍然在 `localhost:8080` 侧超时，首批需处理 `BaseInfo`、`Revenue`、`Analysis`、`Audit`。
2. 新旧接口错误分支口径不一致，典型表现是旧接口只有 `Message`，新接口却返回 `Result_Code/Result_Data/Result_Desc` 或 `detail`。
3. DTO/序列化映射不完整，缺失字段高频集中在 `BaseInfo`、`BusinessProject`、`Revenue`。
4. 空值和数值类型处理不一致，常见是：
   - `float -> int`
   - `'' -> null`
   - 日期格式从 `yyyy/M/d` 变成 ISO 字符串
5. 树接口装配逻辑与 C# 不一致，常见是：
   - `children` 从 `[]` 变成 `None`
   - 节点层级被展开或截断
   - `desc`、`node` 子字段丢失
6. 一部分接口是“旧接口本身不稳定”，例如 `Verification/GetEndaccountList`，这类要隔离，不应直接驱动 Python 代码修改。

## 6. 建议的整改顺序

1. 先修所有 `新 API 超时` 接口，否则后续字段比对没有意义。
2. 再统一修错误分支包装，解决 `Message / Result_* / detail` 三套壳混用问题。
3. 再按模块修字段缺失、树结构差异、类型差异：
   - 第一组：`BaseInfo`、`BusinessProject`
   - 第二组：`Revenue`、`Finance`
   - 第三组：`Analysis`、`Audit`
4. 最后单独隔离 `原 API 超时/基线异常` 接口。

## 7. 相关输出物

- 总汇总报告：[dynamic_compare_master_report_20260310.md](/E:/workfile/JAVA/NewAPI/docs/dynamic_compare_master_report_20260310.md)
- window_1 接口级整改清单：[window_1_interface_rectification_plan_20260310.md](/E:/workfile/JAVA/NewAPI/docs/window_1_interface_rectification_plan_20260310.md)

如果下一步要继续拆给其他 AI，建议按模块继续产出：

- `window_2_interface_rectification_plan_20260310.md`
- `window_3_interface_rectification_plan_20260310.md`
- `window_4_interface_rectification_plan_20260310.md`
