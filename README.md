# OpenClaw Runbook

> Checked against OpenClaw at commit `5dccba7405` (`2026-05-25`)
> Example config based on a working `2026.5.x` setup

This repo is a practical runbook for running OpenClaw day to day without burning money, exposing your gateway, or trusting random automation you did not inspect.

It is not official OpenClaw documentation.
It is not a universal best setup.
It is the way I run OpenClaw after enough broken configs, noisy agents, and avoidable risk to want something predictable.

## What this is

- A runbook for people who want OpenClaw to run for weeks, not minutes
- Opinionated guidance on models, access, memory, automation, and guardrails
- Tailscale-first for dashboard/control access
- Skeptical of third-party skills by default
- Written from the post-honeymoon phase

## What this is not

- A beginner replacement for the official docs
- A model leaderboard
- A ClawHub install guide
- A claim that my exact config is right for everyone

## Access stance

My setup uses Tailscale as the normal access path, including when I am local. The Gateway stays loopback-bound, and Tailscale handles remote access.

If you do not want to sign up for Tailscale, keep OpenClaw local and use a messaging channel such as Telegram for remote use. Avoid public ports and casual LAN exposure unless you know exactly what boundary you are accepting.

## Skills stance

I do not recommend blindly installing third-party skills from ClawHub.

Use ClawHub as a discovery and source-reading tool. Find an idea, inspect the source, then ask your agent to rebuild a local skill for your setup. That is slower than clicking install, but it is safer than trusting unknown code, broad tool assumptions, hidden behavior, or token-heavy abstractions.

The example config keeps `clawhub` disabled on purpose.

## The guide

The main guide lives here:

- [guide.md](./guide.md)

It covers the current setup flow, Tailscale-first access, model routing, memory, automation, skills, and security.

## Examples

The `examples/` directory contains templates and references:

- [sanitized-config.json](examples/sanitized-config.json) - Current sanitized config reference
- [config-example-guide.md](examples/config-example-guide.md) - Config section reference
- [agent-prompts.md](examples/agent-prompts.md) - Specialized agent examples
- [spawning-patterns.md](examples/spawning-patterns.md) - Current `sessions_spawn` and subagent patterns
- [heartbeat-example.md](examples/heartbeat-example.md) - Heartbeat checklist and `tasks:` pattern
- [task-tracking-prompt.md](examples/task-tracking-prompt.md) - Using OpenClaw's task ledger instead of an external black box
- [security-hardening.md](examples/security-hardening.md) - Security baseline and audit workflow
- [security-quickstart.md](examples/security-quickstart.md) - Prompts for applying basic guardrails
- [security-patterns.md](examples/security-patterns.md) - Prompt injection rules
- [vps-setup.md](examples/vps-setup.md) - VPS setup with Tailscale as the default remote access path
- [skill-builder-prompt.md](examples/skill-builder-prompt.md) - Prompt template for rebuilding local skills
- [check-quotas.sh](examples/check-quotas.sh) - Optional quota check helper

## Showcases

The `showcases/` directory contains automation patterns you can adapt:

- [daily-brief](showcases/daily-brief.md) - Morning summary with weather, calendar, and tasks
- [idea-pipeline](showcases/idea-pipeline.md) - Overnight research on captured ideas
- [linkedin-drafter](showcases/linkedin-drafter.md) - Weekly draft generation
- [tech-discoveries](showcases/tech-discoveries.md) - Curated tech news
- [homelab-access](showcases/homelab-access.md) - Safer remote SSH through Telegram confirmations
- [agent-orchestrator](showcases/agent-orchestrator.md) - Route coding tasks to configured agents/tools
- [coeus-knowledge-base](showcases/coeus-knowledge-base.md) - Local semantic knowledge base example
- [autonomous-operation](showcases/autonomous-operation.md) - Community-contributed health-check pattern
- [claworc](showcases/claworc.md) - Community-contributed review of an external control-plane project

Treat showcases as starting points. Review tool access, channels, delivery targets, and model choices before running them unattended. Some showcases are community contributions or external project reviews; keep their attribution intact.

## Share This

If this guide helped you, please consider:

- sharing it with others who might find it useful;
- linking back if you reference it in blog posts, videos, or other resources;
- submitting your own showcases so others can learn from your setup.

This is a community resource. The more people contribute real working patterns, the better it gets.

## Community resources

- [OpenClaw Docs](https://docs.openclaw.ai) - Official documentation
- [ClawHub](https://clawhub.com) - Good for discovery and source inspection; not something I install from blindly
- [OpenClaw GitHub](https://github.com/openclaw/openclaw) - Issues, releases, and source
- [awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases) - Real-world use cases and examples
- [awesome-openclaw](https://github.com/SamurAIGPT/awesome-openclaw) - Curated tools and resources
- [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) - Community-contributed skills to inspect before rebuilding your own

## Contributing

Contributions are welcome, but this is not a free-for-all.

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening issues or pull requests.

## License

MIT
