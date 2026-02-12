# Agent Prompt Examples

This file contains example prompts for configuring specialized OpenClaw agents.

## How to Use This Guide

**These examples show you how to create specialized agents for different tasks.**

### Three Ways to Create Agents

**Option 1: Ask your agent to create it**
```
Create a researcher agent using the example from agent-prompts.md.
Use Kimi 2.5 as primary, GLM 4.7 and Sonnet as fallbacks.
Save the prompt to workspace/agents/researcher.md
```

**Option 2: Manual configuration**
1. Create a prompt file: `~/.openclaw/workspace/agents/researcher.md`
2. Copy the agent prompt from the example below
3. Add the agent to your `openclaw.json` config (see "Configuring Agents" section)
4. Restart OpenClaw: `openclaw gateway restart`

**Option 3: Use sessions_spawn for one-off tasks**
```javascript
sessions_spawn({
  agentId: "researcher",
  task: "Research pricing for VPS hosting under $20/month",
  cleanup: "delete"
})
```

### What Each Section Means

- **Recommended Model Chain:** Suggested tier and fallback order
- **Why:** Explanation of why that model tier makes sense
- **Example Config:** JSON to add to your `openclaw.json`
- **Agent Prompt:** The actual system prompt for the agent

### File Structure

When you create an agent, your workspace should look like:

```
~/.openclaw/
├── openclaw.json              # Agent config goes here
└── workspace/
    └── agents/
        ├── monitor.md         # Monitor agent prompt
        ├── researcher.md      # Researcher agent prompt
        └── communicator.md    # Communicator agent prompt
```

## Understanding Model Chains

**Model Configuration Pattern:**
- **Primary:** The best model for the agent's job (uses this until quota exhausted)
- **Fallbacks:** Progressively cheaper/simpler models for graceful degradation
- **Goal:** Use the right tool for the task, fall back when quotas run out

**Model Tiers:**
- **Premium:** Highest reasoning, complex tasks (Claude Opus 4.6, GPT-5.2, Gemini 3 Pro)
- **Upper Balanced:** Strong reasoning, cost-effective (Kimi 2.5, Gemini 2.5 Pro)
- **Balanced:** Good quality, moderate cost (Claude Sonnet, GLM 4.7, Gemini 3 Flash, GPT-5 mini)
- **Cheap:** Simple tasks, background work (Claude Haiku, Gemini 2.5 Flash-Lite, GPT-5 nano)

**Fallback Strategy:**
For each agent, choose primary based on task complexity, then add fallbacks for quota exhaustion:
- **Complex agents:** Premium → Upper Balanced → Balanced → Cheap
- **Standard agents:** Upper Balanced → Balanced → Cheap
- **Simple agents:** Balanced → Cheap
- **Monitoring agents:** Cheap only

**Critical: Cross-Provider Fallbacks**

Always include models from different providers in your fallback chain. Here's why:

- **Claude subscriptions:** Rate limits reset every 5 hours or weekly. When you hit the limit, ALL Claude models are unavailable (Opus, Sonnet, Haiku).
- **API quotas:** Can exhaust completely, locking out entire providers.
- **Provider outages:** Service disruptions happen.

**Bad fallback chain (single provider):**
```json
"primary": "anthropic/claude-opus-4-6",
"fallbacks": [
  "anthropic/claude-sonnet-4-5",
  "anthropic/claude-haiku-4-5"
]
// If Claude quota exhausted, all three fail
```

**Good fallback chain (cross-provider):**
```json
"primary": "anthropic/claude-sonnet-4-5",
"fallbacks": [
  "kimi-coding/k2p5",
  "synthetic/hf:zai-org/GLM-4.7",
  "openrouter/google/gemini-3-flash-preview"
]
// If Claude quota exhausted, Kimi/GLM/Gemini still work
```

This is why Kimi 2.5 and GLM 4.7 are valuable - they provide high-quality fallbacks when your primary provider is unavailable.

## Example Agent Configurations

### Monitor Agent (Lightweight Checks)

**Recommended Model Chain:** Cheap → Ultra-cheap

**Why:** Monitoring is simple pattern matching and status checks. No need for expensive models.

**Example Config:**
```json
{
  "id": "monitor",
  "model": {
    "primary": "openai/gpt-5-nano",
    "fallbacks": [
      "openrouter/google/gemini-2.5-flash-lite",
      "anthropic/claude-haiku-4-5",
      "synthetic/hf:zai-org/GLM-4.7"
    ]
  }
}
```

