# HEARTBEAT.md 示例

此示例显示一个旋转心跳模式，其中单个心跳根据节奏而不是一次性运行所有检查。

## 代理的提示词模板

复制并自定义此提示词以使您的代理构建旋转心跳系统：

```
Build a rotating heartbeat check system for HEARTBEAT.md:

Create these checks with their cadences:
- Email: every 30 min (9 AM - 9 PM only)
- Calendar: every 2 hours (8 AM - 10 PM only)
- Tasks: every 30 min (anytime)
- Git: every 24 hours (anytime)
- System: every 24 hours (3 AM only)

Create heartbeat-state.json to track last run timestamps.

On each heartbeat:
1. Read state file
2. Calculate which check is most overdue (respect time windows)
3. Run that check
4. Update timestamp in state file
5. Report only if check finds something actionable
6. Return HEARTBEAT_OK if nothing needs attention

Check implementations:
- Email: Check [your email service] for new messages from authorized senders
- Calendar: Check [your calendar] for events in next 24-48h
- Tasks: Check [your task manager] for stalled/blocked work
- Git: Check workspace for uncommitted changes
- System: Check for failed cron jobs and error logs

Adapt these to my specific services and tools.
```

## 示例 HEARTBEAT.md 结构

```markdown
# HEARTBEAT.md

## Cadence-Based Checks

Read `heartbeat-state.json`. Run whichever check is most overdue.

**Cadences:**
- Email: every 30 min (9 AM - 9 PM)
- Calendar: every 2 hours (8 AM - 10 PM)
- Tasks: every 30 min (anytime)
- Git: every 24 hours (anytime)
- System: every 24 hours (3 AM only)

**Process:**
1. Load timestamps from heartbeat-state.json
2. Calculate which check is most overdue (considering time windows)
3. Run that check
4. Update timestamp
5. Report if actionable, otherwise HEARTBEAT_OK

---

## Email Check

Check [your email service] for new messages.

**Report ONLY if:**
- New email from authorized sender
- Contains actionable request

**Update:** email timestamp in state file

---

## Calendar Check

Check [your calendar] for upcoming events.

**Report ONLY if:**
- Event starting in <2 hours
- New event since last check

**Update:** calendar timestamp in state file

---

## Task Check

Check [your task manager] for work status.

**Report ONLY if:**
- Tasks stalled >24h
- Blocked tasks need attention

**Update:** tasks timestamp in state file

---

## Git Check

Check workspace git status.

**Report ONLY if:**
- Uncommitted changes exist
- Unpushed commits found

**Update:** git timestamp in state file

---

## System Check

Check for system issues.

**Report ONLY if:**
- Failed cron jobs found
- Recent errors in logs

**Update:** system timestamp in state file
```

## 示例状态文件

```json
{
  "lastChecks": {
    "email": 1703275200000,
    "calendar": 1703260800000,
    "tasks": 1703270000000,
    "git": 1703250000000,
    "system": 1703240000000
  }
}
```

## 好处

- **单一心跳，多个检查** - 比管理单独的 cron 工作简单
- **分散负载** - 检查在逾期时运行，而不是全部一次运行
- **成本高效** - 一个便宜的模型进行路由
- **可调试** - 状态文件显示每次检查最后运行的时间
- **自适应** - 最逾期的先运行

## 自定义

**调整节奏：**
- 高优先级：15-30 分钟
- 中优先级：1-2 小时
- 低优先级：6-24 小时

**设置时间窗口：**
- 电子邮件/日历：仅清醒时间
- 系统检查：晚上安静时
- Git：任何时间

**替换检查类型：**
- 电子邮件 → RSS 源、webhooks
- 日历 → 项目截止日期
- 任务 → CI/CD 状态
- Git → 备份状态
- 系统 → 服务健康

## 替代方案：单独的 Cron 工作

如果您更喜欢显式调度：

```javascript
// Email check: every 30 min, 9 AM - 9 PM
cron({
  action: "add",
  job: {
    schedule: { kind: "cron", expr: "*/30 9-21 * * *" },
    payload: { kind: "agentTurn", message: "Check email" }
  }
})

// Git check: daily at 3 AM
cron({
  action: "add",
  job: {
    schedule: { kind: "cron", expr: "0 3 * * *" },
    payload: { kind: "agentTurn", message: "Check git status" }
  }
})
```

旋转心跳对于频繁检查和成本优化更好。单独的 cron 对于精确时序更好。
