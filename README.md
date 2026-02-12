# OpenClaw Runbook (Non-Hype Edition)

> Tested with OpenClaw 2026.2.x  
> AI-assisted documentation created with Claude

This repo contains a practical guide for running OpenClaw day to day without burning money, quotas, or your sanity.

It is not an official guide.
It is not a "best setup."
It reflects how I actually run OpenClaw after breaking it repeatedly and wanting something stable, predictable, and boring in the best way.

If you are looking for flashy demos or "this changes everything" energy, this probably isn't it.

## What this is

- A runbook for people who want OpenClaw to run for weeks, not minutes
- Opinionated, but explicit about tradeoffs
- Focused on coordinator vs worker models, cost control, memory boundaries, and guardrails
- Written from the "post-honeymoon" phase

## What this is not

- A beginner tutorial
- A marketing page for models or vendors
- A claim that this setup is right for everyone

## The guide

The main guide lives here:

- [guide.md](./guide.md)

It includes real config snippets, explanations of why certain choices were made, and patterns that held up over time.

## Examples

The `examples/` directory contains actionable templates and references:

- **[agent-prompts.md](examples/agent-prompts.md)** - Creating specialized agents, model chains, and coordinator/researcher/communicator patterns
- **[spawning-patterns.md](examples/spawning-patterns.md)** - How to spawn sub-agents from skills, prompts, and cron jobs
- **[heartbeat-example.md](examples/heartbeat-example.md)** - Rotating heartbeat pattern for monitoring
- **[skill-builder-prompt.md](examples/skill-builder-prompt.md)** - Prompt template for creating AgentSkills
- **[task-tracking-prompt.md](examples/task-tracking-prompt.md)** - Build a task tracking system for agent visibility
- **[security-patterns.md](examples/security-patterns.md)** - Prompt injection defense and security rules
- **[vps-setup.md](examples/vps-setup.md)** - VPS deployment and hardening guide
- **[sanitized-config.json](examples/sanitized-config.json)** - Example OpenClaw configuration
- **[config-example-guide.md](examples/config-example-guide.md)** - Config section reference
- **[check-quotas.sh](examples/check-quotas.sh)** - Script to check API quota usage across providers

## Showcases

The `showcases/` directory contains copy-paste ready automation patterns from the community:

- **[daily-brief](showcases/daily-brief.md)** - Morning summary with weather, calendar, tasks
- **[idea-pipeline](showcases/idea-pipeline.md)** - Overnight research on captured ideas
- **[linkedin-drafter](showcases/linkedin-drafter.md)** - Weekly content generation
- **[tech-discoveries](showcases/tech-discoveries.md)** - Curated tech news
- **[homelab-access](showcases/homelab-access.md)** - Safe remote SSH via Telegram
- **[agent-orchestrator](showcases/agent-orchestrator.md)** - Route coding tasks to optimal tools

Each showcase is designed to be immediately usable. Copy the cron job, replace the placeholders, and deploy.

Have an automation that works well? See [showcases/template.md](showcases/template.md) to submit your own.

## Share This

If this guide helped you, please consider:

- **Sharing it** with others who might find it useful
- **Linking back** if you reference it in blog posts, videos, or other resources
- **Submitting your own showcases** so others can learn from your setup

This is a community resource. The more people contribute, the better it gets for everyone.

## Community Resources

Other helpful OpenClaw resources from the community:

**Official & Discovery**
- **[ClawHub](https://clawhub.com)** - Discover and share AgentSkills
- **[OpenClaw Docs](https://docs.openclaw.ai)** - Official documentation

**Awesome Lists**
- **[awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases)** - Real-world use cases and examples
- **[awesome-openclaw](https://github.com/SamurAIGPT/awesome-openclaw)** - Curated list of tools and resources
- **[awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)** - Community-contributed skills

These complement this runbook with more examples, skills, and community patterns.

## Contributing

Contributions are welcome, but this is not a free-for-all.

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening issues or pull requests.

## License

MIT
