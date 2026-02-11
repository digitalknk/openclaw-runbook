# Daily Brief

**Category:** Daily Automation  
**Example Model:** Balanced tier (Sonnet, Gemini Flash, etc.)  
**Updated:** 2026-02-09

> **HOW TO USE:** Copy the cron job and prompt below into your OpenClaw config. Replace `[PLACEHOLDERS]` with your actual values. Test with `openclaw cron run daily-brief`.

## Quick Start

### 1. Prerequisites

- [ ] Weather tool configured (built-in, no API key needed)
- [ ] Calendar access (Google Calendar, Nextcloud, or CalDAV)
- [ ] Task manager with API (Todoist, Trello, or file-based)
- [ ] Delivery channel configured (Telegram bot, Discord, or email)

### 2. Copy This Cron Job

Paste into your gateway config's `cron.jobs` section:

```json
{
  "name": "daily-brief",
  "schedule": {
    "kind": "cron",
    "expr": "30 9 * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Generate a daily brief. 1) Get weather for [YOUR_CITY]. 2) Check calendar for next 24 hours. 3) Get active tasks from [YOUR_TASK_SYSTEM]. 4) Check for stalled tasks >24h. Format as clean, scannable message with clear headers. Deliver to [YOUR_CHANNEL]."
  },
  "sessionTarget": "isolated"
}
```

**Replace:**
- `[YOUR_CITY]` - Your location (e.g., "New York, NY")
- `[YOUR_TASK_SYSTEM]` - Your task manager (e.g., "Todoist", "Trello")
- `[YOUR_CHANNEL]` - Where to deliver (e.g., "Telegram chat [CHAT_ID]" or "Discord channel [CHANNEL_ID]")

### 3. Configure Tools

Add to your gateway config:

```yaml
tools:
  weather: {}
  calendar: {}  # or your specific calendar tool
  message: {}   # Telegram, Discord, or email
```

### 4. Test It

```bash
openclaw cron run daily-brief
```

---

## What This Does

**Problem:** Starting the day requires checking multiple apps: weather, calendar, tasks. Easy to miss something important.

**Solution:** Automated morning summary delivered at 9:30 AM UTC via your preferred channel. Combines weather, calendar events (next 24h), active tasks, and reminders into one scannable message.

## Full Prompt (Detailed)

Use this if you want more control over formatting:

```
Generate a daily brief for me.

1. WEATHER: Get current weather for [YOUR_CITY]
   - Current temp and condition
   - High/low for today
   - Any alerts or notable conditions

2. CALENDAR: Check calendar for next 24 hours
   - List all events with times
   - Highlight events starting within 2 hours
   - Note any all-day events

3. TASKS: Get active tasks from [YOUR_TASK_SYSTEM]
   - List top 3-5 priority items
   - Note any tasks marked as waiting

4. REMINDERS: Check if anything needs attention
   - Tasks stalled >24h
   - Upcoming deadlines

Format as a clean, scannable message with clear headers.
Skip sections that have nothing notable.
Keep it brief enough to read in 30 seconds.

Deliver to [YOUR_CHANNEL].
```

## Configuration Options

### Delivery Channels

**Telegram (most popular):**
```
Deliver to Telegram chat [CHAT_ID].
```
Get chat ID from @userinfobot.

**Discord:**
```
Deliver to Discord channel [CHANNEL_ID].
```
Enable developer mode in Discord, right-click channel, "Copy ID".

**Email:**
```
Email results to [YOUR_EMAIL] with subject "Daily Brief [DATE]".
```

**Slack:**
```
Deliver to Slack channel [CHANNEL_NAME] via webhook.
```

### Calendar Options

**Google Calendar (gcalcli):**
```bash
# Install
pip install gcalcli

# Authenticate
gcalcli list
```

**Nextcloud (khal + vdirsyncer):**
```bash
# Install
pip install khal vdirsyncer

# Configure ~/.config/vdirsyncer/config
# Configure ~/.config/khal/config
```

**CalDAV:**
Use any CalDAV client that outputs to CLI or API.

### Task Manager Options

**Todoist:**
```bash
pip install todoist-api-python
export TODOIST_API_TOKEN="your-token"
```

**Trello:**
Use Trello REST API with key/token.

**File-based:**
Tasks in markdown files, parsed by custom script.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Job not running at right time | Wrong timezone | Change `"tz": "UTC"` to your timezone (e.g., `"America/New_York"`) |
| Missing calendar events | Sync delay | Calendar sync runs on its own schedule; brief might miss very recent additions |
| Too many tasks shown | No filtering | Add "top 3" or filter by project/label to your prompt |
| Formatting looks bad | Channel limitations | Some channels (Telegram, Discord) don't support tables; use bullets |

## Customization

### Change Schedule

Edit the `expr` field:
- `"0 7 * * *"` = 7:00 AM (earlier)
- `"0 12 * * *"` = 12:00 PM (later)
- `"0 9 * * 1-5"` = Weekdays only

### Add Sections

Add to the prompt:
```
5. STOCKS: Check portfolio value
6. NEWS: Get headlines from [SOURCE]
```

### Weekend Version

Create separate job for Saturdays:
```json
{
  "name": "weekend-brief",
  "schedule": { "expr": "30 9 * * 6" },  // Saturdays only
  "payload": {
    "message": "Generate weekend brief: Include personal projects, hobby tasks."
  }
}
```

## Lessons Learned

### What Worked

- **Balanced model (Sonnet)** - Fast, cheap, reliable formatting
- **Isolated session** - Keeps main session uncluttered
- **Consistent time** - Creates habit and expectation

### Gotchas

- Calendar sync delays are real - don't expect minute-by-minute accuracy
- Large task lists hit rate limits - filter aggressively
- Skip empty sections entirely rather than saying "nothing found"

## Security

- No secrets in the prompt
- All API keys in `~/.openclaw/credentials/`
- Isolated session prevents session pollution

## Related

- [idea-pipeline](idea-pipeline.md) - Overnight research on ideas
- [tech-discoveries](tech-discoveries.md) - Weekly tech news curation

## Changelog

- **2026-02-09** - Initial version
- **2026-02-10** - Generalized for public sharing
