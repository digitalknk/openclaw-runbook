# 检查配额脚本

简单脚本来检查多个提供商之间的 API 配额状态。

## 安装

1. 将 `check-quotas.sh` 复制到您的本地 bin 目录：

```bash
cp check-quotas.sh ~/.local/bin/check-quotas
chmod +x ~/.local/bin/check-quotas
```

2. 验证 `~/.local/bin` 在您的 PATH 中：

```bash
echo $PATH | grep -q "$HOME/.local/bin" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

## 配置

该脚本默认在 `~/.openclaw/credentials/` 中查找 API 密钥。

**使用环境变量覆盖：**

```bash
export OPENCLAW_CREDENTIALS_DIR="/path/to/your/credentials"
export CLAUDE_KEYCHAIN_ITEM="Your-Keychain-Item"
```

**预期的凭证文件：**

每个文件应仅包含**原始 API 密钥**（无变量名、无引号、无换行符）：

```bash
# 正确格式 - 仅原始令牌：
echo "sk-ant-api03-xxxxxxxxxxxx" > ~/.openclaw/credentials/anthropic

# 错误格式 - 不要使用：
echo "ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxx" > ~/.openclaw/credentials/anthropic
```

**脚本查找的文件：**
- `$CREDENTIALS_DIR/synthetic` - Synthetic API 密钥（仅原始令牌）
- `$CREDENTIALS_DIR/openrouter` - OpenRouter API 密钥（仅原始令牌）
- `$CREDENTIALS_DIR/anthropic` - Anthropic API 密钥（仅原始令牌）

**macOS Keychain（Claude Code）：**
- 该脚本检查 macOS Keychain 中的 Claude Code OAuth 凭证
- 仅在装有 Claude Code 的 macOS 上工作

## 使用

从任何地方运行：

```bash
check-quotas
```

**输出格式（JSON）：**

```json
{
  "claude_code": {
    "usage": {...},
    "limit": {...}
  },
  "synthetic": {
    "credits_remaining": 1000
  },
  "openrouter": {
    "usage": 45.23,
    "limit": 100.00
  },
  "anthropic_api": "valid",
  "checked_at": "2026-02-09T20:28:00Z"
}
```

## 解析输出

**检查提供商是否超过 90% 配额：**

```bash
check-quotas | jq '.openrouter | (.usage / .limit) > 0.9'
```

**获取剩余的 Synthetic 信用：**

```bash
check-quotas | jq -r '.synthetic.credits_remaining'
```

**为人类输出美化打印：**

```bash
check-quotas | jq .
```

## 添加新提供商

要添加新提供商，创建遵循此模式的函数：

```bash
check_yourprovider() {
    local api_key=$(cat "$CREDENTIALS_DIR/yourprovider" 2>/dev/null || echo "")

    if [ -z "$api_key" ]; then
        echo "null"
        return
    fi

    curl -s https://api.yourprovider.com/quota \
        -H "Authorization: Bearer $api_key" 2>/dev/null || echo "null"
}
```

然后将其添加到最终的 jq 输出。

## 与 OpenClaw 集成

在代理提示词或技能中使用：

```bash
# 在生成昂贵代理前检查配额
QUOTAS=$(check-quotas)
OPENROUTER_USAGE=$(echo $QUOTAS | jq -r '.openrouter.usage // 0')

if [ "$OPENROUTER_USAGE" -gt 90 ]; then
    echo "OpenRouter quota high, using fallback"
fi
```

## 要求

- `bash`
- `curl`
- `jq`
- `security`（仅 macOS，用于 Keychain 访问）

## 限制

- Claude Code 检查仅在 macOS 上工作
- Anthropic API 没有公共配额端点，所以我们只是验证密钥有效
- 速率限制可能适用于配额检查 API 本身

## 安全

该脚本从文件中读取 API 密钥。每个文件应仅包含**原始令牌**，无变量名或格式。

**创建凭证文件：**

```bash
# 创建凭证目录
mkdir -p ~/.openclaw/credentials

# 添加您的 API 密钥（仅原始令牌，无引号）
echo "your-api-key-here" > ~/.openclaw/credentials/openrouter
echo "your-api-key-here" > ~/.openclaw/credentials/synthetic
echo "your-api-key-here" > ~/.openclaw/credentials/anthropic

# 设置正确的权限
chmod 700 ~/.openclaw/credentials
chmod 600 ~/.openclaw/credentials/*
```

**文件格式：**
- ✅ 正确：`sk-ant-api03-xxxxx`（仅原始令牌）
- ❌ 错误：`ANTHROPIC_API_KEY=sk-ant-api03-xxxxx`（无 ENV 格式）
- ❌ 错误：`"sk-ant-api03-xxxxx"`（无引号）

永远不要将 API 密钥提交到 git 或公开分享输出。
