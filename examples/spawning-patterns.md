# Spawning Patterns

How to spawn sub-agents from different contexts in OpenClaw.

## Quick Reference

| Context | How to Spawn | Use Case |
|---------|--------------|----------|
| From a skill | `sessions_spawn()` in code | Orchestration, parallel work |
| From an agent | `sessions_spawn` tool in prompt | Self-delegation |
| From cron | Inline or spawn in payload | Scheduled isolated tasks |

---

## Pattern 1: Spawning from a Skill

Most common pattern. Your skill code decides when to spawn.

**Example:** Research orchestrator that spawns multiple researchers in parallel.

```javascript
// File: skills/research-orchestrator/index.js

async function researchTopics(topics) {
  // Spawn a researcher for each topic
  const promises = topics.map(topic => 
    sessions_spawn({
      agentId: "researcher",
      task: `Research: ${topic}. Find pricing, features, and reviews.`,
      label: `research-${topic.replace(/\s+/g, '-')}`,
      cleanup: "delete"
    })
  );
  
  // Wait for all to complete
  const results = await Promise.all(promises);
  
  // Combine results
  return results.map((result, i) => ({
    topic: topics[i],
    findings: result
  }));
}
```

**When to use:**
- Parallel processing (multiple independent tasks)
- Heavy work that should not block main session
- Tasks that might fail independently

**Key options:**
- `agentId` - Which agent config to use
- `task` - The prompt/instruction
- `label` - For tracking (optional)
- `cleanup: "delete"` - Auto-remove session when done
- `timeoutSeconds` - Max time to wait (default: 300)

---

## Pattern 2: Spawning from an Agent Prompt

Agent decides when to spawn based on its instructions.

**Example:** Coordinator agent that delegates to specialists.

```
You are a coordinator agent. When you receive a complex request:

1. Break it into subtasks
2. Spawn appropriate specialist agents for each subtask
3. Wait for results
4. Synthesize and report back

Available specialists:
- researcher: Web research, data gathering
- writer: Content creation, documentation
- coder: Code generation, debugging

To spawn an agent, use the sessions_spawn tool with:
- agentId: which specialist
- task: clear instructions
- label: for tracking

Example:
sessions_spawn({
  agentId: "researcher",
  task: "Find current pricing for AWS EC2 t3.large in us-east-1",
  label: "ec2-pricing-research"
})
```

**Agent config:**
```json
{
  "agents": {
    "list": [
      {
        "id": "coordinator",
        "model": {
          "primary": "anthropic/claude-sonnet-4-5"
        },
        "tools": ["sessions_spawn"]
      }
    ]
  }
}
```

**When to use:**
- Self-directed delegation
- Multi-step workflows
- Dynamic task breakdown

---

## Pattern 3: Spawning from Cron

Scheduled jobs that spawn isolated work.

**Example:** Daily digest that spawns research agents for multiple topics.

```json
{
  "name": "daily-research-digest",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Spawn researcher agents for today's topics: AI news, tech funding, and security alerts. Combine results into a digest and email it to me."
  },
  "sessionTarget": "isolated"
}
```

**Or more explicit spawning:**

```javascript
// In your agent's prompt or skill
cron.schedule('0 9 * * *', async () => {
  const topics = ['AI news', 'tech funding', 'security alerts'];
  
  for (const topic of topics) {
    sessions_spawn({
      agentId: "researcher",
      task: `Research ${topic} from the last 24 hours`,
      label: `daily-${topic}`,
      cleanup: "delete"
    });
  }
});
```

**When to use:**
- Scheduled heavy work
- Overnight batch processing
- Parallel morning digests

---

## Complete Example: Smart Email Assistant

**Goal:** When you receive an email, spawn an agent to research the topic and draft a response.

**Setup:**

1. **Add to AGENTS.md** (all agents see this, including sub-agents):
```
## Email Assistant Agent

When spawned as "email-assistant", your role is:
- Identify the topic/request from the email
- Spawn a researcher agent to gather context
- Wait for research results
- Draft a response incorporating the research
- Present the draft for approval

Research prompt template:
"Research [TOPIC]. Find: key facts, recent developments, relevant data."
```

