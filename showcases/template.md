# [Use Case Name]

**Category:** [Daily Automation / Content / Infrastructure / Development]
**Example Model:** [cheap / balanced / strong / local]
**Updated:** [YYYY-MM-DD]
**Source:** [Original / Community contribution / External URL]
**Ownership note:** [Personal runbook example / Community-contributed showcase / External project review]

Use this template for automations that have been tested manually. Replace every bracketed placeholder before running the job.

## Quick Start

### 1. Prerequisites

- [ ] [Tool or plugin] configured
- [ ] [Channel] configured and allowlisted
- [ ] Provider auth profile set up, if this job needs an API model
- [ ] Secrets stored outside the published config

### 2. Add The Cron Job

Use the CLI:

```bash
openclaw cron add \
  --name "[use-case-name]" \
  --cron "[minute] [hour] * * *" \
  --timezone "[TIMEZONE]" \
  --session isolated \
  --message "[PROMPT_TEXT]"
```

Replace:

- `[use-case-name]` with a short job name.
- `[minute] [hour]` with the cron expression.
- `[TIMEZONE]` with a real timezone such as `America/Los_Angeles`.
- `[PROMPT_TEXT]` with the prompt below.

### 3. Prompt

```text
[Paste your complete prompt here.]

Requirements:
1. [What to check]
2. [What to produce]
3. [Where to deliver]
4. [What to skip]

Return HEARTBEAT_OK if nothing needs attention.
```

### 4. Test

```bash
openclaw cron list
openclaw cron run <job-id> --wait
openclaw tasks list
```

Watch the output. Fix the prompt before enabling repeated runs.

## What This Does

**Problem:** [One concrete sentence.]

**Solution:** [One concrete sentence.]

## Configuration Notes

### Schedule Examples

| Schedule | Cron |
| --- | --- |
| Daily at 7 AM | `0 7 * * *` |
| Weekdays at 9 AM | `0 9 * * 1-5` |
| Sunday at 8 AM | `0 8 * * 0` |
| Every six hours | `0 */6 * * *` |

### Model Selection

| Task Type | Suggested Tier |
| --- | --- |
| Status check | cheap |
| Normal research | balanced |
| Public writing | strong |
| Private local processing | local |

Use model IDs from your own `agents.defaults.models`; do not copy provider names from an example unless they exist in your config.

### Delivery Options

Telegram:

```text
Deliver the result to Telegram chat [CHAT_ID].
```

Email:

```text
Save a draft email to [DESTINATION]. Do not send it without approval.
```

Task ledger:

```text
Create or update OpenClaw tasks for each actionable item.
```

## Troubleshooting

| Problem | Likely Cause | Fix |
| --- | --- | --- |
| Job does not run | Disabled cron or wrong timezone | Check `openclaw cron list` |
| Wrong model | Job inherits defaults | Set an explicit agent/model path |
| Missing data | Tool or channel not configured | Check plugin/channel config |
| Too much output | Prompt too broad | Add limits and skip rules |
| Repeated noise | No no-op signal | Tell it to return `HEARTBEAT_OK` |

## Lessons Learned

### What Worked Well

- [Technique that was effective]
- [Prompt constraint that improved output]
- [Operational habit that made this reliable]

### What Did Not Work

- [Approach you abandoned]
- [Source that was too noisy]
- [Schedule that created too much output]

### Gotchas To Watch For

- [Rate limits, timing issues, channel formatting, stale data, or auth failures]
- [Anything that made the automation look correct while silently failing]

## Variations

**Alternative schedule:** [Brief description]

**Different delivery channel:** [Brief description]

**Read-only mode:** [Brief description]

## Security Notes

- No hardcoded secrets.
- No public dashboard requirement.
- Confirm destructive commands.
- Keep remote access through Tailscale or an allowlisted messaging channel.
- Treat ClawHub as inspiration only; rebuild local skills before use.

## Related

- [OpenClaw Showcases](README.md)
- [Security hardening](../examples/security-hardening.md)
- [Heartbeat example](../examples/heartbeat-example.md)

## Changelog

- **[YYYY-MM-DD]** - Initial version by [author]
- **[YYYY-MM-DD]** - [Change description]
