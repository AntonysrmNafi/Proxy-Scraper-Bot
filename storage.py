"""SQLite-backed store for proxy results, plus JSON-lines backup/restore.

Three tables:
- dead_proxies: a proxy that failed a check. Permanently skipped on future scrapes.
- active_proxies: a proxy that passed a check at some point, with its country and last-seen
  ping. Every scrape job re-verifies these first (see bot.py) before scraping anything new -
  if one has gone dead since, it moves to dead_proxies; if it's still alive its ping/country
  here gets refreshed.
- source_stats: per-source (per scraping site) running totals of how many proxies from it
  were checked vs. turned out live. Used to check proxies from historically-better sources
  first on future jobs.

A proxy is never in both dead_proxies and active_proxies at once - mark_dead_bulk removes it
from active_proxies, and restoring a backup skips a row if that proxy is already known (dead
or active) rather than overwriting the DB's current status.

All access runs on a background thread (asyncio.to_thread) since sqlite3 is synchronous -
this keeps the bot's event loop from ever blocking on disk I/O. A threading.Lock serializes
that access: asyncio.to_thread uses a real OS thread pool, and a single shared sqlite3
connection isn't safe under concurrent multi-thread access even with check_same_thread=False -
without the lock, a backup export running at the same moment as a job persisting a batch could
hit "database is locked".

Made by @AntonysrmNafi
"""
import asyncio
import json
import os
import sqlite3
import threading
import time

from config import DB_PATH

_conn: sqlite3.Connection | None = None
_lock = threading.Lock()


def _get_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        db_dir = os.path.dirname(DB_PATH)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.execute(
            "CREATE TABLE IF NOT EXISTS dead_proxies ("
            "proxy TEXT NOT NULL, method TEXT NOT NULL, marked_at REAL NOT NULL, "
            "PRIMARY KEY (proxy, method))"
        )
        _conn.execute(
            "CREATE TABLE IF NOT EXISTS active_proxies ("
            "proxy TEXT NOT NULL, method TEXT NOT NULL, country TEXT NOT NULL DEFAULT 'Unknown', "
            "ping_ms INTEGER NOT NULL DEFAULT 0, "
            "marked_at REAL NOT NULL, PRIMARY KEY (proxy, method))"
        )
        _conn.execute(
            "CREATE TABLE IF NOT EXISTS source_stats ("
            "source TEXT PRIMARY KEY, checked INTEGER NOT NULL DEFAULT 0, live INTEGER NOT NULL DEFAULT 0)"
        )
        _conn.execute(
            "CREATE TABLE IF NOT EXISTS user_stats ("
            "chat_id INTEGER PRIMARY KEY, jobs_run INTEGER NOT NULL DEFAULT 0, "
            "proxies_delivered INTEGER NOT NULL DEFAULT 0, "
            "first_seen REAL NOT NULL, last_seen REAL NOT NULL)"
        )
        _conn.commit()
    return _conn


def _get_dead_set_sync(method: str) -> set:
    with _lock:
        conn = _get_conn()
        rows = conn.execute("SELECT proxy FROM dead_proxies WHERE method = ?", (method,)).fetchall()
        return {row[0] for row in rows}


def _mark_dead_bulk_sync(proxies, method: str):
    if not proxies:
        return
    with _lock:
        conn = _get_conn()
        now = time.time()
        conn.executemany(
            "INSERT OR IGNORE INTO dead_proxies (proxy, method, marked_at) VALUES (?, ?, ?)",
            [(p, method, now) for p in proxies],
        )
        # a proxy can't be both dead and active at once - drop it from active_proxies now
        conn.executemany(
            "DELETE FROM active_proxies WHERE proxy = ? AND method = ?",
            [(p, method) for p in proxies],
        )
        conn.commit()


