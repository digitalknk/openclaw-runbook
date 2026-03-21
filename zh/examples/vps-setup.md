# VPS 设置指南

本指南涵盖在 VPS 上设置 OpenClaw 并进行安全加固。

## 硬件要求

你不需要大型机器。Hetzner CX23 或等效的机器就足够了：
- 2 个 vCPU
- 4 GB RAM
- 40 GB 磁盘

## 使用 Tailscale 进行网络安全

**关键：按此顺序完全遵循以避免锁定。**

### 第 1 步：在本地机器上安装 Tailscale

```bash
# 在你的本地机器上（Mac/Linux/Windows）
# 访问：https://tailscale.com/download
# 安装并验证
```

### 第 2 步：在 VPS 上安装 Tailscale

```bash
# 首先正常 SSH 到 VPS
ssh user@your-vps-ip

# 安装 Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --ssh=true
```

`--ssh=true` 标志启用通过 Tailscale 的 SSH。

### 第 3 步：获取 VPS Tailscale IP

```bash
# 在 VPS 上，获取你的 Tailscale IP
tailscale ip -4
# 示例输出：100.64.1.2
```

### 第 4 步：通过 Tailscale 测试 SSH

**关键：不要跳过此步骤。**

从你的本地机器，通过 Tailscale 测试 SSH：

```bash
# 使用 Tailscale IP，而不是你的公共 IP
ssh user@100.64.1.2
```

**如果有效，你已准备好阻止公共 SSH。**
**如果失败，不要继续。首先调试 Tailscale。**

### 第 5 步：阻止公共访问（仅在验证后）

现在 Tailscale SSH 已验证，在防火墙处阻止端口 22：

```bash
# Hetzner 防火墙（通过 Web UI）
# 1. 创建新防火墙规则
# 2. 阻止：端口 22 的所有入站流量
# 3. 保持 Tailscale 流量不受限制（100.64.0.0/10）
```

### 第 6 步：验证锁定防止

再测试一次：

```bash
# 这应该有效（Tailscale）
ssh user@100.64.1.2

# 这应该失败/超时（公共 IP 已阻止）
ssh user@your-public-vps-ip
```

**如果 Tailscale SSH 此时失败，你仍然可以通过提供商的 Web 控制台访问来修复它。**

### 安全网

大多数 VPS 提供商（Hetzner、DigitalOcean、Linode）提供基于 Web 的控制台访问作为最后手段，以防你锁定自己。在进行防火墙更改之前找到这个。

## OpenClaw 安装

安装 OpenClaw 后，在做任何其他事情之前运行这些命令：

```bash
# 验证配置并自动修复常见问题
openclaw doctor --fix

# 运行深度安全扫描
openclaw security audit --deep
```

安全审计应该返回零关键问题。几个警告是正常的：
- `gateway.trusted_proxies_missing`（如果仅本地主机可以）
- `fs.credentials_dir.perms_readable`（使用 chmod 修复）

## 文件权限

锁定配置目录：

```bash
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/openclaw.json
chmod 700 ~/.openclaw/credentials
```

这防止系统上的其他用户读取你的配置或 API 密钥。

## 网关绑定

验证网关绑定到本地主机而不是暴露到公共互联网：

```bash
netstat -an | grep 18789 | grep LISTEN
# 你想看到：127.0.0.1:18789
# 你不想看到：0.0.0.0:18789
```

如果你看到 `0.0.0.0`，你的网关正在所有接口上监听，任何可以到达该端口的人都可以与你的代理通话。

**在配置中修复：**

```json
"gateway": {
  "bind": "loopback"
}
```

然后重启：

```bash
openclaw gateway restart
```

## 加固配置

一旦基础被锁定，配置这些设置：

### 带有编辑的日志记录

```json
"logging": {
  "redactSensitive": "tools"
}
```

选项：
- `"off"` - 无编辑（危险）
- `"tools"` - 编辑工具输出（推荐）
- `"all"` - 激进编辑（更难调试）

### 工具策略

限制代理可以使用哪些工具：

```json
"tools": {
  "profile": "minimal",
  "deny": ["exec"],
  "allow": ["web_search", "web_fetch", "read"]
}
```

**工具配置文件：**
- `minimal` - 仅 `session_status`（最严格）
- `coding` - 文件系统、运行时、会话、内存
- `messaging` - 仅消息工具
- `full` - 无限制（默认）

这防止代理在没有明确许可的情况下执行任意命令。

### 沙箱模式（可选）

如果你想要容器化执行（需要 Docker）：

```json
"agents": {
  "defaults": {
    "sandbox": {
      "enabled": true,
      "image": "openclaw-sandbox"
    }
  }
}
```

在共享 VPS 上运行并想要代理工作隔离时很有用。

## Git 跟踪你的配置

Git 跟踪 OpenClaw 配置目录以实现回滚能力：

```bash
cd ~/.openclaw && git init
printf 'agents/*/sessions/\nagents/*/agent/*.jsonl\n*.log\n' > .gitignore
git add .gitignore openclaw.json
git commit -m "config: baseline"
```

之后，在任何重大变化之前和之后提交：

```bash
# 在进行更改前
git commit -am "config: before model update"

# 进行你的更改
vim openclaw.json

# 测试并提交
openclaw doctor --fix
git commit -am "config: switched to Gemini 3 Flash"
```

