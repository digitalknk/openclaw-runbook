# LinkedIn Drafter

**Category:** Content
**Example Model:** strong writing model
**Updated:** 2026-05-25

Draft posts for review. Do not auto-post.

## Quick Start

### Prerequisites

- [ ] Activity source: memory files, task history, git commits, notes, or calendar.
- [ ] Draft destination: Notion, Airtable, Markdown file, Google Doc, or task ledger.
- [ ] Voice notes, if you have them.
- [ ] A model that is good at writing in a constrained style.

### Add The Job

```bash
openclaw cron add \
  --name "linkedin-drafter" \
  --cron "0 10 * * 2" \
  --timezone "America/Los_Angeles" \
  --session isolated \
  --message "Draft 2 LinkedIn posts from [YOUR_ACTIVITY_SOURCE]. Use my voice: direct, concrete, no hype, no em dashes, no emoji. Topics to prefer: [TOPIC_1], [TOPIC_2], [TOPIC_3]. Save drafts to [YOUR_DRAFT_DESTINATION] with status Draft. Do not post."
```

### Test

```bash
openclaw cron list
openclaw cron run <job-id> --wait
```

## Full Prompt

```text
Draft 2 LinkedIn posts for review.

Source material:
- [YOUR_ACTIVITY_SOURCE]

Topics to prefer:
- [TOPIC_1]
- [TOPIC_2]
- [TOPIC_3]

Voice:
- direct
- grounded
- specific examples over general advice
- professional but plain
- no em dashes
- no emoji
- no "5 lessons" filler unless the source material genuinely supports it
- no claims that are not in the source material

For each draft:
- first line should state the point plainly
- 150 to 300 words
- one idea per post
- include a specific example or detail
- end without engagement bait

Save to [YOUR_DRAFT_DESTINATION] with:
- title
- content
- source notes used
- status: Draft

Do not publish, schedule, or send externally.
```

## Good Sources

| Source | What It Produces |
| --- | --- |
| Memory files | Decisions, lessons, patterns |
| Git commits | Concrete technical work |
| Task history | Shipped work and blockers |
| Calendar | Talks, meetings, workshops |
| Notes | Raw thinking and examples |

## Security

- Never auto-post.
- Do not use confidential work.
- Review drafts manually.
- Keep draft storage private.
- Avoid copying private memory into public posts.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Drafts are generic | Add richer source notes |
| Voice is off | Add examples of approved posts |
| Too much polish | Tell it to preserve rough specifics |
| Sensitive details leak | Add a redaction checklist |
| Repeated topics | Rotate topic preferences |

## Related

- [daily-brief](daily-brief.md)
- [idea-pipeline](idea-pipeline.md)
