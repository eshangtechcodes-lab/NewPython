# EShang API (FastAPI) 迁移完成接口文档

> **基础地址**: `http://localhost:8080` (本地测试版)

## 业主单位管理 (OWNERUNIT)

### POST /EShangApiMain/BaseInfo/GetOWNERUNITList
**接口名称**: Get Ownerunit List

#### 📝 查询入参 (SearchModel)
| 核心字段 | 说明 |
| --- | --- |
| PageIndex | 页码 (1...) |
| PageSize | 条数 (0=全量) |
| SearchParameter | **详细过滤字段 (见下表)** |

**OWNERUNIT 过滤字段 (SearchParameter 内部):**

| 字段名 | 说明 |
| --- | --- |
| OWNERUNIT_ID | 业主内码 |
| OWNERUNIT_PID | 父级内码 |
| PROVINCE_CODE | 省份标识 |
| PROVINCE_BUSINESSCODE | 业务省份标识 |
| OWNERUNIT_NAME | 业主单位 |
| OWNERUNIT_EN | 业主简称 |
| OWNERUNIT_NATURE | 业主单位性质(1000:管理单位;2000:经营单位) |
| OWNERUNIT_GUID | 业主标识 |
| OWNERUNIT_INDEX | 排序字段 |
| OWNERUNIT_ICO | 业主图标 |

**请求 JSON 示例**:
```json
{
  "PageIndex": 1,
  "PageSize": 20,
  "SearchParameter": {
    "OWNERUNIT_ID": 0,
    "OWNERUNIT_PID": 0,
    "PROVINCE_CODE": 0
  }
}
```

---

### GET /EShangApiMain/BaseInfo/GetOWNERUNITDetail
**接口名称**: Get Ownerunit Detail

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| OWNERUNITId | integer | Y | 业主单位管理表内码 |

---

### POST /EShangApiMain/BaseInfo/SynchroOWNERUNIT
**接口名称**: Synchro Ownerunit

#### 📝 同步入参 (Entity Body)
| 字段名 | 说明 |
| --- | --- |
| OWNERUNIT_ID | 业主内码 |
| OWNERUNIT_PID | 父级内码 |
| PROVINCE_CODE | 省份标识 |
| PROVINCE_BUSINESSCODE | 业务省份标识 |
| OWNERUNIT_NAME | 业主单位 |
| OWNERUNIT_EN | 业主简称 |
| OWNERUNIT_NATURE | 业主单位性质(1000:管理单位;2000:经营单位) |
| OWNERUNIT_GUID | 业主标识 |
| OWNERUNIT_INDEX | 排序字段 |
| OWNERUNIT_ICO | 业主图标 |
| OWNERUNIT_STATE | 有效状态 |
| STAFF_ID | 操作人员内码 |
| STAFF_NAME | 操作人员名称 |
| OPERATE_DATE | 操作时间 |
| OWNERUNIT_DESC | 备注 |
| ISSUPPORTPOINT | 是否支持积分功能 |
| DOWNLOAD_DATE | 下载时间 |
| WECHATPUBLICSIGN_ID | 公众号ID |

**同步 JSON 示例**:
```json
{
  "OWNERUNIT_ID": 0,
  "OWNERUNIT_PID": 0,
  "PROVINCE_CODE": "string",
  "PROVINCE_BUSINESSCODE": "string",
  "OWNERUNIT_NAME": "string"
}
```

---

### GET /EShangApiMain/BaseInfo/DeleteOWNERUNIT
**接口名称**: Delete Ownerunit

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| OWNERUNITId | integer | Y | 业主单位管理表内码 |

---

### POST /EShangApiMain/BaseInfo/DeleteOWNERUNIT
**接口名称**: Delete Ownerunit

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| OWNERUNITId | integer | Y | 业主单位管理表内码 |

---

## 品牌管理 (BRAND)

### POST /EShangApiMain/BaseInfo/GetBrandList
**接口名称**: Get Brand List

#### 📝 查询入参 (SearchModel)
| 核心字段 | 说明 |
| --- | --- |
| PageIndex | 页码 (1...) |
| PageSize | 条数 (0=全量) |
| SearchParameter | **详细过滤字段 (见下表)** |


