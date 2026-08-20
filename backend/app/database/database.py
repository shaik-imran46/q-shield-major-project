import sqlite3
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

def _determine_db_path():
    env_path = os.getenv("DATABASE_PATH")
    if env_path:
        return env_path
    # Try local directory first
    local_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "qshield.db")
    try:
        conn = sqlite3.connect(local_path)
        conn.execute("CREATE TABLE IF NOT EXISTS _test_probe (id INT)")
        conn.execute("DROP TABLE _test_probe")
        conn.close()
        return local_path
    except Exception:
        # Fallback to /tmp or standard writable temp
        return "/tmp/qshield.db"

DB_PATH = _determine_db_path()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=MEMORY;")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'analyst',
        created_at TEXT NOT NULL
    )
    """)
    
    # Agents registry table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agents (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        agent_type TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'ACTIVE',
        events_processed INTEGER NOT NULL DEFAULT 0,
        threats_detected INTEGER NOT NULL DEFAULT 0,
        confidence REAL NOT NULL DEFAULT 0.95,
        trust_score REAL NOT NULL DEFAULT 95.0,
        last_activity TEXT NOT NULL
    )
    """)
    
    # Incidents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id TEXT PRIMARY KEY,
        event_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        attack_type TEXT NOT NULL,
        risk_score REAL NOT NULL,
        risk_level TEXT NOT NULL,
        source_agent TEXT NOT NULL,
        destination_agent TEXT NOT NULL,
        triggered_agents_json TEXT NOT NULL,
        evidence_json TEXT NOT NULL,
        security_controls_json TEXT NOT NULL,
        final_decision TEXT NOT NULL,
        recommendation TEXT NOT NULL,
        ml_prediction_json TEXT NOT NULL,
        raw_event_json TEXT NOT NULL
    )
    """)
    
    # Security events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS security_events (
        event_id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        source_agent TEXT NOT NULL,
        destination_agent TEXT NOT NULL,
        message_id TEXT NOT NULL,
        payload TEXT NOT NULL,
        message_frequency REAL NOT NULL,
        normal_frequency REAL NOT NULL,
        authenticated INTEGER NOT NULL,
        authorized INTEGER NOT NULL,
        integrity_valid INTEGER NOT NULL,
        replay_detected INTEGER NOT NULL,
        attack_type TEXT NOT NULL
    )
    """)
    
    # Agent findings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_findings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT NOT NULL,
        agent_name TEXT NOT NULL,
        finding TEXT NOT NULL,
        severity REAL NOT NULL,
        confidence REAL NOT NULL,
        evidence_json TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)
    
    # Seed default agents if table empty
    cursor.execute("SELECT COUNT(*) as count FROM agents")
    if cursor.fetchone()['count'] == 0:
        now = datetime.utcnow().isoformat()
        default_agents = [
            ("agent-behavioral", "Behavioral Agent", "Anomaly & Rate Analysis", "ACTIVE", 342, 28, 0.91, 95.0, now),
            ("agent-file-integrity", "File Integrity Agent", "Cryptographic Hashing & SHA-256", "ACTIVE", 218, 14, 0.97, 98.0, now),
            ("agent-trust", "Trust / Verification Agent", "Identity & Authorization Registry", "ACTIVE", 450, 19, 0.94, 96.0, now),
            ("agent-risk", "Risk Agent", "Evidence Aggregation & Synthesis", "ACTIVE", 512, 45, 0.96, 99.0, now),
            ("agent-decision", "Final Decision Agent", "Adaptive Policy & Control Orchestrator", "ACTIVE", 512, 45, 0.98, 99.0, now)
        ]
        cursor.executemany("""
        INSERT INTO agents (id, name, agent_type, status, events_processed, threats_detected, confidence, trust_score, last_activity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, default_agents)
    
    conn.commit()
    conn.close()

# Repository Helper Functions
def save_incident(incident_data: Dict[str, Any]):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO incidents (
        id, event_id, timestamp, attack_type, risk_score, risk_level,
        source_agent, destination_agent, triggered_agents_json, evidence_json,
        security_controls_json, final_decision, recommendation, ml_prediction_json, raw_event_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        incident_data['id'],
        incident_data['event_id'],
        incident_data['timestamp'],
        incident_data['attack_type'],
        incident_data['risk_score'],
        incident_data['risk_level'],
        incident_data.get('source_agent', 'Agent-A'),
        incident_data.get('destination_agent', 'Agent-B'),
        json.dumps(incident_data.get('triggered_agents', [])),
        json.dumps(incident_data.get('evidence', [])),
        json.dumps(incident_data.get('security_controls', {})),
        incident_data['final_decision'],
        incident_data['recommendation'],
        json.dumps(incident_data.get('ml_prediction', {})),
        json.dumps(incident_data.get('raw_event', {}))
    ))
    conn.commit()
    conn.close()

def get_all_incidents(limit: int = 100, attack_type: Optional[str] = None, risk_level: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM incidents WHERE 1=1"
    params = []
    
    if attack_type:
        query += " AND attack_type = ?"
        params.append(attack_type)
    if risk_level:
        query += " AND risk_level = ?"
        params.append(risk_level)
        
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    incidents = []
    for r in rows:
        incidents.append({
            "id": r['id'],
            "event_id": r['event_id'],
            "timestamp": r['timestamp'],
            "attack_type": r['attack_type'],
            "risk_score": r['risk_score'],
            "risk_level": r['risk_level'],
            "source_agent": r['source_agent'],
            "destination_agent": r['destination_agent'],
            "triggered_agents": json.loads(r['triggered_agents_json']),
            "evidence": json.loads(r['evidence_json']),
            "security_controls": json.loads(r['security_controls_json']),
            "final_decision": r['final_decision'],
            "recommendation": r['recommendation'],
            "ml_prediction": json.loads(r['ml_prediction_json']),
            "raw_event": json.loads(r['raw_event_json'])
        })
    conn.close()
    return incidents

def get_incident_by_id(incident_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents WHERE id = ? OR event_id = ?", (incident_id, incident_id))
    r = cursor.fetchone()
    conn.close()
    if not r:
        return None
    return {
        "id": r['id'],
        "event_id": r['event_id'],
        "timestamp": r['timestamp'],
        "attack_type": r['attack_type'],
        "risk_score": r['risk_score'],
        "risk_level": r['risk_level'],
        "source_agent": r['source_agent'],
        "destination_agent": r['destination_agent'],
        "triggered_agents": json.loads(r['triggered_agents_json']),
        "evidence": json.loads(r['evidence_json']),
        "security_controls": json.loads(r['security_controls_json']),
        "final_decision": r['final_decision'],
        "recommendation": r['recommendation'],
        "ml_prediction": json.loads(r['ml_prediction_json']),
        "raw_event": json.loads(r['raw_event_json'])
    }

def get_all_agents() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_agent_stats(agent_name: str, detected_threat: bool = False):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    if detected_threat:
        cursor.execute("""
        UPDATE agents 
        SET events_processed = events_processed + 1, 
            threats_detected = threats_detected + 1,
            last_activity = ?
        WHERE name = ? OR agent_type LIKE ?
        """, (now, agent_name, f"%{agent_name}%"))
    else:
        cursor.execute("""
        UPDATE agents 
        SET events_processed = events_processed + 1,
            last_activity = ?
        WHERE name = ? OR agent_type LIKE ?
        """, (now, agent_name, f"%{agent_name}%"))
    conn.commit()
    conn.close()