当午夜某事坏掉时，`git diff` 和 `git checkout` 比试图记住你改了什么要快得多。

## 验证工作流

在任何配置更改后：

1. **验证：**
   ```bash
   openclaw doctor --fix
   ```

2. **安全审计：**
   ```bash
   openclaw security audit --deep
   ```

3. **测试：**
   ```bash
   openclaw status
   # 发送测试消息
   ```

4. **提交：**
   ```bash
   git commit -am "config: description of change"
   ```

这个工作流快速捕捉错误并给你回滚能力。

## 系统监控

设置基本监控：

```bash
# 检查 OpenClaw 状态
openclaw status

# 检查日志中的错误
tail -100 ~/.openclaw/gateway.log | grep -i error

# 检查系统资源
htop
```

考虑添加 cron 任务或心跳检查来监控失败的任务和错误日志（见 `heartbeat-example.md`）。

## 备份策略

要备份什么：
- `~/.openclaw/openclaw.json`（配置）
- `~/.openclaw/credentials/`（API 密钥）
- `~/.openclaw/workspace/`（你的工作）

不要备份什么：
- 会话日志（重新创建）
- 代理状态（重新生成）
- 日志文件（临时）

### 备份脚本

创建 `~/bin/backup-openclaw.sh`：

```bash
#!/bin/bash
# OpenClaw backup script
BACKUP_DIR=~/backups
DATE=$(date +%Y-%m-%d)

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create backup
tar czf $BACKUP_DIR/openclaw-$DATE.tar.gz \
  ~/.openclaw/openclaw.json \
  ~/.openclaw/credentials \
  ~/.openclaw/workspace

# Keep only last 7 days of backups
find $BACKUP_DIR -name "openclaw-*.tar.gz" -mtime +7 -delete

# Log completion
echo "$(date): Backup completed - openclaw-$DATE.tar.gz" >> $BACKUP_DIR/backup.log
```

使其可执行：

```bash
chmod +x ~/bin/backup-openclaw.sh
```

### 使用 Cron 计划

编辑你的 crontab：

```bash
crontab -e
```

添加以下日程表之一：

```bash
# 每天凌晨 3 点
0 3 * * * ~/bin/backup-openclaw.sh

# 每 6 小时
0 */6 * * * ~/bin/backup-openclaw.sh

# 每周日凌晨 2 点
0 2 * * 0 ~/bin/backup-openclaw.sh
```

**验证 cron 任务已计划：**

```bash
crontab -l
```

**检查备份日志：**

```bash
cat ~/backups/backup.log
```

## 服务管理

OpenClaw 向导在安装期间在 Linux 上自动设置 systemd 用户服务（或在 macOS 上设置 launchd）。无需手动配置。

**检查服务状态：**
```bash
openclaw status
# 或
systemctl --user status openclaw
```

**管理服务：**
```bash
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
```

向导会自动处理服务安装。仅对于自定义配置或非向导安装才需要手动 systemd 设置。

## Tailscale 故障排除

**Tailscale SSH 不工作：**

```bash
# 在 VPS 上，检查 Tailscale 状态
sudo tailscale status

# 检查 SSH 是否启用
sudo tailscale status | grep ssh

# 如果禁用，重新启用
sudo tailscale up --ssh=true
```

**找不到 Tailscale IP：**

```bash
# 在 VPS 上
tailscale ip -4    # IPv4
tailscale ip -6    # IPv6
hostname           # Tailscale 网络上的机器名
```

**防火墙更改后被锁定：**

1. 使用提供商的 Web 控制台（Hetzner 控制台、DigitalOcean Droplet 控制台）
2. 通过 Web 界面登录
3. 修复防火墙规则或重新启用 Tailscale
4. 在关闭控制台之前测试 Tailscale SSH

## OpenClaw 故障排除

**网关不会启动：**
```bash
openclaw doctor --fix
openclaw gateway stop
openclaw gateway start
```

**配置错误：**
```bash
openclaw doctor --fix
# 阅读输出，修复问题
```

**权限被拒绝：**
```bash
ls -la ~/.openclaw
# 检查所有权和权限
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/openclaw.json
```

**端口已在使用中：**
```bash
lsof -i :18789
# 终止进程或在配置中更改端口
```

## 安全检查清单

在生产环境中运行 OpenClaw 之前：

- [ ] 文件权限被锁定（700/600）
- [ ] 网关仅绑定到本地主机
- [ ] `openclaw security audit --deep` 返回零关键问题
- [ ] Tailscale 已配置，防火墙已阻止 SSH
- [ ] 日志编辑已启用
- [ ] 工具策略已配置
- [ ] 配置已 git 跟踪
- [ ] 备份策略已制定

## 成本优化

在 VPS 上运行不意味着昂贵：

- Hetzner CX23：约 $5/月
- 便宜的模型用于心跳（GPT-5 nano）
- 跨提供商回退以避免配额耗尽
- 并发限制以防止失控成本

参见 `agent-prompts.md` 了解模型配置策略。

## 资源

- [Security Patterns](security-patterns.md) - 提示注入防御和安全规则
- [Agent Prompts](agent-prompts.md) - 模型配置和回退链
- [Heartbeat Example](heartbeat-example.md) - 轮换检查以进行监控
