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

## Related

- [daily-brief](daily-brief.md)
- [tech-discoveries](tech-discoveries.md)
