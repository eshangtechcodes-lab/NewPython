# 已完成接口一致性审计

> 审计时间：2026-03-09
>
> 审计范围：当前 FastAPI 运行时已注册的 `/EShangApiMain/*` 路由，与原 C# 手写 Controller 中的对应接口进行静态匹配核查。
>
> 审计方式：代码级静态比对，不包含真实请求联调。

## 1. 审计结论

结论：**当前项目已实现接口与原 C# 接口不完全一致，而且存在较多“确定性不兼容项”**。

本次核查得到的核心数字如下：

- FastAPI 运行时路由：628 个
- 能在原 C# Controller 中匹配到的对应路由：621 个
- Python 独有、在原 C# 中不存在的路由：7 个
- HTTP 方法不一致：62 个
- Header 处理不一致：103 个
- 查询参数名/参数结构不一致：171 个
- 响应包结构明显不一致（直接返回 `code/message/data`）：192 个

## 2. 最高优先级问题

### P0. 响应包结构大面积不兼容

原项目标准响应字段是：

- `Result_Code`
- `Result_Desc`
- `Result_Data`

但当前有 **192 个接口** 直接返回：

- `code`
- `message`
- `data`

这不是风格问题，而是接口契约变化。

问题集中在：

- `routers/eshang_api_main/batch_modules/batch_router_part1.py`
- `routers/eshang_api_main/batch_modules/batch_router_part2.py`
- `routers/eshang_api_main/bigdata/bigdata_router.py` 中的散装接口

典型例子：

- `Audit/GetYSABNORMALITYList`
- `Analysis/GetANALYSISINSList`
- `MobilePay/GetKwyRoyaltyRate`
- `Verification/GetEndaccountList`
- `Sales/GetCOMMODITYSALEList`
- `Picture/GetPictureList`
- `BigData/A2305052305180725`

### P0. Picture 模块与原 C# 路由集合不一致

当前 Python `Picture` 前缀下 9 个接口中，仅有 3 个和原 C# 路由对上，另外 6 个是 Python 独有路由，原 C# 中不存在。

Python 独有：

- `Picture/BatchDeletePicture`
- `Picture/GetPictureByShop`
- `Picture/GetPictureCount`
- `Picture/GetPictureDetail`
- `Picture/GetPictureTypeList`
- `Picture/SynchroPicture`

原 C# 存在但 Python 未实现：

- `Picture/DeleteMultiPicture`
- `Picture/GetAuditEvidence`
- `Picture/GetEndaccountEvidence`
- `Picture/SaveImgFile`
- `Picture/UploadAuditEvidence`
- `Picture/UploadEndaccountEvidence`

这说明当前 `Picture` 模块不是“平移”，而是被替换成了另一套接口集合。

### P0. 动态批量路由大量使用泛化参数名，和原接口参数名不一致

在 `batch_router_part2.py` 中，很多 Detail/Delete 类接口使用了统一参数名：

- `pk_val`

而原 C# 使用的是实体专属参数名，例如：

- `ANALYSISINSId`
- `SupplierId`
- `QualificationId`
- `ENDACCOUNTId`

这会直接导致原调用方按旧参数名请求时无法兼容。

典型例子：

- `Analysis/GetANALYSISINSDetail`
- `Supplier/GetSupplierDetail`
- `Supplier/DeleteSupplier`
- `Verification/DeleteENDACCOUNT`

## 3. 重要不一致分类

### 3.1 HTTP 方法不一致

共发现 **62 个**。

高发模块：

- Audit：12 个
- Revenue：11 个
- Analysis：11 个
- Sales：8 个
- Verification：5 个

典型例子：

- `Analysis/DeleteANALYSISINS`
  - C#：`GET+POST`
  - Python：`POST`
- `Audit/GetAuditList`
  - C#：`GET+POST`
  - Python：`POST`
- `Audit/GetCheckAccountReport`
  - C#：`GET`
  - Python：`POST`
- `Revenue/GetBusinessAnalysisReport`
  - C#：`GET`
  - Python：`POST`
- `BaseInfo/GetServerpartShopDetail`
  - C#：`GET`
  - Python：`GET+POST`
- `BaseInfo/DelServerpartShop`
  - C#：`POST`
  - Python：`GET+POST`

### 3.2 Header 处理缺失或不一致

共发现 **103 个**。

高发模块：

