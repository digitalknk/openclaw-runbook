# 生成模式

如何在 OpenClaw 中从不同的上下文生成子代理。

## 快速参考

| 上下文 | 如何生成 | 用例 |
|---------|--------------|----------|
| 从技能 | 代码中的 `sessions_spawn()` | 编排、并行工作 |
| 从代理 | 提示词中的 `sessions_spawn` 工具 | 自委派 |
| 从 cron | 内联或在有效载荷中生成 | 计划的隔离任务 |
| 从聊天 | `/subagents spawn` 命令 | 从任何通道手动激活 |

---

## 聊天命令：`/subagents spawn`

**可用版本：** OpenClaw 2026.2.17+

直接从聊天生成子代理，无需使用工具界面。

**用法：**
```
/subagents spawn <agent-id> <task>
```

**示例：**
```
/subagents spawn researcher "Find recent papers on transformer architectures"
```

**何时使用：**
- 从移动设备/聊天快速一次性任务
- 当你想要确定性激活而不是代理决定生成时
- 在不修改提示词的情况下测试代理配置

**注意：**
- 代理必须存在于你的 `agents.list` 配置中
- 与 `sessions_spawn` 工具相同的超时和行为
- 结果返回到同一聊天线程
- 对一次性聊天命令禁用轮询子代理（无需 `wait`）

---

## 模式 1：从技能生成

最常见的模式。你的技能代码决定何时生成。

**示例：** 研究编排器，并行生成多个研究者。

```javascript
// File: skills/research-orchestrator/index.js

async function researchTopics(topics) {
  // Spawn a researcher for each topic
  const promises = topics.map(topic =>
    sessions_spawn({
      agentId: "researcher",
      task: `Research: ${topic}. Find pricing, features, and reviews.`,
      label: `research-${topic.replace(/\s+/g, '-')}`,
      cleanup: "delete"
    })
  );

  // Wait for all to complete
  const results = await Promise.all(promises);

  // Combine results
  return results.map((result, i) => ({
    topic: topics[i],
    findings: result
  }));
}
```

**何时使用：**
- 并行处理（多个独立任务）
- 不应阻止主会话的繁重工作
- 可能独立失败的任务

**关键选项：**
- `agentId` - 使用哪个代理配置
- `task` - 提示词/指令
- `label` - 用于跟踪（可选）
- `cleanup: "delete"` - 完成时自动删除会话
- `timeoutSeconds` - 最长等待时间（默认：300）

---

## 模式 2：从代理提示词生成

代理根据其指令决定何时生成。

**示例：** 协调器代理委派给专家。

```
You are a coordinator agent. When you receive a complex request:

1. Break it into subtasks
2. Spawn appropriate specialist agents for each subtask
3. Wait for results
4. Synthesize and report back

Available specialists:
- researcher: Web research, data gathering
- writer: Content creation, documentation
- coder: Code generation, debugging

To spawn an agent, use the sessions_spawn tool with:
- agentId: which specialist
- task: clear instructions
- label: for tracking

Example:
sessions_spawn({
  agentId: "researcher",
  task: "Find current pricing for AWS EC2 t3.large in us-east-1",
  label: "ec2-pricing-research"
})
```

**代理配置：**
```json
{
  "agents": {
    "list": [
      {
        "id": "coordinator",
        "model": {
          "primary": "anthropic/claude-sonnet-4-5"
        },
        "tools": ["sessions_spawn"]
      }
    ]
  }
}
```

**何时使用：**
- 自主委派
- 多步骤工作流
- 动态任务分解

---

## 模式 3：从 Cron 生成

生成隔离工作的计划任务。

**示例：** 每日摘要为多个主题生成研究代理。

```json
{
  "name": "daily-research-digest",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Spawn researcher agents for today's topics: AI news, tech funding, and security alerts. Combine results into a digest and email it to me."
  },
  "sessionTarget": "isolated"
}
```

**或更显式的生成：**

```javascript
// In your agent's prompt or skill
cron.schedule('0 9 * * *', async () => {
  const topics = ['AI news', 'tech funding', 'security alerts'];

  for (const topic of topics) {
    sessions_spawn({
      agentId: "researcher",
      task: `Research ${topic} from the last 24 hours`,
      label: `daily-${topic}`,
      cleanup: "delete"
    });
  }
});
```

**何时使用：**
- 计划的繁重工作
- 隔夜批处理
- 并行早晨摘要

---

## 完整示例：智能电子邮件助手

**目标：** 当你收到电子邮件时，生成一个代理来研究该主题并草拟回复。

