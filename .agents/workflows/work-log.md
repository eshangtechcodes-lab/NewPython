---
description: 每次会话结束时自动保存工作日志到 workLog 目录
---

# 工作日志 Workflow

## 触发时机
- 会话结束前
- 用户主动要求保存日志
- 完成较大功能模块后

## 日志目录
- **固定路径**：`D:\AISpace\EShangPython\workLog\`
- **文件命名**：`YYYYMMDD-NN.md`（如 `20260313-01.md`、`20260313-02.md`）
- 同一天多个会话递增序号，检查已有文件确定下一个序号

## 日志模板

```markdown
# YYYYMMDD-NN 工作日志 — [一句话标题]

## 📋 工作内容
- 逐项列出完成的工作，每项包含目标、修改方式、结果

## 📂 相关材料
| 类型 | 路径 |
|------|------|
| 主文件 | `path/to/file` |
| 分支 | `feature/xxx` → merged |

## 🔧 修改内容
- 具体文件修改和行数变化
- Git commit 列表（hash + 说明）

## ⚠️ 踩坑记录
- 遇到的问题（现象 → 原因 → 解决方案）

## 📊 验证结果
- 测试通过率、关键指标

## 📝 总结
- 整体评价、经验教训

## 🔜 下一步工作
- [ ] 待办事项
```

## 操作步骤

// turbo-all

1. 检查 `git status`，确保所有改动已提交
2. `git log --oneline` 收集本次会话的 commit 信息
3. 检查 `workLog/` 目录中当天已有几个文件，确定序号（如已有 01 则用 02）
4. 按模板格式生成工作日志，写入 `workLog/YYYYMMDD-NN.md`
5. `git add workLog/ && git commit -m "chore: 保存工作日志 YYYYMMDD-NN"`