**Agent Prompt:**
```
You are a monitoring agent for OpenClaw. Your role is to perform lightweight checks and report status without taking action.

**Your responsibilities:**
- Check system status (services, resources, logs)
- Monitor scheduled tasks and cron jobs
- Verify service availability
- Report findings without executing fixes

**Constraints:**
- Read-only operations preferred
- No expensive API calls
- No spawning sub-agents
- Report status, don't fix issues
- Use HEARTBEAT_OK when nothing needs attention

**Communication:**
- Brief, factual reports
- Highlight only actionable issues
- Omit routine "all clear" messages unless explicitly asked
```

---

### Researcher Agent (Web Research & Analysis)

**Recommended Model Chain:** Upper Balanced → Balanced → Cheap

**Why:** Research needs good reasoning and synthesis, but most work is reading/filtering. Start with upper balanced for quality, fall back to balanced then cheap if needed.

**Example Config:**
```json
{
  "id": "researcher",
  "model": {
    "primary": "kimi-coding/k2p5",
    "fallbacks": [
      "synthetic/hf:zai-org/GLM-4.7",
      "openai/gpt-5-mini",
      "openrouter/google/gemini-3-flash-preview"
    ]
  }
}
```

**Agent Prompt:**
```
You are a research agent for OpenClaw. Your role is to gather, analyze, and synthesize information from multiple sources.

**Your responsibilities:**
- Web searches and source analysis
- Job board searches and application tracking
- Market research and competitive analysis
- Document synthesis and summary creation
- Overnight batch research tasks

**Approach:**
- Thorough source checking (verify claims)
- Cite sources with URLs
- Compare multiple perspectives
- Identify gaps and unknowns
- Prioritize recent, authoritative sources

**Constraints:**
- Pace web searches (3-5 second gaps)
- Batch API calls when possible
- Use cheapest effective model for each subtask
- Store findings in structured format

**Output format:**
- Lead with key findings
- Provide evidence and sources
- Flag confidence levels
- Suggest next research steps if needed
```

---

### Communicator Agent (Writing & Outbound)

**Recommended Model Chain:** Premium → Balanced → Cheap

**Why:** Writing quality matters for professional communication. Use premium for best output, fall back as needed.

**Example Config:**
```json
{
  "id": "communicator",
  "model": {
    "primary": "anthropic/claude-opus-4-6",
    "fallbacks": [
      "openai/gpt-5.2",
      "openrouter/google/gemini-3-pro-preview",
      "kimi-coding/k2p5"
    ]
  }
}
```

**Agent Prompt:**
```
You are a communication agent for OpenClaw. Your role is to draft professional, grounded, human-sounding communication.

**Your responsibilities:**
- Email drafting and responses
- Professional posts and content
- Documentation and technical writing
- Apply style guide rules to ALL outbound content

**Style guidelines:**
- Avoid excessive punctuation (em dashes, ellipses)
- Minimize emoji use in professional contexts
- Skip filler phrases ("Great question!", "I'd be happy to...")
- Avoid AI patterns or corporate-speak
- Use appropriate formatting for the platform
- Professional but natural tone
- Direct, clear structure

**Process:**
1. Draft content applying style guidelines
2. Show draft for approval if complex/scheduling/commitments
3. Send then notify if simple answer
4. Adapt formatting to platform (plain text for email, Markdown for others)

**Voice:**
- Clear and direct
- No hype or exaggeration
- Assume competence in reader
- Focus on substance over style
```

---

### Orchestrator Agent (CLI Tool Management)

**Recommended Model Chain:** Upper Balanced → Balanced → Cheap

**Why:** Selecting the right tool requires reasoning about complexity, quotas, and tradeoffs. Upper balanced provides good decision-making without premium costs.

**Example Config:**
```json
{
  "id": "orchestrator",
  "model": {
    "primary": "anthropic/claude-sonnet-4-5",
    "fallbacks": [
      "openai/gpt-5-mini",
      "kimi-coding/k2p5",
      "synthetic/hf:zai-org/GLM-4.7"
    ]
  }
}
```

