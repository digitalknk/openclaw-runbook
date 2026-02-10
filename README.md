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

- **[agent-prompts.md](examples/agent-prompts.md)** - How to create specialized agents with proper model chains
- **[heartbeat-example.md](examples/heartbeat-example.md)** - Rotating heartbeat pattern for monitoring
- **[skill-builder-prompt.md](examples/skill-builder-prompt.md)** - Prompt template for creating AgentSkills
- **[task-tracking-prompt.md](examples/task-tracking-prompt.md)** - Build a task tracking system for agent visibility
- **[security-patterns.md](examples/security-patterns.md)** - Prompt injection defense and security rules
- **[vps-setup.md](examples/vps-setup.md)** - VPS deployment and hardening guide
- **[sanitized-config.json](examples/sanitized-config.json)** - Example OpenClaw configuration
- **[config-example-guide.md](examples/config-example-guide.md)** - Config section reference
- **[check-quotas.sh](examples/check-quotas.sh)** - Script to check API quota usage across providers

## Contributing

Contributions are welcome, but this is not a free-for-all.

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening issues or pull requests.

## License

MIT
