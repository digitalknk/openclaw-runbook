# 想法管道

**分类:** 研究
**示例模型:** 研究等级 (Kimi, Gemini Flash 等)
**更新时间:** 2026-02-09

> **使用方法:** 复制下面的定时任务和提示词。将 `[占位符]` 替换为你的值。这将在夜间运行，研究你在白天捕获的想法。

## 快速开始

### 1. 前置条件

- [ ] 想法捕获方法 (Telegram 机器人、Discord 频道、电子邮件或笔记本)
- [ ] 带有 API 的任务管理器 (Todoist、Trello、Asana 或基于文件)
- [ ] Web 搜索工具已配置 (Brave、Serper 或替代 API 密钥)
- [ ] 启用了子代理生成

### 2. 复制此定时任务

粘贴到你的网关配置的 `cron.jobs` 部分:

```json
{
  "name": "idea-pipeline",
  "schedule": {
    "kind": "cron",
    "expr": "0 3 * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Process ideas from [YOUR_CAPTURE_METHOD]. For each idea: 1) Search web for existing solutions and market landscape. 2) Analyze technical feasibility (complexity 1-5, estimated time, blockers). 3) Write summary to [YOUR_TASK_SYSTEM] with findings, top 3 similar solutions, feasibility assessment, and next steps. Be concise."
  },
  "sessionTarget": "isolated"
}
```

**替换:**
- `[YOUR_CAPTURE_METHOD]` - 你如何捕获想法 (例如, "Telegram 机器人", "Discord #ideas 频道")
- `[YOUR_TASK_SYSTEM]` - 结果写入地点 (例如, "Todoist", "Trello")

### 3. 配置工具

```yaml
tools:
  web_search: {}  # Brave, Serper 等
  message: {}     # 用于读取捕获的想法
  todoist: {}     # 或你的任务管理器
```

### 4. 测试

```bash
openclaw cron run idea-pipeline
```

---

## 功能说明

**问题:** 白天捕获的想法需要研究来验证可行性。手动研究容易被跳过，导致好的想法被放弃。

**解决方案:** 夜间研究代理。在 UTC 凌晨 3 点运行，研究每个捕获的想法，分析可行性，使用摘要更新任务。结果在早上准备好。

## 完整提示词(详细)

```
Process the ideas captured from [YOUR_CAPTURE_METHOD].

For each idea:
1. SEARCH: Search web for
   - Existing products/services solving similar problem
   - Open source alternatives
   - Technical approaches others used
   - Market size or demand indicators

2. ANALYZE feasibility:
   - Technical complexity (1-5 scale)
   - Estimated build time
   - Key technical decisions needed
   - Potential blockers

3. WRITE summary to [YOUR_TASK_SYSTEM]:
   - Brief overview of findings
   - Top 3 similar solutions found with links
   - Feasibility assessment
   - Recommended next steps

Be concise. Focus on actionable insights, not exhaustive research.
Limit to top 3 ideas per night by priority.
```

## 捕获方法选项

**Telegram 机器人(推荐):**
1. 通过 @BotFather 创建机器人
2. 用户将想法转发给机器人
3. 机器人使用标签 `idea-pipeline` 保存到任务管理器

**Discord 频道:**
- 专用频道 (例如, #ideas)
- Webhook 监控消息
- 自动创建任务

**电子邮件:**
- 专用地址: ideas@yourdomain.com
- 主题 = 想法标题
- 正文 = 详情

**笔记本/文件:**
- 想法写入 markdown 文件
- 代理扫描目录
- 文件名 = 想法标题

## 任务管理器集成

**Todoist:**
```python
# Label tasks for processing
tasks = api.get_tasks(label="idea-pipeline")

# After research, update with label "researched"
api.update_task(task_id, labels=["researched"])
```

**Trello:**
- 想法进入 "Backlog" 列表
- 研究后，移到 "Researched" 列表
- 添加包含发现的检查清单

**基于文件:**
```
ideas/
├── backlog/
│   └── idea-001.md
└── researched/
    └── idea-001.md  # 研究后移动
```

## 并行处理(高级)

对于多个想法，生成子代理:

```javascript
// In your agent logic
for (const idea of ideas) {
  sessions_spawn({
    task: `Research: "${idea.text}". Search web, analyze feasibility, return structured summary.`,
    agentId: "researcher",
    model: "gemini"  // Cheap, fast for research
  });
}
```

## 故障排除

| 问题 | 原因 | 解决方案 |
|---------|-------|----------|
| 研究太浅 | 搜索查询不足 | 在提示词中添加 "从 3 个不同角度搜索" |
| 输出过多 | 搜索结果太多 | 限制为 "前 3 个来源" |
| 想法丢失 | 聊天消息消失 | 始终将结果写入任务管理器，不要写回聊天 |
| 被限流 | 过多 web 搜索 | 在搜索之间添加 2-3 秒延迟 |

## 经验教训

### 有效的方法

- **生成子代理** 用于多个想法的并行研究
- **Gemini Flash** - 初始研究的绝佳选择(快速、便宜)
- **结构化输出** - 可行性得分 + 后续步骤比散文更容易扫描

### 无效的方法

- **单代理处理所有想法** - 耗时太长，命中超时
- **过度研究** - 每个想法 10+ 个结果太多
- **更新聊天** - 消息会丢失；始终写入任务管理器

## 变体

**每周深度分析:**
```json
{
  "name": "idea-deep-dive",
  "schedule": { "expr": "0 3 * * 0" },  // 周日
  "payload": {
    "message": "Pick highest priority idea and do thorough research..."
  }
}
```

**市场分析:**
在提示词中添加: "包括竞争对手定价、商业模式分析。"

**技术探讨:**
添加: "为可行性最高的想法生成概念代码。"

## 相关链接

- [daily-brief](daily-brief.md) - 早晨摘要
- [tech-discoveries](tech-discoveries.md) - 每周策展新闻

## 更新日志

- **2026-02-09** - 初始版本
- **2026-02-10** - 为公开分享进行了推广
