# 任务跟踪系统提示词

这个提示词帮助你构建一个任务跟踪系统，使代理工作可见，无需翻查日志。

## 为什么要进行任务跟踪？

OpenClaw 可能感觉像一个黑箱。你不知道它在做什么、什么卡住了或什么需要你的注意。任务跟踪系统通过在你已经查看的工具（Todoist、GitHub Projects、Linear 等）中使所有代理工作可见来解决这个问题。

## 关于这种方法

这个示例使用 Todoist，但该模式适用于任何具有 API 的任务管理器。关键是通过你可以随时瞥一眼的工具创建对代理状态的可见性。

## 前置条件

在将此提示词提供给你的代理之前：

1. **Todoist 账户** - 免费或付费 (https://todoist.com)

2. **API 令牌** - 从 Todoist 获取：
   - 设置 → 集成 → 开发者 → API 令牌
   - 复制令牌

3. **项目** - 手动创建或让代理创建：
   - 待办/队列项目
   - 活跃项目
   - 可选：等待/阻止项目（或使用任务分配）

4. **凭据目录** - 使用适当的权限设置：
   ```bash
   mkdir -p ~/.openclaw/credentials
   echo "your-todoist-api-token-here" > ~/.openclaw/credentials/todoist
   chmod 700 ~/.openclaw/credentials
   chmod 600 ~/.openclaw/credentials/todoist
   ```

## 提示词模板

复制并自定义此提示词以提供给你的代理：

```
Build a Todoist-based task tracking system for OpenClaw:

GOAL: Make agent work visible without checking logs. Glance at Todoist and see exactly what's happening.

STATE MODEL:
- Queue/Backlog: Tasks waiting to start
- Active: Work currently in progress
- Waiting/Assigned to me: Blocked on human input
- Done: Completed

OPERATIONS NEEDED:
1. create_task(title, project) - Add task to queue/backlog
2. move_to_active(task_id) - Start work, move to Active project
3. assign_to_me(task_id, reason) - Mark blocked, assign with comment explaining why
4. complete_task(task_id) - Mark done and close
5. add_comment(task_id, status) - Add progress updates to task

RECONCILIATION (runs via heartbeat every 30 min):
- Find Active tasks with no updates >24 hours (stalled)
- List tasks assigned to me (need my attention)
- Report summary if issues found, otherwise HEARTBEAT_OK

TECHNICAL:
- Use Todoist REST API v1: https://api.todoist.com/api/v1/
- API Documentation: https://developer.todoist.com/api/v1/
- Python SDK: https://doist.github.io/todoist-api-python/
- TypeScript SDK: https://doist.github.io/todoist-api-typescript/
- Store API token in ~/.openclaw/credentials/todoist (raw token, no ENV format)
- Create separate projects for Queue, Active, etc. or use a single project with labels
- Handle API rate limits gracefully

VISIBILITY:
I should open Todoist and immediately understand:
- What the agent is working on right now
- What's waiting for me
- What's stuck
- What's been completed

Adapt this to my Todoist setup. Ask me for project IDs or let me create them first.
```

## 自定义

**对于不同的任务管理器：**
- GitHub Projects: 使用 GitHub Projects API
- Linear: 使用 Linear API
- Notion: 使用 Notion 数据库 API
- Asana: 使用 Asana API

**状态模型变化：**
- 更简单：队列 → 活跃 → 完成（无等待状态）
- 更复杂：队列 → 活跃 → 审查 → 等待 → 完成
- 看板风格：待办 → 进行中 → 阻止 → 完成

**协调频率：**
- 更激进：每 15 分钟
- 不那么激进：每小时
- 时间限制：仅在工作时间

## 预期行为

一旦构建完成，系统应该：

1. **自动创建任务** 当代理开始工作时
2. **更新任务状态** 随着工作进展
3. **分配给你** 当被输入阻止时
4. **添加评论** 带有进度更新
5. **完成任务** 完成时
6. **报告停滞工作** 通过协调

你应该能够打开 Todoist 并立即看到：
- 当前工作（活跃项目）
- 阻止的工作（分配给你）
- 排队的工作（待办项目）
- 最近的完成（最近完成）

## 故障排除

**代理没有创建任务：**
- 验证 API 令牌正确
- 检查凭据文件有原始令牌（无 ENV 格式）
- 确保项目存在或代理有权创建它们

**任务卡在活跃状态：**
- 检查协调是否运行（每 30 分钟一次心跳）
- 查找停滞任务报告
- 如果需要，手动移动任务

**速率限制错误：**
- Todoist API 有速率限制（查阅文档）
- 在错误处理中添加指数退避
- 如果需要，减少协调频率

## 替代方法

你可以不从头开始构建，而是：

1. **寻找灵感** - 浏览 https://clawhub.com 寻找任务管理技能作为参考，而不是即插即用的解决方案
2. **让你的代理构建它** - 使用上面的提示词并让你的代理创建系统
3. **与现有工具集成** - GitHub Issues、Jira 等
4. **构建你自己的状态跟踪** - 基于文件、数据库等

**关于第三方技能的注意：** 直接从他人安装技能要谨慎。编写不当或恶意的技能可能会导致真实问题。将社区技能视为灵感而不是即插即用的解决方案。你的代理有能力构建这个 - 使用提示词。

关键是使代理工作可见，而不是使用的具体工具。
