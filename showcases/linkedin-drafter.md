# LinkedIn Drafter

**Category:** Content  
**Example Model:** Premium tier (Sonnet, Opus, GPT-4/5, etc.)  
**Updated:** 2026-02-09

> **HOW TO USE:** Copy the cron job and prompt below. Replace `[PLACEHOLDERS]` with your values. Creates draft posts weekly for your review before posting.

## Quick Start

### 1. Prerequisites

- [ ] Notion account (or Airtable, Google Sheets) with database for drafts
- [ ] Activity logging system (memory files, git commits, or manual notes)
- [ ] Task/activity tracking (Todoist, Trello, or calendar)
- [ ] Voice/persona guidelines (optional - can use generic professional tone)

### 2. Copy This Cron Job

Paste into your gateway config's `cron.jobs` section:

```json
{
  "name": "linkedin-drafter",
  "schedule": {
    "kind": "cron",
    "expr": "0 10 * * 2",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Draft 2-3 LinkedIn posts. Review my recent activity from [YOUR_ACTIVITY_SOURCE]. Identify post-worthy insights. Draft in my voice: direct, no fluff, professional but human, no em dashes/emojis. Rotate topics: [YOUR_TOPIC_1], [YOUR_TOPIC_2], [YOUR_TOPIC_3]. Save drafts to [YOUR_DATABASE] with status 'Draft'."
  },
  "sessionTarget": "isolated"
}
```

**Replace:**
- `[YOUR_ACTIVITY_SOURCE]` - Where to look for content (e.g., "memory files from last 7 days", "Todoist completed tasks", "GitHub commits")
- `[YOUR_TOPIC_1/2/3]` - Your content pillars (e.g., "infrastructure", "homelab", "cost optimization")
- `[YOUR_DATABASE]` - Where to save drafts (e.g., "Notion LinkedIn Content database")

### 3. Configure Tools

```yaml
tools:
  notion: {}      # Or airtable, sheets
  memory_search: {}  # If using memory files
  todoist: {}     # Or your task manager
```

### 4. Test It

```bash
openclaw cron run linkedin-drafter
```

---

## What This Does

**Problem:** Maintaining LinkedIn visibility requires consistent posting, but writing posts takes time and mental energy. Hard to maintain voice when delegating.

**Solution:** Weekly automated drafting. Every Tuesday at 10 AM UTC, reviews your recent work, identifies insights, drafts 2-3 posts in your voice, saves to database for your review. You post the best one.

## Full Prompt (Detailed)

```
Draft LinkedIn posts for me.

**My voice characteristics:**
- Direct, no fluff, grounded tone
- Professional but human (not corporate)
- Specific examples over general advice
- No em dashes, no emojis, no AI-sounding language
- Clear structure, direct language

**Content topics (rotate through):**
1. [YOUR_TOPIC_1] - [Brief description]
2. [YOUR_TOPIC_2] - [Brief description]
3. [YOUR_TOPIC_3] - [Brief description]

**Process:**
1. Review my recent activity from [YOUR_ACTIVITY_SOURCE]
2. Check what I'm actively working on
3. Identify authentic insights worth sharing
4. Draft 2-3 posts (150-300 words each)
5. Vary formats: observation, lesson learned, question, behind-the-scenes

**For each draft:**
- Hook in first line
- Specific example or story
- Clear takeaway or question
- No hashtags, no "engage with this post" language

Save to [YOUR_DATABASE] with:
- Title: Post topic
- Content: Full draft
- Status: Draft
- Topic: Category
- Created: Today's date
```

## Activity Source Options

**Memory Files:**
```
Review memory files from last 7 days at [PATH_TO_MEMORY].
Look for: decisions, lessons, experiments, challenges overcome.
```

**Task Manager:**
```
Check completed tasks from last 7 days in [YOUR_TASK_SYSTEM].
Look for: project completions, problems solved, new tools tried.
```

**Git Activity:**
```
Review recent commits and PRs from [GITHUB_USERNAME] repositories.
Look for: interesting technical decisions, refactoring work, new features.
```

**Calendar:**
```
Check calendar from last 7 days for meetings, workshops, learning sessions.
```

## Notion Database Schema

**Table: LinkedIn Content**

| Field | Type | Notes |
|-------|------|-------|
| Title | Title | Post topic/summary |
| Content | Text | Full draft text |
| Status | Select | Draft / Ready / Posted |
| Topic | Select | [YOUR_TOPIC_1] / [YOUR_TOPIC_2] / [YOUR_TOPIC_3] |
| Created | Date | Auto-filled |
| Posted | Date | Fill when posted |

## Alternative: Airtable

Same schema as Notion. Use Airtable API:
```yaml
tools:
  airtable:
    api_key: "${AIRTABLE_API_KEY}"
    base_id: "${AIRTABLE_BASE_ID}"
```

## Voice Guidelines

If you don't have a voice doc, add this to your prompt:

```
**Writing style:**
- No em dashes (use commas or periods)
- No emojis
- Avoid filler phrases like "Great question!" or "I'd be happy to help!"
- Avoid academic/corporate buzzwords
- Sound like a competent professional talking to peers
- One clear idea per post
```

Or create a `VOICE.md` file and reference it:
```
Read VOICE.md for my writing style guidelines, then draft posts.
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Generic posts | No recent activity logged | Start logging work in memory files or tasks |
| Wrong tone | Voice guidelines unclear | Add more specific examples to prompt |
| Too similar | Not enough topic variety | Expand topic list, add new categories |
| All drafts about same thing | Activity source too narrow | Pull from multiple sources (git + tasks + calendar) |

## Lessons Learned

### What Worked

- **Source from actual work** - Posts based on real activity are more authentic
- **Save to database, don't auto-post** - Review buffer prevents bad posts
- **Tuesday timing** - Early week energy, time to review before posting

### What Did Not Work

- **Auto-posting** - Some drafts needed heavy editing
- **Generic topics** - "5 tips for X" performed worse than specific stories
- **Daily schedule** - Too frequent; weekly is better

### Gotchas

- **Memory gaps** - If you don't log work, agent has nothing to source
- **Sensitive topics** - Avoid discussing job search, compensation, etc.
- **Timing** - Posts perform better Tuesday-Thursday, 8-10 AM in your timezone

## Variations

**Twitter/X Crosspost:**
Add to prompt: "Also create Twitter versions (280 chars, thread if needed)."

**Thread Format:**
Add: "For one draft, break into 5-tweet thread."

**Analytics Review:**
Create second job: "Review last week's posts, report engagement."

## Security

- **Never auto-post** - Always review before publishing
- **No sensitive data** - Don't source from confidential work
- **Database is private** - Keep drafts in private Notion/Airtable

## Related

- [daily-brief](daily-brief.md) - Can surface content ideas
- [idea-pipeline](idea-pipeline.md) - Research insights make good topics

## Changelog

- **2026-02-09** - Initial version, Tuesdays 10 AM
- **2026-02-10** - Generalized for public sharing
