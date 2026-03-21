# OpenClaw 配置示例 - 使用指南

这个已清理的配置显示了 [OpenClaw 指南](../guide.md) 中引用的关键设置。

## 快速开始

1. 将 `sanitized-config.json` 复制到 `~/.openclaw/openclaw.json`
2. 将所有 `YOUR_*` 占位符替换为真实值
3. 运行 `openclaw doctor --fix` 进行验证
4. 运行 `openclaw security audit --deep` 检查问题

## 关键部分解释

### 模型配置（`agents.defaults.model`）

**协调器与工作模型模式：**
- 保持昂贵的模型（Opus、Sonnet）不在 `primary` 位置
- 使用有能力但便宜的模型作为您的默认值
- 强大的模型放在 `fallbacks` 中或固定到特定代理

**为什么这很重要：**
昂贵的默认值 = 日常工作中的配额浪费。便宜的默认值与范围有限的回退 = 可预测的成本。

### 内存搜索（`memorySearch`）

使用廉价的嵌入（`text-embedding-3-small`）搜索您的内存文件。

```json
"memorySearch": {
  "sources": ["memory", "sessions"],
  "experimental": { "sessionMemory": true },
  "provider": "openai",
  "model": "text-embedding-3-small"
}
```

**成本比较：**
- 数千次搜索：~$0.10
- 使用高级模型进行相同操作：$5-10+

### 上下文裁剪（`contextPruning`）

```json
"contextPruning": {
  "mode": "cache-ttl",
  "ttl": "6h",
  "keepLastAssistants": 3
}
```

**`cache-ttl` 模式：**
- 保持提示符缓存有效 6 小时
- 缓存过期时自动删除旧消息
- `keepLastAssistants: 3` 保留最近的连续性

**为什么 TTL 很重要：**
没有这个，您将更快地达到令牌限制，并为重复处理相同上下文付费。

### 压缩（`compaction.memoryFlush`）

```json
"compaction": {
  "mode": "default",
  "memoryFlush": {
    "enabled": true,
    "softThresholdTokens": 40000,
    "prompt": "Distill this session to memory/YYYY-MM-DD.md. Focus on decisions, state changes, lessons, blockers. If nothing worth storing: NO_FLUSH",
    "systemPrompt": "Extract only what is worth remembering. No fluff."
  }
}
```

**它做什么：**
当上下文达到 `softThresholdTokens`（40k）时，代理将会话提取到 `memory/YYYY-MM-DD.md`。

**提示词很重要：**
冲洗提示词告诉代理*什么*要记住。专注于决定、状态变化和教训，而不是常规交换。

**当它写 `NO_FLUSH` 时：**
如果没有发生值得存储的事情，代理跳过写入。无杂乱。

### 心跳模型（`heartbeat.model`）

**使用您有权访问的最便宜的模型。**

心跳经常运行但进行简单检查（读取文件、检查条件）。没有理由在此烧毁高级模型。

示例成本：
- GPT-5 Nano：~$0.0001 每次心跳
- Claude Sonnet：~$0.005 每次心跳

在 48 次心跳/天时，这是 $0.005/天 vs $0.24/天。

### 并发限制

```json
"maxConcurrent": 4,
"subagents": {
  "maxConcurrent": 8
}
```

**为什么这很重要：**
防止一个坏任务生成 50 次重试并在几分钟内烧毁您的配额。

### 安全：网关绑定

```json
"gateway": {
  "bind": "loopback"
}
```

**关键：** 这将网关绑定到 `127.0.0.1`（仅本地主机），而不是 `0.0.0.0`（所有接口）。

**检查它：**
```bash
netstat -an | grep 18789 | grep LISTEN
# 您想看到：127.0.0.1:18789
# 不是：0.0.0.0:18789
```

如果您看到 `0.0.0.0`，您的网关暴露在网络中。立即修复。

### 日志记录（`logging.redactSensitive`）

```json
"logging": {
  "redactSensitive": "tools"
}
```

从日志中的工具输出编辑敏感数据（API 密钥、令牌）。

**选项：**
- `"off"` - 无编辑（危险）
- `"tools"` - 仅编辑工具输出（推荐）
- `"all"` - 激进编辑（可能使调试更困难）

