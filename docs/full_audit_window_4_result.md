# 窗口 4 审计结果

结论摘要：`Picture` 模块未与原 C# 保持同一接口集合，Python 以一套 `T_PICTURE` CRUD/统计接口错误替换了原凭证/上传接口；`Video` 模块原 C# 16 条接口在 Python 侧确认全部未迁移。

角色：收尾与高风险模块审计员

负责模块：
- Picture
- Video

补充结论：
- `Picture` 路由集：C# 9 条，Python 9 条，同名仅 3 条，且 0 条完全一致。
- `Video` 路由集：C# 16 条，Python 0 条，确认 16 条全部为 `Python 缺失`。

## 模块总表

| 模块 | 已迁移路由数 | 完全一致 | 契约不一致 | 逻辑不一致 | 占位实现 | Python 多出 | Python 缺失 | 备注 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Picture | 9 | 0 | 0 | 3 | 0 | 6 | 6 | 原 9 条 C# 凭证接口只保留了 3 个同名路由，但 3 个都改义；Python 另起 6 条 `T_PICTURE` CRUD/统计接口。 |
| Video | 0 | 0 | 0 | 0 | 0 | 0 | 16 | `ShopVideoController` 16 条接口全部缺失；可拆为 `12 条 CRUD 模板` + `4 条散装逻辑` 两段实施。 |

## 路由级问题清单

统一 Python 证据说明：
- `Picture` 现有路由只在 `E:\workfile\JAVA\NewAPI\routers\eshang_api_main\batch_modules\batch_router_part2.py:363-406` 与 `E:\workfile\JAVA\NewAPI\services\picture\picture_service.py:12-111` 中实现。
- `Video` 全仓静态检索 `/ShopVideo/` 仅命中 `docs` 与 `baseline`，未命中任何 Python `router/service` 实现。

