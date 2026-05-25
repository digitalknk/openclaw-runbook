# VPS Setup Guide

This guide covers a small OpenClaw VPS with Tailscale as the preferred access path.

You do not need a large machine. A small VPS such as a Hetzner CX23-class box is usually enough for the Gateway if your models are hosted elsewhere.

## Target Setup

- VPS runs OpenClaw.
- Gateway binds to loopback.
- Tailscale handles SSH and Control UI access.
- Public SSH is blocked after Tailscale SSH is verified.
- Remote chat goes through Telegram, BlueBubbles, or another configured channel.

If you do not want Tailscale, keep OpenClaw local and use a messaging channel for remote access. Do not replace Tailscale with a public dashboard unless you have a clear reason and understand the risk.

## Install Tailscale Safely

Do this in order to avoid locking yourself out.

### 1. Install Tailscale locally

Install Tailscale on your laptop/desktop and sign in:

```bash
tailscale status
```

### 2. Install Tailscale on the VPS

SSH to the public IP first:

```bash
ssh user@<PUBLIC_VPS_IP>
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --ssh=true
```

### 3. Get the Tailnet address

```bash
tailscale ip -4
hostname
```

### 4. Verify Tailscale SSH

From your local machine:

```bash
ssh user@<TAILSCALE_IP_OR_HOSTNAME>
```

Do not block public SSH until this works.

### 5. Block public SSH

Use your VPS provider firewall. Block inbound port 22 from the public internet after Tailscale SSH is confirmed.

Then test:

```bash
ssh user@<TAILSCALE_IP_OR_HOSTNAME>
ssh user@<PUBLIC_VPS_IP>
```

The Tailscale path should work. The public path should fail.

Keep the provider web console available while changing firewall rules.

## Install OpenClaw

Use current onboarding:

```bash
openclaw onboard --install-daemon
openclaw gateway status
openclaw dashboard
```

Then validate:

```bash
openclaw doctor --fix
openclaw security audit --deep
openclaw status --all
```

## Gateway Config

Use loopback plus Tailscale Serve:

```json
{
  "gateway": {
    "mode": "local",
    "port": 18789,
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "<LONG_RANDOM_TOKEN>"
    },
    "tailscale": {
      "mode": "serve",
      "resetOnExit": true
    },
    "controlUi": {
      "allowedOrigins": ["https://<YOUR_TAILSCALE_HOSTNAME>"]
    }
  }
}
```

If you use `allowInsecureAuth: true`, keep it limited to a controlled Tailnet-only setup with explicit origins. Do not use that setting for public access.

## Verify Binding

```bash
lsof -nP -iTCP:18789 -sTCP:LISTEN
```

You want loopback, not `0.0.0.0`.

If the Gateway is exposed:

```bash
openclaw config set gateway.bind loopback
openclaw gateway restart
```

## Channels for Remote Use

Telegram is a good fallback if you do not want to use the dashboard remotely:

```json
{
  "plugins": {
    "entries": {
      "telegram": {
        "enabled": true
      }
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "allowlist",
      "allowFrom": ["<YOUR_TELEGRAM_USER_ID>"],
      "groups": {
        "*": {
          "requireMention": true
        }
      }
    }
  }
}
```

That keeps the Gateway private while still giving you remote interaction.

## Permissions

```bash
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/openclaw.json
chmod 700 ~/.openclaw/credentials
```

## Config Rollback

Track your config and workspace in a private repo:

```bash
cd ~/.openclaw
git init
printf 'agents/*/sessions/\nagents/*/agent/*.jsonl\n*.log\ncredentials/\n' > .gitignore
git add .gitignore openclaw.json workspace
git commit -m "config: baseline"
```

Commit before and after risky changes:

```bash
git status --short
openclaw doctor --fix
git commit -am "config: update model routing"
```

Do not commit credentials.

## Tool Policy

Start with the minimum tools that make the VPS useful:

```json
{
  "tools": {
    "profile": "messaging",
    "deny": ["group:automation", "group:runtime", "group:fs", "sessions_spawn", "sessions_send"],
    "fs": {
      "workspaceOnly": true
    },
    "exec": {
      "security": "deny",
      "ask": "always"
    }
  }
}
```

Widen access per agent after testing.

## Monitoring

```bash
openclaw gateway status
openclaw status --all
openclaw health --json
openclaw tasks audit
openclaw cron list
```

Use heartbeat for approximate awareness. Use cron for exact schedules.

## Backups

Back up config and workspace:

```bash
mkdir -p ~/backups/openclaw
tar czf ~/backups/openclaw/openclaw-$(date +%Y-%m-%d).tar.gz \
  ~/.openclaw/openclaw.json \
  ~/.openclaw/workspace
```

Handle credentials separately. They are sensitive.

## Troubleshooting

### Tailscale SSH fails

```bash
sudo tailscale status
sudo tailscale up --ssh=true
tailscale ip -4
```

Use the provider console if firewall changes locked you out.

### Gateway will not start

```bash
openclaw doctor --fix
openclaw gateway status
openclaw logs
```

### Port already in use

```bash
lsof -nP -iTCP:18789 -sTCP:LISTEN
```

Stop the old process or change the configured port.

## Checklist

- [ ] Tailscale SSH works before public SSH is blocked.
- [ ] Public SSH is blocked after verification.
- [ ] Gateway binds to loopback.
- [ ] Token auth is enabled.
- [ ] Control UI is reached through Tailscale or not exposed.
- [ ] Telegram or another channel is allowlisted if used remotely.
- [ ] `openclaw doctor --fix` has been run.
- [ ] `openclaw security audit --deep` has been reviewed.
- [ ] Config is backed up.
- [ ] Credentials are not committed.

## Related

- [Config guide](config-example-guide.md)
- [Security hardening](security-hardening.md)
- [Heartbeat example](heartbeat-example.md)
