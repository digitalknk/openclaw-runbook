# Sub-Agent Architecture

How to structure persona-based sub-agents that handle specialized tasks without losing control.

## The Problem

As your OpenClaw setup grows, you'll want agents handling different domains:
- Social media engagement
- Customer support
- Research and analysis
- Content creation

Cramming everything into one agent's instructions creates bloat and confusion. The agent tries to be everything and excels at nothing.

## The Solution: Persona-Based Sub-Agents

Each sub-agent gets:
- Its own identity (SOUL.md)
- Its own operating instructions (AGENTS.md)
- Its own memory folder
- Clear constraints on what it can/cannot do

## Directory Structure

```
workspace/
├── SOUL.md              # Main agent identity
├── AGENTS.md            # Main agent instructions
├── MEMORY.md            # Main agent long-term memory
└── agents/
    ├── kate/            # Social media sub-agent
    │   ├── SOUL.md
    │   ├── AGENTS.md
    │   ├── GUIDELINES.md
    │   └── memory/
    │       ├── activity-log.md
    │       └── strategy.md
    └── kain/            # Support sub-agent
        ├── SOUL.md
        ├── AGENTS.md
        └── memory/
```

## Sub-Agent SOUL.md Example

```markdown
# SOUL.md — Kate

## Identity
- **Name:** Kate
- **Role:** Social media engagement specialist
- **Personality:** Extroverted, observational, adapts tone to platform

## Voice
- Casual on Reddit, professional on LinkedIn
- Never promotional or salesy
- Asks questions that invite discussion
- Matches the energy of the conversation

## Constraints
- No product mentions until [DATE]
- No controversial topics
- No engagement with negative threads
- Maximum 3-4 comments per day

## Mission
Build authentic presence in technical communities. 
Quality over quantity. Blend in, don't stand out.
```

## Sub-Agent AGENTS.md Example

```markdown
# AGENTS.md — Kate's Operating Instructions

## Every Session
1. Read SOUL.md — internalize Kate's voice
2. Read memory/activity-log.md — know recent activity
3. Read memory/strategy.md — current approach
4. Check DECISIONS.md in parent workspace — respect main session decisions

## Workflow
1. Browse target subreddits (rotate, never repeat same sub twice in a row)
2. Find 2-3 posts worth engaging with
3. Write comments that add genuine value
4. Space comments 10-15 minutes apart
5. Log everything to memory/activity-log.md

## Quality Standards
- Add value: insight, experience, or genuine question
- Match platform tone
- Vary length and style
- Never use templates or patterns

## Red Flags
- ❌ Too frequent activity
- ❌ Same comment patterns
- ❌ Posting at exact same times daily
- ❌ Generic responses ("Great post!")
```

## Running Sub-Agents

Sub-agents run via cron jobs in isolated sessions:

```json
{
  "name": "kate-morning",
  "schedule": {
    "kind": "cron",
    "expr": "0 10 * * *",
    "tz": "Europe/Paris"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Morning run. Read agents/kate/SOUL.md and agents/kate/AGENTS.md. Follow the workflow. Log activity.",
    "timeoutSeconds": 300
  },
  "sessionTarget": "isolated"
}
```

Key points:
- `sessionTarget: "isolated"` — sub-agent runs in its own session, not main
- Cron message tells it which files to read
- Sub-agent has no access to main session context (by design)

## Coordination Pattern: DECISIONS.md

The "Dory Problem": cron-triggered sub-agents don't know what main session decided.

Solution: Main session writes decisions to `DECISIONS.md`, sub-agents read before acting.

```markdown
# DECISIONS.md

## 2026-02-11 10:00 — [SOCIAL] Promotion embargo
No product mentions until launch date.
**Action:** Skip any content that promotes the product.
Expires: 2026-02-15

## 2026-02-11 14:30 — [REDDIT] Avoid r/technology
Thread went hostile. Stay away for a week.
**Action:** Do not engage with r/technology.
Expires: 2026-02-18
```

Sub-agent AGENTS.md includes:
```markdown
## Before Acting
Read workspace/DECISIONS.md (last 24h entries).
If a decision affects your task, follow it or skip.
```

## Benefits

1. **Separation of concerns** — Each agent does one thing well
2. **Clear constraints** — Boundaries prevent overreach
3. **Independent memory** — Sub-agents track their own context
4. **Easy iteration** — Update one agent without affecting others
5. **Audit trail** — Each agent logs to its own memory folder

## Anti-Patterns

❌ **Sub-agent with full workspace access**
Give them only what they need. Kate doesn't need access to financial docs.

❌ **No constraints**
"Do social media" is too broad. Specify platforms, frequency, tone, limits.

❌ **Shared memory**
Sub-agents should have isolated memory. Cross-contamination creates confusion.

❌ **Direct agent-to-agent communication**
Route through main session or DECISIONS.md. Direct coordination is fragile.

## When to Use Sub-Agents

✅ Task requires a different persona/voice
✅ Task runs on a schedule (cron)
✅ Task has clear boundaries and constraints
✅ You want isolated memory and logging

❌ One-off tasks (just use main agent)
❌ Tasks requiring real-time coordination
❌ Tasks that need full workspace context
