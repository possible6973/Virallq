from database.db import get_connection
from database.models import Script, Prediction, ViralScript, GeneratedCandidate, Report, User
from typing import List, Optional, Dict, Any

# ================= USER CRUD =================
def ensure_default_user() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = 'creator@viraliq.ai'")
    row = cursor.fetchone()
    if row:
        user_id = row['id']
    else:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            ("Default Creator", "creator@viraliq.ai")
        )
        conn.commit()
        user_id = cursor.lastrowid
    conn.close()
    return user_id

# ================= SCRIPTS CRUD =================
def create_script(script: Script) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scripts (user_id, title, script_text, category, audience, platform, duration)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (script.user_id, script.title, script.script_text, script.category, script.audience, script.platform, script.duration))
    conn.commit()
    script_id = cursor.lastrowid
    conn.close()
    return script_id

def get_script_by_id(script_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scripts WHERE id = ?", (script_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_scripts(limit: int = 100) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scripts ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_script(script_id: int, title: str, script_text: str, category: str, audience: str, platform: str, duration: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE scripts
        SET title = ?, script_text = ?, category = ?, audience = ?, platform = ?, duration = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (title, script_text, category, audience, platform, duration, script_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

def delete_script(script_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scripts WHERE id = ?", (script_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

# ================= PREDICTIONS CRUD =================
def save_prediction(prediction: Prediction) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (script_id, ml_score, ann_score, final_score, status)
        VALUES (?, ?, ?, ?, ?)
    """, (prediction.script_id, prediction.ml_score, prediction.ann_score, prediction.final_score, prediction.status))
    conn.commit()
    pred_id = cursor.lastrowid
    conn.close()
    return pred_id

def get_predictions_for_script(script_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions WHERE script_id = ? ORDER BY created_at DESC", (script_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_predictions() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, s.title as script_title, s.category
        FROM predictions p
        LEFT JOIN scripts s ON p.script_id = s.id
        ORDER BY p.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ================= VIRAL SCRIPTS LIBRARY CRUD =================
def add_viral_script(viral_script: ViralScript) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO viral_scripts (category, topic, audience, hook, script_text, duration, views, likes, comments, shares, engagement_rate, performance_label)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        viral_script.category, viral_script.topic, viral_script.audience, viral_script.hook,
        viral_script.script_text, viral_script.duration, viral_script.views, viral_script.likes,
        viral_script.comments, viral_script.shares, viral_script.engagement_rate, viral_script.performance_label
    ))
    conn.commit()
    v_id = cursor.lastrowid
    conn.close()
    return v_id

def get_all_viral_scripts() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM viral_scripts ORDER BY engagement_rate DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def search_viral_scripts(category: str = None, topic: str = None, limit: int = 5) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM viral_scripts WHERE 1=1"
    params = []
    if category and category != "All":
        query += " AND category LIKE ?"
        params.append(f"%{category}%")
    if topic:
        query += " AND (topic LIKE ? OR hook LIKE ? OR script_text LIKE ?)"
        params.extend([f"%{topic}%", f"%{topic}%", f"%{topic}%"])
    query += " ORDER BY engagement_rate DESC LIMIT ?"
    params.append(limit)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_viral_script(script_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM viral_scripts WHERE id = ?", (script_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

# ================= GENERATED CANDIDATES CRUD =================
def save_candidate(candidate: GeneratedCandidate) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO generated_candidates (original_script_id, batch_number, candidate_number, script_text, ml_score, ann_score, final_score, is_best)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (candidate.original_script_id, candidate.batch_number, candidate.candidate_number, candidate.script_text, candidate.ml_score, candidate.ann_score, candidate.final_score, 1 if candidate.is_best else 0))
    conn.commit()
    cid = cursor.lastrowid
    conn.close()
    return cid

def get_candidates_by_script_id(original_script_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM generated_candidates WHERE original_script_id = ? ORDER BY batch_number ASC, final_score DESC", (original_script_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ================= REPORTS CRUD =================
def save_report(report: Report) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reports (script_id, analysis, recommendations)
        VALUES (?, ?, ?)
    """, (report.script_id, report.analysis, report.recommendations))
    conn.commit()
    rid = cursor.lastrowid
    conn.close()
    return rid

def get_reports_by_script_id(script_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports WHERE script_id = ? ORDER BY created_at DESC", (script_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_reports() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, s.title as script_title
        FROM reports r
        LEFT JOIN scripts s ON r.script_id = s.id
        ORDER BY r.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