def _mark_active_bulk_sync(entries, method: str):
    """entries: list of (proxy, country, ping_ms) tuples. Uses REPLACE (not IGNORE) so a
    proxy seen live again gets its ping_ms/country refreshed instead of keeping stale data."""
    if not entries:
        return
    with _lock:
        conn = _get_conn()
        now = time.time()
        conn.executemany(
            "INSERT OR REPLACE INTO active_proxies (proxy, method, country, ping_ms, marked_at) "
            "VALUES (?, ?, ?, ?, ?)",
            [(p, method, country, ping_ms, now) for p, country, ping_ms in entries],
        )
        conn.commit()


def _get_active_proxies_sync(method: str, country: str | None = None) -> list:
    with _lock:
        conn = _get_conn()
        if country:
            rows = conn.execute(
                "SELECT proxy FROM active_proxies WHERE method = ? AND LOWER(country) LIKE ?",
                (method, f"%{country.lower()}%"),
            ).fetchall()
        else:
            rows = conn.execute("SELECT proxy FROM active_proxies WHERE method = ?", (method,)).fetchall()
        return [row[0] for row in rows]


def _bump_source_stats_sync(counts: dict):
    """counts: {source: (checked_in_batch, live_in_batch)}"""
    if not counts:
        return
    with _lock:
        conn = _get_conn()
        conn.executemany(
            "INSERT INTO source_stats (source, checked, live) VALUES (?, ?, ?) "
            "ON CONFLICT(source) DO UPDATE SET checked = checked + excluded.checked, live = live + excluded.live",
            [(source, checked, live) for source, (checked, live) in counts.items()],
        )
        conn.commit()


def _get_source_scores_sync() -> dict:
    """{source: score in (0,1)}, Laplace-smoothed so a brand-new source starts near 0.5
    (neither prioritized nor buried) instead of 0 or a divide-by-zero."""
    with _lock:
        conn = _get_conn()
        rows = conn.execute("SELECT source, checked, live FROM source_stats").fetchall()
        return {source: (live + 1) / (checked + 2) for source, checked, live in rows}


def _count_sync(table: str, method: str) -> int:
    with _lock:
        conn = _get_conn()
        return conn.execute(f"SELECT COUNT(*) FROM {table} WHERE method = ?", (method,)).fetchone()[0]


def _get_stats_sync() -> dict:
    """A snapshot of the whole DB's health: per-method active/dead counts, average ping among
    active proxies, and which countries are best represented right now."""
    with _lock:
        conn = _get_conn()
        active_rows = conn.execute(
            "SELECT method, COUNT(*), AVG(ping_ms) FROM active_proxies GROUP BY method"
        ).fetchall()
        dead_rows = conn.execute("SELECT method, COUNT(*) FROM dead_proxies GROUP BY method").fetchall()
        top_countries = conn.execute(
            "SELECT country, COUNT(*) AS c FROM active_proxies GROUP BY country ORDER BY c DESC LIMIT 5"
        ).fetchall()
        return {
            "active": {method: {"count": count, "avg_ping": round(avg_ping or 0)} for method, count, avg_ping in active_rows},
            "dead": {method: count for method, count in dead_rows},
            "top_countries": top_countries,
        }


def _clear_dead_sync() -> int:
    """Wipes the dead-proxy memory clean. Useful maintenance since that list only ever grows -
    a proxy that was dead months ago might be back up now, and this lets the bot give it
    another chance instead of skipping it forever."""
    with _lock:
        conn = _get_conn()
        count = conn.execute("SELECT COUNT(*) FROM dead_proxies").fetchone()[0]
        conn.execute("DELETE FROM dead_proxies")
        conn.commit()
        return count


def _touch_user_sync(chat_id: int):
    """Records a chat's first/last-seen time, for the Profile screen's 'member since'. Never
    overwrites first_seen on repeat visits - only last_seen moves forward."""
    with _lock:
        conn = _get_conn()
        now = time.time()
        conn.execute(
            "INSERT INTO user_stats (chat_id, jobs_run, proxies_delivered, first_seen, last_seen) "
            "VALUES (?, 0, 0, ?, ?) "
            "ON CONFLICT(chat_id) DO UPDATE SET last_seen = excluded.last_seen",
            (chat_id, now, now),
        )
        conn.commit()


