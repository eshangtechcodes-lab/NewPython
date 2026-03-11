# 代码修改记录

## 2026-03-05

### [GetServerpartShopInfo] Service 驼峰命名映射
- **文件**: `services/base_info/base_info_misc_service.py` (L105-159)
- **修改内容**: 
  - 将 `SELECT *` 的原始返回改为手动映射 19 个驼峰字段的 `ServerpartShopModel`
  - SQL 增加 `B.OWNERUNIT_NAME` 关联字段
  - 添加品牌图标查询逻辑: 通过 `T_BRAND.BRAND_INTRO` 拼接完整 URL
- **原因**: 原 C# 返回 `ServerpartShopModel` 使用驼峰命名，直接 `SELECT *` 返回全大写不匹配

### [GetServerpartDDL] 添加省份映射辅助函数
- **文件**: `services/base_info/base_info_misc_service.py` (L162-178)
- **修改内容**: 新增 `_get_province_id_by_code()` 函数
- **逻辑**: `T_FIELDEXPLAIN`(DIVISION_CODE) → `T_FIELDENUM`(VALUE=省份编码) → `FIELDENUM_ID`
- **原因**: 原 C# 通过 `DictionaryHelper.GetFieldEnum("DIVISION_CODE", ProvinceCode)` 获取内码

### [GetServerpartDDL] 修正 Router 返回结构
- **文件**: `routers/eshang_api_main/base_info/base_info_misc_router.py` (L120-135)
- **修改内容**: `Result_Data` 从直接返回数组改为嵌套 `{PageIndex, PageSize, TotalCount, List}`
- **原因**: 原 C# 返回 `JsonMsg<JsonList<CommonModel>>` 嵌套结构，直接返回数组与原 API 不一致

### [数据库] 同步字典表到达梦
- **文件**: `scripts/server_migrate.py` (L48-51)
- **修改内容**: `MIGRATE_TABLES` 新增:
  - `{"oracle_schema": "PLATFORM_DICTIONARY", "table": "T_FIELDEXPLAIN", "sequence": "SEQ_FIELDEXPLAIN"}`
  - `{"oracle_schema": "PLATFORM_DICTIONARY", "table": "T_FIELDENUM", "sequence": "SEQ_FIELDENUM"}`
- **原因**: `GetServerpartDDL` 的省份编码映射依赖字典表数据

### [GetServerpartTree] 重写 Service 逻辑
- **文件**: `services/base_info/base_info_misc_service.py` (L228-370)
- **修改内容**:
  - 重写 `get_serverpart_tree()` 函数，严格按原 C# Helper L405-658 逻辑实现
  - 区域表 `T_SERVERPARTTYPE` 用原始 `ProvinceCode`（如 340000）查询
  - 服务区表 `T_SERVERPART` 用 SQL 子查询映射 `PROVINCE_CODE = (SELECT FIELDENUM_ID...)`
  - 补全 `desc`、`ico`、`children` 字段
  - 用 `assigned_sp_ids` 集合跟踪无归属服务区
  - 支持 `ShowRoyalty` 模式（JOIN T_SERVERPARTSHOP 统计门店数）
- **原因**: 原有实现存在多个问题：硬编码 STATISTICS_TYPE、缺少字段、省份映射方式错误

### [GetServerpartTree] 修正 Router 返回结构
- **文件**: `routers/eshang_api_main/base_info/base_info_misc_router.py` (L167-177)
- **修改内容**: `Result_Data` 从直接返回数组改为嵌套 `{PageIndex, PageSize, TotalCount, List}`
- **原因**: 与 `GetServerpartDDL` 相同，原 C# 返回 `JsonMsg<JsonList<CommonTypeTreeModel>>`

### [省份映射] 辅助函数改为 SQL 子查询
- **文件**: `services/base_info/base_info_misc_service.py` (L166-178)
- **修改内容**: `_get_province_id_by_code()` 的 JOIN + ROWNUM SQL 在 API 运行时返回空值。`get_serverpart_tree` 改为直接在 WHERE 中嵌入子查询
- **原因**: 辅助函数独立测试正常但在 API 运行时通过 `DatabaseHelper` 返回空值，可能与达梦 JOIN 行为差异相关

## 2026-03-06

### [GetSPRegionShopTree] 新增 Service 函数
- **文件**: `services/base_info/base_info_misc_service.py` (L985-1254)
- **修改内容**: 新增 `get_sp_region_shop_tree()` + `_bing_serverpart_shop_tree()` 两个函数
- **逻辑**: JOIN `T_SERVERPART A, T_SERVERPARTSHOP B`，构建区域(type=0)→服务区(type=1)→门店(type=2) 三级嵌套树
- **原因**: 迁移原 `ServerpartShopHelper.GetSPRegionShopTree` (L1330-1488) + `BingServerpartShopTree` (L1585-1666)

### [GetSPRegionShopTree] 修正 Router 返回结构
- **文件**: `routers/eshang_api_main/base_info/base_info_misc_router.py` (L222-231)
- **修改内容**: `Result_Data` 从直接返回数组改为嵌套 `{PageIndex, PageSize, TotalCount, List}`
- **原因**: 原 C# 返回 `JsonMsg<JsonList<NestingModel<CommonTypeTreeModel>>>`

