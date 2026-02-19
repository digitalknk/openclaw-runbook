#!/usr/bin/env python3
"""
Coeus Knowledge Base - Core Module v2.0
Personal knowledge capture for ADHD workflows with semantic search
"""

import sqlite3
import time
import secrets
import json
import os
import re
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class Block:
    id: str
    created_at: str
    updated_at: str
    type: str
    content: str
    session_id: Optional[str] = None
    tags: List[str] = None
    people: List[str] = None
    projects: List[str] = None


class Coeus:
    def __init__(self, base_path: str = "~/coeus"):
        self.base_path = os.path.expanduser(base_path)
        self.db_path = os.path.join(self.base_path, "coeus.db")
        self.state_path = os.path.join(self.base_path, "state.json")
        self.vec0_extension = '/usr/local/lib/sqlite3/vec0.so'
        
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
        # Try to load vec0 extension
        self.has_vec0 = self._load_vec0()
        
        # Initialize sentence transformer if vec0 available
        self.encoder = None
        if self.has_vec0:
            self.encoder = self._load_encoder()
            if self.encoder is None:
                self.has_vec0 = False
        
        self.state = self._load_state()
    
    def _load_vec0(self) -> bool:
        """Load vec0 extension, return True if successful"""
        try:
            self.conn.enable_load_extension(True)
            self.conn.load_extension(self.vec0_extension)
            return True
        except Exception as e:
            print(f"Warning: vec0 not available: {e}")
            return False
    
    def _load_encoder(self):
        """Load sentence transformer, return None if fails"""
        try:
            from sentence_transformers import SentenceTransformer
            return SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Warning: sentence-transformers not available: {e}")
            return None
    
    def _load_state(self) -> Dict:
        """Load state.json or return defaults"""
        if os.path.exists(self.state_path):
            with open(self.state_path, 'r') as f:
                return json.load(f)
        return {
            "capture_mode": False,
            "current_session_id": None,
            "last_capture_block_id": None
        }
    
    def _save_state(self):
        """Persist state to disk"""
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def _get_timestamp(self) -> str:
        """Get current UTC timestamp in ISO format"""
        return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    def generate_embedding(self, text: str) -> Optional[Any]:
        """Generate embedding for text if encoder available"""
        if not self.has_vec0 or self.encoder is None:
            return None
        return self.encoder.encode(text)
    
    def _resolve_tag_alias(self, tag: str) -> str:
        """Resolve tag alias to canonical form"""
        result = self.conn.execute(
            "SELECT canonical FROM tag_aliases WHERE alias = ?",
            (tag.lower(),)
        ).fetchone()
        return result['canonical'] if result else tag.lower()
    
    def _infer_type(self, content: str) -> str:
        """Infer block type from content"""
        content_lower = content.lower()
        
        # Work log signals
        work_signals = ['shipped', 'fixed', 'deployed', 'pr #', 'merged', 'standup', 'meeting', '1:1']
        if any(s in content_lower for s in work_signals):
            return 'work_log'
        
        # Journal signals
        journal_signals = ['i feel', 'i think', 'i realized', 'feeling', 'frustrated', 'grateful']
        if any(s in content_lower for s in journal_signals):
            return 'journal'
        
        # Idea signals
        idea_signals = ['what if', 'i should', 'maybe', 'could', 'would be nice']
        if any(s in content_lower for s in idea_signals):
            return 'idea'
        
        # Default
        return 'research'
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract hashtags and technical terms"""
        tags = set()
        
        # Explicit hashtags
        hashtag_pattern = r'#(\w+)'
        for match in re.finditer(hashtag_pattern, content):
            tags.add(match.group(1).lower())
        
        return list(tags)
    
    def capture(self, content: str, block_type: Optional[str] = None, 
                tags: Optional[List[str]] = None, 
                people: Optional[List[str]] = None,
                projects: Optional[List[str]] = None) -> str:
        """
        Capture a knowledge block
        
        Returns block_id
        """
        # Generate block ID
        block_id = f"b_{int(time.time())}_{secrets.token_hex(2)}"
        now = self._get_timestamp()
        
        # Infer type if not specified
        if block_type is None:
            block_type = self._infer_type(content)
        
        # Auto-extract tags if none provided
        if tags is None:
            tags = self._extract_tags(content)
        
        # Get session
        session_id = self.state.get('current_session_id')
        
        # Insert block
        self.conn.execute(
            """INSERT INTO blocks (id, created_at, updated_at, type, content, session_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (block_id, now, now, block_type, content, session_id)
        )
        
        # Add tags with alias resolution
        for tag in tags:
            canonical = self._resolve_tag_alias(tag)
            self.conn.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (canonical,))
            self.conn.execute(
                """INSERT OR IGNORE INTO block_tags (block_id, tag_id)
                   SELECT ?, id FROM tags WHERE name = ?""",
                (block_id, canonical)
            )
        
        # Add people
        if people:
            for person in people:
                self.conn.execute("INSERT OR IGNORE INTO people (name) VALUES (?)", (person,))
                self.conn.execute(
                    """INSERT OR IGNORE INTO block_people (block_id, person_id)
                       SELECT ?, id FROM people WHERE name = ?""",
                    (block_id, person)
                )
        
        # Add projects
        if projects:
            for project in projects:
                self.conn.execute("INSERT OR IGNORE INTO projects (name) VALUES (?)", (project,))
                self.conn.execute(
                    """INSERT OR IGNORE INTO block_projects (block_id, project_id)
                       SELECT ?, id FROM projects WHERE name = ?""",
                    (block_id, project)
                )
        
        # Generate summary + embedding for research/idea blocks
        if block_type in ('research', 'idea') and self.has_vec0:
            summary = content[:60] + "..." if len(content) > 60 else content
            
            self.conn.execute(
                """INSERT INTO block_summaries (block_id, one_line, generated_at)
                   VALUES (?, ?, ?)""",
                (block_id, summary, now)
            )
            
            embedding = self.generate_embedding(content)
            if embedding is not None:
                self.conn.execute(
                    """INSERT INTO block_embeddings (block_id, embedding)
                       VALUES (?, vec_f32(?))""",
                    (block_id, embedding.tobytes())
                )
        
        # Auto-link with confidence
        self._auto_link(block_id, tags)
        
        # Update capture day
        self.conn.execute(
            """INSERT INTO capture_days (date, block_count)
               VALUES (DATE('now'), 1)
               ON CONFLICT(date) DO UPDATE SET block_count = block_count + 1"""
        )
        
        self.conn.commit()
        
        # Update state
        self.state['last_capture_block_id'] = block_id
        self._save_state()
        
        return block_id
    
    def _auto_link(self, block_id: str, tags: List[str]):
        """Auto-link block to others with shared tags"""
        if not tags:
            return
        
        placeholders = ','.join('?' * len(tags))
        related = self.conn.execute(
            f"""SELECT DISTINCT b.id FROM blocks b
                JOIN block_tags bt ON b.id = bt.block_id
                JOIN tags t ON bt.tag_id = t.id
                WHERE t.name IN ({placeholders})
                AND b.id != ?
                LIMIT 10""",
            (*tags, block_id)
        ).fetchall()
        
        now = self._get_timestamp()
        for row in related:
            confidence = min(len(tags) / 5.0, 1.0)
            self.conn.execute(
                """INSERT OR IGNORE INTO links (source_id, target_id, link_type, confidence, created_at)
                   VALUES (?, ?, 'auto', ?, ?)""",
                (block_id, row['id'], confidence, now)
            )
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Hybrid search: FTS first, then semantic if needed
        """
        # Try FTS first
        fts_results = self.conn.execute(
            """SELECT b.id, b.type, b.created_at,
                      COALESCE(s.one_line, SUBSTR(b.content, 1, 60)) as summary
               FROM blocks_fts
               JOIN blocks b ON blocks_fts.id = b.id
               LEFT JOIN block_summaries s ON b.id = s.block_id
               WHERE blocks_fts MATCH ?
               ORDER BY rank
               LIMIT ?""",
            (query, limit)
        ).fetchall()
        
        if len(fts_results) >= 3 or not self.has_vec0:
            return [dict(r) for r in fts_results]
        
        # Semantic fallback
        query_emb = self.generate_embedding(query)
        if query_emb is None:
            return [dict(r) for r in fts_results]
        
        semantic = self.conn.execute(
            """SELECT b.id, b.type, b.created_at,
                      COALESCE(s.one_line, SUBSTR(b.content, 1, 60)) as summary,
                      1.0 - vec_distance_cosine(be.embedding, vec_f32(?)) as similarity
               FROM block_embeddings be
               JOIN blocks b ON be.block_id = b.id
               LEFT JOIN block_summaries s ON b.id = s.block_id
               WHERE similarity > 0.6
               ORDER BY similarity DESC
               LIMIT ?""",
            (query_emb.tobytes(), limit)
        ).fetchall()
        
        # Combine and dedupe
        seen = {r['id'] for r in fts_results}
        combined = list(fts_results)
        for row in semantic:
            if row['id'] not in seen:
                combined.append(dict(row))
                seen.add(row['id'])
        
        return combined[:limit]
    
    def find_related(self, block_id: str, limit: int = 10) -> List[Dict]:
        """Find related blocks using tags and semantic similarity"""
        # Tag matches
        tag_matches = self.conn.execute(
            """SELECT DISTINCT b.id, b.type, b.created_at,
                      COALESCE(s.one_line, SUBSTR(b.content, 1, 60)) as summary,
                      1.0 as score, 'tag_match' as source
               FROM blocks b1
               JOIN block_tags bt1 ON b1.id = bt1.block_id
               JOIN block_tags bt2 ON bt1.tag_id = bt2.tag_id
               JOIN blocks b ON bt2.block_id = b.id
               LEFT JOIN block_summaries s ON b.id = s.block_id
               WHERE b1.id = ? AND b.id != ?
               LIMIT ?""",
            (block_id, block_id, limit)
        ).fetchall()
        
        if not self.has_vec0:
            return [dict(r) for r in tag_matches]
        
        # Semantic matches
        semantic = self.conn.execute(
            """SELECT b.id, b.type, b.created_at,
                      COALESCE(s.one_line, SUBSTR(b.content, 1, 60)) as summary,
                      1.0 - vec_distance_cosine(be1.embedding, be2.embedding) as score,
                      'semantic' as source
               FROM block_embeddings be1
               JOIN block_embeddings be2 ON be1.block_id != be2.block_id
               JOIN blocks b ON be2.block_id = b.id
               LEFT JOIN block_summaries s ON b.id = s.block_id
               WHERE be1.block_id = ?
               AND vec_distance_cosine(be1.embedding, be2.embedding) < 0.4
               ORDER BY score DESC
               LIMIT ?""",
            (block_id, limit)
        ).fetchall()
        
        # Combine and score
        seen = {r['id'] for r in tag_matches}
        combined = [dict(r) for r in tag_matches]
        
        for row in semantic:
            if row['id'] not in seen:
                combined.append(dict(row))
            else:
                for item in combined:
                    if item['id'] == row['id']:
                        item['score'] = min(1.0, item['score'] + 0.2)
                        item['source'] = 'both'
        
        combined.sort(key=lambda x: x['score'], reverse=True)
        return combined[:limit]
    
    def brief(self, period: str = "today") -> Dict:
        """Generate brief for a time period"""
        # Time range calculation
        now = datetime.now(timezone.utc)
        
        if period == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        elif period == "yesterday":
            yesterday = now.replace(hour=0, minute=0, second=0, microsecond=0)
            yesterday = yesterday.replace(day=yesterday.day - 1)
            start = yesterday
            end = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "week":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            start = start.replace(day=start.day - start.weekday())
            end = now
        else:
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        
        start_str = start.isoformat().replace('+00:00', 'Z')
        end_str = end.isoformat().replace('+00:00', 'Z')
        
        # Get counts
        counts = self.conn.execute(
            """SELECT type, COUNT(*) as count
               FROM blocks
               WHERE created_at BETWEEN ? AND ?
               GROUP BY type""",
            (start_str, end_str)
        ).fetchall()
        
        # Get summaries
        blocks = self.conn.execute(
            """SELECT b.type, b.id,
                      COALESCE(s.one_line, SUBSTR(b.content, 1, 60)) as summary,
                      b.created_at
               FROM blocks b
               LEFT JOIN block_summaries s ON b.id = s.block_id
               WHERE b.created_at BETWEEN ? AND ?
               ORDER BY b.type, b.created_at
               LIMIT 100""",
            (start_str, end_str)
        ).fetchall()
        
        grouped = {}
        for row in blocks:
            t = row['type']
            if t not in grouped:
                grouped[t] = []
            grouped[t].append(dict(row))
        
        return {
            'period': period,
            'counts': {r['type']: r['count'] for r in counts},
            'blocks': grouped,
            'total': sum(r['count'] for r in counts)
        }
    
    def start_capture_mode(self) -> str:
        """Start batch capture session"""
        session_id = f"cs_{int(time.time())}_{secrets.token_hex(2)}"
        now = self._get_timestamp()
        
        self.conn.execute(
            """INSERT INTO capture_sessions (id, started_at, mode)
               VALUES (?, ?, 'batch')""",
            (session_id, now)
        )
        self.conn.commit()
        
        self.state['capture_mode'] = True
        self.state['current_session_id'] = session_id
        self._save_state()
        
        return session_id
    
    def stop_capture_mode(self) -> int:
        """Stop batch capture, return block count"""
        session_id = self.state.get('current_session_id')
        if not session_id:
            return 0
        
        now = self._get_timestamp()
        
        count = self.conn.execute(
            "SELECT COUNT(*) FROM blocks WHERE session_id = ?",
            (session_id,)
        ).fetchone()[0]
        
        self.conn.execute(
            """UPDATE capture_sessions
               SET ended_at = ?, block_count = ?
               WHERE id = ?""",
            (now, count, session_id)
        )
        self.conn.commit()
        
        self.state['capture_mode'] = False
        self.state['current_session_id'] = None
        self._save_state()
        
        return count
    
    def stats(self) -> Dict:
        """Get database statistics"""
        total = self.conn.execute("SELECT COUNT(*) FROM blocks").fetchone()[0]
        by_type = self.conn.execute(
            "SELECT type, COUNT(*) as count FROM blocks GROUP BY type"
        ).fetchall()
        
        links = self.conn.execute("SELECT COUNT(*) FROM links").fetchone()[0]
        sessions = self.conn.execute("SELECT COUNT(*) FROM capture_sessions").fetchone()[0]
        embeddings = self.conn.execute("SELECT COUNT(*) FROM block_embeddings").fetchone()[0] if self.has_vec0 else 0
        
        return {
            'total_blocks': total,
            'by_type': {r['type']: r['count'] for r in by_type},
            'links': links,
            'sessions': sessions,
            'embeddings': embeddings,
            'has_semantic': self.has_vec0,
            'capture_mode': self.state.get('capture_mode', False)
        }
    
    def close(self):
        """Close database connection"""
        self.conn.close()


if __name__ == "__main__":
    # Simple CLI test
    import sys
    
    coeus = Coeus()
    
    if len(sys.argv) < 2:
        print("Usage: coeus.py <command> [args]")
        print("Commands: capture, search, brief, stats, start, stop")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "capture" and len(sys.argv) > 2:
        content = " ".join(sys.argv[2:])
        block_id = coeus.capture(content)
        print(f"Captured {block_id}")
    
    elif cmd == "search" and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        results = coeus.search(query)
        for r in results:
            print(f"[{r['id']}] {r['type']} - {r['summary'][:50]}...")
    
    elif cmd == "brief":
        period = sys.argv[2] if len(sys.argv) > 2 else "today"
        data = coeus.brief(period)
        print(f"Brief for {data['period']}: {data['total']} blocks")
        for t, blocks in data['blocks'].items():
            print(f"\n{t} ({len(blocks)}):")
            for b in blocks[:5]:
                print(f"  - {b['summary'][:60]}")
    
    elif cmd == "stats":
        s = coeus.stats()
        print(f"Total: {s['total_blocks']} blocks")
        print(f"Types: {s['by_type']}")
        print(f"Links: {s['links']} | Sessions: {s['sessions']} | Embeddings: {s['embeddings']}")
        print(f"Semantic: {'Yes' if s['has_semantic'] else 'No'} | Capture mode: {'On' if s['capture_mode'] else 'Off'}")
    
    elif cmd == "start":
        sid = coeus.start_capture_mode()
        print(f"Capture mode on ({sid})")
    
    elif cmd == "stop":
        count = coeus.stop_capture_mode()
        print(f"Capture mode off. Captured {count} blocks.")
    
    else:
        print(f"Unknown command: {cmd}")
    
    coeus.close()
