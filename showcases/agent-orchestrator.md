# Agent Orchestrator

**Category:** Development
**Example Model:** strong reasoning model
**Updated:** 2026-05-25

Use an orchestrator when the hard part is routing work, not doing the work. It should choose the right local tool, subagent, or workflow and leave a short audit trail.

## What It Solves

Coding tasks are not all the same. A typo, a docs refresh, a multi-file refactor, and a production incident should not go through the same path. The orchestrator pattern makes that routing explicit.

## Agent Instructions

Add to `AGENTS.md`:

```markdown
## Orchestrator Agent

When spawned as `orchestrator`:

- classify the task before acting
- choose the smallest capable tool or subagent
- check whether the task needs current docs, local repo context, or user approval
- do not write code directly unless explicitly asked
- do not run destructive commands
- do not publish, send, delete, reboot, or merge without approval
- record the selected path and why

Routing:
- simple edit: use the main coding agent or a lightweight coding subagent
- repo-wide change: use a coding agent with full repo context
- current docs needed: use a researcher first, then coding agent
- writing-only work: use writer
- validation-only work: use monitor or test runner
- risky operation: ask the user first

Return:
- selected route
- reason
- expected risk
- next action taken
```

## Config Example

```json
{
  "agents": {
    "list": [
      {
        "id": "orchestrator",
        "workspace": "~/.openclaw/workspace",
        "model": {
          "primary": "zai/glm-5.1",
          "fallbacks": ["openrouter/free"]
        }
      },
      {
        "id": "researcher",
        "workspace": "~/.openclaw/workspace"
      },
      {
        "id": "monitor",
        "workspace": "~/.openclaw/workspace"
      }
    ]
  }
}
```

Replace model IDs with entries from your own model catalog.

## Spawn Example

```javascript
sessions_spawn({
  agentId: "orchestrator",
  task: "Route this task: update the OpenClaw runbook against the local docs snapshot and preserve the user's Tailscale-first stance.",
  taskName: "route_runbook_refresh",
  label: "route-runbook-refresh",
  context: "isolated"
});
```

## Routing Matrix

| Task | Route |
| --- | --- |
| typo or small docs edit | lightweight coding agent |
| config/schema update | coding agent plus validation |
| current external facts | researcher, then writer/coder |
| long-running monitoring | monitor with `HEARTBEAT_OK` |
| public writing | writer and user review |
| destructive infrastructure change | user approval first |

## Quota And Cost

Use provider dashboards for hard spend limits. OpenClaw config can steer usage, but provider-side limits are still the real stop.

Do not assign the strongest model to routine status checks. Use explicit cheaper models for monitor agents and cron jobs.

## What Worked

- Making routing explicit reduced surprise costs.
- Keeping a short audit trail made bad routing decisions easier to fix.
- Using isolated sessions for specialist work kept the main conversation easier to follow.
- A small set of routes worked better than trying to classify every possible task.

## What Did Not Work

- Letting the orchestrator do the work directly defeated the point of routing.
- Sending every task to the strongest model burned quota without improving routine work.
- Hiding the selected route made debugging harder.

## Tool Selection Matrix

| Situation | Better Route |
| --- | --- |
| Small text or docs edit | main coding agent |
| Requires current provider docs | researcher first |
| Multi-file code change | coding agent with repo context |
| Long-running comparison | subagent with isolated context |
| Public-facing prose | writer and user review |
| Risky command or deployment | ask user first |

## Security

- The orchestrator should route, not hide decisions.
- Each spawned agent should have a narrow task.
- Use isolated sessions for long-running work.
- Keep ClawHub disabled unless you are only inspecting source.
- Do not let a third-party skill define your routing policy.

## Related

- [agent prompts](../examples/agent-prompts.md)
- [spawning patterns](../examples/spawning-patterns.md)
- [idea pipeline](idea-pipeline.md)

## Changelog

- **2026-02-09** - Initial version with tool routing
- **2026-05-25** - Updated for current subagent behavior and explicit routing notes
