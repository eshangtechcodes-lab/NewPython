# EShangApiMain接口文档

> **基础地址**: `https://api.eshangtech.com/EShangApiMain/`
> 
> ⚠️ **测试规范说明**:
> 1. **严禁使用占位符**: 在进行接口测试或联调时，**禁止使用 `test`、`123` 等无意义的占位符作为参数值**。
> 2. **类型转换风险**: 后台对参数类型校验严格，使用非预期类型的字符串作为 ID（如将数字 ID 传为 "test"）会导致 `System.Decimal` 转换异常或 SQL 执行失败。
> 3. **真实数据优先**: 请务必使用真实的业务内码（如 `ProvinceCode: 340000`）和正确的日期格式（如 `yyyy-MM-dd`）进行请求。

## 系统登录相关接口【LoggingController】

---
### POST /Logging/UserLogin
**名称**: 用户登录
**Action**: `UserLogin`

**场景**: 
用于驿商云平台，用户登录界面，在用户输入登录账号和密码后，点击登录按钮调用接口。
**说明**: 
用户登录的接口，验证账号密码是否正确，验证登录状态是否异常，验证登录密码是否符合要求：
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| UserPassport | string | Y | 用户登录账号 |
| UserPassWord | string | Y | 用户登录密码 |
| LoginIP | string | N | 登录IP |
| LoginPlace | string | N | 登录地点 |
| BrowserVersion | string | N | 浏览器版本 |
| OperatingSystem | string | N | 操作系统 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<PassportInfo> | 返回数据集合 |

PassportInfo 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| UserName | string | 登录帐户 |
| UserPassWord | string | 登录密码 |
| ID | integer | 帐户内码 |
| ID_Encrypted | string | 帐户内码 |
| Name | string | 用户名称 |
| HeadImgUrl | string | 用户名称 |
| DepartmentName | string | 所属部门 |
| UserMobilephone | string | 手机号码 |
| ProvinceCode | string | 省份编码，如330000 |
| ProvinceUnit | string | 业主单位 |
| OwnerUnitId | integer | 业主单位 |
| OwnerUnitName | string | 业主单位 |
| SupplierID | integer | 供应商内码 |
| SupplierName | string | 供应商名称 |
| BusinessManID | integer | 商户内码 |
| BusinessManName | string | 商户名称 |
| UserToken | string | 登录标识 |
| CityAuthority | string | 用户服务区权限（编码） |
| ServerpartIds | string | 服务区权限（内码） |
| ServerpartShopIds | string | 服务区门店权限 |
| SellerId | integer | 统一配送商户内码 |
| WarehouseId | string | 仓库内码 |
| UserPattern | integer | 数据模式（1000：业主；2000：商户） |
| SuperAdmin | integer | 超级管理员 |
| TopSystemRoleId | integer | 顶级系统角色 |
| EnabledRepeat | boolean | 是否允许重复登录 |
| totalCount | integer | 消息总条数 |
| unreadCount | integer | 未读消息条数 |
| UserModuleList | List<NestingModel[SYSTEMMENUModel]> | 用户模块权限 |

NestingModel[SYSTEMMENUModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | SYSTEMMENUModel | 结点 |
| children | List<NestingModel[SYSTEMMENUModel]> | 子级 |

SYSTEMMENUModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMENU_PID | integer | 系统菜单父级内码 |
| SYSTEMMENU_NAME | string | 系统菜单名称 |
| SYSTEMMENU_INDEX | integer | 系统菜单索引 |
| SYSTEMMENU_LEVEL | integer | 系统菜单级别 |
| SYSTEMMENU_ICO | string | 系统菜单图标 |
| SYSTEMMENU_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMENU_DESC | string | 备注说明 |
| SystemModuleList | List<SYSTEMMODULEModel> | 系统模块列表 |

SYSTEMMODULEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMODULE_ID | integer | 系统模块内码 |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMODULE_TYPE | integer | 系统模块类型 |
| SYSTEMMODULE_NAME | string | 系统模块名称 |
| SYSTEMMODULE_INDEX | integer | 系统模块索引 |
| SYSTEMMODULE_GUID | string | 模块唯一标识 |
| SYSTEMMODULE_URL | string | 系统模块地址 |
| SYSTEMMODULE_ICO | string | 系统模块图标 |
| SYSTEMMODULE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMODULE_DESC | string | 备注说明 |

---
### POST /Logging/CheckLoginError
**名称**: 验证账号登录是否存在异常
**Action**: `CheckLoginError`

**场景**: 
在商业综合管理平台调用，判断当前用户账号登录状态是否有异常。
**说明**: 
验证账号登录是否存在异常，返回100可以登录系统，返回其他表示账号已被锁定：
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| UserPassport | string | Y | 用户登录账号 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |

---
### POST /Logging/DealLoginEvent
**名称**: 处理登录验证后的事件
**Action**: `DealLoginEvent`

**场景**: 
驿商云平台和商业综合管理平台，记录用户登录后的内容，将数据存储在日志表中。
**说明**: 
处理登录验证后的事件
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| EventType | int | Y | 事件类型：1【账户或密码错误】，2【账户已失效】，3【登录失败超过5次】，其他【登录成功】 |
| UserPassport | string | Y | 用户登录账号 |
| UserID | int | N | 用户账号内码 |
| UserName | string | N | 用户名称 |
| LoginIP | string | N | 登录IP |
| LoginPlace | string | N | 登录地点 |
| BrowserVersion | string | N | 浏览器版本 |
| OperatingSystem | string | N | 操作系统 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 记录成功 |
| Result_Data | string | 异常说明 |

---
### GET/POST /Logging/GetPassportInfoById
**名称**: 根据加密id获取用户信息
**Action**: `GetPassportInfoById`

**场景**: 
驿商云平台，在用户登录系统后，根据获取到的加密内码查询用户基本信息。
**说明**: 
根据加密id获取用户信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| UserIdEncrypted | string | Y | 用户id加密字符串 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<PassportInfo> | 返回数据集合 |

PassportInfo 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| UserName | string | 登录帐户 |
| UserPassWord | string | 登录密码 |
| ID | integer | 帐户内码 |
| ID_Encrypted | string | 帐户内码 |
| Name | string | 用户名称 |
| HeadImgUrl | string | 用户名称 |
| DepartmentName | string | 所属部门 |
| UserMobilephone | string | 手机号码 |
| ProvinceCode | string | 省份编码，如330000 |
| ProvinceUnit | string | 业主单位 |
| OwnerUnitId | integer | 业主单位 |
| OwnerUnitName | string | 业主单位 |
| SupplierID | integer | 供应商内码 |
| SupplierName | string | 供应商名称 |
| BusinessManID | integer | 商户内码 |
| BusinessManName | string | 商户名称 |
| UserToken | string | 登录标识 |
| CityAuthority | string | 用户服务区权限（编码） |
| ServerpartIds | string | 服务区权限（内码） |
| ServerpartShopIds | string | 服务区门店权限 |
| SellerId | integer | 统一配送商户内码 |
| WarehouseId | string | 仓库内码 |
| UserPattern | integer | 数据模式（1000：业主；2000：商户） |
| SuperAdmin | integer | 超级管理员 |
| TopSystemRoleId | integer | 顶级系统角色 |
| EnabledRepeat | boolean | 是否允许重复登录 |
| totalCount | integer | 消息总条数 |
| unreadCount | integer | 未读消息条数 |
| UserModuleList | List<NestingModel[SYSTEMMENUModel]> | 用户模块权限 |

NestingModel[SYSTEMMENUModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | SYSTEMMENUModel | 结点 |
| children | List<NestingModel[SYSTEMMENUModel]> | 子级 |

SYSTEMMENUModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMENU_PID | integer | 系统菜单父级内码 |
| SYSTEMMENU_NAME | string | 系统菜单名称 |
| SYSTEMMENU_INDEX | integer | 系统菜单索引 |
| SYSTEMMENU_LEVEL | integer | 系统菜单级别 |
| SYSTEMMENU_ICO | string | 系统菜单图标 |
| SYSTEMMENU_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMENU_DESC | string | 备注说明 |
| SystemModuleList | List<SYSTEMMODULEModel> | 系统模块列表 |

SYSTEMMODULEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMODULE_ID | integer | 系统模块内码 |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMODULE_TYPE | integer | 系统模块类型 |
| SYSTEMMODULE_NAME | string | 系统模块名称 |
| SYSTEMMODULE_INDEX | integer | 系统模块索引 |
| SYSTEMMODULE_GUID | string | 模块唯一标识 |
| SYSTEMMODULE_URL | string | 系统模块地址 |
| SYSTEMMODULE_ICO | string | 系统模块图标 |
| SYSTEMMODULE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMODULE_DESC | string | 备注说明 |

---
### GET/POST /Logging/GetPassportInfoByToken
**名称**: 根据用户token获取用户信息
**Action**: `GetPassportInfoByToken`

**场景**: 
驿商云平台，在用户登录后，刷新或者重新加载页面，根据缓存在浏览器中的token获取用户基本信息。
**说明**: 
根据用户token获取用户信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| token | string | Y | 用户token |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[PassportInfo]> | 返回数据集合 |

PassportInfo 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| UserName | string | 登录帐户 |
| UserPassWord | string | 登录密码 |
| ID | integer | 帐户内码 |
| ID_Encrypted | string | 帐户内码 |
| Name | string | 用户名称 |
| HeadImgUrl | string | 用户名称 |
| DepartmentName | string | 所属部门 |
| UserMobilephone | string | 手机号码 |
| ProvinceCode | string | 省份编码，如330000 |
| ProvinceUnit | string | 业主单位 |
| OwnerUnitId | integer | 业主单位 |
| OwnerUnitName | string | 业主单位 |
| SupplierID | integer | 供应商内码 |
| SupplierName | string | 供应商名称 |
| BusinessManID | integer | 商户内码 |
| BusinessManName | string | 商户名称 |
| UserToken | string | 登录标识 |
| CityAuthority | string | 用户服务区权限（编码） |
| ServerpartIds | string | 服务区权限（内码） |
| ServerpartShopIds | string | 服务区门店权限 |
| SellerId | integer | 统一配送商户内码 |
| WarehouseId | string | 仓库内码 |
| UserPattern | integer | 数据模式（1000：业主；2000：商户） |
| SuperAdmin | integer | 超级管理员 |
| TopSystemRoleId | integer | 顶级系统角色 |
| EnabledRepeat | boolean | 是否允许重复登录 |
| totalCount | integer | 消息总条数 |
| unreadCount | integer | 未读消息条数 |
| UserModuleList | List<NestingModel[SYSTEMMENUModel]> | 用户模块权限 |

NestingModel[SYSTEMMENUModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | SYSTEMMENUModel | 结点 |
| children | List<NestingModel[SYSTEMMENUModel]> | 子级 |

SYSTEMMENUModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMENU_PID | integer | 系统菜单父级内码 |
| SYSTEMMENU_NAME | string | 系统菜单名称 |
| SYSTEMMENU_INDEX | integer | 系统菜单索引 |
| SYSTEMMENU_LEVEL | integer | 系统菜单级别 |
| SYSTEMMENU_ICO | string | 系统菜单图标 |
| SYSTEMMENU_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMENU_DESC | string | 备注说明 |
| SystemModuleList | List<SYSTEMMODULEModel> | 系统模块列表 |

SYSTEMMODULEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMODULE_ID | integer | 系统模块内码 |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMODULE_TYPE | integer | 系统模块类型 |
| SYSTEMMODULE_NAME | string | 系统模块名称 |
| SYSTEMMODULE_INDEX | integer | 系统模块索引 |
| SYSTEMMODULE_GUID | string | 模块唯一标识 |
| SYSTEMMODULE_URL | string | 系统模块地址 |
| SYSTEMMODULE_ICO | string | 系统模块图标 |
| SYSTEMMODULE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMODULE_DESC | string | 备注说明 |

---
### POST /Logging/UserLogout
**名称**: 用户登出
**Action**: `UserLogout`

**场景**: 
驿商云平台，在用户登出系统后，调用接口记录登出日志。
**说明**: 
用户登出，请求参数：用户登录token
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| token | string | Y | 用户token |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |

---
### POST /Logging/ModifyPasswordByPassport
**名称**: 根据用户账号修改密码
**Action**: `ModifyPasswordByPassport`

**场景**: 
用于 Logging 模块日志记录、查询与审计分析。
**说明**:
> ⚠️ **加密要求**: 该接口入参 `postData` 需进行 AES 加密转换。
> 
> **请求模式**:
> 1. 将业务参数构建为 JSON 字符串。
> 2. 使用 AES 算法对字符串加密。
> 3. 将密文作为 `value` 字段的值发送，格式如：`{"name": "", "value": "BASE64_ENCRYPTED_STRING"}`。
 
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：登录账号【PassportName】原密码【OriPassword】新密码【NewPassword】 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| value | string | 请求入参加密后的字符串 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 修改结果 |

## 系统数据字典相关接口【DictionaryController】

---
### POST /Dictionary/GetEXPLAINTYPEList
**名称**: 获取枚举类型列表
**Action**: `GetEXPLAINTYPEList`

**场景**: 
用于 Dictionary 模块字典数据维护与查询。
**说明**:
> ⚠️ **加密要求**: 该接口入参 `postData` 需进行 AES 加密转换。
> 
> **请求模式**:
> 1. 将业务参数构建为 JSON 字符串。
> 2. 使用 AES 算法对字符串加密。
> 3. 将密文作为 `value` 字段的值发送，格式如：`{"name": "", "value": "BASE64_ENCRYPTED_STRING"}`。
 
获取枚举类型列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：查询条件对象 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[EXPLAINTYPEModel]]> | 返回数据集合 |

JsonList[EXPLAINTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<EXPLAINTYPEModel> | 返回数据集 |

EXPLAINTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| EXPLAINTYPE_ID | integer | 分类内码 |
| EXPLAINTYPE_NAME | string | 分类名称 |
| EXPLAINTYPE_INDEX | integer | 分类索引 |
| EXPLAINTYPE_PID | integer | 上级分类 |
| EXPLAINTYPE_DESC | string | 说明 |

---
### POST /Dictionary/GetEXPLAINTYPEDetail
**名称**: 获取枚举类型明细
**Action**: `GetEXPLAINTYPEDetail`

**场景**: 
用于 Dictionary 模块字典数据维护与查询。
**说明**:
> ⚠️ **加密要求**: 该接口入参 `postData` 需进行 AES 加密转换。
> 
> **请求模式**:
> 1. 将业务参数构建为 JSON 字符串。
> 2. 使用 AES 算法对字符串加密。
> 3. 将密文作为 `value` 字段的值发送，格式如：`{"name": "", "value": "BASE64_ENCRYPTED_STRING"}`。
 
获取枚举类型明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：枚举类型内码【EXPLAINTYPEId】 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[EXPLAINTYPEModel]> | 返回数据集合 |

EXPLAINTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| EXPLAINTYPE_ID | integer | 分类内码 |
| EXPLAINTYPE_NAME | string | 分类名称 |
| EXPLAINTYPE_INDEX | integer | 分类索引 |
| EXPLAINTYPE_PID | integer | 上级分类 |
| EXPLAINTYPE_DESC | string | 说明 |

---
### POST /Dictionary/GetFIELDEXPLAINList
**名称**: 获取字段类型列表
**Action**: `GetFIELDEXPLAINList`

**场景**: 
用于 Dictionary 模块字典数据维护与查询。
**说明**:
> ⚠️ **加密要求**: 该接口入参 `postData` 需进行 AES 加密转换。
> 
> **请求模式**:
> 1. 将业务参数构建为 JSON 字符串。
> 2. 使用 AES 算法对字符串加密。
> 3. 将密文作为 `value` 字段的值发送，格式如：`{"name": "", "value": "BASE64_ENCRYPTED_STRING"}`。
 
获取字段类型列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：查询条件对象 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[FIELDEXPLAINModel]]> | 返回数据集合 |

JsonList[FIELDEXPLAINModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<FIELDEXPLAINModel> | 返回数据集 |

FIELDEXPLAINModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| FIELDEXPLAIN_ID | integer | 字段内码 |
| EXPLAINTYPE_ID | integer | 分类内码 |
| FIELDEXPLAIN_NAME | string | 字段中文 |
| FIELDEXPLAIN_FIELD | string | 字段英文 |
| FIELDEXPLAIN_TYPE | string | 枚举类型 |
| FIELDEXPLAIN_INDEX | integer | 字段索引 |
| FIELDEXPLAIN_DESC | string | 说明 |

---
### POST /Dictionary/GetFIELDEXPLAINDetail
**名称**: 获取字段类型明细
**Action**: `GetFIELDEXPLAINDetail`

**场景**: 
用于 Dictionary 模块字典数据维护与查询。
**说明**:
> ⚠️ **加密要求**: 该接口入参 `postData` 需进行 AES 加密转换。
> 
> **请求模式**:
> 1. 将业务参数构建为 JSON 字符串。
> 2. 使用 AES 算法对字符串加密。
> 3. 将密文作为 `value` 字段的值发送，格式如：`{"name": "", "value": "BASE64_ENCRYPTED_STRING"}`。
 
获取字段类型明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：字段类型内码【FIELDEXPLAINId】 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[FIELDEXPLAINModel]> | 返回数据集合 |

FIELDEXPLAINModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| FIELDEXPLAIN_ID | integer | 字段内码 |
| EXPLAINTYPE_ID | integer | 分类内码 |
| FIELDEXPLAIN_NAME | string | 字段中文 |
| FIELDEXPLAIN_FIELD | string | 字段英文 |
| FIELDEXPLAIN_TYPE | string | 枚举类型 |
| FIELDEXPLAIN_INDEX | integer | 字段索引 |
| FIELDEXPLAIN_DESC | string | 说明 |

---
### POST /Dictionary/GetFIELDENUMList
**名称**: 获取字段枚举列表
**Action**: `GetFIELDENUMList`

**场景**: 
用于 Dictionary 模块字典数据维护与查询。
**说明**:
> ⚠️ **加密要求**: 该接口入参 `postData` 需进行 AES 加密转换。
> 
> **请求模式**:
> 1. 将业务参数构建为 JSON 字符串。
> 2. 使用 AES 算法对字符串加密。
> 3. 将密文作为 `value` 字段的值发送，格式如：`{"name": "", "value": "BASE64_ENCRYPTED_STRING"}`。
 
获取字段枚举列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：查询条件对象 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[FIELDENUMModel]]> | 返回数据集合 |

JsonMsg[JsonList[FIELDENUMModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[FIELDENUMModel] | 返回对象 |

JsonList[FIELDENUMModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<FIELDENUMModel> | 返回数据集 |

FIELDENUMModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| FIELDENUM_ID | integer | 枚举内码 |
| FIELDENUM_IDS | string | 枚举内码(查询条件) |
| FIELDEXPLAIN_ID | integer | 字段内码 |
| FIELDENUM_NAME | string | 枚举名称 |
| FIELDENUM_VALUE | string | 枚举值域 |
| FIELDENUM_VALUES | string | 枚举值域(查询条件) |
| FIELDENUM_KEY | string | 枚举键值 |
| FIELDENUM_INDEX | integer | 枚举索引 |
| FIELDENUM_STATUS | integer | 枚举状态 |
| FIELDENUM_PID | integer | 上级枚举 |
| FIELDENUM_DESC | string | 说明 |

---
### POST /Dictionary/GetFIELDENUMDetail
**名称**: 获取字段枚举明细
**Action**: `GetFIELDENUMDetail`

**场景**: 
用于 Dictionary 模块字典数据维护与查询。
**说明**:
> ⚠️ **加密要求**: 该接口入参 `postData` 需进行 AES 加密转换。
> 
> **请求模式**:
> 1. 将业务参数构建为 JSON 字符串。
> 2. 使用 AES 算法对字符串加密。
> 3. 将密文作为 `value` 字段的值发送，格式如：`{"name": "", "value": "BASE64_ENCRYPTED_STRING"}`。
 
获取字段枚举明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：字段枚举内码【FIELDENUMId】 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[FIELDENUMModel]> | 返回数据集合 |

FIELDENUMModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| FIELDENUM_ID | integer | 枚举内码 |
| FIELDENUM_IDS | string | 枚举内码(查询条件) |
| FIELDEXPLAIN_ID | integer | 字段内码 |
| FIELDENUM_NAME | string | 枚举名称 |
| FIELDENUM_VALUE | string | 枚举值域 |
| FIELDENUM_VALUES | string | 枚举值域(查询条件) |
| FIELDENUM_KEY | string | 枚举键值 |
| FIELDENUM_INDEX | integer | 枚举索引 |
| FIELDENUM_STATUS | integer | 枚举状态 |
| FIELDENUM_PID | integer | 上级枚举 |
| FIELDENUM_DESC | string | 说明 |

---
### GET/POST /Dictionary/GetFieEnumList
**名称**: 获取字段枚举
**Action**: `GetFieEnumList`

**场景**: 
用于 Dictionary 模块字典数据维护与查询。
**说明**: 
获取字段枚举
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| FieldEnum_ID | integer | N | 枚举内码 |
| FieldExplain_ID | integer | N | 字段内码 |
| FieldexPlain_Field | string | N | 字段名称 |
| FieldEnum_Value | string | N | 枚举值 |
| FieldEnum_Name | string | N | 枚举中文名称 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[FieldEnumModel]]> | 返回数据集合 |

JsonMsg[JsonList[FieldEnumModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[FieldEnumModel] | 返回对象 |

JsonList[FieldEnumModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<FieldEnumModel> | 返回数据集 |

FieldEnumModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| FieldEnum_ID | integer | 枚举内码 |
| FieldExplain_ID | integer | 字段内码 |
| FieldEnum_Name | string | 枚举名称 |
| FieldEnum_Value | string | 枚举值域 |
| FieldEnum_Key | string | 枚举键值 |
| FieldEnum_Index | integer | 枚举索引 |
| FieldEnum_Status | integer | 枚举状态 |
| FieldEnum_PID | integer | 上级枚举 |
| FieldEnum_Desc | string | 说明 |
| FieldEnum_Date | string | 操作时间 |

---
### GET /Dictionary/GetNestingEXPLAINTYPEList
**名称**: 获取枚举类型嵌套列表
**Action**: `GetNestingEXPLAINTYPEList`

**场景**: 
用于 Dictionary 模块字典数据维护与查询。
**说明**: 
获取枚举类型嵌套列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| EXPLAINTYPE_PID | string | N | 上级分类 |
| SearchKey | string | N | 模糊查询内容 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[EXPLAINTYPEModel]]]> | 返回数据集合 |

JsonList[NestingModel[EXPLAINTYPEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[EXPLAINTYPEModel]> | 返回数据集 |

NestingModel[EXPLAINTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | EXPLAINTYPEModel | 结点 |
| children | List<NestingModel[EXPLAINTYPEModel]> | 子级 |

EXPLAINTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| EXPLAINTYPE_ID | integer | 分类内码 |
| EXPLAINTYPE_NAME | string | 分类名称 |
| EXPLAINTYPE_INDEX | integer | 分类索引 |
| EXPLAINTYPE_PID | integer | 上级分类 |
| EXPLAINTYPE_DESC | string | 说明 |

---
### GET /Dictionary/GetNestingEXPLAINTYPETree
**名称**: 获取枚举类型嵌套树
**Action**: `GetNestingEXPLAINTYPETree`

**场景**: 
用于 Dictionary 模块字典数据维护与查询。
**说明**: 
获取枚举类型嵌套树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| EXPLAINTYPE_PID | string | N | 上级分类 |
| SearchKey | string | N | 模糊查询内容 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### POST /Dictionary/GetNestingFIELDENUMList
**名称**: 获取字段枚举嵌套列表
**Action**: `GetNestingFIELDENUMList`

**场景**: 
用于 Dictionary 模块字典数据维护与查询。
**说明**:
> ⚠️ **加密要求**: 该接口入参 `postData` 需进行 AES 加密转换。
> 
> **请求模式**:
> 1. 将业务参数构建为 JSON 字符串。
> 2. 使用 AES 算法对字符串加密。
> 3. 将密文作为 `value` 字段的值发送，格式如：`{"name": "", "value": "BASE64_ENCRYPTED_STRING"}`。
 
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：字典名称【FIELDEXPLAIN_FIELD】字典内码【FIELDEXPLAIN_ID】上级枚举【FIELDENUM_PID】有效状态【FIELDENUM_STATUS】模糊查询内容【SearchKey】 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[FIELDENUMModel]]]> | 返回数据集合 |

JsonList[NestingModel[FIELDENUMModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[FIELDENUMModel]> | 返回数据集 |

NestingModel[FIELDENUMModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | FIELDENUMModel | 结点 |
| children | List<NestingModel[FIELDENUMModel]> | 子级 |

FIELDENUMModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| FIELDENUM_ID | integer | 枚举内码 |
| FIELDENUM_IDS | string | 枚举内码(查询条件) |
| FIELDEXPLAIN_ID | integer | 字段内码 |
| FIELDENUM_NAME | string | 枚举名称 |
| FIELDENUM_VALUE | string | 枚举值域 |
| FIELDENUM_VALUES | string | 枚举值域(查询条件) |
| FIELDENUM_KEY | string | 枚举键值 |
| FIELDENUM_INDEX | integer | 枚举索引 |
| FIELDENUM_STATUS | integer | 枚举状态 |
| FIELDENUM_PID | integer | 上级枚举 |
| FIELDENUM_DESC | string | 说明 |

---
### POST /Dictionary/GetNestingFIELDENUMTree
**名称**: 获取字段枚举嵌套树
**Action**: `GetNestingFIELDENUMTree`

**场景**: 
用于 Dictionary 模块字典数据维护与查询。
**说明**:
> ⚠️ **加密要求**: 该接口入参 `postData` 需进行 AES 加密转换。
> 
> **请求模式**:
> 1. 将业务参数构建为 JSON 字符串。
> 2. 使用 AES 算法对字符串加密。
> 3. 将密文作为 `value` 字段的值发送，格式如：`{"name": "", "value": "BASE64_ENCRYPTED_STRING"}`。
 
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：字典名称【FIELDEXPLAIN_FIELD】字典内码【FIELDEXPLAIN_ID】上级枚举【FIELDENUM_PID】有效状态【FIELDENUM_STATUS】模糊查询内容【SearchKey】 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

## 系统框架相关接口【FrameWorkController】

---
### GET /FrameWork/GetFieldEnumByField
**名称**: 绑定枚举下拉框
**Action**: `GetFieldEnumByField`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
绑定枚举下拉框
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| FieldExplainField | string | Y | 字段名称商品状态：COMMODITYSTATE质量等级：COMMODITYGRADE是否散装：ISBULK称重方式/计量方式：METERINGMETHOD商品业态/门店业态：BUSINESSTYPE门店方位：SHOPREGION人员类型：CASHWORKER_TYPE有效状态：ISVALID |
| FieldEnumStatus | string | N | 有效状态0：无效1：有效2：有效不可选 |
| FieldEnumValue | string | N | 枚举值 |
| ProvinceCode | integer | N | 用户省份编码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[CommonModel]]> | 返回数据集合 |

JsonMsg[JsonList[CommonModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[CommonModel] | 返回对象 |

JsonList[CommonModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<CommonModel> | 返回数据集 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

---
### GET /FrameWork/GetFieldEnumTree
**名称**: 绑定枚举树
**Action**: `GetFieldEnumTree`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
绑定枚举树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| FieldExplainField | string | Y | 枚举字段名称 |
| FieldEnumPID | integer | N | 父级枚举内码 |
| FieldEnumStatus | boolean | N | 是否只查询有效数据 |
| DataType | integer | N | 数据类型【默认0】：<br />0【返回枚举值】<br />1【返回枚举内码】 |
| ShowChild | boolean | N | 是否显示子集，默认显示 |
| SearchKey | string | N | 模糊查询条件 |
| ShowWholePower | boolean | N | 显示全局权限 |
| ServerpartId | string | N | 服务区内码，用于查询服务区商品业态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[LabelValueModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[LabelValueModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[LabelValueModel]] | 返回对象 |

JsonList[NestingModel[LabelValueModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[LabelValueModel]> | 返回数据集 |

NestingModel[LabelValueModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | LabelValueModel | 结点 |
| children | List<NestingModel[LabelValueModel]> | 子级 |

LabelValueModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | number | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| ico | string | 图标地址 |
| index | integer | 数据索引 |

---
### GET /FrameWork/BindingSystemRoleDDL
**名称**: 获取系统角色下拉框
**Action**: `BindingSystemRoleDDL`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取系统角色下拉框
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SystemRolePID | integer | N | 系统角色父级内码 |
| ShowStatus | boolean | N | 是否只查询有效数据 |
| ProvinceCode | integer | N | 角色所属省份编码 |
| SystemRole_Type | integer | N | 角色类型：1000【模块角色】2000【账号角色】 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonPidModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonPidModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonPidModel]] | 返回对象 |

JsonList[NestingModel[CommonPidModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonPidModel]> | 返回数据集 |

NestingModel[CommonPidModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonPidModel | 结点 |
| children | List<NestingModel[CommonPidModel]> | 子级 |

CommonPidModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| pid | integer | 上级类别内码 |
| level | integer | 类别等级 |

---
### POST /FrameWork/ChangeUserHeadImg
**名称**: 上传账户头像
**Action**: `ChangeUserHeadImg`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
上传账户头像
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| User_Id_Encrypted | string | Y | 账户加密内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |

---
### GET /FrameWork/GetAntdRouteList
**名称**: 获取antd框架路由嵌套列表
**Action**: `GetAntdRouteList`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取antd框架路由嵌套列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| AntdRoutePID | integer | N | 父级框架路由内码 |
| RouteStatus | string | N | 数据状态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[ANTDROUTEModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[ANTDROUTEModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[ANTDROUTEModel]] | 返回对象 |

JsonList[NestingModel[ANTDROUTEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[ANTDROUTEModel]> | 返回数据集 |

NestingModel[ANTDROUTEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | ANTDROUTEModel | 结点 |
| children | List<NestingModel[ANTDROUTEModel]> | 子级 |

ANTDROUTEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ANTDROUTE_ID | integer | 路由内码 |
| ANTDROUTE_PID | integer | 父级内码 |
| ANTDROUTE_PATH | string | 相对路径 |
| ANTDROUTE_NAME | string | 路由名称 |
| ANTDROUTE_COMPONENT | string | 组件地址 |
| ANTDROUTE_AUTHORITY | string | 权限配置 |
| ANTDROUTE_ICON | string | 图标地址 |
| ANTDROUTE_INDEX | integer | 显示索引 |
| ANTDROUTE_VISIBLE | integer | 显示菜单(0：隐藏；1：显示) |
| ANTDROUTE_REDIRECT | string | 重定向地址 |
| ANTDROUTE_STATE | integer | 有效状态 |
| OPERATE_DATE | string | 操作时间 |
| ANTDROUTE_DESC | string | 备注说明 |

---
### GET /FrameWork/GetAntdRouteTree
**名称**: 获取系统路由树
**Action**: `GetAntdRouteTree`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取系统路由树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| AntdRoutePID | integer | N | 父级框架路由内码 |
| RouteStatus | string | N | 数据状态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeTreeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeTreeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeTreeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeTreeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeTreeModel]> | 返回数据集 |

NestingModel[CommonTypeTreeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeTreeModel | 结点 |
| children | List<NestingModel[CommonTypeTreeModel]> | 子级 |

CommonTypeTreeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| ico | string | 图标地址 |
| desc | string | 额外描述内容 |
| children | List<CommonTypeModel> | 子集列表 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /FrameWork/GetCUSTOMTYPEDetail
**名称**: 获取用户自定义类别表明细
**Action**: `GetCUSTOMTYPEDetail`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取用户自定义类别表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| CUSTOMTYPEId | integer | Y | 用户自定义类别表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[CUSTOMTYPEModel]> | 返回数据集合 |

JsonMsg[CUSTOMTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | CUSTOMTYPEModel | 返回对象 |

CUSTOMTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| CUSTOMTYPE_ID | integer | 自定义类别内码 |
| CUSTOMTYPE_PID | integer | 自定义类别父级内码 |
| CUSTOMTYPE_NAME | string | 自定义类别名称 |
| CUSTOMTYPE_CODE | string | 自定义类别代码 |
| CUSTOMTYPE_INDEX | integer | 自定义类别索引 |
| CUSTOMTYPE_TYPE | integer | 类别类型 |
| CUSTOMTYPE_TYPENAME | string | 类型名称 |
| BUSINESSMAN_ID | integer | 商户内码 |
| BELONGUSER_ID | integer | 所属人内码 |
| SERVERPART_ID | integer | 服务区内码 |
| OWNERUNIT_ID | integer | 业主单位内码 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人名称 |
| OPERATE_DATE | string | 操作时间 |
| CUSTOMTYPE_STATE | integer | 有效状态 |
| CUSTOMTYPE_DESC | string | 备注说明 |

---
### POST /FrameWork/GetCUSTOMTYPEList
**名称**: 获取用户自定义类别表列表
**Action**: `GetCUSTOMTYPEList`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取用户自定义类别表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[CUSTOMTYPEModel] | Y | 查询条件对象 |

SearchModel[CUSTOMTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式0:模糊查询，1:精确查询 |
| SearchParameter | CUSTOMTYPEModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

CUSTOMTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| CUSTOMTYPE_ID | integer | 自定义类别内码 |
| CUSTOMTYPE_PID | integer | 自定义类别父级内码 |
| CUSTOMTYPE_NAME | string | 自定义类别名称 |
| CUSTOMTYPE_CODE | string | 自定义类别代码 |
| CUSTOMTYPE_INDEX | integer | 自定义类别索引 |
| CUSTOMTYPE_TYPE | integer | 类别类型 |
| CUSTOMTYPE_TYPENAME | string | 类型名称 |
| BUSINESSMAN_ID | integer | 商户内码 |
| BELONGUSER_ID | integer | 所属人内码 |
| SERVERPART_ID | integer | 服务区内码 |
| OWNERUNIT_ID | integer | 业主单位内码 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人名称 |
| OPERATE_DATE | string | 操作时间 |
| CUSTOMTYPE_STATE | integer | 有效状态 |
| CUSTOMTYPE_DESC | string | 备注说明 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[CUSTOMTYPEModel]]> | 返回数据集合 |

JsonMsg[JsonList[CUSTOMTYPEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[CUSTOMTYPEModel] | 返回对象 |

JsonList[CUSTOMTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<CUSTOMTYPEModel> | 返回数据集 |

CUSTOMTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| CUSTOMTYPE_ID | integer | 自定义类别内码 |
| CUSTOMTYPE_PID | integer | 自定义类别父级内码 |
| CUSTOMTYPE_NAME | string | 自定义类别名称 |
| CUSTOMTYPE_CODE | string | 自定义类别代码 |
| CUSTOMTYPE_INDEX | integer | 自定义类别索引 |
| CUSTOMTYPE_TYPE | integer | 类别类型 |
| CUSTOMTYPE_TYPENAME | string | 类型名称 |
| BUSINESSMAN_ID | integer | 商户内码 |
| BELONGUSER_ID | integer | 所属人内码 |
| SERVERPART_ID | integer | 服务区内码 |
| OWNERUNIT_ID | integer | 业主单位内码 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人名称 |
| OPERATE_DATE | string | 操作时间 |
| CUSTOMTYPE_STATE | integer | 有效状态 |
| CUSTOMTYPE_DESC | string | 备注说明 |

---
### GET /FrameWork/GetCustomTypeDDL
**名称**: 获取用户自定义类别树
**Action**: `GetCustomTypeDDL`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取用户自定义类别树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| CustomType | integer | Y | 数据分类，字段值参照字典CUSTOMTYPE_TYPE |
| BusinessManId | integer | Y | 用户内码 |
| BelongStaffId | integer | N | 归属人内码 |
| CustomTypePID | integer | N | 父级用户自定义类别内码 |
| ShowStatus | boolean | N | 是否只查询有效数据 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonPidModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonPidModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonPidModel]] | 返回对象 |

JsonList[NestingModel[CommonPidModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonPidModel]> | 返回数据集 |

NestingModel[CommonPidModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonPidModel | 结点 |
| children | List<NestingModel[CommonPidModel]> | 子级 |

CommonPidModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| pid | integer | 上级类别内码 |
| level | integer | 类别等级 |

---
### GET /FrameWork/GetMerchantShopTree
**名称**: 获取商户门店权限树
**Action**: `GetMerchantShopTree`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取商户门店权限树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessManId | integer | N | 商户内码 |
| ProvinceCode | integer | N | 省份编码 |
| UserId | integer | N | 用户账号内码 |
| ShowShop | boolean | N | 是否显示门店树 |
| ShowState | boolean | N | 是否显示门店经营状态 |
| ServerpartShopId | string | N | 门店权限集合 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[LabelValueModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[LabelValueModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[LabelValueModel]] | 返回对象 |

JsonList[NestingModel[LabelValueModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[LabelValueModel]> | 返回数据集 |

NestingModel[LabelValueModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | LabelValueModel | 结点 |
| children | List<NestingModel[LabelValueModel]> | 子级 |

LabelValueModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | number | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| ico | string | 图标地址 |
| index | integer | 数据索引 |

---
### GET /FrameWork/GetNestingCustomTypeLsit
**名称**: 获取用户自定义类别嵌套列表
**Action**: `GetNestingCustomTypeLsit`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取用户自定义类别嵌套列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| CustomType | integer | Y | 数据分类，字段值参照字典CUSTOMTYPE_TYPE |
| BusinessManId | integer | N | 用户内码 |
| BelongStaffId | integer | N | 归属人内码 |
| CustomTypePID | integer | N | 父级用户自定义类别内码 |
| ShowStatus | boolean | N | 是否只查询有效数据 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CUSTOMTYPEModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CUSTOMTYPEModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CUSTOMTYPEModel]] | 返回对象 |

JsonList[NestingModel[CUSTOMTYPEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CUSTOMTYPEModel]> | 返回数据集 |

NestingModel[CUSTOMTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CUSTOMTYPEModel | 结点 |
| children | List<NestingModel[CUSTOMTYPEModel]> | 子级 |

CUSTOMTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| CUSTOMTYPE_ID | integer | 自定义类别内码 |
| CUSTOMTYPE_PID | integer | 自定义类别父级内码 |
| CUSTOMTYPE_NAME | string | 自定义类别名称 |
| CUSTOMTYPE_CODE | string | 自定义类别代码 |
| CUSTOMTYPE_INDEX | integer | 自定义类别索引 |
| CUSTOMTYPE_TYPE | integer | 类别类型 |
| CUSTOMTYPE_TYPENAME | string | 类型名称 |
| BUSINESSMAN_ID | integer | 商户内码 |
| BELONGUSER_ID | integer | 所属人内码 |
| SERVERPART_ID | integer | 服务区内码 |
| OWNERUNIT_ID | integer | 业主单位内码 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人名称 |
| OPERATE_DATE | string | 操作时间 |
| CUSTOMTYPE_STATE | integer | 有效状态 |
| CUSTOMTYPE_DESC | string | 备注说明 |

---
### GET /FrameWork/GetServerpartTree
**名称**: 获取服务区权限树
**Action**: `GetServerpartTree`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取服务区权限树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | N | 省份编码 |
| ShowStatus | boolean | N | 是否只查询有效数据 |
| DataType | integer | N | 数据类型：<br />0【返回枚举值】，1【返回枚举内码】 |
| ShowChild | boolean | N | 是否显示子集，默认显示 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[LabelValueModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[LabelValueModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[LabelValueModel]] | 返回对象 |

JsonList[NestingModel[LabelValueModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[LabelValueModel]> | 返回数据集 |

NestingModel[LabelValueModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | LabelValueModel | 结点 |
| children | List<NestingModel[LabelValueModel]> | 子级 |

LabelValueModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | number | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| ico | string | 图标地址 |
| index | integer | 数据索引 |

---
### GET /FrameWork/GetSystemMenuLsit
**名称**: 获取系统菜单嵌套列表
**Action**: `GetSystemMenuLsit`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取系统菜单嵌套列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SystemMenuPID | integer | N | 父级系统菜单内码 |
| MenuStatus | string | N | 查询模块状态 |
| ShowStatus | boolean | N | 是否只查询有效数据 |
| ShowModule | boolean | N | 是否显示模块列表 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[SYSTEMMENUModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[SYSTEMMENUModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[SYSTEMMENUModel]] | 返回对象 |

JsonList[NestingModel[SYSTEMMENUModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[SYSTEMMENUModel]> | 返回数据集 |

NestingModel[SYSTEMMENUModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | SYSTEMMENUModel | 结点 |
| children | List<NestingModel[SYSTEMMENUModel]> | 子级 |

SYSTEMMENUModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMENU_PID | integer | 系统菜单父级内码 |
| SYSTEMMENU_NAME | string | 系统菜单名称 |
| SYSTEMMENU_INDEX | integer | 系统菜单索引 |
| SYSTEMMENU_LEVEL | integer | 系统菜单级别 |
| SYSTEMMENU_ICO | string | 系统菜单图标 |
| SYSTEMMENU_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMENU_DESC | string | 备注说明 |
| SystemModuleList | List<SYSTEMMODULEModel> | 系统模块列表 |

SYSTEMMODULEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMODULE_ID | integer | 系统模块内码 |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMODULE_TYPE | integer | 系统模块类型 |
| SYSTEMMODULE_NAME | string | 系统模块名称 |
| SYSTEMMODULE_INDEX | integer | 系统模块索引 |
| SYSTEMMODULE_GUID | string | 模块唯一标识 |
| SYSTEMMODULE_URL | string | 系统模块地址 |
| SYSTEMMODULE_ICO | string | 系统模块图标 |
| SYSTEMMODULE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMODULE_DESC | string | 备注说明 |

---
### GET /FrameWork/GetSystemMenuTree
**名称**: 获取系统菜单树
**Action**: `GetSystemMenuTree`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取系统菜单树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SystemMenuPID | integer | N | 父级系统菜单内码 |
| ShowStatus | boolean | N | 是否只查询有效数据 |
| ShowModule | boolean | N | 是否显示模块列表 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeTreeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeTreeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeTreeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeTreeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeTreeModel]> | 返回数据集 |

NestingModel[CommonTypeTreeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeTreeModel | 结点 |
| children | List<NestingModel[CommonTypeTreeModel]> | 子级 |

CommonTypeTreeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| ico | string | 图标地址 |
| desc | string | 额外描述内容 |
| children | List<CommonTypeModel> | 子集列表 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /FrameWork/GetSystemRoleCount
**名称**: 获取系统角色分类数量
**Action**: `GetSystemRoleCount`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取系统角色分类数量
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | N | 省份编码 |
| SystemRole_Type | integer | N | 角色类型：1000【模块角色】2000【账号角色】 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[PatternCountModel]> | 返回数据集合 |

JsonMsg[PatternCountModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | PatternCountModel | 返回对象 |

PatternCountModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| OwnerUnitCount | integer | 业主单位数据分类数量 |
| SupplierCount | integer | 供应商用户分类数量 |
| MerchantCount | integer | 商家用户分类数量 |
| TouristCount | integer | 游客分类数量 |
| AdminCount | integer | 内部人员分类数量 |

---
### GET /FrameWork/GetSystemRoleList
**名称**: 获取系统角色菜单嵌套列表
**Action**: `GetSystemRoleList`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取系统角色菜单嵌套列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SystemRolePID | integer | N | 系统角色父级内码 |
| ShowStatus | boolean | N | 是否只查询有效数据 |
| ProvinceCode | integer | N | 角色所属省份编码 |
| SystemRolePattern | string | N | 数据模式：1000【业主】2000【商户】 |
| SystemRole_Name | string | N | 系统角色名称（模糊查询） |
| SystemRole_Type | integer | N | 角色类型：1000【模块角色】2000【账号角色】 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[SYSTEMROLEModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[SYSTEMROLEModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[SYSTEMROLEModel]] | 返回对象 |

JsonList[NestingModel[SYSTEMROLEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[SYSTEMROLEModel]> | 返回数据集 |

NestingModel[SYSTEMROLEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | SYSTEMROLEModel | 结点 |
| children | List<NestingModel[SYSTEMROLEModel]> | 子级 |

SYSTEMROLEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMROLE_ID | integer | 系统角色内码 |
| SYSTEMROLE_PID | integer | 系统角色父级内码 |
| SYSTEMROLE_TYPE | integer | 系统角色类型 |
| SYSTEMROLE_PROVINCE | integer | 角色所属省份 |
| SYSTEMROLE_BUSINESS | integer | 角色所属商户 |
| SYSTEMROLE_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| SYSTEMROLE_NAME | string | 系统角色名称 |
| SYSTEMROLE_LEVEL | integer | 系统角色级别 |
| SYSTEMROLE_INDEX | integer | 系统角色索引 |
| SYSTEMROLE_ICO | string | 系统角色图标 |
| SYSTEMROLE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMROLE_DESC | string | 备注说明 |
| SystemModuleList | List<integer> | 角色模块权限数组 |
| UserIds | List<integer> | 用户IDs |
| UserTypeIds | List<integer> | 用户分类IDs |
| UserNames | List<string> | 用户名称s |

---
### GET /FrameWork/GetSystemRoleModuleTree
**名称**: 获取系统角色菜单树
**Action**: `GetSystemRoleModuleTree`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取系统角色菜单树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SystemRoleId | string | Y | 系统角色内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeTreeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeTreeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeTreeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeTreeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeTreeModel]> | 返回数据集 |

NestingModel[CommonTypeTreeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeTreeModel | 结点 |
| children | List<NestingModel[CommonTypeTreeModel]> | 子级 |

CommonTypeTreeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| ico | string | 图标地址 |
| desc | string | 额外描述内容 |
| children | List<CommonTypeModel> | 子集列表 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /FrameWork/GetUserModuleList
**名称**: 获取账户菜单树
**Action**: `GetUserModuleList`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取账户菜单树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| UserId | integer | Y | 账户内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[SYSTEMMENUModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[SYSTEMMENUModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[SYSTEMMENUModel]] | 返回对象 |

JsonList[NestingModel[SYSTEMMENUModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[SYSTEMMENUModel]> | 返回数据集 |

NestingModel[SYSTEMMENUModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | SYSTEMMENUModel | 结点 |
| children | List<NestingModel[SYSTEMMENUModel]> | 子级 |

SYSTEMMENUModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMENU_PID | integer | 系统菜单父级内码 |
| SYSTEMMENU_NAME | string | 系统菜单名称 |
| SYSTEMMENU_INDEX | integer | 系统菜单索引 |
| SYSTEMMENU_LEVEL | integer | 系统菜单级别 |
| SYSTEMMENU_ICO | string | 系统菜单图标 |
| SYSTEMMENU_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMENU_DESC | string | 备注说明 |
| SystemModuleList | List<SYSTEMMODULEModel> | 系统模块列表 |

SYSTEMMODULEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMODULE_ID | integer | 系统模块内码 |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMODULE_TYPE | integer | 系统模块类型 |
| SYSTEMMODULE_NAME | string | 系统模块名称 |
| SYSTEMMODULE_INDEX | integer | 系统模块索引 |
| SYSTEMMODULE_GUID | string | 模块唯一标识 |
| SYSTEMMODULE_URL | string | 系统模块地址 |
| SYSTEMMODULE_ICO | string | 系统模块图标 |
| SYSTEMMODULE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMODULE_DESC | string | 备注说明 |

---
### GET /FrameWork/GetUserShopTree
**名称**: 获取用户门店权限树
**Action**: `GetUserShopTree`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取用户门店权限树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| UserId | integer | Y | 用户内码 |
| ShowShop | boolean | N | 是否显示门店树 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[LabelValueModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[LabelValueModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[LabelValueModel]] | 返回对象 |

JsonList[NestingModel[LabelValueModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[LabelValueModel]> | 返回数据集 |

NestingModel[LabelValueModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | LabelValueModel | 结点 |
| children | List<NestingModel[LabelValueModel]> | 子级 |

LabelValueModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | number | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| ico | string | 图标地址 |
| index | integer | 数据索引 |

---
### GET /FrameWork/GetUserSystemRoleTree
**名称**: 获取用户系统角色权限树
**Action**: `GetUserSystemRoleTree`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取用户系统角色权限树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| UserId | integer | Y | 用户内码 |
| ShowStatus | boolean | N | 是否只查询有效数据 |
| SystemRole_Type | integer | N | 角色类型：1000【模块角色】2000【账号角色】 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonPidModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonPidModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonPidModel]] | 返回对象 |

JsonList[NestingModel[CommonPidModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonPidModel]> | 返回数据集 |

NestingModel[CommonPidModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonPidModel | 结点 |
| children | List<NestingModel[CommonPidModel]> | 子级 |

CommonPidModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| pid | integer | 上级类别内码 |
| level | integer | 类别等级 |

---
### GET /FrameWork/GetUserTypeCount
**名称**: 获取部门分类数量
**Action**: `GetUserTypeCount`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取部门分类数量
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | N | 省份编码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[PatternCountModel]> | 返回数据集合 |

JsonMsg[PatternCountModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | PatternCountModel | 返回对象 |

PatternCountModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| OwnerUnitCount | integer | 业主单位数据分类数量 |
| SupplierCount | integer | 供应商用户分类数量 |
| MerchantCount | integer | 商家用户分类数量 |
| TouristCount | integer | 游客分类数量 |
| AdminCount | integer | 内部人员分类数量 |

---
### GET /FrameWork/GetUserTypeList
**名称**: 获取账户分类嵌套列表
**Action**: `GetUserTypeList`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取账户分类嵌套列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| UserTypePattern | integer | N | 数据模式：1000【业主】，2000【商户】 |
| ProvinceCode | integer | N | 省份编码 |
| UserTypePID | integer | N | 父级账户分类内码 |
| ShowStatus | boolean | N | 是否只查询有效数据 |
| ShowUser | boolean | N | 是否显示账户列表 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[USERTYPEModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[USERTYPEModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[USERTYPEModel]] | 返回对象 |

JsonList[NestingModel[USERTYPEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[USERTYPEModel]> | 返回数据集 |

NestingModel[USERTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | USERTYPEModel | 结点 |
| children | List<NestingModel[USERTYPEModel]> | 子级 |

USERTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USERTYPE_ID | integer | 用户类型内码 |
| USERTYPE_NAME | string | 用户类型名称 |
| USERTYPE_PID | integer | 用户类型父级内码 |
| USERTYPE_INDEX | integer | 用户类型索引 |
| USERTYPE_LEVEL | integer | 用户类型级别 |
| USERTYPE_GUID | string | 用户类型唯一标识 |
| USERTYPE_ICO | string | 用户类型图标 |
| USERTYPE_PROVINCE | integer | 所属省份 |
| USERTYPE_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| USERTYPE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| USERTYPE_DESC | string | 备注说明 |
| UserList | List<USERModel> | 用户列表 |

USERModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USER_ID | integer | 用户内码 |
| USER_IDS | string | 用户内码S |
| USER_ID_Encrypted | string | 用户内码（加密） |
| USERTYPE_ID | integer | 用户类型内码 |
| UserTypeIds | string | 用户类型内码集合 |
| USER_NAME | string | 用户名称 |
| USER_PASSPORT | string | 登录账户 |
| USER_PASSWORD | string | 账户密码 |
| USER_TIMEOUT | integer | 有效时间 |
| USER_INDEX | integer | 显示顺序 |
| USER_INDEFINIT | integer | 用户类型 |
| USER_EXPIRY | string | 授权时间 |
| USER_CITYAUTHORITY | string | 服务区权限 |
| USER_REPEATLOGON | integer | 允许重复登录 |
| USER_MOBILEPHONE | string | 手机号码 |
| USER_PROVINCE | integer | 用户省份 |
| PROVINCE_UNIT | string | 业主单位 |
| BUSINESSMAN_ID | integer | 商户内码 |
| BUSINESSMAN_IDS | string | 商户内码（查询条件） |
| BUSINESSMAN_NAME | string | 商户名称 |
| USER_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| SUPER_ADMIN | integer | 是否超级管理员（0：否；1：是） |
| USER_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| USER_DESC | string | 备注说明 |
| USER_HEADIMGURL | string | 用户头像地址 |
| IDENTITY_CODE | string | 短信验证码 |
| ServerpartIds | string | 用户服务区权限(查询条件) |
| ServerpartList | List<string> | 用户服务区权限列表 |
| ServerpartShopList | List<integer> | 用户服务区门店权限列表（内码） |
| ShopNameList | List<string> | 用户服务区门店权限列表（名称） |
| SystemRoleList | List<integer> | 用户角色权限列表 |
| AnalysisPermission | boolean | 是否有驿达看板权限 |
| PushPermission | boolean | 是否有微信推送权限 |
| PushList | List<CommonTypeModel> | 微信推送权限列表 |
| SYSTEMROLE_IDS | string | 系统角色内码 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /FrameWork/GetUserTypeTree
**名称**: 获取账户分类树
**Action**: `GetUserTypeTree`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
获取账户分类树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| UserTypePattern | integer | N | 数据模式：1000【业主】，2000【商户】 |
| ProvinceCode | integer | N | 省份编码 |
| UserTypePID | integer | N | 父级账户分类内码 |
| ShowStatus | boolean | N | 是否只查询有效数据 |
| ShowUser | boolean | N | 是否显示账户列表 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeTreeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeTreeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeTreeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeTreeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeTreeModel]> | 返回数据集 |

NestingModel[CommonTypeTreeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeTreeModel | 结点 |
| children | List<NestingModel[CommonTypeTreeModel]> | 子级 |

CommonTypeTreeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| ico | string | 图标地址 |
| desc | string | 额外描述内容 |
| children | List<CommonTypeModel> | 子集列表 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### POST /FrameWork/ModifyUserInfo
**名称**: 更新账户信息
**Action**: `名称、密码、手机号码`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
---
### POST /FrameWork/ModifyUserInfo
**名称**: 更新账户信息
**Action**: `名称、密码、手机号码`

#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| userModel | USERModel | Y | 用户model |

USERModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USER_ID | integer | 用户内码 |
| USER_IDS | string | 用户内码S |
| USER_ID_Encrypted | string | 用户内码（加密） |
| USERTYPE_ID | integer | 用户类型内码 |
| UserTypeIds | string | 用户类型内码集合 |
| USER_NAME | string | 用户名称 |
| USER_PASSPORT | string | 登录账户 |
| USER_PASSWORD | string | 账户密码 |
| USER_TIMEOUT | integer | 有效时间 |
| USER_INDEX | integer | 显示顺序 |
| USER_INDEFINIT | integer | 用户类型 |
| USER_EXPIRY | string | 授权时间 |
| USER_CITYAUTHORITY | string | 服务区权限 |
| USER_REPEATLOGON | integer | 允许重复登录 |
| USER_MOBILEPHONE | string | 手机号码 |
| USER_PROVINCE | integer | 用户省份 |
| PROVINCE_UNIT | string | 业主单位 |
| BUSINESSMAN_ID | integer | 商户内码 |
| BUSINESSMAN_IDS | string | 商户内码（查询条件） |
| BUSINESSMAN_NAME | string | 商户名称 |
| USER_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| SUPER_ADMIN | integer | 是否超级管理员（0：否；1：是） |
| USER_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| USER_DESC | string | 备注说明 |
| USER_HEADIMGURL | string | 用户头像地址 |
| IDENTITY_CODE | string | 短信验证码 |
| ServerpartIds | string | 用户服务区权限(查询条件) |
| ServerpartList | List<string> | 用户服务区权限列表 |
| ServerpartShopList | List<integer> | 用户服务区门店权限列表（内码） |
| ShopNameList | List<string> | 用户服务区门店权限列表（名称） |
| SystemRoleList | List<integer> | 用户角色权限列表 |
| AnalysisPermission | boolean | 是否有驿达看板权限 |
| PushPermission | boolean | 是否有微信推送权限 |
| PushList | List<CommonTypeModel> | 微信推送权限列表 |
| SYSTEMROLE_IDS | string | 系统角色内码 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |

---
### POST /FrameWork/ModifyUserMobilePhone
**名称**: 更新账户手机号码
**Action**: `ModifyUserMobilePhone`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
更新账户手机号码
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| userModel | USERModel | Y | 用户model |

USERModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USER_ID | integer | 用户内码 |
| USER_IDS | string | 用户内码S |
| USER_ID_Encrypted | string | 用户内码（加密） |
| USERTYPE_ID | integer | 用户类型内码 |
| UserTypeIds | string | 用户类型内码集合 |
| USER_NAME | string | 用户名称 |
| USER_PASSPORT | string | 登录账户 |
| USER_PASSWORD | string | 账户密码 |
| USER_TIMEOUT | integer | 有效时间 |
| USER_INDEX | integer | 显示顺序 |
| USER_INDEFINIT | integer | 用户类型 |
| USER_EXPIRY | string | 授权时间 |
| USER_CITYAUTHORITY | string | 服务区权限 |
| USER_REPEATLOGON | integer | 允许重复登录 |
| USER_MOBILEPHONE | string | 手机号码 |
| USER_PROVINCE | integer | 用户省份 |
| PROVINCE_UNIT | string | 业主单位 |
| BUSINESSMAN_ID | integer | 商户内码 |
| BUSINESSMAN_IDS | string | 商户内码（查询条件） |
| BUSINESSMAN_NAME | string | 商户名称 |
| USER_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| SUPER_ADMIN | integer | 是否超级管理员（0：否；1：是） |
| USER_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| USER_DESC | string | 备注说明 |
| USER_HEADIMGURL | string | 用户头像地址 |
| IDENTITY_CODE | string | 短信验证码 |
| ServerpartIds | string | 用户服务区权限(查询条件) |
| ServerpartList | List<string> | 用户服务区权限列表 |
| ServerpartShopList | List<integer> | 用户服务区门店权限列表（内码） |
| ShopNameList | List<string> | 用户服务区门店权限列表（名称） |
| SystemRoleList | List<integer> | 用户角色权限列表 |
| AnalysisPermission | boolean | 是否有驿达看板权限 |
| PushPermission | boolean | 是否有微信推送权限 |
| PushList | List<CommonTypeModel> | 微信推送权限列表 |
| SYSTEMROLE_IDS | string | 系统角色内码 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |

---
### POST /FrameWork/ModifyUserPassword
**名称**: 更新账户密码
**Action**: `ModifyUserPassword`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
更新账户密码
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| userPassword | UserPassword | Y |  |

UserPassword 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| DataType | integer | 数据类型1000【用户修改密码】2000【用户找回密码】 |
| User_Id_Encrypted | string | 账户内码（加密） |
| OriginPassword | string | 原账户密码 |
| UserMobilephone | string | 手机号码 |
| IdentityCode | string | 手机号码 |
| NewPassword | string | 新账户密码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |

---
### POST /FrameWork/ModifyUserCityAuthority
**名称**: 批量更新用户服务区权限
**Action**: `ModifyUserCityAuthority`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**:
> ⚠️ **加密要求**: 该接口入参 `postData` 需进行 AES 加密转换。
> 
> **请求模式**:
> 1. 将业务参数构建为 JSON 字符串。
> 2. 使用 AES 算法对字符串加密。
> 3. 将密文作为 `value` 字段的值发送，格式如：`{"name": "", "value": "BASE64_ENCRYPTED_STRING"}`。
 
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：是否新增服务区权限【AddAuthority】<br>待更新用户列表【UserIdList】<br>变更服务区列表【CityAuthorityList】 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[String]> | 返回数据集合 |

---
### GET /FrameWork/AuthorPush
**名称**: 授权微信推送权限
**Action**: `AuthorPush`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
授权微信推送权限
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| userId | integer | Y | 平台账号内码 |
| AuthorType | boolean | Y | 是否授权微信推送权限 |
| OperateUser | string | Y | 操作人员 |
| GroupType | integer | N | 业主推送权限的分类：            1000【本级】<br />1010【服务区】<br />1020【区域】 |
| ServerpartIds | string | N | 业主推送配置的服务区权限 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |

---
### GET /FrameWork/AuthorAnalysis
**名称**: 授权驿达看板权限
**Action**: `AuthorAnalysis`

**场景**: 
用于 FrameWork 模块系统框架级功能、通用组件及基础能力支持。
**说明**: 
授权驿达看板权限
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| userId | integer | Y | 平台账号内码 |
| AuthorType | boolean | Y | 是否授权驿达看板权限 |
| OperateUser | string | Y | 操作人员 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |

---
### GET /Log/GetChangeList
**名称**: 系统日志相关方法
**Action**: `LogController`

---
### GET /Log/GetChangeList
**名称**: 获取数据变更日志
**Action**: `GetChangeList`

**场景**: 
用于 Log 模块系统日志记录、查询及审计分析。
**说明**: 
获取数据变更日志
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| OperateLogType | string | Y | 操作类型 |
| ServerpartId | string | N | 服务区内码 |
| ServerpartShopId | string | N | 门店内码 |
| StartDate | string | N | 开始日期 |
| EndDate | string | N | 结束日期 |
| BusinessType | string | N | 经营模式 |
| ShopNames | string | N | 门店名称 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[OPERATELOGModel]]> | 返回数据集合 |

JsonMsg[JsonList[OPERATELOGModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[OPERATELOGModel] | 返回对象 |

JsonList[OPERATELOGModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<OPERATELOGModel> | 返回数据集 |

OPERATELOGModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| OPERATELOG_ID | integer | 内码 |
| OPERATELOG_TYPE | integer | 操作类型3000【无效数据】3001【回退数据】3002【变更日期】3003【变更金额】 |
| OPERATELOG_TYPES | string | 操作类型(查询条件) |
| USER_ID | integer | 帐户内码 |
| USER_NAME | string | 用户名称 |
| USER_PASSPORT | string | 登录账户 |
| MODULE_ID | integer | 模块内码 |
| MODULE_NAME | string | 模块名称 |
| MODULE_GUID | string | 唯一标识 |
| OPERATE_DATE | string | 操作时间 |
| OPERATE_DATE_Start | string | 操作时间(查询条件) |
| OPERATE_DATE_End | string | 操作时间(查询条件) |
| OPERATELOG_DESC | string | 备注说明 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_CODE | string | 服务区编码 |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| SHOPCODE | string | 门店编码 |
| BUSINESS_DATE | string | 业务时间 |
| BUSINESS_DATE_Start | string | 业务时间(查询条件) |
| BUSINESS_DATE_End | string | 业务时间(查询条件) |
| BUSINESSTYPE | integer | 商品业态 |
| DIFFERENT_AMOUNT | number | 金额差异 |
| MOBILEPAY_DIFFERENT | number | 移动支付差异 |
| OPERATE_STATE | integer | 处理状态 |
| USER_LOGINIP | string | 登录IP |
| USER_LOGINPLACE | string | 登录地址 |
| BROWSER_VERSION | string | 浏览器版本 |
| OPERATING_SYSTEM | string | 操作系统 |

---
### POST /PlatForm/GetDATACHANGEList
**名称**: 获取数据变更日志表列表
**Action**: `GetDATACHANGEList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取数据变更日志表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[DATACHANGEModel] | Y | 查询条件对象 |

SearchModel[DATACHANGEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | DATACHANGEModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

DATACHANGEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| DATACHANGE_ID | integer | 内码 |
| TABLE_ID | integer | 变更表主键值 |
| TABLE_NAME | string | 变更表名称 |
| OWNER_NAME | string | 变更用户名称 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人名称 |
| OPERATE_DATE | string | 操作时间 |
| OPERATE_DESC | string | 操作说明 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[DATACHANGEModel]]> | 返回数据集合 |

JsonMsg[JsonList[DATACHANGEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[DATACHANGEModel] | 返回对象 |

JsonList[DATACHANGEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<DATACHANGEModel> | 返回数据集 |

---
### GET /PlatForm/GetDATACHANGEDetail
**名称**: 获取数据变更日志表明细
**Action**: `GetDATACHANGEDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取数据变更日志表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| DATACHANGEId | integer | Y | 数据变更日志表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[DATACHANGEModel]> | 返回数据集合 |

JsonMsg[DATACHANGEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | DATACHANGEModel | 返回对象 |

DATACHANGEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| DATACHANGE_ID | integer | 内码 |
| TABLE_ID | integer | 变更表主键值 |
| TABLE_NAME | string | 变更表名称 |
| OWNER_NAME | string | 变更用户名称 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人名称 |
| OPERATE_DATE | string | 操作时间 |
| OPERATE_DESC | string | 操作说明 |

---
### POST /Log/GetOPERATELOGList
**名称**: 获取操作日志表列表
**Action**: `GetOPERATELOGList`

**场景**: 
用于 Log 模块系统日志记录、查询及审计分析。
**说明**: 
获取操作日志表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[OPERATELOGModel] | Y | 查询条件对象 |

SearchModel[OPERATELOGModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式0:模糊查询，1:精确查询 |
| SearchParameter | OPERATELOGModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

OPERATELOGModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| OPERATELOG_ID | integer | 内码 |
| OPERATELOG_TYPE | integer | 操作类型3000【无效数据】3001【回退数据】3002【变更日期】3003【变更金额】 |
| OPERATELOG_TYPES | string | 操作类型(查询条件) |
| USER_ID | integer | 帐户内码 |
| USER_NAME | string | 用户名称 |
| USER_PASSPORT | string | 登录账户 |
| MODULE_ID | integer | 模块内码 |
| MODULE_NAME | string | 模块名称 |
| MODULE_GUID | string | 唯一标识 |
| OPERATE_DATE | string | 操作时间 |
| OPERATE_DATE_Start | string | 操作时间(查询条件) |
| OPERATE_DATE_End | string | 操作时间(查询条件) |
| OPERATELOG_DESC | string | 备注说明 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_CODE | string | 服务区编码 |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| SHOPCODE | string | 门店编码 |
| BUSINESS_DATE | string | 业务时间 |
| BUSINESS_DATE_Start | string | 业务时间(查询条件) |
| BUSINESS_DATE_End | string | 业务时间(查询条件) |
| BUSINESSTYPE | integer | 商品业态 |
| DIFFERENT_AMOUNT | number | 金额差异 |
| MOBILEPAY_DIFFERENT | number | 移动支付差异 |
| OPERATE_STATE | integer | 处理状态 |
| USER_LOGINIP | string | 登录IP |
| USER_LOGINPLACE | string | 登录地址 |
| BROWSER_VERSION | string | 浏览器版本 |
| OPERATING_SYSTEM | string | 操作系统 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[OPERATELOGModel]]> | 返回数据集合 |

JsonList[OPERATELOGModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<OPERATELOGModel> | 返回数据集 |

---
### GET /Log/GetOPERATELOGDetail
**名称**: 获取操作日志表明细
**Action**: `GetOPERATELOGDetail`

**场景**: 
用于 Log 模块系统日志记录、查询及审计分析。
**说明**: 
获取操作日志表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| OPERATELOGId | integer | Y | 操作日志表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[OPERATELOGModel]> | 返回数据集合 |

OPERATELOGModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| OPERATELOG_ID | integer | 内码 |
| OPERATELOG_TYPE | integer | 操作类型3000【无效数据】3001【回退数据】3002【变更日期】3003【变更金额】 |
| OPERATELOG_TYPES | string | 操作类型(查询条件) |
| USER_ID | integer | 帐户内码 |
| USER_NAME | string | 用户名称 |
| USER_PASSPORT | string | 登录账户 |
| MODULE_ID | integer | 模块内码 |
| MODULE_NAME | string | 模块名称 |
| MODULE_GUID | string | 唯一标识 |
| OPERATE_DATE | string | 操作时间 |
| OPERATE_DATE_Start | string | 操作时间(查询条件) |
| OPERATE_DATE_End | string | 操作时间(查询条件) |
| OPERATELOG_DESC | string | 备注说明 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_CODE | string | 服务区编码 |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| SHOPCODE | string | 门店编码 |
| BUSINESS_DATE | string | 业务时间 |
| BUSINESS_DATE_Start | string | 业务时间(查询条件) |
| BUSINESS_DATE_End | string | 业务时间(查询条件) |
| BUSINESSTYPE | integer | 商品业态 |
| DIFFERENT_AMOUNT | number | 金额差异 |
| MOBILEPAY_DIFFERENT | number | 移动支付差异 |
| OPERATE_STATE | integer | 处理状态 |
| USER_LOGINIP | string | 登录IP |
| USER_LOGINPLACE | string | 登录地址 |
| BROWSER_VERSION | string | 浏览器版本 |
| OPERATING_SYSTEM | string | 操作系统 |

---
### POST /Platform/SetMessageState
**名称**: 批量设置消息状态
**Action**: `SetMessageState`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
批量设置消息状态
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| messageStateModel | MessageStateModel | Y |  |

MessageStateModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| messageIds | string | 消息内码集合 |
| recStaffId | integer | 发送人内码 |
| messageState | integer | 消息状态（0：无效；1：未读；2：已读） |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[String]> | 返回数据集合 |

JsonMsg[String] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | string | 返回对象 |

## 框架平台相关接口【PlatformController】

---
### POST /PlatForm/GetCATALOGUEList
**名称**: 获取附件目录表列表
**Action**: `GetCATALOGUEList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取附件目录表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[CATALOGUEModel] | Y | 查询条件对象 |

SearchModel[CATALOGUEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | CATALOGUEModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

CATALOGUEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| CATALOGUE_ID | integer | 目录内码 |
| CATALOGUE_PID | integer | 父级目录内码 |
| CATALOGUE_TYPE | integer | 目录类型 |
| CATALOGUE_NAME | string | 目录名称 |
| CATALOGUE_PATH | string | 目录相对路径 |
| CATALOGUE_URL | string | 目录地址 |
| CONTAIN_TABLEID | integer | 目录包含表内码（0：否，1：是） |
| PARAMS_TABLENAME | string | 入参表名（接口入参中传递的表名称） |
| DATABASE_TABLENAME | string | 数据库表名称 |
| STORAGE_TABLENAME | string | 存储数据表 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| CATALOGUE_DESC | string | 备注说明 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[CATALOGUEModel]]> | 返回数据集合 |

JsonMsg[JsonList[CATALOGUEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[CATALOGUEModel] | 返回对象 |

JsonList[CATALOGUEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<CATALOGUEModel> | 返回数据集 |

---
### GET /PlatForm/GetCATALOGUEDetail
**名称**: 获取附件目录表明细
**Action**: `GetCATALOGUEDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取附件目录表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| CATALOGUEId | integer | Y | 附件目录表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[CATALOGUEModel]> | 返回数据集合 |

JsonMsg[CATALOGUEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | CATALOGUEModel | 返回对象 |

CATALOGUEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| CATALOGUE_ID | integer | 目录内码 |
| CATALOGUE_PID | integer | 父级目录内码 |
| CATALOGUE_TYPE | integer | 目录类型 |
| CATALOGUE_NAME | string | 目录名称 |
| CATALOGUE_PATH | string | 目录相对路径 |
| CATALOGUE_URL | string | 目录地址 |
| CONTAIN_TABLEID | integer | 目录包含表内码（0：否，1：是） |
| PARAMS_TABLENAME | string | 入参表名（接口入参中传递的表名称） |
| DATABASE_TABLENAME | string | 数据库表名称 |
| STORAGE_TABLENAME | string | 存储数据表 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| CATALOGUE_DESC | string | 备注说明 |

---
### GET /PlatForm/GetUserByPhoneNum
**名称**: 根据手机号码获取系统用户表列表
**Action**: `GetUserByPhoneNum`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
根据手机号码获取系统用户表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PhoneNumber | string | Y | 手机号码 |
| UserPattern | integer | Y | 用户类型 |
| UserStatus | integer | N | 有效状态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[USERModel]]> | 返回数据集合 |

JsonMsg[JsonList[USERModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[USERModel] | 返回对象 |

JsonList[USERModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<USERModel> | 返回数据集 |

USERModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USER_ID | integer | 用户内码 |
| USER_IDS | string | 用户内码S |
| USER_ID_Encrypted | string | 用户内码（加密） |
| USERTYPE_ID | integer | 用户类型内码 |
| UserTypeIds | string | 用户类型内码集合 |
| USER_NAME | string | 用户名称 |
| USER_PASSPORT | string | 登录账户 |
| USER_PASSWORD | string | 账户密码 |
| USER_TIMEOUT | integer | 有效时间 |
| USER_INDEX | integer | 显示顺序 |
| USER_INDEFINIT | integer | 用户类型 |
| USER_EXPIRY | string | 授权时间 |
| USER_CITYAUTHORITY | string | 服务区权限 |
| USER_REPEATLOGON | integer | 允许重复登录 |
| USER_MOBILEPHONE | string | 手机号码 |
| USER_PROVINCE | integer | 用户省份 |
| PROVINCE_UNIT | string | 业主单位 |
| BUSINESSMAN_ID | integer | 商户内码 |
| BUSINESSMAN_IDS | string | 商户内码（查询条件） |
| BUSINESSMAN_NAME | string | 商户名称 |
| USER_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| SUPER_ADMIN | integer | 是否超级管理员（0：否；1：是） |
| USER_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| USER_DESC | string | 备注说明 |
| USER_HEADIMGURL | string | 用户头像地址 |
| IDENTITY_CODE | string | 短信验证码 |
| ServerpartIds | string | 用户服务区权限(查询条件) |
| ServerpartList | List<string> | 用户服务区权限列表 |
| ServerpartShopList | List<integer> | 用户服务区门店权限列表（内码） |
| ShopNameList | List<string> | 用户服务区门店权限列表（名称） |
| SystemRoleList | List<integer> | 用户角色权限列表 |
| AnalysisPermission | boolean | 是否有驿达看板权限 |
| PushPermission | boolean | 是否有微信推送权限 |
| PushList | List<CommonTypeModel> | 微信推送权限列表 |
| SYSTEMROLE_IDS | string | 系统角色内码 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /Platform/GetANTDROUTEDetail
**名称**: 获取AntDesign框架路由表明细
**Action**: `GetANTDROUTEDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取AntDesign框架路由表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ANTDROUTEId | integer | Y | AntDesign框架路由表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[ANTDROUTEModel]> | 返回数据集合 |

JsonMsg[ANTDROUTEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | ANTDROUTEModel | 返回对象 |

ANTDROUTEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ANTDROUTE_ID | integer | 路由内码 |
| ANTDROUTE_PID | integer | 父级内码 |
| ANTDROUTE_PATH | string | 相对路径 |
| ANTDROUTE_NAME | string | 路由名称 |
| ANTDROUTE_COMPONENT | string | 组件地址 |
| ANTDROUTE_AUTHORITY | string | 权限配置 |
| ANTDROUTE_ICON | string | 图标地址 |
| ANTDROUTE_INDEX | integer | 显示索引 |
| ANTDROUTE_VISIBLE | integer | 显示菜单(0：隐藏；1：显示) |
| ANTDROUTE_REDIRECT | string | 重定向地址 |
| ANTDROUTE_STATE | integer | 有效状态 |
| OPERATE_DATE | string | 操作时间 |
| ANTDROUTE_DESC | string | 备注说明 |

---
### POST /Platform/GetANTDROUTEList
**名称**: 获取AntDesign框架路由表列表
**Action**: `GetANTDROUTEList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取AntDesign框架路由表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[ANTDROUTEModel] | Y | 查询条件对象 |

SearchModel[ANTDROUTEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | ANTDROUTEModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

ANTDROUTEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ANTDROUTE_ID | integer | 路由内码 |
| ANTDROUTE_PID | integer | 父级内码 |
| ANTDROUTE_PATH | string | 相对路径 |
| ANTDROUTE_NAME | string | 路由名称 |
| ANTDROUTE_COMPONENT | string | 组件地址 |
| ANTDROUTE_AUTHORITY | string | 权限配置 |
| ANTDROUTE_ICON | string | 图标地址 |
| ANTDROUTE_INDEX | integer | 显示索引 |
| ANTDROUTE_VISIBLE | integer | 显示菜单(0：隐藏；1：显示) |
| ANTDROUTE_REDIRECT | string | 重定向地址 |
| ANTDROUTE_STATE | integer | 有效状态 |
| OPERATE_DATE | string | 操作时间 |
| ANTDROUTE_DESC | string | 备注说明 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[ANTDROUTEModel]]> | 返回数据集合 |

JsonMsg[JsonList[ANTDROUTEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[ANTDROUTEModel] | 返回对象 |

JsonList[ANTDROUTEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<ANTDROUTEModel> | 返回数据集 |

---
### GET /Platform/GetBEHAVIORRECORDDetail
**名称**: 获取用户行为记录表明细
**Action**: `GetBEHAVIORRECORDDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取用户行为记录表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BEHAVIORRECORDId | integer | Y | 用户行为记录表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[BEHAVIORRECORDModel]> | 返回数据集合 |

JsonMsg[BEHAVIORRECORDModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | BEHAVIORRECORDModel | 返回对象 |

BEHAVIORRECORDModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| BEHAVIORRECORD_ID | integer | 用户行为记录内码 |
| USER_ID | integer | 用户内码 |
| USER_NAME | string | 用户名称 |
| USER_PASSPORT | string | 登录账户 |
| USER_MOBILEPHONE | string | 手机号码 |
| BEHAVIORRECORD_TYPE | integer | 行为类型 |
| BEHAVIORRECORD_EXPLAIN | string | 行为描述 |
| BEHAVIORRECORD_TIME | string | 发生时间 |
| BEHAVIORRECORD_ROUT | string | 访问路径 |
| BEHAVIORRECORD_ROUTNAME | string | 页面名称 |
| BEHAVIORRECORD_PREROUT | string | 前序路径 |
| BEHAVIORRECORD_LEAVETIME | string | 结束时间 |
| BEHAVIORRECORD_DURATION | number | 停留时长 |
| OWNERUNIT_ID | integer | 业主单位/经营商户内码 |
| OWNERUNIT_NAME | string | 业主单位/经营商户名称 |
| BUSINESSMAN_ID | integer | 经营商户内码 |
| BUSINESSMAN_NAME | string | 经营商户名称 |
| SOURCE_PLATFORM | string | 审批平台(0：PC端；1：小程序；2：APP) |
| VISIT_CHANNELS | string | 访问渠道 |
| BEHAVIORRECORD_DESC | string | 备注说明 |
| USER_IDS | string | 用户内码(查询条件) |
| BEHAVIORRECORD_TYPES | string | 行为类型(查询条件) |
| BEHAVIORRECORD_TIME_Start | string | 发生时间(查询条件) |
| BEHAVIORRECORD_TIME_End | string | 发生时间(查询条件) |
| SOURCE_PLATFORMS | string | 审批平台(PC端；小程序；APP)(查询条件) |
| USER_LOGINIP | string | 登录IP |
| USER_LOGINPLACE | string | 登录地址 |
| BROWSER_VERSION | string | 浏览器版本 |
| OPERATING_SYSTEM | string | 操作系统 |
| REQUEST_INFO | string | 请求结果 |

---
### POST /Platform/GetBEHAVIORRECORDList
**名称**: 获取用户行为记录表列表
**Action**: `GetBEHAVIORRECORDList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取用户行为记录表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[BEHAVIORRECORDModel] | Y | 查询条件对象 |

SearchModel[BEHAVIORRECORDModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | BEHAVIORRECORDModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

BEHAVIORRECORDModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| BEHAVIORRECORD_ID | integer | 用户行为记录内码 |
| USER_ID | integer | 用户内码 |
| USER_NAME | string | 用户名称 |
| USER_PASSPORT | string | 登录账户 |
| USER_MOBILEPHONE | string | 手机号码 |
| BEHAVIORRECORD_TYPE | integer | 行为类型 |
| BEHAVIORRECORD_EXPLAIN | string | 行为描述 |
| BEHAVIORRECORD_TIME | string | 发生时间 |
| BEHAVIORRECORD_ROUT | string | 访问路径 |
| BEHAVIORRECORD_ROUTNAME | string | 页面名称 |
| BEHAVIORRECORD_PREROUT | string | 前序路径 |
| BEHAVIORRECORD_LEAVETIME | string | 结束时间 |
| BEHAVIORRECORD_DURATION | number | 停留时长 |
| OWNERUNIT_ID | integer | 业主单位/经营商户内码 |
| OWNERUNIT_NAME | string | 业主单位/经营商户名称 |
| BUSINESSMAN_ID | integer | 经营商户内码 |
| BUSINESSMAN_NAME | string | 经营商户名称 |
| SOURCE_PLATFORM | string | 审批平台(0：PC端；1：小程序；2：APP) |
| VISIT_CHANNELS | string | 访问渠道 |
| BEHAVIORRECORD_DESC | string | 备注说明 |
| USER_IDS | string | 用户内码(查询条件) |
| BEHAVIORRECORD_TYPES | string | 行为类型(查询条件) |
| BEHAVIORRECORD_TIME_Start | string | 发生时间(查询条件) |
| BEHAVIORRECORD_TIME_End | string | 发生时间(查询条件) |
| SOURCE_PLATFORMS | string | 审批平台(PC端；小程序；APP)(查询条件) |
| USER_LOGINIP | string | 登录IP |
| USER_LOGINPLACE | string | 登录地址 |
| BROWSER_VERSION | string | 浏览器版本 |
| OPERATING_SYSTEM | string | 操作系统 |
| REQUEST_INFO | string | 请求结果 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[BEHAVIORRECORDModel]]> | 返回数据集合 |

JsonMsg[JsonList[BEHAVIORRECORDModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[BEHAVIORRECORDModel] | 返回对象 |

JsonList[BEHAVIORRECORDModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<BEHAVIORRECORDModel> | 返回数据集 |

---
### GET /Platform/GetMESSAGEDetail
**名称**: 获取消息通知表明细
**Action**: `GetMESSAGEDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取消息通知表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| MESSAGEId | integer | Y | 消息通知表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[MESSAGEModel]> | 返回数据集合 |

JsonMsg[MESSAGEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | MESSAGEModel | 返回对象 |

MESSAGEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| MESSAGE_ID | integer | 消息通知内码 |
| MESSAGE_TYPE | integer | 消息类型（1000：通知；2000：待办事项） |
| MESSAGE_TITLE | string | 消息标题 |
| MESSAGE_CONTENT | string | 消息内容 |
| TABLE_ID | integer | 关联业务表内码 |
| TABLE_NAME | string | 关联业务表名称 |
| SENDSTAFF_ID | integer | 发送人内码 |
| SENDSTAFF_NAME | string | 发送人名称 |
| SEND_DATE | string | 发送时间 |
| RECSTAFF_ID | integer | 接收人内码 |
| RECSTAFF_NAME | string | 接收人名称 |
| MESSAGE_STATE | integer | 消息状态（0：无效；1：未读；2：已读） |
| OPERATE_DATE | string | 操作时间 |
| ACCEPT_CODE | string | 业务编码 |
| BUSINESSPROCESS_STATE | integer | 审批状态（1000：已提交；2000：审核中；9000：已通过；3000：不通过） |

---
### POST /Platform/GetMESSAGEList
**名称**: 获取消息通知表列表
**Action**: `GetMESSAGEList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取消息通知表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[MESSAGEModel] | Y | 查询条件对象 |

SearchModel[MESSAGEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | MESSAGEModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

MESSAGEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| MESSAGE_ID | integer | 消息通知内码 |
| MESSAGE_TYPE | integer | 消息类型（1000：通知；2000：待办事项） |
| MESSAGE_TITLE | string | 消息标题 |
| MESSAGE_CONTENT | string | 消息内容 |
| TABLE_ID | integer | 关联业务表内码 |
| TABLE_NAME | string | 关联业务表名称 |
| SENDSTAFF_ID | integer | 发送人内码 |
| SENDSTAFF_NAME | string | 发送人名称 |
| SEND_DATE | string | 发送时间 |
| RECSTAFF_ID | integer | 接收人内码 |
| RECSTAFF_NAME | string | 接收人名称 |
| MESSAGE_STATE | integer | 消息状态（0：无效；1：未读；2：已读） |
| OPERATE_DATE | string | 操作时间 |
| ACCEPT_CODE | string | 业务编码 |
| BUSINESSPROCESS_STATE | integer | 审批状态（1000：已提交；2000：审核中；9000：已通过；3000：不通过） |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[MESSAGEModel]]> | 返回数据集合 |

JsonMsg[JsonList[MESSAGEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[MESSAGEModel] | 返回对象 |

JsonList[MESSAGEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<MESSAGEModel> | 返回数据集 |

---
### GET /Platform/GetPERMISSIONAPPLYDETAILDetail
**名称**: 获取权限申请明细表明细
**Action**: `GetPERMISSIONAPPLYDETAILDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取权限申请明细表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PERMISSIONAPPLYDETAILId | integer | Y | 权限申请明细表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[PERMISSIONAPPLYDETAILModel]> | 返回数据集合 |

JsonMsg[PERMISSIONAPPLYDETAILModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | PERMISSIONAPPLYDETAILModel | 返回对象 |

PERMISSIONAPPLYDETAILModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PERMISSIONAPPLYDETAIL_ID | integer | 权限申请明细内码 |
| PERMISSIONAPPLY_ID | integer | 权限申请内码 |
| PERMISSIONAPPLYDETAIL_TYPE | integer | 操作类型（1000：账号新增；2000：权限新增；权限移除） |
| USER_PASSPORT | string | 用户账号 |
| SYSTEMROLE_ID | integer | 系统角色内码 |
| SYSTEMROLE_NAME | string | 系统角色名称 |
| PRODEFROLE_ID | integer | 流程环节内码 |
| PRODEFROLE_NAME | string | 流程环节名称 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_NAME | string | 服务区名称 |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| SERVERPARTSHOP_NAME | string | 门店名称 |
| OPERATE_DATE | string | 操作时间 |

---
### POST /Platform/GetPERMISSIONAPPLYDETAILList
**名称**: 获取权限申请明细表列表
**Action**: `GetPERMISSIONAPPLYDETAILList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取权限申请明细表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[PERMISSIONAPPLYDETAILModel] | Y | 查询条件对象 |

SearchModel[PERMISSIONAPPLYDETAILModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | PERMISSIONAPPLYDETAILModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

PERMISSIONAPPLYDETAILModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PERMISSIONAPPLYDETAIL_ID | integer | 权限申请明细内码 |
| PERMISSIONAPPLY_ID | integer | 权限申请内码 |
| PERMISSIONAPPLYDETAIL_TYPE | integer | 操作类型（1000：账号新增；2000：权限新增；权限移除） |
| USER_PASSPORT | string | 用户账号 |
| SYSTEMROLE_ID | integer | 系统角色内码 |
| SYSTEMROLE_NAME | string | 系统角色名称 |
| PRODEFROLE_ID | integer | 流程环节内码 |
| PRODEFROLE_NAME | string | 流程环节名称 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_NAME | string | 服务区名称 |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| SERVERPARTSHOP_NAME | string | 门店名称 |
| OPERATE_DATE | string | 操作时间 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[PERMISSIONAPPLYDETAILModel]]> | 返回数据集合 |

JsonMsg[JsonList[PERMISSIONAPPLYDETAILModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[PERMISSIONAPPLYDETAILModel] | 返回对象 |

JsonList[PERMISSIONAPPLYDETAILModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<PERMISSIONAPPLYDETAILModel> | 返回数据集 |

---
### GET /Platform/GetPERMISSIONAPPLYDetail
**名称**: 获取权限申请表明细
**Action**: `GetPERMISSIONAPPLYDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取权限申请表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PERMISSIONAPPLYId | integer | Y | 权限申请表内码 |
| ModuleGuid | string | N | 用户模块权限 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[PERMISSIONAPPLYModel]> | 返回数据集合 |

JsonMsg[PERMISSIONAPPLYModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | PERMISSIONAPPLYModel | 返回对象 |

PERMISSIONAPPLYModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PERMISSIONAPPLY_ID | integer | 权限申请内码 |
| PERMISSIONAPPLY_TYPE | integer | *权限申请类型：1000：新增账户；2000：模块权限变更；3000：流程权限变更；4000：门店权限变更；5000：服务区权限变更；7000：门店状态变更；8000：商家信息完善 |
| USER_MOBILEPHONE | string | *手机号码 |
| USER_NAME | string | *申请人员 |
| PERMISSIONAPPLY_DATE | string | 申请时间 |
| PERMISSIONAPPLY_REASON | string | *申请缘由 |
| LEGAL_PERSON | string | 商家法人 |
| LEGAL_MOBILEPHONE | string | 法人手机号码 |
| USER_IDCARD | string | 身份证号码 |
| USER_PASSWORD | string | 账号密码 |
| BUSINESSMAN_ID | integer | 经营商户内码 |
| BUSINESSMAN_NAME | string | 经营商户名称 |
| TAXPAYER_IDENTIFYCODE | string | 统一信用代码 |
| BANK_NAME | string | 开户银行 |
| BANK_ACCOUNT | string | 结算卡号 |
| OWNERUNIT_ID | integer | 业主单位内码 |
| OWNERUNIT_NAME | string | 业主单位名称 |
| SERVERPART_ID | integer | 申请服务区内码【PERMISSIONAPPLY_TYPE：2000、4000、5000、7000、8000时必填】 |
| SERVERPART_NAME | string | 申请服务区名称 |
| APPLYSHOP_NAME | string | 申请门店 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| APPOVED_ID | integer | 审批人内码 |
| APPOVED_NAME | string | 审批人员 |
| APPOVED_INFO | string | 意见内容 |
| APPOVED_DATE | string | 审批时间 |
| TIME_EFFICIENCY | number | 处理时效 |
| SOURCE_PLATFORM | integer | 审批平台(0：PC端；1：小程序；2：APP) |
| PERMISSIONAPPLY_STATE | integer | 审批状态 |
| PERMISSIONAPPLY_DESC | string | 备注说明 |
| IDENTITY_CODE | string | 短信验证码 |
| SERVERPART_IDS | string | 服务区内码集合（商家资料审批） |
| PendState | integer | 是否为待办事项0：待办；1：非待办 |
| approveList | List<APPLYAPPROVEModel> | 审批意见列表 |

APPLYAPPROVEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| APPLYAPPROVE_ID | integer | 审批意见内码 |
| TABLE_ID | integer | 数据表主键值 |
| TABLE_IDS | string | 数据表主键值(查询条件) |
| TABLE_NAME | string | 数据表名称 |
| APPLYAPPROVE_TYPE | integer | 意见类型 |
| APPLYAPPROVE_NAME | string | 环节名称 |
| APPLYAPPROVE_INFO | string | 审批意见 |
| APPLYAPPROVE_DATE | string | 审批时间 |
| APPLYAPPROVE_DATE_Start | string | 审批时间(查询条件) |
| APPLYAPPROVE_DATE_End | string | 审批时间(查询条件) |
| APPROVED_NAME | string | 组件名称 |
| TIME_EFFICIENCY | number | 审批时效（存储小时） |
| STAFF_ID | integer | 审批人内码 |
| STAFF_NAME | string | 审批人员 |
| MOBILE_APPROVE | integer | 移动端审批（0：否；1：是） |
| REJECT_ID | integer | 驳回人内码 |
| REJECT_TYPE | integer | 驳回环节 |
| REJECT_STAFF | string | 驳回人员 |
| REJECT_NAME | string | 驳回环节名称 |

---
### POST /Platform/GetPERMISSIONAPPLYList
**名称**: 获取权限申请表列表
**Action**: `GetPERMISSIONAPPLYList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取权限申请表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[PERMISSIONAPPLYModel] | Y | 查询条件对象 |

SearchModel[PERMISSIONAPPLYModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | PERMISSIONAPPLYModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

PERMISSIONAPPLYModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PERMISSIONAPPLY_ID | integer | 权限申请内码 |
| PERMISSIONAPPLY_TYPE | integer | *权限申请类型：1000：新增账户；2000：模块权限变更；3000：流程权限变更；4000：门店权限变更；5000：服务区权限变更；7000：门店状态变更；8000：商家信息完善 |
| USER_MOBILEPHONE | string | *手机号码 |
| USER_NAME | string | *申请人员 |
| PERMISSIONAPPLY_DATE | string | 申请时间 |
| PERMISSIONAPPLY_REASON | string | *申请缘由 |
| LEGAL_PERSON | string | 商家法人 |
| LEGAL_MOBILEPHONE | string | 法人手机号码 |
| USER_IDCARD | string | 身份证号码 |
| USER_PASSWORD | string | 账号密码 |
| BUSINESSMAN_ID | integer | 经营商户内码 |
| BUSINESSMAN_NAME | string | 经营商户名称 |
| TAXPAYER_IDENTIFYCODE | string | 统一信用代码 |
| BANK_NAME | string | 开户银行 |
| BANK_ACCOUNT | string | 结算卡号 |
| OWNERUNIT_ID | integer | 业主单位内码 |
| OWNERUNIT_NAME | string | 业主单位名称 |
| SERVERPART_ID | integer | 申请服务区内码【PERMISSIONAPPLY_TYPE：2000、4000、5000、7000、8000时必填】 |
| SERVERPART_NAME | string | 申请服务区名称 |
| APPLYSHOP_NAME | string | 申请门店 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| APPOVED_ID | integer | 审批人内码 |
| APPOVED_NAME | string | 审批人员 |
| APPOVED_INFO | string | 意见内容 |
| APPOVED_DATE | string | 审批时间 |
| TIME_EFFICIENCY | number | 处理时效 |
| SOURCE_PLATFORM | integer | 审批平台(0：PC端；1：小程序；2：APP) |
| PERMISSIONAPPLY_STATE | integer | 审批状态 |
| PERMISSIONAPPLY_DESC | string | 备注说明 |
| IDENTITY_CODE | string | 短信验证码 |
| SERVERPART_IDS | string | 服务区内码集合（商家资料审批） |
| PendState | integer | 是否为待办事项0：待办；1：非待办 |
| approveList | List<APPLYAPPROVEModel> | 审批意见列表 |

APPLYAPPROVEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| APPLYAPPROVE_ID | integer | 审批意见内码 |
| TABLE_ID | integer | 数据表主键值 |
| TABLE_IDS | string | 数据表主键值(查询条件) |
| TABLE_NAME | string | 数据表名称 |
| APPLYAPPROVE_TYPE | integer | 意见类型 |
| APPLYAPPROVE_NAME | string | 环节名称 |
| APPLYAPPROVE_INFO | string | 审批意见 |
| APPLYAPPROVE_DATE | string | 审批时间 |
| APPLYAPPROVE_DATE_Start | string | 审批时间(查询条件) |
| APPLYAPPROVE_DATE_End | string | 审批时间(查询条件) |
| APPROVED_NAME | string | 组件名称 |
| TIME_EFFICIENCY | number | 审批时效（存储小时） |
| STAFF_ID | integer | 审批人内码 |
| STAFF_NAME | string | 审批人员 |
| MOBILE_APPROVE | integer | 移动端审批（0：否；1：是） |
| REJECT_ID | integer | 驳回人内码 |
| REJECT_TYPE | integer | 驳回环节 |
| REJECT_STAFF | string | 驳回人员 |
| REJECT_NAME | string | 驳回环节名称 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[PERMISSIONAPPLYModel]]> | 返回数据集合 |

JsonMsg[JsonList[PERMISSIONAPPLYModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[PERMISSIONAPPLYModel] | 返回对象 |

JsonList[PERMISSIONAPPLYModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<PERMISSIONAPPLYModel> | 返回数据集 |

---
### GET /Platform/GetSYSTEMMENUDetail
**名称**: 获取系统菜单表明细
**Action**: `GetSYSTEMMENUDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取系统菜单表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SYSTEMMENUId | integer | Y | 系统菜单表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[SYSTEMMENUModel]> | 返回数据集合 |

JsonMsg[SYSTEMMENUModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | SYSTEMMENUModel | 返回对象 |

SYSTEMMENUModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMENU_PID | integer | 系统菜单父级内码 |
| SYSTEMMENU_NAME | string | 系统菜单名称 |
| SYSTEMMENU_INDEX | integer | 系统菜单索引 |
| SYSTEMMENU_LEVEL | integer | 系统菜单级别 |
| SYSTEMMENU_ICO | string | 系统菜单图标 |
| SYSTEMMENU_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMENU_DESC | string | 备注说明 |
| SystemModuleList | List<SYSTEMMODULEModel> | 系统模块列表 |

SYSTEMMODULEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMODULE_ID | integer | 系统模块内码 |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMODULE_TYPE | integer | 系统模块类型 |
| SYSTEMMODULE_NAME | string | 系统模块名称 |
| SYSTEMMODULE_INDEX | integer | 系统模块索引 |
| SYSTEMMODULE_GUID | string | 模块唯一标识 |
| SYSTEMMODULE_URL | string | 系统模块地址 |
| SYSTEMMODULE_ICO | string | 系统模块图标 |
| SYSTEMMODULE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMODULE_DESC | string | 备注说明 |

---
### POST /Platform/GetSYSTEMMENUList
**名称**: 获取系统菜单表列表
**Action**: `GetSYSTEMMENUList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取系统菜单表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[SYSTEMMENUModel] | Y | 查询条件对象 |

SearchModel[SYSTEMMENUModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | SYSTEMMENUModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

SYSTEMMENUModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMENU_PID | integer | 系统菜单父级内码 |
| SYSTEMMENU_NAME | string | 系统菜单名称 |
| SYSTEMMENU_INDEX | integer | 系统菜单索引 |
| SYSTEMMENU_LEVEL | integer | 系统菜单级别 |
| SYSTEMMENU_ICO | string | 系统菜单图标 |
| SYSTEMMENU_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMENU_DESC | string | 备注说明 |
| SystemModuleList | List<SYSTEMMODULEModel> | 系统模块列表 |

SYSTEMMODULEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMODULE_ID | integer | 系统模块内码 |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMODULE_TYPE | integer | 系统模块类型 |
| SYSTEMMODULE_NAME | string | 系统模块名称 |
| SYSTEMMODULE_INDEX | integer | 系统模块索引 |
| SYSTEMMODULE_GUID | string | 模块唯一标识 |
| SYSTEMMODULE_URL | string | 系统模块地址 |
| SYSTEMMODULE_ICO | string | 系统模块图标 |
| SYSTEMMODULE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMODULE_DESC | string | 备注说明 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[SYSTEMMENUModel]]> | 返回数据集合 |

JsonMsg[JsonList[SYSTEMMENUModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[SYSTEMMENUModel] | 返回对象 |

JsonList[SYSTEMMENUModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<SYSTEMMENUModel> | 返回数据集 |

---
### GET /Platform/GetSYSTEMMODULEDetail
**名称**: 获取系统模块表明细
**Action**: `GetSYSTEMMODULEDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取系统模块表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SYSTEMMODULEId | integer | Y | 系统模块表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[SYSTEMMODULEModel]> | 返回数据集合 |

JsonMsg[SYSTEMMODULEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | SYSTEMMODULEModel | 返回对象 |

SYSTEMMODULEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMODULE_ID | integer | 系统模块内码 |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMODULE_TYPE | integer | 系统模块类型 |
| SYSTEMMODULE_NAME | string | 系统模块名称 |
| SYSTEMMODULE_INDEX | integer | 系统模块索引 |
| SYSTEMMODULE_GUID | string | 模块唯一标识 |
| SYSTEMMODULE_URL | string | 系统模块地址 |
| SYSTEMMODULE_ICO | string | 系统模块图标 |
| SYSTEMMODULE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMODULE_DESC | string | 备注说明 |

---
### POST /Platform/GetSYSTEMMODULEList
**名称**: 获取系统模块表列表
**Action**: `GetSYSTEMMODULEList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取系统模块表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[SYSTEMMODULEModel] | Y | 查询条件对象 |

SearchModel[SYSTEMMODULEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | SYSTEMMODULEModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

SYSTEMMODULEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMMODULE_ID | integer | 系统模块内码 |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMODULE_TYPE | integer | 系统模块类型 |
| SYSTEMMODULE_NAME | string | 系统模块名称 |
| SYSTEMMODULE_INDEX | integer | 系统模块索引 |
| SYSTEMMODULE_GUID | string | 模块唯一标识 |
| SYSTEMMODULE_URL | string | 系统模块地址 |
| SYSTEMMODULE_ICO | string | 系统模块图标 |
| SYSTEMMODULE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMMODULE_DESC | string | 备注说明 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[SYSTEMMODULEModel]]> | 返回数据集合 |

JsonMsg[JsonList[SYSTEMMODULEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[SYSTEMMODULEModel] | 返回对象 |

JsonList[SYSTEMMODULEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<SYSTEMMODULEModel> | 返回数据集 |

---
### GET /Platform/GetSYSTEMROLEDetail
**名称**: 获取系统角色表明细
**Action**: `GetSYSTEMROLEDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取系统角色表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SYSTEMROLEId | integer | Y | 系统角色表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[SYSTEMROLEModel]> | 返回数据集合 |

JsonMsg[SYSTEMROLEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | SYSTEMROLEModel | 返回对象 |

SYSTEMROLEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMROLE_ID | integer | 系统角色内码 |
| SYSTEMROLE_PID | integer | 系统角色父级内码 |
| SYSTEMROLE_TYPE | integer | 系统角色类型 |
| SYSTEMROLE_PROVINCE | integer | 角色所属省份 |
| SYSTEMROLE_BUSINESS | integer | 角色所属商户 |
| SYSTEMROLE_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| SYSTEMROLE_NAME | string | 系统角色名称 |
| SYSTEMROLE_LEVEL | integer | 系统角色级别 |
| SYSTEMROLE_INDEX | integer | 系统角色索引 |
| SYSTEMROLE_ICO | string | 系统角色图标 |
| SYSTEMROLE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMROLE_DESC | string | 备注说明 |
| SystemModuleList | List<integer> | 角色模块权限数组 |
| UserIds | List<integer> | 用户IDs |
| UserTypeIds | List<integer> | 用户分类IDs |
| UserNames | List<string> | 用户名称s |

---
### POST /Platform/GetSYSTEMROLEList
**名称**: 获取系统角色表列表
**Action**: `GetSYSTEMROLEList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取系统角色表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[SYSTEMROLEModel] | Y | 查询条件对象 |

SearchModel[SYSTEMROLEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | SYSTEMROLEModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

SYSTEMROLEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMROLE_ID | integer | 系统角色内码 |
| SYSTEMROLE_PID | integer | 系统角色父级内码 |
| SYSTEMROLE_TYPE | integer | 系统角色类型 |
| SYSTEMROLE_PROVINCE | integer | 角色所属省份 |
| SYSTEMROLE_BUSINESS | integer | 角色所属商户 |
| SYSTEMROLE_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| SYSTEMROLE_NAME | string | 系统角色名称 |
| SYSTEMROLE_LEVEL | integer | 系统角色级别 |
| SYSTEMROLE_INDEX | integer | 系统角色索引 |
| SYSTEMROLE_ICO | string | 系统角色图标 |
| SYSTEMROLE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMROLE_DESC | string | 备注说明 |
| SystemModuleList | List<integer> | 角色模块权限数组 |
| UserIds | List<integer> | 用户IDs |
| UserTypeIds | List<integer> | 用户分类IDs |
| UserNames | List<string> | 用户名称s |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[SYSTEMROLEModel]]> | 返回数据集合 |

JsonMsg[JsonList[SYSTEMROLEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[SYSTEMROLEModel] | 返回对象 |

JsonList[SYSTEMROLEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<SYSTEMROLEModel> | 返回数据集 |

---
### GET /Platform/GetSYSTEMROLEMODULEDetail
**名称**: 获取角色模块关联表明细
**Action**: `GetSYSTEMROLEMODULEDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取角色模块关联表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SYSTEMROLEMODULEId | integer | Y | 角色模块关联表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[SYSTEMROLEMODULEModel]> | 返回数据集合 |

JsonMsg[SYSTEMROLEMODULEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | SYSTEMROLEMODULEModel | 返回对象 |

SYSTEMROLEMODULEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMROLEMODULE_ID | integer | 内码 |
| SYSTEMROLE_ID | integer | 系统角色内码 |
| SYSTEMMODULE_ID | integer | 系统模块内码 |
| OPERATE_DATE | string | 操作时间 |

---
### POST /Platform/GetSYSTEMROLEMODULEList
**名称**: 获取角色模块关联表列表
**Action**: `GetSYSTEMROLEMODULEList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取角色模块关联表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[SYSTEMROLEMODULEModel] | Y | 查询条件对象 |

SearchModel[SYSTEMROLEMODULEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | SYSTEMROLEMODULEModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

SYSTEMROLEMODULEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMROLEMODULE_ID | integer | 内码 |
| SYSTEMROLE_ID | integer | 系统角色内码 |
| SYSTEMMODULE_ID | integer | 系统模块内码 |
| OPERATE_DATE | string | 操作时间 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[SYSTEMROLEMODULEModel]]> | 返回数据集合 |

JsonMsg[JsonList[SYSTEMROLEMODULEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[SYSTEMROLEMODULEModel] | 返回对象 |

JsonList[SYSTEMROLEMODULEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<SYSTEMROLEMODULEModel> | 返回数据集 |

---
### GET /Platform/GetSYSTEMROUTEDetail
**名称**: 获取系统路由表明细
**Action**: `GetSYSTEMROUTEDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取系统路由表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SYSTEMROUTEId | integer | Y | 系统路由表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[SYSTEMROUTEModel]> | 返回数据集合 |

JsonMsg[SYSTEMROUTEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | SYSTEMROUTEModel | 返回对象 |

SYSTEMROUTEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMROUTE_ID | integer | 系统路由内码 |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMODULE_ID | integer | 系统模块内码 |
| SYSTEMROUTE_NAME | string | 系统路由名称 |
| SYSTEMROUTE_INDEX | integer | 系统路由索引 |
| SYSTEMROUTE_LEVEL | integer | 系统路由级别 |
| SYSTEMROUTE_URL | string | 系统路由地址 |
| SYSTEMROUTE_ICO | string | 系统路由图标 |
| SYSTEMROUTE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMROUTE_DESC | string | 备注说明 |

---
### POST /Platform/GetSYSTEMROUTEList
**名称**: 获取系统路由表列表
**Action**: `GetSYSTEMROUTEList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取系统路由表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[SYSTEMROUTEModel] | Y | 查询条件对象 |

SearchModel[SYSTEMROUTEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | SYSTEMROUTEModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

SYSTEMROUTEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SYSTEMROUTE_ID | integer | 系统路由内码 |
| SYSTEMMENU_ID | integer | 系统菜单内码 |
| SYSTEMMODULE_ID | integer | 系统模块内码 |
| SYSTEMROUTE_NAME | string | 系统路由名称 |
| SYSTEMROUTE_INDEX | integer | 系统路由索引 |
| SYSTEMROUTE_LEVEL | integer | 系统路由级别 |
| SYSTEMROUTE_URL | string | 系统路由地址 |
| SYSTEMROUTE_ICO | string | 系统路由图标 |
| SYSTEMROUTE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMROUTE_DESC | string | 备注说明 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[SYSTEMROUTEModel]]> | 返回数据集合 |

JsonMsg[JsonList[SYSTEMROUTEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[SYSTEMROUTEModel] | 返回对象 |

JsonList[SYSTEMROUTEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<SYSTEMROUTEModel> | 返回数据集 |

---
### GET /Platform/GetUSERDetail
**名称**: 获取系统用户表明细
**Action**: `GetUSERDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取系统用户表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| USERId | integer | Y | 系统用户表内码 |
| ShowPush | boolean | N | 是否显示推送相关权限 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[USERModel]> | 返回数据集合 |

JsonMsg[USERModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | USERModel | 返回对象 |

USERModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USER_ID | integer | 用户内码 |
| USER_IDS | string | 用户内码S |
| USER_ID_Encrypted | string | 用户内码（加密） |
| USERTYPE_ID | integer | 用户类型内码 |
| UserTypeIds | string | 用户类型内码集合 |
| USER_NAME | string | 用户名称 |
| USER_PASSPORT | string | 登录账户 |
| USER_PASSWORD | string | 账户密码 |
| USER_TIMEOUT | integer | 有效时间 |
| USER_INDEX | integer | 显示顺序 |
| USER_INDEFINIT | integer | 用户类型 |
| USER_EXPIRY | string | 授权时间 |
| USER_CITYAUTHORITY | string | 服务区权限 |
| USER_REPEATLOGON | integer | 允许重复登录 |
| USER_MOBILEPHONE | string | 手机号码 |
| USER_PROVINCE | integer | 用户省份 |
| PROVINCE_UNIT | string | 业主单位 |
| BUSINESSMAN_ID | integer | 商户内码 |
| BUSINESSMAN_IDS | string | 商户内码（查询条件） |
| BUSINESSMAN_NAME | string | 商户名称 |
| USER_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| SUPER_ADMIN | integer | 是否超级管理员（0：否；1：是） |
| USER_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| USER_DESC | string | 备注说明 |
| USER_HEADIMGURL | string | 用户头像地址 |
| IDENTITY_CODE | string | 短信验证码 |
| ServerpartIds | string | 用户服务区权限(查询条件) |
| ServerpartList | List<string> | 用户服务区权限列表 |
| ServerpartShopList | List<integer> | 用户服务区门店权限列表（内码） |
| ShopNameList | List<string> | 用户服务区门店权限列表（名称） |
| SystemRoleList | List<integer> | 用户角色权限列表 |
| AnalysisPermission | boolean | 是否有驿达看板权限 |
| PushPermission | boolean | 是否有微信推送权限 |
| PushList | List<CommonTypeModel> | 微信推送权限列表 |
| SYSTEMROLE_IDS | string | 系统角色内码 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### POST /Platform/GetUSERList
**名称**: 获取系统用户表列表
**Action**: `GetUSERList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取系统用户表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[USERModel] | Y | 查询条件对象 |

SearchModel[USERModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | USERModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

USERModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USER_ID | integer | 用户内码 |
| USER_IDS | string | 用户内码S |
| USER_ID_Encrypted | string | 用户内码（加密） |
| USERTYPE_ID | integer | 用户类型内码 |
| UserTypeIds | string | 用户类型内码集合 |
| USER_NAME | string | 用户名称 |
| USER_PASSPORT | string | 登录账户 |
| USER_PASSWORD | string | 账户密码 |
| USER_TIMEOUT | integer | 有效时间 |
| USER_INDEX | integer | 显示顺序 |
| USER_INDEFINIT | integer | 用户类型 |
| USER_EXPIRY | string | 授权时间 |
| USER_CITYAUTHORITY | string | 服务区权限 |
| USER_REPEATLOGON | integer | 允许重复登录 |
| USER_MOBILEPHONE | string | 手机号码 |
| USER_PROVINCE | integer | 用户省份 |
| PROVINCE_UNIT | string | 业主单位 |
| BUSINESSMAN_ID | integer | 商户内码 |
| BUSINESSMAN_IDS | string | 商户内码（查询条件） |
| BUSINESSMAN_NAME | string | 商户名称 |
| USER_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| SUPER_ADMIN | integer | 是否超级管理员（0：否；1：是） |
| USER_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| USER_DESC | string | 备注说明 |
| USER_HEADIMGURL | string | 用户头像地址 |
| IDENTITY_CODE | string | 短信验证码 |
| ServerpartIds | string | 用户服务区权限(查询条件) |
| ServerpartList | List<string> | 用户服务区权限列表 |
| ServerpartShopList | List<integer> | 用户服务区门店权限列表（内码） |
| ShopNameList | List<string> | 用户服务区门店权限列表（名称） |
| SystemRoleList | List<integer> | 用户角色权限列表 |
| AnalysisPermission | boolean | 是否有驿达看板权限 |
| PushPermission | boolean | 是否有微信推送权限 |
| PushList | List<CommonTypeModel> | 微信推送权限列表 |
| SYSTEMROLE_IDS | string | 系统角色内码 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[USERModel]]> | 返回数据集合 |

JsonMsg[JsonList[USERModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[USERModel] | 返回对象 |

JsonList[USERModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<USERModel> | 返回数据集 |

---
### GET /Platform/GetUSERSYSTEMROLEDetail
**名称**: 获取用户角色权限表明细
**Action**: `GetUSERSYSTEMROLEDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取用户角色权限表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| USERSYSTEMROLEId | integer | Y | 用户角色权限表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[USERSYSTEMROLEModel]> | 返回数据集合 |

JsonMsg[USERSYSTEMROLEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | USERSYSTEMROLEModel | 返回对象 |

USERSYSTEMROLEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USERSYSTEMROLE_ID | integer | 内码 |
| USER_ID | integer | 用户内码 |
| USER_IDS | string | 用户内码(查询条件) |
| SYSTEMROLE_ID | integer | 系统角色内码 |
| SYSTEMROLE_IDS | string | 系统角色内码(查询条件) |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMROLE_TYPE | integer | 系统角色类型（1000：模块角色,2000：账号角色） |
| SYSTEMROLE_TYPES | string | 系统角色类型（1000：模块角色,2000：账号角色）(查询条件) |

---
### POST /Platform/GetUSERSYSTEMROLEList
**名称**: 获取用户角色权限表列表
**Action**: `GetUSERSYSTEMROLEList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取用户角色权限表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[USERSYSTEMROLEModel] | Y | 查询条件对象 |

SearchModel[USERSYSTEMROLEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | USERSYSTEMROLEModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

USERSYSTEMROLEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USERSYSTEMROLE_ID | integer | 内码 |
| USER_ID | integer | 用户内码 |
| USER_IDS | string | 用户内码(查询条件) |
| SYSTEMROLE_ID | integer | 系统角色内码 |
| SYSTEMROLE_IDS | string | 系统角色内码(查询条件) |
| OPERATE_DATE | string | 操作时间 |
| SYSTEMROLE_TYPE | integer | 系统角色类型（1000：模块角色,2000：账号角色） |
| SYSTEMROLE_TYPES | string | 系统角色类型（1000：模块角色,2000：账号角色）(查询条件) |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[USERSYSTEMROLEModel]]> | 返回数据集合 |

JsonMsg[JsonList[USERSYSTEMROLEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[USERSYSTEMROLEModel] | 返回对象 |

JsonList[USERSYSTEMROLEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<USERSYSTEMROLEModel> | 返回数据集 |

---
### GET /Platform/GetUSERTYPEDetail
**名称**: 获取用户类型表明细
**Action**: `GetUSERTYPEDetail`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取用户类型表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| USERTYPEId | integer | Y | 用户类型表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[USERTYPEModel]> | 返回数据集合 |

JsonMsg[USERTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | USERTYPEModel | 返回对象 |

USERTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USERTYPE_ID | integer | 用户类型内码 |
| USERTYPE_NAME | string | 用户类型名称 |
| USERTYPE_PID | integer | 用户类型父级内码 |
| USERTYPE_INDEX | integer | 用户类型索引 |
| USERTYPE_LEVEL | integer | 用户类型级别 |
| USERTYPE_GUID | string | 用户类型唯一标识 |
| USERTYPE_ICO | string | 用户类型图标 |
| USERTYPE_PROVINCE | integer | 所属省份 |
| USERTYPE_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| USERTYPE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| USERTYPE_DESC | string | 备注说明 |
| UserList | List<USERModel> | 用户列表 |

USERModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USER_ID | integer | 用户内码 |
| USER_IDS | string | 用户内码S |
| USER_ID_Encrypted | string | 用户内码（加密） |
| USERTYPE_ID | integer | 用户类型内码 |
| UserTypeIds | string | 用户类型内码集合 |
| USER_NAME | string | 用户名称 |
| USER_PASSPORT | string | 登录账户 |
| USER_PASSWORD | string | 账户密码 |
| USER_TIMEOUT | integer | 有效时间 |
| USER_INDEX | integer | 显示顺序 |
| USER_INDEFINIT | integer | 用户类型 |
| USER_EXPIRY | string | 授权时间 |
| USER_CITYAUTHORITY | string | 服务区权限 |
| USER_REPEATLOGON | integer | 允许重复登录 |
| USER_MOBILEPHONE | string | 手机号码 |
| USER_PROVINCE | integer | 用户省份 |
| PROVINCE_UNIT | string | 业主单位 |
| BUSINESSMAN_ID | integer | 商户内码 |
| BUSINESSMAN_IDS | string | 商户内码（查询条件） |
| BUSINESSMAN_NAME | string | 商户名称 |
| USER_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| SUPER_ADMIN | integer | 是否超级管理员（0：否；1：是） |
| USER_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| USER_DESC | string | 备注说明 |
| USER_HEADIMGURL | string | 用户头像地址 |
| IDENTITY_CODE | string | 短信验证码 |
| ServerpartIds | string | 用户服务区权限(查询条件) |
| ServerpartList | List<string> | 用户服务区权限列表 |
| ServerpartShopList | List<integer> | 用户服务区门店权限列表（内码） |
| ShopNameList | List<string> | 用户服务区门店权限列表（名称） |
| SystemRoleList | List<integer> | 用户角色权限列表 |
| AnalysisPermission | boolean | 是否有驿达看板权限 |
| PushPermission | boolean | 是否有微信推送权限 |
| PushList | List<CommonTypeModel> | 微信推送权限列表 |
| SYSTEMROLE_IDS | string | 系统角色内码 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### POST /Platform/GetUSERTYPEList
**名称**: 获取用户类型表列表
**Action**: `GetUSERTYPEList`

**场景**: 
用于 Platform 模块平台级配置、管理与公共能力支持。
**说明**: 
获取用户类型表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[USERTYPEModel] | Y | 查询条件对象 |

SearchModel[USERTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | USERTYPEModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

USERTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USERTYPE_ID | integer | 用户类型内码 |
| USERTYPE_NAME | string | 用户类型名称 |
| USERTYPE_PID | integer | 用户类型父级内码 |
| USERTYPE_INDEX | integer | 用户类型索引 |
| USERTYPE_LEVEL | integer | 用户类型级别 |
| USERTYPE_GUID | string | 用户类型唯一标识 |
| USERTYPE_ICO | string | 用户类型图标 |
| USERTYPE_PROVINCE | integer | 所属省份 |
| USERTYPE_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| USERTYPE_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| USERTYPE_DESC | string | 备注说明 |
| UserList | List<USERModel> | 用户列表 |

USERModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USER_ID | integer | 用户内码 |
| USER_IDS | string | 用户内码S |
| USER_ID_Encrypted | string | 用户内码（加密） |
| USERTYPE_ID | integer | 用户类型内码 |
| UserTypeIds | string | 用户类型内码集合 |
| USER_NAME | string | 用户名称 |
| USER_PASSPORT | string | 登录账户 |
| USER_PASSWORD | string | 账户密码 |
| USER_TIMEOUT | integer | 有效时间 |
| USER_INDEX | integer | 显示顺序 |
| USER_INDEFINIT | integer | 用户类型 |
| USER_EXPIRY | string | 授权时间 |
| USER_CITYAUTHORITY | string | 服务区权限 |
| USER_REPEATLOGON | integer | 允许重复登录 |
| USER_MOBILEPHONE | string | 手机号码 |
| USER_PROVINCE | integer | 用户省份 |
| PROVINCE_UNIT | string | 业主单位 |
| BUSINESSMAN_ID | integer | 商户内码 |
| BUSINESSMAN_IDS | string | 商户内码（查询条件） |
| BUSINESSMAN_NAME | string | 商户名称 |
| USER_PATTERN | integer | 数据模式（1000：业主；2000：商户） |
| SUPER_ADMIN | integer | 是否超级管理员（0：否；1：是） |
| USER_STATUS | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| USER_DESC | string | 备注说明 |
| USER_HEADIMGURL | string | 用户头像地址 |
| IDENTITY_CODE | string | 短信验证码 |
| ServerpartIds | string | 用户服务区权限(查询条件) |
| ServerpartList | List<string> | 用户服务区权限列表 |
| ServerpartShopList | List<integer> | 用户服务区门店权限列表（内码） |
| ShopNameList | List<string> | 用户服务区门店权限列表（名称） |
| SystemRoleList | List<integer> | 用户角色权限列表 |
| AnalysisPermission | boolean | 是否有驿达看板权限 |
| PushPermission | boolean | 是否有微信推送权限 |
| PushList | List<CommonTypeModel> | 微信推送权限列表 |
| SYSTEMROLE_IDS | string | 系统角色内码 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[USERTYPEModel]]> | 返回数据集合 |

JsonMsg[JsonList[USERTYPEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[USERTYPEModel] | 返回对象 |

JsonList[USERTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<USERTYPEModel> | 返回数据集 |

## 服务区基础信息相关接口【BaseInfoController】

---
### GET /BaseInfo/BindingMerchantTree
**名称**: 3. 绑定经营商户树
**Action**: `BindingMerchantTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定经营商户树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| MerchantPid | integer | N | 父级商户内码 |
| ProvinceCode | integer | N | 省份编码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /BaseInfo/BindingOwnerUnitDDL
**名称**: 4. 绑定业主单位下拉框
**Action**: `BindingOwnerUnitDDL`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定业主单位下拉框
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | N | 省份编码 |
| DataType | integer | N | 数据类型【默认0】：<br />0【返回业主单位编码】<br />1【返回业主单位内码】 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[CommonTypeModel]]> | 返回数据集合 |

JsonMsg[JsonList[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[CommonTypeModel] | 返回对象 |

JsonList[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<CommonTypeModel> | 返回数据集 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /BaseInfo/BindingOwnerUnitTree
**名称**: 5. 绑定业主单位树
**Action**: `BindingOwnerUnitTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定业主单位树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| DataType | integer | N | 数据类型【默认0】：<br />0【返回业主单位编码】<br />1【返回业主单位内码】 |
| OwnerUnitPid | integer | N | 父级业主单位内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /BaseInfo/GetAUTOSTATISTICSDetail
**名称**: 35. 获取自定义统计归口明细
**Action**: `GetAUTOSTATISTICSDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取自定义统计归口明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| AUTOSTATISTICSId | integer | Y | 自定义归口统计内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[AUTOSTATISTICSModel]> | 返回数据集合 |

JsonMsg[AUTOSTATISTICSModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | AUTOSTATISTICSModel | 返回对象 |

AUTOSTATISTICSModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| AUTOSTATISTICS_ID | integer | 统计归口内码 |
| AUTOSTATISTICS_PID | integer | 父级内码 |
| AUTOSTATISTICS_NAME | string | 归口名称 |
| AUTOSTATISTICS_VALUE | string | 归口值域 |
| AUTOSTATISTICS_INDEX | integer | 归口索引 |
| AUTOSTATISTICS_TYPE | integer | 归口类型（1000：考核口径；2000：经营业态；2010：业态考核规则；3000：考核部门；4000：供应商类别；合作商户分类） |
| STATISTICS_TYPE | integer | 统计归口 |
| INELASTIC_DEMAND | integer | 刚需类型 |
| AUTOSTATISTICS_ICO | string | 显示图标 |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_NAME | string | 业主单位 |
| PROVINCE_CODE | integer | 省份标识 |
| AUTOSTATISTICS_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| AUTOSTATISTICS_DESC | string | 备注说明 |

---
### POST /BaseInfo/GetAUTOSTATISTICSDetail
**名称**: 36. 获取自定义统计归口明细
**Action**: `GetAUTOSTATISTICSDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取自定义统计归口明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| AUTOSTATISTICSId | integer | Y | 自定义归口统计内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[AUTOSTATISTICSModel]> | 返回数据集合 |

JsonMsg[AUTOSTATISTICSModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | AUTOSTATISTICSModel | 返回对象 |

AUTOSTATISTICSModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| AUTOSTATISTICS_ID | integer | 统计归口内码 |
| AUTOSTATISTICS_PID | integer | 父级内码 |
| AUTOSTATISTICS_NAME | string | 归口名称 |
| AUTOSTATISTICS_VALUE | string | 归口值域 |
| AUTOSTATISTICS_INDEX | integer | 归口索引 |
| AUTOSTATISTICS_TYPE | integer | 归口类型（1000：考核口径；2000：经营业态；2010：业态考核规则；3000：考核部门；4000：供应商类别；合作商户分类） |
| STATISTICS_TYPE | integer | 统计归口 |
| INELASTIC_DEMAND | integer | 刚需类型 |
| AUTOSTATISTICS_ICO | string | 显示图标 |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_NAME | string | 业主单位 |
| PROVINCE_CODE | integer | 省份标识 |
| AUTOSTATISTICS_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| AUTOSTATISTICS_DESC | string | 备注说明 |

---
### GET /BaseInfo/GetAssetsRevenueAmount
**名称**: 37. 获取服务区资产总效益
**Action**: `GetAssetsRevenueAmount`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区资产总效益
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchMonth | string | Y | 查询收益月份，格式yyyyMM |
| ServerpartIds | string | Y | 查询服务区ID |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[List[RevenueAmountModel]]]> | 返回数据集合 |

JsonMsg[JsonList[List[RevenueAmountModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[List[RevenueAmountModel]] | 返回对象 |

JsonList[List[RevenueAmountModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<array> | 返回数据集 |

---
### GET /BaseInfo/GetAutoStatisticsTreeList
**名称**: 38. 获取自定义统计归口表 树形列表
**Action**: `GetAutoStatisticsTreeList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
1. 统计归口包含多种归口类型数据。1.1 归口类型AutoStatistics_Type包含：1000：考核口径； 2000：经营业态； 2010：业态考核规则； 3000：考核部门； 4000：供应商类别；合作商户分类2. 统计归口类型省份内码ID，业主内码ID为必传参数。
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | Y | 省份编码 |
| OwnerUnit_Id | integer | Y | 业主内码ID |
| AutoStatistics_Type | integer | Y | 归口类型 |
| AutoStatistics_PID | integer | N | 统计归口父级内码 |
| AutoStatistics_State | integer | N | 有效状态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[AUTOSTATISTICSModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[AUTOSTATISTICSModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[AUTOSTATISTICSModel]] | 返回对象 |

JsonList[NestingModel[AUTOSTATISTICSModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[AUTOSTATISTICSModel]> | 返回数据集 |

NestingModel[AUTOSTATISTICSModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | AUTOSTATISTICSModel | 结点 |
| children | List<NestingModel[AUTOSTATISTICSModel]> | 子级 |

AUTOSTATISTICSModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| AUTOSTATISTICS_ID | integer | 统计归口内码 |
| AUTOSTATISTICS_PID | integer | 父级内码 |
| AUTOSTATISTICS_NAME | string | 归口名称 |
| AUTOSTATISTICS_VALUE | string | 归口值域 |
| AUTOSTATISTICS_INDEX | integer | 归口索引 |
| AUTOSTATISTICS_TYPE | integer | 归口类型（1000：考核口径；2000：经营业态；2010：业态考核规则；3000：考核部门；4000：供应商类别；合作商户分类） |
| STATISTICS_TYPE | integer | 统计归口 |
| INELASTIC_DEMAND | integer | 刚需类型 |
| AUTOSTATISTICS_ICO | string | 显示图标 |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_NAME | string | 业主单位 |
| PROVINCE_CODE | integer | 省份标识 |
| AUTOSTATISTICS_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| AUTOSTATISTICS_DESC | string | 备注说明 |

---
### POST /BaseInfo/GetAutoStatisticsTreeList
**名称**: 39. 获取自定义统计归口表 树形列表
**Action**: `GetAutoStatisticsTreeList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
1. 统计归口包含多种归口类型数据。1.1 归口类型AutoStatistics_Type包含：1000：考核口径； 2000：经营业态； 2010：业态考核规则； 3000：考核部门； 4000：供应商类别；合作商户分类2. 统计归口类型省份内码ID，业主内码ID为必传参数。
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | Y | 省份编码 |
| OwnerUnit_Id | integer | Y | 业主内码ID |
| AutoStatistics_Type | integer | Y | 归口类型 |
| AutoStatistics_PID | integer | N | 统计归口父级内码 |
| AutoStatistics_State | integer | N | 有效状态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[AUTOSTATISTICSModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[AUTOSTATISTICSModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[AUTOSTATISTICSModel]] | 返回对象 |

JsonList[NestingModel[AUTOSTATISTICSModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[AUTOSTATISTICSModel]> | 返回数据集 |

NestingModel[AUTOSTATISTICSModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | AUTOSTATISTICSModel | 结点 |
| children | List<NestingModel[AUTOSTATISTICSModel]> | 子级 |

AUTOSTATISTICSModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| AUTOSTATISTICS_ID | integer | 统计归口内码 |
| AUTOSTATISTICS_PID | integer | 父级内码 |
| AUTOSTATISTICS_NAME | string | 归口名称 |
| AUTOSTATISTICS_VALUE | string | 归口值域 |
| AUTOSTATISTICS_INDEX | integer | 归口索引 |
| AUTOSTATISTICS_TYPE | integer | 归口类型（1000：考核口径；2000：经营业态；2010：业态考核规则；3000：考核部门；4000：供应商类别；合作商户分类） |
| STATISTICS_TYPE | integer | 统计归口 |
| INELASTIC_DEMAND | integer | 刚需类型 |
| AUTOSTATISTICS_ICO | string | 显示图标 |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_NAME | string | 业主单位 |
| PROVINCE_CODE | integer | 省份标识 |
| AUTOSTATISTICS_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| AUTOSTATISTICS_DESC | string | 备注说明 |

---
### GET /BaseInfo/GetBrandDetail
**名称**: 40. 获取品牌表明细
**Action**: `GetBrandDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取品牌表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BrandId | integer | Y | 品牌表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[BRANDModel]> | 返回数据集合 |

JsonMsg[BRANDModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | BRANDModel | 返回对象 |

BRANDModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| BRAND_ID | integer | 内码 |
| BRAND_PID | integer | 上级内码 |
| BRAND_INDEX | integer | 品牌索引 |
| BRAND_NAME | string | 品牌名称 |
| BRAND_CATEGORY | integer | 品牌分类（1000：经营品牌；2000：商城品牌） |
| BRAND_INDUSTRY | integer | 经营业态 |
| BUSINESSTRADE_NAME | string | 经营业态名称 |
| BRAND_TYPE | integer | 品牌类型 |
| BRAND_INTRO | string | 品牌图标 |
| BRAND_STATE | integer | 有效状态 |
| WECHATAPPSIGN_ID | integer | 小程序内码 |
| WECHATAPPSIGN_NAME | string | 小程序名字 |
| WECHATAPP_APPID | string | 小程序APPID |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_NAME | string | 业主单位 |
| PROVINCE_CODE | integer | 省份标识 |
| STAFF_ID | integer | 人员内码 |
| STAFF_NAME | string | 配置人员 |
| OPERATE_DATE | string | 配置时间 |
| BRAND_DESC | string | 品牌介绍 |
| MANAGE_TYPE | integer | 建议提成比例 |
| COMMISSION_RATIO | string | 建议提成比例 |
| SPREGIONTYPE_IDS | string | 片区内码集合（用于查询多个片区） |
| SERVERPART_IDS | string | 服务区内码集合（用于查询多个服务区） |
| MerchantID | string | 经营商户内码 |
| MerchantID_Encrypt | string | 经营商户加密内码 |
| MerchantName | string | 经营商户 |
| ServerpartList | List<CommonModel> | 经营服务区列表 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

---
### GET /BaseInfo/GetBrandIdTree
**名称**: 41. 绑定经营品牌内码树
**Action**: `GetBrandIdTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定经营品牌内码树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| Pid | integer | N | 经营业态内码 |
| ProvinceCode | integer | N | 省份编码 |
| OwnerUnitId | integer | N | 业主单位内码 |
| BrandState | integer | N | 有效状态 |
| SearchKey | string | N | 模糊查询条件 |
| ShowWholePower | boolean | N | 显示全局权限 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### POST /BaseInfo/GetBrandList
**名称**: 42. 获取品牌表列表
**Action**: `GetBrandList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取品牌表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[BRANDModel] | Y | 查询条件对象 |

SearchModel[BRANDModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | BRANDModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

BRANDModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| BRAND_ID | integer | 内码 |
| BRAND_PID | integer | 上级内码 |
| BRAND_INDEX | integer | 品牌索引 |
| BRAND_NAME | string | 品牌名称 |
| BRAND_CATEGORY | integer | 品牌分类（1000：经营品牌；2000：商城品牌） |
| BRAND_INDUSTRY | integer | 经营业态 |
| BUSINESSTRADE_NAME | string | 经营业态名称 |
| BRAND_TYPE | integer | 品牌类型 |
| BRAND_INTRO | string | 品牌图标 |
| BRAND_STATE | integer | 有效状态 |
| WECHATAPPSIGN_ID | integer | 小程序内码 |
| WECHATAPPSIGN_NAME | string | 小程序名字 |
| WECHATAPP_APPID | string | 小程序APPID |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_NAME | string | 业主单位 |
| PROVINCE_CODE | integer | 省份标识 |
| STAFF_ID | integer | 人员内码 |
| STAFF_NAME | string | 配置人员 |
| OPERATE_DATE | string | 配置时间 |
| BRAND_DESC | string | 品牌介绍 |
| MANAGE_TYPE | integer | 建议提成比例 |
| COMMISSION_RATIO | string | 建议提成比例 |
| SPREGIONTYPE_IDS | string | 片区内码集合（用于查询多个片区） |
| SERVERPART_IDS | string | 服务区内码集合（用于查询多个服务区） |
| MerchantID | string | 经营商户内码 |
| MerchantID_Encrypt | string | 经营商户加密内码 |
| MerchantName | string | 经营商户 |
| ServerpartList | List<CommonModel> | 经营服务区列表 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[BRANDModel]]> | 返回数据集合 |

JsonMsg[JsonList[BRANDModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[BRANDModel] | 返回对象 |

JsonList[BRANDModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<BRANDModel> | 返回数据集 |

---
### GET /BaseInfo/GetBusinessBrandList
**名称**: 43. 查询门店经营品牌列表
**Action**: `GetBusinessBrandList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
查询门店经营品牌列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartShopIds | string | Y | 门店内码集合 |
| ShowWholePower | boolean | N | 显示全局权限 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[BRANDModel]]> | 返回数据集合 |

JsonMsg[JsonList[BRANDModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[BRANDModel] | 返回对象 |

JsonList[BRANDModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<BRANDModel> | 返回数据集 |

BRANDModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| BRAND_ID | integer | 内码 |
| BRAND_PID | integer | 上级内码 |
| BRAND_INDEX | integer | 品牌索引 |
| BRAND_NAME | string | 品牌名称 |
| BRAND_CATEGORY | integer | 品牌分类（1000：经营品牌；2000：商城品牌） |
| BRAND_INDUSTRY | integer | 经营业态 |
| BUSINESSTRADE_NAME | string | 经营业态名称 |
| BRAND_TYPE | integer | 品牌类型 |
| BRAND_INTRO | string | 品牌图标 |
| BRAND_STATE | integer | 有效状态 |
| WECHATAPPSIGN_ID | integer | 小程序内码 |
| WECHATAPPSIGN_NAME | string | 小程序名字 |
| WECHATAPP_APPID | string | 小程序APPID |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_NAME | string | 业主单位 |
| PROVINCE_CODE | integer | 省份标识 |
| STAFF_ID | integer | 人员内码 |
| STAFF_NAME | string | 配置人员 |
| OPERATE_DATE | string | 配置时间 |
| BRAND_DESC | string | 品牌介绍 |
| MANAGE_TYPE | integer | 建议提成比例 |
| COMMISSION_RATIO | string | 建议提成比例 |
| SPREGIONTYPE_IDS | string | 片区内码集合（用于查询多个片区） |
| SERVERPART_IDS | string | 服务区内码集合（用于查询多个服务区） |
| MerchantID | string | 经营商户内码 |
| MerchantID_Encrypt | string | 经营商户加密内码 |
| MerchantName | string | 经营商户 |
| ServerpartList | List<CommonModel> | 经营服务区列表 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

---
### GET /BaseInfo/GetBusinessTradeDetail
**名称**: 44. 获取经营业态明细
**Action**: `GetBusinessTradeDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取经营业态明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessTradeId | integer | Y | 经营业态内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[AUTOSTATISTICSModel]> | 返回数据集合 |

JsonMsg[AUTOSTATISTICSModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | AUTOSTATISTICSModel | 返回对象 |

AUTOSTATISTICSModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| AUTOSTATISTICS_ID | integer | 统计归口内码 |
| AUTOSTATISTICS_PID | integer | 父级内码 |
| AUTOSTATISTICS_NAME | string | 归口名称 |
| AUTOSTATISTICS_VALUE | string | 归口值域 |
| AUTOSTATISTICS_INDEX | integer | 归口索引 |
| AUTOSTATISTICS_TYPE | integer | 归口类型（1000：考核口径；2000：经营业态；2010：业态考核规则；3000：考核部门；4000：供应商类别；合作商户分类） |
| STATISTICS_TYPE | integer | 统计归口 |
| INELASTIC_DEMAND | integer | 刚需类型 |
| AUTOSTATISTICS_ICO | string | 显示图标 |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_NAME | string | 业主单位 |
| PROVINCE_CODE | integer | 省份标识 |
| AUTOSTATISTICS_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| AUTOSTATISTICS_DESC | string | 备注说明 |

---
### POST /BaseInfo/GetBusinessTradeDetail
**名称**: 45. 获取经营业态明细
**Action**: `GetBusinessTradeDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取经营业态明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessTradeId | integer | Y | 经营业态内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[AUTOSTATISTICSModel]> | 返回数据集合 |

JsonMsg[AUTOSTATISTICSModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | AUTOSTATISTICSModel | 返回对象 |

AUTOSTATISTICSModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| AUTOSTATISTICS_ID | integer | 统计归口内码 |
| AUTOSTATISTICS_PID | integer | 父级内码 |
| AUTOSTATISTICS_NAME | string | 归口名称 |
| AUTOSTATISTICS_VALUE | string | 归口值域 |
| AUTOSTATISTICS_INDEX | integer | 归口索引 |
| AUTOSTATISTICS_TYPE | integer | 归口类型（1000：考核口径；2000：经营业态；2010：业态考核规则；3000：考核部门；4000：供应商类别；合作商户分类） |
| STATISTICS_TYPE | integer | 统计归口 |
| INELASTIC_DEMAND | integer | 刚需类型 |
| AUTOSTATISTICS_ICO | string | 显示图标 |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_NAME | string | 业主单位 |
| PROVINCE_CODE | integer | 省份标识 |
| AUTOSTATISTICS_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| AUTOSTATISTICS_DESC | string | 备注说明 |

---
### GET /BaseInfo/GetBusinessTradeEnum
**名称**: 46. 查询经营业态枚举树
**Action**: `GetBusinessTradeEnum`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
查询经营业态枚举树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessTrade_PID | integer | N | 经营业态父级内码 |
| ProvinceCode | integer | N | 省份编码 |
| OwnerUnitId | integer | N | 业主单位内码 |
| BusinessTradeState | integer | N | 有效状态 |
| SearchKey | string | N | 模糊查询内容 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### POST /BaseInfo/GetBusinessTradeEnum
**名称**: 47. 查询经营业态枚举树
**Action**: `GetBusinessTradeEnum`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
查询经营业态枚举树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessTrade_PID | integer | N | 经营业态父级内码 |
| ProvinceCode | integer | N | 省份编码 |
| OwnerUnitId | integer | N | 业主单位内码 |
| BusinessTradeState | integer | N | 有效状态 |
| SearchKey | string | N | 模糊查询内容 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /BaseInfo/GetBusinessTradeIdTree
**名称**: 48. 获取经营业态内码树
**Action**: `GetBusinessTradeIdTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取经营业态内码树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| Pid | string | N | 上级内码 |
| OWNERUNIT_ID | string | N | 业主内码 |
| ProvinceCode | string | N | 省份标识 |
| BUSINESSTRADE_STATE | string | N | 有效状态 |
| SearchKey | string | N | 模糊查询内容 |
| ShowWholePower | boolean | N | 显示全局权限 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### POST /BaseInfo/GetBusinessTradeList
**名称**: 49. 获取经营业态列表
**Action**: `GetBusinessTradeList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取经营业态列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[AUTOSTATISTICSModel] | Y | 查询条件对象 |

SearchModel[AUTOSTATISTICSModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | AUTOSTATISTICSModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

AUTOSTATISTICSModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| AUTOSTATISTICS_ID | integer | 统计归口内码 |
| AUTOSTATISTICS_PID | integer | 父级内码 |
| AUTOSTATISTICS_NAME | string | 归口名称 |
| AUTOSTATISTICS_VALUE | string | 归口值域 |
| AUTOSTATISTICS_INDEX | integer | 归口索引 |
| AUTOSTATISTICS_TYPE | integer | 归口类型（1000：考核口径；2000：经营业态；2010：业态考核规则；3000：考核部门；4000：供应商类别；合作商户分类） |
| STATISTICS_TYPE | integer | 统计归口 |
| INELASTIC_DEMAND | integer | 刚需类型 |
| AUTOSTATISTICS_ICO | string | 显示图标 |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_NAME | string | 业主单位 |
| PROVINCE_CODE | integer | 省份标识 |
| AUTOSTATISTICS_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| AUTOSTATISTICS_DESC | string | 备注说明 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[AUTOSTATISTICSModel]]> | 返回数据集合 |

JsonMsg[JsonList[AUTOSTATISTICSModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[AUTOSTATISTICSModel] | 返回对象 |

JsonList[AUTOSTATISTICSModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<AUTOSTATISTICSModel> | 返回数据集 |

---
### GET /BaseInfo/GetBusinessTradeTree
**名称**: 50. 查询经营业态树
**Action**: `GetBusinessTradeTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
查询经营业态树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessTrade_PID | integer | N | 经营业态父级内码 |
| ProvinceCode | integer | N | 省份编码 |
| OwnerUnitId | integer | N | 业主单位内码 |
| BusinessTradeState | integer | N | 有效状态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[AUTOSTATISTICSModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[AUTOSTATISTICSModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[AUTOSTATISTICSModel]] | 返回对象 |

JsonList[NestingModel[AUTOSTATISTICSModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[AUTOSTATISTICSModel]> | 返回数据集 |

NestingModel[AUTOSTATISTICSModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | AUTOSTATISTICSModel | 结点 |
| children | List<NestingModel[AUTOSTATISTICSModel]> | 子级 |

AUTOSTATISTICSModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| AUTOSTATISTICS_ID | integer | 统计归口内码 |
| AUTOSTATISTICS_PID | integer | 父级内码 |
| AUTOSTATISTICS_NAME | string | 归口名称 |
| AUTOSTATISTICS_VALUE | string | 归口值域 |
| AUTOSTATISTICS_INDEX | integer | 归口索引 |
| AUTOSTATISTICS_TYPE | integer | 归口类型（1000：考核口径；2000：经营业态；2010：业态考核规则；3000：考核部门；4000：供应商类别；合作商户分类） |
| STATISTICS_TYPE | integer | 统计归口 |
| INELASTIC_DEMAND | integer | 刚需类型 |
| AUTOSTATISTICS_ICO | string | 显示图标 |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_NAME | string | 业主单位 |
| PROVINCE_CODE | integer | 省份标识 |
| AUTOSTATISTICS_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| AUTOSTATISTICS_DESC | string | 备注说明 |

---
### POST /BaseInfo/GetBusinessTradeTree
**名称**: 51. 查询经营业态树
**Action**: `GetBusinessTradeTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
查询经营业态树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessTrade_PID | integer | N | 经营业态父级内码 |
| ProvinceCode | integer | N | 省份编码 |
| OwnerUnitId | integer | N | 业主单位内码 |
| BusinessTradeState | integer | N | 有效状态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[AUTOSTATISTICSModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[AUTOSTATISTICSModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[AUTOSTATISTICSModel]] | 返回对象 |

JsonList[NestingModel[AUTOSTATISTICSModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[AUTOSTATISTICSModel]> | 返回数据集 |

NestingModel[AUTOSTATISTICSModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | AUTOSTATISTICSModel | 结点 |
| children | List<NestingModel[AUTOSTATISTICSModel]> | 子级 |

AUTOSTATISTICSModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| AUTOSTATISTICS_ID | integer | 统计归口内码 |
| AUTOSTATISTICS_PID | integer | 父级内码 |
| AUTOSTATISTICS_NAME | string | 归口名称 |
| AUTOSTATISTICS_VALUE | string | 归口值域 |
| AUTOSTATISTICS_INDEX | integer | 归口索引 |
| AUTOSTATISTICS_TYPE | integer | 归口类型（1000：考核口径；2000：经营业态；2010：业态考核规则；3000：考核部门；4000：供应商类别；合作商户分类） |
| STATISTICS_TYPE | integer | 统计归口 |
| INELASTIC_DEMAND | integer | 刚需类型 |
| AUTOSTATISTICS_ICO | string | 显示图标 |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_NAME | string | 业主单位 |
| PROVINCE_CODE | integer | 省份标识 |
| AUTOSTATISTICS_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人内码 |
| STAF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| AUTOSTATISTICS_DESC | string | 备注说明 |

---
### GET /BaseInfo/GetCASHWORKERDetail
**名称**: 52. 获取收银人员表明细
**Action**: `GetCASHWORKERDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取收银人员表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| CASHWORKERId | integer | Y | 收银人员表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[CASHWORKERModel]> | 返回数据集合 |

JsonMsg[CASHWORKERModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | CASHWORKERModel | 返回对象 |

CASHWORKERModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| CASHWORKER_ID | integer | 员工内码 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| CASHWORKER_NAME | string | 员工名称 |
| CASHWORKER_LOGINNAME | string | 收银工号 |
| CASHWORKER_LOGINPWD | string | 工号密码 |
| CASHWORKER_TYPE | integer | 员工类型 |
| WORKER_OTHER | string | 收银系统权限 |
| POST | string | 员工岗位 |
| SERVERPART_CODE | string | 服务区编码 |
| SERVERPART_CODES | string | 服务区编码(查询条件) |
| WORKER_VALID | integer | 有效状态 |
| OPERATE_NAME | string | 添加人名称 |
| OPERATE_DATE | string | 添加时间 |
| OPERATE_DATE_Start | string | 添加时间(查询条件) |
| OPERATE_DATE_End | string | 添加时间(查询条件) |
| WORK_OLD | string | 员工工作年龄 |
| LINKTEL | string | 员工联系方式 |
| WORKER_ADDRESS | string | 员工住址 |
| WORKER_CODE | string | 员工编号 |
| BIRTH | string | 员工生日 |
| HEALTHCERT | integer | 健康证 |
| PERSONCERT | string | 个人证件 |
| EDUCATIONAL | integer | 教育证 |
| DISCOUNT_RATE | number | 折扣率 |
| OPERATE_ID | integer | 添加人内码 |
| ServerPart_Name | string | 服务区名称 |

---
### POST /BaseInfo/GetCASHWORKERList
**名称**: 53. 获取收银人员表列表
**Action**: `GetCASHWORKERList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取收银人员表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[CASHWORKERModel] | Y | 查询条件对象 |

SearchModel[CASHWORKERModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | CASHWORKERModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

CASHWORKERModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| CASHWORKER_ID | integer | 员工内码 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| CASHWORKER_NAME | string | 员工名称 |
| CASHWORKER_LOGINNAME | string | 收银工号 |
| CASHWORKER_LOGINPWD | string | 工号密码 |
| CASHWORKER_TYPE | integer | 员工类型 |
| WORKER_OTHER | string | 收银系统权限 |
| POST | string | 员工岗位 |
| SERVERPART_CODE | string | 服务区编码 |
| SERVERPART_CODES | string | 服务区编码(查询条件) |
| WORKER_VALID | integer | 有效状态 |
| OPERATE_NAME | string | 添加人名称 |
| OPERATE_DATE | string | 添加时间 |
| OPERATE_DATE_Start | string | 添加时间(查询条件) |
| OPERATE_DATE_End | string | 添加时间(查询条件) |
| WORK_OLD | string | 员工工作年龄 |
| LINKTEL | string | 员工联系方式 |
| WORKER_ADDRESS | string | 员工住址 |
| WORKER_CODE | string | 员工编号 |
| BIRTH | string | 员工生日 |
| HEALTHCERT | integer | 健康证 |
| PERSONCERT | string | 个人证件 |
| EDUCATIONAL | integer | 教育证 |
| DISCOUNT_RATE | number | 折扣率 |
| OPERATE_ID | integer | 添加人内码 |
| ServerPart_Name | string | 服务区名称 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[CASHWORKERModel]]> | 返回数据集合 |

JsonMsg[JsonList[CASHWORKERModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[CASHWORKERModel] | 返回对象 |

JsonList[CASHWORKERModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<CASHWORKERModel> | 返回数据集 |

---
### GET /BaseInfo/GetCOMMODITYDetail
**名称**: 54. 获取服务区在售商品明细
**Action**: `GetCOMMODITYDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区在售商品明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| COMMODITYId | integer | Y | 在售商品内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[SaleCommodityModel]> | 返回数据集合 |

JsonMsg[SaleCommodityModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | SaleCommodityModel | 返回对象 |

SaleCommodityModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| COMMODITY_ID | integer | 商品内码 |
| COMMODITY_TYPE | string | 商品类型 |
| COMMODITY_CODE | string | 商品编码 |
| COMMODITY_NAME | string | 商品名称 |
| COMMODITY_BARCODE | string | 商品条码 |
| COMMODITY_EN | string | 商品英文缩写 |
| COMMODITY_UNIT | string | 商品单位 |
| COMMODITY_RULE | string | 商品规格 |
| COMMODITY_ORI | string | 商品产地 |
| COMMODITY_GRADE | string | 商品质量等级 |
| COMMODITY_RETAILPRICE | number | 商品零售价 |
| COMMODITY_MEMBERPRICE | number | 商品会员价 |
| COMMODITY_PURCHASEPRICE | number | 商品进货价 |
| DUTY_PARAGRAPH | integer | 进价税率 |
| RETAIL_DUTY | integer | 零售税率 |
| ADDTIME | string | 添加时间 |
| CANSALE | integer | 是否可售 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码（查询字段） |
| SERVERPART_NAME | string | 服务区名称 |
| SERVERPARTSHOP_IDS | string | 门店内码集合 |
| PROVINCE_CODE | integer | 省份编码 |
| BUSINESSTYPE | integer | 商品业态 |
| SHOPNAME | string | 门店名称 |
| ISBULK | integer | 是否散装 |
| METERINGMETHOD | integer | 称重方式 |
| COMMODITY_SYMBOL | string | 商品标识 |
| COMMODITY_HOTKEY | string | 商品快捷键 |
| USERDEFINEDTYPE_ID | integer | 自定义类别内码 |
| HIGHWAYPROINST_ID | integer | 业务流程内码 |
| OPERATE_DATE | string | 修改时间 |
| COMMODITY_STATE | integer | 商品状态 |
| COMMODITY_DESC | string | 商品说明 |
| COMMODITY_BUSINESS_ID | integer | 商品内码 |
| QUALIFICATION_ID | string | 资质证书内码 |
| QUALIFICATIONList | List<QUALIFICATIONModel> | 资质证书集合 |
| originCommodity | OriginCommodityModel | 原商品数据 |

QUALIFICATIONModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QUALIFICATION_ID | integer | 资质证书内码 |
| QUALIFICATION_TYPE | integer | 资质证书类型 |
| QUALIFICATION_NAME | string | 资质证书名称 |
| QUALIFICATION_CODE | string | 资质证书代码 |
| ISSUING_AUTHORITY | string | 颁发机构 |
| ISSUING_DATE | string | 颁发日期 |
| QUALIFICATION_STARTDATE | string | 有效开始日期 |
| QUALIFICATION_ENDDATE | string | 有效结束日期 |
| BUSINESSMAN_ID | integer | 商户内码 |
| SUPPLIER_ID | integer | 供应商内码 |
| SUPPLIER_NAME | string | 供应商名称 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人名称 |
| OPERATE_DATE | string | 操作时间 |
| QUALIFICATION_STATE | integer | 有效状态 |
| QUALIFICATION_STATESEARCH | string | 有效状态 |
| QUALIFICATION_DESC | string | 备注说明 |
| ImgList | List<PictureModel> | 资质证书图片列表 |

PictureModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ImageId | integer | 图片内码 |
| ImageType | integer | 图片类型 |
| ImageIndex | integer | 图片索引 |
| ImageName | string | 图片名称 |
| TableType | string | 数据表类型 |
| TableName | string | 数据表名称 |
| ImageUrl | string | 图片地址 |
| ImagePath | string | 图片相对路径（删除图片时提供的参数） |
| ImageDate | string | 图片日期 |
| IsImg | boolean | 是否图片 |

OriginCommodityModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| COMMODITY_TYPE | string | 商品类型 |
| COMMODITY_NAME | string | 商品名称 |
| COMMODITY_EN | string | 商品英文缩写 |
| COMMODITY_UNIT | string | 商品单位 |
| COMMODITY_RULE | string | 商品规格 |
| COMMODITY_ORI | string | 商品产地 |
| COMMODITY_GRADE | string | 商品质量等级 |
| COMMODITY_RETAILPRICE | number | 商品零售价 |
| COMMODITY_MEMBERPRICE | number | 商品会员价 |
| COMMODITY_PURCHASEPRICE | number | 商品进货价 |
| DUTY_PARAGRAPH | integer | 进价税率 |
| RETAIL_DUTY | integer | 零售税率 |
| CANSALE | integer | 是否可售 |
| ISBULK | integer | 是否散装 |
| METERINGMETHOD | integer | 称重方式 |
| COMMODITY_HOTKEY | string | 商品快捷键 |
| USERDEFINEDTYPE_ID | integer | 自定义类别内码 |
| HIGHWAYPROINST_ID | integer | 业务流程内码 |
| OPERATE_DATE | string | 修改时间 |
| COMMODITY_STATE | integer | 商品状态 |
| COMMODITY_DESC | string | 商品说明 |

---
### POST /BaseInfo/GetCOMMODITYList
**名称**: 55. 获取服务区在售商品列表
**Action**: `GetCOMMODITYList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区在售商品列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[SaleCommodityModel] | Y | 查询条件对象 |

SearchModel[SaleCommodityModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | SaleCommodityModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

SaleCommodityModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| COMMODITY_ID | integer | 商品内码 |
| COMMODITY_TYPE | string | 商品类型 |
| COMMODITY_CODE | string | 商品编码 |
| COMMODITY_NAME | string | 商品名称 |
| COMMODITY_BARCODE | string | 商品条码 |
| COMMODITY_EN | string | 商品英文缩写 |
| COMMODITY_UNIT | string | 商品单位 |
| COMMODITY_RULE | string | 商品规格 |
| COMMODITY_ORI | string | 商品产地 |
| COMMODITY_GRADE | string | 商品质量等级 |
| COMMODITY_RETAILPRICE | number | 商品零售价 |
| COMMODITY_MEMBERPRICE | number | 商品会员价 |
| COMMODITY_PURCHASEPRICE | number | 商品进货价 |
| DUTY_PARAGRAPH | integer | 进价税率 |
| RETAIL_DUTY | integer | 零售税率 |
| ADDTIME | string | 添加时间 |
| CANSALE | integer | 是否可售 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码（查询字段） |
| SERVERPART_NAME | string | 服务区名称 |
| SERVERPARTSHOP_IDS | string | 门店内码集合 |
| PROVINCE_CODE | integer | 省份编码 |
| BUSINESSTYPE | integer | 商品业态 |
| SHOPNAME | string | 门店名称 |
| ISBULK | integer | 是否散装 |
| METERINGMETHOD | integer | 称重方式 |
| COMMODITY_SYMBOL | string | 商品标识 |
| COMMODITY_HOTKEY | string | 商品快捷键 |
| USERDEFINEDTYPE_ID | integer | 自定义类别内码 |
| HIGHWAYPROINST_ID | integer | 业务流程内码 |
| OPERATE_DATE | string | 修改时间 |
| COMMODITY_STATE | integer | 商品状态 |
| COMMODITY_DESC | string | 商品说明 |
| COMMODITY_BUSINESS_ID | integer | 商品内码 |
| QUALIFICATION_ID | string | 资质证书内码 |
| QUALIFICATIONList | List<QUALIFICATIONModel> | 资质证书集合 |
| originCommodity | OriginCommodityModel | 原商品数据 |

QUALIFICATIONModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QUALIFICATION_ID | integer | 资质证书内码 |
| QUALIFICATION_TYPE | integer | 资质证书类型 |
| QUALIFICATION_NAME | string | 资质证书名称 |
| QUALIFICATION_CODE | string | 资质证书代码 |
| ISSUING_AUTHORITY | string | 颁发机构 |
| ISSUING_DATE | string | 颁发日期 |
| QUALIFICATION_STARTDATE | string | 有效开始日期 |
| QUALIFICATION_ENDDATE | string | 有效结束日期 |
| BUSINESSMAN_ID | integer | 商户内码 |
| SUPPLIER_ID | integer | 供应商内码 |
| SUPPLIER_NAME | string | 供应商名称 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人名称 |
| OPERATE_DATE | string | 操作时间 |
| QUALIFICATION_STATE | integer | 有效状态 |
| QUALIFICATION_STATESEARCH | string | 有效状态 |
| QUALIFICATION_DESC | string | 备注说明 |
| ImgList | List<PictureModel> | 资质证书图片列表 |

PictureModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ImageId | integer | 图片内码 |
| ImageType | integer | 图片类型 |
| ImageIndex | integer | 图片索引 |
| ImageName | string | 图片名称 |
| TableType | string | 数据表类型 |
| TableName | string | 数据表名称 |
| ImageUrl | string | 图片地址 |
| ImagePath | string | 图片相对路径（删除图片时提供的参数） |
| ImageDate | string | 图片日期 |
| IsImg | boolean | 是否图片 |

OriginCommodityModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| COMMODITY_TYPE | string | 商品类型 |
| COMMODITY_NAME | string | 商品名称 |
| COMMODITY_EN | string | 商品英文缩写 |
| COMMODITY_UNIT | string | 商品单位 |
| COMMODITY_RULE | string | 商品规格 |
| COMMODITY_ORI | string | 商品产地 |
| COMMODITY_GRADE | string | 商品质量等级 |
| COMMODITY_RETAILPRICE | number | 商品零售价 |
| COMMODITY_MEMBERPRICE | number | 商品会员价 |
| COMMODITY_PURCHASEPRICE | number | 商品进货价 |
| DUTY_PARAGRAPH | integer | 进价税率 |
| RETAIL_DUTY | integer | 零售税率 |
| CANSALE | integer | 是否可售 |
| ISBULK | integer | 是否散装 |
| METERINGMETHOD | integer | 称重方式 |
| COMMODITY_HOTKEY | string | 商品快捷键 |
| USERDEFINEDTYPE_ID | integer | 自定义类别内码 |
| HIGHWAYPROINST_ID | integer | 业务流程内码 |
| OPERATE_DATE | string | 修改时间 |
| COMMODITY_STATE | integer | 商品状态 |
| COMMODITY_DESC | string | 商品说明 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[SaleCommodityModel]]> | 返回数据集合 |

JsonMsg[JsonList[SaleCommodityModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[SaleCommodityModel] | 返回对象 |

JsonList[SaleCommodityModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<SaleCommodityModel> | 返回数据集 |

---
### GET /BaseInfo/GetCOMMODITYTYPEDetail
**名称**: 56. 获取商品类别明细
**Action**: `GetCOMMODITYTYPEDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取商品类别明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| COMMODITYTYPEId | integer | Y | 商品类别内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[COMMODITYTYPEModel]> | 返回数据集合 |

JsonMsg[COMMODITYTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | COMMODITYTYPEModel | 返回对象 |

COMMODITYTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| COMMODITYTYPE_ID | integer | 内码 |
| COMMODITYTYPE_NAME | string | 类别名称 |
| COMMODITYTYPE_EN | string | 分类简称 |
| COMMODITYTYPE_DESC | string | 分类说明 |
| COMMODITYTYPE_VALID | integer | 分类是否有效 |
| COMMODITYTYPE_PID | integer | 上级分类 |
| COMMODITYTYPE_INDEX | number | 顺序 |
| COMMODITYTYPE_CODE | number | 商品编码 |
| CIGARETTE_TYPE | integer | 香烟类型 |
| PROVINCE_ID | integer | 省份枚举 |
| PROVINCE_CODE | integer | 所属省份 |
| ADDTIME | string | 添加时间 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| OPERATE_DATE_Start | string | 操作时间(查询条件) |
| OPERATE_DATE_End | string | 操作时间(查询条件) |

---
### POST /BaseInfo/GetCOMMODITYTYPEList
**名称**: 57. 获取商品类别列表
**Action**: `GetCOMMODITYTYPEList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取商品类别列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[COMMODITYTYPEModel] | Y | 查询条件对象 |

SearchModel[COMMODITYTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | COMMODITYTYPEModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

COMMODITYTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| COMMODITYTYPE_ID | integer | 内码 |
| COMMODITYTYPE_NAME | string | 类别名称 |
| COMMODITYTYPE_EN | string | 分类简称 |
| COMMODITYTYPE_DESC | string | 分类说明 |
| COMMODITYTYPE_VALID | integer | 分类是否有效 |
| COMMODITYTYPE_PID | integer | 上级分类 |
| COMMODITYTYPE_INDEX | number | 顺序 |
| COMMODITYTYPE_CODE | number | 商品编码 |
| CIGARETTE_TYPE | integer | 香烟类型 |
| PROVINCE_ID | integer | 省份枚举 |
| PROVINCE_CODE | integer | 所属省份 |
| ADDTIME | string | 添加时间 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| OPERATE_DATE_Start | string | 操作时间(查询条件) |
| OPERATE_DATE_End | string | 操作时间(查询条件) |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[COMMODITYTYPEModel]]> | 返回数据集合 |

JsonMsg[JsonList[COMMODITYTYPEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[COMMODITYTYPEModel] | 返回对象 |

JsonList[COMMODITYTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<COMMODITYTYPEModel> | 返回数据集 |

---
### GET /BaseInfo/GetCombineBrandList
**名称**: 58. 获取品牌表列表
**Action**: `GetCombineBrandList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取品牌表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PROVINCE_CODE | integer | N | 省份编码 |
| SPREGIONTYPE_IDS | string | N | 片区内码 |
| SERVERPART_IDS | string | N | 服务区内码 |
| BRAND_INDUSTRY | string | N | 经营业态 |
| BRAND_TYPE | string | N | 品牌类型 |
| BRAND_STATE | string | N | 有效状态 |
| BRAND_NAME | string | N | 品牌名称（模糊查询内容） |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[BrandCombineModel]]> | 返回数据集合 |

JsonMsg[JsonList[BrandCombineModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[BrandCombineModel] | 返回对象 |

JsonList[BrandCombineModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<BrandCombineModel> | 返回数据集 |

BrandCombineModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| BRAND_ID | integer | 内码 |
| BRAND_PID | integer | 上级内码 |
| BRAND_INDEX | integer | 品牌索引 |
| BRAND_NAME | string | 品牌名称 |
| BRAND_CATEGORY | integer | 品牌分类（1000：经营品牌；2000：商城品牌） |
| BRAND_INDUSTRY | string | 经营业态 |
| BUSINESSTRADE_NAME | string | 经营业态名称 |
| BRAND_TYPE | string | 品牌类型 |
| BRAND_TYPENAME | string | 品牌类型名称 |
| BRAND_INTRO | string | 品牌图标 |
| BRAND_STATE | integer | 有效状态 |
| WECHATAPPSIGN_ID | integer | 小程序内码 |
| WECHATAPPSIGN_NAME | string | 小程序名字 |
| WECHATAPP_APPID | string | 小程序APPID |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_NAME | string | 业主单位 |
| PROVINCE_CODE | integer | 省份标识 |
| STAFF_ID | integer | 人员内码 |
| STAFF_NAME | string | 配置人员 |
| OPERATE_DATE | string | 配置时间 |
| BRAND_DESC | string | 品牌介绍 |
| COMMISSION_RATIO | string | 建议提成比例 |
| BUSINESS_TRADE | integer | 经营业态 |
| SETTLEMENT_MODES | integer | 结算模式 |
| REVENUE_AMOUNT | number | 营收金额 |
| REVENUE_DAILYAMOUNT | number | 日均营收 |
| ROYALTY_PRICE | number | 业主分润 |
| BusinessState | integer | 经营状态 |
| MerchantName | string | 经营商户 |
| ServerpartList | List<CommonModel> | 经营服务区列表 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

---
### GET /BaseInfo/GetCommodityTypeIdTree
**名称**: 59. 绑定商品类型内码树
**Action**: `GetCommodityTypeIdTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定商品类型内码树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| Pid | string | N | 上级分类 |
| ProvinceCode | string | N | 省份编码 |
| COMMODITYTYPE_VALID | string | N | 分类是否有效 |
| SearchKey | string | N | 模糊查询内容 |
| ShowWholePower | boolean | N | 显示全局权限 |
| ShowCode | boolean | N | 是否显示商品类型代码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /BaseInfo/GetNestingCOMMODITYTYPEList
**名称**: 60. 获取商品类别嵌套列表
**Action**: `GetNestingCOMMODITYTYPEList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取商品类别嵌套列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| COMMODITYTYPE_PID | string | N | 上级分类 |
| PROVINCE_CODE | string | N | 省份编码 |
| COMMODITYTYPE_VALID | string | N | 分类是否有效 |
| SearchKey | string | N | 模糊查询内容 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[COMMODITYTYPEModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[COMMODITYTYPEModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[COMMODITYTYPEModel]] | 返回对象 |

JsonList[NestingModel[COMMODITYTYPEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[COMMODITYTYPEModel]> | 返回数据集 |

NestingModel[COMMODITYTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | COMMODITYTYPEModel | 结点 |
| children | List<NestingModel[COMMODITYTYPEModel]> | 子级 |

COMMODITYTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| COMMODITYTYPE_ID | integer | 内码 |
| COMMODITYTYPE_NAME | string | 类别名称 |
| COMMODITYTYPE_EN | string | 分类简称 |
| COMMODITYTYPE_DESC | string | 分类说明 |
| COMMODITYTYPE_VALID | integer | 分类是否有效 |
| COMMODITYTYPE_PID | integer | 上级分类 |
| COMMODITYTYPE_INDEX | number | 顺序 |
| COMMODITYTYPE_CODE | number | 商品编码 |
| CIGARETTE_TYPE | integer | 香烟类型 |
| PROVINCE_ID | integer | 省份枚举 |
| PROVINCE_CODE | integer | 所属省份 |
| ADDTIME | string | 添加时间 |
| STAFF_ID | integer | 操作人内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| OPERATE_DATE_Start | string | 操作时间(查询条件) |
| OPERATE_DATE_End | string | 操作时间(查询条件) |

---
### GET /BaseInfo/GetNestingCOMMODITYTYPETree
**名称**: 61. 获取商品类别嵌套树
**Action**: `GetNestingCOMMODITYTYPETree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取商品类别嵌套树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| COMMODITYTYPE_PID | string | N | 上级分类 |
| PROVINCE_CODE | string | N | 省份编码 |
| COMMODITYTYPE_VALID | string | N | 分类是否有效 |
| SearchKey | string | N | 模糊查询内容 |
| ShowCode | boolean | N | 是否显示商品类型代码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /BaseInfo/GetNestingOwnerUnitList
**名称**: 62. 获取业主单位嵌套列表
**Action**: `GetNestingOwnerUnitList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取业主单位嵌套列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| OwnerUnitPID | integer | N | 业主单位父级内码 |
| ShowStatus | boolean | N | 是否只查询有效数据 |
| ProvinceCode | integer | N | 业务省份编码 |
| OwnerUnitNature | string | N | 单位性质：1000【业主】，2000【商户】 |
| OwnerUnitName | string | N | 业主单位名称（模糊查询） |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[OWNERUNITModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[OWNERUNITModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[OWNERUNITModel]] | 返回对象 |

JsonList[NestingModel[OWNERUNITModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[OWNERUNITModel]> | 返回数据集 |

NestingModel[OWNERUNITModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | OWNERUNITModel | 结点 |
| children | List<NestingModel[OWNERUNITModel]> | 子级 |

OWNERUNITModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_PID | integer | 父级内码 |
| PROVINCE_CODE | integer | 省份标识 |
| PROVINCE_BUSINESSCODE | integer | 业务省份标识 |
| OWNERUNIT_NAME | string | 业主单位 |
| OWNERUNIT_EN | string | 业主简称 |
| OWNERUNIT_NATURE | integer | 业主单位性质(1000：管理单位；2000：经营单位) |
| OWNERUNIT_GUID | string | 业主标识 |
| OWNERUNIT_INDEX | integer | 排序字段 |
| OWNERUNIT_ICO | string | 业主图标 |
| OWNERUNIT_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人员内码 |
| STAFF_NAME | string | 操作人员名称 |
| OPERATE_DATE | string | 操作时间 |
| OWNERUNIT_DESC | string | 备注 |
| ISSUPPORTPOINT | integer | 业主单位是否支持积分功能 |
| DOWNLOAD_DATE | string | 下载时间 |
| WECHATPUBLICSIGN_ID | integer | 公众号ID |

---
### GET /BaseInfo/GetOWNERUNITDetail
**名称**: 63. 获取业主单位管理表明细
**Action**: `GetOWNERUNITDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取业主单位管理表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| OWNERUNITId | integer | Y | 业主单位管理表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[OWNERUNITModel]> | 返回数据集合 |

JsonMsg[OWNERUNITModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | OWNERUNITModel | 返回对象 |

OWNERUNITModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_PID | integer | 父级内码 |
| PROVINCE_CODE | integer | 省份标识 |
| PROVINCE_BUSINESSCODE | integer | 业务省份标识 |
| OWNERUNIT_NAME | string | 业主单位 |
| OWNERUNIT_EN | string | 业主简称 |
| OWNERUNIT_NATURE | integer | 业主单位性质(1000：管理单位；2000：经营单位) |
| OWNERUNIT_GUID | string | 业主标识 |
| OWNERUNIT_INDEX | integer | 排序字段 |
| OWNERUNIT_ICO | string | 业主图标 |
| OWNERUNIT_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人员内码 |
| STAFF_NAME | string | 操作人员名称 |
| OPERATE_DATE | string | 操作时间 |
| OWNERUNIT_DESC | string | 备注 |
| ISSUPPORTPOINT | integer | 业主单位是否支持积分功能 |
| DOWNLOAD_DATE | string | 下载时间 |
| WECHATPUBLICSIGN_ID | integer | 公众号ID |

---
### POST /BaseInfo/GetOWNERUNITList
**名称**: 64. 获取业主单位管理表列表
**Action**: `GetOWNERUNITList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取业主单位管理表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[OWNERUNITModel] | Y | 查询条件对象 |

SearchModel[OWNERUNITModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | OWNERUNITModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

OWNERUNITModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| OWNERUNIT_ID | integer | 业主内码 |
| OWNERUNIT_PID | integer | 父级内码 |
| PROVINCE_CODE | integer | 省份标识 |
| PROVINCE_BUSINESSCODE | integer | 业务省份标识 |
| OWNERUNIT_NAME | string | 业主单位 |
| OWNERUNIT_EN | string | 业主简称 |
| OWNERUNIT_NATURE | integer | 业主单位性质(1000：管理单位；2000：经营单位) |
| OWNERUNIT_GUID | string | 业主标识 |
| OWNERUNIT_INDEX | integer | 排序字段 |
| OWNERUNIT_ICO | string | 业主图标 |
| OWNERUNIT_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人员内码 |
| STAFF_NAME | string | 操作人员名称 |
| OPERATE_DATE | string | 操作时间 |
| OWNERUNIT_DESC | string | 备注 |
| ISSUPPORTPOINT | integer | 业主单位是否支持积分功能 |
| DOWNLOAD_DATE | string | 下载时间 |
| WECHATPUBLICSIGN_ID | integer | 公众号ID |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[OWNERUNITModel]]> | 返回数据集合 |

JsonMsg[JsonList[OWNERUNITModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[OWNERUNITModel] | 返回对象 |

JsonList[OWNERUNITModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<OWNERUNITModel> | 返回数据集 |

---
### GET /BaseInfo/GetOwnerUnitIdTree
**名称**: 65. 绑定业主单位树
**Action**: `GetOwnerUnitIdTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定业主单位树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| Pid | integer | N | 父级业主单位内码 |
| ProvinceCode | string | N | 省份编码 |
| SearchKey | string | N | 模糊查询条件 |
| ShowWholePower | boolean | N | 显示全局权限 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /BaseInfo/GetPROPERTYASSETSDetail
**名称**: 66. 获取服务区资产表明细
**Action**: `GetPROPERTYASSETSDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区资产表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PROPERTYASSETSId | integer | Y | 服务区资产表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[PROPERTYASSETSModelDetail]> | 返回数据集合 |

JsonMsg[PROPERTYASSETSModelDetail] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | PROPERTYASSETSModelDetail | 返回对象 |

PROPERTYASSETSModelDetail 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PropertyShop | SERVERPARTSHOPModel | 服务区资产与门店关联信息 |
| BusinessProjectList | List<BUSINESSPROJECT_SimpleModel> | 经营项目相关，简易信息 |
| PROPERTYASSETS_ID | integer | 服务区资产内码 |
| PROPERTYASSETS_IDS | string | 服务区资产内码(查询条件) |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| PROPERTYASSETS_REGION | integer | 区域方位 |
| PROPERTYASSETS_TYPE | integer | 资产类型(1综合楼,子类型[1000：商铺，2000：仓库，3000：餐饮区，4000：开水间，5000：公共区，6000：厕所])小于100为父类 |
| PROPERTYASSETS_TYPES | string | 资产类型(查询条件) |
| PROPERTYASSETS_CODE | string | 物业资产编码 |
| PROPERTYASSETS_NAME | string | 物业资产名称 |
| PROPERTYASSETS_INDEX | integer | 排序 |
| PROPERTYASSETS_AREA | number | 面积大小 |
| PROPERTYASSETS_INFO | string | 说明信息 |
| PROPERTYASSETS_STATE | integer | 是否有效 |
| PROPERTYASSETS_DESC | string | 备注 |
| PROPERTYASSETS_AMOUNT | number | 金额 |
| PROPERTYASSETS_FEETYPE | integer | 费用类型 |
| EXTENDJSON | string | 扩展JSON |
| STAFF_ID | integer | 创建人ID |
| STAFF_NAME | string | 创建人 |
| CREATE_DATE | string | 创建时间 |
| OPERATOR_ID | integer | 操作人ID |
| OPERATOR_NAME | string | 操作人 |
| OPERATE_DATE | string | 操作时间 |

SERVERPARTSHOPModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTSHOP_ID | integer | 内码 |
| SHOPTRADE | string | 行业名称 |
| SHOPNAME | string | 门店名称 |
| SHOPSHORTNAME | string | 门店简称 |
| ISVALID | integer | 否有效 |
| SERVERPARTSHOP_INDEX | number | 顺序 |
| TOPPERSON | string | 最高领导人 |
| TOPPERSON_MOBILE | string | 领导人电话 |
| LINKMAN | string | 联系人 |
| LINKMAN_MOBILE | string | 联系人电话 |
| SERVERPART_ID | integer | 服务区 |
| SHOPREGION | integer | 所属区域 |
| STOREHOUSE_TYPE | integer | 合作商户平台-仓储物资模式(0：否；1：是) |
| UNIFORMMANAGE_TYPE | integer | 是否接受统一定价管理(0：否；1：是) |
| AUDIT_UPLOADSTATE | integer | 是否上传稽核数据(0：否；1：是) |
| REVENUE_UPLOADSTATE | integer | 是否上传营收数据(0：否；1：是) |
| SALECOUNT_LIMIT | integer | 销售数量上限(是否存在销售数量异常的条件) |
| SALEAMOUNT_LIMIT | integer | 销售金额上限(是否存在销售金额异常的条件) |
| SHOPCODE | string | 门店编码 |
| ROYALTYRATE | number | 提成比例 |
| BUSINESS_UNIT | string | 经营单位 |
| BUSINESS_DATE | string | 开始经营时间 |
| BUS_STARTDATE | string | 经营时间 |
| BUSINESSAREA | number | 经营面积 |
| SETTLINGACCOUNTS | integer | 结算方式 |
| SELLER_ID | integer | 商户内码 |
| BUSINESS_TYPE | integer | 经营模式(1000：自营，2000：合作经营，3000：固定租金，4000：展销) |
| BUSINESS_STATE | integer | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| BUSINESS_REGION | integer | 经营区域(1000：服务区，2000：加油站) |
| BUSINESS_NATURE | integer | 经营性质(1000：油炸，2000：非油炸) |
| STATISTIC_TYPE | integer | 统计类型(1000：正式，2000：测试，3000：替代) |
| BUSINESS_ENDDATE | string | 停业时间 |
| REGISTERCOMPACT_ID | integer | 合同内码 |
| SERVERPART_NAME | string | 服务区名称 |
| BUSINESS_BRAND | integer | 经营品牌 |
| BUSINESS_TRADE | string | 经营业态 |
| STATISTICS_TYPE | string | 统计归口(收归口、进销存归口、走动式管理（用于权限控制)) |
| STAFF_ID | number | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SERVERPARTSHOP_DESC | string | 备注说明 |
| SELLER_NAME | string | 商户名称 |
| TAXPAYER_IDENTIFYCODE | string | 商户名称 |
| BANK_NAME | string | 商户名称 |
| BANK_ACCOUNT | string | 商户名称 |
| REGISTERCOMPACT_NAME | string | 合同名称 |
| BUSINESS_TRADENAME | string | 经营业态名称 |
| BRAND_NAME | string | 经营品牌名称 |
| SERVERPART_CODE | string | 服务区编码 |
| RECORD_DISCOUNT | integer | 是否记录优惠折扣(0：不记异常稽核；1：记录异常稽核) |
| OWNERUNIT_ID | integer | 业主单位内码 |
| OWNERUNIT_NAME | string | 业主单位名称 |
| REVENUE_INCLUDE | integer | 是否纳入营收【每日营收推送中是否展示该门店的营收数据】(0：否；1：是) |
| TRANSFER_TYPE | integer | 传输类型(0：收银系统；1：扫码传输【商户通过扫固定二维码上传数据】；2：接口传输【第三方营收数据通过接口上传至综管平台】) |
| APPROVAL_TYPE | integer | 审批模式(0：商品数据无需业主审批监管；1：商品数据需业主审批监管后生效；2：商品数据先生效业主再做监管) |
| INSALES_TYPE | integer | 综管平台-进销存模式(0：否；1：是) |
| PROVINCE_CODE | integer | 省份标识 |
| SERVERPARTSHOP_IDS | string | 门店内码集合（用于查询多个门店） |
| SERVERPART_IDS | string | 服务区内码集合（用于查询多个服务区） |

BUSINESSPROJECT_SimpleModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| BUSINESSPROJECT_ID | integer | 经营项目内码 |
| BUSINESSPROJECT_NAME | string | 项目名称 |
| REGISTERCOMPACT_ID | integer | 经营合同内码 |
| COMPACT_NAME | string | 经营合同名称 |
| PROJECT_STARTDATE | string | 开始日期 |
| PROJECT_ENDDATE | string | 结束日期 |
| PROJECT_VALID | integer | 有效状态 |

---
### POST /BaseInfo/GetPROPERTYASSETSLOGList
**名称**: 67. 获取物业资产操作日志表列表
**Action**: `GetPROPERTYASSETSLOGList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
用于查看资产新增、修改、删除、资产关联门店、解除门店关联等相关操作的操作记录
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[PROPERTYASSETSLOGModel] | Y | 查询条件对象 |

SearchModel[PROPERTYASSETSLOGModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | PROPERTYASSETSLOGModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

PROPERTYASSETSLOGModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PROPERTYASSETSLOG_ID | integer | 内码 |
| TABLE_ID | integer | 操作表内码 |
| TABLE_NAME | string | 操作表名称 |
| CHANGE_TYPE | integer | 修改类型 |
| OPERATE_DATE | string | 操作时间 |
| OPERATE_DESC | string | 操作描述 |
| OPERATE_TYPE | string | 操作类型 |
| OPERATE_VALUE | string | 操作原值 |
| OPERATE_NEWVALUE | string | 操作新值 |
| OPERATE_ID | integer | 操作员ID |
| OPERATE_NAME | string | 操作人 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[PROPERTYASSETSLOGModel]]> | 返回数据集合 |

JsonMsg[JsonList[PROPERTYASSETSLOGModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[PROPERTYASSETSLOGModel] | 返回对象 |

JsonList[PROPERTYASSETSLOGModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<PROPERTYASSETSLOGModel> | 返回数据集 |

---
### POST /BaseInfo/GetPROPERTYASSETSList
**名称**: 68. 获取服务区资产表列表
**Action**: `GetPROPERTYASSETSList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区资产表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[PROPERTYASSETSModel] | Y | 查询条件对象 |

SearchModel[PROPERTYASSETSModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | PROPERTYASSETSModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

PROPERTYASSETSModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PROPERTYASSETS_ID | integer | 服务区资产内码 |
| PROPERTYASSETS_IDS | string | 服务区资产内码(查询条件) |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| PROPERTYASSETS_REGION | integer | 区域方位 |
| PROPERTYASSETS_TYPE | integer | 资产类型(1综合楼,子类型[1000：商铺，2000：仓库，3000：餐饮区，4000：开水间，5000：公共区，6000：厕所])小于100为父类 |
| PROPERTYASSETS_TYPES | string | 资产类型(查询条件) |
| PROPERTYASSETS_CODE | string | 物业资产编码 |
| PROPERTYASSETS_NAME | string | 物业资产名称 |
| PROPERTYASSETS_INDEX | integer | 排序 |
| PROPERTYASSETS_AREA | number | 面积大小 |
| PROPERTYASSETS_INFO | string | 说明信息 |
| PROPERTYASSETS_STATE | integer | 是否有效 |
| PROPERTYASSETS_DESC | string | 备注 |
| PROPERTYASSETS_AMOUNT | number | 金额 |
| PROPERTYASSETS_FEETYPE | integer | 费用类型 |
| EXTENDJSON | string | 扩展JSON |
| STAFF_ID | integer | 创建人ID |
| STAFF_NAME | string | 创建人 |
| CREATE_DATE | string | 创建时间 |
| OPERATOR_ID | integer | 操作人ID |
| OPERATOR_NAME | string | 操作人 |
| OPERATE_DATE | string | 操作时间 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[PROPERTYASSETSExtendModel]]> | 返回数据集合 |

JsonMsg[JsonList[PROPERTYASSETSExtendModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[PROPERTYASSETSExtendModel] | 返回对象 |

JsonList[PROPERTYASSETSExtendModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<PROPERTYASSETSExtendModel> | 返回数据集 |

PROPERTYASSETSExtendModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SPREGIONTYPE_ID | integer | 归属区域内码 |
| SPREGIONTYPE_NAME | string | 归属区域名字 |
| SPREGIONTYPE_INDEX | integer | 归属区域索引 |
| SERVERPARTSHOP_ID | string | 内码 |
| SHOPNAME | string | 门店名称 |
| BUSINESS_STATE | integer | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| ShopList | List<ServerPartShopStateExtendModel> | 资产对应的门店列表 |
| TOTAL_AREA | number | 总面积 |
| BUSINESSPROJECT_ID | integer | 经营项目内码 |
| BUSINESSPROJECT_NAME | string | 项目名称 |
| REGISTERCOMPACT_ID | integer | 经营合同内码 |
| COMPACT_NAME | string | 经营合同名称 |
| PROJECT_STARTDATE | string | 开始日期 |
| PROJECT_ENDDATE | string | 结束日期 |
| PROJECT_VALID | integer | 有效状态 |
| PROPERTYASSETS_ID | integer | 服务区资产内码 |
| PROPERTYASSETS_IDS | string | 服务区资产内码(查询条件) |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| PROPERTYASSETS_REGION | integer | 区域方位 |
| PROPERTYASSETS_TYPE | integer | 资产类型(1综合楼,子类型[1000：商铺，2000：仓库，3000：餐饮区，4000：开水间，5000：公共区，6000：厕所])小于100为父类 |
| PROPERTYASSETS_TYPES | string | 资产类型(查询条件) |
| PROPERTYASSETS_CODE | string | 物业资产编码 |
| PROPERTYASSETS_NAME | string | 物业资产名称 |
| PROPERTYASSETS_INDEX | integer | 排序 |
| PROPERTYASSETS_AREA | number | 面积大小 |
| PROPERTYASSETS_INFO | string | 说明信息 |
| PROPERTYASSETS_STATE | integer | 是否有效 |
| PROPERTYASSETS_DESC | string | 备注 |
| PROPERTYASSETS_AMOUNT | number | 金额 |
| PROPERTYASSETS_FEETYPE | integer | 费用类型 |
| EXTENDJSON | string | 扩展JSON |
| STAFF_ID | integer | 创建人ID |
| STAFF_NAME | string | 创建人 |
| CREATE_DATE | string | 创建时间 |
| OPERATOR_ID | integer | 操作人ID |
| OPERATOR_NAME | string | 操作人 |
| OPERATE_DATE | string | 操作时间 |

ServerPartShopStateExtendModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTSHOP_ID | integer | 内码 |
| SHOPNAME | string | 门店名称 |
| BUSINESS_STATE | integer | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| BUSINESS_DATE | string | 开始经营时间 |
| BUSINESS_ENDDATE | string | 停业时间 |

---
### POST /BaseInfo/GetPROPERTYASSETSTreeList
**名称**: 69. 获取服务区资产-树形分组列表
**Action**: `GetPROPERTYASSETSTreeList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
1. 根据资产列表数据组建树形数据列表，父节点汇总计算，汇总节点分为区域中心、服务区、服务区方位2. 返回数据包含未匹配资产门店信息，未匹配门店，资产编码为空。
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[PROPERTYASSETSModel] | Y | 查询条件对象 |

SearchModel[PROPERTYASSETSModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | PROPERTYASSETSModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

PROPERTYASSETSModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PROPERTYASSETS_ID | integer | 服务区资产内码 |
| PROPERTYASSETS_IDS | string | 服务区资产内码(查询条件) |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| PROPERTYASSETS_REGION | integer | 区域方位 |
| PROPERTYASSETS_TYPE | integer | 资产类型(1综合楼,子类型[1000：商铺，2000：仓库，3000：餐饮区，4000：开水间，5000：公共区，6000：厕所])小于100为父类 |
| PROPERTYASSETS_TYPES | string | 资产类型(查询条件) |
| PROPERTYASSETS_CODE | string | 物业资产编码 |
| PROPERTYASSETS_NAME | string | 物业资产名称 |
| PROPERTYASSETS_INDEX | integer | 排序 |
| PROPERTYASSETS_AREA | number | 面积大小 |
| PROPERTYASSETS_INFO | string | 说明信息 |
| PROPERTYASSETS_STATE | integer | 是否有效 |
| PROPERTYASSETS_DESC | string | 备注 |
| PROPERTYASSETS_AMOUNT | number | 金额 |
| PROPERTYASSETS_FEETYPE | integer | 费用类型 |
| EXTENDJSON | string | 扩展JSON |
| STAFF_ID | integer | 创建人ID |
| STAFF_NAME | string | 创建人 |
| CREATE_DATE | string | 创建时间 |
| OPERATOR_ID | integer | 操作人ID |
| OPERATOR_NAME | string | 操作人 |
| OPERATE_DATE | string | 操作时间 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[PROPERTYASSETSExtendModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[PROPERTYASSETSExtendModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[PROPERTYASSETSExtendModel]] | 返回对象 |

JsonList[NestingModel[PROPERTYASSETSExtendModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[PROPERTYASSETSExtendModel]> | 返回数据集 |

NestingModel[PROPERTYASSETSExtendModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | PROPERTYASSETSExtendModel | 结点 |
| children | List<NestingModel[PROPERTYASSETSExtendModel]> | 子级 |

PROPERTYASSETSExtendModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SPREGIONTYPE_ID | integer | 归属区域内码 |
| SPREGIONTYPE_NAME | string | 归属区域名字 |
| SPREGIONTYPE_INDEX | integer | 归属区域索引 |
| SERVERPARTSHOP_ID | string | 内码 |
| SHOPNAME | string | 门店名称 |
| BUSINESS_STATE | integer | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| ShopList | List<ServerPartShopStateExtendModel> | 资产对应的门店列表 |
| TOTAL_AREA | number | 总面积 |
| BUSINESSPROJECT_ID | integer | 经营项目内码 |
| BUSINESSPROJECT_NAME | string | 项目名称 |
| REGISTERCOMPACT_ID | integer | 经营合同内码 |
| COMPACT_NAME | string | 经营合同名称 |
| PROJECT_STARTDATE | string | 开始日期 |
| PROJECT_ENDDATE | string | 结束日期 |
| PROJECT_VALID | integer | 有效状态 |
| PROPERTYASSETS_ID | integer | 服务区资产内码 |
| PROPERTYASSETS_IDS | string | 服务区资产内码(查询条件) |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| PROPERTYASSETS_REGION | integer | 区域方位 |
| PROPERTYASSETS_TYPE | integer | 资产类型(1综合楼,子类型[1000：商铺，2000：仓库，3000：餐饮区，4000：开水间，5000：公共区，6000：厕所])小于100为父类 |
| PROPERTYASSETS_TYPES | string | 资产类型(查询条件) |
| PROPERTYASSETS_CODE | string | 物业资产编码 |
| PROPERTYASSETS_NAME | string | 物业资产名称 |
| PROPERTYASSETS_INDEX | integer | 排序 |
| PROPERTYASSETS_AREA | number | 面积大小 |
| PROPERTYASSETS_INFO | string | 说明信息 |
| PROPERTYASSETS_STATE | integer | 是否有效 |
| PROPERTYASSETS_DESC | string | 备注 |
| PROPERTYASSETS_AMOUNT | number | 金额 |
| PROPERTYASSETS_FEETYPE | integer | 费用类型 |
| EXTENDJSON | string | 扩展JSON |
| STAFF_ID | integer | 创建人ID |
| STAFF_NAME | string | 创建人 |
| CREATE_DATE | string | 创建时间 |
| OPERATOR_ID | integer | 操作人ID |
| OPERATOR_NAME | string | 操作人 |
| OPERATE_DATE | string | 操作时间 |

ServerPartShopStateExtendModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTSHOP_ID | integer | 内码 |
| SHOPNAME | string | 门店名称 |
| BUSINESS_STATE | integer | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| BUSINESS_DATE | string | 开始经营时间 |
| BUSINESS_ENDDATE | string | 停业时间 |

---
### GET /BaseInfo/GetPROPERTYSHOPDetail
**名称**: 70. 获取物业资产与商户对照表明细
**Action**: `GetPROPERTYSHOPDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取物业资产与商户对照表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PROPERTYSHOPId | integer | Y | 物业资产与商户对照表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[PROPERTYSHOPModelDetail]> | 返回数据集合 |

JsonMsg[PROPERTYSHOPModelDetail] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | PROPERTYSHOPModelDetail | 返回对象 |

PROPERTYSHOPModelDetail 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ServerpartShop | SERVERPARTSHOPModel | 服务区门店信息 |
| PROPERTYSHOP_ID | integer | 内码 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| PROPERTYASSETS_ID | integer | 物业资产内码 |
| PROPERTYASSETS_IDS | string | 物业资产内码(查询条件) |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| SERVERPARTSHOP_IDS | string | 门店内码(查询条件) |
| STARTDATE | string | 开始时间 |
| STARTDATE_Start | string | 开始时间(查询条件) |
| STARTDATE_End | string | 开始时间(查询条件) |
| ENDDATE | string | 结束时间 |
| ENDDATE_Start | string | 结束时间(查询条件) |
| ENDDATE_End | string | 结束时间(查询条件) |
| PROPERTYSHOP_STATE | integer | 是否有效 |
| STAFF_ID | integer | 创建人ID |
| STAFF_NAME | string | 创建人 |
| CREATE_DATE | string | 创建时间 |
| OPERATOR_ID | integer | 操作人ID |
| OPERATOR_NAME | string | 操作人 |
| OPERATE_DATE | string | 操作时间 |
| PROPERTYSHOP_DESC | string | 备注 |
| EXTENDJSON | string | 扩展JSON |

SERVERPARTSHOPModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTSHOP_ID | integer | 内码 |
| SHOPTRADE | string | 行业名称 |
| SHOPNAME | string | 门店名称 |
| SHOPSHORTNAME | string | 门店简称 |
| ISVALID | integer | 否有效 |
| SERVERPARTSHOP_INDEX | number | 顺序 |
| TOPPERSON | string | 最高领导人 |
| TOPPERSON_MOBILE | string | 领导人电话 |
| LINKMAN | string | 联系人 |
| LINKMAN_MOBILE | string | 联系人电话 |
| SERVERPART_ID | integer | 服务区 |
| SHOPREGION | integer | 所属区域 |
| STOREHOUSE_TYPE | integer | 合作商户平台-仓储物资模式(0：否；1：是) |
| UNIFORMMANAGE_TYPE | integer | 是否接受统一定价管理(0：否；1：是) |
| AUDIT_UPLOADSTATE | integer | 是否上传稽核数据(0：否；1：是) |
| REVENUE_UPLOADSTATE | integer | 是否上传营收数据(0：否；1：是) |
| SALECOUNT_LIMIT | integer | 销售数量上限(是否存在销售数量异常的条件) |
| SALEAMOUNT_LIMIT | integer | 销售金额上限(是否存在销售金额异常的条件) |
| SHOPCODE | string | 门店编码 |
| ROYALTYRATE | number | 提成比例 |
| BUSINESS_UNIT | string | 经营单位 |
| BUSINESS_DATE | string | 开始经营时间 |
| BUS_STARTDATE | string | 经营时间 |
| BUSINESSAREA | number | 经营面积 |
| SETTLINGACCOUNTS | integer | 结算方式 |
| SELLER_ID | integer | 商户内码 |
| BUSINESS_TYPE | integer | 经营模式(1000：自营，2000：合作经营，3000：固定租金，4000：展销) |
| BUSINESS_STATE | integer | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| BUSINESS_REGION | integer | 经营区域(1000：服务区，2000：加油站) |
| BUSINESS_NATURE | integer | 经营性质(1000：油炸，2000：非油炸) |
| STATISTIC_TYPE | integer | 统计类型(1000：正式，2000：测试，3000：替代) |
| BUSINESS_ENDDATE | string | 停业时间 |
| REGISTERCOMPACT_ID | integer | 合同内码 |
| SERVERPART_NAME | string | 服务区名称 |
| BUSINESS_BRAND | integer | 经营品牌 |
| BUSINESS_TRADE | string | 经营业态 |
| STATISTICS_TYPE | string | 统计归口(收归口、进销存归口、走动式管理（用于权限控制)) |
| STAFF_ID | number | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SERVERPARTSHOP_DESC | string | 备注说明 |
| SELLER_NAME | string | 商户名称 |
| TAXPAYER_IDENTIFYCODE | string | 商户名称 |
| BANK_NAME | string | 商户名称 |
| BANK_ACCOUNT | string | 商户名称 |
| REGISTERCOMPACT_NAME | string | 合同名称 |
| BUSINESS_TRADENAME | string | 经营业态名称 |
| BRAND_NAME | string | 经营品牌名称 |
| SERVERPART_CODE | string | 服务区编码 |
| RECORD_DISCOUNT | integer | 是否记录优惠折扣(0：不记异常稽核；1：记录异常稽核) |
| OWNERUNIT_ID | integer | 业主单位内码 |
| OWNERUNIT_NAME | string | 业主单位名称 |
| REVENUE_INCLUDE | integer | 是否纳入营收【每日营收推送中是否展示该门店的营收数据】(0：否；1：是) |
| TRANSFER_TYPE | integer | 传输类型(0：收银系统；1：扫码传输【商户通过扫固定二维码上传数据】；2：接口传输【第三方营收数据通过接口上传至综管平台】) |
| APPROVAL_TYPE | integer | 审批模式(0：商品数据无需业主审批监管；1：商品数据需业主审批监管后生效；2：商品数据先生效业主再做监管) |
| INSALES_TYPE | integer | 综管平台-进销存模式(0：否；1：是) |
| PROVINCE_CODE | integer | 省份标识 |
| SERVERPARTSHOP_IDS | string | 门店内码集合（用于查询多个门店） |
| SERVERPART_IDS | string | 服务区内码集合（用于查询多个服务区） |

---
### POST /BaseInfo/GetPROPERTYSHOPList
**名称**: 71. 获取物业资产与商户对照表列表
**Action**: `GetPROPERTYSHOPList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取物业资产与商户对照表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[PROPERTYSHOPModel] | Y | 查询条件对象 |

SearchModel[PROPERTYSHOPModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | PROPERTYSHOPModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

PROPERTYSHOPModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PROPERTYSHOP_ID | integer | 内码 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| PROPERTYASSETS_ID | integer | 物业资产内码 |
| PROPERTYASSETS_IDS | string | 物业资产内码(查询条件) |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| SERVERPARTSHOP_IDS | string | 门店内码(查询条件) |
| STARTDATE | string | 开始时间 |
| STARTDATE_Start | string | 开始时间(查询条件) |
| STARTDATE_End | string | 开始时间(查询条件) |
| ENDDATE | string | 结束时间 |
| ENDDATE_Start | string | 结束时间(查询条件) |
| ENDDATE_End | string | 结束时间(查询条件) |
| PROPERTYSHOP_STATE | integer | 是否有效 |
| STAFF_ID | integer | 创建人ID |
| STAFF_NAME | string | 创建人 |
| CREATE_DATE | string | 创建时间 |
| OPERATOR_ID | integer | 操作人ID |
| OPERATOR_NAME | string | 操作人 |
| OPERATE_DATE | string | 操作时间 |
| PROPERTYSHOP_DESC | string | 备注 |
| EXTENDJSON | string | 扩展JSON |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[PROPERTYSHOPModel]]> | 返回数据集合 |

JsonMsg[JsonList[PROPERTYSHOPModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[PROPERTYSHOPModel] | 返回对象 |

JsonList[PROPERTYSHOPModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<PROPERTYSHOPModel> | 返回数据集 |

---
### GET /BaseInfo/GetRTSERVERPARTSHOPDetail
**名称**: 72. 获取门店经营时间表明细
**Action**: `GetRTSERVERPARTSHOPDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取门店经营时间表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| RTSERVERPARTSHOPId | integer | Y | 门店经营时间表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[RTSERVERPARTSHOPModel]> | 返回数据集合 |

JsonMsg[RTSERVERPARTSHOPModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | RTSERVERPARTSHOPModel | 返回对象 |

RTSERVERPARTSHOPModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| RTSERVERPARTSHOP_ID | integer | 内码 |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| SERVERPARTSHOP_IDS | string | 门店内码(查询条件) |
| SHOPNAME | string | 门店名称 |
| SELLER_ID | integer | 商户内码 |
| BUSINESS_UNIT | string | 经营单位 |
| ROYALTYRATE | number | 提成比例 |
| BUSINESS_DATE | string | 开业时间 |
| BUSINESS_ENDDATE | string | 停业时间 |
| BUS_STARTDATE | string | 经营时段 |
| BUSINESSAREA | number | 经营面积 |
| BUSINESS_TYPE | integer | 经营模式 |
| BUSINESS_TYPES | string | 经营模式(查询条件) |
| BUSINESS_REGION | integer | 经营区域 |
| BUSINESS_NATURE | integer | 经营性质 |
| TOPPERSON | string | 门店负责人 |
| TOPPERSON_MOBILE | string | 负责人电话 |
| LINKMAN | string | 门店联系人 |
| LINKMAN_MOBILE | string | 联系人电话 |
| REGISTERCOMPACT_ID | integer | 合同内码 |
| REGISTERCOMPACT_NAME | string | 合同名称 |
| STAFF_ID | integer | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| RTSERVERPARTSHOP_DESC | string | 备注说明 |

---
### POST /BaseInfo/GetRTSERVERPARTSHOPList
**名称**: 73. 获取门店经营时间表列表
**Action**: `GetRTSERVERPARTSHOPList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取门店经营时间表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[RTSERVERPARTSHOPModel] | Y | 查询条件对象 |

SearchModel[RTSERVERPARTSHOPModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | RTSERVERPARTSHOPModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

RTSERVERPARTSHOPModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| RTSERVERPARTSHOP_ID | integer | 内码 |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| SERVERPARTSHOP_IDS | string | 门店内码(查询条件) |
| SHOPNAME | string | 门店名称 |
| SELLER_ID | integer | 商户内码 |
| BUSINESS_UNIT | string | 经营单位 |
| ROYALTYRATE | number | 提成比例 |
| BUSINESS_DATE | string | 开业时间 |
| BUSINESS_ENDDATE | string | 停业时间 |
| BUS_STARTDATE | string | 经营时段 |
| BUSINESSAREA | number | 经营面积 |
| BUSINESS_TYPE | integer | 经营模式 |
| BUSINESS_TYPES | string | 经营模式(查询条件) |
| BUSINESS_REGION | integer | 经营区域 |
| BUSINESS_NATURE | integer | 经营性质 |
| TOPPERSON | string | 门店负责人 |
| TOPPERSON_MOBILE | string | 负责人电话 |
| LINKMAN | string | 门店联系人 |
| LINKMAN_MOBILE | string | 联系人电话 |
| REGISTERCOMPACT_ID | integer | 合同内码 |
| REGISTERCOMPACT_NAME | string | 合同名称 |
| STAFF_ID | integer | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| RTSERVERPARTSHOP_DESC | string | 备注说明 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[RTSERVERPARTSHOPModel]]> | 返回数据集合 |

JsonMsg[JsonList[RTSERVERPARTSHOPModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[RTSERVERPARTSHOPModel] | 返回对象 |

JsonList[RTSERVERPARTSHOPModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<RTSERVERPARTSHOPModel> | 返回数据集 |

---
### GET /BaseInfo/GetSERVERPARTCRTDetail
**名称**: 74. 获取服务区成本核算对照表明细
**Action**: `GetSERVERPARTCRTDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区成本核算对照表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SERVERPARTCRTId | integer | N | 服务区成本核算对照表内码 |
| SERVERPARTTId | integer | N | 服务区内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[SERVERPARTCRTModel]> | 返回数据集合 |

JsonMsg[SERVERPARTCRTModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | SERVERPARTCRTModel | 返回对象 |

SERVERPARTCRTModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTCRT_ID | integer | 内码 |
| ACCOUNTBODY_CODE | string | 核算主体编码 |
| ACCOUNTBODY_NAME | string | 核算主体名称 |
| DEPARTMENT_CODE | string | 核算部门编码 |
| COSTCENTER_CODE | string | 成本中心编码 |
| COSTCENTER_NAME | string | 成本中心名称 |
| SERVERPART_CODE | string | 服务区编码 |
| SERVERPART_CODES | string | 服务区编码(查询条件) |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| RESPONSIBLEDEP_CODE | string | 责任部门编码 |
| STAYTAX | number | 住宿费税率 |
| PROPERTYTAX | number | 物业费税率 |
| ACCOUNTTAX | number | 到账税率 |
| STAFF_ID | integer | 操作人ID |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SPREGIONTYPE_INDEX | integer | 区域序号 |
| SERVERPART_INDEX | integer | 区域序号 |
| SPREGIONTYPE_ID | integer | 片区内码 |
| SPREGIONTYPE_NAME | string | 片区名称 |
| SERVERPART_NAME | string | 服务区名称 |

---
### POST /BaseInfo/GetSERVERPARTCRTList
**名称**: 75. 获取服务区成本核算对照表列表
**Action**: `GetSERVERPARTCRTList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区成本核算对照表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[SERVERPARTCRTModel] | Y | 查询条件对象 |

SearchModel[SERVERPARTCRTModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | SERVERPARTCRTModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

SERVERPARTCRTModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTCRT_ID | integer | 内码 |
| ACCOUNTBODY_CODE | string | 核算主体编码 |
| ACCOUNTBODY_NAME | string | 核算主体名称 |
| DEPARTMENT_CODE | string | 核算部门编码 |
| COSTCENTER_CODE | string | 成本中心编码 |
| COSTCENTER_NAME | string | 成本中心名称 |
| SERVERPART_CODE | string | 服务区编码 |
| SERVERPART_CODES | string | 服务区编码(查询条件) |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| RESPONSIBLEDEP_CODE | string | 责任部门编码 |
| STAYTAX | number | 住宿费税率 |
| PROPERTYTAX | number | 物业费税率 |
| ACCOUNTTAX | number | 到账税率 |
| STAFF_ID | integer | 操作人ID |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SPREGIONTYPE_INDEX | integer | 区域序号 |
| SERVERPART_INDEX | integer | 区域序号 |
| SPREGIONTYPE_ID | integer | 片区内码 |
| SPREGIONTYPE_NAME | string | 片区名称 |
| SERVERPART_NAME | string | 服务区名称 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[SERVERPARTCRTModel]]> | 返回数据集合 |

JsonMsg[JsonList[SERVERPARTCRTModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[SERVERPARTCRTModel] | 返回对象 |

JsonList[SERVERPARTCRTModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<SERVERPARTCRTModel> | 返回数据集 |

---
### POST /BaseInfo/GetSERVERPARTCRTTreeList
**名称**: 76. 获取服务区成本核算对照表--树形列表
**Action**: `GetSERVERPARTCRTTreeList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区成本核算对照表--树形列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[SERVERPARTCRTModel] | Y | 查询条件对象 |

SearchModel[SERVERPARTCRTModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | SERVERPARTCRTModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

SERVERPARTCRTModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTCRT_ID | integer | 内码 |
| ACCOUNTBODY_CODE | string | 核算主体编码 |
| ACCOUNTBODY_NAME | string | 核算主体名称 |
| DEPARTMENT_CODE | string | 核算部门编码 |
| COSTCENTER_CODE | string | 成本中心编码 |
| COSTCENTER_NAME | string | 成本中心名称 |
| SERVERPART_CODE | string | 服务区编码 |
| SERVERPART_CODES | string | 服务区编码(查询条件) |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| RESPONSIBLEDEP_CODE | string | 责任部门编码 |
| STAYTAX | number | 住宿费税率 |
| PROPERTYTAX | number | 物业费税率 |
| ACCOUNTTAX | number | 到账税率 |
| STAFF_ID | integer | 操作人ID |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SPREGIONTYPE_INDEX | integer | 区域序号 |
| SERVERPART_INDEX | integer | 区域序号 |
| SPREGIONTYPE_ID | integer | 片区内码 |
| SPREGIONTYPE_NAME | string | 片区名称 |
| SERVERPART_NAME | string | 服务区名称 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[SERVERPARTCRTModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[SERVERPARTCRTModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[SERVERPARTCRTModel]] | 返回对象 |

JsonList[NestingModel[SERVERPARTCRTModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[SERVERPARTCRTModel]> | 返回数据集 |

NestingModel[SERVERPARTCRTModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | SERVERPARTCRTModel | 结点 |
| children | List<NestingModel[SERVERPARTCRTModel]> | 子级 |

---
### GET /BaseInfo/GetSERVERPARTDetail
**名称**: 77. 获取服务区详情
**Action**: `GetSERVERPARTDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区详情
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SERVERPARTId | integer | N | 服务区站点内码 |
| FieldEnumId | integer | N | 服务区枚举内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[SERVERPARTModel]> | 返回数据集合 |

JsonMsg[SERVERPARTModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | SERVERPARTModel | 返回对象 |

SERVERPARTModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPART_ID | integer | 内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| SERVERPART_NAME | string | 服务区名称 |
| SERVERPART_ADDRESS | string | 服务区地址 |
| SERVERPART_INDEX | integer | 服务区索引 |
| EXPRESSWAY_NAME | string | 服务区所在高速路 |
| SELLERCOUNT | integer | 商家服务数 |
| SERVERPART_AREA | number | 服务区面积 |
| SERVERPART_X | number | 服务区坐标X |
| SERVERPART_Y | number | 服务区坐标Y |
| SERVERPART_TEL | string | 服务区电话号码 |
| SERVERPART_INFO | string | 服务区说明 |
| PROVINCE_CODE | integer | 省份编码 |
| CITY_CODE | integer | 城市编码 |
| COUNTY_CODE | integer | 区县编码 |
| SERVERPART_CODE | string | 服务区编码 |
| SERVERPART_CODES | string | 服务区编码(查询条件) |
| FIELDENUM_ID | integer | 枚举内码 |
| SERVERPART_IPADDRESS | string | 服务区IP地址描述 |
| SERVERPART_TYPE | integer | 服务区类型 |
| DAYINCAR | number | 日均入区车辆 |
| HKBL | string | 入区车辆客货比例 |
| STARTDATE | string | 开业时间 |
| OWNEDCOMPANY | string | 所属公司 |
| FLOORAREA | number | 占地面积 |
| BUSINESSAREA | number | 经营面积 |
| SHAREAREA | number | 公共区域面积 |
| TOTALPARKING | integer | 车位数 |
| MANAGERCOMPANY | string | 管理公司 |
| SHORTNAME | string | 服务区简称 |
| REGIONTYPE_ID | integer | 附属管辖内码 |
| STATISTIC_TYPE | integer | 统计类型(1000：正式，2000：测试，3000：替代) |
| PROVINCE_NAME | string | 省份名称 |
| SPREGIONTYPE_ID | integer | 归属区域内码 |
| SPREGIONTYPE_NAME | string | 归属区域名字 |
| SPREGIONTYPE_INDEX | integer | 归属区域索引 |
| REGIONTYPE_NAME | string | 附属管辖名称 |
| STATISTICS_TYPE | string | 站点类型(服务区、加油站、单位部门) |
| STAFF_ID | integer | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SERVERPART_DESC | string | 备注说明 |
| OWNERUNIT_ID | integer | 业主单位内码 |
| OWNERUNIT_NAME | string | 业主单位名称 |
| RtServerPart | RTSERVERPARTModel | 服务区附属信息 |
| ServerPartInfo | List<SERVERPARTINFOModel> | 服务区详情 |

RTSERVERPARTModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| RTSERVERPART_ID | integer | 内码 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_ADDRESS | string | 服务区地址 |
| EXPRESSWAY_NAME | string | 服务区所在高速路 |
| SELLERCOUNT | integer | 商家服务数 |
| SERVERPART_X | number | 服务区坐标X |
| SERVERPART_Y | number | 服务区坐标Y |
| SERVERPART_TEL | string | 联系电话 |
| STARTDATE | string | 开业时间 |
| SERVERPART_AREA | number | 服务区面积 |
| FLOORAREA | number | 占地面积 |
| BUSINESSAREA | number | 经营面积 |
| SHAREAREA | number | 公共区域面积 |
| TOTALPARKING | integer | 车位数量 |
| OWNEDCOMPANY | string | 所属公司 |
| MANAGERCOMPANY | string | 管理公司 |
| STAFF_ID | integer | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SERVERPART_INFO | string | 备注说明 |
| CENTERSTAKE_NUM | string | 中心桩号 |
| TAXPAYER_IDENTIFYCODE | string | 统一信用代码 |
| WATERINTAKE_TYPE | integer | 取水形式（1：自来水；2：井水） |
| SEWAGEDISPOSAL_TYPE | integer | 污水处理形式（1：市政；2：污水处理设备） |
| BUSINESS_REGION | integer | 分区形式（1000：服务区双侧；1010：服务区单侧；2000：加油站双侧；2010：加油站单侧） |
| SERVERPART_TARGET | string | 服务区标签（参照枚举SERVERPART_TARGET） |

SERVERPARTINFOModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTINFO_ID | integer | 内码 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| SMALLPARKING | integer | 小客车位 |
| PACKING | integer | 客车位 |
| TRUCKPACKING | integer | 货车位 |
| LONGPACKING | integer | 超长车位 |
| DANPACKING | integer | 危化品车位 |
| LIVESTOCKPACKING | integer | 禽畜车位（充电桩数） |
| TOILETCOUNT | integer | 厕位数 |
| BUSINESSTYPE | string | 业态布局 |
| DININGROOMCOUNT | integer | 餐厅餐位 |
| DININGBXCOUNT | integer | 餐厅包厢数 |
| HASMOTHER | integer | 母婴室是否有 |
| HASCHILD | integer | 儿童游乐场是否有 |
| HASSHOWERROOM | integer | 淋浴房 |
| HASTHIRDTOILETS | integer | 第三卫生间是否 |
| HASWATERROOM | integer | 开水间是否有 |
| HASPILOTLOUNGE | integer | 驾驶员休息室 |
| GREENSPACEAREA | number | 绿化面积 |
| POINTCONTROLCOUNT | integer | 监控点位位数 |
| HASBACKGROUNDRADIO | integer | 有没有背景广播 |
| HASWIFI | integer | Wifi是否有 |
| HASMESSAGESEARCH | integer | 信息查询屏 |
| HASPANTRY | integer | 冷菜间 |
| SCENICAREA | string | 周边景点 |
| SERVERPART_REGION | integer | 服务区方位 |
| MICROWAVEOVEN | integer | 微波炉数量 |
| WASHERCOUNT | integer | 洗衣机数量 |
| SLEEPINGPODS | integer | 睡眠舱数量 |
| REFUELINGGUN92 | integer | 加油枪92号 |
| REFUELINGGUN95 | integer | 加油枪95号 |
| REFUELINGGUN0 | integer | 加油枪0号 |
| STATEGRIDCHARGE | integer | 国网充电桩数量 |
| LIAUTOCHARGE | integer | 理想5C充电桩数量 |
| GACENERGYCHARGE | integer | 广汽能源充电桩数量 |
| OTHERCHARGE | integer | 其他充电桩数量 |
| FLOORAREA | integer | 占地面积 |
| PARKINGAREA | integer | 停车场面积 |
| BUILDINGAREA | integer | 建筑面积 |
| VEHICLEWATERFILLING | integer | 是否具有车辆加水 |

---
### POST /BaseInfo/GetSERVERPARTList
**名称**: 78. 获取服务区站点列表
**Action**: `GetSERVERPARTList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区站点列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[SERVERPARTModel] | Y | 查询条件对象 |

SearchModel[SERVERPARTModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | SERVERPARTModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

SERVERPARTModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPART_ID | integer | 内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| SERVERPART_NAME | string | 服务区名称 |
| SERVERPART_ADDRESS | string | 服务区地址 |
| SERVERPART_INDEX | integer | 服务区索引 |
| EXPRESSWAY_NAME | string | 服务区所在高速路 |
| SELLERCOUNT | integer | 商家服务数 |
| SERVERPART_AREA | number | 服务区面积 |
| SERVERPART_X | number | 服务区坐标X |
| SERVERPART_Y | number | 服务区坐标Y |
| SERVERPART_TEL | string | 服务区电话号码 |
| SERVERPART_INFO | string | 服务区说明 |
| PROVINCE_CODE | integer | 省份编码 |
| CITY_CODE | integer | 城市编码 |
| COUNTY_CODE | integer | 区县编码 |
| SERVERPART_CODE | string | 服务区编码 |
| SERVERPART_CODES | string | 服务区编码(查询条件) |
| FIELDENUM_ID | integer | 枚举内码 |
| SERVERPART_IPADDRESS | string | 服务区IP地址描述 |
| SERVERPART_TYPE | integer | 服务区类型 |
| DAYINCAR | number | 日均入区车辆 |
| HKBL | string | 入区车辆客货比例 |
| STARTDATE | string | 开业时间 |
| OWNEDCOMPANY | string | 所属公司 |
| FLOORAREA | number | 占地面积 |
| BUSINESSAREA | number | 经营面积 |
| SHAREAREA | number | 公共区域面积 |
| TOTALPARKING | integer | 车位数 |
| MANAGERCOMPANY | string | 管理公司 |
| SHORTNAME | string | 服务区简称 |
| REGIONTYPE_ID | integer | 附属管辖内码 |
| STATISTIC_TYPE | integer | 统计类型(1000：正式，2000：测试，3000：替代) |
| PROVINCE_NAME | string | 省份名称 |
| SPREGIONTYPE_ID | integer | 归属区域内码 |
| SPREGIONTYPE_NAME | string | 归属区域名字 |
| SPREGIONTYPE_INDEX | integer | 归属区域索引 |
| REGIONTYPE_NAME | string | 附属管辖名称 |
| STATISTICS_TYPE | string | 站点类型(服务区、加油站、单位部门) |
| STAFF_ID | integer | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SERVERPART_DESC | string | 备注说明 |
| OWNERUNIT_ID | integer | 业主单位内码 |
| OWNERUNIT_NAME | string | 业主单位名称 |
| RtServerPart | RTSERVERPARTModel | 服务区附属信息 |
| ServerPartInfo | List<SERVERPARTINFOModel> | 服务区详情 |

RTSERVERPARTModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| RTSERVERPART_ID | integer | 内码 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_ADDRESS | string | 服务区地址 |
| EXPRESSWAY_NAME | string | 服务区所在高速路 |
| SELLERCOUNT | integer | 商家服务数 |
| SERVERPART_X | number | 服务区坐标X |
| SERVERPART_Y | number | 服务区坐标Y |
| SERVERPART_TEL | string | 联系电话 |
| STARTDATE | string | 开业时间 |
| SERVERPART_AREA | number | 服务区面积 |
| FLOORAREA | number | 占地面积 |
| BUSINESSAREA | number | 经营面积 |
| SHAREAREA | number | 公共区域面积 |
| TOTALPARKING | integer | 车位数量 |
| OWNEDCOMPANY | string | 所属公司 |
| MANAGERCOMPANY | string | 管理公司 |
| STAFF_ID | integer | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SERVERPART_INFO | string | 备注说明 |
| CENTERSTAKE_NUM | string | 中心桩号 |
| TAXPAYER_IDENTIFYCODE | string | 统一信用代码 |
| WATERINTAKE_TYPE | integer | 取水形式（1：自来水；2：井水） |
| SEWAGEDISPOSAL_TYPE | integer | 污水处理形式（1：市政；2：污水处理设备） |
| BUSINESS_REGION | integer | 分区形式（1000：服务区双侧；1010：服务区单侧；2000：加油站双侧；2010：加油站单侧） |
| SERVERPART_TARGET | string | 服务区标签（参照枚举SERVERPART_TARGET） |

SERVERPARTINFOModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTINFO_ID | integer | 内码 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| SMALLPARKING | integer | 小客车位 |
| PACKING | integer | 客车位 |
| TRUCKPACKING | integer | 货车位 |
| LONGPACKING | integer | 超长车位 |
| DANPACKING | integer | 危化品车位 |
| LIVESTOCKPACKING | integer | 禽畜车位（充电桩数） |
| TOILETCOUNT | integer | 厕位数 |
| BUSINESSTYPE | string | 业态布局 |
| DININGROOMCOUNT | integer | 餐厅餐位 |
| DININGBXCOUNT | integer | 餐厅包厢数 |
| HASMOTHER | integer | 母婴室是否有 |
| HASCHILD | integer | 儿童游乐场是否有 |
| HASSHOWERROOM | integer | 淋浴房 |
| HASTHIRDTOILETS | integer | 第三卫生间是否 |
| HASWATERROOM | integer | 开水间是否有 |
| HASPILOTLOUNGE | integer | 驾驶员休息室 |
| GREENSPACEAREA | number | 绿化面积 |
| POINTCONTROLCOUNT | integer | 监控点位位数 |
| HASBACKGROUNDRADIO | integer | 有没有背景广播 |
| HASWIFI | integer | Wifi是否有 |
| HASMESSAGESEARCH | integer | 信息查询屏 |
| HASPANTRY | integer | 冷菜间 |
| SCENICAREA | string | 周边景点 |
| SERVERPART_REGION | integer | 服务区方位 |
| MICROWAVEOVEN | integer | 微波炉数量 |
| WASHERCOUNT | integer | 洗衣机数量 |
| SLEEPINGPODS | integer | 睡眠舱数量 |
| REFUELINGGUN92 | integer | 加油枪92号 |
| REFUELINGGUN95 | integer | 加油枪95号 |
| REFUELINGGUN0 | integer | 加油枪0号 |
| STATEGRIDCHARGE | integer | 国网充电桩数量 |
| LIAUTOCHARGE | integer | 理想5C充电桩数量 |
| GACENERGYCHARGE | integer | 广汽能源充电桩数量 |
| OTHERCHARGE | integer | 其他充电桩数量 |
| FLOORAREA | integer | 占地面积 |
| PARKINGAREA | integer | 停车场面积 |
| BUILDINGAREA | integer | 建筑面积 |
| VEHICLEWATERFILLING | integer | 是否具有车辆加水 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[SERVERPARTModel]]> | 返回数据集合 |

JsonMsg[JsonList[SERVERPARTModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[SERVERPARTModel] | 返回对象 |

JsonList[SERVERPARTModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<SERVERPARTModel> | 返回数据集 |

---
### POST /BaseInfo/GetSERVERPARTSHOP_LOGList
**名称**: 79. 获取门店变更日志表列表
**Action**: `GetSERVERPARTSHOP_LOGList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取门店变更日志表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[SERVERPARTSHOP_LOGModel] | Y | 查询条件对象 |

SearchModel[SERVERPARTSHOP_LOGModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | SERVERPARTSHOP_LOGModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

SERVERPARTSHOP_LOGModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| SERVERPARTSHOP_IDS | string | 门店内码(查询条件) |
| SHOPTRADE | string | 商品业态 |
| SHOPTRADES | string | 商品业态(查询条件) |
| SHOPNAME | string | 门店名称 |
| SHOPSHORTNAME | string | 门店简称 |
| ISVALID | integer | 否有效 |
| SERVERPARTSHOP_INDEX | integer | 顺序 |
| TOPPERSON | string | 负责人 |
| TOPPERSON_MOBILE | string | 负责人电话 |
| LINKMAN | string | 联系人 |
| LINKMAN_MOBILE | string | 联系人电话 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码(查询条件) |
| SERVERPART_NAME | string | 服务区名称 |
| SHOPREGION | integer | 所属区域 |
| SHOPCODE | string | 门店编码 |
| ROYALTYRATE | number | 提成比例 |
| BUSINESS_UNIT | string | 经营单位 |
| BUSINESS_DATE | string | 开始经营时间 |
| BUS_STARTDATE | string | 经营时间 |
| BUSINESSAREA | number | 经营面积 |
| SETTLINGACCOUNTS | integer | 结算方式 |
| SELLER_ID | integer | 商户内码 |
| BUSINESS_TYPE | integer | 经营模式 |
| BUSINESS_STATE | integer | 经营状态 |
| BUSINESS_REGION | integer | 经营区域 |
| BUSINESS_NATURE | integer | 经营性质 |
| STATISTIC_TYPE | integer | 统计类型 |
| BUSINESS_ENDDATE | string | 停业时间 |
| REGISTERCOMPACT_ID | integer | 合同内码 |
| BUSINESS_TRADE | string | 经营业态 |
| BUSINESS_BRAND | integer | 经营品牌 |
| STATISTICS_TYPE | string | 统计归口 |
| STAFF_ID | number | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| OPERATE_DATE_Start | string | 操作时间(查询条件) |
| OPERATE_DATE_End | string | 操作时间(查询条件) |
| SERVERPARTSHOP_DESC | string | 备注说明 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[SERVERPARTSHOP_LOGModel]]> | 返回数据集合 |

JsonMsg[JsonList[SERVERPARTSHOP_LOGModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[SERVERPARTSHOP_LOGModel] | 返回对象 |

JsonList[SERVERPARTSHOP_LOGModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<SERVERPARTSHOP_LOGModel> | 返回数据集 |

---
### GET /BaseInfo/GetSPRegionShopTree
**名称**: 80. 绑定区域服务区门店树
**Action**: `GetSPRegionShopTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定区域服务区门店树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | N | 省份编码 |
| ServerpartId | string | N | 服务区内码集合 |
| ServerpartCodes | string | N | 服务区编码集合 |
| ServerpartShopId | string | N | 门店内码集合 |
| BusinessState | string | N | 经营状态 |
| BusinessType | string | N | 经营模式 |
| ShowWholePower | boolean | N | 显示全局权限 |
| ShowState | boolean | N | 显示经营状态 |
| ShowShortName | boolean | N | 树的门店节点是否按照简称显示 |
| ShowInSale | boolean | N | 是否只显示进销存门店 |
| SortStr | string | N | 排序字段 |
| ShowRoyalty | boolean | N | 是否只显示营收分润的门店 |
| ShowUnpaidExpense | boolean | N | 是否显示未缴付费用 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeTreeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeTreeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeTreeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeTreeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeTreeModel]> | 返回数据集 |

NestingModel[CommonTypeTreeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeTreeModel | 结点 |
| children | List<NestingModel[CommonTypeTreeModel]> | 子级 |

CommonTypeTreeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| ico | string | 图标地址 |
| desc | string | 额外描述内容 |
| children | List<CommonTypeModel> | 子集列表 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /BaseInfo/GetServerPartShopNewDetail
**名称**: 81. 获取服务区门店明细(业主使用)
**Action**: `GetServerPartShopNewDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区门店明细(业主使用)
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| serverPartShopId | integer | Y | 门店内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[ServerPartShopNewModel]> | 返回数据集合 |

JsonMsg[ServerPartShopNewModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | ServerPartShopNewModel | 返回对象 |

ServerPartShopNewModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ServerPartShop | SERVERPARTSHOPModel | 服务门店基础信息 |
| ShopBusinessStateList | List<ShopBusinessStateModel> | 门店经营状态 |
| RtServerPartShopList | List<RtServerPartShopModel> | 门店附属信息 |

SERVERPARTSHOPModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTSHOP_ID | integer | 内码 |
| SHOPTRADE | string | 行业名称 |
| SHOPNAME | string | 门店名称 |
| SHOPSHORTNAME | string | 门店简称 |
| ISVALID | integer | 否有效 |
| SERVERPARTSHOP_INDEX | number | 顺序 |
| TOPPERSON | string | 最高领导人 |
| TOPPERSON_MOBILE | string | 领导人电话 |
| LINKMAN | string | 联系人 |
| LINKMAN_MOBILE | string | 联系人电话 |
| SERVERPART_ID | integer | 服务区 |
| SHOPREGION | integer | 所属区域 |
| STOREHOUSE_TYPE | integer | 合作商户平台-仓储物资模式(0：否；1：是) |
| UNIFORMMANAGE_TYPE | integer | 是否接受统一定价管理(0：否；1：是) |
| AUDIT_UPLOADSTATE | integer | 是否上传稽核数据(0：否；1：是) |
| REVENUE_UPLOADSTATE | integer | 是否上传营收数据(0：否；1：是) |
| SALECOUNT_LIMIT | integer | 销售数量上限(是否存在销售数量异常的条件) |
| SALEAMOUNT_LIMIT | integer | 销售金额上限(是否存在销售金额异常的条件) |
| SHOPCODE | string | 门店编码 |
| ROYALTYRATE | number | 提成比例 |
| BUSINESS_UNIT | string | 经营单位 |
| BUSINESS_DATE | string | 开始经营时间 |
| BUS_STARTDATE | string | 经营时间 |
| BUSINESSAREA | number | 经营面积 |
| SETTLINGACCOUNTS | integer | 结算方式 |
| SELLER_ID | integer | 商户内码 |
| BUSINESS_TYPE | integer | 经营模式(1000：自营，2000：合作经营，3000：固定租金，4000：展销) |
| BUSINESS_STATE | integer | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| BUSINESS_REGION | integer | 经营区域(1000：服务区，2000：加油站) |
| BUSINESS_NATURE | integer | 经营性质(1000：油炸，2000：非油炸) |
| STATISTIC_TYPE | integer | 统计类型(1000：正式，2000：测试，3000：替代) |
| BUSINESS_ENDDATE | string | 停业时间 |
| REGISTERCOMPACT_ID | integer | 合同内码 |
| SERVERPART_NAME | string | 服务区名称 |
| BUSINESS_BRAND | integer | 经营品牌 |
| BUSINESS_TRADE | string | 经营业态 |
| STATISTICS_TYPE | string | 统计归口(收归口、进销存归口、走动式管理（用于权限控制)) |
| STAFF_ID | number | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SERVERPARTSHOP_DESC | string | 备注说明 |
| SELLER_NAME | string | 商户名称 |
| TAXPAYER_IDENTIFYCODE | string | 商户名称 |
| BANK_NAME | string | 商户名称 |
| BANK_ACCOUNT | string | 商户名称 |
| REGISTERCOMPACT_NAME | string | 合同名称 |
| BUSINESS_TRADENAME | string | 经营业态名称 |
| BRAND_NAME | string | 经营品牌名称 |
| SERVERPART_CODE | string | 服务区编码 |
| RECORD_DISCOUNT | integer | 是否记录优惠折扣(0：不记异常稽核；1：记录异常稽核) |
| OWNERUNIT_ID | integer | 业主单位内码 |
| OWNERUNIT_NAME | string | 业主单位名称 |
| REVENUE_INCLUDE | integer | 是否纳入营收【每日营收推送中是否展示该门店的营收数据】(0：否；1：是) |
| TRANSFER_TYPE | integer | 传输类型(0：收银系统；1：扫码传输【商户通过扫固定二维码上传数据】；2：接口传输【第三方营收数据通过接口上传至综管平台】) |
| APPROVAL_TYPE | integer | 审批模式(0：商品数据无需业主审批监管；1：商品数据需业主审批监管后生效；2：商品数据先生效业主再做监管) |
| INSALES_TYPE | integer | 综管平台-进销存模式(0：否；1：是) |
| PROVINCE_CODE | integer | 省份标识 |
| SERVERPARTSHOP_IDS | string | 门店内码集合（用于查询多个门店） |
| SERVERPART_IDS | string | 服务区内码集合（用于查询多个服务区） |

ShopBusinessStateModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ServerPartId | integer | 服务区内码 |
| ServerPartName | string | 服务门店名称 |
| ServerPartCode | string | 服务门店编码 |
| ServerPartShopId | integer | 服务门店内码 |
| SellerId | integer | 商户内码 |
| SellerName | string | 商户名称 |
| TaxPayerIdEntityCode | string | 统一信用代码 |
| BankAccount | string | 返款账户 |
| BusinessBrand | integer | 经营品牌 |
| BankName | string | 开户支行 |
| TopPerson | string | 负责人 |
| TopPersonMobile | string | 负责人电话 |
| LinkMan | string | 联系人名 |
| LinkManMobile | string | 联系电话 |
| ShopTrade | string | 商品业态 |
| BusinessTrade | string | 经营业态 |
| BrandName | string | 经营品牌 |
| ShopShortName | string | 门店简称 |
| ServerPartShopDesc | string | 门店备注说明 |
| IsValid | integer | 是否有效 |
| SaleCountLimit | number | 销售数量上限 |
| SaleAmountLimit | number | 销售金额上限 |
| RecordDiscount | integer | 优惠折扣 |
| BusinessRegion | integer | 经营区域 |
| ShopRegion | integer | 门店方位 |
| ShopName | string | 门店名称 |
| ShopCode | string | 门店编码 |
| BusinessDate | string | 开业时间 |
| BusinessEndDate | string | 停业时间 |
| BusinessType | integer | 经营模式 |
| BusinessState | integer | 经营状态 |

RtServerPartShopModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ServerPartShopId | integer | 门店内码 |
| ShopName | string | 门店名称 |
| BusinessDate | string | 开业时间 |
| BusinessEndDate | string | 停业时间 |
| StaffName | string | 操作人员 |
| OperateDate | string | 操作时间 |

---
### GET /BaseInfo/GetServerPartShopNewList
**名称**: 82. 获取服务区门店列表(业主使用)
**Action**: `GetServerPartShopNewList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区门店列表(业主使用)
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| provinceCode | integer | N | 省份编码 |
| serverPartId | string | N | 服务区内码 |
| businessState | string | N | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| businessType | string | N | 经营模式(1000：自营，2000：合作经营，3000：固定租金，4000：展销) |
| searchKeyName | string | N | 模糊查询字段 |
| searchKeyValue | string | N | 模糊查询值 |
| orderByStr | string | N | 排序字段 |
| sortStr | string | N | DESC:降序 ASC:升序 |
| pageIndex | integer | N | 查询页码数 |
| pageSize | integer | N | 每页显示数量 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[ShopCombineModel]]> | 返回数据集合 |

JsonMsg[JsonList[ShopCombineModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[ShopCombineModel] | 返回对象 |

JsonList[ShopCombineModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<ShopCombineModel> | 返回数据集 |

ShopCombineModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTSHOP_IDS | string | 门店内码集合（用于查询多个门店） |
| SERVERPARTSHOP_ID | integer | 内码 |
| SHOPTRADE | string | 行业名称 |
| SHOPNAME | string | 门店名称 |
| SHOPSHORTNAME | string | 门店简称 |
| ISVALID | integer | 否有效 |
| SERVERPARTSHOP_INDEX | number | 顺序 |
| LINKMAN | string | 联系人 |
| LINKMAN_MOBILE | string | 联系人电话 |
| SERVERPART_ID | integer | 服务区 |
| SHOPREGION | string | 所属区域 |
| SHOPCODE | string | 门店编码 |
| BUSINESS_UNIT | string | 经营单位 |
| BUSINESS_DATE | string | 开始经营时间 |
| BUS_STARTDATE | string | 经营时间 |
| BUSINESS_ENDDATE | string | 停业时间 |
| SELLER_ID | integer | 商户内码 |
| BUSINESS_TYPE | integer | 经营模式(1000：自营，2000：合作经营，3000：固定租金，4000：展销) |
| BUSINESS_STATE | integer | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| SERVERPART_NAME | string | 服务区名称 |
| BUSINESS_BRAND | integer | 经营品牌 |
| BUSINESS_TRADE | string | 经营业态 |
| OPERATE_DATE | string | 操作时间 |
| BUSINESS_TRADENAME | string | 经营业态名称 |
| BRAND_NAME | string | 经营品牌名称 |
| SERVERPART_CODE | string | 服务区编码 |
| OWNERUNIT_ID | integer | 业主单位内码 |
| OWNERUNIT_NAME | string | 业主单位名称 |
| PROVINCE_CODE | integer | 省份标识 |

---
### GET /BaseInfo/GetServerpartDDL
**名称**: 83. 绑定服务区下拉框
**Action**: `GetServerpartDDL`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定服务区下拉框
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartCodes | string | N | 服务区编码集合 |
| ProvinceCode | string | N | 省份编码 |
| ServerpartType | string | N | 服务区类型<br />            1000【服务区】<br />1010【区域】<br />2000【加油站】<br />            3000【业务部门】<br />4000【子公司】 |
| StatisticsType | string | N | 统计类型<br />            1000【正式】<br />2000【测试】<br />3000【替代】 |
| ShowWholePower | boolean | N | 显示全局权限 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[CommonModel]]> | 返回数据集合 |

JsonMsg[JsonList[CommonModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[CommonModel] | 返回对象 |

JsonList[CommonModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<CommonModel> | 返回数据集 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

---
### GET /BaseInfo/GetServerpartIdTree
**名称**: 84. 绑定服务区内码树
**Action**: `GetServerpartIdTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定服务区内码树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartCodes | string | N | 服务区编码集合 |
| ProvinceCode | string | N | 省份编码 |
| ServerpartType | string | N | 服务区类型<br />            1000【服务区】<br />1010【区域】<br />2000【加油站】<br />            3000【业务部门】<br />4000【子公司】 |
| StatisticsType | string | N | 统计类型<br />            1000【正式】<br />2000【测试】<br />3000【替代】 |
| SearchKey | string | N | 模糊查询条件 |
| ShowWholePower | boolean | N | 显示全局权限 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /BaseInfo/GetServerpartShopDDL
**名称**: 85. 绑定服务区门店下拉框
**Action**: `GetServerpartShopDDL`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定服务区门店下拉框
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | N | 省份编码 |
| ServerpartId | string | N | 服务区内码集合 |
| ShowWholePower | boolean | N | 显示全局权限 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[CommonModel]]> | 返回数据集合 |

JsonMsg[JsonList[CommonModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[CommonModel] | 返回对象 |

JsonList[CommonModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<CommonModel> | 返回数据集 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

---
### GET /BaseInfo/GetServerpartShopDetail
**名称**: 86. 获取门店明细
**Action**: `GetServerpartShopDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取门店明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartShopId | integer | Y | 门店内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[SERVERPARTSHOPModel]> | 返回数据集合 |

JsonMsg[SERVERPARTSHOPModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | SERVERPARTSHOPModel | 返回对象 |

SERVERPARTSHOPModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTSHOP_ID | integer | 内码 |
| SHOPTRADE | string | 行业名称 |
| SHOPNAME | string | 门店名称 |
| SHOPSHORTNAME | string | 门店简称 |
| ISVALID | integer | 否有效 |
| SERVERPARTSHOP_INDEX | number | 顺序 |
| TOPPERSON | string | 最高领导人 |
| TOPPERSON_MOBILE | string | 领导人电话 |
| LINKMAN | string | 联系人 |
| LINKMAN_MOBILE | string | 联系人电话 |
| SERVERPART_ID | integer | 服务区 |
| SHOPREGION | integer | 所属区域 |
| STOREHOUSE_TYPE | integer | 合作商户平台-仓储物资模式(0：否；1：是) |
| UNIFORMMANAGE_TYPE | integer | 是否接受统一定价管理(0：否；1：是) |
| AUDIT_UPLOADSTATE | integer | 是否上传稽核数据(0：否；1：是) |
| REVENUE_UPLOADSTATE | integer | 是否上传营收数据(0：否；1：是) |
| SALECOUNT_LIMIT | integer | 销售数量上限(是否存在销售数量异常的条件) |
| SALEAMOUNT_LIMIT | integer | 销售金额上限(是否存在销售金额异常的条件) |
| SHOPCODE | string | 门店编码 |
| ROYALTYRATE | number | 提成比例 |
| BUSINESS_UNIT | string | 经营单位 |
| BUSINESS_DATE | string | 开始经营时间 |
| BUS_STARTDATE | string | 经营时间 |
| BUSINESSAREA | number | 经营面积 |
| SETTLINGACCOUNTS | integer | 结算方式 |
| SELLER_ID | integer | 商户内码 |
| BUSINESS_TYPE | integer | 经营模式(1000：自营，2000：合作经营，3000：固定租金，4000：展销) |
| BUSINESS_STATE | integer | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| BUSINESS_REGION | integer | 经营区域(1000：服务区，2000：加油站) |
| BUSINESS_NATURE | integer | 经营性质(1000：油炸，2000：非油炸) |
| STATISTIC_TYPE | integer | 统计类型(1000：正式，2000：测试，3000：替代) |
| BUSINESS_ENDDATE | string | 停业时间 |
| REGISTERCOMPACT_ID | integer | 合同内码 |
| SERVERPART_NAME | string | 服务区名称 |
| BUSINESS_BRAND | integer | 经营品牌 |
| BUSINESS_TRADE | string | 经营业态 |
| STATISTICS_TYPE | string | 统计归口(收归口、进销存归口、走动式管理（用于权限控制)) |
| STAFF_ID | number | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SERVERPARTSHOP_DESC | string | 备注说明 |
| SELLER_NAME | string | 商户名称 |
| TAXPAYER_IDENTIFYCODE | string | 商户名称 |
| BANK_NAME | string | 商户名称 |
| BANK_ACCOUNT | string | 商户名称 |
| REGISTERCOMPACT_NAME | string | 合同名称 |
| BUSINESS_TRADENAME | string | 经营业态名称 |
| BRAND_NAME | string | 经营品牌名称 |
| SERVERPART_CODE | string | 服务区编码 |
| RECORD_DISCOUNT | integer | 是否记录优惠折扣(0：不记异常稽核；1：记录异常稽核) |
| OWNERUNIT_ID | integer | 业主单位内码 |
| OWNERUNIT_NAME | string | 业主单位名称 |
| REVENUE_INCLUDE | integer | 是否纳入营收【每日营收推送中是否展示该门店的营收数据】(0：否；1：是) |
| TRANSFER_TYPE | integer | 传输类型(0：收银系统；1：扫码传输【商户通过扫固定二维码上传数据】；2：接口传输【第三方营收数据通过接口上传至综管平台】) |
| APPROVAL_TYPE | integer | 审批模式(0：商品数据无需业主审批监管；1：商品数据需业主审批监管后生效；2：商品数据先生效业主再做监管) |
| INSALES_TYPE | integer | 综管平台-进销存模式(0：否；1：是) |
| PROVINCE_CODE | integer | 省份标识 |
| SERVERPARTSHOP_IDS | string | 门店内码集合（用于查询多个门店） |
| SERVERPART_IDS | string | 服务区内码集合（用于查询多个服务区） |

---
### GET /BaseInfo/GetServerpartShopIdTree
**名称**: 87. 绑定门店内码树
**Action**: `GetServerpartShopIdTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定门店内码树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartCodes | string | N | 服务区编码集合 |
| OWNERUNIT_ID | string | N | 业主单位内码 |
| ISVALID | string | N | 有效状态 |
| SearchKey | string | N | 模糊查询条件 |
| ShowWholePower | boolean | N | 显示全局权限 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /BaseInfo/GetServerpartShopInfo
**名称**: 88. 获取服务区门店信息
**Action**: `GetServerpartShopInfo`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区门店信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartCode | string | Y | 服务区编码 |
| ShopCode | string | Y | 门店编码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[ServerpartShopModel]> | 返回数据集合 |

JsonMsg[ServerpartShopModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | ServerpartShopModel | 返回对象 |

ServerpartShopModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ServerpartShopId | integer | 门店内码 |
| ServerpartShop_Code | string | 门店编码 |
| ServerpartShop_Name | string | 门店名称 |
| Serverpart_Id | integer | 服务区内码 |
| Serverpart_Code | string | 服务区编码 |
| Serverpart_Name | string | 服务区名称 |
| ServerpartShop_Trade | string | 商品业态 |
| ServerpartShop_Region | integer | 门店方位 |
| ServerpartShop_ShortName | string | 门店简称 |
| OwnerUnit_Id | integer | 业主单位内码 |
| OwnerUnit_Name | string | 业主单位名称 |
| Business_TradeName | string | 经营业态 |
| Business_BrandName | string | 经营品牌 |
| Business_BrandIcon | string | 经营品牌图标 |
| Business_Type | integer | 经营模式1000：业主自营2000：合作经营3000：固定租金4000：临时展销 |
| Business_State | integer | 经营状态1000：运营中1010：待运营2000：暂停中3000：已关闭 |
| Transfer_Type | integer | 传输方式0：收银系统1：扫码传输【商户通过扫固定二维码上传数据】2：接口传输【第三方营收数据通过接口上传至综管平台】 |
| InSalesType | integer | 办理进销存业务0：否1：是 |
| ServerpartShop_State | integer | 有效状态0：无效1：有效 |

---
### POST /BaseInfo/GetServerpartShopInfo
**名称**: 89. 获取服务区门店信息
**Action**: `GetServerpartShopInfo`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区门店信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartCode | string | Y | 服务区编码 |
| ShopCode | string | Y | 门店编码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[ServerpartShopModel]> | 返回数据集合 |

JsonMsg[ServerpartShopModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | ServerpartShopModel | 返回对象 |

ServerpartShopModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ServerpartShopId | integer | 门店内码 |
| ServerpartShop_Code | string | 门店编码 |
| ServerpartShop_Name | string | 门店名称 |
| Serverpart_Id | integer | 服务区内码 |
| Serverpart_Code | string | 服务区编码 |
| Serverpart_Name | string | 服务区名称 |
| ServerpartShop_Trade | string | 商品业态 |
| ServerpartShop_Region | integer | 门店方位 |
| ServerpartShop_ShortName | string | 门店简称 |
| OwnerUnit_Id | integer | 业主单位内码 |
| OwnerUnit_Name | string | 业主单位名称 |
| Business_TradeName | string | 经营业态 |
| Business_BrandName | string | 经营品牌 |
| Business_BrandIcon | string | 经营品牌图标 |
| Business_Type | integer | 经营模式1000：业主自营2000：合作经营3000：固定租金4000：临时展销 |
| Business_State | integer | 经营状态1000：运营中1010：待运营2000：暂停中3000：已关闭 |
| Transfer_Type | integer | 传输方式0：收银系统1：扫码传输【商户通过扫固定二维码上传数据】2：接口传输【第三方营收数据通过接口上传至综管平台】 |
| InSalesType | integer | 办理进销存业务0：否1：是 |
| ServerpartShop_State | integer | 有效状态0：无效1：有效 |

---
### POST /BaseInfo/GetServerpartShopList
**名称**: 90. 获取门店列表
**Action**: `GetServerpartShopList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取门店列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[SERVERPARTSHOPModel] | Y | 查询条件对象 |

SearchModel[SERVERPARTSHOPModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | SERVERPARTSHOPModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

SERVERPARTSHOPModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTSHOP_ID | integer | 内码 |
| SHOPTRADE | string | 行业名称 |
| SHOPNAME | string | 门店名称 |
| SHOPSHORTNAME | string | 门店简称 |
| ISVALID | integer | 否有效 |
| SERVERPARTSHOP_INDEX | number | 顺序 |
| TOPPERSON | string | 最高领导人 |
| TOPPERSON_MOBILE | string | 领导人电话 |
| LINKMAN | string | 联系人 |
| LINKMAN_MOBILE | string | 联系人电话 |
| SERVERPART_ID | integer | 服务区 |
| SHOPREGION | integer | 所属区域 |
| STOREHOUSE_TYPE | integer | 合作商户平台-仓储物资模式(0：否；1：是) |
| UNIFORMMANAGE_TYPE | integer | 是否接受统一定价管理(0：否；1：是) |
| AUDIT_UPLOADSTATE | integer | 是否上传稽核数据(0：否；1：是) |
| REVENUE_UPLOADSTATE | integer | 是否上传营收数据(0：否；1：是) |
| SALECOUNT_LIMIT | integer | 销售数量上限(是否存在销售数量异常的条件) |
| SALEAMOUNT_LIMIT | integer | 销售金额上限(是否存在销售金额异常的条件) |
| SHOPCODE | string | 门店编码 |
| ROYALTYRATE | number | 提成比例 |
| BUSINESS_UNIT | string | 经营单位 |
| BUSINESS_DATE | string | 开始经营时间 |
| BUS_STARTDATE | string | 经营时间 |
| BUSINESSAREA | number | 经营面积 |
| SETTLINGACCOUNTS | integer | 结算方式 |
| SELLER_ID | integer | 商户内码 |
| BUSINESS_TYPE | integer | 经营模式(1000：自营，2000：合作经营，3000：固定租金，4000：展销) |
| BUSINESS_STATE | integer | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| BUSINESS_REGION | integer | 经营区域(1000：服务区，2000：加油站) |
| BUSINESS_NATURE | integer | 经营性质(1000：油炸，2000：非油炸) |
| STATISTIC_TYPE | integer | 统计类型(1000：正式，2000：测试，3000：替代) |
| BUSINESS_ENDDATE | string | 停业时间 |
| REGISTERCOMPACT_ID | integer | 合同内码 |
| SERVERPART_NAME | string | 服务区名称 |
| BUSINESS_BRAND | integer | 经营品牌 |
| BUSINESS_TRADE | string | 经营业态 |
| STATISTICS_TYPE | string | 统计归口(收归口、进销存归口、走动式管理（用于权限控制)) |
| STAFF_ID | number | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SERVERPARTSHOP_DESC | string | 备注说明 |
| SELLER_NAME | string | 商户名称 |
| TAXPAYER_IDENTIFYCODE | string | 商户名称 |
| BANK_NAME | string | 商户名称 |
| BANK_ACCOUNT | string | 商户名称 |
| REGISTERCOMPACT_NAME | string | 合同名称 |
| BUSINESS_TRADENAME | string | 经营业态名称 |
| BRAND_NAME | string | 经营品牌名称 |
| SERVERPART_CODE | string | 服务区编码 |
| RECORD_DISCOUNT | integer | 是否记录优惠折扣(0：不记异常稽核；1：记录异常稽核) |
| OWNERUNIT_ID | integer | 业主单位内码 |
| OWNERUNIT_NAME | string | 业主单位名称 |
| REVENUE_INCLUDE | integer | 是否纳入营收【每日营收推送中是否展示该门店的营收数据】(0：否；1：是) |
| TRANSFER_TYPE | integer | 传输类型(0：收银系统；1：扫码传输【商户通过扫固定二维码上传数据】；2：接口传输【第三方营收数据通过接口上传至综管平台】) |
| APPROVAL_TYPE | integer | 审批模式(0：商品数据无需业主审批监管；1：商品数据需业主审批监管后生效；2：商品数据先生效业主再做监管) |
| INSALES_TYPE | integer | 综管平台-进销存模式(0：否；1：是) |
| PROVINCE_CODE | integer | 省份标识 |
| SERVERPARTSHOP_IDS | string | 门店内码集合（用于查询多个门店） |
| SERVERPART_IDS | string | 服务区内码集合（用于查询多个服务区） |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[SERVERPARTSHOPModel]]> | 返回数据集合 |

JsonMsg[JsonList[SERVERPARTSHOPModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[SERVERPARTSHOPModel] | 返回对象 |

JsonList[SERVERPARTSHOPModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<SERVERPARTSHOPModel> | 返回数据集 |

---
### GET /BaseInfo/GetServerpartShopTrade
**名称**: 91. 获取服务区商品业态
**Action**: `GetServerpartShopTrade`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取服务区商品业态
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | N | 省份编码 |
| ServerpartId | integer | N | 服务区内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[CommonModel]]> | 返回数据集合 |

JsonMsg[JsonList[CommonModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[CommonModel] | 返回对象 |

JsonList[CommonModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<CommonModel> | 返回数据集 |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

---
### GET /BaseInfo/GetServerpartShopTree
**名称**: 92. 绑定服务区门店树
**Action**: `GetServerpartShopTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定服务区门店树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | N | 省份编码 |
| ServerpartId | string | N | 服务区内码集合 |
| ServerpartCodes | string | N | 服务区编码集合 |
| ServerpartShopId | string | N | 门店内码集合 |
| BusinessState | string | N | 经营状态 |
| BusinessType | string | N | 经营模式 |
| ShowWholePower | boolean | N | 显示全局权限 |
| ShowState | boolean | N | 显示经营状态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeTreeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeTreeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeTreeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeTreeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeTreeModel]> | 返回数据集 |

NestingModel[CommonTypeTreeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeTreeModel | 结点 |
| children | List<NestingModel[CommonTypeTreeModel]> | 子级 |

CommonTypeTreeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| ico | string | 图标地址 |
| desc | string | 额外描述内容 |
| children | List<CommonTypeModel> | 子集列表 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /BaseInfo/GetServerpartTree
**名称**: 93. 绑定服务区树
**Action**: `GetServerpartTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定服务区树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | Y | 省份编码 |
| SPRegionType_ID | integer | N | 区域内码 |
| ServerpartType | string | N | 服务区类型：<br />            1000【服务区】<br />1010【区域】<br />2000【加油站】<br />            3000【业务部门】<br />4000【子公司】 |
| StatisticsType | string | N | 统计类型：<br />            1000【正式】<br />2000【测试】<br />3000【替代】 |
| ServerpartIds | string | N | 服务区内码集合 |
| ServerpartCodes | string | N | 服务区编码集合 |
| ShowWholePower | boolean | N | 显示全局权限 |
| ShowSPRegion | boolean | N | 是否显示区域，默认显示 |
| ShowRoyalty | boolean | N | 是否只显示营收分润的服务区 |
| ShowCompactCount | boolean | N | 是否显示合同数量 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[CommonTypeTreeModel]]> | 返回数据集合 |

JsonMsg[JsonList[CommonTypeTreeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[CommonTypeTreeModel] | 返回对象 |

JsonList[CommonTypeTreeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<CommonTypeTreeModel> | 返回数据集 |

CommonTypeTreeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| ico | string | 图标地址 |
| desc | string | 额外描述内容 |
| children | List<CommonTypeModel> | 子集列表 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /BaseInfo/GetServerpartUDTypeTree
**名称**: 94. 绑定区域服务区门店树
**Action**: `GetServerpartUDTypeTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定区域服务区门店树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | N | 省份编码 |
| ServerpartId | string | N | 服务区内码集合 |
| ShopTrade | string | N | 商品业态 |
| UserDefinedTypeState | integer | N | 有效状态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### GET /BaseInfo/GetShopReceivables
**名称**: 95. 获取经营门店关联合同项目信息
**Action**: `GetShopReceivables`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取经营门店关联合同项目信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartId | string | Y | 服务区内码 |
| BusinessState | string | N | 门店经营状态 |
| BusinessType | string | N | 门店经营模式 |
| AbnormalShop | boolean | N | 无合同在营门店 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[MerchantsReceivablesModel]> | 返回数据集合 |

JsonMsg[MerchantsReceivablesModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | MerchantsReceivablesModel | 返回对象 |

MerchantsReceivablesModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| COOPMERCHANTS_ID | string | 商户内码 |
| COOPMERCHANTS_ID_Encrypted | string | 商户加密内码 |
| COOPMERCHANTS_NAME | string | 商户名称 |
| COOPMERCHANTS_TYPENAME | string | 商户类别 |
| COOPMERCHANTS_NATURE | string | 商户性质 |
| COOPMERCHANTS_EN | string | 商户简称 |
| TAXPAYER_IDENTIFYCODE | string | 统一信用代码 |
| BANK_NAME | string | 开户银行 |
| BANK_ACCOUNT | string | 银行账号 |
| COOPMERCHANTS_LEGALPERSON | string | 法人 |
| COOPMERCHANTS_LEGALMOBILE | string | 法人手机号码 |
| COOPMERCHANTS_LINKMAN | string | 联系人员 |
| COOPMERCHANTS_MOBILEPHONE | string | 手机号码 |
| PROJECT_SIGNCOUNT | integer | 签约项目 |
| ACCOUNT_AMOUNT | number | 应收账款金额 |
| ACTUAL_PAYMENT | number | 已缴金额 |
| CURRENTBALANCE | number | 未缴金额 |
| UNDISTRIBUTED_AMOUNT | number | 未分配金额 |
| ACCOUNT_DATE | string | 应收账款日期 |
| AccountReceivablesList | List<AccountReceivablesModel> | 应收账款集合 |

AccountReceivablesModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| COOPMERCHANTS_ID | string | 商户内码 |
| COOPMERCHANTS_ID_Encrypted | string | 商户加密内码 |
| COOPMERCHANTS_NAME | string | 商户名称 |
| THREEPART_NAME | string | 丙方 |
| SERVERPART_IDS | string | 服务区内码 |
| SERVERPART_TYPE | string | 服务区类型 |
| SERVERPART_NAME | string | 服务区名称 |
| SECTIONFLOW_NUM | integer | 断面流量 |
| REGISTERCOMPACT_ID | string | 备案合同内码 |
| BUSINESSPROJECT_ID | integer | 经营项目内码 |
| BUSINESSPROJECT_NAME | string | 项目名称 |
| BUSINESSPROJECT_ICO | string | 项目图标 |
| BRAND_NAME | string | 品牌名称 |
| BUSINESSTRADE_NAME | string | 品牌业态名称 |
| BRAND_TYPENAME | string | 品牌类型名称 |
| BUSINESS_TRADE | integer | 合同业态 |
| BUSINESS_TYPE | integer | 经营模式 |
| SETTLEMENT_MODES | integer | 结算模式 |
| PROJECT_STARTDATE | string | 开始日期 |
| PROJECT_ENDDATE | string | 结束日期 |
| PROJECT_AMOUNT | number | 项目金额 |
| COMPACT_DURATION | integer | 合同年限 |
| PROJECT_DAYS | integer | 自然天数 |
| BUSINESSDAYS | integer | 营业天数 |
| DAILY_AMOUNT | number | 预期日均营业额 |
| SERVERPARTSHOP_ID | string | 门店内码 |
| SERVERPARTSHOP_NAME | string | 门店名称 |
| BUSINESS_STATE | integer | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| COMMISSION_RATIO | string | 提成比例 |
| ACCOUNT_DATE | string | 应收账款日期 |
| PAYABLE_AMOUNT | number | 应缴金额 |
| COMPACT_NAME | string | 经营合同名称 |
| COMMODITY_COUNT | integer | 商品数量 |
| REVENUE_AMOUNT | number | 营收金额 |
| ROYALTY_PRICE | number | 业主分润 |
| SUBROYALTY_PRICE | number | 商家分润 |
| CompactWarning | boolean | 合同信息不完整 |
| ProjectWarning | boolean | 经营项目信息不完整 |
| ProjectAccountDetailList | List<ProjectAccountDetailModel> | 经营项目应收账款明细列表 |

ProjectAccountDetailModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ACCOUNT_TYPE | number | 应收款项类型 |
| ACCOUNT_NAME | string | 应收款项名称 |
| PAYABLE_AMOUNT | number | 应缴金额 |

---
### GET /BaseInfo/GetShopShortNames
**名称**: 96. 获取服务区门店简称
**Action**: `GetShopShortNames`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
**场景**: 1、安徽查询自营业态有哪些门店
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | N | 省份编码 |
| ServerpartId | string | N | 服务区内码 |
| ShopTrade | string | N | 商品业态 |
| BusinessType | string | N | 经营模式，默认自营【1000】 |
| BusinessState | string | N | 经营状态 |
| ShopValid | integer | N | 有效状态，默认有效【1】 |
| ExcludeStaffMeal | boolean | N | 是否排除员工餐 |
| ShowFinance | boolean | N | 是否显示财务共享业态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[SERVERPARTSHOPModel]]> | 返回数据集合 |

JsonMsg[JsonList[SERVERPARTSHOPModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[SERVERPARTSHOPModel] | 返回对象 |

JsonList[SERVERPARTSHOPModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<SERVERPARTSHOPModel> | 返回数据集 |

SERVERPARTSHOPModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTSHOP_ID | integer | 内码 |
| SHOPTRADE | string | 行业名称 |
| SHOPNAME | string | 门店名称 |
| SHOPSHORTNAME | string | 门店简称 |
| ISVALID | integer | 否有效 |
| SERVERPARTSHOP_INDEX | number | 顺序 |
| TOPPERSON | string | 最高领导人 |
| TOPPERSON_MOBILE | string | 领导人电话 |
| LINKMAN | string | 联系人 |
| LINKMAN_MOBILE | string | 联系人电话 |
| SERVERPART_ID | integer | 服务区 |
| SHOPREGION | integer | 所属区域 |
| STOREHOUSE_TYPE | integer | 合作商户平台-仓储物资模式(0：否；1：是) |
| UNIFORMMANAGE_TYPE | integer | 是否接受统一定价管理(0：否；1：是) |
| AUDIT_UPLOADSTATE | integer | 是否上传稽核数据(0：否；1：是) |
| REVENUE_UPLOADSTATE | integer | 是否上传营收数据(0：否；1：是) |
| SALECOUNT_LIMIT | integer | 销售数量上限(是否存在销售数量异常的条件) |
| SALEAMOUNT_LIMIT | integer | 销售金额上限(是否存在销售金额异常的条件) |
| SHOPCODE | string | 门店编码 |
| ROYALTYRATE | number | 提成比例 |
| BUSINESS_UNIT | string | 经营单位 |
| BUSINESS_DATE | string | 开始经营时间 |
| BUS_STARTDATE | string | 经营时间 |
| BUSINESSAREA | number | 经营面积 |
| SETTLINGACCOUNTS | integer | 结算方式 |
| SELLER_ID | integer | 商户内码 |
| BUSINESS_TYPE | integer | 经营模式(1000：自营，2000：合作经营，3000：固定租金，4000：展销) |
| BUSINESS_STATE | integer | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| BUSINESS_REGION | integer | 经营区域(1000：服务区，2000：加油站) |
| BUSINESS_NATURE | integer | 经营性质(1000：油炸，2000：非油炸) |
| STATISTIC_TYPE | integer | 统计类型(1000：正式，2000：测试，3000：替代) |
| BUSINESS_ENDDATE | string | 停业时间 |
| REGISTERCOMPACT_ID | integer | 合同内码 |
| SERVERPART_NAME | string | 服务区名称 |
| BUSINESS_BRAND | integer | 经营品牌 |
| BUSINESS_TRADE | string | 经营业态 |
| STATISTICS_TYPE | string | 统计归口(收归口、进销存归口、走动式管理（用于权限控制)) |
| STAFF_ID | number | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SERVERPARTSHOP_DESC | string | 备注说明 |
| SELLER_NAME | string | 商户名称 |
| TAXPAYER_IDENTIFYCODE | string | 商户名称 |
| BANK_NAME | string | 商户名称 |
| BANK_ACCOUNT | string | 商户名称 |
| REGISTERCOMPACT_NAME | string | 合同名称 |
| BUSINESS_TRADENAME | string | 经营业态名称 |
| BRAND_NAME | string | 经营品牌名称 |
| SERVERPART_CODE | string | 服务区编码 |
| RECORD_DISCOUNT | integer | 是否记录优惠折扣(0：不记异常稽核；1：记录异常稽核) |
| OWNERUNIT_ID | integer | 业主单位内码 |
| OWNERUNIT_NAME | string | 业主单位名称 |
| REVENUE_INCLUDE | integer | 是否纳入营收【每日营收推送中是否展示该门店的营收数据】(0：否；1：是) |
| TRANSFER_TYPE | integer | 传输类型(0：收银系统；1：扫码传输【商户通过扫固定二维码上传数据】；2：接口传输【第三方营收数据通过接口上传至综管平台】) |
| APPROVAL_TYPE | integer | 审批模式(0：商品数据无需业主审批监管；1：商品数据需业主审批监管后生效；2：商品数据先生效业主再做监管) |
| INSALES_TYPE | integer | 综管平台-进销存模式(0：否；1：是) |
| PROVINCE_CODE | integer | 省份标识 |
| SERVERPARTSHOP_IDS | string | 门店内码集合（用于查询多个门店） |
| SERVERPART_IDS | string | 服务区内码集合（用于查询多个服务区） |

---
### POST /BaseInfo/GetShopShortNames
**名称**: 97. 获取服务区门店简称
**Action**: `GetShopShortNames`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
**场景**: 1、安徽查询自营业态有哪些门店
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | N | 省份编码 |
| ServerpartId | string | N | 服务区内码 |
| ShopTrade | string | N | 商品业态 |
| BusinessType | string | N | 经营模式，默认自营【1000】 |
| BusinessState | string | N | 经营状态 |
| ShopValid | integer | N | 有效状态，默认有效【1】 |
| ExcludeStaffMeal | boolean | N | 是否排除员工餐 |
| ShowFinance | boolean | N | 是否显示财务共享业态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[SERVERPARTSHOPModel]]> | 返回数据集合 |

JsonMsg[JsonList[SERVERPARTSHOPModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[SERVERPARTSHOPModel] | 返回对象 |

JsonList[SERVERPARTSHOPModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<SERVERPARTSHOPModel> | 返回数据集 |

SERVERPARTSHOPModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| SERVERPARTSHOP_ID | integer | 内码 |
| SHOPTRADE | string | 行业名称 |
| SHOPNAME | string | 门店名称 |
| SHOPSHORTNAME | string | 门店简称 |
| ISVALID | integer | 否有效 |
| SERVERPARTSHOP_INDEX | number | 顺序 |
| TOPPERSON | string | 最高领导人 |
| TOPPERSON_MOBILE | string | 领导人电话 |
| LINKMAN | string | 联系人 |
| LINKMAN_MOBILE | string | 联系人电话 |
| SERVERPART_ID | integer | 服务区 |
| SHOPREGION | integer | 所属区域 |
| STOREHOUSE_TYPE | integer | 合作商户平台-仓储物资模式(0：否；1：是) |
| UNIFORMMANAGE_TYPE | integer | 是否接受统一定价管理(0：否；1：是) |
| AUDIT_UPLOADSTATE | integer | 是否上传稽核数据(0：否；1：是) |
| REVENUE_UPLOADSTATE | integer | 是否上传营收数据(0：否；1：是) |
| SALECOUNT_LIMIT | integer | 销售数量上限(是否存在销售数量异常的条件) |
| SALEAMOUNT_LIMIT | integer | 销售金额上限(是否存在销售金额异常的条件) |
| SHOPCODE | string | 门店编码 |
| ROYALTYRATE | number | 提成比例 |
| BUSINESS_UNIT | string | 经营单位 |
| BUSINESS_DATE | string | 开始经营时间 |
| BUS_STARTDATE | string | 经营时间 |
| BUSINESSAREA | number | 经营面积 |
| SETTLINGACCOUNTS | integer | 结算方式 |
| SELLER_ID | integer | 商户内码 |
| BUSINESS_TYPE | integer | 经营模式(1000：自营，2000：合作经营，3000：固定租金，4000：展销) |
| BUSINESS_STATE | integer | 经营状态(1000：正常，2000：暂停，3000：关闭) |
| BUSINESS_REGION | integer | 经营区域(1000：服务区，2000：加油站) |
| BUSINESS_NATURE | integer | 经营性质(1000：油炸，2000：非油炸) |
| STATISTIC_TYPE | integer | 统计类型(1000：正式，2000：测试，3000：替代) |
| BUSINESS_ENDDATE | string | 停业时间 |
| REGISTERCOMPACT_ID | integer | 合同内码 |
| SERVERPART_NAME | string | 服务区名称 |
| BUSINESS_BRAND | integer | 经营品牌 |
| BUSINESS_TRADE | string | 经营业态 |
| STATISTICS_TYPE | string | 统计归口(收归口、进销存归口、走动式管理（用于权限控制)) |
| STAFF_ID | number | 操作员内码 |
| STAFF_NAME | string | 操作人员 |
| OPERATE_DATE | string | 操作时间 |
| SERVERPARTSHOP_DESC | string | 备注说明 |
| SELLER_NAME | string | 商户名称 |
| TAXPAYER_IDENTIFYCODE | string | 商户名称 |
| BANK_NAME | string | 商户名称 |
| BANK_ACCOUNT | string | 商户名称 |
| REGISTERCOMPACT_NAME | string | 合同名称 |
| BUSINESS_TRADENAME | string | 经营业态名称 |
| BRAND_NAME | string | 经营品牌名称 |
| SERVERPART_CODE | string | 服务区编码 |
| RECORD_DISCOUNT | integer | 是否记录优惠折扣(0：不记异常稽核；1：记录异常稽核) |
| OWNERUNIT_ID | integer | 业主单位内码 |
| OWNERUNIT_NAME | string | 业主单位名称 |
| REVENUE_INCLUDE | integer | 是否纳入营收【每日营收推送中是否展示该门店的营收数据】(0：否；1：是) |
| TRANSFER_TYPE | integer | 传输类型(0：收银系统；1：扫码传输【商户通过扫固定二维码上传数据】；2：接口传输【第三方营收数据通过接口上传至综管平台】) |
| APPROVAL_TYPE | integer | 审批模式(0：商品数据无需业主审批监管；1：商品数据需业主审批监管后生效；2：商品数据先生效业主再做监管) |
| INSALES_TYPE | integer | 综管平台-进销存模式(0：否；1：是) |
| PROVINCE_CODE | integer | 省份标识 |
| SERVERPARTSHOP_IDS | string | 门店内码集合（用于查询多个门店） |
| SERVERPART_IDS | string | 服务区内码集合（用于查询多个服务区） |

---
### GET /BaseInfo/GetTradeBrandTree
**名称**: 98. 查询经营品牌树
**Action**: `GetTradeBrandTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
查询经营品牌树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessTrade_PID | integer | N | 经营业态父级内码 |
| ProvinceCode | integer | N | 省份编码 |
| OwnerUnitId | integer | N | 业主单位内码 |
| BrandState | integer | N | 有效状态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[TradeBrandTreeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[TradeBrandTreeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[TradeBrandTreeModel]] | 返回对象 |

JsonList[NestingModel[TradeBrandTreeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[TradeBrandTreeModel]> | 返回数据集 |

NestingModel[TradeBrandTreeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | TradeBrandTreeModel | 结点 |
| children | List<NestingModel[TradeBrandTreeModel]> | 子级 |

TradeBrandTreeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| BusinessTrade_Id | integer | 经营业态内码 |
| BusinessTrade_Name | string | 经营业态名称 |
| BusinessTrade_ICO | string | 经营业态图标 |
| BrandTreeList | List<BrandTreeModel> | 经营品牌集合 |

BrandTreeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Brand_ID | integer | 品牌内码 |
| Brand_Name | string | 品牌名称 |
| Brand_Type | integer | 品牌类型 |
| Brand_ICO | string | 品牌图标 |

---
### POST /BaseInfo/GetTradeBrandTree
**名称**: 99. 查询经营品牌树
**Action**: `GetTradeBrandTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
查询经营品牌树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessTrade_PID | integer | N | 经营业态父级内码 |
| ProvinceCode | integer | N | 省份编码 |
| OwnerUnitId | integer | N | 业主单位内码 |
| BrandState | integer | N | 有效状态 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[TradeBrandTreeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[TradeBrandTreeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[TradeBrandTreeModel]] | 返回对象 |

JsonList[NestingModel[TradeBrandTreeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[TradeBrandTreeModel]> | 返回数据集 |

NestingModel[TradeBrandTreeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | TradeBrandTreeModel | 结点 |
| children | List<NestingModel[TradeBrandTreeModel]> | 子级 |

TradeBrandTreeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| BusinessTrade_Id | integer | 经营业态内码 |
| BusinessTrade_Name | string | 经营业态名称 |
| BusinessTrade_ICO | string | 经营业态图标 |
| BrandTreeList | List<BrandTreeModel> | 经营品牌集合 |

BrandTreeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Brand_ID | integer | 品牌内码 |
| Brand_Name | string | 品牌名称 |
| Brand_Type | integer | 品牌类型 |
| Brand_ICO | string | 品牌图标 |

---
### GET /BaseInfo/GetUSERAUTHORITYDetail
**名称**: 100. 获取用户门店权限表明细
**Action**: `GetUSERAUTHORITYDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取用户门店权限表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| USERAUTHORITYId | integer | Y | 用户门店权限表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[USERAUTHORITYModel]> | 返回数据集合 |

JsonMsg[USERAUTHORITYModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | USERAUTHORITYModel | 返回对象 |

USERAUTHORITYModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USERAUTHORITY_ID | integer | 用户门店权限内码 |
| USER_ID | integer | 帐户内码 |
| USER_IDS | string | 帐户内码(查询条件) |
| OWNERUNIT_ID | integer | 业主单位内码 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码（查询条件） |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| SERVERPARTSHOP_IDS | string | 门店内码(查询条件) |
| OPERATE_DATE | string | 操作时间 |
| UserName | string | 用户名 |

---
### POST /BaseInfo/GetUSERAUTHORITYList
**名称**: 101. 获取用户门店权限表列表
**Action**: `GetUSERAUTHORITYList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取用户门店权限表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[USERAUTHORITYModel] | Y | 查询条件对象 |

SearchModel[USERAUTHORITYModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | USERAUTHORITYModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

USERAUTHORITYModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USERAUTHORITY_ID | integer | 用户门店权限内码 |
| USER_ID | integer | 帐户内码 |
| USER_IDS | string | 帐户内码(查询条件) |
| OWNERUNIT_ID | integer | 业主单位内码 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPART_IDS | string | 服务区内码（查询条件） |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| SERVERPARTSHOP_IDS | string | 门店内码(查询条件) |
| OPERATE_DATE | string | 操作时间 |
| UserName | string | 用户名 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[USERAUTHORITYModel]]> | 返回数据集合 |

JsonMsg[JsonList[USERAUTHORITYModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[USERAUTHORITYModel] | 返回对象 |

JsonList[USERAUTHORITYModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<USERAUTHORITYModel> | 返回数据集 |

---
### GET /BaseInfo/GetUSERDEFINEDTYPEDetail
**名称**: 102. 获取商品自定义类别表明细
**Action**: `GetUSERDEFINEDTYPEDetail`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取商品自定义类别表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| USERDEFINEDTYPEId | integer | Y | 商品自定义类别表内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[USERDEFINEDTYPEModel]> | 返回数据集合 |

JsonMsg[USERDEFINEDTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | USERDEFINEDTYPEModel | 返回对象 |

USERDEFINEDTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USERDEFINEDTYPE_ID | integer | 自定义类内码 |
| USERDEFINEDTYPE_PID | integer | 上级内码 |
| USERDEFINEDTYPE_NAME | string | 类别名称 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPARTCODE | string | 服务区编码 |
| SERVERPARTCODES | string | 服务区编码(查询条件) |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| BUSINESSTYPE | integer | 业态 |
| SCANCODE_ORDER | integer | 扫码点餐 |
| USERDEFINEDTYPE_DATE | string | 添加时间 |
| USERDEFINEDTYPE_INDEX | integer | 类别索引 |
| USERDEFINEDTYPE_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人员内码 |
| STAFF_NAME | string | 操作人员名称 |
| OPERATE_DATE | string | 操作时间 |
| USERDEFINEDTYPE_DESC | string | 备注 |
| ShopNames | string | 门店名称 |

---
### POST /BaseInfo/GetUSERDEFINEDTYPEList
**名称**: 103. 获取商品自定义类别表列表
**Action**: `GetUSERDEFINEDTYPEList`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
获取商品自定义类别表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel[USERDEFINEDTYPEModel] | Y | 查询条件对象 |

SearchModel[USERDEFINEDTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| QueryType | integer | 查询方式<br />0:模糊查询，1:精确查询 |
| SearchParameter | USERDEFINEDTYPEModel | 查询表对象 |
| keyWord | KeyWord | 组合查询条件 |
| PageIndex | integer | 查询页码数 |
| PageSize | integer | 每页显示数量 |
| SortStr | string | 排序条件 |
| ShowWholePower | boolean | 是否按省份编码显示数据 |
| Province_Code | string | 省份编码 |

USERDEFINEDTYPEModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| USERDEFINEDTYPE_ID | integer | 自定义类内码 |
| USERDEFINEDTYPE_PID | integer | 上级内码 |
| USERDEFINEDTYPE_NAME | string | 类别名称 |
| SERVERPART_ID | integer | 服务区内码 |
| SERVERPARTCODE | string | 服务区编码 |
| SERVERPARTCODES | string | 服务区编码(查询条件) |
| SERVERPARTSHOP_ID | integer | 门店内码 |
| BUSINESSTYPE | integer | 业态 |
| SCANCODE_ORDER | integer | 扫码点餐 |
| USERDEFINEDTYPE_DATE | string | 添加时间 |
| USERDEFINEDTYPE_INDEX | integer | 类别索引 |
| USERDEFINEDTYPE_STATE | integer | 有效状态 |
| STAFF_ID | integer | 操作人员内码 |
| STAFF_NAME | string | 操作人员名称 |
| OPERATE_DATE | string | 操作时间 |
| USERDEFINEDTYPE_DESC | string | 备注 |
| ShopNames | string | 门店名称 |

KeyWord 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Key | string | 字段 |
| Value | string | 值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[USERDEFINEDTYPEModel]]> | 返回数据集合 |

JsonMsg[JsonList[USERDEFINEDTYPEModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[USERDEFINEDTYPEModel] | 返回对象 |

JsonList[USERDEFINEDTYPEModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<USERDEFINEDTYPEModel> | 返回数据集 |

---
### GET /BaseInfo/GetUserDefinedTypeIdTree
**名称**: 104. 绑定自定义商品类型内码树
**Action**: `GetUserDefinedTypeIdTree`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
绑定自定义商品类型内码树
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| Pid | string | N | 上级分类 |
| SERVERPART_ID | string | N | 服务区内码 |
| BUSINESSTYPE | string | N | 商品业态 |
| USERDEFINEDTYPE_STATE | string | N | 分类是否有效 |
| SearchKey | string | N | 模糊查询内容 |
| ShowWholePower | boolean | N | 显示全局权限 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[JsonList[NestingModel[CommonTypeModel]]]> | 返回数据集合 |

JsonMsg[JsonList[NestingModel[CommonTypeModel]]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | JsonList[NestingModel[CommonTypeModel]] | 返回对象 |

JsonList[NestingModel[CommonTypeModel]] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| PageIndex | integer | 页码 |
| PageSize | integer | 每页显示数量 |
| TotalCount | integer | 数据总数量 |
| List | List<NestingModel[CommonTypeModel]> | 返回数据集 |

NestingModel[CommonTypeModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| node | CommonTypeModel | 结点 |
| children | List<NestingModel[CommonTypeModel]> | 子级 |

CommonTypeModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | integer | 数值（对应数据表id） |
| key | string | 数值代码（字符串） |
| type | integer | 数据类型 |
| desc | string | 额外描述内容 |
| ico | string | 图标地址 |

---
### POST /BaseInfo/LowerShelfCommodity
**名称**: 105. 下架服务区在售商品
**Action**: `LowerShelfCommodity`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
---
### POST /BaseInfo/LowerShelfCommodity
**名称**: 传入参数：ProvinceCode
**Action**: `业主省份编码`

#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[String]> | 返回数据集合 |

JsonMsg[String] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | string | 返回对象 |

---
### POST /BaseInfo/ModifyShopBusinessState
**名称**: 106. 批量设置门店经营状态（内部使用）
**Action**: `ModifyShopBusinessState`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**:
> ⚠️ **加密要求**: 该接口入参 `postData` 需进行 AES 加密转换。
> 
> **请求模式**:
> 1. 将业务参数构建为 JSON 字符串。
> 2. 使用 AES 算法对字符串加密。
> 3. 将密文作为 `value` 字段的值发送，格式如：`{"name": "", "value": "BASE64_ENCRYPTED_STRING"}`。
 
批量设置门店经营状态（内部使用）
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了： |

CommonModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| label | string | 名称 |
| value | string | 数值（对应数据表id） |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[ServerPartShopStateModel]> | 返回数据集合 |

JsonMsg[ServerPartShopStateModel] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | ServerPartShopStateModel | 返回对象 |

ServerPartShopStateModel 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ServerPartShopId | integer | 服务门店内码 |
| BusinessState | integer | 经营状态 |

---
### POST /BaseInfo/ModifyShopState
**名称**: 107. 变更门店经营状态
**Action**: `ModifyShopState`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
变更门店经营状态
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ShopModifyList | array | Y | 变更的门店列表 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[String]> | 返回数据集合 |

JsonMsg[String] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | string | 返回对象 |

---
### POST /BaseInfo/OnShelfCommodity
**名称**: 108. 上架服务区在售商品
**Action**: `OnShelfCommodity`

**场景**: 
用于 BaseInfo 模块基础数据维护与查询。
**说明**: 
---
### POST /BaseInfo/OnShelfCommodity
**名称**: 传入参数：ProvinceCode
**Action**: `业主省份编码`

#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | List<JsonMsg[String]> | 返回数据集合 |

JsonMsg[String] 结构说明
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | integer | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | string | 返回对象 |

---
### POST /Commodity/GetCOMMODITYList
**名称**: 获取商品管理列表
**Action**: `GetCOMMODITYList`

**场景**: 
用于 Commodity 模块商品管理相关操作。
**说明**: 
获取商品管理列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Commodity/GetCOMMODITYDetail
**名称**: 获取商品管理明细
**Action**: `GetCOMMODITYDetail`

**场景**: 
用于 Commodity 模块商品管理相关操作。
**说明**: 
获取商品管理明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| COMMODITYId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET,POST /Commodity/DeleteCOMMODITY
**名称**: 删除商品管理
**Action**: `DeleteCOMMODITY`

**场景**: 
用于 Commodity 模块商品管理相关操作。
**说明**: 
删除商品管理
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| COMMODITYId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Commodity/GetCOMMODITY_RUNNINGList
**名称**: 获取商品管理（审批过程）列表
**Action**: `GetCOMMODITY_RUNNINGList`

**场景**: 
用于 Commodity 模块商品管理相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
获取获取商品管理（审批过程）列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了： |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Commodity/GetCOMMODITY_RUNNINGDetail
**名称**: 获取商品管理（审批过程）明细
**Action**: `GetCOMMODITY_RUNNINGDetail`

**场景**: 
用于 Commodity 模块商品管理相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
获取获取商品管理（审批过程）明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了： |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Commodity/GetCOMMODITY_HISTORYList
**名称**: 获取商品管理列表（历史记录）
**Action**: `GetCOMMODITY_HISTORYList`

**场景**: 
用于 Commodity 模块商品管理相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
获取获取商品管理列表（历史记录）
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了： |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### Get /Commodity/GetCommodityList
**名称**: 获取商品信息列表
**Action**: ``

**场景**: 
用于 Commodity 模块商品管理相关操作。
**说明**: 
获取商品信息列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SearchType | string | Y |  |
| ProvinceCode | string | Y |  |
| SPRegionTypeID | string | Y |  |
| ServerpartID | string | Y |  |
| ServerpartShopID | string | Y |  |
| ShopTrade | string | Y |  |
| CommodityTypeId | integer | Y |  |
| CommodityState | string | Y |  |
| UserDefinedTypeId | integer | Y |  |
| ShowJustUDType | string | Y |  |
| OperateDate_Start | string | Y |  |
| OperateDate_End | string | Y |  |
| SearchKey | string | Y |  |
| SearchValue | string | Y |  |
| PageIndex | string | Y |  |
| PageSize | string | Y |  |
| SortStr | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Commodity/RelateUDType
**名称**: 关联商品自定义类别
**Action**: `RelateUDType`

**场景**: 
用于 Commodity 模块商品管理相关操作。
**说明**: 
关联商品自定义类别
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| CommodityIdList | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Commodity/GetServerpartShopTrade
**名称**: 根据服务区查询商品业态
**Action**: `GetServerpartShopTrade`

**场景**: 
用于 Commodity 模块商品管理相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
获取根据服务区查询商品业态
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了： |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Commodity/GetApprovalCommodityList
**名称**: 查询商品审批记录
**Action**: `GetApprovalCommodityList`

**场景**: 
用于 Commodity 模块商品管理相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
获取查询商品审批记录
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了： |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Commodity/ApproveCommodityInfo_AHJG
**名称**: 审核安徽建工便利店商品数据
**Action**: `ApproveCommodityInfo_AHJG`

**场景**: 
用于 Commodity 模块商品管理相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
获取审核安徽建工便利店商品数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了： |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |


## 合同备案表相关接口【ContractController】

---
### POST /Contract/GetRegisterCompactList
**名称**: 合同备案表相关接口
**Action**: `GetRegisterCompactList`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
合同备案表相关接口
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Contract/GetRegisterCompactDetail
**名称**: 获取合同备案明细
**Action**: `GetRegisterCompactDetail`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
获取合同备案明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| RegisterCompactId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Contract/GetRegisterCompactSubList
**名称**: 获取备案合同附属列表
**Action**: `GetRegisterCompactSubList`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
获取备案合同附属列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Contract/GetRegisterCompactSubDetail
**名称**: 获取备案合同附属表明细
**Action**: `GetRegisterCompactSubDetail`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
获取备案合同附属表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| RegisterCompactSubId | integer | Y |  |
| RegisterCompactId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Contract/GetRTRegisterCompactList
**名称**: 获取经营合同服务区关联表列表
**Action**: `GetRTRegisterCompactList`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
获取经营合同服务区关联表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Contract/GetRTRegisterCompactDetail
**名称**: 获取经营合同服务区关联表明细
**Action**: `GetRTRegisterCompactDetail`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
获取经营合同服务区关联表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| RTRegisterCompactId | integer | Y |  |
| RegisterCompactId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Contract/GetAttachmentList
**名称**: 获取附件表列表
**Action**: `GetAttachmentList`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
获取附件表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Contract/GetAttachmentDetail
**名称**: 获取附件表明细
**Action**: `GetAttachmentDetail`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
获取附件表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| AttachmentId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Contract/GetProjectSummaryInfo
**名称**: 获取项目欠款汇总信息
**Action**: `GetProjectSummaryInfo`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
获取项目欠款汇总信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | Y |  |
| ServerpartId | integer | Y |  |
| ServerpartShopIds | string | Y |  |
| GetFromRedis | boolean | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Contract/GetContractExpiredInfo
**名称**: 获取合同到期信息
**Action**: `GetContractExpiredInfo`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
获取合同到期信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | Y | 省份编码 |
| ServerpartId | integer | Y | 服务区内码集合 |
| ServerpartShopIds | string | Y | 门店内码集合 |
| GetFromRedis | boolean | Y | 从缓存表取值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Contract/GetProjectYearlyArrearageList
**名称**: 获取合同年度完成度信息
**Action**: `GetProjectYearlyArrearageList`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
获取合同年度完成度信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | Y | 省份编码 |
| ServerpartId | integer | Y | 服务区内码集合 |
| ServerpartShopIds | string | Y | 门店内码集合 |
| GetFromRedis | boolean | Y | 从缓存表取值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Contract/GetProjectMonthlyArrearageList
**名称**: 获取合同月度完成度信息
**Action**: `GetProjectMonthlyArrearageList`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
获取合同月度完成度信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StatisticsYear | integer | Y |  |
| ProvinceCode | integer | Y | 省份编码 |
| ServerpartId | integer | Y | 服务区内码集合 |
| ServerpartShopIds | string | Y | 门店内码集合 |
| GetFromRedis | boolean | Y | 从缓存表取值 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Contract/GetContractYearList
**名称**: 获取合同年份列表
**Action**: `GetContractYearList`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
获取合同年份列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SortStr | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Contract/GetShopBusinessTypeRatio
**名称**: 统计门店经营模式占比
**Action**: `GetShopBusinessTypeRatio`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
统计门店经营模式占比
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Contract/AddContractSupplement
**名称**: 增加合同补充协议
**Action**: `AddContractSupplement`

**场景**: 
用于 Contract 模块相关操作。
**说明**: 
增加合同补充协议
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| contractSAModel | escm.contractsamodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetBusinessProjectList
**名称**: 经营项目相关接口
**Action**: `GetBusinessProjectList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
经营项目相关接口
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetBusinessProjectDetail
**名称**: 获取经营项目明细
**Action**: `GetBusinessProjectDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营项目明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessProjectId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetShopRoyaltyList
**名称**: 获取门店提成比例表列表
**Action**: `GetShopRoyaltyList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取门店提成比例表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetShopRoyaltyDetail
**名称**: 获取门店提成比例明细
**Action**: `GetShopRoyaltyDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取门店提成比例明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ShopRoyaltyId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetSHOPROYALTYDETAILList
**名称**: 获取门店应收拆分明细表列表
**Action**: `GetSHOPROYALTYDETAILList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取门店应收拆分明细表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetSHOPROYALTYDETAILDetail
**名称**: 获取门店应收拆分明细表明细
**Action**: `GetSHOPROYALTYDETAILDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取门店应收拆分明细表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SHOPROYALTYDETAILId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetRevenueConfirmList
**名称**: 获取营收回款确认表列表
**Action**: `GetRevenueConfirmList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取营收回款确认表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetRevenueConfirmList
**名称**: 获取营收回款确认表列表
**Action**: `GetRevenueConfirmList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取营收回款确认表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartId | string | Y |  |
| MerchantsId | string | Y |  |
| BusinessType | string | Y |  |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| PageSize | integer | Y |  |
| PageIndex | integer | Y |  |
| SortStr | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetRevenueConfirmDetail
**名称**: 获取营收回款确认表明细
**Action**: `GetRevenueConfirmDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取营收回款确认表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| RevenueConfirmId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetPaymentConfirmList
**名称**: 获取商家应收回款列表
**Action**: `GetPaymentConfirmList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取商家应收回款列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetPaymentConfirmList
**名称**: 获取商家应收回款列表
**Action**: `GetPaymentConfirmList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取商家应收回款列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| MerchantsId | string | Y |  |
| ServerpartShopIds | string | Y |  |
| BusinessProjectId | string | Y |  |
| AccountDate | string | Y |  |
| ShowJustPayable | integer | Y |  |
| WholeAccountType | integer | Y |  |
| AccountType | string | Y |  |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| ShowRemarks | boolean | Y |  |
| SortStr | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetPaymentConfirmDetail
**名称**: 获取营收回款到账明细
**Action**: `GetPaymentConfirmDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取营收回款到账明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PaymentConfirmId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetRTPaymentRecordList
**名称**: 获取商家回款记录表列表
**Action**: `GetRTPaymentRecordList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取商家回款记录表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetRTPaymentRecordDetail
**名称**: 获取商家回款记录表明细
**Action**: `GetRTPaymentRecordDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取商家回款记录表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| RTPaymentRecordId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetRemarksList
**名称**: 获取备注说明表列表
**Action**: `GetRemarksList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取备注说明表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetRemarksDetail
**名称**: 获取备注说明表明细
**Action**: `GetRemarksDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取备注说明表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| RemarksId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetBusinessPaymentList
**名称**: 获取经营商户经营项目执行情况表列表
**Action**: `GetBusinessPaymentList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营商户经营项目执行情况表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetBusinessPaymentDetail
**名称**: 获取经营商户经营项目执行情况表明细
**Action**: `GetBusinessPaymentDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营商户经营项目执行情况表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessPaymentId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetBUSINESSPROJECTSPLITList
**名称**: 获取经营项目应收拆分表列表
**Action**: `GetBUSINESSPROJECTSPLITList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营项目应收拆分表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetBUSINESSPROJECTSPLITDetail
**名称**: 获取经营项目应收拆分表明细
**Action**: `GetBUSINESSPROJECTSPLITDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营项目应收拆分表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BUSINESSPROJECTSPLITId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetBIZPSPLITMONTHList
**名称**: 获取月度经营项目应收拆分表列表
**Action**: `GetBIZPSPLITMONTHList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取月度经营项目应收拆分表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetBIZPSPLITMONTHDetail
**名称**: 获取月度经营项目应收拆分表明细
**Action**: `GetBIZPSPLITMONTHDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取月度经营项目应收拆分表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BIZPSPLITMONTHId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetPROJECTWARNINGList
**名称**: 获取经营项目预警表列表
**Action**: `GetPROJECTWARNINGList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营项目预警表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetPROJECTWARNINGDetail
**名称**: 获取经营项目预警表明细
**Action**: `GetPROJECTWARNINGDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营项目预警表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PROJECTWARNINGId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetPERIODWARNINGList
**名称**: 获取经营项目周期预警表列表
**Action**: `GetPERIODWARNINGList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营项目周期预警表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetPERIODWARNINGDetail
**名称**: 获取经营项目周期预警表明细
**Action**: `GetPERIODWARNINGDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营项目周期预警表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PERIODWARNINGId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetAPPROVEDList
**名称**: 获取审批意见列表
**Action**: `GetAPPROVEDList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取审批意见列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetSHOPEXPENSEList
**名称**: 获取门店费用列表
**Action**: `GetSHOPEXPENSEList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取门店费用列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y | 查询条件对象 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetSHOPEXPENSEDetail
**名称**: 获取门店费用明细
**Action**: `GetSHOPEXPENSEDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取门店费用明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SHOPEXPENSEId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/ApproveSHOPEXPENSE
**名称**: 审批门店费用
**Action**: `ApproveSHOPEXPENSE`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
审批门店费用
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| approveSHOPEXPENSEModel | list<escm.approveshopexpensemodel> | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/GetPROJECTSPLITMONTHList
**名称**: 获取租赁商铺按月收入确认表列表
**Action**: `GetPROJECTSPLITMONTHList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取租赁商铺按月收入确认表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetPROJECTSPLITMONTHDetail
**名称**: 获取租赁商铺按月收入确认表明细
**Action**: `GetPROJECTSPLITMONTHDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取租赁商铺按月收入确认表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PROJECTSPLITMONTHId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetMerchantsReceivablesList
**名称**: 获取经营商户应收账款列表
**Action**: `GetMerchantsReceivablesList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营商户应收账款列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| MerchantsId | string | Y |  |
| MerchantsName | string | Y |  |
| ShowJustPayable | integer | Y |  |
| PageIndex | integer | Y |  |
| PageSize | integer | Y |  |
| SortStr | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetMerchantsReceivables
**名称**: 获取经营商户应收账款信息
**Action**: `GetMerchantsReceivables`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营商户应收账款信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| MerchantsId | string | Y | 经营商户内码（加密） |
| ServerpartShopIds | string | Y |  |
| StartDate | string | Y |  |
| ShowRevenueSplit | boolean | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetBrandReceivables
**名称**: 获取经营品牌关联应收账款信息
**Action**: `GetBrandReceivables`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营品牌关联应收账款信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessTradeId | string | Y |  |
| BusinessBrandId | string | Y |  |
| ServerpartId | string | Y |  |
| StartDate | string | Y | 统计营收开始日期 |
| ShowProjectSplit | boolean | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetMerchantsReceivablesReport
**名称**: 获取经营商户应收预警统计表
**Action**: `GetMerchantsReceivablesReport`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营商户应收预警统计表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| MerchantsId | string | Y |  |
| AccountDate | string | Y |  |
| PaymentDate | string | Y |  |
| SearchKeyName | string | Y |  |
| SearchKeyValue | string | Y |  |
| BusinessType | string | Y |  |
| SortStr | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/CreateRevenueAccount
**名称**: 根据门店提成比例生成应收账款信息（合作分成）
**Action**: `CreateRevenueAccount`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
根据门店提成比例生成应收账款信息（合作分成）
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ShopRoyaltyId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/ApproveProinst
**名称**: 审批移动支付分账比例切换流程
**Action**: `ApproveProinst`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
审批移动支付分账比例切换流程
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessId | integer | Y |  |
| StaffId | integer | Y |  |
| StaffName | string | Y |  |
| SwitchRate | integer | Y |  |
| ApproveState | short | Y |  |
| SourcePlatform | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetExpenseSummary
**名称**: 获取服务区门店费用汇总数据
**Action**: `GetExpenseSummary`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取服务区门店费用汇总数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| serverpart_ids | string | Y |  |
| shopShortName | string | Y |  |
| BusinessUnit | string | Y |  |
| statistics_month | string | Y |  |
| StartMonth | string | Y |  |
| EndMonth | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetShopExpenseSummary
**名称**: 获取商户月度应收款项明细表
**Action**: `GetShopExpenseSummary`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取商户月度应收款项明细表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| serverpartshop_id | string | Y |  |
| statistics_month_start | string | Y |  |
| statistics_month_end | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetMonthSummaryList
**名称**: 获取经营项目月度汇总信息
**Action**: `GetSummaryList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营项目月度汇总信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StatisticsMonth | string | Y |  |
| StatisticsStartMonth | string | Y |  |
| SPRegionTypeId | string | Y |  |
| ServerpartId | string | Y |  |
| ServerpartShopId | string | Y |  |
| MerchantId | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetNoProjectShopList
**名称**: 获取没有设置经营项目的移动支付分账门店
**Action**: `GetNoProjectShopList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取没有设置经营项目的移动支付分账门店
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProvinceCode | string | Y |  |
| SPRegionTypeID | string | Y |  |
| ServerpartID | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetAnnualSplit
**名称**: 获取年度经营项目拆分结果
**Action**: `GetAnnualSplit`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取年度经营项目拆分结果
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| DataType | integer | Y |  |
| BusinessProjectId | integer | Y |  |
| CompactId | integer | Y |  |
| ShopRoyaltyId | string | Y |  |
| BusinessDate | string | Y |  |
| StartDate | string | Y |  |
| EndDate | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetProjectAccountList
**名称**: 获取待结算的项目周期列表
**Action**: `GetProjectAccountList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取待结算的项目周期列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartId | string | Y |  |
| ServerpartShopId | string | Y |  |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| SettlementMode | string | Y |  |
| SettlementType | integer | Y |  |
| SettlementState | string | Y |  |
| PageIndex | integer | Y |  |
| PageSize | integer | Y |  |
| SortStr | string | Y |  |
| SearchKeyName | string | Y |  |
| SearchKeyValue | string | Y |  |
| UserId | integer | Y |  |
| ToDoFirst | boolean | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetProjectAccountTree
**名称**: 获取待结算的项目列表（组织架构模式）
**Action**: `GetProjectAccountTree`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取待结算的项目列表（组织架构模式）
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartId | string | Y | 服务区内码 |
| ServerpartShopId | string | Y | 门店内码 |
| StartDate | string | Y | 统计开始日期 |
| EndDate | string | Y | 统计结束日期 |
| SettlementMode | string | Y | 结算模式 |
| SettlementState | string | Y |  |
| SearchKeyName | string | Y | 模糊查询字段 |
| SearchKeyValue | string | Y | 模糊查询内容 |
| UserId | integer | Y | 用户内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetProjectAccountDetail
**名称**: 获取待结算的项目周期详情数据
**Action**: `GetProjectAccountDetail`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取待结算的项目周期详情数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessApprovalId | integer | Y |  |
| UserId | integer | Y | 用户内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetAccountWarningList
**名称**: 获取门店经营预警列表
**Action**: `GetAccountWarningList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取门店经营预警列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartId | string | Y |  |
| BusinessTrade | string | Y |  |
| Business_Type | string | Y |  |
| SettlementMode | string | Y |  |
| BusinessState | string | Y |  |
| WarningType | string | Y |  |
| ProjectId | string | Y |  |
| ShowMulti | boolean | Y |  |
| ShowNormal | boolean | Y |  |
| Format | integer | Y |  |
| BusinessBrand | string | Y |  |
| MerchantName | string | Y |  |
| ShopName | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/SolidAccountWarningList
**名称**: 生成门店经营预警列表
**Action**: `SolidAccountWarningList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
生成门店经营预警列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartId | string | Y | 服务区内码 |
| ProjectId | string | Y | 经营项目内码 |
| HisProjectStartDate | string | Y |  |
| HisProjectEndDate | string | Y |  |
| CloseDays | integer | Y |  |
| OverRatio | number | Y |  |
| MinCostAmount | number | Y |  |
| MinProfitAmount | number | Y |  |
| ProfitWarning | number | Y |  |
| CloseWaring | number | Y |  |
| RoyaltyWaring | number | Y |  |
| CostRate | number | Y |  |
| LaboursCount | number | Y |  |
| LaboursWage | number | Y |  |
| DepreciationYear | integer | Y |  |
| DepreciationExpense | number | Y |  |
| OtherExpense | number | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetAccountWarningListSummary
**名称**: 获取门店经营预警汇总
**Action**: `GetAccountWarningSummary`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取门店经营预警汇总
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| Business_Type | string | Y |  |
| SettlementMode | string | Y |  |
| BusinessState | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetMerchantSplit
**名称**: 获取经营商户项目拆分结果
**Action**: `GetMerchantSplit`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营商户项目拆分结果
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| MerchantId | string | Y |  |
| ServerpartId | string | Y |  |
| StartDate | string | Y |  |
| EndDate | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/SolidProjectRevenue
**名称**: 固化经营项目月度营收数据（自然日数据）
**Action**: `SolidProjectRevenue`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
固化经营项目月度营收数据（自然日数据）
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StatisticsMonth | string | Y |  |
| ServerpartId | string | Y | 服务区内码 |
| ProjectId | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/SolidPeriodWarningList
**名称**: 生成经营项目周期预警
**Action**: `SolidPeriodWarningList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
生成经营项目周期预警
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| periodwarningList | list<escm.periodwarningmodel> | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/SolidPeriodAnalysis
**名称**: 生成经营项目盈利分析
**Action**: `SolidPeriodAnalysis`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
生成经营项目盈利分析
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| UserId | integer | Y |  |
| ProjectId | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetPeriodWarningList
**名称**: 获取经营项目周期预警列表
**Action**: `GetPeriodWarningList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
获取经营项目周期预警列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartId | string | Y |  |
| ServerpartShopId | string | Y |  |
| DataType | integer | Y |  |
| Business_Type | string | Y |  |
| SettlementMode | string | Y |  |
| PeriodState | integer | Y |  |
| ProfitState | integer | Y |  |
| BusinessState | string | Y |  |
| BusinessTrade | string | Y |  |
| ProjectId | string | Y | 经营项目内码 |
| WarningType | string | Y |  |
| SearchKeyName | string | Y |  |
| SearchKeyValue | string | Y |  |
| ShowNormal | boolean | Y |  |
| ShowSelf | boolean | Y |  |
| BusinessBrand | string | Y |  |
| MerchantName | string | Y |  |
| ShopName | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/ReconfigureProfit
**名称**: 经营项目盈利重分析
**Action**: `ReconfigureProfit`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
经营项目盈利重分析
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProjectId | string | Y | 经营项目内码 |
| BusinessTrade | string | Y | 经营业态 |
| MerchantId | string | Y |  |
| ServerpartId | string | Y | 服务区内码 |
| HisProjectStartDate | string | Y |  |
| HisProjectEndDate | string | Y |  |
| CloseDays | integer | Y |  |
| OverRatio | number | Y |  |
| MinCostAmount | number | Y |  |
| MinProfitAmount | number | Y |  |
| ProfitWarning | number | Y |  |
| CloseWaring | number | Y |  |
| RoyaltyWaring | number | Y |  |
| CostRate | number | Y |  |
| LaboursCount | number | Y |  |
| LaboursWage | number | Y |  |
| DepreciationYear | integer | Y |  |
| DepreciationExpense | number | Y |  |
| OtherExpense | number | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProject/GetWillSettleProject
**名称**: 查询即将结算的年度审批数据
**Action**: `GetWillSettleProject`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
查询即将结算的年度审批数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| ServerpartId | string | Y | 服务区内码 |
| ServerpartShopId | string | Y |  |
| SettlementModes | string | Y |  |
| SettlementType | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProject/UploadRevenueConfirmList
**名称**: 上传退场结算应收拆分数据
**Action**: `UploadRevenueConfirmList`

**场景**: 
用于 BusinessProject 模块相关操作。
**说明**: 
上传退场结算应收拆分数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| revenueconfirmList | list<escm.revenueconfirmmodel> | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |


## 单品销售相关接口【SalesController】

---
### POST /Sales/GetCOMMODITYSALEList
**名称**: 单品销售相关接口
**Action**: `GetCOMMODITYSALEList`

**场景**: 
用于 Sales 模块相关操作。
**说明**: 
单品销售相关接口
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Sales/GetCOMMODITYSALEDetail
**名称**: 获取门店单品汇总表明细
**Action**: `GetCOMMODITYSALEDetail`

**场景**: 
用于 Sales 模块相关操作。
**说明**: 
获取门店单品汇总表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| COMMODITYSALEId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Sales/GetEndaccountSaleInfo
**名称**: 获取账期单品数据
**Action**: `GetEndaccountSaleInfo`

**场景**: 
用于 Sales 模块相关操作。
**说明**: 
获取账期单品数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartCode | string | Y |  |
| ServerpartShopCode | string | Y |  |
| MachineCode | string | Y |  |
| EndaccountDate | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Sales/RecordSaleData
**名称**: 记录单品销售日志
**Action**: `RecordSaleData`

**场景**: 
用于 Sales 模块相关操作。
**说明**: 
记录单品销售日志
#### 请求参数 (Request)
无

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Sales/GetEndaccountError
**名称**: 获取单品销售有差异数据列表
**Action**: `GetEndaccountError`

**场景**: 
用于 Sales 模块相关操作。
**说明**: 
获取单品销售有差异数据列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Sales/UpdateEndaccountError
**名称**: 修正单品销售有差异数据
**Action**: `UpdateEndaccountError`

**场景**: 
用于 Sales 模块相关操作。
**说明**: 
修正单品销售有差异数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ENDACCOUNT_ID | integer | Y |  |
| amountdiffer | number | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |


## 数据校验相关接口【VerificationController】

---
### GET /Verification/GetENDACCOUNTModel
**名称**: 数据校验相关接口
**Action**: `GetENDACCOUNTModel`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
数据校验相关接口
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ENDACCOUNTId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Verification/GetEndaccountList
**名称**: 获取数据校验列表
**Action**: `GetEndaccountList`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
获取数据校验列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartIds | string | Y |  |
| ServerpartCode | string | Y |  |
| ServerpartShopCode | string | Y |  |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| TreatmentMarkState | string | Y |  |
| ExceptionState | string | Y |  |
| EndaccountState | integer | Y |  |
| PageIndex | integer | Y |  |
| PageSize | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Verification/GetEndaccountDetail
**名称**: 获取日结账单明细
**Action**: `GetEndaccountDetail`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
获取日结账单明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| EndaccountId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Verification/VerifyEndaccount
**名称**: 日结数据校验
**Action**: `VerifyEndaccount`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
日结数据校验
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| endaccountDetailModel | escm.endaccountdetailmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Verification/ApproveEndaccount
**名称**: 批量审核日结账期数据
**Action**: `ApproveEndaccountList`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
批量审核日结账期数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| EndaccountIdList | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Verification/SubmitEndaccountState
**名称**: 财务审核/主任复核
**Action**: `SubmitEndaccountState`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
财务审核/主任复核
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| submitEndaccountModel | escm.submitendaccountmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Verification/GetEndaccountHisList
**名称**: 查询历史账期列表
**Action**: `GetEndaccountHisList`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
查询历史账期列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartIds | string | Y |  |
| ServerpartCode | string | Y |  |
| ServerpartShopCode | string | Y |  |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| TreatmentMarkState | string | Y |  |
| ExceptionState | string | Y |  |
| EndaccountState | integer | Y |  |
| PageIndex | integer | Y |  |
| PageSize | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Verification/GetSuppEndaccountList
**名称**: 获取补录账期列表
**Action**: `GetSuppEndaccountList`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
获取补录账期列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartIds | string | Y | 服务区内码集合 |
| ServerpartCode | string | Y | 服务区编码集合 |
| ServerpartShopCode | string | Y | 门店编码 |
| StartDate | string | Y | 查询开始日期 |
| EndDate | string | Y | 查询结束日期 |
| EndaccountState | integer | Y |  |
| PageIndex | integer | Y | 查询页码，默认为1 |
| PageSize | integer | Y | 每页显示数量，默认10 |
| SortStr | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Verification/ApplyEndaccountInvalid
**名称**: 申请日结账期无效操作
**Action**: `ApplyEndaccountInvalid`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
申请日结账期无效操作
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PPModel | escm.permissionproinstmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Verification/CancelEndaccount
**名称**: 将日结账单设置成无效
**Action**: `CancelEndaccount`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
将日结账单设置成无效
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PPModel | escm.permissionproinstmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Verification/GetDataVerificationList
**名称**: 获取服务区日结数据校验汇总列表
**Action**: `GetDataVerificationList`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
获取服务区日结数据校验汇总列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| RoleType | integer | Y |  |
| ProvinceCode | integer | Y |  |
| ServerpartId | string | Y |  |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| Business_Type | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Verification/GetShopEndaccountSum
**名称**: 获取门店日结数据校验汇总数据
**Action**: `GetShopEndaccountSum`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
获取门店日结数据校验汇总数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| RoleType | integer | Y |  |
| ServerpartId | integer | Y | 服务区内码，多个用,隔开 |
| ServerpartShopCode | string | Y |  |
| StartDate | string | Y | 统计开始日期 |
| EndDate | string | Y | 统计结束日期 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Verification/GetEndAccountData
**名称**: 获取日结账期销售明细数据
**Action**: `GetEndAccountData`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
获取日结账期销售明细数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| Data_Type | integer | Y |  |
| Endaccount_ID | integer | Y |  |
| CigaretteType | string | Y |  |
| ReloadType | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Verification/GetCommoditySaleList
**名称**: 获取单品/香烟数据列表
**Action**: `GetCommoditySaleList`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
获取单品/香烟数据列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartCode | string | Y |  |
| ShopCode | string | Y |  |
| MachineCode | string | Y |  |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| CommodityTypeId | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Verification/GetMobilePayDataList
**名称**: 获取移动支付交易记录
**Action**: `GetMobilePayDataList`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
获取移动支付交易记录
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ExceptionType | integer | Y |  |
| ServerpartCode | string | Y | 服务区编码 |
| ShopCode | string | Y | 门店编码 |
| MachineCode | string | Y | 机器编码 |
| StartDate | string | Y | 账期开始时间 |
| EndDate | string | Y | 账期结束时间 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Verification/GetEndaccountSupplement
**名称**: 获取数据校验流水冲正数据
**Action**: `GetEndaccountSupplement`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
获取数据校验流水冲正数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| EndaccountId | integer | Y |  |
| Revenue_Amount | number | Y |  |
| FactAmount_Mobilepayment | number | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Verification/ExceptionHandling
**名称**: 日结账期异常处理
**Action**: `ExceptionHandling`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
日结账期异常处理
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| RollbackModel | escm.endaccountrollbackmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Verification/RebuildDailyAccount
**名称**: 根据销售流水重新生成自然日报表数据
**Action**: `RebuildDailyAccount`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
根据销售流水重新生成自然日报表数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StatisticsDate | string | Y |  |
| ServerpartId | string | Y |  |
| ServerpartShopId | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Verification/CorrectDailyEndaccount
**名称**: 根据销售流水校准自然日报表数据
**Action**: `CorrectDailyEndaccount`

**场景**: 
用于 Verification 模块相关操作。
**说明**: 
根据销售流水校准自然日报表数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StatisticsDate | string | Y | 统计日期 |
| ServerpartId | string | Y | 服务区内码 |
| ServerpartShopId | string | Y | 门店内码 |
| BusinessProjectId | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |


## 营收数据相关接口【RevenueController】

---
### POST /Revenue/GetREVENUEDAILYSPLITList
**名称**: 营收数据相关接口
**Action**: `GetREVENUEDAILYSPLITList`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
营收数据相关接口
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetREVENUEDAILYSPLITDetail
**名称**: 获取服务区日度营收拆分表明细
**Action**: `GetREVENUEDAILYSPLITDetail`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取服务区日度营收拆分表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| REVENUEDAILYSPLITId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Revenue/GetPERSONSELLList
**名称**: 获取收银员交班表列表
**Action**: `GetPERSONSELLList`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取收银员交班表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetPERSONSELLDetail
**名称**: 获取收银员交班表明细
**Action**: `GetPERSONSELLDetail`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取收银员交班表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PERSONSELLId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Revenue/GetBUSINESSANALYSISList
**名称**: 获取经营数据分析表列表
**Action**: `GetBUSINESSANALYSISList`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取经营数据分析表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetBUSINESSANALYSISDetail
**名称**: 获取经营数据分析表明细
**Action**: `GetBUSINESSANALYSISDetail`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取经营数据分析表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BUSINESSANALYSISId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Revenue/GetBRANDANALYSISList
**名称**: 获取AI智能经营品牌分析列表
**Action**: `GetBRANDANALYSISList`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取AI智能经营品牌分析列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetBRANDANALYSISDetail
**名称**: 获取AI智能经营品牌分析明细
**Action**: `GetBRANDANALYSISDetail`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取AI智能经营品牌分析明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BRANDANALYSISId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Revenue/GetSITUATIONANALYSISList
**名称**: 获取AI智能经营情况分析列表
**Action**: `GetSITUATIONANALYSISList`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取AI智能经营情况分析列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetSITUATIONANALYSISDetail
**名称**: 获取AI智能经营情况分析明细
**Action**: `GetSITUATIONANALYSISDetail`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取AI智能经营情况分析明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| SITUATIONANALYSISId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Revenue/GetBUSINESSWARNINGList
**名称**: 获取经营异常预警月度固化数据列表
**Action**: `GetBUSINESSWARNINGList`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取经营异常预警月度固化数据列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetBUSINESSWARNINGDetail
**名称**: 获取经营异常预警月度固化数据明细
**Action**: `GetBUSINESSWARNINGDetail`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取经营异常预警月度固化数据明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BUSINESSWARNINGId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Revenue/GetACCOUNTWARNINGList
**名称**: 获取门店经营预警表列表
**Action**: `GetACCOUNTWARNINGList`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取门店经营预警表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetACCOUNTWARNINGDetail
**名称**: 获取门店经营预警表明细
**Action**: `GetACCOUNTWARNINGDetail`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取门店经营预警表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ACCOUNTWARNINGId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetBusinessDate
**名称**: 获取门店经营开始时间
**Action**: `GetBusinessDate`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取门店经营开始时间
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartIds | string | Y |  |
| ServerpartShopIds | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Revenue/ModifyRevenueDailySplitList
**名称**: 批量更新服务区日度营收拆分表
**Action**: `ModifyRevenueDailySplitList`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
批量更新服务区日度营收拆分表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| revenuedailysplitList | list<escm.revenuedailysplitmodel> | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetRevenuePushList")]
        //[ResponseType(typeof(JsonMsg<ESCom.Model.ServerpartModel>))]
        public IHttpActionResult GetRevenuePushList(string pushProvinceCode, string Statistics_Date)
        {
            try
            {
                //获取服务区营收数据
                DataTable dtRevenuePushList = ESCG.RevenuePush.GetRevenuePushList(transaction, pushProvinceCode, Statistics_Date);

                //生成返回值返回
                return base.Ok(Method.Common.ReturnJson(100, "查询成功", dtRevenuePushList));
            }
            catch (Exception ex)
            {
                SuperMap.RealEstate.Utility.ErrorLogHelper.Write(ex, "接口【GetServerPartBrand】", "");
                transaction.Rollback();
                string msg = "查询失败" + ex.Message;
                return Ok(Method.Common.ReturnJson(999, msg));
            }
        }
        #endregion

        #region 方法 -> 获取历史单品销售数据
        /// <summary>
        /// 获取历史单品销售数据
        /// </summary>
        /// <param name="ProvinceCode">省份编码</param>
        /// <param name="startMonth">开始时间</param>
        /// <param name="endMonth">结束时间</param>
        /// <param name="ServerpartShopIds">门店内码集合</param>
        /// <returns></returns>
        [AcceptVerbs("GET", "POST")]
        [Route("Revenue/GetHisCommoditySaleList")]
        //[ResponseType(typeof(JsonMsg<ESCom.Model.ServerpartModel>))]
        public IHttpActionResult GetHisCommoditySaleList(string ProvinceCode,
            string startMonth, string endMonth, string ServerpartShopIds)
        {
            //根据用户权限获取门店权限
            ServerpartShopIds = GetStringHeader("ServerpartShopIds", ServerpartShopIds);

            string Parameter = "入参信息：省份编码【" + ProvinceCode + "】，门店内码集合【" + ServerpartShopIds + "】，" +
                "查询开始月份【" + startMonth + "】，查询结束月份【" + endMonth + "】";
            try
            {
                //获取服务区营收数据
                DataTable dtHisCommoditySaleList = EShang.Common.Revenue.GetHisCommoditySaleList(
                    transaction, ProvinceCode, startMonth, endMonth, ServerpartShopIds);

                //生成返回值返回
                return base.Ok(Method.Common.ReturnJson(100, "查询成功", dtHisCommoditySaleList));
            }
            catch (Exception ex)
            {
                //事务回滚
                transaction.Rollback();
                LogUtil.WriteLog(null, "查询失败！失败原因：" + ex.Message + "\r\n" + Parameter,
                    DateTime.Now.ToString("yyyyMMdd") + "_GetHisCommoditySaleList");
                return Ok(Method.Common.ReturnJson(999, "查询失败" + ex.Message));
            }
        }
        #endregion

        #region 方法 -> 获取营收数据列表
        /// <summary>
        /// 获取营收数据列表
        /// </summary>
        /// <param name="ServerpartIds">门店内码集合</param>
        /// <param name="ServerpartShopIds">服务区内码集合</param>
        /// <param name="StartDate">查询开始日期</param>
        /// <param name="EndDate">查询结束日期</param>
        /// <param name="DataSourceType">数据模式</param>
        /// <returns></returns>
        [Route("Revenue/GetRevenueDataList
**名称**: 获取营收推送数据表列表
**Action**: `GetRevenueDataList`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取营收推送数据表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartIds | string | Y |  |
| ServerpartShopIds | string | Y |  |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| DataSourceType | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetRevenueReport
**名称**: 获取业主营收统计报表数据
**Action**: `GetRevenueReport`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取业主营收统计报表数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| DataType | integer | Y |  |
| ServerpartIds | string | Y | 门店内码集合 |
| ServerpartShopIds | string | Y | 服务区内码集合 |
| StartDate | string | Y | 查询开始日期 |
| EndDate | string | Y | 查询结束日期 |
| DataSourceType | integer | Y | 数据模式 |
| ShowShop | boolean | Y |  |
| GroupByDaily | boolean | Y |  |
| shopNames | string | Y |  |
| shopTrade | string | Y |  |
| businessType | string | Y |  |
| targetSystem | integer | Y |  |
| SearchKeyName | string | Y |  |
| SearchKeyValue | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetRevenueReportByDate
**名称**: 获取业主营收统计报表数据(按日展示)
**Action**: `GetRevenueReportByDate`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取业主营收统计报表数据(按日展示)
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartIds | string | Y | 服务区内码集合 |
| ServerpartShopIds | string | Y | 门店内码集合 |
| StartDate | string | Y | 统计开始日期 |
| EndDate | string | Y | 统计结束日期 |
| DataSourceType | integer | Y | 数据来源类型，1为日结营收，2为自然日营收 |
| GroupByDaily | boolean | Y | 是否按日做数据分组 |
| shopNames | string | Y | 自营业态 |
| shopTrade | string | Y | 商品业态 |
| businessType | string | Y | 经营模式 |
| targetSystem | integer | Y | 外部系统 1是，0否 |
| SearchKeyName | string | Y |  |
| SearchKeyValue | string | Y | 搜索值 |
| wrapType | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetMerchantRevenueReport
**名称**: 获取商家营收统计报表数据
**Action**: `GetMerchantRevenueReport`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取商家营收统计报表数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| DataType | integer | Y |  |
| ServerpartIds | string | Y | 服务区内码集合 |
| ServerpartShopIds | string | Y | 门店内码集合 |
| StartDate | string | Y | 统计开始日期 |
| EndDate | string | Y | 统计结束日期 |
| DataSourceType | integer | Y | 数据来源类型，1为日结营收，2为自然日营收 |
| GroupByDaily | boolean | Y | 是否按日做数据分组 |
| CalculateStartDate | boolean | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/BankAccountCompare
**名称**: 对比移动支付到账金额差异
**Action**: `BankAccountCompare`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
对比移动支付到账金额差异
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| AccountDate | string | Y |  |
| ServerpartCode | string | Y |  |
| ShopCode | string | Y |  |
| MachineCode | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetBankAccountReport
**名称**: 查询门店移动支付到账报表
**Action**: `GetBankAccountReport`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
查询门店移动支付到账报表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| ServerpartShopIds | string | Y |  |
| Payment_Channel | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetBankAccountList
**名称**: 查询门店移动支付到账数据
**Action**: `GetBankAccountList`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
查询门店移动支付到账数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartDate | string | Y | 查询开始日期 |
| EndDate | string | Y | 查询结束日期 |
| ServerpartShopIds | string | Y | 服务区内码集合 |
| Payment_Channel | string | Y | 移动支付渠道<br/>枚举：MOBILEPAYOPERATORS |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetCurTotalRevenue
**名称**: 获取实时营收汇总数据
**Action**: `GetCurTotalRevenue`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取实时营收汇总数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartIds | string | Y |  |
| ServerpartShopIds | string | Y | 服务区内码集合 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetTotalRevenue
**名称**: 获取营收汇总数据
**Action**: `GetTotalRevenue`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取营收汇总数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartIds | string | Y | 门店内码集合 |
| ServerpartShopIds | string | Y | 服务区内码集合 |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| DataSourceType | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Revenue/GetYSSellMasterList
**名称**: 获取交易流水订单表列表
**Action**: `GetYSSellMasterList`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取交易流水订单表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Revenue/GetSellMasterCompareList
**名称**: 获取客无忧交易和收银交易流水订单比较列表
**Action**: `GetSellMasterCompareList`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取客无忧交易和收银交易流水订单比较列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| serverpartShopIds | string | Y |  |
| startDate | string | Y |  |
| endDate | string | Y |  |
| isNew | boolean | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Revenue/GetYSSellDetailsList
**名称**: 获取交易流水明细表列表
**Action**: `GetYSSellDetailsList`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取交易流水明细表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetTransactionCustomer")]
        [ResponseType(typeof(Models.JsonMsg<ESCM.TransactionCustomerModel>))]
        public IHttpActionResult GetTransactionCustomer(string ServerpartIds, string startDate, string endDate,
            string shopNames = "", string shopTrade = "", string businessType = "", int? targetSystem = null, string SearchKeyName = "", string SearchKeyValue = "")
        {
            //根据用户权限获取门店权限
            //ServerpartIds = GetStringHeader("ServerpartShopIds", ServerpartIds);

            string Parameter = "入参信息： 开始时间【" + startDate + "】，结束时间【" + endDate + "】，" +
                "门店内码集合【" + ServerpartIds + "】，商品业态【" + shopTrade + "】，" +
                "经营模式【" + businessType + "】" +
                "外部系统【" + targetSystem + "】" +
                "自营业态【" + shopNames + "】"
                ;

            try
            {
                //获取服务区营收数据
                List<ESCM.NestingModel<ESCM.TransactionCustomerModel>> CommoditySaleSummary = ESCG.RevenueHelper.GetTransactionCustomer(
                    transaction, ServerpartIds, startDate, endDate, shopNames, shopTrade, businessType, targetSystem, SearchKeyName, SearchKeyValue);

                int TotalCount = CommoditySaleSummary.Count;
                //转化json形式
                Models.JsonList<ESCM.NestingModel<ESCM.TransactionCustomerModel>> jsonList =
                    Models.JsonList<ESCM.NestingModel<ESCM.TransactionCustomerModel>>.Success(CommoditySaleSummary, TotalCount, 1, TotalCount);

                return Ok(Models.JsonMsg<Models.JsonList<ESCM.NestingModel<ESCM.TransactionCustomerModel>>>.Success(jsonList, 100, "查询成功"));
            }
            catch (Exception ex)
            {
                //事务回滚
                transaction.Rollback();
                LogUtil.WriteLog(null, "查询失败！失败原因：" + ex.Message + "\r\n" + Parameter,
                    DateTime.Now.ToString("yyyyMMdd") + "_GetTransactionCustomer");
                return Ok(Method.Common.ReturnJson(999, "查询失败" + ex.Message));
            }
        }

        /// <summary>
        /// 获取客单交易分析(按日展示)
        /// </summary>
        /// <param name="ServerpartIds">服务区内码集合</param>
        /// <param name="startDate">开始时间</param>
        /// <param name="endDate">结束时间</param>
        /// <param name="shopNames">自营业态</param>
        /// <param name="shopTrade">商品业态</param>
        /// <param name="businessType">经营模式</param>
        /// <param name="targetSystem">外部系统 1是，0否</param>
        /// <param name="SearchKeyName">搜索项，【 MerchantName 商户，Brand 品牌 ，Shop 门店 Serverpart，服务区 】，多个用 , 连接 例如 MerchantName,Brand,Shop,Serverpart</param>
        /// <param name="SearchKeyValue">搜索值</param>
        /// <param name="wrapType">外部包裹类型，0 没有， 1 片区服务区层级 </param>
        /// <returns></returns>
        [AcceptVerbs("GET")]
        [Route("Revenue/GetTransactionCustomerByDate")]
        [ResponseType(typeof(Models.JsonMsg<ESCM.TransactionCustomerModel>))]
        public IHttpActionResult GetTransactionCustomerByDate(string ServerpartIds, string startDate, string endDate,
            string shopNames = "", string shopTrade = "", string businessType = "", int? targetSystem = null, string SearchKeyName = "", string SearchKeyValue = "", int wrapType = 0)
        {
            //根据用户权限获取门店权限
            //ServerpartIds = GetStringHeader("ServerpartShopIds", ServerpartIds);

            string Parameter = "入参信息： 开始时间【" + startDate + "】，结束时间【" + endDate + "】，" +
                "门店内码集合【" + ServerpartIds + "】，商品业态【" + shopTrade + "】，" +
                "经营模式【" + businessType + "】" +
                "外部系统【" + targetSystem + "】" +
                "自营业态【" + shopNames + "】"
                ;

            try
            {
                //获取服务区营收数据
                List<ESCM.NestingModel<ESCM.TransactionCustomerModel>> CommoditySaleSummary = ESCG.RevenueHelper.GetTransactionCustomerByDate(
                    transaction, ServerpartIds, startDate, endDate, shopNames, shopTrade, businessType, targetSystem, SearchKeyName, SearchKeyValue, wrapType);

                int TotalCount = CommoditySaleSummary.Count;
                //转化json形式
                Models.JsonList<ESCM.NestingModel<ESCM.TransactionCustomerModel>> jsonList =
                    Models.JsonList<ESCM.NestingModel<ESCM.TransactionCustomerModel>>.Success(CommoditySaleSummary, TotalCount, 1, TotalCount);

                return Ok(Models.JsonMsg<Models.JsonList<ESCM.NestingModel<ESCM.TransactionCustomerModel>>>.Success(jsonList, 100, "查询成功"));
            }
            catch (Exception ex)
            {
                //事务回滚
                transaction.Rollback();
                LogUtil.WriteLog(null, "查询失败！失败原因：" + ex.Message + "\r\n" + Parameter,
                    DateTime.Now.ToString("yyyyMMdd") + "_GetTransactionCustomerByDate");
                return Ok(Method.Common.ReturnJson(999, "查询失败" + ex.Message));
            }
        }

        #endregion

        #region 方法 -> 获取同环比分析表

        /// <summary>
        /// 获取同环比分析表
        /// </summary>
        /// <param name="ShowShop"> true 代表 门店， false 代表服务区</param>
        /// <param name="ServerpartIds">服务区内码集合</param>
        /// <param name="startDate">开始时间</param>
        /// <param name="endDate">结束时间</param>
        /// <param name="shopNames">自营业态</param>
        /// <param name="shopTrade">商品业态</param>
        /// <param name="businessType">经营模式</param>
        /// <param name="targetSystem">外部系统 1是，0否</param>
        /// <param name="SearchKeyName">搜索项，【 MerchantName 商户，Brand 品牌 ，Shop 门店 Serverpart，服务区 】，多个用 , 连接 例如 MerchantName,Brand,Shop,Serverpart</param>
        /// <param name="SearchKeyValue">搜索值</param>
        /// <returns></returns>
        [AcceptVerbs("GET")]
        [Route("Revenue/GetRevenueYOYQOQ")]
        [ResponseType(typeof(Models.JsonMsg<ESCM.RevenueYOYQOQModel>))]
        public IHttpActionResult GetRevenueYOYQOQ(string ServerpartIds, string startDate, string endDate, bool ShowShop = true,
            string shopNames = "", string shopTrade = "", string businessType = "", int? targetSystem = null, string SearchKeyName = "", string SearchKeyValue = "")
        {
            //根据用户权限获取门店权限
            //ServerpartIds = GetStringHeader("ServerpartShopIds", ServerpartIds);

            string Parameter = "入参信息： 开始时间【" + startDate + "】，结束时间【" + endDate + "】，" +
                "门店内码集合【" + ServerpartIds + "】" +
                "经营模式【" + businessType + "】"
                ;

            try
            {
                //获取服务区营收数据
                List<ESCM.NestingModel<ESCM.RevenueYOYQOQModel>> result = ESCG.RevenueHelper.GetRevenueYOYQOQ(
                    transaction, ServerpartIds, startDate, endDate, ShowShop, shopNames, shopTrade, businessType, targetSystem, SearchKeyName, SearchKeyValue);

                int TotalCount = result.Count;

                //转化json形式
                Models.JsonList<ESCM.NestingModel<ESCM.RevenueYOYQOQModel>> jsonList =
                    Models.JsonList<ESCM.NestingModel<ESCM.RevenueYOYQOQModel>>.Success(result, TotalCount, 1, TotalCount);

                return Ok(Models.JsonMsg<Models.JsonList<ESCM.NestingModel<ESCM.RevenueYOYQOQModel>>>.Success(jsonList, 100, "查询成功"));
            }
            catch (Exception ex)
            {
                //事务回滚
                transaction.Rollback();
                LogUtil.WriteLog(null, "查询失败！失败原因：" + ex.Message + "\r\n" + Parameter,
                    DateTime.Now.ToString("yyyyMMdd") + "_GetRevenueYOYQOQ");
                return Ok(Method.Common.ReturnJson(999, "查询失败" + ex.Message));
            }
        }

        /// <summary>
        /// 获取同环比分析表(按日展示)
        /// </summary>
        /// <param name="ServerpartIds">服务区内码集合</param>
        /// <param name="startDate">开始时间</param>
        /// <param name="endDate">结束时间</param>
        /// <param name="shopNames">自营业态</param>
        /// <param name="shopTrade">商品业态</param>
        /// <param name="businessType">经营模式</param>
        /// <param name="targetSystem">外部系统 1是，0否</param>
        /// <param name="SearchKeyName">搜索项，【 MerchantName 商户，Brand 品牌 ，Shop 门店 Serverpart，服务区 】，多个用 , 连接 例如 MerchantName,Brand,Shop,Serverpart</param>
        /// <param name="SearchKeyValue">搜索值</param>
        /// <param name="wrapType">外部包裹类型，0 没有， 1 片区服务区层级 </param>
        /// <param name="ServerpartShopId">门店内码</param>
        /// <returns></returns>
        [AcceptVerbs("GET")]
        [Route("Revenue/GetRevenueYOYQOQByDate")]
        [ResponseType(typeof(Models.JsonMsg<ESCM.RevenueYOYQOQModel>))]
        public IHttpActionResult GetRevenueYOYQOQByDate(string ServerpartIds, string startDate, string endDate,
            string shopNames = "", string shopTrade = "", string businessType = "", int? targetSystem = null, string SearchKeyName = "", string SearchKeyValue = "", int wrapType = 0, string ServerpartShopId = "")
        {
            //根据用户权限获取门店权限
            //ServerpartIds = GetStringHeader("ServerpartShopIds", ServerpartIds);

            string Parameter = "入参信息： 开始时间【" + startDate + "】，结束时间【" + endDate + "】，" +
                "门店内码集合【" + ServerpartIds + "】" +
                "经营模式【" + businessType + "】"
                ;

            try
            {
                //获取服务区营收数据
                List<ESCM.NestingModel<ESCM.RevenueYOYQOQModel>> result = ESCG.RevenueHelper.GetRevenueYOYQOQByDate(
                    transaction, ServerpartIds, startDate, endDate, shopNames, shopTrade, businessType, targetSystem, SearchKeyName, SearchKeyValue, wrapType, ServerpartShopId);

                int TotalCount = result.Count;

                //转化json形式
                Models.JsonList<ESCM.NestingModel<ESCM.RevenueYOYQOQModel>> jsonList =
                    Models.JsonList<ESCM.NestingModel<ESCM.RevenueYOYQOQModel>>.Success(result, TotalCount, 1, TotalCount);

                return Ok(Models.JsonMsg<Models.JsonList<ESCM.NestingModel<ESCM.RevenueYOYQOQModel>>>.Success(jsonList, 100, "查询成功"));
            }
            catch (Exception ex)
            {
                //事务回滚
                transaction.Rollback();
                LogUtil.WriteLog(null, "查询失败！失败原因：" + ex.Message + "\r\n" + Parameter,
                    DateTime.Now.ToString("yyyyMMdd") + "_GetRevenueYOYQOQByDate");
                return Ok(Method.Common.ReturnJson(999, "查询失败" + ex.Message));
            }
        }

        #endregion

        #region 方法 -> 获取销售环比分析

        /// <summary>
        /// 获取销售环比分析
        /// </summary>
        /// <param name="ShowShop"> true 代表 门店， false 代表服务区</param>
        /// <param name="SELECTTYPE">1 实收金额,2 销售数量,3 客单数量</param>
        /// <param name="ServerpartIds">服务区内码集合</param>
        /// <param name="startDate">开始时间</param>
        /// <param name="endDate">结束时间</param>
        /// <param name="MOMstartDate">上期统计开始日期</param>
        /// <param name="MOMendDate">上期统计结束日期</param>
        /// <param name="shopNames">自营业态</param>
        /// <param name="shopTrade">商品业态</param>
        /// <param name="businessType">经营模式</param>
        /// <param name="targetSystem">外部系统 1是，0否</param>
        /// <param name="SearchKeyName">搜索项，【 MerchantName 商户，Brand 品牌 ，Shop 门店 Serverpart，服务区 】，多个用 , 连接 例如 MerchantName,Brand,Shop,Serverpart</param>
        /// <param name="SearchKeyValue">搜索值</param>
        /// <returns></returns>
        [AcceptVerbs("GET")]
        [Route("Revenue/GetRevenueQOQ")]
        [ResponseType(typeof(Models.JsonMsg<ESCM.RevenueQOQModel>))]
        public IHttpActionResult GetRevenueQOQ(string ServerpartIds, string startDate, string endDate, string MOMstartDate,
            string MOMendDate, int SELECTTYPE = 1, bool ShowShop = true, string shopNames = "", string shopTrade = "",
            string businessType = "", int? targetSystem = null, string SearchKeyName = "", string SearchKeyValue = "")
        {
            //根据用户权限获取门店权限
            //ServerpartIds = GetStringHeader("ServerpartShopIds", ServerpartIds);

            string Parameter = "入参信息： 开始时间【" + startDate + "】，结束时间【" + endDate + "】，" +
                "门店内码集合【" + ServerpartIds + "】，商品业态【" + shopTrade + "】，" +
                "经营模式【" + businessType + "】"
                ;

            try
            {
                //获取服务区营收数据
                List<ESCM.NestingModel<ESCM.RevenueQOQModel>> result = ESCG.RevenueHelper.GetRevenueQOQ(
                    transaction, ServerpartIds, startDate, endDate, MOMstartDate, MOMendDate, SELECTTYPE, ShowShop,
                    shopNames, shopTrade, businessType, targetSystem, SearchKeyName, SearchKeyValue);

                int TotalCount = result.Count;

                //转化json形式
                Models.JsonList<ESCM.NestingModel<ESCM.RevenueQOQModel>> jsonList =
                    Models.JsonList<ESCM.NestingModel<ESCM.RevenueQOQModel>>.Success(result, TotalCount, 1, TotalCount);

                return Ok(Models.JsonMsg<Models.JsonList<ESCM.NestingModel<ESCM.RevenueQOQModel>>>.Success(jsonList, 100, "查询成功"));
            }
            catch (Exception ex)
            {
                //事务回滚
                transaction.Rollback();
                LogUtil.WriteLog(null, "查询失败！失败原因：" + ex.Message + "\r\n" + Parameter,
                    DateTime.Now.ToString("yyyyMMdd") + "_GetRevenueQOQ");
                return Ok(Method.Common.ReturnJson(999, "查询失败" + ex.Message));
            }
        }

        /// <summary>
        /// 获取销售环比分析(按日展示)
        /// </summary>
        /// <param name="SELECTTYPE">1 实收金额,2 销售数量,3 客单数量</param>
        /// <param name="ServerpartIds">服务区内码集合</param>
        /// <param name="startDate">开始时间</param>
        /// <param name="endDate">结束时间</param>
        /// <param name="MOMstartDate">上期统计开始日期</param>
        /// <param name="MOMendDate">上期统计结束日期</param>
        /// <param name="shopNames">自营业态</param>
        /// <param name="shopTrade">商品业态</param>
        /// <param name="businessType">经营模式</param>
        /// <param name="targetSystem">外部系统 1是，0否</param>
        /// <param name="SearchKeyName">搜索项，【 MerchantName 商户，Brand 品牌 ，Shop 门店 Serverpart，服务区 】，多个用 , 连接 例如 MerchantName,Brand,Shop,Serverpart</param>
        /// <param name="SearchKeyValue">搜索值</param>
        /// <param name="wrapType">外部包裹类型，0 没有， 1 片区服务区层级 </param>
        /// <returns></returns>
        [AcceptVerbs("GET")]
        [Route("Revenue/GetRevenueQOQByDate")]
        [ResponseType(typeof(Models.JsonMsg<ESCM.RevenueQOQModel>))]
        public IHttpActionResult GetRevenueQOQByDate(string ServerpartIds, string startDate, string endDate, string MOMstartDate,
            string MOMendDate, int SELECTTYPE = 1, string shopNames = "", string shopTrade = "", string businessType = "",
            int? targetSystem = null, string SearchKeyName = "", string SearchKeyValue = "", int wrapType = 0)
        {
            //根据用户权限获取门店权限
            //ServerpartIds = GetStringHeader("ServerpartShopIds", ServerpartIds);

            string Parameter = "入参信息： 开始时间【" + startDate + "】，结束时间【" + endDate + "】，" +
                "门店内码集合【" + ServerpartIds + "】，商品业态【" + shopTrade + "】，" +
                "经营模式【" + businessType + "】"
                ;

            try
            {
                //获取服务区营收数据
                List<ESCM.NestingModel<ESCM.RevenueQOQModel>> result = ESCG.RevenueHelper.GetRevenueQOQByDate(
                    transaction, ServerpartIds, startDate, endDate, MOMstartDate, MOMendDate, SELECTTYPE, shopNames,
                    shopTrade, businessType, targetSystem, SearchKeyName, SearchKeyValue, wrapType);

                int TotalCount = result.Count;

                //转化json形式
                Models.JsonList<ESCM.NestingModel<ESCM.RevenueQOQModel>> jsonList =
                    Models.JsonList<ESCM.NestingModel<ESCM.RevenueQOQModel>>.Success(result, TotalCount, 1, TotalCount);

                return Ok(Models.JsonMsg<Models.JsonList<ESCM.NestingModel<ESCM.RevenueQOQModel>>>.Success(jsonList, 100, "查询成功"));
            }
            catch (Exception ex)
            {
                //事务回滚
                transaction.Rollback();
                LogUtil.WriteLog(null, "查询失败！失败原因：" + ex.Message + "\r\n" + Parameter,
                    DateTime.Now.ToString("yyyyMMdd") + "_GetRevenueQOQByDate");
                return Ok(Method.Common.ReturnJson(999, "查询失败" + ex.Message));
            }
        }

        #endregion

        #region 方法 -> 获取月度营收差异分析
        /// <summary>
        /// 获取月度营收差异分析
        /// </summary>
        /// <param name="serverpartId">服务区ID（416）单个</param>
        /// <param name="serverpartShopIds">指定的门店ID（3068,3069）</param>
        /// <param name="startMonth">开始月份（2023-3-1）</param>
        /// <param name="endMonth">结束月份（2024-2-1）</param>
        /// <param name="compareMonth">环比月份（2023-01）</param>
        /// <returns></returns>
        [AcceptVerbs("GET")]
        [Route("Revenue/GetMonthCompare")]
        [ResponseType(typeof(Models.JsonMsg<ESCM.MonthCompareModel>))]
        public IHttpActionResult GetMonthCompare(string serverpartId, string startMonth, string endMonth, string compareMonth, string serverpartShopIds = "")
        {
            //根据用户权限获取门店权限
            serverpartShopIds = GetStringHeader("ServerpartShopIds", serverpartShopIds);

            string Parameter = "入参信息： 开始时间【" + startMonth + "】，结束时间【" + endMonth + "】，" +
                "服务区Id【" + serverpartId + "】，比较月份【" + compareMonth + "】，"
                ;

            try
            {
                //获取服务区营收数据
                List<ESCM.MonthCompareModel> result = ESCG.RevenueHelper.GetMonthCompare(
                    transaction, serverpartId, serverpartShopIds, startMonth, endMonth, compareMonth);

                int TotalCount = result.Count;

                //转化json形式
                Models.JsonList<ESCM.MonthCompareModel> jsonList = Models.JsonList<ESCM.MonthCompareModel>.Success(
                    result, TotalCount, 1, TotalCount);

                return Ok(Models.JsonMsg<Models.JsonList<ESCM.MonthCompareModel>>.Success(jsonList, 100, "查询成功"));
            }
            catch (Exception ex)
            {
                //事务回滚
                transaction.Rollback();
                LogUtil.WriteLog(null, "查询失败！失败原因：" + ex.Message + "\r\n" + Parameter,
                    DateTime.Now.ToString("yyyyMMdd") + "_GetMonthCompare");
                return Ok(Method.Common.ReturnJson(999, "查询失败" + ex.Message));
            }
        }
        #endregion

        #region 方法 -> 获取智慧招商分析报表
        /// <summary>
        /// 获取智慧招商分析报表
        /// </summary>
        /// <param name="ContainHoliday">
        /// 是否计算节日：<br/>
        /// 0【全部】<br/>
        /// 1【节假日】<br/>
        /// 2【非节假日】
        /// </param>
        /// <param name="ServerpartId">服务区内码</param>
        /// <param name="ServerpartType">服务区类型</param>
        /// <param name="BusinessTrade">经营业态</param>
        /// <param name="BusinessTradeType">
        /// 经营业态大类：<br/>
        /// 1：自营便利店<br/>
        /// 2：自营餐饮客房<br/>
        /// 3：商铺租赁
        /// </param>
        /// <param name="StartMonth">统计开始月份，格式yyyyMM</param>
        /// <param name="EndMonth">统计结束月份，格式yyyyMM</param>
        /// <param name="DueStartDate">合同到期开始日期</param>
        /// <param name="DueEndDate">合同到期结束日期</param>
        /// <param name="SearchKeyName">
        /// 模糊查询字段<br/>
        /// 多个字段用,隔开<br/>
        /// 例如：REVENUE_AMOUNT,SERVERPART_AVGFLOW
        /// </param>
        /// <param name="SearchKeyValue">
        /// 模糊查询内容<br/>
        /// 多个字段用,隔开<br/>
        /// 区间值用|隔开<br/>
        /// 例如：2|,2|4
        /// </param>
        /// <returns></returns>
        [AcceptVerbs("GET")]
        [Route("Revenue/GetBusinessAnalysisReport")]
        [ResponseType(typeof(Models.JsonMsg<Models.JsonList<ESCM.BUSINESSANALYSISModel>>))]
        public IHttpActionResult GetBusinessAnalysisReport(string ServerpartId, int ContainHoliday = 0, string ServerpartType = "",
            string BusinessTrade = "", string BusinessTradeType = "", string StartMonth = "", string EndMonth = "",
            string DueStartDate = "", string DueEndDate = "", string SearchKeyName = "", string SearchKeyValue = "")
        {
            string Parameter = "入参信息： 服务区内码【" + ServerpartType + "】，服务区类型【" + ServerpartType + "】，" +
                "经营业态【" + BusinessTrade + "】，统计开始月份【" + StartMonth + "】，统计结束月份【" + EndMonth + "】，" +
                "合同到期开始日期【" + DueStartDate + "】，合同到期结束日期【" + DueEndDate + "】，" +
                "模糊查询字段【" + SearchKeyName + "】，模糊查询内容【" + SearchKeyValue + "】";

            try
            {
                List<ESCM.BUSINESSANALYSISModel> result = ESCG.BUSINESSANALYSISHelper.GetBusinessAnalysisReport(
                    transaction, ServerpartId, ServerpartType, BusinessTrade, BusinessTradeType, StartMonth, EndMonth,
                    DueStartDate, DueEndDate, SearchKeyName, SearchKeyValue, ContainHoliday);

                Models.JsonList<ESCM.BUSINESSANALYSISModel> jsonList = Models.JsonList<ESCM.BUSINESSANALYSISModel>.Success(
                    result, result.Count, 1, result.Count);

                return Ok(Models.JsonMsg<Models.JsonList<ESCM.BUSINESSANALYSISModel>>.Success(jsonList, 100, "查询成功"));
            }
            catch (Exception ex)
            {
                transaction.Rollback();
                LogUtil.WriteLog(null, "查询失败！失败原因：" + ex.Message + "\r\n" + Parameter,
                    DateTime.Now.ToString("yyyyMMdd") + "_GetBusinessAnalysisReport");
                return Ok(Method.Common.ReturnJson(999, "查询失败" + ex.Message));
            }
        }
        #endregion

        #region 方法 -> 分析服务区的经营情况
        /// <summary>
        /// 分析服务区的经营情况
        /// </summary>
        /// <param name="ServerpartId">服务区内码ID</param>
        /// <returns></returns>
        [Route("Revenue/GetSituationAnalysis
**名称**: 获取客单交易分析
**Action**: `GetSituationAnalysis`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取客单交易分析
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartId | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetBusinessTradeAnalysis
**名称**: 分析此业态在驿达服务区的经营情况
**Action**: `GetBusinessTradeAnalysis`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
分析此业态在驿达服务区的经营情况
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartId | string | Y | 服务区内码ID |
| ServerpartShopId | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetBrandAnalysis
**名称**: 分析此品牌在驿达旗下的经营情况
**Action**: `GetBrandAnalysis`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
分析此品牌在驿达旗下的经营情况
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartId | string | Y | 服务区内码ID |
| ServerpartShopId | string | Y | 门店内码集合 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetMonthINCAnalysis
**名称**: 月度服务区门店营收对比固化数据
**Action**: `GetMonthINCAnalysis`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
月度服务区门店营收对比固化数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StatisticsStartMonth | string | Y |  |
| StatisticsEndMonth | string | Y |  |
| ServerpartId | string | Y | 服务区内码ID |
| ServerpartShopIds | string | Y |  |
| DataType | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetRevenueReportByBIZPSPLITMONTH
**名称**: 月度服务区门店营收对比分析详情
**Action**: `GetRevenueDPCompare`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
月度服务区门店营收对比分析详情
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| SHOPROYALTY_ID | integer | Y |  |
| BUSINESSPROJECT_ID | integer | Y |  |
| ACCOUNT_TYPE | integer | Y |  |
| SERVERPARTSHOP_ID | string | Y |  |
| DataSourceType | integer | Y |  |
| SERVERPART_ID | string | Y |  |
| STATISTICS_MONTH | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Revenue/CorrectShopCigarette
**名称**: 重新生成日度营收拆分香烟数据
**Action**: `CorrectShopCigarette`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
重新生成日度营收拆分香烟数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartShopId | string | Y |  |
| StartDate | string | Y | 开始日期 |
| EndDate | string | Y | 结束日期 |
| UserName | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetCigaretteReport
**名称**: 获取香烟报表数据
**Action**: `GetCigaretteReport`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取香烟报表数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| DataSourceType | integer | Y |  |
| StartDate | string | Y | 统计开始日期 |
| EndDate | string | Y | 统计结束日期 |
| ServerpartIds | string | Y |  |
| ServerpartShopIds | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Revenue/GetBusinessItemSummary
**名称**: 获取安徽驿达月度营收分析
**Action**: `GetBusinessItemSummary`

**场景**: 
用于 Revenue 模块相关操作。
**说明**: 
获取安徽驿达月度营收分析
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| DataType | integer | Y |  |
| ProvinceCode | string | Y |  |
| ServerpartId | string | Y |  |
| StartDate | string | Y | 开始日期 |
| EndDate | string | Y | 结束日期 |
| CompareStartDate | string | Y |  |
| CompareEndDate | string | Y |  |
| AccStartDate | string | Y |  |
| AccEndDate | string | Y |  |
| AccCompareStartDate | string | Y |  |
| AccCompareEndDate | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |


## 凭证相关接口【PictureController】

---
### GET /Picture/GetPictureList
**名称**: 凭证相关接口
**Action**: `GetPictureList`

**场景**: 
用于 Picture 模块相关操作。
**说明**: 
凭证相关接口
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| TableId | integer | Y |  |
| TableName | string | Y |  |
| TableType | string | Y |  |
| ImageType | string | Y |  |
| ImageIndex | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Picture/UploadPicture
**名称**: 上传图片信息（文件格式传输）
        /// 入参数据：
        /// TableId【数据表内码】
        /// TableName【数据表名称】
        /// TableType【数据表类型】
        /// ImageName【图片名称】
**Action**: `UploadPicture`

**场景**: 
用于 Picture 模块相关操作。
**说明**: 
上传图片信息（文件格式传输）
        /// 入参数据：
        /// TableId【数据表内码】
        /// TableName【数据表名称】
        /// TableType【数据表类型】
        /// ImageName【图片名称】
#### 请求参数 (Request)
无

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Picture/GetEndaccountEvidence
**名称**: 获取日结账单凭据
**Action**: `GetEndaccountEvidence`

**场景**: 
用于 Picture 模块相关操作。
**说明**: 
获取日结账单凭据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| EndaccountId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Picture/UploadEndaccountEvidence
**名称**: 上传日结账单凭据
        /// 入参数据：
        /// EndaccountId【日结账单内码】
        /// ImageInfo【图片base64位码】
**Action**: `UploadEndaccountEvidence`

**场景**: 
用于 Picture 模块相关操作。
**说明**: 
上传日结账单凭据
        /// 入参数据：
        /// EndaccountId【日结账单内码】
        /// ImageInfo【图片base64位码】
#### 请求参数 (Request)
无

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Picture/GetAuditEvidence
**名称**: 获取稽核数据凭据
**Action**: `GetAuditEvidence`

**场景**: 
用于 Picture 模块相关操作。
**说明**: 
获取稽核数据凭据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| AuditId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Picture/UploadAuditEvidence
**名称**: 上传稽核数据凭据
        /// 入参数据：
        /// AuditId【稽核内码】
        /// ImageInfo【图片base64位码】
**Action**: `UploadAuditEvidence`

**场景**: 
用于 Picture 模块相关操作。
**说明**: 
上传稽核数据凭据
        /// 入参数据：
        /// AuditId【稽核内码】
        /// ImageInfo【图片base64位码】
#### 请求参数 (Request)
无

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetATTACHMENTList
**名称**: 附件上传相关接口
**Action**: `GetATTACHMENTList`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
附件上传相关接口
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| FinanceProinstId | integer | Y |  |
| DataType | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetATTACHMENTDetail
**名称**: 获取附件上传明细
**Action**: `GetATTACHMENTDetail`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取附件上传明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ATTACHMENTId | integer | Y |  |
| DataType | integer | Y | 数据类型：0【RUNNING】，1【STORAGE】 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetProjectSplitSummary
**名称**: 获取月度营收分润数据
**Action**: `GetProjectSplitSummary`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取月度营收分润数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| SPRegionTypeId | string | Y |  |
| ServerpartId | string | Y |  |
| MerchantId | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetProjectSummary
**名称**: 获取服务区营收分润数据
**Action**: `GetProjectSummary`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取服务区营收分润数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartDate | string | Y | 统计开始日期 |
| EndDate | string | Y | 统计结束日期 |
| SPRegionTypeId | string | Y | 片区内码 |
| ServerpartId | string | Y | 服务区内码 |
| MerchantId | string | Y | 商户内码 |
| BusinessType | string | Y |  |
| SettlementModes | string | Y |  |
| CompactType | string | Y |  |
| ShowOwnerDif | boolean | Y |  |
| ShowSubDif | boolean | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetRevenueSplitSummary
**名称**: 获取服务区营收分润报表（四川）
**Action**: `GetRevenueSplitSummary`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取服务区营收分润报表（四川）
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartDate | string | Y | 统计开始日期 |
| EndDate | string | Y | 统计结束日期 |
| SPRegionTypeId | string | Y | 片区内码 |
| ServerpartId | string | Y | 服务区内码 |
| MerchantId | string | Y | 商户内码 |
| BusinessType | string | Y | 经营模式 |
| SettlementModes | string | Y | 结算模式 |
| CompactType | string | Y | 合同类型 |
| ServerpartShopId | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetProjectMerchantSummary
**名称**: 获取经营商户营收分润数据
**Action**: `GetProjectMerchantSummary`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取经营商户营收分润数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartDate | string | Y | 统计开始日期 |
| EndDate | string | Y | 统计结束日期 |
| SPRegionTypeId | string | Y | 片区内码 |
| ServerpartId | string | Y | 服务区内码 |
| MerchantId | string | Y | 商户内码 |
| BusinessType | string | Y | 经营模式 |
| SettlementModes | string | Y | 结算模式 |
| CompactType | string | Y | 合同类型 |
| ShowOwnerDif | boolean | Y |  |
| ShowSubDif | boolean | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/CreateSingleProjectSplit
**名称**: 生成单个门店/合同/项目应收拆分数据
**Action**: `CreateSingleProjectSplit`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
生成单个门店/合同/项目应收拆分数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartDate | string | Y | 统计开始日期 |
| EndDate | string | Y | 统计结束日期 |
| ServerpartShopId | string | Y |  |
| CompactId | string | Y |  |
| ProjectId | string | Y |  |
| OutBusinessType | string | Y |  |
| BusinessStartDate | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/SolidMonthProjectSplit
**名称**: 重新生成月度应收拆分固化数据
**Action**: `SolidMonthProjectSplit`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
重新生成月度应收拆分固化数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StatisticsMonth | string | Y |  |
| ServerpartShopId | string | Y | 门店内码 |
| CompactId | string | Y | 经营合同内码 |
| ProjectId | string | Y | 经营项目内码 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetRoyaltyDateSumReport
**名称**: 获取日度业主到账汇总数据(一级日期汇总)
**Action**: `GetRoyaltyDateSumReport`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取日度业主到账汇总数据(一级日期汇总)
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| ServerpartIds | string | Y |  |
| ServerpartShopIds | string | Y |  |
| CompareSplit | boolean | Y |  |
| KeyWord | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetRoyaltyReport
**名称**: 获取日度业主到账汇总数据
**Action**: `GetRoyaltyReport`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取日度业主到账汇总数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartDate | string | Y | 统计开始日期 |
| EndDate | string | Y | 统计结束日期 |
| ServerpartIds | string | Y | 服务区内码集合 |
| ServerpartShopIds | string | Y | 门店内码集合 |
| CompareSplit | boolean | Y | 是否对比经营项目拆分数据 |
| KeyWord | string | Y | 搜索经营商户 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetProjectShopIncome
**名称**: 获取日度业主到账汇总数据
**Action**: `GetProjectShopIncome`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取日度业主到账汇总数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StatisticsDate | string | Y |  |
| ContrastDate | string | Y |  |
| ServerpartIds | string | Y | 服务区内码集合 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetContractMerchant
**名称**: 获取合同商户信息
**Action**: `GetContractMerchant`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取合同商户信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartIds | string | Y | 服务区内码(520,521) |
| SETTLEMENT_MODES | string | Y |  |
| startDate | string | Y |  |
| endDate | string | Y |  |
| keyword | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetAccountReached
**名称**: 获取分账收银到账
**Action**: `GetAccountReached`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取分账收银到账
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartIds | string | Y | 服务区内码(520,521) |
| SETTLEMENT_MODES | string | Y | 结算模式 |
| startDate | string | Y | 开始时间 |
| endDate | string | Y | 结束时间 |
| keyword | string | Y | 搜索经营商户 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetShopExpense
**名称**: 获取分账收银扣费明细
**Action**: `GetShopExpense`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取分账收银扣费明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartIds | string | Y | 服务区内码(520,521) |
| SETTLEMENT_MODES | string | Y | 结算模式 |
| startDate | string | Y | 月份 |
| endDate | string | Y | 月份 |
| keyword | string | Y | 搜索经营商户 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetReconciliation
**名称**: 获取合作商户月对账
**Action**: `GetReconciliation`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取合作商户月对账
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BUSINESSPROJECT_ID | integer | Y |  |
| SHOPROYALTY_ID | string | Y |  |
| START_MONTH | string | Y |  |
| END_MONTH | string | Y |  |
| StaffId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetRevenueRecognition
**名称**: 获取分账收银收入确认
**Action**: `GetRevenueRecognition`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取分账收银收入确认
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartIds | string | Y |  |
| startDate | string | Y |  |
| endDate | string | Y |  |
| SETTLEMENT_MODES | string | Y |  |
| BusinessProjectId | integer | Y |  |
| ShopRoyaltyId | string | Y |  |
| keyword | string | Y |  |
| SolidType | boolean | Y |  |
| ShowHisProject | boolean | Y |  |
| ShowSelf | boolean | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetProjectPeriodIncome
**名称**: 获取经营项目分账收银收入
**Action**: `GetProjectPeriodIncome`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取经营项目分账收银收入
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessProjectId | integer | Y | 经营项目内码 |
| StatisticsMonth | string | Y |  |
| StatisticsMonthStart | string | Y |  |
| ShopRoyaltyId | string | Y | 应收拆分内码 |
| MobilePayCorrect | number | Y |  |
| CashPayCorrect | number | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetProjectPeriodAccount
**名称**: 查询经营周期结算明细
**Action**: `GetProjectPeriodAccount`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
查询经营周期结算明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BUSINESSPROJECT_ID | integer | Y |  |
| SHOPROYALTY_ID | string | Y |  |
| BUSINESSAPPROVAL_ID | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Finance/ApplyAccountProinst
**名称**: 发起商户年度结算审批
**Action**: `ApplyAccountProinst`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
发起商户年度结算审批
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| applyAccountProinstModel | escm.applyaccountproinstmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/ApproveAccountProinst
**名称**: 提交/审批商户对账
**Action**: `ApproveAccountProinst`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
提交/审批商户对账
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| businessApprovalID | integer | Y |  |
| curProinstState | integer | Y |  |
| approveedInfo | string | Y |  |
| approveedStaffId | integer | Y |  |
| approveedStaffName | string | Y |  |
| nextId | integer | Y |  |
| nextState | integer | Y |  |
| SourcePlatform | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/RejectAccountProinst
**名称**: 驳回商户对账审批业务
**Action**: `RejectAccountProinst`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
驳回商户对账审批业务
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| businessApprovalID | integer | Y | 业务流程内码 |
| approveedStaffId | integer | Y | 审核人账号内码 |
| approveedStaffName | string | Y | 审核人员 |
| approveedInfo | string | Y | 审核意见 |
| targetProinstState | integer | Y |  |
| rejectType | integer | Y |  |
| endReject | boolean | Y |  |
| SourcePlatform | string | Y | 审批平台 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Finance/GetMonthAccountProinst
**名称**: 获取经营项目月度结算审批列表
**Action**: `GetMonthAccountProinst`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取经营项目月度结算审批列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Finance/ApplyMonthAccountProinst
**名称**: 发起经营项目月度结算审批（处理移动支付和现金差异）
**Action**: `ApplyMonthAccountProinst`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
发起经营项目月度结算审批（处理移动支付和现金差异）
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| applyAccountProinstModel | escm.applyaccountproinstmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/ApproveMonthAccountProinst
**名称**: 提交/审批经营项目月度结算流程
**Action**: `ApproveMonthAccountProinst`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
提交/审批经营项目月度结算流程
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| businessApprovalID | integer | Y |  |
| curProinstState | integer | Y |  |
| approveedInfo | string | Y |  |
| approveedStaffId | integer | Y |  |
| approveedStaffName | string | Y |  |
| nextId | integer | Y |  |
| nextState | integer | Y |  |
| SourcePlatform | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/ApproveMAPList
**名称**: 批量审批经营项目月度结算流程
**Action**: `ApproveMAPList`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
批量审批经营项目月度结算流程
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| businessApprovalID | string | Y | 业务流程内码 |
| curProinstState | integer | Y | 当前环节状态 |
| approveedInfo | string | Y | 审核意见 |
| approveedStaffId | integer | Y | 审核人账号内码 |
| approveedStaffName | string | Y | 审核人员 |
| nextId | integer | Y | 指定下一个人 |
| SourcePlatform | string | Y | 审批平台 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/RejectMonthAccountProinst
**名称**: 驳回经营项目月度结算流程
**Action**: `RejectMonthAccountProinst`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
驳回经营项目月度结算流程
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| businessApprovalID | integer | Y | 业务流程内码 |
| approveedStaffId | integer | Y | 审核人账号内码 |
| approveedStaffName | string | Y | 审核人员 |
| approveedInfo | string | Y | 审核意见 |
| targetProinstState | integer | Y |  |
| rejectType | integer | Y |  |
| endReject | boolean | Y |  |
| SourcePlatform | string | Y | 审批平台 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Finance/StorageMonthProjectAccount
**名称**: 固化月度分账收银收入数据
**Action**: `StorageMonthProjectAccount`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
固化月度分账收银收入数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProjectSplitList | list<escm.nestingmodel<escm.revenuerecognitionmodel>> | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetMonthAccountDiff
**名称**: 对比分账收银收入累计营业额差异
**Action**: `GetMonthAccountDiff`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
对比分账收银收入累计营业额差异
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartId | string | Y |  |
| StatisticsMonth | string | Y |  |
| ShowDiff | boolean | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/ApprovePeriodAccount
**名称**: 生成经营项目月度结算审批数据
**Action**: `ApprovePeriodAccount`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
生成经营项目月度结算审批数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProjectId | integer | Y |  |
| ShopRoyaltyId | string | Y |  |
| StartMonth | string | Y |  |
| EndMonth | string | Y |  |
| UserId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/RejectPeriodAccount
**名称**: 批量驳回经营项目月度结算审批数据（年度结算时处理）
**Action**: `RejectPeriodAccount`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
批量驳回经营项目月度结算审批数据（年度结算时处理）
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ProjectId | integer | Y | 经营项目内码 |
| ShopRoyaltyId | string | Y | 应收拆分内码 |
| StartMonth | string | Y | 开始月份 |
| EndMonth | string | Y | 结束月份 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetPeriodSupplementList
**名称**: 获取经营项目年度日结冲正记录
**Action**: `GetPeriodSupplementList`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取经营项目年度日结冲正记录
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessProjectId | integer | Y |  |
| ShopRoyaltyId | string | Y | 应收拆分内码 |
| ServerpartShopId | string | Y |  |
| StartDate | string | Y |  |
| EndDate | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetProjectExpenseList
**名称**: 获取经营商户费用列表
**Action**: `GetProjectExpenseList`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取经营商户费用列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessProjectId | integer | Y | 经营项目内码 |
| ShopRoyaltyId | string | Y | 项目拆分内码 |
| StartMonth | string | Y |  |
| EndMonth | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetBankAccountAnalyseList
**名称**: 获取银行到账拆解明细表（导出Excel）
**Action**: `GetBankAccountAnalyseList`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取银行到账拆解明细表（导出Excel）
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchMonth | string | Y |  |
| ServerpartIds | string | Y |  |
| ServerpartShopIds | string | Y |  |
| KeyWord | string | Y |  |
| SolidType | boolean | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetBankAccountAnalyseTreeList
**名称**: 获取银行到账拆解明细--树形列表（页面展示）
**Action**: `GetBankAccountAnalyseTreeList`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取银行到账拆解明细--树形列表（页面展示）
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchMonth | string | Y | 查询统计年月，格式yyyyMM 或 yyyy-MM-dd |
| ServerpartIds | string | Y | 服务区内码集合 |
| ServerpartShopIds | string | Y | 门店内码集合 |
| KeyWord | string | Y | 搜索经营商户 |
| SolidType | boolean | Y | 是否查询固化数据 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Finance/SolidBankAccountSplit
**名称**: 固化银行到账拆解明细表
**Action**: `SolidBankAccountSplit`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
固化银行到账拆解明细表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| accountList | list<escm.bankaccountanalysedetailmodel> | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetContractExcuteAnalysis
**名称**: 合作商户合同执行情况一览表
**Action**: `GetContractExcuteAnalysis`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
合作商户合同执行情况一览表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartIds | string | Y |  |
| StatisticsMonth | string | Y |  |
| Settlement_Modes | string | Y |  |
| keyword | string | Y |  |
| SolidType | boolean | Y |  |
| ShowProjectNode | boolean | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/RebuildSCSplit
**名称**: 重新生成自营提成项目应收拆分数据
**Action**: `RebuildSCSplit`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
重新生成自营提成项目应收拆分数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartDate | string | Y |  |
| EndDate | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Finance/CorrectRevenueAccountData
**名称**: 更正分账收银收入差异数据
**Action**: `CorrectRevenueAccountData`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
更正分账收银收入差异数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| correctAccountParamModel | escm.correctaccountparammodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Finance/RebuildClosedPeriod
**名称**: 生成撤场经营周期结算数据
**Action**: `RebuildClosedPeriod`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
生成撤场经营周期结算数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| projectPeriodModel | escm.reconciliationmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Finance/RebuildReductionPeriod
**名称**: 生成经营周期免租情况结算数据
**Action**: `RebuildReductionPeriod`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
生成经营周期免租情况结算数据
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| projectPeriodModel | escm.reconciliationmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/SendSMSMessage
**名称**: 发送业务审批短信提醒
**Action**: `GetSMSIdentityCode`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
发送业务审批短信提醒
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PhoneNumber | string | Y |  |
| UserName | string | Y |  |
| ProcessCount | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/LadingBill
**名称**: 合同期结算流程提单
**Action**: `LadingBill`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
合同期结算流程提单
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| businessApprovalID | integer | Y |  |
| approveedInfo | string | Y |  |
| approveedStaffId | integer | Y |  |
| approveedStaffName | string | Y |  |
| SourcePlatform | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/RejectLadingBill
**名称**: 驳回合同期结算流程提单
**Action**: `RejectLadingBill`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
驳回合同期结算流程提单
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| businessApprovalID | integer | Y | 业务流程内码 |
| approveedStaffId | integer | Y | 审核人账号内码 |
| approveedStaffName | string | Y | 审核人员 |
| approveedInfo | string | Y | 审核意见 |
| SourcePlatform | string | Y | 审批平台 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Finance/GetAHJKtoken
**名称**: 获取安徽交控token
**Action**: `GetAHJKtoken`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取安徽交控token
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| tokenModel | escm.tokenmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetAccountCompare
**名称**: 获取经营数据对比分析表
**Action**: `GetAccountCompare`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取经营数据对比分析表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartDate | string | Y |  |
| EndDate | string | Y |  |
| ServerpartId | string | Y |  |
| CompareStartDate | string | Y |  |
| CompareEndDate | string | Y |  |
| CompareYear | integer | Y |  |
| BusinessType | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Finance/GetAnnualAccountList
**名称**: 获取年度结算汇总表
**Action**: `GetAnnualAccountList`

**场景**: 
用于 Finance 模块相关操作。
**说明**: 
获取年度结算汇总表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StatisticsYear | integer | Y |  |
| ServerpartId | string | Y | 服务区内码 |
| ServerpartShopId | string | Y |  |
| SettlementModes | string | Y |  |
| SettlementState | string | Y |  |
| SettlementType | string | Y |  |
| StartDate | string | Y | 统计开始日期 |
| EndDate | string | Y | 统计结束日期 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |


## 票据相关接口【InvoiceController】

---
### POST /Invoice/GetBILLList
**名称**: 票据相关接口
**Action**: `GetBILLList`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
票据相关接口
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Invoice/GetBILLDetail
**名称**: 获取票据信息表明细
**Action**: `GetBILLDetail`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
获取票据信息表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BILLId | integer | Y |  |
| BillNo | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Invoice/GetBILLDETAILList
**名称**: 获取发票明细表列表
**Action**: `GetBILLDETAILList`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
获取发票明细表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /Invoice/GetBILLDETAILDetail
**名称**: 获取发票明细表明细
**Action**: `GetBILLDETAILDetail`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
获取发票明细表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BILLDETAILId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Invoice/GetINVOICEINFOList
**名称**: 获取客户开票信息表列表
**Action**: `GetINVOICEINFOList`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
获取客户开票信息表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了： |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Invoice/GetINVOICEINFODetail
**名称**: 获取客户开票信息表明细
**Action**: `GetINVOICEINFODetail`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
获取客户开票信息表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：查询条件对象 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Invoice/GetGOODSTAXINFOList
**名称**: 获取商品税务信息列表
**Action**: `GetGOODSTAXINFOList`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
获取商品税务信息列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：客户开票信息表内码【INVOICEINFOId】 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Invoice/GetGOODSTAXINFODetail
**名称**: 获取商品税务信息明细
**Action**: `GetGOODSTAXINFODetail`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
获取商品税务信息明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：查询条件对象 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Office/GetAPPLYAPPROVEList
**名称**: 获取报销审核列表
**Action**: `GetAPPLYAPPROVEList`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
获取报销审核列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：商品税务信息内码【GOODSTAXINFOId】 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Office/GetAPPLYAPPROVEDetail
**名称**: 获取报销审核明细
**Action**: `GetAPPLYAPPROVEDetail`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
获取报销审核明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了：查询条件对象 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Invoice/WriteBackInvoice
**名称**: 回写票据开票结果信息
**Action**: `WriteBackInvoice`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
回写票据开票结果信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| writeBackInvoiceModel | escm.writebackinvoicemodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Invoice/SendHXInvoiceInfo
**名称**: 发送开票信息至航行开票系统
**Action**: `SendHXInvoiceInfo`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
发送开票信息至航行开票系统
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| InvoiceList | list<escm.hxinvoicemodel> | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Invoice/RewriteJDPJInfo
**名称**: 回写金蝶开票结果信息
**Action**: `RewriteJDPJInfo`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
回写金蝶开票结果信息
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| rewriteJDPJModel | escm.rewritejdpjmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /Invoice/ForwardJDPJInterface
**名称**: 金蝶开票/红冲申请（接口转发）
**Action**: `ForwardJDPJInterface`

**场景**: 
用于 Invoice 模块相关操作。
**说明**: 
金蝶开票/红冲申请（接口转发）
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| jDPJModel | escm.jdpjreqmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |


## 业务审批相关接口【BusinessProcessController】

---
### POST /BusinessProcess/GetBUSINESSAPPROVALList
**名称**: 业务审批相关接口
**Action**: `GetBUSINESSAPPROVALList`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
业务审批相关接口
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProcess/GetBUSINESSAPPROVALDetail
**名称**: 获取业务审批记录表明细
**Action**: `GetBUSINESSAPPROVALDetail`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
获取业务审批记录表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BUSINESSAPPROVALId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/GetAPPROVALROUTEList
**名称**: 获取业务审批记录环节表列表
**Action**: `GetAPPROVALROUTEList`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
获取业务审批记录环节表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProcess/GetAPPROVALROUTEDetail
**名称**: 获取业务审批记录环节表明细
**Action**: `GetAPPROVALROUTEDetail`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
获取业务审批记录环节表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| APPROVALROUTEId | integer | Y |  |
| OperationType | integer | Y |  |
| CurState | integer | Y |  |
| IsValid | integer | Y |  |
| ShowApprovalUser | boolean | Y |  |
| ServerpartIds | string | Y |  |
| ShopIds | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/GetAPPLYAPPROVEList
**名称**: 获取审批意见列表
**Action**: `GetAPPLYAPPROVEList`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
获取审批意见列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProcess/GetAPPLYAPPROVEDetail
**名称**: 获取审批意见明细
**Action**: `GetAPPLYAPPROVEDetail`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
获取审批意见明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| APPLYAPPROVEId | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/GetBusinessProcessList
**名称**: 获取业务审批列表
**Action**: `GetBusinessProcessList`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
获取业务审批列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProcess/GetBusinessProcessDetail
**名称**: 获取业务审批详情
**Action**: `GetBusinessProcessDetail`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
获取业务审批详情
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessProcessID | integer | Y |  |
| AcceptCode | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/GetHIGHWAYPROINSTList
**名称**: 获取项目实例表列表
**Action**: `GetHIGHWAYPROINSTList`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
获取项目实例表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/GetACTINSTOPINIONList
**名称**: 获取项目审批意见列表
**Action**: `GetACTINSTOPINIONList`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
获取项目审批意见列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y | 查询条件对象 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/GetProinstCommodityList
**名称**: 获取商品申请流程商品列表
**Action**: `GetProinstCommodityList`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
获取商品申请流程商品列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y | 查询条件对象 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProcess/GetPermissionApplyDetailList
**名称**: 获取权限审批流程明细列表
**Action**: `GetPermissionApplyDetailList`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
获取权限审批流程明细列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PermissionApplyId | integer | Y |  |
| PermissionApplyType | integer | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/CreateProInst
**名称**: 提交商家商品申请业务
**Action**: `CreateProInst`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
提交商家商品申请业务
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| commodityProinstModel | escm.commodityproinstmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/RegisterUserApply
**名称**: 注册驿商云平台新用户
**Action**: `RegisterUserApply`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
注册驿商云平台新用户
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PPModel | escm.permissionproinstmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/CreateMerchantApply
**名称**: 创建商家权限申请业务
**Action**: `CreateMerchantApply`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
创建商家权限申请业务
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PPModel | escm.permissionproinstmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/ApprovedMerchantApply
**名称**: 审批商家权限申请业务
**Action**: `ApprovedMerchantApply`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
审批商家权限申请业务
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PPModel | escm.permissionproinstmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/RejectPermissionApply
**名称**: 驳回权限申请业务
**Action**: `RejectPermissionApply`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
驳回权限申请业务
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| PPModel | escm.permissionproinstmodel | Y | 权限申请model |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProcess/GetBUSINESSAPPROVALS
**名称**: 根据【业务审批记录环节表】来取【业务审批记录表】里的记录
**Action**: `GetBUSINESSAPPROVALS`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
根据【业务审批记录环节表】来取【业务审批记录表】里的记录
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| STAFF_ID | integer | Y |  |
| PageIndex | integer | Y |  |
| PageSize | integer | Y |  |
| OPERATION_TYPE | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessProcess/GetApprovalReport
**名称**: 获取经营项目月度/年度结算审批各环节待审批数量
**Action**: `GetApprovalReport`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
获取经营项目月度/年度结算审批各环节待审批数量
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| StartMonth | string | Y |  |
| EndMonth | string | Y |  |
| ServerpartId | string | Y |  |
| ServerpartShopId | string | Y |  |
| SettlementMode | string | Y |  |
| SearchKeyName | string | Y |  |
| SearchKeyValue | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/CreateCommodityProInst
**名称**: 创建服务区商品审批流程
**Action**: `CreateCommodityProInst`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
创建服务区商品审批流程
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了： |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/ReapplyCommodityProInst
**名称**: 重新发起商品审批流程
**Action**: `ReapplyCommodityProInst`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
重新发起商品审批流程
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了： |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/ApproveCommodityProInst
**名称**: 审核服务区商品审批流程
**Action**: `ApproveCommodityProInst`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
审核服务区商品审批流程
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了： |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessProcess/RejectCommodityProInst
**名称**: 驳回服务区商品审批流程
**Action**: `RejectCommodityProInst`

**场景**: 
用于 BusinessProcess 模块相关操作。
**说明**: 
> ⚠️ **加密要求**: 该接口入参需进行 AES 加密转换。
驳回服务区商品审批流程
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| postData | CommonModel | Y | 加密后的请求对象。包含了：加密后的请求对象。包含了： |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessLog/GetBUSINESSLOGList
**名称**: 业务办理日志表相关接口
**Action**: `GetBUSINESSLOGList`

**场景**: 
用于 BusinessLog 模块相关操作。
**说明**: 
业务办理日志表相关接口
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| searchModel | SearchModel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessLog/GetBusinessLogList
**名称**: 获取业务办理日志表列表
**Action**: `GetBusinessLogList`

**场景**: 
用于 BusinessLog 模块相关操作。
**说明**: 
获取业务办理日志表列表
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| ServerpartCode | string | Y |  |
| ShopCode | string | Y |  |
| MachineCode | string | Y |  |
| BusinessLogType | string | Y |  |
| CheckState | string | Y |  |
| ReloadData | boolean | Y |  |
| PageIndex | integer | Y |  |
| PageSize | integer | Y |  |
| StartDate | number | Y |  |
| EndDate | number | Y |  |
| DataType | integer | Y |  |
| SortStr | string | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### GET /BusinessLog/GetBusinessLogDetail
**名称**: 获取业务办理日志表明细
**Action**: `GetBusinessLogDetail`

**场景**: 
用于 BusinessLog 模块相关操作。
**说明**: 
获取业务办理日志表明细
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessLogId | integer | Y |  |
| DataType | integer | Y | 数据类型：<br/>1【正式数据】<br/>2【历史数据】 |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessLog/RecordBusinessLog
**名称**: 记录业务办理日志
**Action**: `RecordBusinessLog`

**场景**: 
用于 BusinessLog 模块相关操作。
**说明**: 
记录业务办理日志
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| BusinessLogType | integer | Y |  |
| BusinessID | integer | Y |  |
| TableName | string | Y |  |
| OwnerName | string | Y |  |
| BusinessLogContent | string | Y |  |
| Data_Consistency | integer | Y |  |
| Check_State | integer | Y |  |
| ServerpartCode | string | Y |  |
| ShopCode | string | Y |  |
| MachineCode | string | Y |  |
| Statistics_Date | long? | Y |  |
| Daily_Amount | number | Y |  |
| Channel_Amount | number | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |

---
### POST /BusinessLog/UpdateBusinessLogState
**名称**: 更新业务办理日志表处理状态
**Action**: `UpdateBusinessLogState`

**场景**: 
用于 BusinessLog 模块相关操作。
**说明**: 
更新业务办理日志表处理状态
#### 请求参数 (Request)
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| businessLogModel | escm.businesslogmodel | Y |  |

#### 返回参数 (Response)
| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| Result_Code | int | 状态码 |
| Result_Desc | string | 消息 |
| Result_Data | object | 返回数据 |
