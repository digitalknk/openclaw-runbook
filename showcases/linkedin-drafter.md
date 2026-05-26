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

## What Worked

- Drafting from actual work produced better posts than starting from generic topics.
- Saving drafts for review was safer than trying to auto-post.
- A weekly cadence was easier to review than a daily one.
- Keeping source notes with each draft made editing faster.

## What Did Not Work

- Auto-posting was a bad idea. Some drafts need heavy editing or should not be public at all.
- Asking for too many drafts produced filler.
- Generic "professional" tone made posts sound interchangeable.

## Gotchas

- Memory gaps matter. If you do not log the work, the agent has nothing specific to use.
- Private client, employer, or product details can leak if the prompt does not include a redaction pass.
- Timing advice changes. Do not overfit the cron schedule to old social-media advice.

## Variations

**Short-form draft:** Ask for one short post under 120 words.

**Technical thread:** Ask for a structured technical explanation, then manually adapt it before posting.

**Internal newsletter:** Use the same source material but save it as a private team update.

## Related

- [daily-brief](daily-brief.md)
- [idea-pipeline](idea-pipeline.md)

## Changelog

- **2026-02-09** - Initial version, Tuesdays 10 AM
- **2026-05-25** - Updated for current cron command style and review-only publishing
