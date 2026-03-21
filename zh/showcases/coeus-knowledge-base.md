# Coeus 知识库 v2.0

**类别:** 日常自动化 / 个人知识管理
**示例模型:** 平衡版 (Sonnet/Gemini 2.5) 用于设置，任何模型用于日常使用
**更新时间:** 2026-02-16

> **使用方法:** 这是一个自托管的知识库，支持语义搜索。它在本地运行，数据存储在 SQLite 中，使用 sentence-transformers 生成嵌入向量。日常操作无需外部 API。

## 快速开始

### 1. 前置条件（先检查这些）

- [ ] Python 3.11+ 已安装
- [ ] SQLite 3.45.1+ 且启用了 FTS5
- [ ] vec0 扩展可在 `/usr/local/lib/sqlite3/vec0.so`
- [ ] 约 500MB 磁盘空间用于 Python 依赖

**验证 vec0:**
```bash
sqlite3 :memory: ".load /usr/local/lib/sqlite3/vec0.so" "SELECT 'vec0 OK';"
```

如果未安装 vec0，请先从 https://github.com/asg017/sqlite-vec 构建。

### 2. 运行设置脚本

```bash
mkdir -p ~/coeus && cd ~/coeus

# 创建 schema 文件
cat > schema.sql << 'SQL'
-- Coeus v2.0 Schema
CREATE TABLE blocks (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT,
    session_id TEXT REFERENCES capture_sessions(id)
);

CREATE VIRTUAL TABLE blocks_fts USING fts5(
    id, content, type,
    content='blocks', content_rowid='rowid'
);

CREATE TRIGGER blocks_ai AFTER INSERT ON blocks BEGIN
    INSERT INTO blocks_fts(id, content, type) VALUES (new.id, new.content, new.type);
END;

CREATE TRIGGER blocks_ad AFTER DELETE ON blocks BEGIN
    INSERT INTO blocks_fts(blocks_fts, id, content, type) VALUES('delete', old.id, old.content, old.type);
END;

CREATE TRIGGER blocks_au AFTER UPDATE ON blocks BEGIN
    INSERT INTO blocks_fts(blocks_fts, id, content, type) VALUES('delete', old.id, old.content, old.type);
    INSERT INTO blocks_fts(id, content, type) VALUES (new.id, new.content, new.type);
END;

CREATE VIRTUAL TABLE block_embeddings USING vec0(
    block_id TEXT PRIMARY KEY, embedding FLOAT[384]
);

CREATE TABLE block_summaries (
    block_id TEXT PRIMARY KEY REFERENCES blocks(id) ON DELETE CASCADE,
    one_line TEXT NOT NULL, generated_at TEXT NOT NULL
);

CREATE TABLE tags (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);
CREATE TABLE block_tags (
    block_id TEXT NOT NULL REFERENCES blocks(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (block_id, tag_id)
);

CREATE TABLE tag_aliases (
    canonical TEXT NOT NULL, alias TEXT NOT NULL UNIQUE,
    PRIMARY KEY (alias),
    FOREIGN KEY (canonical) REFERENCES tags(name) ON DELETE CASCADE
);

CREATE TABLE links (
    source_id TEXT NOT NULL REFERENCES blocks(id) ON DELETE CASCADE,
    target_id TEXT NOT NULL REFERENCES blocks(id) ON DELETE CASCADE,
    link_type TEXT DEFAULT 'auto' CHECK(link_type IN ('auto', 'manual', 'mentioned')),
    confidence REAL DEFAULT 1.0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (source_id, target_id)
);

CREATE TABLE people (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);
CREATE TABLE block_people (
    block_id TEXT NOT NULL REFERENCES blocks(id) ON DELETE CASCADE,
    person_id INTEGER NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    PRIMARY KEY (block_id, person_id)
);

CREATE TABLE projects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);
CREATE TABLE block_projects (
    block_id TEXT NOT NULL REFERENCES blocks(id) ON DELETE CASCADE,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    PRIMARY KEY (block_id, project_id)
);

CREATE TABLE revisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_id TEXT NOT NULL REFERENCES blocks(id) ON DELETE CASCADE,
    timestamp TEXT NOT NULL, reason TEXT, previous_content TEXT NOT NULL
);

CREATE TABLE capture_sessions (
    id TEXT PRIMARY KEY, started_at TEXT NOT NULL,
    ended_at TEXT, block_count INTEGER DEFAULT 0,
    mode TEXT DEFAULT 'explicit' CHECK(mode IN ('explicit', 'batch'))
);

CREATE TABLE capture_days (date TEXT PRIMARY KEY, block_count INTEGER NOT NULL DEFAULT 0);

CREATE INDEX idx_blocks_type ON blocks(type);
CREATE INDEX idx_blocks_created ON blocks(created_at);
CREATE INDEX idx_blocks_session ON blocks(session_id);
CREATE INDEX idx_tags_name ON tags(name);
CREATE INDEX idx_links_confidence ON links(confidence);

INSERT OR IGNORE INTO tags (name) VALUES
    ('kubernetes'), ('postgresql'), ('typescript'), ('javascript'), ('python'), ('golang');
INSERT OR IGNORE INTO tag_aliases (canonical, alias) VALUES
    ('kubernetes', 'k8s'), ('postgresql', 'postgres'), ('typescript', 'ts'),
    ('javascript', 'js'), ('python', 'py'), ('golang', 'go');
SQL

# 初始化数据库
sqlite3 coeus.db << 'INIT'
.load /usr/local/lib/sqlite3/vec0.so
.read schema.sql
INIT

# 创建状态文件
echo '{"capture_mode": false, "current_session_id": null, "last_capture_block_id": null}' > state.json
mkdir -p exports
```

