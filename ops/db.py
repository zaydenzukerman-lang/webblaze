#!/usr/bin/env python3
"""WebBlaze client database — the single source of truth every agent reads/writes.
SQLite, local, zero-setup. Blaidd writes leads, Patches updates replies, Jarvis onboards,
Andre builds, Emma logs changes, Cornifer runs Maps, Peter reads the list to send reports.
"""
import sqlite3, os, time, json

DB = os.path.expanduser("~/webblaze/ops/webblaze.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS clients(
  slug         TEXT PRIMARY KEY,
  business     TEXT,
  contact_name TEXT,
  email        TEXT,
  phone        TEXT,
  city         TEXT,
  plan         TEXT DEFAULT 'website',   -- website | maps | both
  brand_color  TEXT,
  intake_path  TEXT,
  site_dir     TEXT,
  live_url     TEXT,
  domain       TEXT,
  gbp_id       TEXT,
  review_link  TEXT,
  status       TEXT DEFAULT 'lead',      -- lead|contacted|interested|onboarding|building|built|live|maps-active|paused|lost
  mrr          REAL DEFAULT 0,           -- monthly recurring (Maps) in $
  notes        TEXT DEFAULT '',
  created_at   TEXT,
  updated_at   TEXT
);
CREATE TABLE IF NOT EXISTS log(
  id INTEGER PRIMARY KEY AUTOINCREMENT, slug TEXT, ts TEXT, actor TEXT, event TEXT
);
CREATE TABLE IF NOT EXISTS changes(
  id INTEGER PRIMARY KEY AUTOINCREMENT, slug TEXT, ts TEXT, request TEXT, status TEXT DEFAULT 'open'
);
"""

def _conn():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; return c

def init():
    with _conn() as c: c.executescript(SCHEMA)

def now(): return time.strftime("%Y-%m-%d %H:%M")

def add_client(d, actor="jarvis"):
    init()
    d = dict(d); d.setdefault("created_at", now()); d["updated_at"] = now()
    cols = ",".join(d); ph = ",".join("?" * len(d))
    with _conn() as c:
        c.execute(f"INSERT OR REPLACE INTO clients({cols}) VALUES({ph})", list(d.values()))
    log(d["slug"], "client added", actor)

def update(slug, actor="jarvis", **f):
    if not f: return
    f["updated_at"] = now()
    sets = ",".join(f"{k}=?" for k in f)
    with _conn() as c:
        c.execute(f"UPDATE clients SET {sets} WHERE slug=?", list(f.values()) + [slug])
    log(slug, "updated " + ", ".join(f"{k}={v}" for k, v in f.items() if k != "updated_at"), actor)

def get(slug):
    with _conn() as c:
        r = c.execute("SELECT * FROM clients WHERE slug=?", (slug,)).fetchone()
        return dict(r) if r else None

def list_clients(status=None):
    q = "SELECT * FROM clients"; a = ()
    if status: q += " WHERE status=?"; a = (status,)
    q += " ORDER BY updated_at DESC"
    with _conn() as c:
        return [dict(r) for r in c.execute(q, a).fetchall()]

def log(slug, event, actor="jarvis"):
    with _conn() as c:
        c.execute("INSERT INTO log(slug,ts,actor,event) VALUES(?,?,?,?)", (slug, now(), actor, event))

def recent_log(n=20):
    with _conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM log ORDER BY id DESC LIMIT ?", (n,)).fetchall()]

def add_change(slug, request, actor="emma"):
    with _conn() as c:
        c.execute("INSERT INTO changes(slug,ts,request) VALUES(?,?,?)", (slug, now(), request))
    log(slug, f"change requested: {request[:70]}", actor)

def open_changes():
    with _conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM changes WHERE status='open' ORDER BY id").fetchall()]

def close_change(cid, actor="emma"):
    with _conn() as c:
        row = c.execute("SELECT slug FROM changes WHERE id=?", (cid,)).fetchone()
        c.execute("UPDATE changes SET status='done' WHERE id=?", (cid,))
    if row: log(row["slug"], f"change #{cid} completed", actor)
