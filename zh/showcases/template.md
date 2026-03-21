# [用例名称]

**分类:** [每日自动化 / 内容 / 基础设施 / 开发]
**示例模型:** [高级 / 均衡 / 便宜等级 - 使用你拥有的]
**更新时间:** [YYYY-MM-DD]

> **如何使用此模板:** 将下面的代码块复制到你的 OpenClaw 配置。将 `[YOUR_LOCATION]` 之类的括号占位符替换为你的实际值。"快速开始"部分包含你需要运行的所有内容。

## 快速开始

### 1. 前置条件(先检查这些)

- [ ] [工具 1] 已配置
- [ ] [工具 2] API 密钥在 `~/.openclaw/credentials/`
- [ ] [外部服务] 账户

### 2. 复制此定时任务

粘贴到你的网关配置的 `cron.jobs` 部分:

```json
{
  "name": "[use-case-name]",
  "schedule": {
    "kind": "cron",
    "expr": "[minute] [hour] * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "[PROMPT_TEXT]"
  },
  "sessionTarget": "isolated"
}
```

**替换:**
- `[use-case-name]` - 你的任务名称 (例如, "daily-brief")
- `[minute] [hour]` - 何时运行 (例如, "30 9" 表示 UTC 上午 9:30)
- `[PROMPT_TEXT]` - 下面第 3 部分的提示词

### 3. 复制此提示词

```
[在此处粘贴完整提示词]

示例:
Generate a daily brief for me.

1. WEATHER: Get current weather for [YOUR_LOCATION]
2. CALENDAR: Check calendar for next 24 hours
3. TASKS: Get active tasks from [YOUR_TASK_SYSTEM]

Format as a clean, scannable message.
```

**替换:**
- `[YOUR_LOCATION]` - 你的城市 (例如, "New York, NY")
- `[YOUR_TASK_SYSTEM]` - 你的任务管理器

### 4. 配置工具

确保这些工具对你的代理可用:

```yaml
# 在你的网关配置中
tools:
  weather: {}  # 或你的天气提供商
  calendar: {}  # 或你的日历提供商
  message: {}   # Telegram, Discord 等
```

### 5. 测试

首先手动运行:
```bash
openclaw cron run [use-case-name]
```

---

## 功能说明

**问题:** [关于痛点的一句话]

**解决方案:** [关于此自动化功能的一句话]

## 完整提示词

带有所有详情的完整提示词:

```
[粘贴包含所有部分、错误处理等的完整提示词]
```

## 配置参考

### Cron 表达式示例

| 计划 | 表达式 |
|----------|------------|
| 每天 UTC 上午 9:30 | `30 9 * * *` |
| 周日上午 8 点 | `0 8 * * 0` |
| 每 6 小时 | `0 */6 * * *` |
| 工作日上午 10 点 | `0 10 * * 1-5` |

### 模型选择

| 任务类型 | 推荐模型 | 原因 |
|-----------|-------------------|-----|
| 简单格式化 | Haiku / Flash-Lite | 快速、便宜 |
| 通用任务 | Sonnet / Gemini 2.5 | 良好平衡 |
| 复杂推理 | Opus / GPT-5.2 | 最佳质量 |

### 工具替代方案

| 功能 | 选项 A | 选项 B | 选项 C |
|----------|----------|----------|----------|
| 天气 | 内置 | OpenWeatherMap | NOAA |
| 日历 | Google Calendar | Nextcloud | CalDAV |
| 任务 | Todoist | Trello | 基于文件 |
| 交付 | Telegram | Discord | 电子邮件 |

## 定制指南

### 更改计划

编辑定时任务中的 `expr` 字段:
- `30 9 * * *` = 每天上午 9:30
- `0 */6 * * *` = 每 6 小时
- `0 8 * * 1` = 周一上午 8 点(每周)

### 更改交付渠道

**改为 Telegram:**
```json
{
  "message": "[your prompt] Deliver results to Telegram chat [YOUR_CHAT_ID]."
}
```

**改为 Discord:**
```json
{
  "message": "[your prompt] Deliver results to Discord channel [CHANNEL_ID]."
}
```

**改为电子邮件:**
```json
{
  "message": "[your prompt] Email results to [YOUR_EMAIL]."
}
```

### 添加新数据源

添加到提示词:
```
4. NEW_SECTION: [要检查的内容]
   - [详情 1]
   - [详情 2]
```

## 故障排除

| 问题 | 可能原因 | 修复 |
|---------|--------------|-----|
| 任务未运行 | 时区不匹配 | 检查 `tz` 字段是否与你的时区匹配 |
| 缺少数据 | 工具未配置 | 验证工具在网关配置中 |
| 输出错误 | 提示词不清楚 | 使提示词更具体 |
| 被限流 | 太频繁 | 增加运行之间的间隔 |

## 经验教训

### 有效的方法

- [有效的技术]

### 无效的方法

- [你放弃的方法]

### 要注意的注意事项

- [限流、时间问题等]

## 安全说明

部署前请审查这些:

- [ ] 提示词中没有硬编码的密钥
- [ ] API 密钥在 `~/.openclaw/credentials/` 中而不是在配置中
- [ ] 敏感命令需要确认 (如果适用)
- [ ] 输出不泄露个人数据

## 变体

**替代方法 1:** [简要描述]

**替代方法 2:** [简要描述]

## 相关链接

- [相关展示 1 的链接]
- [相关展示 2 的链接]

## 更新日志

- **[YYYY-MM-DD]** - 初始版本，作者 [作者]
- **[YYYY-MM-DD]** - [更改描述]

---

**提交你自己的:** 复制此模板，填写，并提交 PR。关注使其即复即用，并带有清晰的 `[占位符]`。