def _bump_user_job_sync(chat_id: int, proxies_delivered: int):
    """Called once per successfully-completed job, for the Profile screen's activity stats."""
    with _lock:
        conn = _get_conn()
        now = time.time()
        conn.execute(
            "INSERT INTO user_stats (chat_id, jobs_run, proxies_delivered, first_seen, last_seen) "
            "VALUES (?, 1, ?, ?, ?) "
            "ON CONFLICT(chat_id) DO UPDATE SET jobs_run = jobs_run + 1, "
            "proxies_delivered = proxies_delivered + excluded.proxies_delivered, last_seen = excluded.last_seen",
            (chat_id, proxies_delivered, now, now),
        )
        conn.commit()


def _get_user_stats_sync(chat_id: int) -> dict:
    with _lock:
        conn = _get_conn()
        row = conn.execute(
            "SELECT jobs_run, proxies_delivered, first_seen FROM user_stats WHERE chat_id = ?", (chat_id,)
        ).fetchone()
        if not row:
            return {"jobs_run": 0, "proxies_delivered": 0, "first_seen": None}
        jobs_run, proxies_delivered, first_seen = row
        return {"jobs_run": jobs_run, "proxies_delivered": proxies_delivered, "first_seen": first_seen}


def _export_sync() -> dict:
    with _lock:
        conn = _get_conn()
        return {
            "dead_proxies": conn.execute("SELECT proxy, method FROM dead_proxies").fetchall(),
            "active_proxies": conn.execute(
                "SELECT proxy, method, country, ping_ms FROM active_proxies"
            ).fetchall(),
        }


def _serialize_backup(data: dict) -> str:
    """One JSON object per line, one line per proxy - everything about that single proxy
    (method, dead/active, country, ping) lives together on its own line, instead of every
    proxy of a kind being crammed into one shared array on one line."""
    lines = []
    for proxy, method in data["dead_proxies"]:
        lines.append(json.dumps({"proxy": proxy, "method": method, "status": "dead"}, ensure_ascii=False))
    for proxy, method, country, ping_ms in data["active_proxies"]:
        lines.append(json.dumps(
            {"proxy": proxy, "method": method, "status": "active", "country": country, "ping_ms": ping_ms},
            ensure_ascii=False,
        ))
    return "\n".join(lines) + ("\n" if lines else "")


def _deserialize_backup(text: str) -> dict:
    """Parses the one-proxy-per-line format back into the (dead_rows, active_rows) shape
    _import_sync expects. Malformed lines are skipped rather than failing the whole restore -
    one bad line shouldn't discard an otherwise-good backup."""
    dead, active = [], []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        proxy, method, status = row.get("proxy"), row.get("method"), row.get("status")
        if not proxy or not method or status not in ("active", "dead"):
            continue
        if status == "dead":
            dead.append((proxy, method))
        else:
            try:
                ping_ms = int(row.get("ping_ms") or 0)
            except (TypeError, ValueError):
                ping_ms = 0
            active.append((proxy, method, row.get("country") or "Unknown", ping_ms))
    return {"dead_proxies": dead, "active_proxies": active}


