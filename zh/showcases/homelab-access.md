# 家庭实验室访问

**类别:** 基础设施
**示例模型:** 平衡版 (Sonnet、Gemini Flash 等)
**更新时间:** 2026-02-09

> **使用方法:** 复制下面的 Telegram 机器人设置和安全规则。这让你可以通过 Telegram 在家庭实验室设备上运行 SSH 命令，危险操作需要确认提示。

## 快速开始

### 1. 前置条件

- [ ] 在所有设备上安装了 Tailscale（或 WireGuard、ZeroTier）
- [ ] SSH 密钥已配置且在设备上授权
- [ ] 通过 @BotFather 创建了 Telegram 机器人
- [ ] SSH 访问首先手动工作

### 2. 设置 Tailscale

在每个家庭实验室设备上：
```bash
# 安装
curl -fsSL https://tailscale.com/install.sh | sh

# 认证
tailscale up

# 获取 Tailscale IP
tailscale ip -4
# 记下此 IP 以供 SSH 配置使用
```

### 3. 配置 SSH

添加到 `~/.ssh/config`：
```
Host homelab-router
    HostName [TAILSCALE_IP]  # 例如 100.x.x.x
    User [USERNAME]
    IdentityFile ~/.ssh/homelab_key
    StrictHostKeyChecking accept-new

Host homelab-nas
    HostName [TAILSCALE_IP]
    User [USERNAME]
    IdentityFile ~/.ssh/homelab_key
```

手动测试：
```bash
ssh homelab-router uptime
```

### 4. 创建 Telegram 机器人

1. 在 Telegram 上给 @BotFather 发送消息
2. 发送 `/newbot`
3. 命名你的机器人（例如 "MyHomelabBot"）
4. 保存 API 令牌
5. 从 @userinfobot 获取你的聊天 ID

添加到 `~/.openclaw/credentials/`：
```
TELEGRAM_BOT_TOKEN=[YOUR_BOT_TOKEN]
TELEGRAM_CHAT_ID=[YOUR_CHAT_ID]
```

### 5. 复制此代理配置

添加到你的网关配置：

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

### 6. 测试

发送到你的 Telegram 机器人：
```
/homelab status router
```

应该返回 uptime 信息。

---

## 功能说明

**问题:** 需要远程访问家庭实验室设备。端口转发有风险，VPN 应用很笨重，原生应用不一致。

**解决方案:** Telegram 机器人 + Tailscale + SSH。你通过 Telegram 机器人发送命令。安全命令立即执行。危险命令需要"YES"确认。一切都通过 Tailscale 进行（加密，无端口转发）。

## 安全模型

### 三层命令系统

**第 1 层 - 允许（立即执行）:**
```bash
uptime                    # 确定
df -h                     # 确定
free -m                   # 确定
systemctl status pihole   # 确定
ping google.com           # 确定
ls /etc/nginx             # 确定
cat /etc/hosts            # 确定
```

**第 2 层 - 确认（先询问）:**
```bash
systemctl restart pihole  # "确认：重启 pihole？回复 YES"
apt install htop          # "确认：安装 htop？回复 YES"
echo "config" > file     # "确认：写入文件？回复 YES"
reboot                    # "确认：重启？回复 YES"
```

**第 3 层 - 禁止（总是拒绝）:**
```bash
rm -rf /                  # 被拒绝
dd if=/dev/zero           # 被拒绝
passwd                    # 被拒绝
iptables -F               # 被拒绝
```

## 命令示例

**检查状态:**
```
你: /homelab status router
机器人: uptime: 45 days, load: 0.12, disk: 67%
```

**检查服务:**
```
你: /homelab systemctl status pihole on nas
机器人: pihole.service - Pi-hole DNS
       Active: active (running) since Mon 2026-02-10
```

**重启（需确认）:**
```
你: /homelab restart pihole on nas
机器人: 确认：systemctl restart pihole on homelab-nas？
       回复 YES 以执行。
你: YES
机器人: 执行中... 完成。Pi-hole 已重启。
```

## 高级：多用户支持

允许多个授权用户：
```yaml
system: |
  授权用户：[USER1], [USER2]

  对于破坏性命令（第 2 层）：
  - 用户 1 可以批准自己的命令
  - 或要求用户 2 的批准（双人规则）
```

## 故障排除

| 问题 | 原因 | 解决方案 |
|---------|-------|----------|
| "权限被拒绝" | SSH 密钥问题 | 验证密钥在设备上 `~/.ssh/authorized_keys` 中 |
| "主机未找到" | Tailscale 未连接 | 在设备上运行 `tailscale up` |
| 无响应 | 机器人未接收消息 | 检查 webhook/轮询设置 |
| 命令超时 | 长时间运行的命令 | 增加超时或在后台运行 |

## 安全检查清单

- [ ] Tailscale ACL 限制哪些设备可以通话
- [ ] 仅基于 SSH 密钥的认证（无密码）
- [ ] 为家庭实验室使用单独的 SSH 密钥（非个人密钥）
- [ ] 破坏性命令需要确认
- [ ] 所有命令记录到审计文件
- [ ] 速率限制（最多 10 个命令/小时）

## 变体

**Discord 替代 Telegram:**
```yaml
system: |
  接受来自 Discord 用户 [DISCORD_USER_ID] 的命令
  ...相同规则...
```

**Slack 集成:**
使用 Slack 机器人与传入 webhook。

**语音命令:**
添加语音转文本层："嘿，助手，重启 NAS"

**Web 仪表板:**
简单的 Web UI，带有常见命令的大按钮。

## 相关

- [daily-brief](daily-brief.md) - 可以包含家庭实验室状态
- [tech-discoveries](tech-discoveries.md) - 查找新的家庭实验室工具

## 更新日志

- **2026-02-09** - 初始版本，基于 Telegram
- **2026-02-10** - 添加确认工作流，已泛化
