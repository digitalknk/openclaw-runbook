# Coeus Knowledge Base v2.0

**Category:** Daily Automation / Personal Knowledge Management  
**Example Model:** Balanced (Sonnet/Gemini 2.5) for setup, any model for daily use  
**Updated:** 2026-02-16

> **HOW TO USE THIS:** This is a self-hosted knowledge base with semantic search. It runs locally on your machine, stores data in SQLite, and uses sentence-transformers for embeddings. No external APIs needed for daily operation.

## Quick Start

### 1. Prerequisites (check these first)

- [ ] Python 3.11+ installed
- [ ] SQLite 3.45.1+ with FTS5 enabled
- [ ] vec0 extension available at `/usr/local/lib/sqlite3/vec0.so`
- [ ] ~500MB disk space for Python dependencies

**Verify vec0:**
```bash
sqlite3 :memory: ".load /usr/local/lib/sqlite3/vec0.so" "SELECT 'vec0 OK';"
```

If vec0 is not installed, build it from https://github.com/asg017/sqlite-vec first.

### 2. Run Setup Script

```bash
mkdir -p ~/coeus && cd ~/coeus

# Create schema file
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

# Initialize database
sqlite3 coeus.db << 'INIT'
.load /usr/local/lib/sqlite3/vec0.so
.read schema.sql
INIT

# Create state file
echo '{"capture_mode": false, "current_session_id": null, "last_capture_block_id": null}' > state.json
mkdir -p exports
```

### 3. Install Python Dependencies

```bash
python3 -m venv venv
source venv/bin/activate

# CPU-only PyTorch (saves 2GB+ GPU packages)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Remaining dependencies
pip install transformers sentence-transformers --no-deps
```

### 4. Download coeus.py

Get `coeus.py` from the examples directory or create it from source. Place it in `~/coeus/coeus.py`.

### 5. Test Installation

```bash
source venv/bin/activate
python3 coeus.py capture "note: Testing Coeus setup"
python3 coeus.py stats
```

Expected output:
```
Total: 1 blocks
Types: {'research': 1}
Links: 0 | Sessions: 0 | Embeddings: 1
Semantic: Yes | Capture mode: Off
```

---

## What This Does

**Problem:** You capture ideas, notes, and research but can never find them later. Traditional search requires exact keywords. Without structure, knowledge becomes a black hole.

**Solution:** A local-first knowledge base that:
- Captures with **explicit triggers** (no accidental logging)
- **Auto-tags and auto-links** content silently
- Uses **semantic search** to find conceptually related items
- Caches **one-line summaries** for 60-70% token savings on briefs
- Tracks **capture sessions** for batch brain dumps

## How It Works

### Capture Types (Auto-Detected)

| Type | Signals | Gets Embedding |
|------|---------|----------------|
| `research` | Facts, TIL, links, concepts | Yes |
| `idea` | "What if", brainstorming, speculation | Yes |
| `work_log` | Shipped, fixed, deployed, standup | No |
| `journal` | Feelings, reflections, "I feel/think" | No |

### Capture Triggers

**Explicit prefixes:**
- `note:`, `capture:`, `log:`, `remember:`, `kb:`

**Template triggers:**
- `standup:` → work_log + tag #standup
- `meeting [name]:` → work_log + extract @attendees
- `idea [project]:` → idea + link [[project]]

**Batch mode:**
```
start capturing
note: First thought
note: Second thought
stop capturing
```

### Search Strategy

1. **FTS first** (zero tokens) - exact keyword matches
2. **If < 3 results**, use semantic search (~50 tokens)
3. **Return summaries** (cached one-liners) not full content
4. **Combine and dedupe** results

### Semantic Search Example

You capture: "Kubernetes uses horizontal pod autoscaling for variable workloads"

Later you search: "find container scaling"

Result: **Found** via semantic similarity, even though "container" and "scaling" weren't in the original capture.

## CLI Usage

```bash
cd ~/coeus
source venv/bin/activate

# Capture
python3 coeus.py capture "note: your content here"
python3 coeus.py capture "idea: something new"

# Search (FTS + semantic fallback)
python3 coeus.py search "your query"

# Brief (uses cached summaries)
python3 coeus.py brief today
python3 coeus.py brief week

# Stats
python3 coeus.py stats

# Batch capture
python3 coeus.py start
python3 coeus.py capture "note: block 1"
python3 coeus.py capture "note: block 2"
python3 coeus.py stop
```

## Skill Integration

To integrate with OpenClaw as a skill, use the `subprocess` tool to call coeus.py:

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

## Configuration Reference

### Tag Aliases

Pre-configured aliases (auto-resolved on capture):

| Alias | Canonical |
|-------|-----------|
| k8s | kubernetes |
| postgres | postgresql |
| ts | typescript |
| js | javascript |
| py | python |
| go | golang |

Add more via SQL:
```sql
INSERT INTO tag_aliases (canonical, alias) VALUES ('your-tag', 'your-alias');
```

### Database Schema

**Core tables:**
- `blocks` - Main content storage
- `block_embeddings` - 384-dim vectors (vec0)
- `block_summaries` - Cached one-liners
- `tags` / `block_tags` - Tag system
- `links` - Block relationships with confidence
- `capture_sessions` - Batch capture tracking

### Storage Requirements

| Component | Size |
|-----------|------|
| Database (~1000 blocks) | ~5-10MB |
| Embeddings (per block) | ~1.5KB |
| Python venv | ~400MB |
| Model cache (~/.cache) | ~100MB |

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| vec0 not found | Extension not installed | Build sqlite-vec from source |
| Embeddings not generating | sentence-transformers missing | Run install-deps.sh |
| Model loads slowly | First run, downloading | Wait for download (~100MB) |
| "No module named X" | venv not activated | Run `source venv/bin/activate` |
| Search returns nothing | FTS syntax error | Use simple keywords, not phrases |

## Lessons Learned

### What Worked Well

- **Explicit triggers only** - Prevents accidental captures, keeps database clean
- **CPU-only PyTorch** - Saves 2GB+ disk space, no GPU needed for inference
- **Write-only captures** - No SELECT after INSERT, fast and simple
- **Cached summaries** - 60-70% token savings on brief generation
- **Graceful degradation** - Works without vec0 (FTS only)

### What Did Not Work

- GPU PyTorch - Unnecessary for embeddings, massive size increase
- Auto-capturing everything - Created noise, reduced signal
- Loading full content for briefs - Wasted tokens on repeated queries

### Gotchas to Watch For

- vec0 extension must be loaded BEFORE creating tables
- Embeddings only generate for research/idea types (by design)
- Model downloads on first use (~100MB) - can be slow
- SQLite FTS5 has query syntax quirks - simple keywords work best

## Security Notes

- All data stored locally in SQLite
- No external APIs needed for daily operation
- sentence-transformers downloads model from HuggingFace on first run
- No secrets in code or config

## Variations

**Web UI:** Add FastAPI layer for browser access (see idea captured in b_1771199388_d307)

**Sync:** Use Syncthing or similar to sync `coeus.db` across devices

**Backup:** Database is a single file - easy to backup/restore

## Related

- [daily-brief](./daily-brief.md) - Use Coeus as a data source for daily summaries
- [idea-pipeline](./idea-pipeline.md) - Research captured ideas overnight

## Changelog

- **2026-02-16** - Initial Coeus v2.0 showcase by KNK

---

**Files:**
- `coeus.py` - Main Python module (19KB)
- `schema.sql` - Database schema
- `install-deps.sh` - Dependency installer

**License:** MIT (match parent project)
