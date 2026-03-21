# 模型委派故障排除

**OpenClaw 子代理委派常见问题的解决方案。**

## 问题所在

委派给子代理时，模型名称有时会被破坏：
- 完整路径被删除（例如，`nvidia/moonshotai/kimi-k2-instruct` → 失败）
- 提供商前缀消失
- API 调用有效，但子代理委派失败

## 已知问题

### Bug #16010：提供商前缀删除

**症状：** 子代理调用失败并返回 404，但直接 API 调用有效。

**根本原因：** OpenClaw 在子代理上下文中删除了模型 ID 的提供商前缀。

**受影响的模型：** 具有路径风格 ID 的 NVIDIA NIM 模型

**解决方案：** 使用别名而不是完整路径。

### 示例委派配置

```markdown
## 委派矩阵

| 任务类型 | 模型 | 提供商 | 备注 |
|---------|------|--------|------|
| CODE | minimax-m2.5:free | kilocode | 默认值 - 有效 |
| FALLBACK | openrouter/free | openrouter | 主要模型失败时 |
| RESEARCH | qwen3-235b-a22b | nvidia | 可用时 |
| REASONING | kimik2thinking | nvidia | 复杂逻辑 |
```

### 使用别名

不要使用：
```json
"model": "nvidia/moonshotai/kimi-k2-instruct-0905"
```

而是在 models.json 中使用别名：
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

然后使用以下方式委派：
```markdown
使用模型：kimik2
```

## 测试委派

```bash
# 测试模型是否适合子代理委派
## 示例（伪代码）：运行模型健康检查
# 注：没有原生的 "openclaw model test" 命令 - 改用 `openclaw models status`

# 或生成快速测试子代理
sessions_spawn --model kimik2 --task "Say hi"
```

## 最佳实践

1. **使用工作默认值**：在依赖委派之前测试委派
2. **准备回退方案**：始终配置备用模型
3. **记录委派**：跟踪哪些模型成功/失败
4. **保持简单**：便宜的模型通常对委派的效果更好

---

*通过调试 OpenClaw 2026.x 委派系统发现的模式*
