# Claworc - OpenClaw 编排器

**来源:** https://github.com/gluk-w/claworc
**日期:** 2026-03-01

## 功能

从单个 Web 仪表板运行多个 OpenClaw 实例。

## 主要功能

- **多实例管理** - 一个仪表板管理所有实例
- **容器隔离** - 每个实例在其自己的容器中
- **SSH 安全** - 基于密钥的身份验证、加密 API 密钥
- **访问控制** - 管理员/用户角色、生物识别身份验证
- **实时浏览器** - 实时观察代理工作

## 架构

```
Browser → Control Plane → [SSH tunnel] → Agent Container
                                    → :3000 (VNC)
                                    → :18789 (Gateway)
```

## 安全层

1. 仅 SSH 密钥身份验证（无密码）
2. 密钥轮换支持
3. 无直接代理访问
4. 每实例 IP 白名单
5. 速率限制
6. 审计日志
7. 静态加密 API 密钥

## 用例

- 团队部署（每个人都有自己的代理）
- 数据分析实例
- IT 支持机器人
- 隔离的敏感操作

## 与我的设置的相关性

- 可用于更好的安全隔离
- 未来：多用户访问
- 与运行手册安全模式一致

---

*运行在树莓派上的替代方案*

---

## 设置步骤

### 前置条件

- 在主机上安装了 Docker
- 用于远程访问的 SSH 密钥对
- 每个 OpenClaw 实例至少 2GB RAM
- 已安装 Git

### 安装

```bash
# 克隆 Claworc 仓库
git clone https://github.com/gluk-w/claworc.git
cd claworc

# 复制示例配置
cp config.example.yaml config.yaml

# 用你的设置编辑配置
nano config.yaml
```

### 配置

```yaml
# config.yaml
instances:
  - name: primary
    container: openclaw-primary
    port: 18789
    ssh_port: 2222
    vnc_port: 3000

  - name: analysis
    container: openclaw-analysis
    port: 18790
    ssh_port: 2223
    vnc_port: 3001

security:
  ssh_key_path: ~/.ssh/id_rsa
  api_key_encryption: enabled
  rate_limit: 100/hour

access_control:
  admin_users:
    - your-email@example.com
  require_biometric: false
```

### 运行

```bash
# 启动所有实例
docker-compose up -d

# 访问仪表板
# 在浏览器中打开 http://localhost:8080

# 查看日志
docker-compose logs -f
```

### 验证设置

```bash
# 检查所有容器运行
docker ps | grep openclaw

# 测试 SSH 访问实例
ssh -p 2222 user@localhost

# 检查网关健康状态
curl http://localhost:18789/health
```

### 维护

```bash
# 停止所有实例
docker-compose down

# 更新到最新版本
git pull
docker-compose pull
docker-compose up -d
```

### 卸载

```bash
# 停止并移除容器
docker-compose down -v

# 移除仓库
cd ..
rm -rf claworc
```
