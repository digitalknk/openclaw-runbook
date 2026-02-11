# [Use Case Name]

**Category:** [Daily Automation / Content / Infrastructure / Development]  
**Example Model:** [Premium / Balanced / Cheap tier - use what you have]  
**Updated:** [YYYY-MM-DD]

> **HOW TO USE THIS:** Copy the code blocks below into your OpenClaw config. Replace bracketed placeholders like `[YOUR_LOCATION]` with your actual values. The "Quick Start" section has everything you need to get running.

## Quick Start

### 1. Prerequisites (check these first)

- [ ] [Tool 1] configured
- [ ] [Tool 2] API key in `~/.openclaw/credentials/`
- [ ] [External service] account

### 2. Copy This Cron Job

Paste this into your gateway config's `cron.jobs` section:

```json
{
  "name": "[use-case-name]",
  "schedule": {
    "kind": "cron",
    "expr": "[minute] [hour] * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "[PROMPT_TEXT]"
  },
  "sessionTarget": "isolated"
}
```

**Replace:**
- `[use-case-name]` - Name for your job (e.g., "daily-brief")
- `[minute] [hour]` - When to run (e.g., "30 9" for 9:30 AM UTC)
- `[PROMPT_TEXT]` - The prompt from section 3 below

### 3. Copy This Prompt

```
[Paste your complete prompt here]

Example:
Generate a daily brief for me.

1. WEATHER: Get current weather for [YOUR_LOCATION]
2. CALENDAR: Check calendar for next 24 hours
3. TASKS: Get active tasks from [YOUR_TASK_SYSTEM]

Format as a clean, scannable message.
```

**Replace:**
- `[YOUR_LOCATION]` - Your city (e.g., "New York, NY")
- `[YOUR_TASK_SYSTEM]` - Your task manager

### 4. Configure Tools

Make sure these tools are available to your agent:

```yaml
# In your gateway config
tools:
  weather: {}  # or your weather provider
  calendar: {}  # or your calendar provider
  message: {}   # Telegram, Discord, etc.
```

### 5. Test It

Run manually first:
```bash
openclaw cron run [use-case-name]
```

---

## What This Does

**Problem:** [One sentence about the pain point]

**Solution:** [One sentence about what this automation does]

## Full Prompt

Complete prompt with all details:

```
[Paste full prompt with all sections, error handling, etc.]
```

## Configuration Reference

### Cron Expression Examples

| Schedule | Expression |
|----------|------------|
| Daily at 9:30 AM UTC | `30 9 * * *` |
| Weekly on Sunday 8 AM | `0 8 * * 0` |
| Every 6 hours | `0 */6 * * *` |
| Weekdays at 10 AM | `0 10 * * 1-5` |

### Model Selection

| Task Type | Recommended Model | Why |
|-----------|-------------------|-----|
| Simple formatting | Haiku / Flash-Lite | Fast, cheap |
| General tasks | Sonnet / Gemini 2.5 | Good balance |
| Complex reasoning | Opus / GPT-5.2 | Best quality |

### Tool Alternatives

| Function | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Weather | Built-in | OpenWeatherMap | NOAA |
| Calendar | Google Calendar | Nextcloud | CalDAV |
| Tasks | Todoist | Trello | File-based |
| Delivery | Telegram | Discord | Email |

## Customization Guide

### Changing the Schedule

Edit the `expr` field in the cron job:
- `30 9 * * *` = 9:30 AM daily
- `0 */6 * * *` = Every 6 hours
- `0 8 * * 1` = Monday 8 AM weekly

### Changing the Delivery Channel

**To Telegram:**
```json
{
  "message": "[your prompt] Deliver results to Telegram chat [YOUR_CHAT_ID]."
}
```

**To Discord:**
```json
{
  "message": "[your prompt] Deliver results to Discord channel [CHANNEL_ID]."
}
```

**To Email:**
```json
{
  "message": "[your prompt] Email results to [YOUR_EMAIL]."
}
```

### Adding New Data Sources

Add to the prompt:
```
4. NEW_SECTION: [What to check]
   - [Detail 1]
   - [Detail 2]
```

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| Job not running | Timezone mismatch | Check `tz` field matches your timezone |
| Missing data | Tool not configured | Verify tool is in gateway config |
| Wrong output | Prompt unclear | Make prompt more specific |
| Rate limited | Too frequent | Increase interval between runs |

## Lessons Learned

### What Worked Well

- [Technique that was effective]

### What Did Not Work

- [Approach you abandoned]

### Gotchas to Watch For

- [Rate limits, timing issues, etc.]

## Security Notes

Review these before deploying:

- [ ] No hardcoded secrets in prompts
- [ ] API keys in `~/.openclaw/credentials/` not in config
- [ ] Sensitive commands require confirmation (if applicable)
- [ ] Output doesn't leak personal data

## Variations

**Alternative approach 1:** [Brief description]

**Alternative approach 2:** [Brief description]

## Related

- [Link to related showcase 1]
- [Link to related showcase 2]

## Changelog

- **[YYYY-MM-DD]** - Initial version by [author]
- **[YYYY-MM-DD]** - [Change description]

---

**Submit your own:** Copy this template, fill it out, and submit a PR. Focus on making it copy-paste ready with clear `[PLACEHOLDERS]`.
