# Homelab Access

**Category:** Infrastructure
**Example Model:** balanced
**Updated:** 2026-05-25

Remote homelab control should not require public SSH or a public OpenClaw dashboard. Use Tailscale for network access and a locked-down messaging channel for prompts.

> **HOW TO USE:** Set up SSH over Tailscale first, then add a Telegram or similar channel with strict allowlists and confirmation rules. Safe commands can run immediately. Destructive commands should require explicit confirmation.

## Quick Start

### 1. Prerequisites

- [ ] Tailscale installed on the OpenClaw host and homelab devices.
- [ ] SSH key auth working manually.
- [ ] Telegram or another channel configured with allowlists.
- [ ] Confirmation rules for destructive commands.
- [ ] Public SSH and public dashboard access disabled.

### 2. Set Up Tailscale And SSH

On each device:

```bash
tailscale up
tailscale ip -4
```

Add SSH hosts:

```text
Host homelab-router
    HostName [TAILSCALE_IP]
    User [USERNAME]
    IdentityFile ~/.ssh/homelab_key
    StrictHostKeyChecking accept-new

Host homelab-nas
    HostName [TAILSCALE_IP]
    User [USERNAME]
    IdentityFile ~/.ssh/homelab_key
    StrictHostKeyChecking accept-new
```

Test outside OpenClaw:

```bash
ssh homelab-router uptime
ssh homelab-nas df -h
```

Do not move on until manual SSH works. OpenClaw should not be debugging your basic network path.

### 3. Create Telegram Bot

1. Message `@BotFather` on Telegram.
2. Send `/newbot`.
3. Name your bot.
4. Save the API token.
5. Get your numeric Telegram user ID from a trusted ID bot or Telegram API tool.

Store secrets outside repo-tracked files. A published config should use placeholders:

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

### 4. Add Homelab Rules

Put this in `AGENTS.md`, a local skill, or a dedicated homelab agent prompt:

```markdown
## Homelab Access Rules

Accept homelab commands only from allowlisted users.

Always route SSH over Tailscale. Never open public ports to satisfy a request.

Allowed without confirmation:
- uptime
- df -h
- free -m
- systemctl status [service]
- journalctl -u [service] -n 100
- ping
- curl -I
- read-only ls/cat commands for non-secret paths

Requires explicit confirmation:
- systemctl restart
- package installs or upgrades
- config file edits
- reboot or shutdown
- commands that write files

Always reject:
- rm -rf
- dd or disk wiping commands
- password or user management
- firewall changes unless the user gives exact context
- commands that bypass Tailscale or expose public ports
- commands that print secrets, tokens, or private keys

Execution:
- SSH command format: ssh [host] [command]
- Timeout: 30 seconds unless the user explicitly approves a longer command
- Return host, command, exit status, and concise output
- Log every executed command
```

### 5. Test It

Send a safe request:

```text
Check uptime and disk usage on homelab-nas.
```

Expected behavior:

```text
host: homelab-nas
command: uptime && df -h
status: 0
summary: uptime returned normally; disk usage is below the configured warning threshold.
```

Send a destructive request:

```text
Restart pihole on homelab-nas.
```

Expected behavior:

```text
Confirm: run "sudo systemctl restart pihole" on homelab-nas?
Reply YES to execute.
```

The agent should not restart the service until you confirm.

## What This Does

**Problem:** You need remote access to homelab devices. Port forwarding is risky, public dashboards are worse, and VPN apps are not always convenient from a phone.

**Solution:** Telegram bot plus Tailscale plus SSH. You send commands through an allowlisted chat channel. Safe commands execute immediately. Dangerous commands require confirmation. Network access stays on Tailscale.

## Security Model

### Three-Tier Command System

**Tier 1 - Allow immediately**

```bash
uptime
df -h
free -m
systemctl status pihole
journalctl -u pihole -n 100
ping 1.1.1.1
curl -I https://example.com
```

**Tier 2 - Confirm first**

