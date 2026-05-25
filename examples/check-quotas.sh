#!/usr/bin/env bash
# Best-effort provider quota/key-status helper.
# This is optional. Provider dashboards remain the source of truth for spend limits.

set -euo pipefail

CREDENTIALS_DIR="${OPENCLAW_CREDENTIALS_DIR:-$HOME/.openclaw/credentials}"

read_secret() {
    local env_name="$1"
    local file_name="$2"
    local value="${!env_name:-}"

    if [ -n "$value" ]; then
        printf '%s' "$value"
        return
    fi

    if [ -f "$CREDENTIALS_DIR/$file_name" ]; then
        tr -d '\n' < "$CREDENTIALS_DIR/$file_name"
    fi
}

check_openrouter() {
    local api_key
    api_key="$(read_secret "OPENROUTER_API_KEY" "openrouter")"

    if [ -z "$api_key" ]; then
        jq -n '{configured:false}'
        return
    fi

    local response
    response="$(curl -s https://openrouter.ai/api/v1/key \
        -H "Authorization: Bearer $api_key" 2>/dev/null || true)"

    if [ -z "$response" ]; then
        jq -n '{configured:true, key_status:"not_checked"}'
        return
    fi

    printf '%s' "$response" | jq '{configured:true, key_status:"checked", data:(.data // .)}' 2>/dev/null \
        || jq -n '{configured:true, key_status:"check_failed"}'
}

check_zai() {
    local api_key
    api_key="$(read_secret "ZAI_API_KEY" "zai")"

    if [ -z "$api_key" ]; then
        jq -n '{configured:false}'
        return
    fi

    jq -n '{configured:true, key_status:"not_checked", note:"check provider dashboard for quota and spend limits"}'
}

openrouter_status="$(check_openrouter)"
zai_status="$(check_zai)"

jq -n \
    --argjson openrouter "$openrouter_status" \
    --argjson zai "$zai_status" \
    '{
        openrouter: $openrouter,
        zai: $zai,
        checked_at: (now | strftime("%Y-%m-%dT%H:%M:%SZ"))
    }'
