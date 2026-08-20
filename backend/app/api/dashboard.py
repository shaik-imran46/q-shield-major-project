from fastapi import APIRouter
from typing import Dict, Any, List
from app.database.database import get_all_incidents, get_all_agents
from app.database.schemas import RiskLevel

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_dashboard_summary() -> Dict[str, Any]:
    incidents = get_all_incidents(limit=100)
    agents = get_all_agents()
    
    total_incidents = len(incidents)
    low_risk = sum(1 for i in incidents if i['risk_level'] == 'LOW')
    medium_risk = sum(1 for i in incidents if i['risk_level'] == 'MEDIUM')
    high_risk = sum(1 for i in incidents if i['risk_level'] == 'HIGH')
    attacks_detected = sum(1 for i in incidents if i['attack_type'] != 'Normal Traffic')
    
    latest_incident = incidents[0] if incidents else None
    
    # Active security controls based on latest incident risk
    if latest_incident:
        current_risk_level = latest_incident['risk_level']
        current_risk_score = latest_incident['risk_score']
    else:
        current_risk_level = "LOW"
        current_risk_score = 12.0
        
    controls = {
        "pqc_active": True,
        "pqc_algorithm": "ML-KEM-768 / ML-DSA-65 (NIST FIPS 203/204)",
        "qrng_active": current_risk_level in ["MEDIUM", "HIGH"],
        "qkd_simulated": current_risk_level == "HIGH",
        "enhanced_auth": current_risk_level in ["MEDIUM", "HIGH"],
        "comm_restrictions": current_risk_level == "HIGH"
    }
    
    return {
        "total_incidents": total_incidents,
        "low_risk_count": low_risk,
        "medium_risk_count": medium_risk,
        "high_risk_count": high_risk,
        "active_agents_count": len(agents),
        "detected_attacks_count": attacks_detected,
        "current_risk_score": current_risk_score,
        "current_risk_level": current_risk_level,
        "security_controls": controls,
        "latest_incident": latest_incident,
        "agents": agents
    }

@router.get("/charts")
def get_dashboard_charts() -> Dict[str, Any]:
    incidents = get_all_incidents(limit=50)
    agents = get_all_agents()
    
    # 1. Timeline series (reversed so oldest to newest)
    timeline = []
    for inc in reversed(incidents):
        timeline.append({
            "timestamp": inc['timestamp'][-8:], # HH:MM:SS
            "risk_score": inc['risk_score'],
            "attack_type": inc['attack_type'],
            "risk_level": inc['risk_level'],
            "ml_probability": inc['ml_prediction'].get('ml_risk_probability', 0.0) * 100
        })
        
    # 2. Incidents by type
    type_counts: Dict[str, int] = {}
    for inc in incidents:
        atype = inc['attack_type']
        type_counts[atype] = type_counts.get(atype, 0) + 1
        
    incidents_by_type = [{"name": k, "count": v} for k, v in type_counts.items()]
    
    # 3. Low/Medium/High distribution
    low = sum(1 for i in incidents if i['risk_level'] == 'LOW')
    med = sum(1 for i in incidents if i['risk_level'] == 'MEDIUM')
    high = sum(1 for i in incidents if i['risk_level'] == 'HIGH')
    
    risk_distribution = [
        {"name": "Low Risk (0-30)", "value": low, "color": "#10B981"},
        {"name": "Medium Risk (31-70)", "value": med, "color": "#F59E0B"},
        {"name": "High Risk (71-100)", "value": high, "color": "#EF4444"}
    ]
    
    # 4. Agent detection counts
    agent_stats = []
    for a in agents:
        agent_stats.append({
            "name": a['name'],
            "events_processed": a['events_processed'],
            "threats_detected": a['threats_detected'],
            "confidence": round(a['confidence'] * 100, 1),
            "trust_score": a['trust_score']
        })
        
    return {
        "risk_timeline": timeline,
        "incidents_by_type": incidents_by_type,
        "risk_distribution": risk_distribution,
        "agent_stats": agent_stats
    }