2. **Add to config**:
```json
{
  "agents": {
    "list": [
      {
        "id": "email-assistant",
        "model": {
          "primary": "anthropic/claude-sonnet-4-5"
        },
        "tools": ["sessions_spawn", "email", "message"]
      },
      {
        "id": "researcher",
        "model": {
          "primary": "kimi-coding/k2p5"
        },
        "tools": ["web_search"]
      }
    ]
  }
}
```

**Note:** Sub-agents do NOT use individual prompt files. They inherit context from workspace bootstrap files (AGENTS.md, TOOLS.md) and the task message you send when spawning.

3. **Trigger from email** (in your skill or main agent):
```javascript
// When new email arrives
sessions_spawn({
  agentId: "email-assistant",
  task: `Handle this email:\n\nFrom: ${email.from}\nSubject: ${email.subject}\n\n${email.body}`,
  label: `email-${email.id}`,
  cleanup: "delete"
});
```

---

## Common Mistakes

**Wrong:** Spawning without waiting for results
```javascript
// Wrong - fire and forget, never know if it worked
sessions_spawn({ agentId: "researcher", task: "Research X" });
console.log("Done"); // Immediately logs, spawn still running
```

**Right:** Proper async handling
```javascript
// Right - wait for completion
const result = await sessions_spawn({ 
  agentId: "researcher", 
  task: "Research X",
  timeoutSeconds: 600 
});
console.log("Result:", result);
```

**Wrong:** Using wrong agentId
```javascript
// Wrong - agent doesn't exist
sessions_spawn({ agentId: "resercher", ... }); // typo
```

**Right:** Verify agent exists
```javascript
// Check your config: agents.list should include "researcher"
```

**Wrong:** Spawning for trivial tasks
```javascript
// Wrong - overhead costs more than task
sessions_spawn({ 
  agentId: "researcher", 
  task: "Check if it's raining" 
});
```

**Right:** Spawn for meaningful work
```javascript
// Right - significant task worth the overhead
sessions_spawn({ 
  agentId: "researcher", 
  task: "Compare 5 VPS providers, analyze pricing/features/reviews" 
});
```

**Workspace Note:** When you spawn an agent via `sessions_spawn`, it creates `workspace-{agentId}/` automatically with its own (empty) AGENTS.md. 

If you want spawned agents to share your main workspace and AGENTS.md, you must:
1. Define the agent in `agents.list` with explicit `workspace: "~/.openclaw/workspace"`, OR
2. Copy AGENTS.md to the spawned agent's workspace before spawning

For shared context across spawned agents, pre-define them in config with explicit workspace paths.

---

## Debugging Spawns

**Check if agent exists:**
```bash
openclaw config get | jq '.agents.list[].id'
```

**Test spawn manually:**
```javascript
// In main session
sessions_spawn({
  agentId: "researcher",
  task: "Test: research OpenClaw documentation",
  timeoutSeconds: 60
})
```

**Check spawn logs:**
```bash
tail -f ~/.openclaw/gateway.log | grep spawn
```

**Session tracking:**
```javascript
// Use labels to track
sessions_spawn({
  agentId: "researcher",
  task: "...",
  label: `research-${Date.now()}`, // unique label
  cleanup: "keep" // do not auto-delete, inspect later
});
```

Then check:
```bash
openclaw sessions list
```

---

## Cost Considerations

Spawning has overhead:
- Context loading (token cost)
- Session setup time
- Inter-session communication

**Spawn when:**
- Task takes more than 2-3 minutes
- Parallel processing needed
- Isolation from main session matters
- Different model capabilities needed

**Do not spawn when:**
- Task is trivial (less than 30 seconds)
- Inline processing is sufficient
- Context continuity is important

---

## Related

- [agent-prompts.md](agent-prompts.md) - Creating specialized agents
- [showcases/agent-orchestrator.md](../showcases/agent-orchestrator.md) - Routing tasks to optimal tools
- [showcases/idea-pipeline.md](../showcases/idea-pipeline.md) - Parallel research spawning