### [GetServerpartShopDDL] 新增 Service 函数
- **文件**: `services/base_info/base_info_misc_service.py` (L985-1038)
- **修改内容**: 新增 `get_serverpart_shop_ddl()` 函数
- **逻辑**: 单表查 `T_SERVERPARTSHOP WHERE ISVALID = 1`，排序 5 字段，返回 `{label=SHOPNAME, value=SERVERPARTSHOP_ID(str)}`
- **原因**: 迁移原 `ServerpartShopHelper.GetServerpartShopDDL` (L1031-1065)

### [GetServerpartShopDDL] 修正 Router 返回结构
- **文件**: `routers/eshang_api_main/base_info/base_info_misc_router.py` (L263-272)
- **修改内容**: `Result_Data` 从直接返回数组改为嵌套 `{PageIndex, PageSize, TotalCount, List}`
- **原因**: 原 C# 返回 `JsonMsg<JsonList<CommonModel>>`

### [GetServerpartShopTree] 新增 Service 函数
- **文件**: `services/base_info/base_info_misc_service.py` (L1041-1118)
- **修改内容**: 新增 `get_serverpart_shop_tree()` 函数，复用 `_bing_serverpart_shop_tree`
- **逻辑**: 与 `GetSPRegionShopTree` 类似但无区域层，直接返回服务区→门店二级树
- **原因**: 迁移原 `ServerpartShopHelper.GetServerpartShopTree` (L1504-1569)

### [GetServerpartShopTree] 修正 Router 返回结构
- **文件**: `routers/eshang_api_main/base_info/base_info_misc_router.py` (L310-319)
- **修改内容**: `Result_Data` 从直接返回改为嵌套 `{PageIndex, PageSize, TotalCount, List}`
- **原因**: 原 C# 返回 `JsonMsg<JsonList<NestingModel<CommonTypeTreeModel>>>`

### [GetNestingOwnerUnitList] 新增 Service 函数
- **文件**: `services/base_info/base_info_misc_service.py` (L1120-1251)
- **修改内容**: 新增 `get_nesting_ownerunit_list()` + `_bind_ownerunit_data()` + `_ownerunit_row_to_model()` 3个函数
- **逻辑**: 查 `T_OWNERUNIT` 单表，按 OWNERUNIT_PID 递归构建父子嵌套树，支持模糊查询过滤
- **原因**: 迁移原 `OwnerUnitHelper.GetNestingOwnerUnitList` (L528-585) + `BinData` (L594-624)

### [GetNestingOwnerUnitList] 修正 Router 返回结构
- **文件**: `routers/eshang_api_main/base_info/base_info_misc_router.py`
- **修改内容**: `Result_Data` 修正为嵌套 `{PageIndex, PageSize, TotalCount, List}`
- **原因**: 原 C# 返回 `JsonMsg<JsonList<NestingModel<OWNERUNITModel>>>`

### [BindingOwnerUnitDDL] 新增 Service 函数
- **文件**: `services/base_info/base_info_misc_service.py` (L1253-1305)
- **修改内容**: 新增 `binding_ownerunit_ddl()` 函数
- **逻辑**: WHERE PID=-1 AND NATURE=1000，DataType 决定 value 字段，ico 带 URL 前缀
- **原因**: 迁移原 `OwnerUnitHelper.BindingOwnerUnitDDL` (L635-664)

### [BindingOwnerUnitDDL] 修正 Router 返回结构
- **文件**: `routers/eshang_api_main/base_info/base_info_misc_router.py`
- **修改内容**: `Result_Data` 修正为嵌套 `{PageIndex, PageSize, TotalCount, List}`
- **原因**: 原 C# 返回 `JsonMsg<JsonList<CommonTypeModel>>`

### [BindingOwnerUnitTree] 新增 Service 函数
- **文件**: `services/base_info/base_info_misc_service.py`
- **修改内容**: 新增 `binding_ownerunit_tree()` + `_bind_child_ownerunit()` + `_build_ownerunit_common_type_node()` 3 个函数
- **逻辑**: 查 T_OWNERUNIT WHERE NATURE=1000，递归构建 CommonTypeModel 嵌套树
- **关键修复**: 递归 PID 用 `value`(DataType 决定) 而非 `OWNERUNIT_ID`，与原 C# `OwnerUnitModel.value.TryParseToInt()` 一致
- **原因**: 迁移原 `OwnerUnitHelper.BindingOwnerUnitTree` (L677-740) + `BindChildOwnerUnit` (L750-803)

### [BindingOwnerUnitTree] 修正 Router 调用和返回结构
- **文件**: `routers/eshang_api_main/base_info/base_info_misc_router.py`
- **修改内容**: 修正参数顺序（固定 OwnerUnitNature=1000），`Result_Data` 修正为嵌套格式
- **原因**: 原 C# 返回 `JsonMsg<JsonList<NestingModel<CommonTypeModel>>>`

### [BindingMerchantTree] 修正 Router 调用
- **文件**: `routers/eshang_api_main/base_info/base_info_misc_router.py`
- **修改内容**: 复用 `binding_ownerunit_tree(db, 2000, MerchantPid, 1, province)`，修正返回结构
- **原因**: 原 C# 调用 `OwnerUnitHelper.BindingOwnerUnitTree(transaction, 2000, MerchantPid, 1, ProvinceCode)`
