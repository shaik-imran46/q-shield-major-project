from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.database.schemas import SyntheticSecurityEvent, RiskLevel
from app.risk.risk_engine import risk_engine
from app.risk.policies import policy_manager
from app.database.database import get_incident_by_id

router = APIRouter(prefix="", tags=["Security Analysis & Risk"])

@router.post("/analyze")
def analyze_custom_event(event: SyntheticSecurityEvent) -> Dict[str, Any]:
    return risk_engine.process_security_event(event)

@router.get("/risk/{incident_id}")
def get_incident_risk(incident_id: str) -> Dict[str, Any]:
    inc = get_incident_by_id(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {
        "incident_id": inc['id'],
        "risk_score": inc['risk_score'],
        "risk_level": inc['risk_level'],
        "evidence": inc['evidence'],
        "ml_prediction": inc['ml_prediction'],
        "final_decision": inc['final_decision']
    }

@router.get("/security-policy/{risk_level}")
def get_security_policy_for_level(risk_level: str) -> Dict[str, Any]:
    try:
        level_enum = RiskLevel(risk_level.upper())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid risk level. Must be LOW, MEDIUM, or HIGH")
        
    policy = policy_manager.get_policy(level_enum)
    return policy.dict()
