# OpenClaw Showcases

These are operational patterns you can adapt. They are not magic templates. Replace the placeholders, test manually, and keep remote access inside your chosen boundary.

Some showcases are community contributions or reviews of external projects. Preserve source attribution when editing those files, and do not rewrite them as if they were the runbook author's personal setup.

## How To Use These

1. Read the prerequisites.
2. Replace every `[PLACEHOLDER]`.
3. Add the cron job with `openclaw cron add` or your current config workflow.
4. Test with `openclaw cron run <job-id> --wait`.
5. Watch the first automatic run before trusting it.

## Showcases

| Showcase | Use Case | Model Guidance |
| --- | --- | --- |
| [daily-brief](daily-brief.md) | Morning weather, calendar, task summary | balanced or cheap |
| [idea-pipeline](idea-pipeline.md) | Overnight research on captured ideas | research-capable |
| [tech-discoveries](tech-discoveries.md) | Weekly curated tech links | balanced |
| [linkedin-drafter](linkedin-drafter.md) | Draft posts for review | stronger writing model |
| [homelab-access](homelab-access.md) | Tailscale SSH via Telegram with confirmations | balanced |
| [agent-orchestrator](agent-orchestrator.md) | Route coding tasks to specialist tools | strong reasoning |
| [coeus-knowledge-base](coeus-knowledge-base.md) | Local semantic knowledge base | local or balanced setup model |
| [autonomous-operation](autonomous-operation.md) | Community-contributed autonomous health-check pattern | cheap monitor, verify current docs |
| [claworc](claworc.md) | Community-contributed review of an external OpenClaw control-plane project | n/a |

## Model Guidance

The showcases use tiers instead of prescribing providers.

| Tier | Use For |
| --- | --- |
| cheap | status checks, heartbeat jobs, formatting, low-risk summaries |
| balanced | daily briefs, normal research, task cleanup |
| strong | public writing, complex planning, multi-step code routing |
| local | privacy-sensitive tasks, cheap background processing, offline workflows |

Use model IDs from your own `agents.defaults.models`. The sample config in this repo uses Z.ai and OpenRouter because it is a working example, not because the runbook requires those providers.

## Common Configuration

Most showcases need some mix of:

```json
{
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
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "allowlist",
      "allowFrom": ["<YOUR_TELEGRAM_USER_ID>"]
    }
  }
}
```

Add service-specific plugins or skills only when you need them. Keep ClawHub disabled by default; inspect third-party skills for ideas and rebuild a local version if the pattern is useful.

## Security Checklist

- [ ] No hardcoded secrets in prompts or config.
- [ ] Gateway binds to loopback.
- [ ] Dashboard access uses Tailscale or stays local.
- [ ] Telegram and group channels are allowlisted.
- [ ] Destructive commands require confirmation.
- [ ] Cron jobs use isolated sessions when they do not need live context.
- [ ] The first run was tested manually.
- [ ] Logs do not print tokens, passwords, or chat IDs.

## Template

Use [template.md](template.md) for a new showcase.

Related examples:

- [agent-prompts.md](../examples/agent-prompts.md)
- [config-example-guide.md](../examples/config-example-guide.md)
- [heartbeat-example.md](../examples/heartbeat-example.md)
- [security-hardening.md](../examples/security-hardening.md)
