# LinkedIn 草稿生成器

**分类:** 内容
**示例模型:** 高级等级 (Sonnet, Opus, GPT-4/5 等)
**更新时间:** 2026-02-09

> **使用方法:** 复制下面的定时任务和提示词。将 `[占位符]` 替换为你的值。每周创建草稿供你在发布前审查。

## 快速开始

### 1. 前置条件

- [ ] Notion 账户 (或 Airtable、Google Sheets) 带有草稿数据库
- [ ] 活动日志系统 (内存文件、git 提交或手动笔记)
- [ ] 任务/活动跟踪 (Todoist、Trello 或日历)
- [ ] 语音/人设指南 (可选 - 可以使用通用专业语气)

### 2. 复制此定时任务

粘贴到你的网关配置的 `cron.jobs` 部分:

```json
{
  "name": "linkedin-drafter",
  "schedule": {
    "kind": "cron",
    "expr": "0 10 * * 2",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Draft 2-3 LinkedIn posts. Review my recent activity from [YOUR_ACTIVITY_SOURCE]. Identify post-worthy insights. Draft in my voice: direct, no fluff, professional but human, no em dashes/emojis. Rotate topics: [YOUR_TOPIC_1], [YOUR_TOPIC_2], [YOUR_TOPIC_3]. Save drafts to [YOUR_DATABASE] with status 'Draft'."
  },
  "sessionTarget": "isolated"
}
```

**替换:**
- `[YOUR_ACTIVITY_SOURCE]` - 在哪里查找内容 (例如, "过去 7 天的内存文件", "Todoist 完成的任务", "GitHub 提交")
- `[YOUR_TOPIC_1/2/3]` - 你的内容支柱 (例如, "基础设施", "家庭实验室", "成本优化")
- `[YOUR_DATABASE]` - 草稿保存位置 (例如, "Notion LinkedIn 内容数据库")

### 3. 配置工具

```yaml
tools:
  notion: {}      # 或 airtable, sheets
  memory_search: {}  # 如果使用内存文件
  todoist: {}     # 或你的任务管理器
```

### 4. 测试

```bash
openclaw cron run linkedin-drafter
```

---

## 功能说明

**问题:** 保持 LinkedIn 曝光需要持续发布，但撰写帖子需要时间和精力。委派时难以保持语音。

**解决方案:** 每周自动草稿生成。每周二上午 10 点 UTC，审查你最近的工作，识别见解，用你的语音起草 2-3 篇帖子，保存到数据库供你审查。你发布最好的一条。

## 完整提示词(详细)

```
Draft LinkedIn posts for me.

**My voice characteristics:**
- Direct, no fluff, grounded tone
- Professional but human (not corporate)
- Specific examples over general advice
- No em dashes, no emojis, no AI-sounding language
- Clear structure, direct language

**Content topics (rotate through):**
1. [YOUR_TOPIC_1] - [Brief description]
2. [YOUR_TOPIC_2] - [Brief description]
3. [YOUR_TOPIC_3] - [Brief description]

**Process:**
1. Review my recent activity from [YOUR_ACTIVITY_SOURCE]
2. Check what I'm actively working on
3. Identify authentic insights worth sharing
4. Draft 2-3 posts (150-300 words each)
5. Vary formats: observation, lesson learned, question, behind-the-scenes

**For each draft:**
- Hook in first line
- Specific example or story
- Clear takeaway or question
- No hashtags, no "engage with this post" language

Save to [YOUR_DATABASE] with:
- Title: Post topic
- Content: Full draft
- Status: Draft
- Topic: Category
- Created: Today's date
```

## 活动源选项

**内存文件:**
```
Review memory files from last 7 days at [PATH_TO_MEMORY].
Look for: decisions, lessons, experiments, challenges overcome.
```

**任务管理器:**
```
Check completed tasks from last 7 days in [YOUR_TASK_SYSTEM].
Look for: project completions, problems solved, new tools tried.
```

**Git 活动:**
```
Review recent commits and PRs from [GITHUB_USERNAME] repositories.
Look for: interesting technical decisions, refactoring work, new features.
```

**日历:**
```
Check calendar from last 7 days for meetings, workshops, learning sessions.
```

## Notion 数据库架构

**表: LinkedIn 内容**

| 字段 | 类型 | 备注 |
|-------|------|-------|
| Title | 标题 | 帖子主题/摘要 |
| Content | 文本 | 完整草稿文本 |
| Status | 选择 | Draft / Ready / Posted |
| Topic | 选择 | [YOUR_TOPIC_1] / [YOUR_TOPIC_2] / [YOUR_TOPIC_3] |
| Created | 日期 | 自动填充 |
| Posted | 日期 | 发布时填充 |

## 替代方案: Airtable

与 Notion 相同的架构。使用 Airtable API:
```yaml
tools:
  airtable:
    api_key: "${AIRTABLE_API_KEY}"
    base_id: "${AIRTABLE_BASE_ID}"
```

## 语音指南

如果你没有语音文档，请将此添加到你的提示词:

```
**Writing style:**
- No em dashes (use commas or periods)
- No emojis
- Avoid filler phrases like "Great question!" or "I'd be happy to help!"
- Avoid academic/corporate buzzwords
- Sound like a competent professional talking to peers
- One clear idea per post
```

或创建 `VOICE.md` 文件并引用它:
```
Read VOICE.md for my writing style guidelines, then draft posts.
```

## 故障排除

| 问题 | 原因 | 解决方案 |
|---------|-------|----------|
| 通用帖子 | 没有记录最近的活动 | 开始在内存文件或任务中记录工作 |
| 错误的语气 | 语音指南不清楚 | 在提示词中添加更多具体例子 |
| 太相似 | 话题多样性不足 | 扩展话题列表，添加新类别 |
| 所有草稿都是同一主题 | 活动源太窄 | 从多个来源提取 (git + 任务 + 日历) |

## 经验教训

### 有效的方法

- **从实际工作来源** - 基于真实活动的帖子更真实
- **保存到数据库，不自动发布** - 审查缓冲防止坏帖子
- **周二时间** - 周初能量，有时间在发布前审查

### 无效的方法

- **自动发布** - 有些草稿需要大量编辑
- **通用话题** - "X 的 5 个技巧" 表现不如具体故事
- **每日计划** - 太频繁；每周更好

### 注意事项

- **内存间隙** - 如果你不记录工作，代理没有来源
- **敏感话题** - 避免讨论求职、薪酬等
- **时间** - 帖子在周二至周四、上午 8-10 点(你的时区)表现更好

## 变体

**Twitter/X 交叉发布:**
在提示词中添加: "也创建 Twitter 版本 (280 字符，需要时创建线程)。"

**线程格式:**
添加: "对于一个草稿，将其分解为 5 条推文线程。"

**分析审查:**
创建第二个任务: "审查上周的帖子，报告参与度。"

## 安全

- **永不自动发布** - 始终在发布前审查
- **无敏感数据** - 不要从机密工作来源
- **数据库是私有的** - 将草稿保存在私有 Notion/Airtable 中

## 相关链接

- [daily-brief](daily-brief.md) - 可以浮出内容想法
- [idea-pipeline](idea-pipeline.md) - 研究见解形成良好话题

## 更新日志

- **2026-02-09** - 初始版本，周二上午 10 点
- **2026-02-10** - 为公开分享进行了推广
