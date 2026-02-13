# OpenClaw Security Quick Start

New to OpenClaw security? Start here. These prompts help you implement basic security step by step.

For complete configuration reference, see [security-hardening.md](security-hardening.md).

---

## Before You Start

**Back up first:**
```bash
tar -czf ~/openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/
```

**Test changes carefully.** Security hardening can restrict agent functionality.

---

## Prompt 1: Security Audit

Audit your current OpenClaw security:

```
Check my OpenClaw deployment at ~/.openclaw/ for security issues:

1. In openclaw.json, check:
   - Are API keys hardcoded or using env vars (${VAR})?
   - Which tools are allowed? List dangerous ones (exec, cron, gateway)
   - Is logging.redactSensitive enabled?
   - Is gateway.bind set to loopback?

2. Check file permissions on ~/.openclaw/ and openclaw.json

Report as:
- CRITICAL: Fix immediately  
- HIGH: Fix today
- MEDIUM: Fix this week
```

---

## Prompt 2: Basic Hardening

Implement core security controls:

```
Update ~/.openclaw/openclaw.json with these security controls:

1. Add environment variables section:
{
  "env": {
    "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
    "OPENAI_API_KEY": "${OPENAI_API_KEY}",
    "GATEWAY_TOKEN": "${GATEWAY_TOKEN}"
  }
}

2. Set default tool policies:
{
  "agents": {
    "defaults": {
      "tools": {
        "allow": ["read", "write", "edit", "web_search"],
        "deny": ["exec", "cron", "gateway", "nodes"]
      }
    }
  }
}

3. Enable logging redaction:
{
  "logging": {
    "redactSensitive": "tools"
  }
}

4. Secure gateway:
{
  "gateway": {
    "bind": "loopback",
    "auth": {
      "mode": "token", 
      "token": "${GATEWAY_TOKEN}"
    }
  }
}

Show the complete updated config.
```

---

## Prompt 3: Cost Protection

Prevent surprise bills:

```
Add cost protection to my OpenClaw config:

1. Track model costs:
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
          }
        ]
      }
    }
  }
}

2. Create agents with appropriate models:
   - "monitor" agent: use gpt-5-nano only
   - "researcher" agent: use kimi/k2p5 or sonnet
   - No agent should default to Opus

3. Ensure Opus cannot be used by cron jobs or public-facing agents

Show which agents get which models.
```

**Important:** Also set hard limits in your Anthropic/OpenAI dashboards. Config tracking alone won't stop bills.

---

## Prompt 4: Backup Setup

Create automated backups:

```
Create a backup script at ~/.openclaw/scripts/backup.sh:

Requirements:
1. Backup location: ~/backups/openclaw/YYYY-MM-DD/
2. Include:
   - openclaw.json
   - workspace/*.md (AGENTS.md, SOUL.md, etc)
   - memory/*.md (last 30 days)
3. Encrypt with gpg
4. Make executable
5. Set up cron for daily 2 AM runs

Provide the complete script and cron line.
```

---

## What Each Prompt Does

| Prompt | Time | Risk |
|--------|------|------|
| Audit | 5 min | None |
| Hardening | 15 min | May limit agent capabilities |
| Cost Control | 10 min | May block expensive requests |
| Backup | 10 min | None |

---

## Next Steps

After these prompts:

1. **Review changes** - Make sure you understand what was modified
2. **Test agents** - Verify they still work as expected  
3. **Read the full guide** - See [security-hardening.md](security-hardening.md) for:
   - Detailed tool policy examples
   - Rate limiting
   - Prompt injection defense
   - Emergency procedures

---

## Troubleshooting

**Agents stopped working:**
- Check tool policies - you may have blocked a needed tool
- Review the "deny" list in agents.defaults.tools

**Can't access gateway:**
- `bind: loopback` means local access only
- This is correct for local deployments

**Costs still high:**
- Dashboard limits at providers matter more than config
- Set hard limits in Anthropic/OpenAI dashboards

---

## References

- [security-hardening.md](security-hardening.md) - Complete security reference
- OpenClaw Docs: https://docs.openclaw.ai/gateway/security
- OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/
