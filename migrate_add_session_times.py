"""
Small migration script for ANCHOR SQLite DB.
- backs up `productivity.db` to `productivity.db.bak`
- adds `session_start` and `session_end` TEXT columns to `Session` if missing
- backfills them from existing `date` and `duration_min` using midnight as start

Run:
    python migrate_add_session_times.py

"""
import sqlite3
import shutil
import os
from datetime import datetime

DB_PATH = 'productivity.db'
BACKUP_PATH = 'productivity.db.bak'

if not os.path.exists(DB_PATH):
    print(f"Database not found at {DB_PATH}")
    raise SystemExit(1)

# backup
shutil.copy2(DB_PATH, BACKUP_PATH)
print(f"Backup created at {BACKUP_PATH}")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# check columns
cur.execute("PRAGMA table_info(Session)")
cols = [r[1] for r in cur.fetchall()]
print("Existing columns:", cols)

added = False
if 'session_start' not in cols:
    cur.execute("ALTER TABLE Session ADD COLUMN session_start TEXT")
    print("Added column session_start")
    added = True
if 'session_end' not in cols:
    cur.execute("ALTER TABLE Session ADD COLUMN session_end TEXT")
    print("Added column session_end")
    added = True

if added:
    conn.commit()
else:
    print("No new columns added")

# backfill session_start/session_end where null using date + duration_min
# session_start = date || ' 00:00:00'
# session_end = datetime(session_start, '+'||duration_min||' minutes')
cur.execute("SELECT COUNT(*) FROM Session WHERE session_start IS NULL OR session_start = ''")
missing_before = cur.fetchone()[0]
print(f"Rows missing session_start before backfill: {missing_before}")

if missing_before > 0:
    cur.execute("UPDATE Session SET session_start = date || ' 00:00:00', session_end = datetime(date || ' 00:00:00', '+' || duration_min || ' minutes') WHERE session_start IS NULL OR session_start = ''")
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM Session WHERE session_start IS NULL OR session_start = ''")
    missing_after = cur.fetchone()[0]
    print(f"Rows missing session_start after backfill: {missing_after}")
else:
    print("No backfill needed")

conn.close()
print("Migration complete. Verify your app and run tests.")