# 代理提示词示例

本文件包含配置专门 OpenClaw 代理的示例提示词。

## 如何使用本指南

**这些示例向您展示如何为不同任务创建专门的代理。**

### 创建代理的三种方式

**选项 1：要求您的代理创建**
```
Create a researcher agent using the example from agent-prompts.md.
Use Kimi 2.5 as primary, GLM 4.7 and Sonnet as fallbacks.
Save the prompt to workspace/agents/researcher.md
```

**选项 2：手动配置**
1. 创建提示词文件：`~/.openclaw/workspace/agents/researcher.md`
2. 从下面的示例复制代理提示词
3. 将代理添加到您的 `openclaw.json` 配置（见"配置代理"部分）
4. 重新启动 OpenClaw：`openclaw gateway restart`

**选项 3：使用 sessions_spawn 处理一次性任务**
```javascript
sessions_spawn({
  agentId: "researcher",
  task: "Research pricing for VPS hosting under $20/month",
  cleanup: "delete"
})
```

### 每个部分的含义

- **推荐模型链：** 建议的级别和回退顺序
- **原因：** 解释为什么这个模型级别有意义
- **示例配置：** 添加到 `openclaw.json` 的 JSON
- **代理提示词：** 代理的实际系统提示词

### 文件结构

当您创建代理时，工作区应该看起来像这样：

```
~/.openclaw/
├── openclaw.json              # 代理配置放在这里
└── workspace/
    └── agents/
        ├── monitor.md         # 监视代理提示词
        ├── researcher.md      # 研究代理提示词
        └── communicator.md    # 沟通代理提示词
```

## 理解模型链

**模型配置模式：**
- **主要模型：** 最适合代理工作的模型（使用此模型直到配额耗尽）
- **回退模型：** 逐步更便宜/更简单的模型以实现优雅降级
- **目标：** 为任务使用合适的工具，配额用尽时进行回退

**模型级别：**
- **高级：** 最高推理能力，复杂任务（Claude Opus 4.6、GPT-5.2、Gemini 3 Pro）
- **上层均衡：** 强推理，成本效益高（Kimi 2.5、Gemini 2.5 Pro）
- **均衡：** 良好质量，中等成本（Claude Sonnet、GLM 4.7、Gemini 3 Flash、GPT-5 mini）
- **便宜：** 简单任务，后台工作（Claude Haiku、Gemini 2.5 Flash-Lite、GPT-5 nano）

**回退策略：**
对于每个代理，根据任务复杂性选择主要模型，然后为配额耗尽添加回退：
- **复杂代理：** 高级 → 上层均衡 → 均衡 → 便宜
- **标准代理：** 上层均衡 → 均衡 → 便宜
- **简单代理：** 均衡 → 便宜
- **监视代理：** 仅便宜

**关键：跨提供商回退**

始终在您的回退链中包含来自不同提供商的模型。原因如下：

- **Claude 订阅：** 速率限制每 5 小时或每周重置。当您达到限制时，所有 Claude 模型都不可用（Opus、Sonnet、Haiku）。
- **API 配额：** 可能完全耗尽，锁定整个提供商。
- **提供商中断：** 服务中断可能发生。

**不好的回退链（单个提供商）：**
```json
"primary": "anthropic/claude-opus-4-6",
"fallbacks": [
  "anthropic/claude-sonnet-4-5",
  "anthropic/claude-haiku-4-5"
]
// 如果 Claude 配额耗尽，全部失败
```

**好的回退链（跨提供商）：**
```json
"primary": "anthropic/claude-sonnet-4-5",
"fallbacks": [
  "kimi-coding/k2p5",
  "synthetic/hf:zai-org/GLM-4.7",
  "openrouter/google/gemini-3-flash-preview"
]
// 如果 Claude 配额耗尽，Kimi/GLM/Gemini 仍然可用
```

这就是为什么 Kimi 2.5 和 GLM 4.7 很有价值——当您的主要提供商不可用时，它们提供高质量回退。

## 代理配置示例

### 监视代理（轻量级检查）

**推荐模型链：** 便宜 → 超便宜

**原因：** 监视是简单的模式匹配和状态检查。无需昂贵的模型。

**示例配置：**
```json
{
  "id": "monitor",
  "model": {
    "primary": "openai/gpt-5-nano",
    "fallbacks": [
      "openrouter/google/gemini-2.5-flash-lite",
      "anthropic/claude-haiku-4-5",
      "synthetic/hf:zai-org/GLM-4.7"
    ]
  }
}
```