### 3. 安装 Python 依赖

```bash
python3 -m venv venv
source venv/bin/activate

# CPU 专用 PyTorch（节省 2GB+ GPU 包）
pip install torch --index-url https://download.pytorch.org/whl/cpu

# 其他依赖
pip install transformers sentence-transformers --no-deps
```

### 4. 下载 coeus.py

从示例目录获取 `coeus.py` 或从源代码创建。将其放在 `~/coeus/coeus.py`。

### 5. 测试安装

```bash
source venv/bin/activate
python3 coeus.py capture "note: Testing Coeus setup"
python3 coeus.py stats
```

预期输出：
```
Total: 1 blocks
Types: {'research': 1}
Links: 0 | Sessions: 0 | Embeddings: 1
Semantic: Yes | Capture mode: Off
```

---

## 功能说明

**问题:** 你捕获想法、笔记和研究，但之后永远找不到它们。传统搜索需要精确关键词。没有结构，知识就变成了黑洞。

**解决方案:** 一个本地优先的知识库，能够：
- 使用**显式触发器**捕获（无意外记录）
- **自动标记和自动链接**内容（无声进行）
- 使用**语义搜索**查找概念相关的项目
- 缓存**单行摘要**，省省 60-70% 的 Token 用于摘要生成
- 跟踪**捕获会话**用于批量大脑转储

## 工作原理

### 捕获类型（自动检测）

| 类型 | 信号 | 生成嵌入 |
|------|---------|----------------|
| `research` | 事实、TIL、链接、概念 | 是 |
| `idea` | "如果...", 头脑风暴、推测 | 是 |
| `work_log` | 已发布、已修复、已部署、站会 | 否 |
| `journal` | 感受、反思、"我感到/认为" | 否 |

### 捕获触发器

**显式前缀:**
- `note:`, `capture:`, `log:`, `remember:`, `kb:`

**模板触发器:**
- `standup:` → work_log + 标记 #standup
- `meeting [name]:` → work_log + 提取 @attendees
- `idea [project]:` → idea + 链接 [[project]]

**批量模式:**
```
start capturing
note: First thought
note: Second thought
stop capturing
```

### 搜索策略

1. **FTS 优先**（零 Token）- 精确关键词匹配
2. **如果结果少于 3 条**，使用语义搜索（约 50 Token）
3. **返回摘要**（缓存的单行）而非完整内容
4. **合并并去重**结果

### 语义搜索示例

你捕获："Kubernetes 对可变工作负载使用水平 Pod 自动缩放"

之后你搜索："查找容器缩放"

结果:**通过语义相似性找到**，即使原始捕获中没有"容器"和"缩放"。

## CLI 用法

