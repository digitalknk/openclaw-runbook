# 代理编排器

**类别:** 开发
**示例模型:** 高端层（Sonnet、Opus 等）用于路由
**更新时间:** 2026-02-09

> **如何使用:** 这是一个模式，不是单个 cron 作业。复制路由逻辑到你的代理中以智能地为每项任务选择正确的编码工具。

## 快速开始

### 1. 前置条件

- [ ] 安装了多个 CLI 编码工具（claude、codex、opencode、gemini）
- [ ] 每个提供商的 API 密钥在 `~/.openclaw/credentials/`
- [ ] 了解每个工具的优势
- [ ] 可选：配额跟踪方法

### 2. 安装 CLI 工具

```bash
# Claude (Anthropic)
npm install -g @anthropics/claude-code

# Codex (OpenAI)
npm install -g openai-codex

# Opencode (local)
npm i -g opencode-ai

# Gemini (Google)
npm install -g @google/gemini-cli
```

将 API 密钥添加到 `~/.openclaw/credentials/`：
```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
```

### 3. 复制此编排器代理

添加到你的网关配置：

```yaml
agents:
  orchestrator:
    model: anthropic/claude-sonnet-4-5
    tools:
      - sessions_spawn
      - exec
    system: |
      You are a coding task router. Analyze each task and select the optimal CLI tool.

      AVAILABLE TOOLS:
      1. claude - Complex multi-file refactors, architecture
      2. codex - Standard features/fixes, structured tasks
      3. opencode - Quick single-file edits
      4. gemini - Research + code hybrid tasks

      SELECTION RULES:

      Use claude if:
      - Changes span 3+ files
      - Requires architectural decisions
      - Complex refactoring
      - Needs deep context

      Use codex if:
      - Single feature or fix
      - Well-defined scope
      - 1-2 files affected
      - Standard patterns

      Use opencode if:
      - Quick edit to single file
      - Simple fix (typo, logic tweak)
      - Fast turnaround needed

      Use gemini if:
      - Needs research (API docs, examples)
      - Learning new technology
      - Research + implementation

      QUOTA CHECK:
      Before assigning to claude:
      1. Check quota via your tracking method
      2. If quota >90% or unavailable, fallback to codex

      FALLBACK CHAIN:
      claude → codex → opencode → gemini

      PROCESS:
      1. Analyze task description
      2. Check quota if needed
      3. Select optimal tool
      4. Spawn agent with selected tool
      5. Report: tool selected, why, expected scope
```

### 4. 使用示例

**路由编码任务：**
```json
{
  "agentId": "orchestrator",
  "message": "Task: Refactor auth system to use JWT. Spans 5 files, needs architectural decisions."
}
```

响应：
```
Selected: claude
Reason: Multi-file refactor (5 files), architectural decisions needed
Scope: Complex, estimated 10-15 minutes
Quota: 45% used, proceeding with claude
```

**简单任务：**
```json
{
  "agentId": "orchestrator",
  "message": "Task: Fix typo in README.md"
}
```

响应：
```
Selected: opencode
Reason: Single file, simple edit
Scope: Trivial, <1 minute
```

**配额回退：**
```json
{
  "agentId": "orchestrator",
  "message": "Task: Add new API endpoint"
}
```

响应：
```
Selected: codex (fallback)
Reason: Claude quota at 95%
Original choice: claude (single feature, well-defined)
```

---

## 这是什么功能

**问题：** 编码任务的复杂性差异很大。使用 Claude 来修复一个打字错误会浪费金钱。使用 Opencode 进行架构设计会浪费时间。手动选择需要了解每个工具的优势和当前配额。

**解决方案：** 编排器代理分析每项任务，检查配额，将其路由到最优工具。简单任务获得快速/便宜的工具。复杂任务获得强大的工具。配额耗尽会触发自动回退。

## 配额跟踪选项

### 选项 A：简单脚本

创建 `~/.local/bin/check-quotas`：
```bash
#!/bin/bash
# 检查每个提供商的配额
# 用你的实际提供商和配额替换

echo "claude: [used]/[limit] ([percent]%)"
echo "codex: [used]/[limit] ([percent]%)"
echo "opencode: unlimited"
```

在代理提示词中：
```
Run check-quotas script. If primary tool shows >90% usage, use fallback tool.
```

### 选项 B：API 状态检查

```python
# 一些提供商通过 API 暴露配额
import requests

def check_quota(provider):
    if provider == "anthropic":
        r = requests.get(
            "https://api.anthropic.com/v1/usage",
            headers={"Authorization": f"Bearer {KEY}"}
        )
        return r.json()["usage"]
```

### 选项 C：本地计数器

在 SQLite 中跟踪请求：
```sql
CREATE TABLE quota (
    provider TEXT,
    date TEXT,
    count INTEGER
);
```

## 工具选择矩阵

| 任务类型 | 最佳工具 | 原因 |
|---------|---------|------|
| 多文件重构 | claude | 深度上下文、架构决策 |
| 标准功能 | codex | 良好的能力和速度平衡 |
| 快速修复 | opencode | 快速、轻量级、本地 |
| 研究 + 代码 | gemini | 快速、擅长解释 |

**注意:** 定价和配额因提供商而异，随时间变化。检查你的提供商当前的定价。

## 成本比较

| 场景 | 不使用编排器 | 使用编排器 | 优势 |
|------|------------|---------|------|
| 用昂贵模型修复打字错误 | 成本更高 | 成本更低（使用更便宜工具） | 成本节省 |
| 错误的任务工具 | 结果差 | 选择正确工具 | 质量 ↑ |
| 配额耗尽 | 卡住/失败 | 自动回退 | 可靠性 ↑ |

## 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 选择错误的工具 | 提示词不清楚 | 使任务描述更具体 |
| 配额检查失败 | API 不可用 | 添加超时，假设配额正常 |
| 工具未安装 | 缺少 CLI | 安装或从选项中移除 |
| 生成失败 | 代理配置错误 | 检查 agentId 和模型名称 |

## 高级：自定义路由

添加你自己的规则：
```yaml
system: |
  ALSO CONSIDER:
  - If task mentions "test" or "testing", prefer codex (good at tests)
  - If task mentions "documentation", prefer gemini (good at explaining)
  - If task mentions "performance", prefer claude (deep analysis)
```

## 变更

**成本优先模式：**
始终选择最便宜的可行工具，即使更慢：
```
Priority: opencode → codex → gemini → claude
Only use claude if explicitly requested
```

**速度优先模式：**
始终选择最快的，成本次之：
```
Parallel spawn: claude + codex
Use first to complete
Cancel others
```

**学习模式：**
跟踪哪些工具对哪些任务类型成功：
```
Log: task_type, tool_selected, success_rating
Over time, optimize selections
```

## 安全

- **编排器中无代码执行** - 仅路由，不运行代码
- **工具隔离** - 每个生成的代理是独立的会话
- **审计跟踪** - 记录所有路由决策以供审查

## 相关资源

- [idea-pipeline](idea-pipeline.md) - 使用相似的生成模式
- [daily-brief](daily-brief.md) - 可根据复杂性路由到不同模型

## 更新日志

- **2026-02-09** - 初始版本，包含 4 工具路由
- **2026-02-10** - 增加了配额检查和回退链
