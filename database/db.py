import sqlite3
import os
import shutil
from pathlib import Path

DB_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DB_DIR / "viraliq.db"

def get_db_path() -> Path:
    # If running on Vercel or serverless read-only filesystem, use writable /tmp
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        tmp_db = Path("/tmp") / "viraliq.db"
        if not tmp_db.exists() and DB_PATH.exists():
            try:
                shutil.copy(DB_PATH, tmp_db)
            except Exception:
                pass
        return tmp_db
    return DB_PATH

def get_connection():
    target_path = get_db_path()
    if not os.environ.get("VERCEL"):
        target_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target_path))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 2. scripts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scripts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER DEFAULT 1,
        title TEXT NOT NULL,
        script_text TEXT NOT NULL,
        category TEXT DEFAULT 'General',
        audience TEXT DEFAULT 'General',
        platform TEXT DEFAULT 'Instagram',
        duration INTEGER DEFAULT 30,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    
    # 3. predictions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        script_id INTEGER NOT NULL,
        ml_score REAL NOT NULL,
        ann_score REAL NOT NULL,
        final_score REAL NOT NULL,
        status TEXT DEFAULT 'Analyzed',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (script_id) REFERENCES scripts(id) ON DELETE CASCADE
    );
    """)
    
    # 4. viral_scripts library table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS viral_scripts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        topic TEXT NOT NULL,
        audience TEXT DEFAULT 'General',
        hook TEXT NOT NULL,
        script_text TEXT NOT NULL,
        duration INTEGER DEFAULT 30,
        views INTEGER DEFAULT 0,
        likes INTEGER DEFAULT 0,
        comments INTEGER DEFAULT 0,
        shares INTEGER DEFAULT 0,
        engagement_rate REAL DEFAULT 0.0,
        performance_label TEXT DEFAULT 'Viral'
    );
    """)
    
    # 5. generated_candidates table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS generated_candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_script_id INTEGER,
        batch_number INTEGER NOT NULL,
        candidate_number INTEGER NOT NULL,
        script_text TEXT NOT NULL,
        ml_score REAL NOT NULL,
        ann_score REAL NOT NULL,
        final_score REAL NOT NULL,
        is_best BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (original_script_id) REFERENCES scripts(id) ON DELETE SET NULL
    );
    """)
    
    # 6. reports table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        script_id INTEGER,
        analysis TEXT NOT NULL,
        recommendations TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (script_id) REFERENCES scripts(id) ON DELETE CASCADE
    );
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized at:", get_db_path())
