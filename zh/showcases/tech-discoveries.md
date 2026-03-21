# 技术发现

**分类:** 研究
**示例模型:** 均衡等级 (Sonnet, Gemini Flash 等)
**更新时间:** 2026-02-09

> **使用方法:** 复制下面的定时任务和提示词。将 `[占位符]` 替换为你的值。每周策展的技术新闻交付到你的首选渠道。

## 快速开始

### 1. 前置条件

- [ ] 新闻通讯订阅 (或以 RSS 源作为替代)
- [ ] 电子邮件访问 (IMAP/SMTP) 或 RSS 阅读器
- [ ] Web 搜索工具已配置 (Brave, Serper API 密钥)
- [ ] 交付渠道已配置 (Telegram, Discord, 电子邮件或 Slack)

### 2. 复制此定时任务

粘贴到你的网关配置的 `cron.jobs` 部分:

```json
{
  "name": "tech-discoveries",
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * 0",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Generate tech discoveries for [YOUR_INTERESTS]. Check: 1) Newsletter emails at [YOUR_EMAIL], 2) GitHub Trending for [YOUR_LANGUAGES], 3) Hacker News top stories, 4) Reddit [YOUR_SUBREDDITS]. Curate 5-10 items. For each: title, one-sentence summary, why relevant, link. Group by category. Deliver to [YOUR_CHANNEL]. Skip: crypto, generic AI hype."
  },
  "sessionTarget": "isolated"
}
```

**替换:**
- `[YOUR_INTERESTS]` - 你的关注领域 (例如, "SRE, 家庭实验室, 3D 打印")
- `[YOUR_EMAIL]` - 新闻通讯到达的位置
- `[YOUR_LANGUAGES]` - GitHub 上要跟踪的语言 (例如, "Go, Python, Rust")
- `[YOUR_SUBREDDITS]` - 要检查的社区 (例如, "r/homelab, r/selfhosted")
- `[YOUR_CHANNEL]` - 交付位置 (Telegram, Discord 等)

### 3. 配置工具

```yaml
tools:
  email: {}       # IMAP/SMTP 访问
  web_search: {}  # Brave, Serper 等
  browser: {}     # 如果需要 HN, Reddit
  message: {}     # Telegram, Discord, 电子邮件
```

### 4. 测试

```bash
openclaw cron run tech-discoveries
```

---

## 功能说明

**问题:** 在多个来源中跟踪技术新闻很耗时。容易错过相关开发。

**解决方案:** 每周自动扫描。每周日上午 8 点 UTC，从新闻通讯、GitHub、HN、Reddit 聚合发现。策展 5-10 个相关项，交付到你的渠道。

## 完整提示词(详细)

```
Generate weekly tech discoveries for me.

**My interests:** [YOUR_INTERESTS]

**Sources to check:**
1. NEWSLETTERS: Check emails at [YOUR_EMAIL]
   - Look for: [NEWSLETTER_1], [NEWSLETTER_2], etc.
2. GITHUB: Trending repos for [YOUR_LANGUAGES]
3. HACKER NEWS: Top stories from past week
4. REDDIT: [YOUR_SUBREDDITS]
5. PRODUCT HUNT: Top launches (optional)

**For each discovery:**
- Title and one-sentence summary
- Why it's relevant to my interests
- Link (Discord: wrap in <> to suppress embeds; Telegram: standard)
- Category tag

**Format:**
- 5-10 items max (quality over quantity)
- Group by category: SRE/DevOps, Homelab, Hardware, etc.
- Brief intro: "Tech Discoveries - [DATE]"
- Brief outro: "Happy exploring!"

Deliver to [YOUR_CHANNEL].

Skip: Enterprise vendor press releases, cryptocurrency, generic AI hype.
```

## 新闻通讯选项

**推荐新闻通讯:**
- **DevOps/SRE:** SRE Weekly, DevOps Weekly, KubeWeekly
- **基础设施:** Last Week in AWS, Console.dev
- **制造商/硬件:** Hackaday, Adafruit, ServeTheHome
- **通用技术:** Changelog News, DevOps'ish, tldr;

**订阅方式:**
- 专用电子邮件 (例如, newsletters@yourdomain.com)
- 过滤器自动标记
- 转发到你的代理的电子邮件

## GitHub Trending

**要跟踪的语言:**
```
Go, Python, Rust, TypeScript
```

**时间框架:** 每周 (过去 7 天)

**注意:** GitHub Trending 经常包括笑话仓库。人类判断有帮助。

## Reddit 社区

**推荐的子版块:**
- r/homelab - 家庭服务器项目
- r/selfhosted - 自托管软件
- r/homelabsales - 硬件交易
- r/buildapcsales - PC 组件交易
- r/MeshNetworking - 网状网络
- r/selfhosted - 云服务的替代方案

**提示:** 使用 RSS 源 (reddit.com/r/[sub]/rss) 而不是抓取。

## 交付格式

**Telegram:**
```
**Tech Discoveries - Feb 10, 2026**

**SRE / DevOps**
- Tool X released - New monitoring solution with built-in alerting
- Article Y - Deep dive into Kubernetes networking

**Homelab**
- Project Z - Open source NAS software
```

**Discord:**
```
**Tech Discoveries - Feb 10, 2026**

**SRE / DevOps**
- Tool X released - New monitoring solution
  <https://github.com/...>
```

**电子邮件:**
主题: "Tech Discoveries - Feb 10, 2026"
正文: 格式化的 HTML 或 markdown

## 故障排除

| 问题 | 原因 | 解决方案 |
|---------|-------|----------|
| 项目太多 | 过滤不够激进 | 在提示词中添加 "最多 5 项" |
| 不相关的链接 | 子版块/来源错误 | 策展你的源列表 |
| 新闻通讯链接断开 | 跟踪 URL | 在提示词中添加 "提取真实 URL" |
| Reddit 限流 | 抓取太快 | 改用 RSS 源 |

## 经验教训

### 有效的方法

- **周日早上时间** - 适合周末阅读
- **聊天交付** (Telegram, Discord) - 易于扫描和点击
- **策展胜于聚合** - 5-10 个优质项胜过 50 个随机链接

### 无效的方法

- **自动点击新闻通讯链接** - 许多使用会断裂的跟踪 URL
- **包括一切** - 没有过滤，变成噪音
- **每日计划** - 太频繁；每周是正确的频率

### 注意事项

- **链接老化** - 一些新闻通讯链接过期
- **Reddit 限流** - 尽可能使用 RSS
- **GitHub Trending** - 经常包括笑话仓库

## 变体

**突发新闻警报:**
```json
{
  "name": "breaking-tech",
  "schedule": { "kind": "every", "everyMs": 3600000 },  // 每小时
  "payload": {
    "message": "Check for major releases (Kubernetes, Docker, etc.). If found, alert immediately."
  }
}
```

**稍后阅读:**
在提示词中添加: "为我应该调查的项创建 Todoist 任务。"

**摘要电子邮件:**
将交付从聊天改为电子邮件以进行正式阅读。

## 相关链接

- [daily-brief](daily-brief.md) - 可以包括顶部发现
- [idea-pipeline](idea-pipeline.md) - 发现的工具形成良好研究话题

## 更新日志

- **2026-02-09** - 初始版本，周日上午 8 点
- **2026-02-10** - 为公开分享进行了推广