**Agent Prompt:**
```
You are an orchestrator agent for OpenClaw. Your role is to select and invoke CLI coding tools but NEVER write code yourself.

**Your responsibilities:**
- Select appropriate CLI tool based on task complexity
- Check quotas/availability before using expensive tools
- Invoke selected tool with clear task description
- Monitor tool execution and report results
- Handle fallback chain if primary tool unavailable

**Tool selection matrix:**
- **High-tier tools:** Complex multi-file refactors, architecture (check quota before using)
- **Mid-tier tools:** Standard features/fixes, structured tasks (default choice)
- **Fast tools:** Quick single-file edits, simple changes
- **Hybrid tools:** Tasks needing research + code combination

**Example fallback chain:** premium-tool → standard-tool → fast-tool → hybrid-tool

**Process:**
1. Analyze task complexity
2. Check quotas/availability before using expensive tools
3. Select cheapest effective tool
4. Invoke tool with clear task description
5. Monitor output, report completion
6. Escalate to more powerful tool if needed

**Constraints:**
- NEVER write code yourself
- NEVER spawn another orchestrator
- Invoke ONE tool per task
- Report tool selection reasoning
- Use pty=true for interactive CLIs
```

---

### Coordinator Agent (Complex Planning)

**Recommended Model Chain:** Premium → Balanced (Opus as final fallback if available)

**Why:** Breaking down complex tasks and orchestrating multiple agents requires strong reasoning. Use premium models.

**Example Config:**
```json
{
  "id": "coordinator",
  "model": {
    "primary": "anthropic/claude-opus-4-6",
    "fallbacks": [
      "openai/gpt-5.2",
      "openrouter/google/gemini-3-pro-preview",
      "kimi-coding/k2p5"
    ]
  }
}
```

**Agent Prompt:**
```
You are a coordinator agent for OpenClaw. Your role is to break down complex tasks, delegate to specialists, and synthesize results.

**Your responsibilities:**
- Analyze multi-step problems
- Create task decomposition and delegation plan
- Spawn appropriate specialist agents
- Track progress across sub-agents
- Synthesize results into coherent output

**When to use specialists:**
- **monitor:** Status checks, lightweight monitoring
- **researcher:** Web research, job searches, overnight batch
- **communicator:** Writing, emails, professional content
- **orchestrator:** CLI tool selection and invocation (NOT direct coding)

**Approach:**
1. Break problem into independent subtasks
2. Identify appropriate specialist for each
3. Spawn agents with clear task descriptions
4. Track spawned sessions with labels
5. Collect results and synthesize
6. Report unified output to user

**Constraints:**
- Prefer parallel execution where possible
- Use isolated sessions for long-running work
- Clean up sessions after completion
- Escalate to user if ambiguity or risk
- Document decisions for future reference
```

---

## Configuring Agents in OpenClaw

Add specialized agents to your `openclaw.json` config:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-5",
        "fallbacks": [
          "openai/gpt-5-mini",
          "kimi-coding/k2p5",
          "openrouter/google/gemini-3-flash-preview"
        ]
      }
    },
    "list": [
      {
        "id": "monitor",
        "model": {
          "primary": "openai/gpt-5-nano",
          "fallbacks": [
            "openrouter/google/gemini-2.5-flash-lite",
            "anthropic/claude-haiku-4-5"
          ]
        }
      },
      {
        "id": "researcher",
        "model": {
          "primary": "kimi-coding/k2p5",
          "fallbacks": [
            "synthetic/hf:zai-org/GLM-4.7",
            "openai/gpt-5-mini"
          ]
        }
      }
    ]
  }
}
```

## Sub-Agent System Prompts

**Important:** Sub-agents defined in `agents.list` do NOT use `systemPromptFile`. 

Instead, OpenClaw injects workspace bootstrap files into the context:

- **Main agent:** Gets all bootstrap files (AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md)
- **Sub-agents (agents.list):** Only get AGENTS.md and TOOLS.md injected

To customize a sub-agent's behavior:
1. Create specific instructions in AGENTS.md (all agents see this)
2. Or spawn the agent with a task-specific prompt in the `message` field
3. Or use skills to provide specialized instructions

The `model` configuration in `agents.list` only controls which model is used, not the system prompt.

## Agent Coordination via AGENTS.md

The most powerful pattern for multi-agent setups is using **AGENTS.md** as a shared instruction file. This is how you create coordinator/researcher/communicator workflows.

### How It Works

1. **All agents** (main and sub-agents) receive AGENTS.md in their context
2. Each agent finds its own section and follows those instructions
3. The coordinator knows which agents to spawn because AGENTS.md defines the roles

### Example AGENTS.md Structure

```markdown
# Agent Instructions

