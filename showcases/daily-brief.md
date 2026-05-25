# Daily Brief

**Category:** Daily Automation
**Example Model:** balanced or cheap
**Updated:** 2026-05-25

Send a short morning brief to an allowlisted channel. This works best when the Gateway stays local or Tailscale-only and delivery happens through Telegram, Discord, email, or another configured channel.

## Quick Start

### Prerequisites

- [ ] Weather source configured.
- [ ] Calendar or task source configured, if you want those sections.
- [ ] Delivery channel configured and allowlisted.
- [ ] A cheap or balanced model available in `agents.defaults.models`.

### Add The Job

```bash
openclaw cron add \
  --name "daily-brief" \
  --cron "30 7 * * *" \
  --timezone "America/Los_Angeles" \
  --session isolated \
  --message "Generate my daily brief. Weather: [YOUR_CITY]. Calendar: next 24 hours from [YOUR_CALENDAR_SOURCE]. Tasks: top active items from [YOUR_TASK_SOURCE]. Flag anything due today or stale for more than 24 hours. Keep it short, use clear headings, skip empty sections, and deliver to [YOUR_CHANNEL]."
```

Replace:

- `[YOUR_CITY]` with your city.
- `[YOUR_CALENDAR_SOURCE]` with your calendar source.
- `[YOUR_TASK_SOURCE]` with your task source.
- `[YOUR_CHANNEL]` with the delivery target.

### Test

```bash
openclaw cron list
openclaw cron run <job-id> --wait
```

Use the job ID from `openclaw cron list`.

## Full Prompt

```text
Generate my daily brief.

Check:
1. Weather for [YOUR_CITY]
   - current condition
   - high and low
   - alerts or notable travel conditions

2. Calendar for the next 24 hours from [YOUR_CALENDAR_SOURCE]
   - meetings with times
   - events starting within 2 hours
   - all-day events

3. Tasks from [YOUR_TASK_SOURCE]
   - top 3 to 5 active items
   - due today
   - stale for more than 24 hours

Format:
- clear headings
- short bullets
- no tables unless the delivery channel handles them well
- skip empty sections
- keep it readable in 30 seconds

Deliver to [YOUR_CHANNEL].
Return HEARTBEAT_OK only if there is truly nothing to report.
```

## Notes

- Use an isolated session so the brief does not pollute the main conversation.
- Use a cheaper model if the sources are simple and stable.
- Keep the dashboard off the public internet. Use Tailscale for Control UI access, or use a local Gateway plus a messaging channel for remote briefs.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Runs at the wrong time | Check the timezone in `openclaw cron list` |
| Too verbose | Add a hard section limit and word limit |
| Empty sections are noisy | Tell the prompt to skip empty sections |
| Channel formatting is poor | Avoid Markdown tables and long nested lists |
| Job cannot access data | Check plugin/channel config and auth profiles |

## Related

- [idea-pipeline](idea-pipeline.md)
- [tech-discoveries](tech-discoveries.md)
