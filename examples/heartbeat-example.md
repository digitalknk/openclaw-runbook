# HEARTBEAT.md Example

Heartbeat is for periodic awareness. Use it for checks that can run approximately on a cadence and benefit from the agent's context.

Use cron when timing must be exact.

## Current Pattern: `tasks:` Block

OpenClaw can parse a small `tasks:` block inside `HEARTBEAT.md`. Each task has its own interval, and only due tasks are included in that heartbeat tick.

```markdown
# HEARTBEAT.md

tasks:

- name: inbox-triage
  interval: 30m
  prompt: "Check for urgent unread messages from allowlisted senders. Alert only if action is needed."
- name: calendar-scan
  interval: 2h
  prompt: "Check the next 24 hours for meetings that need prep or follow-up."
- name: task-review
  interval: 1h
  prompt: "Review active background tasks and surface stalled or failed work."
- name: system-check
  interval: 24h
  prompt: "Check gateway status, recent errors, and task audit output."

# General rules

- Keep alerts short.
- Do not repeat old alerts.
- If nothing needs attention, reply HEARTBEAT_OK.
```

## Heartbeat Config

For a low-cost heartbeat, combine an isolated session with light context:

```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "30m",
        "target": "last",
        "lightContext": true,
        "isolatedSession": true,
        "skipWhenBusy": true,
        "ackMaxChars": 300
      }
    }
  }
}
```

Notes:

- `target: "none"` runs the heartbeat without sending external messages.
- `target: "last"` sends alerts to the last external contact.
- `HEARTBEAT_OK` suppresses no-op replies.
- `lightContext: true` keeps the prompt smaller.
- `isolatedSession: true` avoids sending the full main conversation into every heartbeat.
- `skipWhenBusy: true` keeps the same agent from stacking heartbeat work on top of active nested work.

## Prompt to Build Your HEARTBEAT.md

```text
Create a small HEARTBEAT.md for my OpenClaw workspace.

Use a tasks: block instead of a custom state file.

Checks:
- inbox-triage every 30m
- calendar-scan every 2h
- task-review every 1h
- system-check every 24h

Rules:
- Alert only for actionable issues.
- Do not include secrets, tokens, or private IDs.
- If nothing needs attention, reply HEARTBEAT_OK.
- Keep each task prompt short.
```

## When to Use Cron Instead

Use cron for:

- reports that must send at a specific time;
- one-shot reminders;
- weekly or daily jobs that should run in isolated sessions;
- long tasks that should produce background task records.

Example:

```bash
openclaw cron add \
  --name "Daily brief" \
  --cron "0 7 * * *" \
  --session isolated \
  --message "Prepare my daily brief from weather, calendar, and active tasks."
```

Inspect runs with:

```bash
openclaw cron list
openclaw cron runs --id <job-id>
openclaw tasks list
```

## Related

- [Config guide](config-example-guide.md)
- [Task tracking](task-tracking-prompt.md)
- [Security hardening](security-hardening.md)