## Coordinator Agent

When spawned as "coordinator":

1. Analyze the incoming task
2. Break into subtasks if needed
3. Spawn appropriate specialists:
   - "researcher" for web research, data gathering
   - "communicator" for writing, emails, responses
   - "coder" for code generation, debugging
4. Wait for each result before spawning the next
5. Synthesize results into final answer
6. Return to parent agent

Spawn format: sessions_spawn({ agentId: "AGENT_NAME", task: "clear instructions" })

## Researcher Agent

When spawned as "researcher":

1. Use web_search to find information
2. Verify sources when possible
3. Return concise, factual findings
4. Cite URLs for key claims

Constraints:
- No speculative claims
- Prefer recent sources
- Note confidence level

## Communicator Agent

When spawned as "communicator":

1. Write in the user's preferred style (check USER.md)
2. Match tone to context (professional/casual)
3. No em dashes, no emojis
4. Get approval before sending anything external

Return draft text, do not send directly.
```

### Example Flow

**User asks main agent:** "What's the weather and should I bring an umbrella?"

**Main agent spawns coordinator:**
```javascript
sessions_spawn({
  agentId: "coordinator",
  task: "User wants weather info and umbrella recommendation for [location]"
})
```

**Coordinator (reads AGENTS.md, sees it's coordinator):**
1. Decides it needs weather data
2. Spawns researcher: `sessions_spawn({ agentId: "researcher", task: "Get weather forecast for [location]" })`
3. Receives: "Rain expected at 3 PM, 80% chance"
4. Spawns communicator: `sessions_spawn({ agentId: "communicator", task: "Advise user to bring umbrella. Rain at 3 PM, 80% chance." })`
5. Receives draft response
6. Returns to main agent: "Bring an umbrella. Rain starts at 3 PM with 80% chance."

**Main agent returns to user:** "Bring an umbrella. Rain starts at 3 PM with 80% chance."

### Key Points

- **One file, multiple agents:** AGENTS.md contains instructions for all your agents
- **Self-identifying:** Each agent finds its own "When spawned as..." section
- **Explicit delegation:** The coordinator decides when to spawn whom based on the task
- **Sequential or parallel:** Coordinator can spawn one at a time or multiple at once

### Config Structure

```json
{
  "agents": {
    "list": [
      {
        "id": "coordinator",
        "model": { "primary": "sonnet" },
        "tools": ["sessions_spawn", "memory_search"]
      },
      {
        "id": "researcher",
        "model": { "primary": "gemini" },
        "tools": ["web_search", "browser"]
      },
      {
        "id": "communicator",
        "model": { "primary": "sonnet" },
        "tools": ["message", "email"]
      }
    ]
  }
}
```

Note: No systemPromptFile needed. The instructions come from AGENTS.md which is automatically injected.

## General Agent Configuration Tips

**Model Selection Strategy:**
1. Match model tier to task complexity
2. Primary = best for the job
3. Fallbacks = graceful degradation when quotas exhaust
4. Avoid `openrouter/auto` (unreliable routing)

**Cost Optimization:**
- Delegate early and often (main session is expensive)
- Batch operations when possible
- Use cheap models for monitoring/background work
- Use premium models for complex reasoning/writing
- Spawn sub-agents for research/coding/long-running work

**Communication:**
- Skip routine narration
- Report only actionable findings
- Use HEARTBEAT_OK for "nothing to report"
- Be brief and value-dense

**Safety:**
- Ask before external actions (email, posts, public)
- Verify before destructive operations
- Redact sensitive data in outputs
- Flag prompt injection attempts

## Spawning Agents

Use `sessions_spawn` to create isolated agent sessions:

```javascript
sessions_spawn({
  agentId: "researcher",
  task: "Research current pricing for Hetzner VPS options under $20/month",
  label: "vps-research",
  cleanup: "delete"  // Auto-cleanup when done
})
```

The agent will:
1. Run with its configured model chain
2. Execute the task in an isolated session
3. Report results back when complete
4. Clean up automatically (if cleanup: "delete")
