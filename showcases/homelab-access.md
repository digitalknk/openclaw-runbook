# Homelab Access

**Category:** Infrastructure  
**Example Model:** Balanced tier (Sonnet, Gemini Flash, etc.)  
**Updated:** 2026-02-09

> **HOW TO USE:** Copy the Telegram bot setup and safety rules below. This lets you run SSH commands on homelab devices via Telegram with confirmation prompts for dangerous operations.

## Quick Start

### 1. Prerequisites

- [ ] Tailscale (or WireGuard, ZeroTier) installed on all devices
- [ ] SSH keys configured and authorized on devices
- [ ] Telegram bot created via @BotFather
- [ ] SSH access working manually first

### 2. Set Up Tailscale

On each homelab device:
```bash
# Install
curl -fsSL https://tailscale.com/install.sh | sh

# Authenticate
tailscale up

# Get Tailscale IP
tailscale ip -4
# Note this IP for SSH config
```

### 3. Configure SSH

Add to `~/.ssh/config`:
```
Host homelab-router
    HostName [TAILSCALE_IP]  # e.g., 100.x.x.x
    User [USERNAME]
    IdentityFile ~/.ssh/homelab_key
    StrictHostKeyChecking accept-new

Host homelab-nas
    HostName [TAILSCALE_IP]
    User [USERNAME]
    IdentityFile ~/.ssh/homelab_key
```

Test manually:
```bash
ssh homelab-router uptime
```

### 4. Create Telegram Bot

1. Message @BotFather on Telegram
2. Send `/newbot`
3. Name your bot (e.g., "MyHomelabBot")
4. Save the API token
5. Get your chat ID from @userinfobot

Add to `~/.openclaw/credentials/`:
```
TELEGRAM_BOT_TOKEN=[YOUR_BOT_TOKEN]
TELEGRAM_CHAT_ID=[YOUR_CHAT_ID]
```

### 5. Copy This Agent Config

Add to your gateway config:

```yaml
agents:
  homelab:
    model: anthropic/claude-sonnet-4-5
    tools:
      - message
      - exec
    system: |
      You are a homelab access controller. Handle SSH commands from Telegram.

      VALIDATION RULES:
      1. Verify sender is authorized ([YOUR_TELEGRAM_USERNAME])
      2. Parse command from message
      3. Check command against allowlist

      ALLOWLIST (no confirmation):
      - Status: uptime, df -h, free -m, systemctl status [service]
      - Network: ping, curl -I, ip addr
      - Info: ls, cat (read-only files)

      REQUIRES CONFIRMATION (ask "Execute? Reply YES"):
      - Service restart: systemctl restart
      - Package install: apt install, pip install
      - File changes: sed, echo >, editing configs
      - Reboot: reboot, shutdown

      FORBIDDEN (always reject):
      - rm -rf, dd, disk wiping
      - Password changes, user management
      - Firewall changes without explicit context

      EXECUTION:
      - SSH via Tailscale: ssh [host] [command]
      - Timeout: 30 seconds
      - Return output to Telegram
```

### 6. Test It

Send to your Telegram bot:
```
/homelab status router
```

Should return uptime info.

---

## What This Does

**Problem:** Need remote access to homelab devices. Port forwarding is risky, VPN apps are clunky, native apps are inconsistent.

**Solution:** Telegram bot + Tailscale + SSH. You send commands via Telegram bot. Safe commands execute immediately. Dangerous commands require "YES" confirmation. All over Tailscale (encrypted, no port forwarding).

## Security Model

### Three-Tier Command System

**Tier 1 - Allow (immediate execution):**
```bash
uptime                    # OK
df -h                     # OK
free -m                   # OK
systemctl status pihole   # OK
ping google.com           # OK
ls /etc/nginx             # OK
cat /etc/hosts            # OK
```

**Tier 2 - Confirm (ask first):**
```bash
systemctl restart pihole  # "Confirm: restart pihole? Reply YES"
apt install htop          # "Confirm: install htop? Reply YES"
echo "config" > file     # "Confirm: write to file? Reply YES"
reboot                    # "Confirm: reboot? Reply YES"
```

**Tier 3 - Forbidden (always reject):**
```bash
rm -rf /                  # REJECTED
dd if=/dev/zero           # REJECTED
passwd                    # REJECTED
iptables -F               # REJECTED
```

## Command Examples

**Check status:**
```
You: /homelab status router
Bot: uptime: 45 days, load: 0.12, disk: 67%
```

**Check service:**
```
You: /homelab systemctl status pihole on nas
Bot: pihole.service - Pi-hole DNS
     Active: active (running) since Mon 2026-02-10
```

**Restart with confirmation:**
```
You: /homelab restart pihole on nas
Bot: Confirm: systemctl restart pihole on homelab-nas?
      Reply YES to execute.
You: YES
Bot: Executing... Done. Pi-hole restarted.
```

## Advanced: Multi-User Support

Allow multiple authorized users:
```yaml
system: |
  Authorized users: [USER1], [USER2]
  
  For destructive commands (Tier 2):
  - User1 can approve their own commands
  - OR require approval from User2 (two-person rule)
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "Permission denied" | SSH key issue | Verify key is in `~/.ssh/authorized_keys` on device |
| "Host not found" | Tailscale not connected | Run `tailscale up` on device |
| No response | Bot not receiving messages | Check webhook/polling setup |
| Command timeout | Long-running command | Increase timeout or run in background |

## Security Checklist

- [ ] Tailscale ACLs restrict which devices can talk
- [ ] SSH key-based auth only (no passwords)
- [ ] Separate SSH keys for homelab (not personal keys)
- [ ] Confirmation required for destructive commands
- [ ] All commands logged to audit file
- [ ] Rate limiting (max 10 commands/hour)

## Variations

**Discord instead of Telegram:**
```yaml
system: |
  Accept commands from Discord user [DISCORD_USER_ID]
  ...same rules...
```

**Slack integration:**
Use Slack bot with incoming webhooks.

**Voice commands:**
Add speech-to-text layer: "Hey Assistant, restart the NAS"

**Web dashboard:**
Simple web UI for common commands with big buttons.

## Related

- [daily-brief](daily-brief.md) - Can include homelab status
- [tech-discoveries](tech-discoveries.md) - Find new homelab tools

## Changelog

- **2026-02-09** - Initial version, Telegram-based
- **2026-02-10** - Added confirmation workflow, generalized
