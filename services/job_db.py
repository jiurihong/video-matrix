import sqlite3
import os
from datetime import datetime

DB_PATH = os.environ.get('VIDEO_MATRIX_DB','/data/video-matrix/jobs.db')

def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = _conn()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        topic TEXT,
        status TEXT,
        created_at TEXT,
        updated_at TEXT,
        draft_path TEXT,
        final_path TEXT,
        error TEXT
    )
    ''')
    conn.commit()
    conn.close()

def create_job(job_id, topic):
    conn = _conn()
    c = conn.cursor()
    now = datetime.utcnow().isoformat()
    c.execute('INSERT OR REPLACE INTO jobs (id,topic,status,created_at,updated_at) VALUES (?,?,?,?,?)',
              (job_id, topic, 'pending', now, now))
    conn.commit()
    conn.close()

def update_job(job_id, **kwargs):
    conn = _conn()
    c = conn.cursor()
    fields = []
    vals = []
    for k,v in kwargs.items():
        fields.append(f"{k}=?")
        vals.append(v)
    vals.append(job_id)
    now = datetime.utcnow().isoformat()
    fields.append('updated_at=?')
    vals.insert(-1, now)
    sql = f"UPDATE jobs SET {','.join(fields)} WHERE id=?"
    c.execute(sql, vals)
    conn.commit()
    conn.close()

def get_job(job_id):
    conn = _conn()
    c = conn.cursor()
    c.execute('SELECT id,topic,status,created_at,updated_at,draft_path,final_path,error FROM jobs WHERE id=?', (job_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    keys = ['id','topic','status','created_at','updated_at','draft_path','final_path','error']
    return dict(zip(keys, row))

def list_jobs(limit=50):
    conn = _conn()
    c = conn.cursor()
    c.execute('SELECT id,topic,status,created_at,updated_at FROM jobs ORDER BY created_at DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return [{'id':r[0],'topic':r[1],'status':r[2],'created_at':r[3],'updated_at':r[4]} for r in rows]