---

### GET /EShangApiMain/BaseInfo/GetCombineBrandList
**接口名称**: Get Combine Brand List

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PROVINCE_CODE | any | N | 省份编码 |
| SPREGIONTYPE_IDS | string | N | 片区内码 |
| SERVERPART_IDS | string | N | 服务区内码 |
| BRAND_INDUSTRY | string | N | 经营业态 |
| BRAND_TYPE | string | N | 品牌类型 |
| BRAND_STATE | string | N | 有效状态 |
| BRAND_NAME | string | N | 品牌名称（模糊查询） |

---

### GET /EShangApiMain/BaseInfo/GetTradeBrandTree
**接口名称**: Get Trade Brand Tree

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessTrade_PID | integer | N | 经营业态父级内码 |
| ProvinceCode | any | N | 省份编码 |
| OwnerUnitId | any | N | 业主单位内码 |
| BrandState | any | N | 有效状态 |

---

### POST /EShangApiMain/BaseInfo/GetTradeBrandTree
**接口名称**: Get Trade Brand Tree

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessTrade_PID | integer | N | 经营业态父级内码 |
| ProvinceCode | any | N | 省份编码 |
| OwnerUnitId | any | N | 业主单位内码 |
| BrandState | any | N | 有效状态 |

---

### GET /EShangApiMain/BaseInfo/GetBrandDetail
**接口名称**: Get Brand Detail

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BrandId | integer | Y | 品牌内码 |

---

### POST /EShangApiMain/BaseInfo/SynchroBrand
**接口名称**: Synchro Brand

#### 📝 同步入参 (Entity Body)

---

### GET /EShangApiMain/BaseInfo/DeleteBrand
**接口名称**: Delete Brand

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BrandId | integer | Y | 品牌内码 |

---

### POST /EShangApiMain/BaseInfo/DeleteBrand
**接口名称**: Delete Brand

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BrandId | integer | Y | 品牌内码 |

---

## 收银人员 (CASHWORKER)

### POST /EShangApiMain/BaseInfo/GetCASHWORKERList
**接口名称**: Get Cashworker List

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartCodes | any | N |  |

#### 📝 查询入参 (SearchModel)
| 核心字段 | 说明 |
| --- | --- |
| PageIndex | 页码 (1...) |
| PageSize | 条数 (0=全量) |
| SearchParameter | **详细过滤字段 (见下表)** |


---

### GET /EShangApiMain/BaseInfo/GetCASHWORKERDetail
**接口名称**: Get Cashworker Detail

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| CASHWORKERId | integer | Y | 收银人员表内码 |

---

### POST /EShangApiMain/BaseInfo/SynchroCASHWORKER
**接口名称**: Synchro Cashworker

#### 📝 同步入参 (Entity Body)

---

### GET /EShangApiMain/BaseInfo/DeleteCASHWORKER
**接口名称**: Delete Cashworker

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| CASHWORKERId | integer | Y | 收银人员表内码 |

---

### POST /EShangApiMain/BaseInfo/DeleteCASHWORKER
**接口名称**: Delete Cashworker

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| CASHWORKERId | integer | Y | 收银人员表内码 |

---

## 服务区站点 (SERVERPART)

### POST /EShangApiMain/BaseInfo/GetSERVERPARTList
**接口名称**: Get Serverpart List

#### 📝 查询入参 (SearchModel)
| 核心字段 | 说明 |
| --- | --- |
| PageIndex | 页码 (1...) |
| PageSize | 条数 (0=全量) |
| SearchParameter | **详细过滤字段 (见下表)** |

**SERVERPART 过滤字段 (SearchParameter 内部):**

| 字段名 | 说明 |
| --- | --- |
| SERVERPART_ID | 内码 |
| SERVERPART_NAME | 服务区名称 |
| SERVERPART_ADDRESS | 服务区地址 |
| SERVERPART_INDEX | 服务区索引 |
| EXPRESSWAY_NAME | 所在高速路 |
| SELLERCOUNT | 商家服务数 |
| SERVERPART_AREA | 服务区面积 |
| SERVERPART_X | 坐标X |
| SERVERPART_Y | 坐标Y |
| SERVERPART_TEL | 电话号码 |

