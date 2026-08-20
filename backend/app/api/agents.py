from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.database.database import get_all_agents, get_db_connection

router = APIRouter(prefix="/agents", tags=["Agents Monitoring"])

@router.get("")
def list_agents() -> List[Dict[str, Any]]:
    return get_all_agents()

@router.get("/{agent_id}")
def get_agent_detail(agent_id: str) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents WHERE id = ? OR name = ?", (agent_id, agent_id))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Agent not found")
    return dict(row)

@router.post("/{agent_id}/reset")
def reset_agent_stats(agent_id: str) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE agents 
    SET events_processed = 0, threats_detected = 0, trust_score = 98.0
    WHERE id = ? OR name = ?
    """, (agent_id, agent_id))
    conn.commit()
    conn.close()
    return {"status": "SUCCESS", "message": f"Agent {agent_id} counters reset."}