```bash
systemctl restart pihole
apt install htop
sed -i 's/foo/bar/' /etc/example.conf
reboot
```

**Tier 3 - Reject**

```bash
rm -rf /
dd if=/dev/zero of=/dev/sda
passwd
useradd admin
iptables -F
cat ~/.ssh/id_rsa
```

## Command Examples

**Check status**

```text
You: /homelab status router
Bot: homelab-router: uptime 45 days, load 0.12, root disk 67%.
```

**Check service**

```text
You: /homelab systemctl status pihole on nas
Bot: pihole.service is active and running. Last restart: 2026-02-10.
```

**Restart with confirmation**

```text
You: /homelab restart pihole on nas
Bot: Confirm: run "sudo systemctl restart pihole" on homelab-nas? Reply YES to execute.
You: YES
Bot: Done. pihole restarted on homelab-nas.
```

**Rejected command**

```text
You: /homelab print ssh private key
Bot: Rejected. That request would expose secrets.
```

## Advanced: Multi-User Support

If more than one person can use the bot, make approval rules explicit:

```markdown
Authorized users:
- [USER1]
- [USER2]

For destructive commands:
- A user may approve their own low-risk restart commands.
- Firewall changes, user management, and storage changes require approval from a second authorized user.
- Unknown users are ignored.
```

This is not enterprise access control. It is a practical guardrail for a personal or family homelab.

## Rate Limits

Add basic abuse protection to the prompt or local skill:

```markdown
Rate limits:
- Maximum 10 commands per hour per user.
- Maximum 3 confirmation-required commands per hour.
- Reject repeated failed confirmation attempts.
- Ask the user to slow down if commands are arriving too quickly.
```

## Troubleshooting

| Problem | Cause | Fix |
| --- | --- | --- |
| Permission denied | SSH key issue | Verify the key is in `~/.ssh/authorized_keys` on the device |
| Host not found | Tailscale DNS/IP issue | Use Tailscale IP or MagicDNS name |
| SSH works locally but not from OpenClaw | Process user mismatch | Check which user runs OpenClaw and which key path it can read |
| Bot accepts the wrong user | Bad allowlist | Fix `allowFrom` and `groupAllowFrom` |
| No response | Channel not receiving messages | Check bot token, webhook/polling setup, and group mention rules |
| Command timeout | Long-running command | Add timeouts and avoid interactive commands |
| Agent runs too broad a command | Prompt too vague | Move the allowlist into a local skill and narrow the command parser |

## Security Checklist

- [ ] No public SSH port.
- [ ] No public OpenClaw dashboard.
- [ ] SSH key-based auth only.
- [ ] SSH keys are dedicated to homelab access.
- [ ] Telegram DMs and groups are allowlisted.
- [ ] Group messages require a mention.
- [ ] Destructive commands require confirmation.
- [ ] Secret-reading commands are rejected.
- [ ] Commands are logged.
- [ ] Tailscale ACLs restrict device access where possible.
- [ ] Rate limits are documented.

## Variations

**Discord instead of Telegram:** Use the same rules with Discord user and channel allowlists.

**Slack integration:** Use Slack bot/webhook access, but keep destructive actions behind confirmation.

**Voice commands:** Add speech-to-text only after the text flow is reliable. Voice increases ambiguity.

**Read-only status bot:** Remove restart, install, write, and reboot commands entirely. This is the safest version.

**Two-person mode:** Require a second authorized user to approve destructive storage, firewall, or user-management changes.

## Related

- [security hardening](../examples/security-hardening.md)
- [vps setup](../examples/vps-setup.md)
- [daily brief](daily-brief.md) - Can include homelab status
- [tech discoveries](tech-discoveries.md) - Find new homelab tools

## Changelog

- **2026-02-09** - Initial version, Telegram-based
- **2026-02-10** - Added confirmation workflow, generalized
- **2026-05-25** - Updated for Tailscale-first access, current channel config, and stricter command rules