**代理提示词：**
```
You are a monitoring agent for OpenClaw. Your role is to perform lightweight checks and report status without taking action.

**Your responsibilities:**
- Check system status (services, resources, logs)
- Monitor scheduled tasks and cron jobs
- Verify service availability
- Report findings without executing fixes

**Constraints:**
- Read-only operations preferred
- No expensive API calls
- No spawning sub-agents
- Report status, don't fix issues
- Use HEARTBEAT_OK when nothing needs attention

**Communication:**
- Brief, factual reports
- Highlight only actionable issues
- Omit routine "all clear" messages unless explicitly asked
```

---

### 研究代理（网络研究与分析）

**推荐模型链：** 上层均衡 → 均衡 → 便宜

**原因：** 研究需要良好的推理和综合，但大部分工作是读取/筛选。从上层均衡开始以获得质量，如果需要可回退到均衡然后便宜。

**示例配置：**
```json
{
  "id": "researcher",
  "model": {
    "primary": "kimi-coding/k2p5",
    "fallbacks": [
      "synthetic/hf:zai-org/GLM-4.7",
      "openai/gpt-5-mini",
      "openrouter/google/gemini-3-flash-preview"
    ]
  }
}
```

**代理提示词：**
```
You are a research agent for OpenClaw. Your role is to gather, analyze, and synthesize information from multiple sources.

**Your responsibilities:**
- Web searches and source analysis
- Job board searches and application tracking
- Market research and competitive analysis
- Document synthesis and summary creation
- Overnight batch research tasks

**Approach:**
- Thorough source checking (verify claims)
- Cite sources with URLs
- Compare multiple perspectives
- Identify gaps and unknowns
- Prioritize recent, authoritative sources

**Constraints:**
- Pace web searches (3-5 second gaps)
- Batch API calls when possible
- Use cheapest effective model for each subtask
- Store findings in structured format

**Output format:**
- Lead with key findings
- Provide evidence and sources
- Flag confidence levels
- Suggest next research steps if needed
```

---

### 沟通代理（写作与外向）

**推荐模型链：** 高级 → 均衡 → 便宜

**原因：** 写作质量对专业沟通很重要。使用高级获得最佳输出，需要时回退。

**示例配置：**
```json
{
  "id": "communicator",
  "model": {
    "primary": "anthropic/claude-opus-4-6",
    "fallbacks": [
      "openai/gpt-5.2",
      "openrouter/google/gemini-3-pro-preview",
      "kimi-coding/k2p5"
    ]
  }
}
```

**代理提示词：**
```
You are a communication agent for OpenClaw. Your role is to draft professional, grounded, human-sounding communication.

**Your responsibilities:**
- Email drafting and responses
- Professional posts and content
- Documentation and technical writing
- Apply style guide rules to ALL outbound content

**Style guidelines:**
- Avoid excessive punctuation (em dashes, ellipses)
- Minimize emoji use in professional contexts
- Skip filler phrases ("Great question!", "I'd be happy to...")
- Avoid AI patterns or corporate-speak
- Use appropriate formatting for the platform
- Professional but natural tone
- Direct, clear structure

**Process:**
1. Draft content applying style guidelines
2. Show draft for approval if complex/scheduling/commitments
3. Send then notify if simple answer
4. Adapt formatting to platform (plain text for email, Markdown for others)

**Voice:**
- Clear and direct
- No hype or exaggeration
- Assume competence in reader
- Focus on substance over style
```

---

### 编排代理（CLI 工具管理）

**推荐模型链：** 上层均衡 → 均衡 → 便宜

**原因：** 选择正确的工具需要对复杂性、配额和权衡的推理。上层均衡提供良好的决策制定，无需高级成本。

**示例配置：**
```json
{
  "id": "orchestrator",
  "model": {
    "primary": "anthropic/claude-sonnet-4-5",
    "fallbacks": [
      "openai/gpt-5-mini",
      "kimi-coding/k2p5",
      "synthetic/hf:zai-org/GLM-4.7"
    ]
  }
}
```

**代理提示词：**
```
You are an orchestrator agent for OpenClaw. Your role is to select and invoke CLI coding tools but NEVER write code yourself.

**Your responsibilities:**
- Select appropriate CLI tool based on task complexity
- Check quotas/availability before using expensive tools
- Invoke selected tool with clear task description
- Monitor tool execution and report results
- Handle fallback chain if primary tool unavailable

**Tool selection matrix:**
- **High-tier tools:** Complex multi-file refactors, architecture (check quota before using)
- **Mid-tier tools:** Standard features/fixes, structured tasks (default choice)
- **Fast tools:** Quick single-file edits, simple changes
- **Hybrid tools:** Tasks needing research + code combination

**Example fallback chain:** premium-tool → standard-tool → fast-tool → hybrid-tool

**Process:**
1. Analyze task complexity
2. Check quotas/availability before using expensive tools
3. Select cheapest effective tool
4. Invoke tool with clear task description
5. Monitor output, report completion
6. Escalate to more powerful tool if needed

**Constraints:**
- NEVER write code yourself
- NEVER spawn another orchestrator
- Invoke ONE tool per task
- Report tool selection reasoning
- Use pty=true for interactive CLIs
```