**设置：**

1. **添加到 AGENTS.md**（所有代理都看到这个，包括子代理）：
```
## Email Assistant Agent

When spawned as "email-assistant", your role is:
- Identify the topic/request from the email
- Spawn a researcher agent to gather context
- Wait for research results
- Draft a response incorporating the research
- Present the draft for approval

Research prompt template:
"Research [TOPIC]. Find: key facts, recent developments, relevant data."
```

2. **添加到配置**：
```json
{
  "agents": {
    "list": [
      {
        "id": "email-assistant",
        "model": {
          "primary": "anthropic/claude-sonnet-4-5"
        },
        "tools": ["sessions_spawn", "email", "message"]
      },
      {
        "id": "researcher",
        "model": {
          "primary": "kimi-coding/k2p5"
        },
        "tools": ["web_search"]
      }
    ]
  }
}
```

**注意：** 子代理不使用单独的提示词文件。它们从工作区引导文件（AGENTS.md、TOOLS.md）和生成时发送的任务消息继承上下文。

3. **从电子邮件触发**（在你的技能或主代理中）：
```javascript
// When new email arrives
sessions_spawn({
  agentId: "email-assistant",
  task: `Handle this email:\n\nFrom: ${email.from}\nSubject: ${email.subject}\n\n${email.body}`,
  label: `email-${email.id}`,
  cleanup: "delete"
});
```

---

## 常见错误

**错误：** 生成而不等待结果
```javascript
// Wrong - fire and forget, never know if it worked
sessions_spawn({ agentId: "researcher", task: "Research X" });
console.log("Done"); // Immediately logs, spawn still running
```

**正确：** 适当的异步处理
```javascript
// Right - wait for completion
const result = await sessions_spawn({
  agentId: "researcher",
  task: "Research X",
  timeoutSeconds: 600
});
console.log("Result:", result);
```

**错误：** 使用错误的 agentId
```javascript
// Wrong - agent doesn't exist
sessions_spawn({ agentId: "resercher", ... }); // typo
```

**正确：** 验证代理存在
```javascript
// Check your config: agents.list should include "researcher"
```

**错误：** 为琐碎任务生成
```javascript
// Wrong - overhead costs more than task
sessions_spawn({
  agentId: "researcher",
  task: "Check if it's raining"
});
```

**正确：** 为有意义的工作生成
```javascript
// Right - significant task worth the overhead
sessions_spawn({
  agentId: "researcher",
  task: "Compare 5 VPS providers, analyze pricing/features/reviews"
});
```

**工作区注意：** 当你通过 `sessions_spawn` 生成代理时，它会自动创建 `workspace-{agentId}/`，其中包含自己的（空）AGENTS.md。

如果你想让生成的代理共享你的主工作区和 AGENTS.md，你必须：
1. 在 `agents.list` 中使用显式 `workspace: "~/.openclaw/workspace"` 定义代理，或
2. 在生成前将 AGENTS.md 复制到生成代理的工作区

对于跨生成代理的共享上下文，在配置中使用显式工作区路径预定义它们。

---

## 调试生成

**检查代理是否存在：**
```bash
openclaw config get | jq '.agents.list[].id'
```

**手动测试生成：**
```javascript
// In main session
sessions_spawn({
  agentId: "researcher",
  task: "Test: research OpenClaw documentation",
  timeoutSeconds: 60
})
```

**检查生成日志：**
```bash
tail -f ~/.openclaw/gateway.log | grep spawn
```

**会话跟踪：**
```javascript
// Use labels to track
sessions_spawn({
  agentId: "researcher",
  task: "...",
  label: `research-${Date.now()}`, // unique label
  cleanup: "keep" // do not auto-delete, inspect later
});
```

然后检查：
```bash
openclaw sessions list
```

---

## 成本考虑

生成有开销：
- 上下文加载（Token 成本）
- 会话设置时间
- 会话间通信

**生成的情况：**
- 任务耗时超过 2-3 分钟
- 需要并行处理
- 与主会话隔离很重要
- 需要不同的模型能力

**不生成的情况：**
- 任务微不足道（少于 30 秒）
- 内联处理就足够了
- 上下文连续性很重要

---

## 相关

- [agent-prompts.md](agent-prompts.md) - 创建专业化代理
- [showcases/agent-orchestrator.md](../showcases/agent-orchestrator.md) - 将任务路由到最优工具
- [showcases/idea-pipeline.md](../showcases/idea-pipeline.md) - 并行研究生成
