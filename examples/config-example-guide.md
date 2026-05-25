# OpenClaw Config Example Guide

This file explains [`sanitized-config.json`](sanitized-config.json). It is based on a working `2026.5.x` config, with secrets and personal identifiers replaced.

Do not copy it blindly. Use it as a reference for your own setup.

## Quick Start

1. Copy `examples/sanitized-config.json` somewhere temporary.
2. Replace every `<PLACEHOLDER>` value.
3. Run:

```bash
openclaw doctor --fix
openclaw security audit --deep
openclaw gateway status
```

If validation fails, fix the config before starting the Gateway. OpenClaw now validates config strictly.

## Access Model

The example is Tailscale-first:

```json
"gateway": {
  "mode": "local",
  "bind": "loopback",
  "tailscale": {
    "mode": "serve",
    "resetOnExit": true
  }
}
```

The Gateway stays bound to loopback. Tailscale Serve becomes the normal way to reach the Control UI. In my own setup, I use that path even when I am local.

If you do not want Tailscale, keep the Gateway local and use a channel like Telegram for remote access. That is safer than exposing the dashboard on a public port.

### `allowInsecureAuth`

The example includes:

```json
"controlUi": {
  "allowInsecureAuth": true,
  "allowedOrigins": ["https://<YOUR_TAILSCALE_HOSTNAME>"]
}
```

This is only appropriate for a controlled Tailscale-only setup with explicit origins. Do not treat it as a public-web setting.

## Model Catalog and Default Model

OpenClaw uses `agents.defaults.models` as the model catalog and allowlist. The active default is separate:

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

The exact model list is not the recommendation. The pattern is:

- put only models you are willing to use in `agents.defaults.models`;
- use explicit `provider/model` references;
- keep fallback behavior visible;
- swap providers based on your own accounts, cost, latency, and quota behavior.

## Provider Definitions

The example defines a custom `zai` provider under `models.providers`.

That block is replaceable. If you use OpenAI, Anthropic, Google, Ollama, OpenRouter, or another provider, use that provider's current OpenClaw docs and update the model refs accordingly.

## Auth Profiles and Secrets

The example has:

```json
"auth": {
  "profiles": {
    "zai:default": {
      "provider": "zai",
      "mode": "api_key"
    },
    "openrouter:default": {
      "provider": "openrouter",
      "mode": "api_key"
    }
  }
}
```

That means OpenClaw is using provider auth profiles. The API keys themselves are not in this published config. Keep it that way.

## Skills

The example disables bundled skills, including `clawhub`.

That is intentional. My preferred pattern is to inspect ClawHub or the skill source for ideas, then ask an agent to rebuild a local skill that matches your setup. Third-party skills can include unwanted behavior, broad tool assumptions, or abstractions that burn context.

Use [`skill-builder-prompt.md`](skill-builder-prompt.md) for the rebuild flow.

## Tools

The example uses:

```json
"tools": {
  "profile": "coding",
  "web": {
    "search": {
      "provider": "duckduckgo",
      "enabled": true
    },
    "fetch": {
      "enabled": true
    }
  }
}
```

That gives the agent coding-oriented tools plus web search/fetch. If your agent reads untrusted pages, issues, documents, or email, pair this with strong tool policy, sandboxing, and prompt-injection rules.

## Channels

The example enables Telegram and BlueBubbles:

- Telegram uses `dmPolicy: "allowlist"` and group mention requirements.
- BlueBubbles is configured for iMessage-style access through its own server URL and password.

If you are not using Tailscale for Control UI access, a Telegram bot is the recommended remote interaction path. Keep the Gateway local; talk to the agent through Telegram.

## Hooks

The example enables:

- `compaction-notifier`
- `bootstrap-extra-files`
- `boot-md`
- `session-memory`
- `command-logger`

These are current built-in OpenClaw hooks for better session continuity, startup context, compaction visibility, and command logging. Leave them on only if they match how you want sessions and memory to behave.

## Memory Search, Pruning, and Compaction

The sanitized config includes a power-user memory baseline. It is current, but it assumes you configure an embedding provider.

These settings are still current in the 2026-05-25 docs:

- `agents.defaults.memorySearch` for embedding provider, model, QMD, hybrid search, and memory indexing.
- `agents.defaults.memorySearch.sources` and `agents.defaults.memorySearch.experimental.sessionMemory` for opt-in session transcript indexing.
- `agents.defaults.contextPruning` for cache-aware context pruning.
- `agents.defaults.compaction.memoryFlush` for the silent pre-compaction memory write.

