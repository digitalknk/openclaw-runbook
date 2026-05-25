# Running OpenClaw Without Burning Money, Quotas, or Your Sanity

## TL;DR

OpenClaw is useful when you treat it like infrastructure instead of a chatbot.

The setup that has held up for me is simple: keep access private, make model routing explicit, use the built-in task and memory systems, keep skills local, and do not expose the Gateway just because remote access sounds convenient.

My current setup is Tailscale-first. The Gateway stays loopback-bound, and I reach the Control UI through Tailscale, even when I am local. If you do not want Tailscale, keep OpenClaw local and use Telegram or another channel for remote access instead.

This guide was refreshed against the local OpenClaw docs at commit `5dccba7405` from `2026-05-25`. OpenClaw changes fast, so check the official docs and recent issues before assuming your config is broken.

- [OpenClaw Docs](https://docs.openclaw.ai/)
- [OpenClaw FAQ](https://docs.openclaw.ai/help/faq)
- [OpenClaw GitHub Issues](https://github.com/openclaw/openclaw/issues)
- [OpenClaw Pull Requests](https://github.com/openclaw/openclaw/pulls)

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

## Do not buy hardware first

Local models are useful for experimentation and some background work. They are not automatically cheaper once you count hardware, setup time, degraded quality, and debugging.

I would not buy a Mac mini, Mac Studio, or GPU box just for OpenClaw until you know:

- which tasks you actually run;
- what your hosted API cost looks like;
- which jobs can tolerate weaker models;
- what failure modes you need to isolate.

Use hosted models until you have real usage data. Then decide whether local inference solves an actual problem.

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

Costs change, model availability changes, and providers change pricing.

The useful takeaway is not my exact bill. The useful takeaway is that costs flatten out when you:

- keep background work on cheaper models;
- cap concurrency;
- avoid retry storms;
- use exact schedules only when needed;
- do not route every routine turn through premium models;
- monitor provider dashboards.

Treat every model and provider claim in this repo as a dated personal note unless it is backed by current OpenClaw docs or provider docs.

## Get stable before 24/7

Do not start by making everything always-on.

Get a local or Tailscale-only setup working first. Watch logs, costs, task records, and channel behavior for a few days. Then add cron, heartbeat, and broader tools one piece at a time.

Letting an agent run unattended before you understand its failure modes is how you wake up to a bill, a noisy chat history, and no clear explanation of what happened.

## Config reference

The sanitized config in this repo is based on a working setup:

- [`examples/sanitized-config.json`](examples/sanitized-config.json)
- [`examples/config-example-guide.md`](examples/config-example-guide.md)

It is a reference, not a template to copy without thought. The provider list, model list, channels, and skill entries should be changed for your environment.

## Links and referrals

Some older versions of this guide included provider notes and referral links. Keep those separate from technical guidance.

For current provider setup, use the official OpenClaw provider docs and the provider's own pricing/auth docs. If a provider note remains in this repo, read it as personal context, not a recommendation.
