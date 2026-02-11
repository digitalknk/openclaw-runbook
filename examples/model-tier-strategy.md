# Model Tier Strategy

How to optimize costs by assigning the right model to each task phase.

## The Problem

Running everything on your best model (Opus, GPT-4) burns money fast:
- Background tasks don't need genius-level reasoning
- Brainstorming benefits from quantity, not perfection
- Only critical decisions require your most capable model

## The Solution: Ideation → Review → Execution

Match model capability to task requirements:

| Phase | Model Tier | Purpose | Cost |
|-------|-----------|---------|------|
| **Ideation** | Haiku / GPT-4o-mini | Generate options, brainstorm, explore | $ |
| **Review** | Opus / GPT-4 | Evaluate, critique, find flaws | $$$ |
| **Execution** | Task-dependent | Implement the chosen approach | Varies |

## Why This Works

**Ideation (cheap model):**
- You want quantity and variety
- "Bad" ideas are fine — you're exploring
- Fast iteration matters more than perfection
- Example: Generate 5 approaches to a problem

**Review (expensive model):**
- Critical thinking and judgment
- Finding edge cases and risks
- "Is this actually good?" requires reasoning
- Example: Evaluate the 5 approaches, pick best 2

**Execution (right-sized model):**
- Depends on what you're building
- Coding → local model (Ollama) or Sonnet
- Writing → Sonnet
- Simple tasks → Haiku
- Example: Implement the chosen approach

## Example Workflow

### Product Feature Decision

```
1. IDEATION (Haiku)
   "Generate 5 different approaches to implement user notifications.
   Include tradeoffs for each. Don't self-censor — include wild ideas."
   
   → Output: 5 approaches with pros/cons

2. REVIEW (Opus)
   "Review these 5 notification approaches. For each:
   - What could go wrong?
   - What's the maintenance burden?
   - How does it scale?
   Pick the best 2 and explain why."
   
   → Output: Top 2 approaches with reasoning

3. EXECUTION (Sonnet or Ollama)
   "Implement approach #1: WebSocket-based real-time notifications.
   Write the server code and client handler."
   
   → Output: Working code
```

### Content Creation

```
1. IDEATION (Haiku)
   "Generate 10 LinkedIn post ideas about AI agents.
   Mix formats: stories, tips, questions, hot takes."
   
2. REVIEW (Opus)
   "Review these 10 post ideas. Score each 1-10 on:
   - Engagement potential
   - Authenticity
   - Value to reader
   Pick top 3."
   
3. EXECUTION (Sonnet)
   "Write the full LinkedIn post for idea #1.
   Keep it under 1300 characters. Hook in first line."
```

## OpenClaw Configuration

### Default Model for Background Tasks

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-3.5-haiku"
      }
    }
  }
}
```

All cron jobs, heartbeats, and routine tasks use Haiku by default.

### Per-Task Model Override

In cron job definitions:

```json
{
  "name": "weekly-review",
  "payload": {
    "kind": "agentTurn",
    "message": "Review this week's decisions...",
    "model": "anthropic/claude-sonnet-4"
  }
}
```

### Dynamic Escalation in Prompts

```markdown
## Model Selection (AGENTS.md)

For each task, choose the appropriate model:
- Brainstorming, drafts, exploration → Stay on Haiku
- Critical decisions, code review, risk assessment → Escalate to Opus
- Implementation, writing, routine work → Use Sonnet

When in doubt: start cheap, escalate if quality insufficient.
```

## Cost Comparison

Rough token costs (as of early 2026):

| Model | Input (1M tokens) | Output (1M tokens) |
|-------|-------------------|-------------------|
| Haiku | $0.25 | $1.25 |
| Sonnet | $3.00 | $15.00 |
| Opus | $15.00 | $75.00 |

**Example savings:**

Traditional (all Opus): 100K tokens/day = ~$9/day = **$270/month**

Tiered approach:
- 80K tokens on Haiku = $0.10/day
- 15K tokens on Sonnet = $0.27/day  
- 5K tokens on Opus = $0.45/day
- Total: $0.82/day = **$25/month**

That's ~90% cost reduction with no quality loss on decisions that matter.

## Local Models for Execution

For coding tasks, consider local models:

```yaml
# Ollama running locally
Model: qwen2.5-coder:7b
Cost: $0 (runs on your hardware)
Context: 32K tokens
Good for: Implementation, unit tests, refactoring
```

Route coding to local:
```markdown
## Coding Tasks (AGENTS.md)

For implementation work:
1. Use local Ollama (qwen2.5-coder) for initial code
2. Review output yourself or escalate to Sonnet for review
3. Only use Opus for architectural decisions
```

## When to Break the Rules

**Always use expensive model:**
- User-facing content that represents you/your brand
- Decisions with significant consequences
- Anything involving money, legal, or safety

**Always use cheap model:**
- Heartbeats and monitoring
- Data formatting and extraction
- Simple CRUD operations
- Drafts that will be heavily edited anyway

## Summary

| Task Type | Recommended Model |
|-----------|------------------|
| Heartbeat/monitoring | Haiku |
| Brainstorming | Haiku |
| First drafts | Haiku |
| Code implementation | Local (Ollama) or Sonnet |
| Code review | Sonnet or Opus |
| Critical decisions | Opus |
| Final content review | Opus |
| Risk assessment | Opus |

The goal: 80% of tokens on cheap models, expensive models only for judgment calls.
