# Idea Pipeline

**Category:** Research  
**Example Model:** Research tier (Kimi, Gemini Flash, etc.)  
**Updated:** 2026-02-09

> **HOW TO USE:** Copy the cron job and prompt below. Replace `[PLACEHOLDERS]` with your values. This runs overnight and researches ideas you captured during the day.

## Quick Start

### 1. Prerequisites

- [ ] Idea capture method (Telegram bot, Discord channel, email, or notebook)
- [ ] Task manager with API (Todoist, Trello, Asana, or file-based)
- [ ] Web search tool configured (Brave, Serper, or alternative API key)
- [ ] Sub-agent spawning enabled

### 2. Copy This Cron Job

Paste into your gateway config's `cron.jobs` section:

```json
{
  "name": "idea-pipeline",
  "schedule": {
    "kind": "cron",
    "expr": "0 3 * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Process ideas from [YOUR_CAPTURE_METHOD]. For each idea: 1) Search web for existing solutions and market landscape. 2) Analyze technical feasibility (complexity 1-5, estimated time, blockers). 3) Write summary to [YOUR_TASK_SYSTEM] with findings, top 3 similar solutions, feasibility assessment, and next steps. Be concise."
  },
  "sessionTarget": "isolated"
}
```

**Replace:**
- `[YOUR_CAPTURE_METHOD]` - How you capture ideas (e.g., "Telegram bot", "Discord #ideas channel")
- `[YOUR_TASK_SYSTEM]` - Where to write results (e.g., "Todoist", "Trello")

### 3. Configure Tools

```yaml
tools:
  web_search: {}  # Brave, Serper, etc.
  message: {}     # To read captured ideas
  todoist: {}     # Or your task manager
```

### 4. Test It

```bash
openclaw cron run idea-pipeline
```

---

## What This Does

**Problem:** Ideas captured throughout the day need research to validate feasibility. Manual research gets skipped, leaving good ideas abandoned.

**Solution:** Overnight research agent. Runs at 3 AM UTC, researches each captured idea, analyzes feasibility, and updates tasks with summaries. Results ready in the morning.

## Full Prompt (Detailed)

```
Process the ideas captured from [YOUR_CAPTURE_METHOD].

For each idea:
1. SEARCH: Search web for
   - Existing products/services solving similar problem
   - Open source alternatives
   - Technical approaches others used
   - Market size or demand indicators

2. ANALYZE feasibility:
   - Technical complexity (1-5 scale)
   - Estimated build time
   - Key technical decisions needed
   - Potential blockers

3. WRITE summary to [YOUR_TASK_SYSTEM]:
   - Brief overview of findings
   - Top 3 similar solutions found with links
   - Feasibility assessment
   - Recommended next steps

Be concise. Focus on actionable insights, not exhaustive research.
Limit to top 3 ideas per night by priority.
```

## Capture Method Options

**Telegram Bot (recommended):**
1. Create bot via @BotFather
2. User forwards ideas to bot
3. Bot saves to task manager with label `idea-pipeline`

**Discord Channel:**
- Dedicated channel (e.g., #ideas)
- Webhook monitors messages
- Auto-creates tasks

**Email:**
- Dedicated address: ideas@yourdomain.com
- Subject = idea title
- Body = details

**Notebook/Files:**
- Ideas written to markdown files
- Agent scans directory
- Filename = idea title

## Task Manager Integration

**Todoist:**
```python
# Label tasks for processing
tasks = api.get_tasks(label="idea-pipeline")

# After research, update with label "researched"
api.update_task(task_id, labels=["researched"])
```

**Trello:**
- Ideas go to "Backlog" list
- After research, move to "Researched" list
- Add checklist with findings

**File-based:**
```
ideas/
├── backlog/
│   └── idea-001.md
└── researched/
    └── idea-001.md  # Moved after research
```

## Parallel Processing (Advanced)

For multiple ideas, spawn sub-agents:

```javascript
// In your agent logic
for (const idea of ideas) {
  sessions_spawn({
    task: `Research: "${idea.text}". Search web, analyze feasibility, return structured summary.`,
    agentId: "researcher",
    model: "gemini"  // Cheap, fast for research
  });
}
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Research too shallow | Not enough search queries | Add "search 3 different angles" to prompt |
| Overwhelming output | Too many search results | Limit to "top 3 sources" |
| Lost ideas | Chat messages disappear | Always write results to task manager, not back to chat |
| Rate limited | Too many web searches | Add 2-3 second delays between searches |

## Lessons Learned

### What Worked

- **Spawning sub-agents** for parallel research on multiple ideas
- **Gemini Flash** - Excellent for initial research (fast, cheap)
- **Structured output** - Feasibility score + next steps easier to scan than prose

### What Did Not Work

- **Single agent processing all ideas** - Took too long, hit timeout
- **Too much research** - 10+ results per idea was overwhelming
- **Updating chat** - Messages get lost; always write to task manager

## Variations

**Weekly Deep-Dive:**
```json
{
  "name": "idea-deep-dive",
  "schedule": { "expr": "0 3 * * 0" },  // Sundays
  "payload": {
    "message": "Pick highest priority idea and do thorough research..."
  }
}
```

**Market Analysis:**
Add to prompt: "Include competitor pricing, business model analysis."

**Technical Spike:**
Add: "Generate proof-of-concept code for highest feasibility idea."

## Related

- [daily-brief](daily-brief.md) - Morning summary
- [tech-discoveries](tech-discoveries.md) - Weekly curated news

## Changelog

- **2026-02-09** - Initial version
- **2026-02-10** - Generalized for public sharing
