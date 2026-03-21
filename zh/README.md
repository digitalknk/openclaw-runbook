# OpenClaw 运行手册（非炒作版）

> 已在 OpenClaw 2026.2.x 版本测试
> 使用 Claude 辅助创建的文档

这个仓库包含了一份实用指南，教你如何日常运行 OpenClaw，而不会浪费金钱、配额，或你的理智。

这不是官方指南。
这不是"最佳设置"。
这反映了我在反复折腾 OpenClaw 之后，想要一个稳定、可预测、无聊（但令人放心）的方式来运行它。

如果你在寻找华丽的演示或"改变一切"的能量，这可能不适合你。

## 这是什么

- 一份为想让 OpenClaw 运行数周而非数分钟的人准备的运行手册
- 立场鲜明，但对权衡利弊有明确说明
- 专注于编排器 vs 工作者模型、成本控制、内存边界和防护栏
- 从"蜜月期后"的阶段写出

## 这不是什么

- 初学者教程
- 模型或供应商的营销页面
- 声称这个设置对所有人都适用

## 指南

主要指南在这里：

- [guide.md](./guide.md)

它包含了真实的配置片段、某些选择的原因解释，以及经历过时间考验的模式。

## 示例

`examples/` 目录包含可操作的模板和参考：

- **[agent-prompts.md](../examples/agent-prompts.md)** - 创建专门的代理、模型链和编排器/研究者/沟通者模式
- **[spawning-patterns.md](../examples/spawning-patterns.md)** - 如何从技能、提示词和 cron 任务生成子代理
- **[heartbeat-example.md](../examples/heartbeat-example.md)** - 用于监控的轮转心跳模式
- **[skill-builder-prompt.md](../examples/skill-builder-prompt.md)** - 创建 AgentSkills 的提示词模板
- **[task-tracking-prompt.md](../examples/task-tracking-prompt.md)** - 为代理可见性构建任务跟踪系统
- **[security-hardening.md](../examples/security-hardening.md)** - 生产安全：API 密钥、工具策略、成本控制、网络锁定
- **[security-quickstart.md](../examples/security-quickstart.md)** - 复制粘贴提示词以实现基本安全控制
- **[security-patterns.md](../examples/security-patterns.md)** - 提示词注入防御和安全规则
- **[vps-setup.md](../examples/vps-setup.md)** - VPS 部署和加固指南
- **[sanitized-config.json](../examples/sanitized-config.json)** - OpenClaw 配置示例
- **[config-example-guide.md](../examples/config-example-guide.md)** - 配置部分参考
- **[check-quotas.sh](../examples/check-quotas.sh)** - 检查跨供应商 API 配额使用情况的脚本

## 应用展示

`showcases/` 目录包含社区提供的即插即用自动化模式：

- **[daily-brief](../showcases/daily-brief.md)** - 包含天气、日历、任务的早间摘要
- **[idea-pipeline](../showcases/idea-pipeline.md)** - 对捕获想法的隔夜研究
- **[linkedin-drafter](../showcases/linkedin-drafter.md)** - 每周内容生成
- **[tech-discoveries](../showcases/tech-discoveries.md)** - 精选科技新闻
- **[homelab-access](../showcases/homelab-access.md)** - 通过 Telegram 安全远程 SSH
- **[agent-orchestrator](../showcases/agent-orchestrator.md)** - 将编码任务路由到最优工具

每个应用展示都设计为立即可用。复制 cron 任务，替换占位符，然后部署。

有一个运行良好的自动化？参见 [showcases/template.md](../showcases/template.md) 提交你自己的。

## 分享这个

如果这个指南对你有帮助，请考虑：

- **分享它**给其他可能觉得有用的人
- **链接回来**如果你在博客文章、视频或其他资源中引用它
- **提交你自己的应用展示**，这样其他人可以从你的设置中学习

这是一个社区资源。参与的人越多，对每个人都越好。

## 社区资源

来自社区的其他有用的 OpenClaw 资源：

**官方和发现**
- **[ClawHub](https://clawhub.com)** - 发现和分享 AgentSkills
- **[OpenClaw 文档](https://docs.openclaw.ai)** - 官方文档

**精选列表**
- **[awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases)** - 真实用例和示例
- **[awesome-openclaw](https://github.com/SamurAIGPT/awesome-openclaw)** - 工具和资源的精选列表
- **[awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)** - 社区贡献的技能

这些通过更多示例、技能和社区模式来补充这个运行手册。

## 贡献

欢迎贡献，但这不是一个自由所有制。

请在开启议题或拉取请求之前阅读 [CONTRIBUTING.md](../CONTRIBUTING.md)。

## 许可证

MIT