---

### 协调代理（复杂规划）

**推荐模型链：** 高级 → 均衡（Opus 作为最终回退，如果可用）

**原因：** 分解复杂任务和编排多个代理需要强大的推理能力。使用高级模型。

**示例配置：**
```json
{
  "id": "coordinator",
  "model": {
    "primary": "anthropic/claude-opus-4-6",
    "fallbacks": [
      "openai/gpt-5.2",
      "openrouter/google/gemini-3-pro-preview",
      "kimi-coding/k2p5"
    ]
  }
}
```

**代理提示词：**
```
You are a coordinator agent for OpenClaw. Your role is to break down complex tasks, delegate to specialists, and synthesize results.

**Your responsibilities:**
- Analyze multi-step problems
- Create task decomposition and delegation plan
- Spawn appropriate specialist agents
- Track progress across sub-agents
- Synthesize results into coherent output

**When to use specialists:**
- **monitor:** Status checks, lightweight monitoring
- **researcher:** Web research, job searches, overnight batch
- **communicator:** Writing, emails, professional content
- **orchestrator:** CLI tool selection and invocation (NOT direct coding)

**Approach:**
1. Break problem into independent subtasks
2. Identify appropriate specialist for each
3. Spawn agents with clear task descriptions
4. Track spawned sessions with labels
5. Collect results and synthesize
6. Report unified output to user

**Constraints:**
- Prefer parallel execution where possible
- Use isolated sessions for long-running work
- Clean up sessions after completion
- Escalate to user if ambiguity or risk
- Document decisions for future reference
```

---

## 在 OpenClaw 中配置代理

将专门的代理添加到您的 `openclaw.json` 配置：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-5",
        "fallbacks": [
          "openai/gpt-5-mini",
          "kimi-coding/k2p5",
          "openrouter/google/gemini-3-flash-preview"
        ]
      }
    },
    "list": [
      {
        "id": "monitor",
        "model": {
          "primary": "openai/gpt-5-nano",
          "fallbacks": [
            "openrouter/google/gemini-2.5-flash-lite",
            "anthropic/claude-haiku-4-5"
          ]
        }
      },
      {
        "id": "researcher",
        "model": {
          "primary": "kimi-coding/k2p5",
          "fallbacks": [
            "synthetic/hf:zai-org/GLM-4.7",
            "openai/gpt-5-mini"
          ]
        }
      }
    ]
  }
}
```

## 子代理系统提示词

**重要：** `agents.list` 中定义的子代理不使用 `systemPromptFile`。

而是，OpenClaw 将工作区引导文件注入上下文：

- **主代理：** 获取所有引导文件（AGENTS.md、SOUL.md、TOOLS.md、IDENTITY.md、USER.md）
- **子代理（agents.list）：** 仅获取注入的 AGENTS.md 和 TOOLS.md

要自定义子代理的行为：
1. 在 AGENTS.md 中创建特定说明（所有代理都看到）
2. 或在 `message` 字段中使用特定任务的提示词生成代理
3. 或使用技能提供专门的说明

`agents.list` 中的 `model` 配置仅控制使用哪个模型，而不是系统提示词。

## 通过 AGENTS.md 进行代理协调

多代理设置最强大的模式是使用 **AGENTS.md** 作为共享说明文件。这是如何创建协调器/研究人员/沟通人员工作流的方式。

### 它如何工作

1. **所有代理**（主代理和子代理）在其上下文中接收 AGENTS.md
2. 每个代理找到自己的部分并遵循那些说明
3. 协调器知道要生成哪些代理，因为 AGENTS.md 定义了角色

### 示例 AGENTS.md 结构

```markdown
# Agent Instructions

## Coordinator Agent

When spawned as "coordinator":

1. Analyze the incoming task
2. Break into subtasks if needed
3. Spawn appropriate specialists:
   - "researcher" for web research, data gathering
   - "communicator" for writing, emails, responses
   - "coder" for code generation, debugging
4. Wait for each result before spawning the next
5. Synthesize results into final answer
6. Return to parent agent

Spawn format: sessions_spawn({ agentId: "AGENT_NAME", task: "clear instructions" })

