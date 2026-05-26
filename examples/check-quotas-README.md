# Check Quotas Script

This is an optional helper for provider spend checks. It is not an OpenClaw requirement, and it should not replace provider-side hard limits.

The current runbook recommends OpenClaw auth profiles and the built-in secret flow for provider keys. This script only works for providers whose keys you intentionally expose to a local file or environment variable for reporting.

## Installation

```bash
cp examples/check-quotas.sh ~/.local/bin/check-quotas
chmod +x ~/.local/bin/check-quotas
```

## Configuration

By default, the script checks:

- `$OPENROUTER_API_KEY`, then `$OPENCLAW_CREDENTIALS_DIR/openrouter`
- `$ZAI_API_KEY`, then `$OPENCLAW_CREDENTIALS_DIR/zai`

Default credentials directory:

```bash
~/.openclaw/credentials
```

Each file should contain only the raw token:

```bash
mkdir -p ~/.openclaw/credentials
printf '%s' '<OPENROUTER_API_KEY>' > ~/.openclaw/credentials/openrouter
printf '%s' '<ZAI_API_KEY>' > ~/.openclaw/credentials/zai
chmod 700 ~/.openclaw/credentials
chmod 600 ~/.openclaw/credentials/*
```

Do not commit this directory. Do not paste the script output into public issues if provider metadata could identify your account.

## Usage

```bash
check-quotas | jq .
```

Example output:

```json
{
  "openrouter": {
    "configured": true,
    "key_status": "checked"
  },
  "zai": {
    "configured": true,
    "key_status": "not_checked"
  },
  "checked_at": "2026-05-25T20:28:00Z"
}
```

## Parsing Output

Check whether a provider is configured:

```bash
check-quotas | jq -r '.openrouter.configured'
```

Use this in an agent prompt as a soft guardrail:

```text
Before running an expensive job, run `check-quotas`.
If a provider is not configured or reports pressure, use the configured fallback model.
Do not print API keys, raw account IDs, or full provider metadata.
```

The helper is intentionally conservative. If a provider does not expose a quota endpoint, the script should report that clearly instead of pretending it knows the remaining spend.

## Limits

- Provider quota APIs differ.
- Some providers expose spend only in their dashboard.
- OpenClaw config can route models, but provider dashboard limits are the real billing stop.
- If you use OpenClaw's secret store only, this script may correctly report a key as not visible.

## Adding Providers

Add a function that returns JSON and does not print the key:

```bash
check_provider() {
  local api_key
  api_key="$(read_secret "PROVIDER_API_KEY" "provider")"

  if [ -z "$api_key" ]; then
    jq -n '{configured:false}'
    return
  fi

  jq -n '{configured:true, key_status:"not_checked"}'
}
```

## OpenClaw Usage

Use this only as a local helper in prompts or scripts:

```text
Before running an expensive research job, run `check-quotas`.
If OpenRouter reports quota or spend pressure, use the configured fallback model.
Do not print API keys or full provider account metadata.
```

## Better Guardrails

- Set hard spend limits in each provider dashboard.
- Assign cheap models to monitoring and heartbeat jobs.
- Use explicit model IDs for unattended cron jobs.
- Review `agents.defaults.models` and `agents.defaults.model.fallbacks` after provider changes.

## Security

The script reads local secrets. Keep it local.

- Do not commit provider keys.
- Do not paste raw output into public issues if it contains account metadata.
- Keep `~/.openclaw/credentials` mode `700`.
- Keep token files mode `600`.
- Prefer provider dashboards for hard billing limits.

## Limitations

- Provider APIs change.
- Some providers have no useful quota endpoint.
- Subscription-style auth may report usage differently from API keys.
- This helper cannot stop spending by itself.
- A failed quota check should not automatically push work onto a more expensive fallback.
