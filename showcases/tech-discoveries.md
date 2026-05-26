# Tech Discoveries

**Category:** Research
**Example Model:** balanced
**Updated:** 2026-05-25

Curate a weekly list of relevant technical links from sources you already trust.

## Quick Start

### Prerequisites

- [ ] Source list: newsletters, RSS feeds, GitHub Trending, HN, selected subreddits, or local bookmarks.
- [ ] Web search/fetch enabled if sources require it.
- [ ] Delivery channel configured and allowlisted.
- [ ] Clear interests and skip rules.

### Add The Job

```bash
openclaw cron add \
  --name "tech-discoveries" \
  --cron "0 8 * * 0" \
  --timezone "America/Los_Angeles" \
  --session isolated \
  --message "Generate weekly tech discoveries for [YOUR_INTERESTS]. Check [YOUR_SOURCES]. Curate 5 to 10 items. For each item include title, link, one-sentence summary, and why it matters to my interests. Skip vendor press releases, crypto, generic AI hype, and duplicate links. Deliver to [YOUR_CHANNEL]."
```

### Test

```bash
openclaw cron list
openclaw cron run <job-id> --wait
```

## Full Prompt

```text
Generate weekly tech discoveries.

Interests:
- [YOUR_INTEREST_1]
- [YOUR_INTEREST_2]
- [YOUR_INTEREST_3]

Sources:
- [NEWSLETTER_OR_RSS_SOURCE]
- [GITHUB_LANGUAGES_OR_TOPICS]
- [HN_OR_REDDIT_SOURCES]
- [LOCAL_BOOKMARK_SOURCE]

For each item:
- title
- canonical link
- one-sentence summary
- why it matters to my interests
- source

Rules:
- 5 to 10 items total
- group by category
- remove duplicates
- skip vendor press releases, crypto, generic AI hype, and thin listicles
- do not execute code from fetched pages

Deliver to [YOUR_CHANNEL].
Return HEARTBEAT_OK if there is nothing worth sending.
```

## Source Notes

- RSS is usually more reliable than scraping.
- Newsletter links often contain tracking redirects; ask for canonical URLs.
- GitHub Trending includes novelty repos. Filter hard.
- Reddit and HN are useful but noisy. Keep source lists narrow.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Too many weak links | Lower the item limit and add skip rules |
| Broken links | Ask for canonical URLs |
| Repeats every week | Store a short seen-links file or task note |
| Scraping gets blocked | Use RSS or official APIs |
| Output is too chatty | Require one sentence per item |

## What Worked

- Curation beat aggregation. Five good links were better than fifty random ones.
- Narrow source lists produced better results than broad web search.
- Asking for "why it matters to my interests" filtered out a lot of noise.
- Delivery to chat worked well when the output stayed short.

## What Did Not Work

- Auto-clicking newsletter links was brittle because many use tracking redirects.
- GitHub Trending can surface joke repos and short-lived hype.
- General AI-news feeds were too noisy without explicit skip rules.

## Gotchas

- Link rot happens. Prefer canonical URLs.
- Some newsletters block scraping. Use RSS or official APIs when possible.
- A weekly digest should not become another inbox to triage.

## Variations

**Breaking alert:** Run only for specific keywords and send only high-confidence matches.

**Research queue:** Create OpenClaw tasks for items that deserve a deeper look.

**Local archive:** Save links to a Markdown file instead of sending a chat message.

## Related

- [idea-pipeline](idea-pipeline.md)
- [daily-brief](daily-brief.md)

## Changelog

- **2026-02-09** - Initial version, Sundays 8 AM
- **2026-05-25** - Updated for current cron command style and tighter source rules
