# 日常摘要

**类别:** 日常自动化
**示例模型:** 平衡版 (Sonnet、Gemini Flash 等)
**更新时间:** 2026-02-09

> **使用方法:** 将下面的 cron 任务和提示词复制到你的 OpenClaw 配置中。用实际值替换 `[PLACEHOLDERS]`。用 `openclaw cron run daily-brief` 测试。

## 快速开始

### 1. 前置条件

- [ ] 天气工具已配置（内置，无需 API 密钥）
- [ ] 日历访问权限（Google Calendar、Nextcloud 或 CalDAV）
- [ ] 有 API 的任务管理器（Todoist、Trello 或基于文件）
- [ ] 已配置交付渠道（Telegram 机器人、Discord 或电子邮件）

### 2. 复制此 Cron 任务

粘贴到你的网关配置的 `cron.jobs` 部分：

```json
{
  "name": "daily-brief",
  "schedule": {
    "kind": "cron",
    "expr": "30 9 * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Generate a daily brief. 1) Get weather for [YOUR_CITY]. 2) Check calendar for next 24 hours. 3) Get active tasks from [YOUR_TASK_SYSTEM]. 4) Check for stalled tasks >24h. Format as clean, scannable message with clear headers. Deliver to [YOUR_CHANNEL]."
  },
  "sessionTarget": "isolated"
}
```

**替换:**
- `[YOUR_CITY]` - 你的位置（例如 "New York, NY"）
- `[YOUR_TASK_SYSTEM]` - 你的任务管理器（例如 "Todoist"、"Trello"）
- `[YOUR_CHANNEL]` - 交付位置（例如 "Telegram chat [CHAT_ID]" 或 "Discord channel [CHANNEL_ID]"）

### 3. 配置工具

添加到你的网关配置：

```yaml
tools:
  weather: {}
  calendar: {}  # or your specific calendar tool
  message: {}   # Telegram, Discord, or email
```

### 4. 测试

```bash
openclaw cron run daily-brief
```

---

## 功能说明

**问题:** 开始一天需要检查多个应用：天气、日历、任务。容易遗漏重要的事情。

**解决方案:** 自动晨间摘要，在 UTC 上午 9:30 通过你的首选渠道交付。将天气、日历事件（接下来 24 小时）、活跃任务和提醒合并为一条易扫描的消息。

## 完整提示词（详细版）

如果你想要更多格式控制，使用此版本：

```
生成我的日常摘要。

1. 天气：获取 [YOUR_CITY] 的当前天气
   - 当前温度和状况
   - 今天的高温/低温
   - 任何警告或显著情况

2. 日历：检查接下来 24 小时的日历
   - 列出所有事件及时间
   - 突出在 2 小时内开始的事件
   - 注记任何全天事件

3. 任务：从 [YOUR_TASK_SYSTEM] 获取活跃任务
   - 列出前 3-5 个优先项目
   - 注记任何标记为等待的任务

4. 提醒：检查是否有需要注意的事项
   - 滞后 >24 小时的任务
   - 即将截止的期限

格式为清晰、易扫描的消息，带有清晰的标题。
跳过没有值得注意内容的部分。
保持简洁，以便在 30 秒内阅读。

交付到 [YOUR_CHANNEL]。
```

## 配置选项

### 交付渠道

**Telegram（最受欢迎）:**
```
Deliver to Telegram chat [CHAT_ID].
```
从 @userinfobot 获取聊天 ID。

**Discord:**
```
Deliver to Discord channel [CHANNEL_ID].
```
在 Discord 中启用开发者模式，右键单击频道，"复制 ID"。

**电子邮件:**
```
Email results to [YOUR_EMAIL] with subject "Daily Brief [DATE]".
```

**Slack:**
```
Deliver to Slack channel [CHANNEL_NAME] via webhook.
```

### 日历选项

**Google Calendar (gcalcli):**
```bash
# 安装
pip install gcalcli

# 认证
gcalcli list
```

**Nextcloud (khal + vdirsyncer):**
```bash
# 安装
pip install khal vdirsyncer

# 配置 ~/.config/vdirsyncer/config
# 配置 ~/.config/khal/config
```

**CalDAV:**
使用任何输出到 CLI 或 API 的 CalDAV 客户端。

### 任务管理器选项

**Todoist:**
```bash
pip install todoist-api-python
export TODOIST_API_TOKEN="your-token"
```

**Trello:**
使用 Trello REST API（带密钥/令牌）。

**基于文件:**
markdown 文件中的任务，由自定义脚本解析。

## 故障排除

| 问题 | 原因 | 解决方案 |
|---------|-------|----------|
| 任务未在正确时间运行 | 时区错误 | 将 `"tz": "UTC"` 改为你的时区（例如 `"America/New_York"`） |
| 缺少日历事件 | 同步延迟 | 日历同步按自己的日程进行；摘要可能会错过最近添加的事项 |
| 显示的任务过多 | 无过滤 | 在提示词中添加"前 3 个"或按项目/标签过滤 |
| 格式看起来不好 | 渠道限制 | 某些渠道（Telegram、Discord）不支持表格；使用项目符号 |

## 自定义

### 改变计划

编辑 `expr` 字段：
- `"0 7 * * *"` = 上午 7:00（更早）
- `"0 12 * * *"` = 下午 12:00（更晚）
- `"0 9 * * 1-5"` = 仅工作日

### 添加部分

添加到提示词：
```
5. 股票：检查投资组合价值
6. 新闻：从 [SOURCE] 获取头条新闻
```

### 周末版本

为周六创建单独的任务：
```json
{
  "name": "weekend-brief",
  "schedule": { "expr": "30 9 * * 6" },  // 仅周六
  "payload": {
    "message": "Generate weekend brief: Include personal projects, hobby tasks."
  }
}
```

## 经验教训

### 有效的

- **平衡模型 (Sonnet)** - 快速、便宜、可靠的格式
- **隔离会话** - 保持主会话整洁
- **一致时间** - 创建习惯和预期

### 陷阱

- 日历同步延迟是真实的 - 不要期望分钟级准确性
- 大型任务列表会触发速率限制 - 积极过滤
- 完全跳过空部分，而不是说"未找到任何内容"

## 安全

- 提示词中无秘钥
- 所有 API 密钥在 `~/.openclaw/credentials/`
- 隔离会话防止会话污染

## 相关

- [idea-pipeline](idea-pipeline.md) - 夜间研究想法
- [tech-discoveries](tech-discoveries.md) - 每周技术新闻管理

## 更新日志

- **2026-02-09** - 初始版本
- **2026-02-10** - 为公开分享而泛化