- BaseInfo：21 个
- Revenue：15 个
- BusinessProject：15 个
- Verification：9 个
- Finance：8 个
- Contract：8 个

典型缺失类型：

- 原 C# 使用 `GetIntHeader("ProvinceCode", ...)`，Python 未读取
- 原 C# 使用 `GetStringHeader("ServerpartCodes", ...)`，Python 未读取
- 原 C# 使用 `GetStringHeader("ServerpartShopIds", ...)`，Python 未读取
- 原 C# 使用 `GetStringHeader("Token", ...)`，Python 未读取

典型例子：

- `BaseInfo/GetSERVERPARTList`
- `BaseInfo/GetCASHWORKERList`
- `Contract/GetRegisterCompactList`
- `BusinessProject/GetPROJECTWARNINGList`
- `Finance/ApprovePeriodAccount`
- `Revenue/GetRevenueReport`
- `Verification/GetDataVerificationList`

### 3.3 参数结构/参数名不一致

共发现 **171 个**。

高发模块：

- Analysis：32 个
- Revenue：25 个
- BusinessProject：15 个
- Verification：14 个
- BaseInfo：14 个

典型问题：

- 原 C# 是多个 Query 参数，Python 变成 `search_model: dict`
- 原 C# 的参数名保留业务语义，Python 变成 `pk_val`
- 原 C# 是 ID 查询，Python 改成了另一组业务参数

典型例子：

- `Verification/GetENDACCOUNTModel`
  - C# 参数：`ENDACCOUNTId`
  - Python 参数：`ServerpartShopId`, `StatisticsDate`
- `Verification/GetEndAccountData`
  - C# 参数：`Data_Type`, `Endaccount_ID`, `CigaretteType`, `ReloadType`
  - Python 参数：`ServerpartShopId`, `StatisticsDate`
- `Revenue/GetTransactionCustomer`
  - C#：多组显式 Query 参数
  - Python：未保留同名参数接口形式
- `Sales/GetEndaccountSaleInfo`
  - C#：`ServerpartCode`, `ServerpartShopCode`, `MachineCode`, `EndaccountDate`
  - Python：改为 `search_model: dict`

## 4. 模块级差异摘要

### 4.1 已实现但仍有明显偏差的模块

- `Picture`
  - 路由集合已偏离原项目
- `Analysis`
  - 4 个加密接口未做，且其余 58 个里存在大量响应包、方法、参数名不一致
- `Audit`
  - 路由数量对上，但方法和响应包不一致较多
- `Verification` / `Sales`
  - 路由数量对上，但参数结构与 Header 处理差异明显
- `Revenue`
  - 路由数量对上，但仍有较多 GET/POST 方式和参数结构差异

### 4.2 与原项目集合不完全对齐的已完结前缀

- `Picture`
  - 3 个匹配，6 个替换
- `Supplier`
  - 多出 `Supplier/DeleteQUALIFICATION_HIS`
- `BigData`
  - 少了 `DeleteBAYONETWARNING` / `GetBAYONETWARNINGDetail` / `SynchroBAYONETWARNING`

## 5. 优先修复顺序建议

### 第一批：先修接口契约

1. 修正所有 `code/message/data` 响应为 `Result_Code/Result_Desc/Result_Data`
2. 修正所有 GET/POST 方法不一致项
3. 修正所有使用 `pk_val` 的动态路由参数名

### 第二批：补齐权限和上下文逻辑

1. 系统性补 Header 读取
2. 逐模块核对 `ProvinceCode` / `ServerpartCodes` / `ServerpartShopIds` / `Token` / `UserPattern`

### 第三批：补 Picture 和少量路由集合偏差

1. 按原 C# 路由恢复 `Picture` 模块真实接口集合
2. 清理 Python 独有但原 C# 不存在的 Picture 路由
3. 处理 `Supplier/DeleteQUALIFICATION_HIS` 这类集合漂移项

### 第四批：再做服务层深比对

在接口契约修正后，再逐模块深入核对：

- SQL 是否一致
- 默认分页是否一致
- 默认排序是否一致
- 删除方式是否一致
- 返回字段是否一致

否则当前先做深层业务比对，容易被上层接口契约差异干扰。

## 6. 备注

本次结果是**静态代码审计结论**，已经足够证明“当前并非完全一致”。

若要继续做下一层验证，建议在接口契约修正后执行：

1. 真请求对比
2. 3 组参数回归
3. 字段值级差异校验
4. 关键 SQL 语义核查
