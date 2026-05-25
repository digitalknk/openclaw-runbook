# Task Tracking Prompt

OpenClaw now has a native background task ledger. Start there before wiring an external task manager.

Use an external tool like Todoist, Linear, GitHub Issues, or Notion only when you want a separate human-facing board.

## Native Task Commands

```bash
openclaw tasks list
openclaw tasks show <lookup>
openclaw tasks audit
openclaw tasks maintenance
openclaw cron list
openclaw cron runs --id <job-id>
```

What creates task records:

- cron executions;
- subagent spawns;
- ACP background runs;
- CLI agent operations;
- session-backed media generation.

What does not create task records:

- normal chat turns;
- heartbeat turns;
- direct slash command responses.

## Prompt: Add a Human-Facing Board

Use this only if you still want a board outside OpenClaw:

```text
Build a bridge from OpenClaw background tasks to [Todoist/Linear/GitHub/Notion].

Goal:
Give me a human-facing board while keeping OpenClaw's native task ledger as the source of truth.

Read-only source:
- Use OpenClaw task and cron status commands or tools.
- Do not invent a second scheduler.
- Do not mark OpenClaw work complete just because the external task moved.

External board states:
- Queued
- Running
- Blocked
- Failed
- Done

Sync rules:
- Create/update external tasks from OpenClaw task records.
- Add comments for terminal failures and stalled work.
- Keep OpenClaw task IDs or run IDs in the external task body.
- Never store API keys, tokens, or full private transcripts in the external tool.
- If OpenClaw and the external board disagree, trust OpenClaw.

Heartbeat reconciliation:
- Run a lightweight check for failed, stale, or blocked work.
- Alert only when action is needed.
- Reply HEARTBEAT_OK when nothing needs attention.

Before implementing:
- Show the data fields you plan to store externally.
- Show the exact commands/tools you will use.
- Ask before writing any credentials.
```

## Todoist Credentials Example

If you use Todoist, store the token outside repo-tracked files:

```bash
mkdir -p ~/.openclaw/credentials
printf '%s\n' '<TODOIST_API_TOKEN>' > ~/.openclaw/credentials/todoist
chmod 700 ~/.openclaw/credentials
chmod 600 ~/.openclaw/credentials/todoist
```

## Reconciliation Checklist

- `openclaw tasks audit` has no unexpected issues.
- External board entries include OpenClaw task IDs or run IDs.
- Failed task summaries do not leak secrets.
- Terminal tasks are not kept active externally.
- Heartbeat reports only actionable mismatches.

## ClawHub Note

If you find a task-management skill on ClawHub, treat it as source material. Read it, then rebuild your own local bridge with the minimum API access needed.

## Related

- [Heartbeat example](heartbeat-example.md)
- [Spawning patterns](spawning-patterns.md)
- [Security hardening](security-hardening.md)