### 自定义模型提供商（NVIDIA NIM 示例）

您可以添加自定义提供商（如 NVIDIA NIM）以访问其他模型：

```json
"models": {
  "mode": "merge",
  "providers": {
    "nvidia-nim": {
      "baseUrl": "https://integrate.api.nvidia.com/v1",
      "api": "openai",
      "models": [
        {
          "id": "nvidia/moonshotai/kimi-k2.5",
          "name": "Kimi K2.5 (NVIDIA NIM)",
          "reasoning": false,
          "input": ["text"],
          "cost": {
            "input": 0,
            "output": 0
          },
          "contextWindow": 256000,
          "maxTokens": 8192
        }
      ]
    }
  }
}
```

**速率限制：** NVIDIA NIM 免费层有 40 RPM 限制。谨慎使用或作为回退。

**认证：** 在环境中或凭证目录中设置 `NVIDIA_API_KEY`。

## 文件结构

您的工作区应该看起来像这样：

```
~/.openclaw/
├── openclaw.json          # 主配置（此文件，已清理）
├── credentials/           # API 密钥（chmod 600）
│   ├── openrouter
│   ├── anthropic
│   └── synthetic
└── workspace/             # 您的工作目录
    ├── AGENTS.md
    ├── SOUL.md
    ├── USER.md
    ├── TOOLS.md
    ├── HEARTBEAT.md
    ├── memory/
    │   ├── 2026-02-07.md
    │   └── ...
    └── skills/
        └── your-skills/
```

## 安全检查清单

在生产环境中运行 OpenClaw 之前：

```bash
# 1. 验证配置
openclaw doctor --fix

# 2. 安全审计
openclaw security audit --deep

# 3. 锁定权限
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/openclaw.json
chmod 700 ~/.openclaw/credentials

# 4. 验证 localhost 绑定
netstat -an | grep 18789 | grep LISTEN

# 5. 检查暴露的秘密
grep -r "sk-" ~/.openclaw/  # 应该在日志中找不到任何东西
```

## 常见错误

**1. 将昂贵的模型留作默认值**
- Opus/Sonnet 在 `primary` = 配额燃尽
- 将它们移到回退或特定代理的配置

**2. 没有上下文裁剪**
- Token 使用量攀升，成本螺旋上升
- 添加带有 `cache-ttl` 的 `contextPruning`

**3. 网关暴露到网络**
- `bind: "0.0.0.0"` = 任何人都可以访问您的代理
- 始终使用 `bind: "loopback"`，除非您知道您在做什么

**4. 没有并发限制**
- 一个卡住的任务生成 50 次重试
- 将 `maxConcurrent` 设置为合理的值（4-8）

**5. 跳过安全审计**
- 每次配置更改后运行 `openclaw security audit --deep`
- 立即解决关键问题

## 后续步骤

1. 设置您的频道（Telegram、Discord 等）
2. 配置角色特定代理（监视、研究、沟通）
3. 将技能添加到 `workspace/skills/`
4. 在 `HEARTBEAT.md` 中设置心跳检查
5. 在启用 24/7 模式之前在本地会话中测试

## 资源

- **完整指南：** 请参阅存储库根目录中的 [`guide.md`](../guide.md)
- **官方文档：** https://docs.openclaw.ai
- **GitHub 问题：** https://github.com/openclaw/openclaw/issues
- **Discord 社区：** https://discord.com/invite/clawd
- **技能目录：** https://clawhub.com

## 成本跟踪

开始运行后，定期检查使用情况：

```bash
# 检查配额（可选脚本）
check-quotas

# 在提供商仪表板中监视成本
# - OpenRouter：https://openrouter.ai/activity
# - Anthropic：https://console.anthropic.com/settings/usage
# - OpenAI：https://platform.openai.com/usage
```

**目标：** 中等使用量（主会话 + 偶尔的子代理）每月 $45-50。

如果成本攀升超过 $100/月，检查：
- 默认配置中昂贵的模型
- 失控的代理重试（没有并发限制）
- 内存冲洗运行太频繁
- 心跳使用高级模型
