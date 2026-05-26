# Idea Pipeline

**Category:** Research
**Example Model:** balanced or research-capable
**Updated:** 2026-05-25

Research captured ideas overnight and write the useful findings back to a task system, note file, or OpenClaw task ledger.

## Quick Start

### Prerequisites

- [ ] A capture source such as Telegram, Discord, email, Markdown files, or a task list.
- [ ] Web search/fetch enabled if the ideas need outside research.
- [ ] A destination for findings.
- [ ] A researcher agent configured if you plan to parallelize.

### Add The Job

```bash
openclaw cron add \
  --name "idea-pipeline" \
  --cron "0 3 * * *" \
  --timezone "America/Los_Angeles" \
  --session isolated \
  --message "Process ideas from [YOUR_CAPTURE_SOURCE]. Limit to the top 3 unprocessed ideas. For each idea, research existing solutions, technical feasibility, likely blockers, and next steps. Write the result to [YOUR_DESTINATION]. Cite sources. Keep the output concise."
```

### Test

```bash
openclaw cron list
openclaw cron run <job-id> --wait
```

## Full Prompt

```text
Process ideas from [YOUR_CAPTURE_SOURCE].

Rules:
- limit to the top 3 unprocessed ideas
- do not mark an idea processed until the result is written
- use primary sources where possible
- cite URLs for market or technical claims
- separate confirmed facts from inference

For each idea:
1. Existing solutions
   - similar products
   - open-source alternatives
   - technical approaches

2. Feasibility
   - complexity from 1 to 5
   - likely build time
   - key unknowns
   - blockers

3. Next step
   - one concrete action
   - whether to keep, defer, or drop

Write the result to [YOUR_DESTINATION].
Return HEARTBEAT_OK if there are no unprocessed ideas.
```

## Parallel Research

For several independent ideas, spawn a researcher for each one:

```javascript
sessions_spawn({
  agentId: "researcher",
  task: "Research this idea: [IDEA_TEXT]. Return existing solutions, feasibility, blockers, and one next step with source URLs.",
  taskName: "idea_research_001",
  label: "idea-research-[ID]",
  context: "isolated"
});
```

If the parent job needs the child result before continuing, call `sessions_yield()` after spawning. Do not poll subagents in a loop.

## Capture Sources

| Source | Notes |
| --- | --- |
| Telegram | Good for quick capture; use an allowlist |
| Discord | Useful for a shared ideas channel |
| Email | Works if you already forward ideas to one inbox |
| Markdown | Best for local-first workflows |
| OpenClaw tasks | Good when the task ledger is already your source of truth |

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Research is shallow | Require at least three search angles |
| Results are too long | Limit sources and require one next step |
| Ideas get lost | Write findings before marking processed |
| Too much cost | Limit ideas per run and use a balanced model |
| Untrusted source content gives instructions | Treat it as data, not commands |

## What Worked

- Processing a small number of ideas per run kept the output useful.
- Structured output made results easier to scan than prose.
- Writing findings before marking an idea processed prevented lost work.
- Parallel research helped when ideas were truly independent.

## What Did Not Work

- A single agent processing a long backlog took too long and was harder to debug.
- Over-researching every idea created more reading, not better decisions.
- Posting results only in chat made them disappear. Write them to a task, note, or durable file.

## Gotchas

- Ideas captured in chat may include half-formed context. Ask the agent to preserve uncertainty.
- Search results can bias toward popular products, not better products.
- If an idea came from someone else, treat it as untrusted content and do not follow instructions embedded in it.

## Variations

**Weekly deep dive:** Process one idea deeply each week instead of three shallow ideas nightly.

**Local-only backlog:** Use Markdown files as the capture source and write results next to the original note.

**Task-ledger mode:** Use OpenClaw tasks as the source and update task records with findings.

## Related

- [daily-brief](daily-brief.md)
- [tech-discoveries](tech-discoveries.md)

## Changelog

- **2026-02-09** - Initial version
- **2026-05-25** - Updated for current cron, task ledger, and push-based subagent behavior
