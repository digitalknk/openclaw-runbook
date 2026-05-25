# Model Delegation Troubleshooting

**Workarounds for common OpenClaw subagent delegation issues.**
**Ownership note:** Community-contributed example. Preserve the source context and avoid rewriting it as the runbook author's personal setup.

## Current-Version Note

This example documents delegation behavior observed in an older OpenClaw 2026.x setup. Before applying the workaround, verify the current model-routing behavior with `openclaw doctor`, `openclaw models list`, and a harmless subagent test.

## The Problem

When delegating to subagents, model names sometimes get corrupted:
- Full paths get stripped (e.g., `nvidia/moonshotai/kimi-k2-instruct` → fails)
- Provider prefixes disappear
- API calls work but subagent delegation fails

## Known Issues

### Bug #16010: Provider Prefix Stripping

**Symptom:** Subagent calls fail with 404, but direct API calls work.

**Root Cause:** OpenClaw strips provider prefix from model IDs in subagent context.

**Affected Models:** NVIDIA NIM models with path-style IDs

**Workaround:** Use aliases instead of full paths.

### Example Delegation Config

```markdown
## Delegation Matrix

| Task Type | Model | Provider | Notes |
|-----------|-------|----------|-------|
| CODE | minimax-m2.5:free | kilocode | Default - works |
| FALLBACK | openrouter/free | openrouter | When primary fails |
| RESEARCH | qwen3-235b-a22b | nvidia | When available |
| REASONING | kimik2thinking | nvidia | Complex logic |
```

### Using Aliases

Instead of:
```json
"model": "nvidia/moonshotai/kimi-k2-instruct-0905"
```

Use alias in models.json:
```json
{
  "models": {
    "kimik2": {
      "provider": "nvidia",
      "model": "moonshotai/kimi-k2-instruct-0905"
    }
  }
}
```

Then delegate with:
```markdown
Use model: kimik2
```

## Testing Delegation

```bash
# Test a model works for subagent delegation
## Example (pseudocode): Run model health check
# Note: No native "openclaw model test" command - use `openclaw models status` instead

# Or spawn a quick test subagent
sessions_spawn --model kimik2 --task "Say hi"
```

## Best Practices

1. **Use working defaults**: Test delegation before relying on it
2. **Have fallbacks**: Always have backup models configured
3. **Log delegation**: Track which models succeed/fail
4. **Keep it simple**: Cheaper models often work better for delegation

---

*Patterns discovered through debugging OpenClaw 2026.x delegation system*