**请求 JSON 示例**:
```json
{
  "PageIndex": 1,
  "PageSize": 20,
  "SearchParameter": {
    "SERVERPART_ID": 0,
    "SERVERPART_NAME": "string",
    "SERVERPART_ADDRESS": 0
  }
}
```

---

### GET /EShangApiMain/BaseInfo/DeleteSERVERPART
**接口名称**: Delete Serverpart

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SERVERPARTId | integer | Y | 服务区站点内码 |

---

### POST /EShangApiMain/BaseInfo/DeleteSERVERPART
**接口名称**: Delete Serverpart

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SERVERPARTId | integer | Y | 服务区站点内码 |

---

## 系统

### GET /
**接口名称**: Root

---

### GET /health
**接口名称**: Health Check

---

## 门店变更日志 (SERVERPARTSHOP_LOG)

### POST /EShangApiMain/BaseInfo/GetSERVERPARTSHOP_LOGList
**接口名称**: Get Serverpartshop Log List

#### 📝 查询入参 (SearchModel)
| 核心字段 | 说明 |
| --- | --- |
| PageIndex | 页码 (1...) |
| PageSize | 条数 (0=全量) |
| SearchParameter | **详细过滤字段 (见下表)** |


---

## 门店管理 (SERVERPARTSHOP)

### POST /EShangApiMain/BaseInfo/GetServerpartShopList
**接口名称**: Get Serverpartshop List

#### 📝 查询入参 (SearchModel)
| 核心字段 | 说明 |
| --- | --- |
| PageIndex | 页码 (1...) |
| PageSize | 条数 (0=全量) |
| SearchParameter | **详细过滤字段 (见下表)** |


---

### GET /EShangApiMain/BaseInfo/GetServerpartShopDetail
**接口名称**: Get Serverpartshop Detail

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartShopId | integer | Y | 门店内码 |

---

### POST /EShangApiMain/BaseInfo/GetServerpartShopDetail
**接口名称**: Get Serverpartshop Detail

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartShopId | integer | Y | 门店内码 |

---

### POST /EShangApiMain/BaseInfo/SynchroServerpartShop
**接口名称**: Synchro Serverpartshop

#### 📝 同步入参 (Entity Body)

---

### GET /EShangApiMain/BaseInfo/DeleteServerpartShop
**接口名称**: Delete Serverpartshop

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartShopId | integer | Y | 门店内码 |

---

### POST /EShangApiMain/BaseInfo/DeleteServerpartShop
**接口名称**: Delete Serverpartshop

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartShopId | integer | Y | 门店内码 |

---

### GET /EShangApiMain/BaseInfo/DelServerpartShop
**接口名称**: Del Serverpartshop


---

### POST /EShangApiMain/BaseInfo/DelServerpartShop
**接口名称**: Del Serverpartshop


---

## 门店经营时间 (RTSERVERPARTSHOP)

### POST /EShangApiMain/BaseInfo/GetRTSERVERPARTSHOPList
**接口名称**: Get Rtserverpartshop List

#### 📝 查询入参 (SearchModel)
| 核心字段 | 说明 |
| --- | --- |
| PageIndex | 页码 (1...) |
| PageSize | 条数 (0=全量) |
| SearchParameter | **详细过滤字段 (见下表)** |


---

### GET /EShangApiMain/BaseInfo/GetRTSERVERPARTSHOPDetail
**接口名称**: Get Rtserverpartshop Detail

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| RTSERVERPARTSHOPId | integer | Y | 门店经营时间表内码 |

---

### POST /EShangApiMain/BaseInfo/SynchroRTSERVERPARTSHOP
**接口名称**: Synchro Rtserverpartshop

#### 📝 同步入参 (Entity Body)

---

### GET /EShangApiMain/BaseInfo/DeleteRTSERVERPARTSHOP
**接口名称**: Delete Rtserverpartshop

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| RTSERVERPARTSHOPId | integer | Y | 门店经营时间表内码 |

---

### POST /EShangApiMain/BaseInfo/DeleteRTSERVERPARTSHOP
**接口名称**: Delete Rtserverpartshop

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| RTSERVERPARTSHOPId | integer | Y | 门店经营时间表内码 |

---

