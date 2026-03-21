# 技能构建提示词

这个提示词帮助你创建或优化遵循最佳实践的代理技能。

## 关于代理技能

[AgentSkills 规范](https://agentskills.io/) 提供了一个结构，用于创建可维护、令牌高效的技能。这个提示词遵循该模型。

## 提示词模板

复制并自定义这个提示词，让你的代理创建或重构一个技能：

```
I need help creating or optimizing an AgentSkill.

Skill name:
[your-skill-name]

Purpose:
What the skill does and when it should activate.

Triggers:
What kinds of tasks or questions should activate this skill.

Tools needed:
Any tools, commands, or APIs the skill will use.

Reference docs:
Docs or specs that should live in references/ for on-demand loading.

Existing skill (if applicable):
Path to the current SKILL.md if this is a refactor.

Please:
- Create or optimize the skill following AgentSkills best practices
- Keep the core workflow in SKILL.md and move details into references/
- Keep SKILL.md under ~500 lines
- Validate the structure using the AgentSkills validator
- Show the final file structure and contents
```

## 为什么硬约束很重要

模糊的指令每次都会产生臃肿、耗费 Token 的技能。硬约束（第 44 行的 ~500 行限制）强制代理执行以下操作：

- 将核心工作流放在 SKILL.md 中
- 将详细信息移到 references/ 中以按需加载
- 保持 Token 使用量较低
- 使技能易于维护

没有约束，你会得到一个 2,000 行的技能文件，这会占用你上下文窗口的一半。

## 示例用法

**创建新技能：**

```
I need help creating an AgentSkill.

Skill name:
weather-checker

Purpose:
Check current weather and forecasts using wttr.in (no API key required).

Triggers:
Questions about weather, temperature, forecast.

Tools needed:
curl to fetch from wttr.in, parsing text output.

Reference docs:
wttr.in documentation should live in references/wttr-in-docs.md

Please:
- Create the skill following AgentSkills best practices
- Keep the core workflow in SKILL.md under ~500 lines
- Move API details into references/
- Show the final file structure and contents
```

**重构现有技能：**

```
I need help optimizing an AgentSkill.

Existing skill:
~/.openclaw/workspace/skills/my-bloated-skill/SKILL.md

Purpose:
The skill works but SKILL.md is 1,800 lines and burns too many tokens.

Please:
- Refactor following AgentSkills best practices
- Keep core workflow in SKILL.md under ~500 lines
- Move details into references/ for on-demand loading
- Validate the structure
- Show what changed
```

## 技能结构

一个结构良好的技能看起来像这样：

```
skills/
└── your-skill-name/
    ├── SKILL.md              # Core workflow (~500 lines max)
    ├── references/           # Loaded on-demand
    │   ├── api-docs.md
    │   └── examples.md
    └── scripts/              # Optional executables
        └── helper.sh
```

## 最佳实践

**保持 SKILL.md 专注：**
- 描述何时触发
- 显示核心工作流
- 在 references/ 中引用详细信息

**使用 references/ 来存放：**
- API 文档
- 详细示例
- 错误处理表
- 命令语法参考

**部署前测试：**
- 运行测试任务
- 检查 Token 使用量
- 验证它只加载需要的内容

## 社区技能

对第三方技能要谨慎。编写不当或恶意的技能可能会导致真实问题。将社区技能视为灵感而不是即插即用的解决方案。

构建自己的技能能给你带来：
- 完全理解它的功能
- 对 Token 使用的控制
- 不依赖外部维护者
- 凌晨 2 点更好的调试体验

## 安全性

在你的工作区内存文件中设置基本规则：
- 永远不要暴露秘密或 API 密钥
- 在外部操作前询问
- 在破坏性操作前验证

不是万无一失的，但有助于作为护栏。
