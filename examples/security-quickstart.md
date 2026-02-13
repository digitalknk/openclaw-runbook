# OpenClaw Security Quick Start

New to OpenClaw security? Start here. These prompts help you implement basic security hardening step by step.

For complete configuration reference, see [security-hardening.md](security-hardening.md).

---

## Before You Start

**Back up your configuration:**
```bash
tar -czf ~/openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/
```

**Test in a safe environment first.** These changes can restrict agent functionality.

---

## Prompt 1: Security Audit

Copy and paste this to audit your current OpenClaw security:

```
Audit my OpenClaw deployment at ~/.openclaw/ for security issues.

Check the following in openclaw.json:
1. Are API keys hardcoded anywhere, or are they using env var substitution (${VAR})?
2. What tools are currently allowed? List any dangerous tools (exec, cron, gateway, nodes).
3. Is logging.redactSensitive enabled?
4. What is the gateway bind setting? (Should be "loopback" for local deployments)
5. Are there any agents without workspace restrictions that might create isolated directories?

Check file permissions:
6. What are the permissions on ~/.openclaw/ and ~/.openclaw/openclaw.json?

Report findings with severity:
- CRITICAL: Fix immediately
- HIGH: Fix today
- MEDIUM: Fix this week
- LOW: Address when convenient
```

---

## Prompt 2: Basic Hardening

Implement core security controls:

```
Update my OpenClaw configuration at ~/.openclaw/openclaw.json to implement these security controls:

1. Add environment variable section if missing:
{
  "env": {
    "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
    "OPENAI_API_KEY": "${OPENAI_API_KEY}",
    "GATEWAY_TOKEN": "${GATEWAY_TOKEN}"
  }
}

2. Set up default tool policies to deny dangerous tools:
{
  "agents": {
    "defaults": {
      "tools": {
        "allow": ["read", "write", "edit", "web_search", "web_fetch"],
        "deny": ["exec", "process", "cron", "gateway", "nodes"]
      }
    }
  }
}

3. Enable sensitive data redaction:
{
  "logging": {
    "redactSensitive": "tools"
  }
}

4. Secure the gateway (for local deployments):
{
  "gateway": {
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "${GATEWAY_TOKEN}"
    }
  }
}

Show me the complete updated configuration. Do not restart anything yet.
```

---

## Prompt 3: Cost Protection

Set up cost controls to prevent runaway bills:

```
Add cost protection to my OpenClaw configuration:

1. Add model costs to track spending:
{
  "models": {
    "providers": {
      "anthropic": {
        "models": [
          {
            "id": "claude-opus-4-6",
            "cost": { "input": 5.0, "output": 25.0 }
          },
          {
            "id": "claude-sonnet-4-5",
            "cost": { "input": 3.0, "output": 15.0 }
          },
          {
            "id": "claude-haiku-4-5",
            "cost": { "input": 1.0, "output": 5.0 }
          }
        ]
      }
    }
  }
}

2. Restrict expensive models to specific agents only:
Create a "researcher" agent that can use Opus, and a "monitor" agent that only uses Haiku.

3. Set up agent configurations that prevent Opus from being used by:
   - Cron jobs
   - Public-facing agents
   - Monitoring agents

Show me which agents should have which model access.
```

**Note:** You must also set up cost alerts in your Anthropic/OpenAI dashboards. The config above tracks costs but doesn't set hard limits.

---

## Prompt 4: Backup Setup

Create an automated backup:

```
Create a backup script for my OpenClaw configuration at ~/.openclaw/:

Requirements:
1. Script location: ~/.openclaw/scripts/backup.sh
2. Backup location: ~/backups/openclaw/YYYY-MM-DD/
3. Include these files:
   - openclaw.json (main config)
   - workspace/*.md (AGENTS.md, SOUL.md, TOOLS.md, etc.)
   - memory/*.md (last 30 days only)
4. Encrypt the backup with gpg
5. Clean up backups older than 90 days
6. Make the script executable

Also create a cron job that runs this daily at 2 AM.

Provide the complete script and cron configuration.
```

---

## What These Prompts Do

| Prompt | Security Level | Risk | Time |
|--------|---------------|------|------|
| Audit | Assessment | None | 5 min |
| Basic Hardening | Medium | May restrict some agent capabilities | 15 min |
| Cost Protection | High | May block expensive model requests | 10 min |
| Backup Setup | Essential | None | 10 min |

---

## Next Steps

After running these prompts:

1. **Review the changes** - Make sure you understand what was modified
2. **Test your agents** - Verify they still work as expected
3. **Check the full guide** - See [security-hardening.md](security-hardening.md) for:
   - Detailed tool policy examples
   - Rate limiting configuration
   - Prompt injection defense
   - Emergency response procedures
   - Security maintenance schedules

---

## Troubleshooting

**Agents stopped working:**
- Check tool policies - you may have blocked a tool the agent needs
- Review the "deny" list in agents.defaults.tools

**Can't access gateway:**
- If you set `bind: loopback`, you can only access from the local machine
- This is correct for local deployments, but check your use case

**Costs still high:**
- Dashboard limits at the provider level are more important than config tracking
- Set hard limits in Anthropic/OpenAI dashboards

---

## Source

Based on security best practices from the OpenClaw community and security research.

For the complete security methodology and additional hardening steps, see [security-hardening.md](security-hardening.md).
