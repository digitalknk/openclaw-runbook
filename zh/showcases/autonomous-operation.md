# 自主运行模式

**让 OpenClaw 能够以扩展时间段自主运行，并具有自我修复能力。**

## 问题

OpenClaw 会话可能会崩溃或卡住。长期运行的自主操作需要：
- 健康监控
- 自动恢复
- 状态持久性（检查点）

## 解决方案

### 架构

```
┌─────────────────────────────────────────────────────────┐
│                   主会话（协调器）                        │
│  - 精简：最多 2 个工具调用（仅生成/发送）                   │
│  - 生成监控子代理                                        │
└──────────────────────┬──────────────────────────────────┘
                       │ 生成
                       ▼
┌─────────────────────────────────────────────────────────┐
│              监控子代理（每 5 分钟）                       │
│  - 检查网关健康状态                                      │
│  - 检查进程状态                                          │
│  - 记录到 autonomous-op.log                            │
│  - 发现问题时发出警报                                    │
└──────────────────────┬──────────────────────────────────┘
                       │ cron（每 30 分钟）
                       ▼
┌─────────────────────────────────────────────────────────┐
│              自我检查脚本（cron）                          │
│  - 验证网关响应                                          │
│  - 检查卡住的进程                                        │
│  - 必要时自动重启                                        │
└─────────────────────────────────────────────────────────┘
```

### 组件

#### 1. 自我检查脚本

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

#### 2. 监控子代理

```yaml
# 从主会话生成
name: monitor-health
schedule: every 5 minutes
model: cheap (minimax-m2.5:free)
tasks:
  - Check gateway: curl -s http://127.0.0.1:18789/health
  - Check processes: ps aux | grep openclaw
  - Log results
  - Alert if issues
```
> **注意:** 这个 YAML 是用于说明的伪代码。OpenClaw 使用 JSON 进行配置文件。YAML 显示预期的结构；在你的实际配置中使用 JSON 实现。

#### 3. Cron 恢复

```bash
# 添加到 cron：crontab -e
*/30 * * * * ~/.openclaw/workspace/scripts/self-check.sh >> /var/log/openclaw-selfcheck.log 2>&1
```

### 参考：精简主会话规则

保持主会话最小化：

```markdown
## 规则：精简主会话

主会话应仅：
1. 生成子代理
2. 向子代理发送消息

所有实际工作都在隔离的子代理会话中进行。

这防止了上下文切换并保持协调器快速。
```

## 优势

- **韧性**: 自动从崩溃中恢复
- **可见性**: 日志跟踪所有健康检查
- **成本**: 使用便宜模型进行监控
- **自主性**: 在无需人工干预的情况下运行 7+ 小时

## 配置

```json
{
  "subagents": {
    "maxConcurrent": 4
  },
  "model": "minimax-m2.5:free"
}
```

## 使用

1. 将自我检查脚本部署到 cron
2. 在会话启动时生成监控子代理
3. 保持主会话精简
4. 通过 `tail -f memory/autonomous-op.log` 监控

---

*模式通过与 OpenClaw 2026.x 的实践经验开发*