def _import_sync(data: dict) -> dict:
    """Merges a backup in. For every row in the file, if that (proxy, method) already exists
    in EITHER table, it's skipped - the DB's current dead/active status always wins over a
    (possibly stale) backup, and a proxy is never inserted a second time."""
    with _lock:
        conn = _get_conn()
        now = time.time()

        known = set()
        for proxy, method in conn.execute("SELECT proxy, method FROM dead_proxies"):
            known.add((proxy, method))
        for proxy, method in conn.execute("SELECT proxy, method FROM active_proxies"):
            known.add((proxy, method))

        dead_rows = data.get("dead_proxies") or []
        new_dead = []
        for p, m in dead_rows:
            if (p, m) not in known:
                new_dead.append((p, m, now))
                known.add((p, m))
        conn.executemany(
            "INSERT OR IGNORE INTO dead_proxies (proxy, method, marked_at) VALUES (?, ?, ?)",
            new_dead,
        )

        active_rows = data.get("active_proxies") or []
        new_active = []
        for row in active_rows:
            # backward-compatible with older backups that don't have ping_ms yet
            if len(row) == 4:
                p, m, c, ping_ms = row
            else:
                p, m, c = row
                ping_ms = 0
            if (p, m) in known:
                continue
            new_active.append((p, m, c, ping_ms, now))
            known.add((p, m))
        conn.executemany(
            "INSERT OR REPLACE INTO active_proxies (proxy, method, country, ping_ms, marked_at) "
            "VALUES (?, ?, ?, ?, ?)",
            new_active,
        )

        conn.commit()
        return {
            "dead_proxies": len(new_dead),
            "active_proxies": len(new_active),
            "skipped_duplicates": len(dead_rows) + len(active_rows) - len(new_dead) - len(new_active),
        }


async def get_dead_set(method: str) -> set:
    return await asyncio.to_thread(_get_dead_set_sync, method)


async def mark_dead_bulk(proxies, method: str):
    await asyncio.to_thread(_mark_dead_bulk_sync, proxies, method)


async def dead_count(method: str) -> int:
    return await asyncio.to_thread(_count_sync, "dead_proxies", method)


async def mark_active_bulk(entries, method: str):
    """entries: list of (proxy, country, ping_ms) tuples."""
    await asyncio.to_thread(_mark_active_bulk_sync, entries, method)


async def get_active_proxies(method: str, country: str | None = None) -> list:
    """Proxy strings currently marked active for `method`, optionally narrowed to those whose
    stored country contains `country` (case-insensitive substring match)."""
    return await asyncio.to_thread(_get_active_proxies_sync, method, country)


async def active_count(method: str) -> int:
    return await asyncio.to_thread(_count_sync, "active_proxies", method)


async def get_stats() -> dict:
    """A snapshot of the whole DB: per-method active/dead counts, average ping, top countries."""
    return await asyncio.to_thread(_get_stats_sync)


async def clear_dead_list() -> int:
    """Wipes the dead-proxy memory clean. Returns how many entries were removed."""
    return await asyncio.to_thread(_clear_dead_sync)


async def touch_user(chat_id: int):
    await asyncio.to_thread(_touch_user_sync, chat_id)


async def bump_user_job(chat_id: int, proxies_delivered: int):
    await asyncio.to_thread(_bump_user_job_sync, chat_id, proxies_delivered)


async def get_user_stats(chat_id: int) -> dict:
    """{jobs_run, proxies_delivered, first_seen} for this chat, for the Profile screen."""
    return await asyncio.to_thread(_get_user_stats_sync, chat_id)


async def bump_source_stats(counts: dict):
    """counts: {source: (checked_in_batch, live_in_batch)}"""
    await asyncio.to_thread(_bump_source_stats_sync, counts)


async def get_source_scores() -> dict:
    """{source: live-rate score}, higher = historically better. Missing source -> treat as 0.5."""
    return await asyncio.to_thread(_get_source_scores_sync)


async def export_backup() -> dict:
    """Full snapshot of both tables, across all methods."""
    return await asyncio.to_thread(_export_sync)


async def export_backup_text() -> str:
    """The backup as one-JSON-object-per-line text (see _serialize_backup) - the format
    actually written to the backup file."""
    data = await asyncio.to_thread(_export_sync)
    return await asyncio.to_thread(_serialize_backup, data)


async def import_backup(data: dict) -> dict:
    """Merge a backup dict (as produced by export_backup) into the DB, skipping any proxy
    already known (dead or active). Returns counts of rows actually newly added."""
    return await asyncio.to_thread(_import_sync, data)


async def import_backup_text(text: str) -> dict:
    """Parse one-proxy-per-line backup text and merge it in, same dedup rules as import_backup."""
    data = await asyncio.to_thread(_deserialize_backup, text)
    return await asyncio.to_thread(_import_sync, data)
