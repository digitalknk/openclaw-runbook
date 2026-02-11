# Agent Orchestrator

**Category:** Development  
**Example Model:** Premium tier (Sonnet, Opus, etc.) for routing  
**Updated:** 2026-02-09

> **HOW TO USE:** This is a pattern, not a single cron job. Copy the routing logic into your agents to intelligently select the right coding tool for each task.

## Quick Start

### 1. Prerequisites

- [ ] Multiple CLI coding tools installed (claude, codex, opencode, gemini)
- [ ] API keys for each provider in `~/.openclaw/credentials/`
- [ ] Understanding of each tool's strengths
- [ ] Optional: Quota tracking method

### 2. Install CLI Tools

```bash
# Claude (Anthropic)
npm install -g @anthropics/claude-code

# Codex (OpenAI)
npm install -g openai-codex

# Opencode (local)
npm i -g opencode-ai

# Gemini (Google)
npm install -g @google/gemini-cli
```

Add API keys to `~/.openclaw/credentials/`:
```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
```

### 3. Copy This Orchestrator Agent

Add to your gateway config:

```yaml
agents:
  orchestrator:
    model: anthropic/claude-sonnet-4-5
    tools:
      - sessions_spawn
      - exec
    system: |
      You are a coding task router. Analyze each task and select the optimal CLI tool.

      AVAILABLE TOOLS:
      1. claude - Complex multi-file refactors, architecture
      2. codex - Standard features/fixes, structured tasks  
      3. opencode - Quick single-file edits
      4. gemini - Research + code hybrid tasks

      SELECTION RULES:

      Use claude if:
      - Changes span 3+ files
      - Requires architectural decisions
      - Complex refactoring
      - Needs deep context

      Use codex if:
      - Single feature or fix
      - Well-defined scope
      - 1-2 files affected
      - Standard patterns

      Use opencode if:
      - Quick edit to single file
      - Simple fix (typo, logic tweak)
      - Fast turnaround needed

      Use gemini if:
      - Needs research (API docs, examples)
      - Learning new technology
      - Research + implementation

      QUOTA CHECK:
      Before assigning to claude:
      1. Check quota via your tracking method
      2. If quota >90% or unavailable, fallback to codex

      FALLBACK CHAIN:
      claude → codex → opencode → gemini

      PROCESS:
      1. Analyze task description
      2. Check quota if needed
      3. Select optimal tool
      4. Spawn agent with selected tool
      5. Report: tool selected, why, expected scope
```

### 4. Usage Examples

**Route a coding task:**
```json
{
  "agentId": "orchestrator",
  "message": "Task: Refactor auth system to use JWT. Spans 5 files, needs architectural decisions."
}
```

Response:
```
Selected: claude
Reason: Multi-file refactor (5 files), architectural decisions needed
Scope: Complex, estimated 10-15 minutes
Quota: 45% used, proceeding with claude
```

**Simple task:**
```json
{
  "agentId": "orchestrator", 
  "message": "Task: Fix typo in README.md"
}
```

Response:
```
Selected: opencode
Reason: Single file, simple edit
Scope: Trivial, <1 minute
```

**Quota fallback:**
```json
{
  "agentId": "orchestrator",
  "message": "Task: Add new API endpoint"
}
```

Response:
```
Selected: codex (fallback)
Reason: Claude quota at 95%
Original choice: claude (single feature, well-defined)
```

---

## What This Does

**Problem:** Coding tasks vary in complexity. Using Claude for a typo wastes money. Using Opencode for architecture wastes time. Manual selection requires knowing each tool's strengths and current quotas.

**Solution:** Orchestrator agent analyzes each task, checks quotas, routes to optimal tool. Simple tasks get fast/cheap tools. Complex tasks get capable tools. Quota exhaustion triggers automatic fallback.

## Quota Tracking Options

### Option A: Simple Script

Create `~/.local/bin/check-quotas`:
```bash
#!/bin/bash
# Check quota for each provider
# Replace with your actual providers and quotas

echo "claude: [used]/[limit] ([percent]%)"
echo "codex: [used]/[limit] ([percent]%)"
echo "opencode: unlimited"
```

In agent prompt:
```
Run check-quotas script. If primary tool shows >90% usage, use fallback tool.
```

### Option B: API Status Check

```python
# Some providers expose quota via API
import requests

def check_quota(provider):
    if provider == "anthropic":
        r = requests.get(
            "https://api.anthropic.com/v1/usage",
            headers={"Authorization": f"Bearer {KEY}"}
        )
        return r.json()["usage"]
```

### Option C: Local Counter

Track requests in SQLite:
```sql
CREATE TABLE quota (
    provider TEXT,
    date TEXT,
    count INTEGER
);
```

## Tool Selection Matrix

| Task Type | Best Tool | Why |
|-----------|-----------|-----|
| Multi-file refactor | claude | Deep context, architectural decisions |
| Standard feature | codex | Good balance of capability and speed |
| Quick fix | opencode | Fast, lightweight, local |
| Research + code | gemini | Fast, good at explaining |

**Note:** Pricing and quotas vary by provider and change over time. Check your provider's current pricing.

## Cost Comparison

| Scenario | Without Orchestrator | With Orchestrator | Benefit |
|----------|---------------------|-------------------|---------|
| Fix typo with expensive model | Higher cost | Lower cost (uses cheaper tool) | Cost savings |
| Wrong tool for task | Poor result | Right tool selected | Quality ↑ |
| Quota exceeded | Stuck/fails | Auto-fallback | Reliability ↑ |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Wrong tool selected | Prompt unclear | Make task description more specific |
| Quota check fails | API unavailable | Add timeout, assume quota OK |
| Tool not installed | Missing CLI | Install or remove from options |
| Spawning fails | Agent config error | Check agentId and model names |

## Advanced: Custom Routing

Add your own rules:
```yaml
system: |
  ALSO CONSIDER:
  - If task mentions "test" or "testing", prefer codex (good at tests)
  - If task mentions "documentation", prefer gemini (good at explaining)
  - If task mentions "performance", prefer claude (deep analysis)
```

## Variations

**Cost-First Mode:**
Always pick cheapest viable tool, even if slower:
```
Priority: opencode → codex → gemini → claude
Only use claude if explicitly requested
```

**Speed-First Mode:**
Always pick fastest, cost secondary:
```
Parallel spawn: claude + codex
Use first to complete
Cancel others
```

**Learning Mode:**
Track which tools succeed for which task types:
```
Log: task_type, tool_selected, success_rating
Over time, optimize selections
```

## Security

- **No code execution in orchestrator** - Only routes, doesn't run code
- **Tool isolation** - Each spawned agent is separate session
- **Audit trail** - Log all routing decisions for review

## Related

- [idea-pipeline](idea-pipeline.md) - Uses similar spawning pattern
- [daily-brief](daily-brief.md) - Could route to different models based on complexity

## Changelog

- **2026-02-09** - Initial version with 4-tool routing
- **2026-02-10** - Added quota checking and fallback chains
