# Running OpenClaw Without Burning Money, Quotas, or Your Sanity

## TL;DR

OpenClaw is useful, but most of the pain people run into comes from letting one model do everything, chasing hype, or running expensive models in places that do not need them.

The setup that has held up for me is simple: keep access private, make model routing explicit, use the built-in task and memory systems, keep skills local, and do not expose the Gateway just because remote access sounds convenient.

My current setup is Tailscale-first. The Gateway stays loopback-bound, and I reach the Control UI through Tailscale, even when I am local. If you do not want Tailscale, keep OpenClaw local and use Telegram or another channel for remote access instead.

This guide was refreshed against OpenClaw at commit `5dccba7405` from `2026-05-25`. OpenClaw changes fast, so check the official docs and recent issues before assuming your config is broken.

- [OpenClaw Docs](https://docs.openclaw.ai/)
- [OpenClaw FAQ](https://docs.openclaw.ai/help/faq)
- [OpenClaw GitHub Issues](https://github.com/openclaw/openclaw/issues)
- [OpenClaw Pull Requests](https://github.com/openclaw/openclaw/pulls)

I kept seeing the same questions come up around OpenClaw. People asking why it feels slow, why it keeps planning instead of doing, why it forgets things, or why free tiers disappear overnight. After answering the same threads over and over, it made more sense to write this once and link it.

This is not official guidance, and I am not affiliated with OpenClaw or any model provider. This is simply what I learned by running it, breaking it, and doing that loop more times than I would like to admit.

Reading open issues and recent PRs has saved me hours. More than once I thought I broke something, only to realize it was already known and actively being worked on.

## Start with current onboarding

If you are setting up OpenClaw from scratch, use the current onboarding flow:

```bash
openclaw onboard --install-daemon
openclaw gateway status
openclaw dashboard
```

Current docs recommend Node 24. Node 22.19+ is still supported.

Most people should start with the stable install or the macOS app and let OpenClaw manage the Gateway. Source checkouts are useful when you want to track dev changes, but they add moving parts. If you do run from source, keep your personal config and workspace outside the repo:

- config: `~/.openclaw/openclaw.json`
- workspace: `~/.openclaw/workspace`

That way updates do not overwrite your prompts, memory, or skill work.

## My access model: Tailscale first

I strongly recommend using Tailscale for Control UI and dashboard access.

My config keeps the Gateway local:

```json
"gateway": {
  "mode": "local",
  "port": 18789,
  "bind": "loopback",
  "auth": {
    "mode": "token",
    "token": "<REDACTED_GATEWAY_TOKEN>"
  },
  "tailscale": {
    "mode": "serve",
    "resetOnExit": true
  },
  "controlUi": {
    "allowInsecureAuth": true,
    "allowedOrigins": ["https://<YOUR_TAILSCALE_HOSTNAME>"]
  }
}
```

The important part is not `allowInsecureAuth`. The important part is the boundary: loopback Gateway, token auth, explicit origins, and Tailscale as the access path.

Do not copy `allowInsecureAuth: true` into a public-web setup. In this runbook it belongs to a controlled Tailnet-only setup. If you are not using Tailscale, leave the Gateway local and talk to the agent through Telegram, iMessage, Discord, or another configured channel.

I do not recommend public ports, casual LAN exposure, or a public reverse proxy as the first answer.

## The mistake most people make early on

The common mistake is treating one default agent as a single super-assistant that should do everything: chat, research, coding, memory, scheduling, monitoring, and tool use.

That setup burns tokens, hides failure modes, and makes cost hard to reason about.

The better pattern is coordinator plus workers:

- the default agent stays capable but not extravagant;
- stronger models are used intentionally;
- background work goes through cron, heartbeat, tasks, or subagents;
- model fallbacks are visible in config;
- task state is inspectable.

## Model routing should be explicit

The current config structure separates the model catalog from the selected default model:

```json
"agents": {
  "defaults": {
    "models": {
      "zai/glm-5.1": { "alias": "GLM" },
      "zai/glm-5-turbo": {},
      "openrouter/free": {}
    },
    "model": {
      "primary": "zai/glm-5.1",
      "fallbacks": ["zai/glm-5-turbo"]
    }
  }
}
```

`agents.defaults.models` is the catalog and allowlist. `agents.defaults.model.primary` is what runs first. `fallbacks` is the ordered failover list.

The model names above are not the recommendation. Use whatever providers you trust and pay for. The recommendation is the pattern:

- use explicit `provider/model` refs;
- keep the allowlist small enough to understand;
- avoid leaving premium models in a hot loop;
- use different providers when fallbacks matter;
- test after provider or model changes.

My current example uses Z.ai and OpenRouter because that is what I am testing. Yours should match your accounts, quota limits, and tolerance for latency.

## Auto-mode and blind routing

I tried auto-mode and blind routing early on. Stopped using both.

The idea of letting the system decide which model to use sounds great. When I actually ran it, it led to indecision, unexpected cost spikes, and behavior I could not reason about when something went wrong.

Being explicit works better. Default routing stays cheap and predictable. Agents get pinned to specific models for specific jobs. When something expensive runs, it should be because you asked for it.

Less magical. Far more debuggable.

## Why strong models should not be defaults

High-quality models are useful. I use them. They are good at restructuring prompts, designing agents, reasoning through messy problems, and fixing things that are already broken.

Where I got burned was leaving that level of model running all day.

It felt powerful until I hit rate limits and ended up locked out waiting for quotas to refresh. At that point you are not building anything. You are just waiting.

Strong models work best when they are scoped. Pin them to specific agents and call them when you actually need them. Do not leave them in the default coordinator loop burning through quota on routine work.

## Do not buy hardware first

Local models are useful for experimentation and some background work. They are not automatically cheaper once you count hardware, setup time, degraded quality, and debugging.

There has been a lot of hype around buying Mac minis or Mac Studios just to run OpenClaw. I would strongly recommend against doing this early.

Not everyone has $600 to drop on a tool, and even if you do, it is usually the wrong move to make first. The FOMO around OpenClaw is real. It is easy to feel like you need dedicated hardware immediately.

I would not buy a Mac mini, Mac Studio, or GPU box just for OpenClaw until you know:

- which tasks you actually run;
- what your hosted API cost looks like;
- which jobs can tolerate weaker models;
- what failure modes you need to isolate.

Use hosted models until you have real usage data. Then decide whether local inference solves an actual problem.

The math rarely works out unless you already have serious hardware. A Mac Studio with 512 GB of unified memory and 2 TB of storage runs over $9,000. To realistically host very large models with usable performance, you can quickly end up looking at multiple machines. Unless you are building a business that needs that hardware for more than just OpenClaw, skip it.

Local models are fine for experimentation and simple tasks. But I have found that bending over backwards to save a few cents usually costs more in lost time and degraded performance than just paying for API calls.

One related note: some free-tier hosted options are not much better. NVIDIA NIM's free tiers and other free hosted queues can be crowded enough that responses arrive in minutes instead of seconds. That kind of latency makes agent workflows painful. Free does not always mean usable.

## The hype problem

This part is worth saying.

There is a lot of hype around OpenClaw right now. Flashy demos, YouTube videos promising it will replace everything you do, and "this changes everything" energy on every social platform. I have watched people spend more time configuring OpenClaw than doing the work they wanted OpenClaw to help with.

I would encourage people to resist the FOMO and ignore most of the YouTube content. A lot of it is optimized for clicks, not for boring Tuesday-afternoon usage.

OpenClaw gets useful when you stop expecting magic and start expecting a tool that needs tuning.

## Memory is files, not magic

OpenClaw remembers things by writing Markdown files in the agent workspace.

The current memory layout is:

- `MEMORY.md` for durable facts, preferences, and decisions;
- `memory/YYYY-MM-DD.md` for daily notes and working context;
- optional `DREAMS.md` for dreaming/review output.

Daily memory files are not all injected into every turn. They are available through memory tools and recent startup context. `MEMORY.md` is the compact layer that should stay high signal.

That does not mean the older memory config knobs disappeared. They are still current:

- `agents.defaults.memorySearch` controls memory search providers, embedding models, QMD, hybrid search, and related indexing behavior.
- `agents.defaults.memorySearch.sources` and `agents.defaults.memorySearch.experimental.sessionMemory` are still used for opt-in session transcript indexing.
- `agents.defaults.contextPruning` still supports `mode: "cache-ttl"` for pruning old tool-result context around prompt-cache windows.
- `agents.defaults.compaction.memoryFlush` still controls the pre-compaction silent memory write, and is enabled by default.

The sanitized baseline now includes a memory search example because vector-backed memory is useful once it is configured correctly. The important part is that the embedding provider must work. Setting memory search to an embedding provider without a real key or reachable endpoint will make a copied config worse, not better. If your existing config has working memory search or pruning settings, keep them and compare the settings rather than replacing it blindly.

Example memory tuning using OpenRouter embeddings:

```json
"agents": {
  "defaults": {
    "memorySearch": {
      "enabled": true,
      "provider": "openai",
      "model": "thenlper/gte-base",
      "remote": {
        "baseUrl": "https://openrouter.ai/api/v1",
        "apiKey": {
          "source": "env",
          "provider": "default",
          "id": "OPENROUTER_API_KEY"
        }
      },
      "sources": ["memory", "sessions"],
      "experimental": {
        "sessionMemory": true
      },
      "query": {
        "hybrid": {
          "enabled": true,
          "vectorWeight": 0.7,
          "textWeight": 0.3,
          "candidateMultiplier": 4,
          "mmr": {
            "enabled": true,
            "lambda": 0.7
          },
          "temporalDecay": {
            "enabled": true,
            "halfLifeDays": 30
          }
        }
      }
    },
    "contextPruning": {
      "mode": "cache-ttl",
      "ttl": "6h"
    },
    "compaction": {
      "memoryFlush": {
        "enabled": true,
        "softThresholdTokens": 40000,
        "prompt": "Write durable decisions, state changes, blockers, and user preferences to memory/YYYY-MM-DD.md. Reply NO_REPLY if nothing needs saving.",
        "systemPrompt": "Pre-compaction memory flush. Save only durable context. Do not summarize routine chatter."
      }
    }
  }
}
```

This uses OpenClaw's OpenAI-compatible embedding adapter with `remote.baseUrl` pointed at OpenRouter. That does not mean the model is an OpenAI model. In `memorySearch`, `provider` selects the embedding adapter. The actual embedding model here is an OpenRouter model. Do not change `provider` to `openrouter` unless current OpenClaw docs show that the OpenRouter plugin registers a memory embedding provider.

Replace the model if you need multilingual embeddings or a different provider. Vector search requires a working embedding model; without one, keep memory search lexical or use a provider you already have configured.

The example config enables hooks I want for continuity:

```json
"hooks": {
  "internal": {
    "enabled": true,
    "entries": {
      "compaction-notifier": { "enabled": true },
      "bootstrap-extra-files": { "enabled": true },
      "boot-md": { "enabled": true },
      "session-memory": { "enabled": true },
      "command-logger": { "enabled": true }
    }
  }
}
```

OpenClaw also runs a memory flush before compaction by default. That silent turn gives the agent a chance to save durable notes before older session context is summarized.

## Heartbeat is for awareness, not exact scheduling

Instead of running separate cron jobs for every periodic check, I like a heartbeat that rotates through checks based on how overdue each one is.

The idea is simple. Each check has a cadence, an optional time window, and a record of the last time it ran. On each heartbeat tick, the system runs whichever check is most overdue.

This batches background work, keeps costs flatter, and avoids the "everything fires at once" problem. Heartbeat checks should run on a cheap model. If a check finds something that needs real work, it should spawn the appropriate agent or create a task instead of trying to do everything inline.

Heartbeat runs periodic agent turns. It is useful for inbox checks, calendar awareness, and lightweight monitoring.

Current heartbeat behavior matters:

- default cadence is usually `30m`;
- `0m` disables it;
- heartbeat turns do not create task records;
- `HEARTBEAT_OK` suppresses no-op replies;
- `target: "none"` runs without external delivery;
- `target: "last"` sends to the last contact;
- `lightContext: true` limits bootstrap context;
- `isolatedSession: true` avoids sending the whole conversation history;
- `skipWhenBusy: true` can defer heartbeats when that same agent has active nested work.

For several checks on different cadences, use a `tasks:` block inside `HEARTBEAT.md` instead of making every check run every tick.

For exact timing, use cron.

## Cron and tasks are native now

Older versions made it tempting to wire your own task visibility through Todoist or a similar tool. You can still do that if you like the interface, but OpenClaw now has native task records.

I used to bridge task state into Todoist because OpenClaw felt like a black box. That was useful at the time. I no longer recommend that as the default starting point. Start with OpenClaw's task ledger first, then mirror tasks into Todoist, Linear, GitHub Issues, or Notion only if you need a separate human-facing board.

Use the current split:

- cron for exact schedules and one-shot reminders;
- heartbeat for approximate periodic awareness;
- background tasks for detached work records;
- Task Flow for multi-step flows;
- inferred commitments for short-lived follow-ups;
- standing orders for durable operating authority.

All cron executions create background task records. Subagents and ACP runs do too. Normal chat and heartbeat runs do not.

Useful commands:

```bash
openclaw cron list
openclaw cron run <job-id> --wait
openclaw tasks list
openclaw tasks show <lookup>
openclaw tasks audit
```

This is better than guessing what the agent is doing from chat replies.

## Subagents are push-based

`sessions_spawn` starts a detached run. It returns quickly. The child result is handed back to the requester session when it finishes.

Do not build polling loops around `/subagents list`, `sessions_list`, shell `sleep`, or repeated status checks just to wait. If the parent needs child results before continuing, use `sessions_yield` when that tool is available.

Important current behavior:

- native subagents are isolated by default;
- use `context: "fork"` only when the child truly needs current conversation context;
- subagent completions create task records;
- child output is evidence for the parent to review, not new user instruction;
- subagents do not get the full parent bootstrap context;
- configure `agents.defaults.subagents.maxConcurrent` as a safety valve.

The goal is to keep the main agent responsive while slow or risky work runs in a trackable lane.

## Build your own skills first

I am cautious with third-party skills.

My recommendation is not "install a bunch of ClawHub skills." My recommendation is:

1. Use ClawHub or a skill repo to find an idea.
2. Read the source.
3. Ask your agent to rebuild a local skill for your setup.
4. Keep only the behavior and tool access you actually need.
5. Test it before leaving it in the normal tool path.

This is slower than installing a skill directly. It is also safer.

Third-party skills can carry broad permissions, hidden assumptions, unnecessary dependencies, noisy prompts, and token-heavy abstractions. Even when nobody is being malicious, debugging someone else's skill at 2am is not a good time.

The example config keeps `clawhub` disabled on purpose. See [`examples/skill-builder-prompt.md`](examples/skill-builder-prompt.md) for the rebuild flow.

### Asking the bot to build or optimize a skill

One thing that helped me was getting more disciplined about how I ask the bot to create or refactor skills. Vague instructions produce bloated, token-hungry skills every time.

The structure I use follows the AgentSkills specification from [https://agentskills.io](https://agentskills.io/). I am not affiliated with it, but following that model made skills easier to maintain and cheaper to run.

The key is giving the bot hard constraints on line count, tool access, file layout, and expected behavior so it does not produce a giant skill file that eats half your context window.

## Prompt injection is normal input, not a surprise

If your setup reads web pages, GitHub issues, documents, email, or chat messages from other people, assume prompt injection will show up eventually.

The defense is not one magic sentence. Use layers:

- restrict who can talk to the bot;
- restrict which tools each channel and agent can use;
- use sandboxing where it fits;
- keep filesystem access narrow;
- use stronger models for tool-enabled work;
- treat untrusted content as data, not instruction;
- audit config after changes.

Run:

```bash
openclaw security audit
openclaw security audit --deep
openclaw doctor --fix
```

OpenClaw's security docs are written around a personal-assistant trust model. Do not treat one shared Gateway as a hostile multi-tenant boundary.

## VPS setup

If you run OpenClaw on a VPS, my recommendation is still Tailscale-first.

The setup I want:

- small VPS is fine;
- install Tailscale on the VPS and local machines;
- verify SSH over Tailscale;
- block public SSH after verifying the Tailnet path;
- keep the Gateway loopback-bound;
- use Tailscale Serve for dashboard/control access;
- use Telegram or another channel for remote chat.

If you do not want Tailscale, do not compensate by opening random ports. Keep the Gateway local and use a messaging channel as the remote interface.

See [`examples/vps-setup.md`](examples/vps-setup.md) for the longer checklist.

## What this costs me

I do not pay for everything through APIs.

I use coding subscriptions and API usage together. Most months, the API portion is still modest because background work runs on cheaper models and the expensive models are not in the default loop.

At the time this guide was refreshed, my normal spend was still roughly in the same range as before: coding subscriptions plus about $5-$10 per month in API usage split across providers such as OpenRouter and OpenAI. Most months I land around $45-$50 total, depending on which subscriptions I keep active and how much agent work I run.

That number is not a promise. It is a sanity check. If you let agents run nonstop, allow unlimited retries, or route everything through premium models, costs will climb. I have seen people burn through a lot of money quickly by leaving things uncapped.

Costs flatten out when you:

- keep background work on cheaper models;
- cap concurrency;
- avoid retry storms;
- use exact schedules only when needed;
- do not route every routine turn through premium models;
- monitor provider dashboards.

Treat every model and provider claim in this repo as a dated personal note unless it is backed by current OpenClaw docs or provider docs.

## Anthropic subscriptions and credits

I previously warned people away from Anthropic subscriptions for OpenClaw because policy and ban risk were unclear. That has changed.

Anthropic's current published guidance says eligible Claude plans can use Agent SDK and `claude -p` workflows through a separate monthly Agent SDK credit starting June 15, 2026. That does not mean your full normal chat quota is available to OpenClaw. The credit amount depends on the plan. Once that credit is used, extra usage can draw from purchased usage credits if you enable that path.

My practical recommendation is still cautious:

- if you use a Claude subscription with OpenClaw, watch the plan credit and usage-credit settings;
- for long-running unattended Gateway hosts, an API key or a provider like OpenRouter is often easier to reason about;
- do not assume subscription access means unlimited agent usage;
- check Anthropic's current docs before building a workflow around a specific quota number.

## Get stable before 24/7

Do not start by making everything always-on.

Get a local or Tailscale-only setup working first. Watch logs, costs, task records, and channel behavior for a few days. Then add cron, heartbeat, and broader tools one piece at a time.

Letting an agent run unattended before you understand its failure modes is how you wake up to a bill, a noisy chat history, and no clear explanation of what happened.

## Config reference

A few people asked to see a sanitized version of my OpenClaw config. I am sharing it as a reference, not something to copy verbatim.

It reflects my usage patterns, my constraints, and my tolerance for cost and latency. Yours will almost certainly be different.

The intent is to show how pieces fit together, not to suggest this is the right configuration.

- [`examples/sanitized-config.json`](examples/sanitized-config.json)
- [`examples/config-example-guide.md`](examples/config-example-guide.md)

It is a reference, not a template to copy without thought. The provider list, model list, channels, and skill entries should be changed for your environment.

## Links and referrals

A few people asked where I am getting access to some of the models and services mentioned above.

For transparency: I am not affiliated with OpenClaw, and nothing in this article depends on using these links.

Some providers I use offer referral programs. Included here for people who ask. Use them or do not.

### Z.ai (GLM models)

Z.ai provides access to GLM models, which I use as capable, lower-cost options for agents that do not need premium models. My exact model choices change as providers update their catalogs, so check Z.ai's current model list before copying an old ID.

- Direct link: [https://z.ai/subscribe](https://z.ai/subscribe)
- Referral link (supports this guide): [https://z.ai/subscribe?ic=6PVT1IFEZT](https://z.ai/subscribe?ic=6PVT1IFEZT)

### Synthetic

Synthetic hosts several open-source and partner models under one subscription, including GLM and Kimi families, plus additional models via providers such as Fireworks and Together. Check the current catalog before treating any specific model note as current.

- Direct link: [https://synthetic.new](https://synthetic.new)
- Referral link (supports this guide): [https://synthetic.new/?referral=p7ZFKQRrWliKZGa](https://synthetic.new/?referral=p7ZFKQRrWliKZGa)

Use whichever links you prefer. Referrals help support this guide but are not required.

## Final thoughts

You do not need expensive hardware or expensive subscriptions to make OpenClaw useful. What you need is to be deliberate about configuration, keep visibility into what is happening, and resist the urge to over-engineer before you understand the basics.

If this saves you some time or frustration, it did its job.