```bash
cd ~/coeus
source venv/bin/activate

# 捕获
python3 coeus.py capture "note: your content here"
python3 coeus.py capture "idea: something new"

# 搜索（FTS + 语义回退）
python3 coeus.py search "your query"

# 摘要（使用缓存的摘要）
python3 coeus.py brief today
python3 coeus.py brief week

# 统计
python3 coeus.py stats

# 批量捕获
python3 coeus.py start
python3 coeus.py capture "note: block 1"
python3 coeus.py capture "note: block 2"
python3 coeus.py stop
```

## 技能集成

要集成到 OpenClaw 作为技能，使用 `subprocess` 工具调用 coeus.py：

```python
import subprocess

def capture_block(content):
    result = subprocess.run(
        ["python3", "~/coeus/coeus.py", "capture", content],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def search_blocks(query):
    result = subprocess.run(
        ["python3", "~/coeus/coeus.py", "search", query],
        capture_output=True, text=True
    )
    return result.stdout
```

## 配置参考

### 标记别名

预配置的别名（捕获时自动解析）：

| 别名 | 规范名称 |
|-------|-----------|
| k8s | kubernetes |
| postgres | postgresql |
| ts | typescript |
| js | javascript |
| py | python |
| go | golang |

通过 SQL 添加更多：
```sql
INSERT INTO tag_aliases (canonical, alias) VALUES ('your-tag', 'your-alias');
```

### 数据库模式

**核心表:**
- `blocks` - 主内容存储
- `block_embeddings` - 384 维向量 (vec0)
- `block_summaries` - 缓存的单行摘要
- `tags` / `block_tags` - 标记系统
- `links` - 块关系（带置信度）
- `capture_sessions` - 批量捕获跟踪

### 存储需求

| 组件 | 大小 |
|-----------|------|
| 数据库 (~1000 块) | ~5-10MB |
| 嵌入（每块） | ~1.5KB |
| Python venv | ~400MB |
| 模型缓存 (~/.cache) | ~100MB |

## 故障排除

| 问题 | 可能原因 | 修复 |
|---------|--------------|-----|
| vec0 未找到 | 扩展未安装 | 从源代码构建 sqlite-vec |
| 嵌入未生成 | sentence-transformers 缺失 | 运行 install-deps.sh |
| 模型加载缓慢 | 首次运行，正在下载 | 等待下载 (~100MB) |
| "No module named X" | venv 未激活 | 运行 `source venv/bin/activate` |
| 搜索无返回结果 | FTS 语法错误 | 使用简单关键词，不用短语 |

## 经验教训

### 效果良好

- **仅显式触发器** - 防止意外捕获，保持数据库清洁
- **CPU 专用 PyTorch** - 省 2GB+ 磁盘空间，推理无需 GPU
- **仅写捕获** - 插入后无 SELECT，快速简单
- **缓存摘要** - 在摘要生成时节省 60-70% Token
- **优雅降级** - 无 vec0 也能工作（仅 FTS）

### 效果不佳

- GPU PyTorch - 嵌入不必要，体积巨大
- 自动捕获所有内容 - 产生噪声，降低信号
- 为摘要加载完整内容 - 在重复查询中浪费 Token

### 需要注意的陷阱

- vec0 扩展必须在创建表之前加载
- 嵌入仅为 research/idea 类型生成（设计如此）
- 模型在首次使用时下载 (~100MB) - 可能缓慢
- SQLite FTS5 有查询语法怪癖 - 简单关键词效果最佳

## 安全说明

- 所有数据本地存储在 SQLite 中
- 日常操作无需外部 API
- sentence-transformers 在首次运行时从 HuggingFace 下载模型
- 代码或配置中无秘钥

## 变体

**Web UI:** 添加 FastAPI 层以供浏览器访问（见在 b_1771199388_d307 中捕获的想法）

**同步:** 使用 Syncthing 或类似工具跨设备同步 `coeus.db`

**备份:** 数据库是单个文件 - 易于备份/恢复

## 相关

- [daily-brief](./daily-brief.md) - 将 Coeus 用作日常摘要的数据源
- [idea-pipeline](./idea-pipeline.md) - 夜间研究捕获的想法

## 更新日志

- **2026-02-16** - 初始 Coeus v2.0 展示（KNK）

---

**文件:**
- `coeus.py` - 主 Python 模块 (19KB)
- `schema.sql` - 数据库模式
- `install-deps.sh` - 依赖安装程序

**许可证:** MIT（与父项目匹配）
