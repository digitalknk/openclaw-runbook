# Homelab Access

**Category:** Infrastructure
**Example Model:** balanced
**Updated:** 2026-05-25

Remote homelab control should not require public SSH or a public OpenClaw dashboard. Use Tailscale for network access and a locked-down messaging channel for prompts.

## Quick Start

### Prerequisites

- [ ] Tailscale installed on the OpenClaw host and homelab devices.
- [ ] SSH key auth working manually.
- [ ] Telegram or another channel configured with allowlists.
- [ ] Confirmation rules for destructive commands.

### Tailscale And SSH

On each device:

```bash
tailscale up
tailscale ip -4
```

Add SSH hosts:

```sshconfig
Host homelab-nas
    HostName [TAILSCALE_IP]
    User [USERNAME]
    IdentityFile ~/.ssh/homelab_key
    StrictHostKeyChecking accept-new
```

Test outside OpenClaw:

```bash
ssh homelab-nas uptime
```

### Channel Rules

Add a role section to `AGENTS.md` or a local skill:

```markdown
## Homelab Access Rules

Accept homelab commands only from allowlisted users.

Allowed without confirmation:
- uptime
- df -h
- free -m
- systemctl status [service]
- journalctl -u [service] -n 100
- ping and curl -I

Requires explicit confirmation:
- systemctl restart
- package installs or upgrades
- config file edits
- reboot or shutdown

Always reject:
- rm -rf
- disk wiping commands
- password or user management
- firewall changes unless the user gives exact context
- commands that bypass Tailscale or open public ports

Run commands through SSH over Tailscale.
Return command, host, exit status, and output summary.
```

## Test Prompts

```text
Check uptime and disk usage on homelab-nas.
```

```text
Restart pihole on homelab-nas. Ask for confirmation first.
```

## Telegram Config Example

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "groups": {
        "*": {
          "requireMention": true
        }
      },
      "botToken": "<TELEGRAM_BOT_TOKEN>",
      "dmPolicy": "allowlist",
      "allowFrom": ["<YOUR_TELEGRAM_USER_ID>"],
      "groupAllowFrom": ["<YOUR_GROUP_ID>"],
      "linkPreview": false
    }
  }
}
```

## Security Checklist

- [ ] No public SSH port.
- [ ] No public OpenClaw dashboard.
- [ ] SSH keys are dedicated to homelab access.
- [ ] Telegram DMs and groups are allowlisted.
- [ ] Destructive commands require confirmation.
- [ ] Commands are logged.
- [ ] Tailscale ACLs restrict device access where possible.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| SSH works locally but not from OpenClaw | Check the OpenClaw process user and key path |
| Host not found | Use Tailscale IP or MagicDNS name |
| Bot accepts the wrong user | Fix `allowFrom` and `groupAllowFrom` |
| Agent runs too broad a command | Move the allowlist into a local skill and narrow the prompt |
| Commands hang | Add timeouts and avoid interactive commands |

## Related

- [security hardening](../examples/security-hardening.md)
- [vps setup](../examples/vps-setup.md)
