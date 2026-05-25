# Agent Prompt Examples

These examples show how to define specialist agents without tying the runbook to one provider. Use your own model IDs from `agents.defaults.models`, then set `model.primary` and `model.fallbacks` per agent.

The examples assume current OpenClaw behavior: subagents are configured through `agents.list`, inherit the workspace bootstrap that OpenClaw injects, and report back through session tools such as `sessions_yield`.

## Model Routing

Model IDs are provider-qualified strings from your catalog:

```json
{
  "agents": {
    "defaults": {
      "models": {
        "zai/glm-5.1": { "alias": "GLM" },
        "zai/glm-5-turbo": {},
        "openrouter/anthropic/claude-sonnet-4.6": {},
        "openrouter/free": {}
      },
      "model": {
        "primary": "zai/glm-5.1",
        "fallbacks": ["zai/glm-5-turbo"]
      }
    }
  }
}
```

Treat those names as examples. A good model chain usually has:

- A primary model that is strong enough for the task.
- At least one fallback from a different provider or billing path.
- Cheaper models for monitoring and repetitive background work.
- No blind use of `auto` routers for jobs that need predictable behavior.

## Agent List

Add named agents under `agents.list`:

```json
{
  "agents": {
    "list": [
      {
        "id": "monitor",
        "workspace": "~/.openclaw/workspace",
        "model": {
          "primary": "openrouter/free",
          "fallbacks": ["zai/glm-5-turbo"]
        }
      },
      {
        "id": "researcher",
        "workspace": "~/.openclaw/workspace",
        "model": {
          "primary": "zai/glm-5.1",
          "fallbacks": ["openrouter/free"]
        }
      },
      {
        "id": "writer",
        "workspace": "~/.openclaw/workspace",
        "model": {
          "primary": "openrouter/anthropic/claude-sonnet-4.6",
          "fallbacks": ["zai/glm-5.1"]
        }
      }
    ]
  }
}
```

Use one shared workspace when the agents should read the same `AGENTS.md`, `TOOLS.md`, memory files, and local runbooks. Give an agent its own workspace only when isolation is intentional.

## Shared Instructions

Put role instructions in `~/.openclaw/workspace/AGENTS.md`:

```markdown
# Agent Instructions

## Monitor Agent

When spawned as `monitor`:

- Check only the requested service, cron job, queue, or file.
- Prefer read-only commands and status tools.
- Report only actionable problems.
- Return `HEARTBEAT_OK` when nothing needs attention.
- Do not spawn more agents.

## Researcher Agent

When spawned as `researcher`:

- Gather facts from named sources first.
- Use web search only when local/source material is missing or stale.
- Cite URLs for factual claims.
- Separate confirmed facts from inference.
- Keep findings concise enough for the parent session to use.

## Writer Agent

When spawned as `writer`:

- Draft in the user's stated voice.
- Use concrete details from the source material.
- Avoid hype, filler, em dashes, and broad claims that are not supported.
- Do not send or publish external messages without explicit approval.

## Coordinator Agent

When spawned as `coordinator`:

- Break the task into independent pieces.
- Spawn specialists only when they reduce risk or time.
- Prefer isolated sessions for long-running work.
- Ask for user approval before destructive, public, or expensive actions.
- Synthesize results and return one final answer to the parent session.
```

## Spawn Patterns

Use `sessions_spawn` for work that benefits from a separate context:

```javascript
sessions_spawn({
  agentId: "researcher",
  task: "Research current VPS options under $20/month. Return a table with provider, region, CPU, RAM, storage, bandwidth, price, and source URL.",
  taskName: "vps_research",
  label: "vps-research",
  context: "isolated"
});
```

When the parent needs the child result before continuing, yield after spawning:

```javascript
sessions_yield();
```

Do not build polling loops around subagents. Current OpenClaw is push-based; the child completion returns to the requester session as an internal event for parent review.

## Example Prompts

### Monitor

```text
Check the OpenClaw gateway and scheduled jobs.

Report only:
- gateway down
- cron jobs failing
- repeated auth failures
- disk usage above 85 percent
- memory pressure high enough to affect the agent

Use HEARTBEAT_OK if there is nothing actionable.
Do not restart services unless the task explicitly asks for recovery.
```

### Researcher

```text
Research [TOPIC].

Use this order:
1. Read the local docs or repo path if provided.
2. Check primary sources.
3. Use web search only for missing or current facts.

Return:
- key findings
- evidence links
- unknowns
- recommended next step

Do not pad the answer. If a claim is uncertain, say so.
```

### Writer

```text
Draft [DOCUMENT_TYPE] from the provided notes.

Rules:
- preserve the user's position
- do not invent facts
- use direct language
- avoid inflated significance claims
- avoid em dashes and emoji
- keep headings useful rather than decorative

Return a draft and a short list of any missing facts.
```

### Coordinator

```text
Coordinate this task: [TASK].

Decide whether it needs specialists.
If it does, spawn only the smallest useful set:
- monitor for status checks
- researcher for evidence gathering
- writer for final prose

Keep a short decision log.
Return one consolidated result.
```

## Cost And Safety Notes

- Monitoring jobs should use cheap or free models when possible.
- Writing and coordination can justify stronger models when the output is public or high-risk.
- Cron jobs should use explicit model IDs and explicit delivery channels.
- External actions such as email, posts, purchases, filesystem deletion, service restarts, and public messages should require confirmation unless you have written a narrow rule for that workflow.
- Keep ClawHub skills disabled by default. Inspect their source for ideas, then rebuild your own local skill with the boundaries you want.
