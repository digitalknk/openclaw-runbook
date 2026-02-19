# OpenClaw Showcases

Real-world automation patterns you can copy, paste, and customize. Each showcase is designed to be immediately usable with minimal edits.

## How to Use These

Each showcase follows the same format:

1. **Quick Start** - Copy-paste ready cron job and prompt
2. **Replace `[PLACEHOLDERS]`** - Fill in your specific values
3. **Test** - Run manually with `openclaw cron run [job-name]`
4. **Deploy** - Let it run automatically

> **Time to first automation:** 5-10 minutes per showcase

## Showcases by Category

### Daily Automation
Stay organized without manual effort.

| Showcase | What It Does | Example Model |
|----------|--------------|---------------|
| [daily-brief](daily-brief.md) | Morning summary (weather, calendar, tasks) | Balanced tier |
| [idea-pipeline](idea-pipeline.md) | Overnight research on your ideas | Research tier |
| [coeus-knowledge-base](coeus-knowledge-base.md) | Self-hosted knowledge capture with semantic search | Any (local CPU) |

### Content & Research
Automate research and content creation.

| Showcase | What It Does | Example Model |
|----------|--------------|---------------|
| [linkedin-drafter](linkedin-drafter.md) | Weekly post drafts in your voice | Premium tier |
| [tech-discoveries](tech-discoveries.md) | Curated tech news weekly | Balanced tier |

### Infrastructure & Operations
Manage systems and access safely.

| Showcase | What It Does | Example Model |
|----------|--------------|---------------|
| [homelab-access](homelab-access.md) | Safe SSH via Telegram with confirmations | Balanced tier |

### Development & Coding
Agents that help with code and technical tasks.

| Showcase | What It Does | Example Model |
|----------|--------------|---------------|
| [agent-orchestrator](agent-orchestrator.md) | Route tasks to optimal CLI tools | Premium tier |

## Model Tier Reference

The showcases reference model tiers as **examples**. Use whatever models you have configured:

| Tier | Example Models | Best For | Cost |
|------|----------------|----------|------|
| **Premium** | Opus, GPT-4/5, Gemini Pro | Complex reasoning, creative tasks | Higher |
| **Upper Balanced** | Kimi, Gemini Pro | Good reasoning, fast | Medium |
| **Balanced** | Sonnet, GLM, Gemini Flash | General tasks | Low |
| **Cheap** | Haiku, Flash-Lite, Nano | Simple tasks, high volume | Minimal |

**Note:** Your models may have different names. The showcases work with any model - adjust based on your setup and budget.

## Quick Start Template

Don't see what you need? Copy this template and build your own:

> **[template.md](template.md)** - Start here for your own showcases

The template includes:
- Copy-paste ready cron job structure
- Prompt template with placeholders
- Troubleshooting guide
- Cost estimation framework

## Submitting Your Own

Built something useful? Share it:

1. Copy `template.md`
2. Fill in your use case
3. Test it works
4. Submit a PR

**Requirements for submission:**
- ✅ Copy-paste ready (minimal edits to work)
- ✅ All `[PLACEHOLDERS]` clearly marked
- ✅ Prerequisites checklist included
- ✅ Cost estimate provided
- ✅ Tested and working
- ✅ No personal info (use placeholders)

## Common Configuration

Most showcases need these tools configured in your gateway:

```yaml
tools:
  # For fetching data
  weather: {}        # Built-in, no API key
  calendar: {}       # Google, Nextcloud, etc.
  todoist: {}        # Or your task manager
  
  # For research
  web_search: {}     # Brave, Serper (API key needed)
  browser: {}        # For HN, Reddit
  email: {}          # IMAP/SMTP access
  
  # For delivery
  message: {}        # Telegram, Discord
  
  # For execution
  exec: {}           # SSH, local commands
```

## Security Checklist

Before deploying any showcase:

- [ ] No hardcoded secrets in prompts or config
- [ ] API keys in `~/.openclaw/credentials/` directory only
- [ ] Sensitive commands require confirmation (if applicable)
- [ ] Output doesn't leak personal data
- [ ] Isolated sessions for automated jobs
- [ ] Review what data sources the agent accesses

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Job not running | Check `tz` field matches your timezone |
| Missing tool | Add to gateway config `tools:` section |
| Wrong output | Make prompt more specific |
| Rate limited | Reduce frequency or use cheaper model |
| Placeholders not replaced | Search for `[YOUR_...]` and fill in |

## Variations

Each showcase includes ideas for customization:

- **Different schedule** - Change cron expression
- **Different delivery** - Telegram, Discord, email, Slack
- **Different sources** - Swap tools for alternatives
- **Extended scope** - Add more data sources
- **Simplified version** - Strip down for lower cost

## Related Resources

- [agent-prompts.md](../examples/agent-prompts.md) - Model selection guide
- [config-example-guide.md](../examples/config-example-guide.md) - Gateway config examples
- [heartbeat.md](../examples/heartbeat.md) - Periodic checks pattern

---

**Want to contribute?** See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
