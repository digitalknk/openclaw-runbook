# Tech Discoveries

**Category:** Research  
**Example Model:** Balanced tier (Sonnet, Gemini Flash, etc.)  
**Updated:** 2026-02-09

> **HOW TO USE:** Copy the cron job and prompt below. Replace `[PLACEHOLDERS]` with your values. Weekly curated tech news delivered to your preferred channel.

## Quick Start

### 1. Prerequisites

- [ ] Newsletter subscriptions (or RSS feeds as alternative)
- [ ] Email access (IMAP/SMTP) or RSS reader
- [ ] Web search tool configured (Brave, Serper API key)
- [ ] Delivery channel configured (Telegram, Discord, email, or Slack)

### 2. Copy This Cron Job

Paste into your gateway config's `cron.jobs` section:

```json
{
  "name": "tech-discoveries",
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * 0",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Generate tech discoveries for [YOUR_INTERESTS]. Check: 1) Newsletter emails at [YOUR_EMAIL], 2) GitHub Trending for [YOUR_LANGUAGES], 3) Hacker News top stories, 4) Reddit [YOUR_SUBREDDITS]. Curate 5-10 items. For each: title, one-sentence summary, why relevant, link. Group by category. Deliver to [YOUR_CHANNEL]. Skip: crypto, generic AI hype."
  },
  "sessionTarget": "isolated"
}
```

**Replace:**
- `[YOUR_INTERESTS]` - Your focus areas (e.g., "SRE, homelab, 3D printing")
- `[YOUR_EMAIL]` - Where newsletters arrive
- `[YOUR_LANGUAGES]` - Languages to track on GitHub (e.g., "Go, Python, Rust")
- `[YOUR_SUBREDDITS]` - Communities to check (e.g., "r/homelab, r/selfhosted")
- `[YOUR_CHANNEL]` - Where to deliver (Telegram, Discord, etc.)

### 3. Configure Tools

```yaml
tools:
  email: {}       # IMAP/SMTP access
  web_search: {}  # Brave, Serper, etc.
  browser: {}     # For HN, Reddit if needed
  message: {}     # Telegram, Discord, email
```

### 4. Test It

```bash
openclaw cron run tech-discoveries
```

---

## What This Does

**Problem:** Keeping up with tech news across multiple sources is time-consuming. Easy to miss relevant developments.

**Solution:** Weekly automated scan. Every Sunday at 8 AM UTC, aggregates discoveries from newsletters, GitHub, HN, Reddit. Curates 5-10 relevant items, delivers to your channel.

## Full Prompt (Detailed)

```
Generate weekly tech discoveries for me.

**My interests:** [YOUR_INTERESTS]

**Sources to check:**
1. NEWSLETTERS: Check emails at [YOUR_EMAIL]
   - Look for: [NEWSLETTER_1], [NEWSLETTER_2], etc.
2. GITHUB: Trending repos for [YOUR_LANGUAGES]
3. HACKER NEWS: Top stories from past week
4. REDDIT: [YOUR_SUBREDDITS]
5. PRODUCT HUNT: Top launches (optional)

**For each discovery:**
- Title and one-sentence summary
- Why it's relevant to my interests
- Link (Discord: wrap in <> to suppress embeds; Telegram: standard)
- Category tag

**Format:**
- 5-10 items max (quality over quantity)
- Group by category: SRE/DevOps, Homelab, Hardware, etc.
- Brief intro: "Tech Discoveries - [DATE]"
- Brief outro: "Happy exploring!"

Deliver to [YOUR_CHANNEL].

Skip: Enterprise vendor press releases, cryptocurrency, generic AI hype.
```

## Newsletter Options

**Recommended Newsletters:**
- **DevOps/SRE:** SRE Weekly, DevOps Weekly, KubeWeekly
- **Infrastructure:** Last Week in AWS, Console.dev
- **Maker/Hardware:** Hackaday, Adafruit, ServeTheHome
- **General Tech:** Changelog News, DevOps'ish, tldr;

**Subscribe with:**
- Dedicated email (e.g., newsletters@yourdomain.com)
- Filters to auto-label
- Forward to your agent's email

## GitHub Trending

**Languages to track:**
```
Go, Python, Rust, TypeScript
```

**Timeframe:** Weekly (past 7 days)

**Note:** GitHub Trending often includes joke repos. Human judgment helps.

## Reddit Communities

**Recommended subs:**
- r/homelab - Home server projects
- r/selfhosted - Self-hosted software
- r/homelabsales - Hardware deals
- r/buildapcsales - PC component deals
- r/MeshNetworking - Mesh networks
- r/selfhosted - Alternative to cloud services

**Tip:** Use RSS feeds (reddit.com/r/[sub]/rss) instead of scraping.

## Delivery Format

**Telegram:**
```
**Tech Discoveries - Feb 10, 2026**

**SRE / DevOps**
- Tool X released - New monitoring solution with built-in alerting
- Article Y - Deep dive into Kubernetes networking

**Homelab**
- Project Z - Open source NAS software
```

**Discord:**
```
**Tech Discoveries - Feb 10, 2026**

**SRE / DevOps**
- Tool X released - New monitoring solution
  <https://github.com/...>
```

**Email:**
Subject: "Tech Discoveries - Feb 10, 2026"
Body: Formatted HTML or markdown

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Too many items | Not filtering aggressively | Add "max 5 items" to prompt |
| Irrelevant links | Wrong subreddits/sources | Curate your source list |
| Newsletter links broken | Tracking URLs | Add "extract real URL" to prompt |
| Rate limited on Reddit | Scraping too fast | Use RSS feeds instead |

## Lessons Learned

### What Worked

- **Sunday morning timing** - Good for weekend reading
- **Chat delivery** (Telegram, Discord) - Easy to scan and click
- **Curation over aggregation** - 5-10 quality items beats 50 random links

### What Did Not Work

- **Auto-clicking newsletter links** - Many use tracking URLs that break
- **Including everything** - Without filtering, becomes noise
- **Daily schedule** - Too frequent; weekly is right cadence

### Gotchas

- **Link rot** - Some newsletter links expire
- **Reddit rate limits** - Use RSS where possible
- **GitHub Trending** - Often includes joke repos

## Variations

**Breaking News Alert:**
```json
{
  "name": "breaking-tech",
  "schedule": { "kind": "every", "everyMs": 3600000 },  // Hourly
  "payload": {
    "message": "Check for major releases (Kubernetes, Docker, etc.). If found, alert immediately."
  }
}
```

**Saved for Later:**
Add to prompt: "Create Todoist tasks for items I should investigate."

**Digest Email:**
Change delivery from chat to email for formal reading.

## Related

- [daily-brief](daily-brief.md) - Can include top discovery
- [idea-pipeline](idea-pipeline.md) - Discovered tools make good research topics

## Changelog

- **2026-02-09** - Initial version, Sundays 8 AM
- **2026-02-10** - Generalized for public sharing