If your real config has these and they work, keep them. Do not replace them with hooks alone.

### OpenRouter Embeddings Example

The example uses OpenRouter through OpenClaw's OpenAI-compatible embedding adapter:

```json
{
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
          "systemPrompt": "Pre-compaction memory flush. Save only durable context."
        }
      }
    }
  }
}
```

Why `provider: "openai"` when this is OpenRouter? In `memorySearch`, `provider` selects the OpenClaw embedding adapter, not the company that hosts the selected model. OpenRouter's embedding endpoint is OpenAI-compatible, so this example uses OpenClaw's OpenAI-compatible embedding adapter with `remote.baseUrl` pointed at OpenRouter. The embedding model is still served by OpenRouter.

Do not change this field to `openrouter` unless current OpenClaw docs show that the OpenRouter plugin registers a memory embedding provider. In the 2026-05-25 docs, the OpenRouter plugin handles model routing and media providers, while the memory docs show OpenAI-compatible embedding endpoints through the `openai` adapter plus `remote.baseUrl`.

The API key is a SecretRef:

```json
{
  "source": "env",
  "provider": "default",
  "id": "OPENROUTER_API_KEY"
}
```

Set that environment variable in the Gateway runtime or replace the SecretRef with your preferred OpenClaw secret configuration. Do not publish the key.

Session transcript indexing is opt-in. Use `sources: ["memory", "sessions"]` and `experimental.sessionMemory: true` only if you want previous session transcripts searchable by memory tools.

### Embedding Model Choices

OpenRouter model availability and pricing change, so treat this as a dated example and verify before publishing your own config.

| Model | Use Case | Note |
| --- | --- | --- |
| `thenlper/gte-base` | default English memory search | cheap, simple baseline |
| `intfloat/multilingual-e5-large` | multilingual memory search | better fit for non-English or cross-language notes |
| `nvidia/llama-nemotron-embed-vl-1b-v2:free` | free or multimodal experiments | free, but expect caveats around availability, routing, provider terms, and model-specific input behavior |

When checked on 2026-05-25, OpenRouter listed [`thenlper/gte-base`](https://openrouter.ai/thenlper/gte-base) at `$0.005` per 1M tokens, [`intfloat/multilingual-e5-large`](https://openrouter.ai/intfloat/multilingual-e5-large) at `$0.01` per 1M tokens, and [`nvidia/llama-nemotron-embed-vl-1b-v2:free`](https://openrouter.ai/nvidia/llama-nemotron-embed-vl-1b-v2%3Afree) as free. Check OpenRouter's model page before relying on those prices. Do not point private memory at a free route until you have reviewed the provider's data handling and uptime tradeoffs.

If a model requires asymmetric input hints, use OpenClaw's OpenAI-compatible fields:

```json
{
  "queryInputType": "query",
  "documentInputType": "passage"
}
```

Do not add those fields unless the selected embedding model expects them. Changing embedding models or input-type behavior should be followed by a memory reindex.

### OpenAI Alternative

OpenAI remains a good embedding option:

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "openai",
        "model": "text-embedding-3-small",
        "sources": ["memory", "sessions"],
        "experimental": {
          "sessionMemory": true
        }
      }
    }
  }
}
```

Use this if you already have OpenAI auth configured and prefer fewer moving parts over routing embeddings through OpenRouter.

## Security Checklist

Before running a config like this long-term:

```bash
openclaw doctor --fix
openclaw security audit --deep
openclaw gateway status
openclaw status --all
```

Also check:

- Gateway is not bound to `0.0.0.0`.
- Control UI is not public.
- Telegram/BlueBubbles identifiers are allowlisted.
- No API keys or tokens are committed.
- Tool access matches the people and channels that can message the agent.

## Common Mistakes

- Treating this exact model list as the point. It is only one working setup.
- Exposing Control UI publicly because Tailscale setup feels annoying.
- Installing third-party skills without reading their source.
- Leaving broad tools enabled for channels with untrusted senders.
- Skipping `openclaw doctor` after editing config.
- Forgetting that `messages.groupChat.visibleReplies: "message_tool"` changes how group replies are sent.

## Related

- [Full guide](../guide.md)
- [Skill builder prompt](skill-builder-prompt.md)
- [Security hardening](security-hardening.md)
- [VPS setup](vps-setup.md)
