# Autonomous Operation Pattern

**Enable OpenClaw to run autonomously for extended periods with self-healing capabilities.**
**Ownership note:** Community-contributed showcase. Preserve the source context and avoid rewriting it as the runbook author's personal setup.

## Current-Version Note

This pattern predates the latest OpenClaw task, heartbeat, and cron documentation. Use it as an operational idea, then verify the commands and scheduling approach against the current docs before deploying it unattended.

## The Problem

OpenClaw sessions can crash or get stuck. Long-running autonomous operations need:
- Health monitoring
- Automatic recovery
- State persistence (checkpointing)

## The Solution

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Main Session (Coordinator)            │
│  - Thin: max 2 tool calls (spawn/send only)            │
│  - Spawns monitor subagent                             │
└──────────────────────┬──────────────────────────────────┘
                       │ spawns
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Monitor Subagent (every 5 min)             │
│  - Check gateway health                                 │
│  - Check process status                                 │
│  - Log to autonomous-op.log                           │
│  - Alert if issues found                               │
└──────────────────────┬──────────────────────────────────┘
                       │ cron (every 30 min)
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Self-Check Script (cron)                   │
│  - Verify gateway responding                            │
│  - Check for stuck processes                           │
│  - Auto-restart if needed                              │
└─────────────────────────────────────────────────────────┘
```

### Components

#### 1. Self-Check Script

```bash
#!/bin/bash
# ~/.openclaw/workspace/scripts/self-check.sh

LOG_FILE="$HOME/.openclaw/workspace/memory/autonomous-op.log"
GATEWAY_URL="http://127.0.0.1:18789"

echo "$(date) - Running self-check..." >> $LOG_FILE

# Check gateway health
HEALTH=$(curl -s $GATEWAY_URL/health 2>/dev/null | jq -r '.status' 2>/dev/null)

if [ "$HEALTH" != "ok" ]; then
    echo "$(date) - ALERT: Gateway not healthy: $HEALTH" >> $LOG_FILE
    # Trigger recovery
    openclaw gateway restart
else
    echo "$(date) - OK: Gateway healthy" >> $LOG_FILE
fi
```

#### 2. Monitor Subagent

```yaml
# Spawn from main session
name: monitor-health
schedule: every 5 minutes
model: cheap (minimax-m2.5:free)
tasks:
  - Check gateway: curl -s http://127.0.0.1:18789/health
  - Check processes: ps aux | grep openclaw
  - Log results
  - Alert if issues
```
> **Note:** This YAML is pseudocode for illustration. OpenClaw uses JSON for configuration files. The YAML shows the intended structure; implement using JSON in your actual config.

#### 3. Cron Recovery

```bash
# Add to cron: crontab -e
*/30 * * * * ~/.openclaw/workspace/scripts/self-check.sh >> /var/log/openclaw-selfcheck.log 2>&1
```

### Reference: Thin Main Session Rule

Keep the main session minimal:

```markdown
## Rule: Thin Main Session

Main session should only:
1. Spawn subagents
2. Send messages to subagents

All actual work happens in isolated subagent sessions.

This prevents context switching and keeps coordinator fast.
```

## Benefits

- **Resilience**: Auto-recovers from crashes
- **Visibility**: Log tracks all health checks
- **Cost**: Uses cheap models for monitoring
- **Autonomy**: Runs without human intervention for 7+ hours

## Configuration

```json
{
  "subagents": {
    "maxConcurrent": 4
  },
  "model": "minimax-m2.5:free"
}
```

## Usage

1. Deploy self-check script to cron
2. Spawn monitor subagent at session start
3. Keep main session thin
4. Monitor via `tail -f memory/autonomous-op.log`

---

*Pattern developed through practical experience with OpenClaw 2026.x*
