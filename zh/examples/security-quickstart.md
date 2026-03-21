# OpenClaw 安全快速入门

初次接触 OpenClaw 安全？从这里开始。这些提示词帮助你逐步实现基本安全。

有关完整配置参考，请参见 [security-hardening.md](security-hardening.md)。

---

## 开始之前

**首先进行备份：**
```bash
tar -czf ~/openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/
```

**谨慎测试更改。** 安全加固可能会限制代理 (Agent) 功能。

---

## 提示词 1：安全审计

审计你的当前 OpenClaw 安全：

```
检查位于 ~/.openclaw/ 的我的 OpenClaw 部署是否存在安全问题：

1. 在 openclaw.json 中，检查：
   - API 密钥是硬编码还是使用环境变量 (${VAR})？
   - 允许哪些工具？列出危险的（exec、cron、gateway）
   - 是否启用了 logging.redactSensitive？
   - gateway.bind 是否设置为环回？

2. 检查 ~/.openclaw/ 和 openclaw.json 上的文件权限

报告为：
- CRITICAL：立即修复
- HIGH：今天修复
- MEDIUM：本周修复
```

---

## 提示词 2：基本加固

实施核心安全控制：

```
使用这些安全控制更新 ~/.openclaw/openclaw.json：

1. 添加环境变量部分：
{
  "env": {
    "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
    "OPENAI_API_KEY": "${OPENAI_API_KEY}",
    "GATEWAY_TOKEN": "${GATEWAY_TOKEN}"
  }
}

2. 设置默认工具策略：
{
  "agents": {
    "defaults": {
      "tools": {
        "allow": ["read", "write", "edit", "web_search"],
        "deny": ["exec", "cron", "gateway", "nodes"]
      }
    }
  }
}

3. 启用日志记录删除：
{
  "logging": {
    "redactSensitive": "tools"
  }
}

4. 加固网关：
{
  "gateway": {
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "${GATEWAY_TOKEN}"
    }
  }
}

显示完整更新的配置。
```

---

## 提示词 3：成本保护

防止惊人账单：

```
向我的 OpenClaw 配置添加成本保护：

1. 跟踪模型成本：
{
  "models": {
    "providers": {
      "anthropic": {
        "models": [
          {
            "id": "claude-opus-4-6",
            "cost": { "input": 5.0, "output": 25.0 }
          },
          {
            "id": "claude-sonnet-4-5",
            "cost": { "input": 3.0, "output": 15.0 }
          }
        ]
      }
    }
  }
}

2. 创建具有适当模型的代理：
   - "monitor" 代理：仅使用 gpt-5-nano
   - "researcher" 代理：使用 kimi/k2p5 或 sonnet
   - 没有代理应默认使用 Opus

3. 确保 Opus 不能被定时任务或面向公众的代理使用

显示哪些代理获得哪些模型。
```

**重要：** 也在你的 Anthropic/OpenAI 仪表板中设置硬限制。单独的配置跟踪不会阻止账单。

---

## 提示词 4：备份设置

创建自动备份：

```
在 ~/.openclaw/scripts/backup.sh 处创建备份脚本：

要求：
1. 备份位置：~/backups/openclaw/YYYY-MM-DD/
2. 包括：
   - openclaw.json
   - workspace/*.md（AGENTS.md、SOUL.md 等）
   - memory/*.md（最后 30 天）
3. 使用 gpg 加密
4. 使其可执行
5. 设置 cron 以进行每天凌晨 2 点运行

提供完整的脚本和 cron 行。
```

---

## 每个提示词执行的操作

| 提示词 | 时间 | 风险 |
|--------|------|------|
| 审计 | 5 分钟 | 无 |
| 加固 | 15 分钟 | 可能限制代理功能 |
| 成本控制 | 10 分钟 | 可能阻止昂贵请求 |
| 备份 | 10 分钟 | 无 |

---

## 后续步骤

在执行这些提示词后：

1. **审查更改** - 确保你理解修改的内容
2. **测试代理** - 验证它们仍按预期工作
3. **阅读完整指南** - 查看 [security-hardening.md](security-hardening.md) 以获取：
   - 详细的工具策略示例
   - 速率限制
   - 提示词注入防御
   - 应急程序

---

## 故障排除

**代理停止工作：**
- 检查工具策略 - 你可能阻止了所需的工具
- 查看 agents.defaults.tools 中的 "deny" 列表

**无法访问网关：**
- `bind: loopback` 意味着仅限本地访问
- 这对本地部署是正确的

**成本仍然很高：**
- 提供商处的仪表板限制比配置更重要
- 在 Anthropic/OpenAI 仪表板中设置硬限制

---

## 参考资源

- [security-hardening.md](security-hardening.md) - 完整的安全参考
- OpenClaw Docs：https://docs.openclaw.ai/gateway/security
- OWASP LLM Top 10：https://owasp.org/www-project-top-10-for-large-language-model-applications/