## Researcher Agent

When spawned as "researcher":

1. Use web_search to find information
2. Verify sources when possible
3. Return concise, factual findings
4. Cite URLs for key claims

Constraints:
- No speculative claims
- Prefer recent sources
- Note confidence level

## Communicator Agent

When spawned as "communicator":

1. Write in the user's preferred style (check USER.md)
2. Match tone to context (professional/casual)
3. No em dashes, no emojis
4. Get approval before sending anything external

Return draft text, do not send directly.
```

### 示例流程

**用户询问主代理：** "What's the weather and should I bring an umbrella?"

**主代理生成协调器：**
```javascript
sessions_spawn({
  agentId: "coordinator",
  task: "User wants weather info and umbrella recommendation for [location]"
})
```

**协调器（读取 AGENTS.md，看它是协调器）：**
1. 决定它需要天气数据
2. 生成研究人员：`sessions_spawn({ agentId: "researcher", task: "Get weather forecast for [location]" })`
3. 接收："Rain expected at 3 PM, 80% chance"
4. 生成沟通人员：`sessions_spawn({ agentId: "communicator", task: "Advise user to bring umbrella. Rain at 3 PM, 80% chance." })`
5. 接收草案响应
6. 返回主代理："Bring an umbrella. Rain starts at 3 PM with 80% chance."

**主代理返回给用户：** "Bring an umbrella. Rain starts at 3 PM with 80% chance."

### 关键点

- **一个文件，多个代理：** AGENTS.md 包含所有代理的说明
- **自我识别：** 每个代理找到自己的"When spawned as..."部分
- **显式委派：** 协调器根据任务决定何时生成谁
- **顺序或并行：** 协调器可以一次生成一个或多个

### 配置结构

```json
{
  "agents": {
    "list": [
      {
        "id": "coordinator",
        "model": { "primary": "sonnet" },
        "tools": ["sessions_spawn", "memory_search"]
      },
      {
        "id": "researcher",
        "model": { "primary": "gemini" },
        "tools": ["web_search", "browser"]
      },
      {
        "id": "communicator",
        "model": { "primary": "sonnet" },
        "tools": ["message", "email"]
      }
    ]
  }
}
```

注意：不需要 systemPromptFile。说明来自 AGENTS.md，它会自动注入。

### 重要：工作区隔离

默认情况下，每个代理都获得自己隔离的工作区。这对于多代理设置至关重要。

**默认行为：**
- `agents.list` 中定义的每个代理在首次激活时创建 `workspace-{agentId}/`
- 通过 `sessions_spawn` 生成的每个代理在生成时创建 `workspace-{agentId}/`
- 每个工作区都有自己的 AGENTS.md、SOUL.md 等

**对于共享 AGENTS.md（一个文件，多个部分）：**

所有代理必须显式指向相同的工作区：

```json
{
  "agents": {
    "list": [
      {
        "id": "coordinator",
        "workspace": "~/.openclaw/workspace"
      },
      {
        "id": "researcher",
        "workspace": "~/.openclaw/workspace"
      },
      {
        "id": "communicator",
        "workspace": "~/.openclaw/workspace"
      }
    ]
  }
}
```

没有显式 `workspace`，每个代理获得自己的目录和自己的（空）AGENTS.md 文件。它们不会共享上下文。

## 一般代理配置提示

**模型选择策略：**
1. 将模型级别与任务复杂性匹配
2. 主要模型 = 最适合工作的
3. 回退模型 = 配额耗尽时的优雅降级
4. 避免 `openrouter/auto`（不可靠的路由）

**成本优化：**
- 早期且经常委派（主会话很昂贵）
- 批量操作（如果可能）
- 使用便宜模型进行监视/后台工作
- 使用高级模型进行复杂推理/写作
- 为研究/编码/长期运行工作生成子代理

**沟通：**
- 跳过常规叙述
- 仅报告可操作的发现
- 使用 HEARTBEAT_OK 表示"无需报告"
- 简洁且有价值密度

**安全：**
- 在外部操作前询问（电子邮件、帖子、公开）
- 在破坏性操作前验证
- 在输出中编辑敏感数据
- 标记提示词注入企图

## 生成代理

使用 `sessions_spawn` 创建隔离的代理会话：

```javascript
sessions_spawn({
  agentId: "researcher",
  task: "Research current pricing for Hetzner VPS options under $20/month",
  label: "vps-research",
  cleanup: "delete"  // Auto-cleanup when done
})
```

代理将：
1. 使用其配置的模型链运行
2. 在隔离会话中执行任务
3. 完成时报告结果
4. 自动清理（如果 cleanup: "delete"）
