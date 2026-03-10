# 动态完整性测试问题记录

- 建立时间：2026-03-09
- 原 API：`http://192.168.1.99:8900/EShangApiMain`
- 新 API：`http://localhost:8080/EShangApiMain`
- 默认 Header：`{"ProvinceCode":"340000"}`
- 执行限制：`不允许真实写接口`

## 记录规则

- 只记录动态联调中实际遇到的问题。
- 每条问题必须写明接口、参数组、现象、初步判断、后续动作。
- Header 或参数口径不清时，先记录再补充，不直接改结论。

## 待确认输入

| 日期 | 分类 | 描述 | 影响范围 | 状态 |
| --- | --- | --- | --- | --- |
| 2026-03-09 | 参数口径 | 默认 Header 采用 `ProvinceCode=340000`，但你给出的 body 样本里出现过 `ProvinceCode=34000`。当前 manifest 已统一按 `340000` 处理。 | 所有依赖 ProvinceCode 的接口 | 待确认 |

## 动态问题记录

| 日期 | 接口 | 用例 | 问题类型 | 现象 | 初步判断 | 后续动作 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-03-09 | `BaseInfo/GetSERVERPARTList` | `empty-body` | 返回契约不一致 | 新旧接口都返回 `Result_Code=999`，但新接口 `Result_Desc` 变成了 Pydantic 校验错误，原接口是 `查询失败未将对象引用设置到对象的实例。` | Python 侧错误包装和原 C# 不一致，且空参分支把 `StaticsModel=None` 直接传入了响应模型。 | 回查 [serverpart_router.py](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/base_info/serverpart_router.py) 与 [serverpart_service.py](/E:/workfile/JAVA/NewAPI/services/base_info/serverpart_service.py) 的空参错误分支，恢复原错误壳。 | 待修复 |
| 2026-03-09 | `BaseInfo/GetSERVERPARTList` | `search-model` | SQL/字段映射错误 | 原接口成功返回 1 条数据；新接口返回 `Result_Code=999`，错误为 `无效的列名[PROVINCECODE]`。 | Python SQL 把 `ProvinceCode` 直接当列名拼进了达梦查询，未映射为实际字段名或 Header 条件。 | 回查 [serverpart_service.py](/E:/workfile/JAVA/NewAPI/services/base_info/serverpart_service.py) 的查询条件拼装，区分 Header `ProvinceCode` 与表字段 `PROVINCE_CODE`。 | 待修复 |
| 2026-03-09 | `BaseInfo/GetSERVERPARTList` | `flat-body` | 入参契约不兼容 | 原接口把扁平 body 当有效查询并返回数据；新接口返回 Pydantic 校验错误，`Result_Data` 缺失。 | Python 路由只接受一种入参模型，没有兼容原接口实际接受的扁平 JSON。 | 核对原 C# Controller 入参形态，决定是兼容扁平 body 还是在动态验收口径里明确排除。 | 待确认 |
| 2026-03-09 | `BaseInfo/GetServerpartDDL` | `default-type/service-area-416/empty-query` | 运行时逻辑错误 | 3 组 GET 用例中，原接口均成功，新接口统一报错 `int object has no attribute strip`，且顶层少了 `Result_Data`。 | Python 侧对 query 参数做了字符串 `strip()`，但实际传入了整数；异常分支也没有保持原 `Result_Data` 包装。 | 回查 [base_info_misc_router.py](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/base_info/base_info_misc_router.py) 与 [base_info_misc_service.py](/E:/workfile/JAVA/NewAPI/services/base_info/base_info_misc_service.py) 的 GET 参数处理。 | 待修复 |
