# OpenClaw 应用展示

真实的自动化模式，你可以复制、粘贴和自定义。每个应用展示都设计得可以直接使用，只需最少编辑。

## 如何使用

每个应用展示都遵循相同的格式：

1. **快速开始** - 复制粘贴现成的 cron 作业和提示词
2. **替换 `[PLACEHOLDERS]`** - 填入你的具体值
3. **测试** - 用 `openclaw cron run [job-name]` 手动运行
4. **部署** - 让它自动运行

> **首次自动化耗时:** 每个应用展示 5-10 分钟

## 应用展示按类别分类

### 每日自动化
无需手动操作，保持条理有序。

| 应用展示 | 功能 | 示例模型 |
|----------|------|---------|
| [daily-brief](daily-brief.md) | 早间摘要（天气、日历、任务） | 均衡型 |
| [idea-pipeline](idea-pipeline.md) | 夜间研究你的想法 | 研究型 |
| [coeus-knowledge-base](coeus-knowledge-base.md) | 自托管知识捕获，支持语义搜索 | 任意（本地 CPU） |

### 内容与研究
自动化研究和内容创建。

| 应用展示 | 功能 | 示例模型 |
|----------|------|---------|
| [linkedin-drafter](linkedin-drafter.md) | 每周用你的风格起草帖子 | 高端型 |
| [tech-discoveries](tech-discoveries.md) | 每周精选科技新闻 | 均衡型 |

### 基础设施与运维
安全地管理系统和访问权限。

| 应用展示 | 功能 | 示例模型 |
|----------|------|---------|
| [homelab-access](homelab-access.md) | 通过 Telegram 安全 SSH，需确认 | 均衡型 |

### 开发与编码
帮助代码和技术任务的代理。

| 应用展示 | 功能 | 示例模型 |
|----------|------|---------|
| [agent-orchestrator](agent-orchestrator.md) | 将任务路由到最优的 CLI 工具 | 高端型 |

## 模型层级参考

应用展示将模型层级作为**示例**引用。使用你已配置的任何模型：

| 层级 | 示例模型 | 最适合 | 成本 |
|------|---------|--------|------|
| **高端** | Opus、GPT-4/5、Gemini Pro | 复杂推理、创意任务 | 较高 |
| **上游均衡** | Kimi、Gemini Pro | 良好推理、快速 | 中等 |
| **均衡** | Sonnet、GLM、Gemini Flash | 通用任务 | 低 |
| **便宜** | Haiku、Flash-Lite、Nano | 简单任务、大量 | 最少 |

**注意:** 你的模型可能有不同的名称。应用展示适用于任何模型 - 根据你的设置和预算调整。

## 快速开始模板

没有找到你需要的？复制这个模板并构建你自己的：

> **[template.md](template.md)** - 从这里开始你自己的应用展示

该模板包括：
- 复制粘贴现成的 cron 作业结构
- 带占位符的提示词模板
- 故障排除指南
- 成本估算框架

## 提交你自己的

做了什么有用的东西？分享它：

1. 复制 `template.md`
2. 填入你的用例
3. 测试它有效
4. 提交 PR

**提交要求:**
- ✅ 复制粘贴现成（最少编辑即可使用）
- ✅ 所有 `[PLACEHOLDERS]` 都清楚标记
- ✅ 包括前置条件检查清单
- ✅ 提供成本估算
- ✅ 已测试和工作
- ✅ 无个人信息（使用占位符）

## 常见配置

大多数应用展示需要在你的网关中配置这些工具：

```yaml
tools:
  # 用于获取数据
  weather: {}        # 内置，无需 API 密钥
  calendar: {}       # Google、Nextcloud 等
  todoist: {}        # 或你的任务管理器

  # 用于研究
  web_search: {}     # Brave、Serper（需要 API 密钥）
  browser: {}        # 用于 HN、Reddit
  email: {}          # IMAP/SMTP 访问

  # 用于交付
  message: {}        # Telegram、Discord

  # 用于执行
  exec: {}           # SSH、本地命令
```

## 安全检查清单

部署任何应用展示前：

- [ ] 提示词或配置中没有硬编码的秘密
- [ ] API 密钥仅在 `~/.openclaw/credentials/` 目录中
- [ ] 敏感命令需要确认（如适用）
- [ ] 输出不泄露个人数据
- [ ] 自动化作业的隔离会话
- [ ] 审查代理访问的数据源

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| 作业没有运行 | 检查 `tz` 字段是否匹配你的时区 |
| 缺少工具 | 添加到网关配置 `tools:` 部分 |
| 输出错误 | 使提示词更具体 |
| 频率限制 | 减少频率或使用更便宜的模型 |
| 占位符未替换 | 搜索 `[YOUR_...]` 并填入 |

## 变更

每个应用展示都包括自定义的想法：

- **不同的计划** - 改变 cron 表达式
- **不同的交付** - Telegram、Discord、电子邮件、Slack
- **不同的来源** - 交换工具以获得替代品
- **扩展范围** - 添加更多数据源
- **简化版本** - 精简以降低成本

## 相关资源

- [agent-prompts.md](../examples/agent-prompts.md) - 模型选择指南
- [config-example-guide.md](../examples/config-example-guide.md) - 网关配置示例
- [heartbeat.md](../examples/heartbeat.md) - 定期检查模式

---

**想要贡献？** 请查看 [CONTRIBUTING.md](../CONTRIBUTING.md) 了解指南。
