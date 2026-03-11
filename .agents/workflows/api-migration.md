---
description: C# API 接口平移到 Python FastAPI 的标准工作流
---

# API 接口平移工作流

## 前置信息
- **C# 源码路径**: `D:\CSharp\Project\000_通用版本\000_通用版本\030_EShangApi\CommercialApi`
- **Python 项目路径**: `D:\Projects\Python\eshang_api`
- **数据库**: Oracle（通过 oracledb 连接）

## 平移步骤（每个接口必须按此流程执行）

### Step 1: 查阅C#源码
// turbo
1. 在 C# Controllers 目录中找到对应的 Controller 文件
2. 找到目标接口的 `[Route("xxx")]` 定义
3. 确认调用的 Helper 方法（如 `BayonetHelper.GetXxx`）
4. 查阅 Helper 方法中的完整 SQL 查询和业务逻辑
5. 记录关键信息：
   - SQL 语句（表名、字段、JOIN、WHERE 条件）
   - 入参到 SQL 的映射
   - 返回数据结构（Model 字段）
   - 特殊逻辑（分组、排序、计算）

### Step 2: Python 实现
1. 在对应的 Python router 文件中找到占位符/代理接口
2. 替换为直接 SQL 查询实现：
   - 使用 `db.execute_query(sql, params)` 执行查询
   - 使用 Oracle 绑定参数（`:param_name` 格式）
   - 处理日期格式转换
   - 实现内存聚合/排序逻辑
3. 将 docstring 标注为 `(SQL平移完成)`
4. 移除 `logger.warning("xxx 暂未完整实现")` 或 `proxy_to_old_api` 调用

### Step 3: 验证
// turbo
1. 检查 Python 服务是否正常启动（无语法错误）
2. 如有运行错误，立即修复

### 注意事项
- Oracle 表名和字段名需要用双引号包裹
- 日期格式统一使用 `yyyyMMdd` 数字格式
- 9天阈值：历史数据切换 `T_ENDACCOUNT` vs `T_ENDACCOUNT_TEMP`
- Province_Code `340000` 对应安徽
- 安徽驿达特有逻辑: SELLER_ID -2846(驿佳), -2802(百和)
- 车流数据仅安徽(340000)有，其他省份直接返回空