| 路由 | 级别 | 类型 | Python 证据 | C# 证据 | 差异说明 | 修复建议 |
| --- | --- | --- | --- | --- | --- | --- |
| Picture/GetPictureList | P0 | 逻辑 | `E:\workfile\JAVA\NewAPI\routers\eshang_api_main\batch_modules\batch_router_part2.py:368-371`；`E:\workfile\JAVA\NewAPI\services\picture\picture_service.py:25-28` | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Picture\PictureController.cs:27-52`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\MainProject\FrameWork\PictureHelper.cs:463-518,531-653,1362-1375` | C# 以 `TableId/TableName/TableType/ImageType/ImageIndex` 解析真实业务表与附件目录并取图片；Python 改成对 `T_PICTURE` 做分页查询，只认 `SearchData.SERVERPART_ID`，返回包装也从 `100/200/999` 漂移为 `200/ok`。`GetPictureList` 原入参和语义已被改坏。 | 恢复原通用查询契约，保留 `GET/POST`、目录翻译、`ImageType/ImageIndex` 过滤和原响应包装。 |
| Picture/UploadPicture | P0 | 逻辑 | `E:\workfile\JAVA\NewAPI\routers\eshang_api_main\batch_modules\batch_router_part2.py:386-389`；`E:\workfile\JAVA\NewAPI\services\picture\picture_service.py:35-69` | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Picture\PictureController.cs:76-118`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\MainProject\FrameWork\PictureHelper.cs:150-223,237-382,774-930` | C# 处理 multipart 文件流或 HWS 图片上传，写物理文件并落到按 `TableType/TableName` 解析出的业务图片/附件表；`TableType == 1127` 且有 `ImageIndex` 时还会触发 `PushNewCheckReport`。Python 仅把 JSON `data` upsert 到 `T_PICTURE`，没有文件接收、目录映射、业务表写入和外部副作用。 | 不能复用当前 `synchro_picture`；需按原 C# 文件上传路径、表路由和副作用重建接口。 |
| Picture/DeletePicture | P0 | 逻辑 | `E:\workfile\JAVA\NewAPI\routers\eshang_api_main\batch_modules\batch_router_part2.py:382-384`；`E:\workfile\JAVA\NewAPI\services\picture\picture_service.py:59-64` | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Picture\PictureController.cs:346-379`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\MainProject\FrameWork\PictureHelper.cs:1068-1290` | C# 以 `ImageId + TableName/TableType + ImagePath` 删除物理文件并删除目标业务表记录，支持 `GET/POST`；Python 只按 `PictureId` 把 `T_PICTURE.PICTURE_STATE` 置 0。该接口不是删文件，而是软删另一张表。 | 恢复原删除契约和文件系统删除逻辑，不能把当前软删视为兼容实现。 |
| Picture/SaveImgFile | P0 | 缺失 | 无对应 Python 路由/服务 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Picture\PictureController.cs:138-176`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\MainProject\FrameWork\PictureHelper.cs:425-452` | 原接口只保存文件、不落数据库；Python 完全缺失，也没有等价替代。 | 补齐单独的“只存文件”接口，不能用 `UploadPicture` 或 `SynchroPicture` 替代。 |
| Picture/GetEndaccountEvidence | P0 | 缺失 | 无对应 Python 路由/服务 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Picture\PictureController.cs:186-200`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\MainProject\FrameWork\PictureHelper.cs:396-414` | 原接口固定查询 `HIGHWAY_SELLDATA.T_ENDACCOUNT` 的 HWS 图片；Python 未迁移。 | 按原表名和 `GetHWSImageList` 逻辑补齐。 |
| Picture/UploadEndaccountEvidence | P0 | 缺失 | 无对应 Python 路由/服务 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Picture\PictureController.cs:222-240`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\MainProject\FrameWork\PictureHelper.cs:38-103` | 原接口接 `EndaccountId + ImageInfo(base64)`，写入 `/UploadImageDir/ENDACCOUNT/` 并落 HWS `IMAGE`；Python 未迁移。 | 按原 base64 上传契约补齐，不要复用 JSON upsert。 |
| Picture/GetAuditEvidence | P0 | 缺失 | 无对应 Python 路由/服务 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Picture\PictureController.cs:259-273`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\MainProject\FrameWork\PictureHelper.cs:396-414` | 原接口固定查询 `HIGHWAY_SELLDATA.T_CHECKACCOUNT` 的 HWS 图片；Python 未迁移。 | 按原表名和 `GetHWSImageList` 逻辑补齐。 |
| Picture/UploadAuditEvidence | P0 | 缺失 | 无对应 Python 路由/服务 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Picture\PictureController.cs:295-324`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\MainProject\FrameWork\PictureHelper.cs:38-103,237-382` | 原接口既支持 `ImageInfo` base64，也支持文件流上传，目标目录固定为 `/UploadImageDir/CHECKACCOUNT/`；Python 未迁移。 | 补齐双路径上传逻辑和原响应码语义。 |
| Picture/DeleteMultiPicture | P1 | 缺失 | 无对应 Python 路由/服务 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Picture\PictureController.cs:395-427`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\MainProject\FrameWork\PictureHelper.cs:1068-1290` | 原接口接 `PictureList`，逐条按 `TableType` 或 `TableName` 删除真实文件和业务表记录；Python 未迁移。 | 按原 `PictureList` 契约补齐，不要用 `ids` 批量软删替代。 |
| Picture/BatchDeletePicture | P1 | Python 多出 | `E:\workfile\JAVA\NewAPI\routers\eshang_api_main\batch_modules\batch_router_part2.py:403-406`；`E:\workfile\JAVA\NewAPI\services\picture\picture_service.py:103-111` | C# `PictureController` 无此路由 | Python 新增 `ids` 批量软删 `T_PICTURE`，看似在替代 `DeleteMultiPicture`，但输入模型、删除语义和目标表都不一致。属于错误替代。 | 不计入 Picture 迁移完成度；仅在原接口补齐后再评估是否保留为增量接口。 |
| Picture/GetPictureDetail | P2 | Python 多出 | `E:\workfile\JAVA\NewAPI\routers\eshang_api_main\batch_modules\batch_router_part2.py:373-375`；`E:\workfile\JAVA\NewAPI\services\picture\picture_service.py:30-33` | C# `PictureController` 无此路由 | Python 新增单表明细查询，查询对象是 `T_PICTURE` 主键，不是原凭证模块的一部分。属于错误替代。 | 从 Picture 迁移验收口径中剔除；不要拿它冲抵缺失的凭据接口。 |
| Picture/GetPictureTypeList | P2 | Python 多出 | `E:\workfile\JAVA\NewAPI\routers\eshang_api_main\batch_modules\batch_router_part2.py:391-393`；`E:\workfile\JAVA\NewAPI\services\picture\picture_service.py:71-78` | C# `PictureController` 无此路由 | 新增 `T_PICTURE` 类型统计接口，与原 C# 凭证中心无对应关系。属于错误替代。 | 同上。 |
| Picture/GetPictureByShop | P2 | Python 多出 | `E:\workfile\JAVA\NewAPI\routers\eshang_api_main\batch_modules\batch_router_part2.py:395-397`；`E:\workfile\JAVA\NewAPI\services\picture\picture_service.py:80-91` | C# `PictureController` 无此路由 | 新增按门店查 `T_PICTURE` 的接口，不对应原 Picture 路由集合。属于错误替代。 | 同上。 |
| Picture/GetPictureCount | P2 | Python 多出 | `E:\workfile\JAVA\NewAPI\routers\eshang_api_main\batch_modules\batch_router_part2.py:399-401`；`E:\workfile\JAVA\NewAPI\services\picture\picture_service.py:93-101` | C# `PictureController` 无此路由 | 新增计数接口，不在原 C# Picture 模块中。属于错误替代。 | 同上。 |
| Picture/SynchroPicture | P1 | Python 多出 | `E:\workfile\JAVA\NewAPI\routers\eshang_api_main\batch_modules\batch_router_part2.py:377-380`；`E:\workfile\JAVA\NewAPI\services\picture\picture_service.py:35-57` | C# `PictureController` 无此路由 | Python 新增 `T_PICTURE` upsert 路由；原 Picture 模块没有“同步图片表”接口。属于错误替代。 | 同上，不得视为 Picture 模块已迁移能力。 |
| Video/GetEXTRANETList | P1 | 缺失 | 无；全仓 `/ShopVideo/` 检索仅命中 `docs` 与 `baseline`，未命中任何 Python 路由/服务 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:28-42`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\EXTRANETHelper.cs:22-78` | `EXTRANET` 主表列表接口完全未迁移。该接口是标准 `SearchModel + 分页 + 排序` CRUD 模板。 | 归入 Video 批次 1，与 `GetEXTRANETDetail/SynchroEXTRANET/DeleteEXTRANET` 一起按 CRUD 模板迁移。 |
| Video/GetEXTRANETDetail | P1 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:64-72`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\EXTRANETHelper.cs:87-107` | `EXTRANET` 主表明细接口完全未迁移。 | 归入 Video 批次 1。 |
| Video/SynchroEXTRANET | P1 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:94-110`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\EXTRANETHelper.cs:117-143` | `EXTRANET` 主表新增/更新接口完全未迁移。C# 逻辑是有主键则更新，无主键则插入。 | 归入 Video 批次 1。 |
| Video/DeleteEXTRANET | P1 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:130-145`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\EXTRANETHelper.cs:174-189` | `EXTRANET` 主表删除接口完全未迁移。 | 归入 Video 批次 1。 |
| Video/GetEXTRANETDETAILList | P1 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:167-181`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\EXTRANETDETAILHelper.cs:22-80` | `EXTRANETDETAIL` 列表接口完全未迁移。整体仍是 `SearchModel + 分页 + 排序` 模板。 | 归入 Video 批次 2，与同实体 3 条接口一起迁移。 |
| Video/GetEXTRANETDETAILDetail | P1 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:203-211`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\EXTRANETDETAILHelper.cs:90-113` | `EXTRANETDETAIL` 明细接口完全未迁移。 | 归入 Video 批次 2。 |
| Video/SynchroEXTRANETDETAIL | P1 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:233-249`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\EXTRANETDETAILHelper.cs:123-165` | `EXTRANETDETAIL` 新增/更新接口完全未迁移。C# 使用 `OperationDataHelper.GetTableExcuteSQL` 生成 SQL，但仍属标准单表同步模板。 | 归入 Video 批次 2。 |
| Video/DeleteEXTRANETDETAIL | P1 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:269-284`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\EXTRANETDETAILHelper.cs:174-189` | `EXTRANETDETAIL` 删除接口完全未迁移。 | 归入 Video 批次 2。 |
| Video/GetSHOPVIDEOList | P1 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:306-320`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\ShopVideoHelper.cs:26-90` | `SHOPVIDEO` 列表接口完全未迁移。仍是标准 `SearchModel + 分页 + 排序` 模板。 | 归入 Video 批次 3，与同实体 3 条接口一起迁移。 |
| Video/GetSHOPVIDEODetail | P1 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:342-350`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\ShopVideoHelper.cs:100-129` | `SHOPVIDEO` 明细接口完全未迁移。 | 归入 Video 批次 3。 |
| Video/SynchroSHOPVIDEO | P1 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:372-388`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\ShopVideoHelper.cs:139-165` | `SHOPVIDEO` 新增/更新接口完全未迁移。 | 归入 Video 批次 3。 |
| Video/DeleteSHOPVIDEO | P1 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:408-423`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\ShopVideoHelper.cs:205-219` | `SHOPVIDEO` 删除接口完全未迁移。 | 归入 Video 批次 3。 |
| Video/GetVIDEOLOGList | P1 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:445-459`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\VIDEOLOGHelper.cs:24-220` | 完全未迁移；且不是简单 CRUD。C# 根据 `Search_Type` 分 1000/2000/2010/3000/4000 等分支，跨 `T_YSABNORMALITY/T_CHECKACCOUNT/T_ABNORMALAUDIT/T_ENDACCOUNT/T_SELLMASTER` 做联表筛选。 | 单独归入 Video 批次 4，不能混入 CRUD 模板。 |
| Video/SynchroVIDEOLOG | P1 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:481-490`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\VIDEOLOGHelper.cs:319-335` | 完全未迁移；逻辑是简单插入日志，但字段组合与 `SERVERPART_CODE` 截取规则需要保留。 | 归入 Video 批次 4，可与 `GetVIDEOLOGList` 同批，但实现上独立。 |
| Video/GetShopVideoInfo | P0 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:520-557`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\ShopVideoHelper.cs:236-490` | 完全未迁移；该接口会先从 `V_SHOPVIDEO` 选摄像头，再根据 `JsonString/ServerpartCode/ServerpartShopCode/MachineCode/AbnormalityCode/CheckEndaccount_ID/AbnormalAudit_ID/Endaccount_ID` 分支解析异常稽核、日结、现场稽查和异常现场稽查，并拼装 `AbnormalityDetails`。 | 单独归入 Video 批次 5，按散装逻辑接口处理，必须逐分支对齐。 |
| Video/GetYSShopVideoInfo | P0 | 缺失 | 同上 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\Video\ShopVideoController.cs:584-621`；`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\Video\ShopVideoHelper.cs:505-789` | 完全未迁移；与 `GetShopVideoInfo` 相似但读取 `T_YSABNORMALITY/T_YSABNORMALITYDETAIL`，同时处理公网/内网 IP 选择、商品明细拼装和多种异常类型文案。 | 单独归入 Video 批次 5，必须单独实现和联调。 |

## 模块整改建议

### Picture

- 第一优先级修复：先把原 C# 的 9 条 Picture 接口集合原样恢复，优先顺序为 `GetPictureList`、`UploadPicture`、`DeletePicture`、`SaveImgFile`、`GetEndaccountEvidence`、`UploadEndaccountEvidence`、`GetAuditEvidence`、`UploadAuditEvidence`、`DeleteMultiPicture`。当前 Python 不是“少量差异”，而是整套接口集合被换掉了。
- 可以批量修复：`GetEndaccountEvidence/GetAuditEvidence` 可共用 `GetHWSImageList` 模式；`UploadEndaccountEvidence/UploadAuditEvidence/SaveImgFile` 可共用文件保存与路径组装模式；`DeletePicture/DeleteMultiPicture` 可共用 `DelFile/DelFileByType` 删除模式。
- 必须人工联调验证：multipart 文件流上传、base64 上传、`TranslateStorageTable/SetFilePath` 目录映射、`TableType == 1127` 时的 `PushNewCheckReport` 副作用、物理文件删除与数据库删除的一致性、以及原 C# `100/200/999` 响应码语义。
- 处置建议：`GetPictureDetail/GetPictureTypeList/GetPictureByShop/GetPictureCount/SynchroPicture/BatchDeletePicture` 不能再作为 Picture 模块迁移完成度依据；它们属于另一套 `T_PICTURE` 管理接口，应与原凭证中心解耦验收。

### Video

- 第一优先级修复：先确认 `ShopVideoController` 16 条接口全部进入迁移清单，不得再按“0 运行时路由”视为后续可选项。
- 明确迁移批次建议：
  1. 批次 1：`EXTRANET` 4 条 CRUD 模板接口  
     `GetEXTRANETList`、`GetEXTRANETDetail`、`SynchroEXTRANET`、`DeleteEXTRANET`
  2. 批次 2：`EXTRANETDETAIL` 4 条 CRUD 模板接口  
     `GetEXTRANETDETAILList`、`GetEXTRANETDETAILDetail`、`SynchroEXTRANETDETAIL`、`DeleteEXTRANETDETAIL`
  3. 批次 3：`SHOPVIDEO` 4 条 CRUD 模板接口  
     `GetSHOPVIDEOList`、`GetSHOPVIDEODetail`、`SynchroSHOPVIDEO`、`DeleteSHOPVIDEO`
  4. 批次 4：日志接口  
     `GetVIDEOLOGList`、`SynchroVIDEOLOG`
  5. 批次 5：散装视频聚合接口  
     `GetShopVideoInfo`、`GetYSShopVideoInfo`
- 可按 CRUD 模板批量迁移：前 12 条 `EXTRANET/EXTRANETDETAIL/SHOPVIDEO` 接口都遵循“列表-明细-同步-删除”的单表模式，C# helper 结构清晰，适合共用模板批量落地。
- 需要单独做的散装逻辑：`GetVIDEOLOGList`、`GetShopVideoInfo`、`GetYSShopVideoInfo`。其中后两条最复杂，涉及 `V_SHOPVIDEO` 摄像头选择、异常表/日结表/现场稽查表分支、商品明细聚合和文案拼接，不能用 CRUD 框架硬套。
- 必须人工联调验证：`JsonString` 与平铺参数双入口、`GET/POST` 双方法兼容、`AbnormalityDetails` 文案分支、`VideoIP` 公网/内网选择、以及不同异常类型时间窗的计算结果。

## 风险与阻塞

- 本次静态审计已能确认路由集合偏差、逻辑替换和 16 条 Video 缺口，但文件上传/删除、副作用调用和 Oracle/文件系统行为仍需联调验证才能闭环。
- Picture 原逻辑高度依赖 `TranslateStorageTable`、`GetCatalogueData`、`SetFilePath`、`SaveDataToOracle` 等动态表映射；若迁移时继续沿用 `T_PICTURE` 单表思路，会再次把接口语义做坏。
- Video 两个聚合接口依赖 `HIGHWAY_EXCHANGE.V_SHOPVIDEO`、`T_ABNORMALITY_{ServerpartCode}`、`T_YSABNORMALITY`、`T_YSABNORMALITYDETAIL`、`HIGHWAY_SELLDATA.T_ENDACCOUNT`、`T_CHECKACCOUNT`、`T_ABNORMALAUDIT`、`T_SELLDETAILS` 等多表/动态表，静态阅读可判定“未迁移”和“复杂度”，但边界数据格式仍要靠联调样例验证。
- `GetVIDEOLOGList` 的 `Search_Type` 分支过滤跨多张业务表；若迁移时只按简单列表模板实现，会造成看似上线、实际查询结果错误的隐性回归。
