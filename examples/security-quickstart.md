# OpenClaw Security Quick Start

Start here if you want a practical security pass before leaving OpenClaw running unattended.

For the longer reference, see [security-hardening.md](security-hardening.md).

## Before You Change Anything

Back up the current config:

```bash
tar -czf ~/openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/
```

Then inspect before editing:

```bash
openclaw doctor
openclaw gateway status
openclaw config get gateway
openclaw config get tools
openclaw config get channels
```

Do not paste secrets into prompts. Use OpenClaw auth profiles and the built-in secret flow for provider API keys.

## Prompt 1: Audit

```text
Audit my OpenClaw setup at ~/.openclaw.

Check:
1. gateway.bind, gateway.mode, gateway.auth, gateway.tailscale, and gateway.controlUi.
2. Whether the dashboard is reachable only through loopback or Tailscale.
3. Whether provider keys are managed through auth.profiles and secret storage instead of hardcoded config values.
4. Which plugins, channels, and tool profiles are enabled.
5. Whether ClawHub skills are disabled or review-only.
6. File permissions on ~/.openclaw and ~/.openclaw/openclaw.json.

Report:
- CRITICAL: public exposure, hardcoded secrets, unsafe channel allowlists
- HIGH: broad tools on unattended agents, weak Telegram allowlists
- MEDIUM: cleanup, logging, and documentation issues

Do not change files yet.
```

## Prompt 2: Tailscale-First Gateway

Use this when you can use Tailscale:

```text
Update my OpenClaw gateway config for a Tailscale-first setup.

Target behavior:
- gateway.mode is local
- gateway.bind is loopback
- gateway.auth.mode is token
- gateway.tailscale.mode is serve
- gateway.tailscale.resetOnExit is true
- gateway.controlUi.allowedOrigins contains only my Tailscale Control UI origin
- gateway.controlUi.allowInsecureAuth may remain true only because access is restricted to my Tailscale network

Preserve all working ports, tokens, channel settings, auth profiles, model providers, plugins, and hooks.
Show the diff before applying.
```

If you do not want Tailscale, keep the Gateway local and use a messaging channel such as Telegram for remote access. Do not expose the Control UI directly to the public internet.

## Prompt 3: Provider Secrets

```text
Review my provider authentication.

Goal:
- keep auth.profiles.<provider>.mode as api_key where appropriate
- avoid hardcoded API keys in openclaw.json
- confirm the configured model IDs match agents.defaults.models
- confirm agents.defaults.model.primary and fallbacks point to existing catalog entries

Use my current provider choices. Do not replace them with OpenAI, Anthropic, or any other provider unless I ask.
```

## Prompt 4: Channel Allowlist

```text
Review my Telegram and BlueBubbles channel config.

For Telegram:
- require an allowlist for DMs
- keep group requireMention enabled unless I explicitly opt out
- verify groupAllowFrom is narrow
- avoid link previews unless I ask for them

For BlueBubbles:
- verify the webhook path is not public without the expected auth boundary
- confirm the server URL and password are not printed in logs

Do not change working channel behavior unless a setting is clearly unsafe.
```

## Prompt 5: Skills

```text
Review my OpenClaw skills setup.

Policy:
- leave clawhub disabled by default
- do not install third-party skills directly from ClawHub
- if a ClawHub skill looks useful, inspect the source and write a local skill from scratch
- keep local skills narrow, auditable, and explicit about required tools

Report which skills are enabled, which are disabled, and which local skills should be rebuilt or removed.
```

## Prompt 6: Cost Guardrails

```text
Review model and cost risk in my OpenClaw config.

Check:
- agents.defaults.models catalog entries
- agents.defaults.model.primary and fallbacks
- cron and heartbeat jobs that may run unattended
- expensive models assigned to monitoring or routine tasks
- provider dashboard limits that I still need to set outside OpenClaw

Keep the guidance provider-agnostic. My model list is illustrative and may use Z.ai, OpenRouter, or another provider.
```

## Common Fixes

| Finding | Fix |
| --- | --- |
| Gateway binds to `0.0.0.0` | Change to loopback and access through Tailscale |
| Hardcoded API key in JSON | Move to provider auth profile and secret store |
| Telegram accepts anyone | Use DM allowlist and group sender allowlist |
| ClawHub enabled by default | Disable it; use source as inspiration only |
| Cron uses a premium model for checks | Assign a cheaper explicit model |
| Dashboard exposed by reverse proxy | Remove public exposure; use Tailscale or local-only |

## References

- [security-hardening.md](security-hardening.md)
- [vps-setup.md](vps-setup.md)
- [config-example-guide.md](config-example-guide.md)
