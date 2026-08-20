from typing import Dict, Any, List
from app.config import settings
from app.database.schemas import SyntheticSecurityEvent, AgentFinding, RiskLevel, IncidentRecord
from app.database.database import save_incident, update_agent_stats
from app.agents.behavioral_agent import behavioral_agent
from app.agents.file_integrity_agent import file_integrity_agent
from app.agents.trust_agent import trust_agent
from app.agents.risk_agent import risk_agent
from app.agents.decision_agent import decision_agent
from app.risk.scoring import rule_scoring_engine
from app.risk.policies import policy_manager
from app.ml.predictor import ml_predictor
from datetime import datetime
import json

class CentralRiskEngine:
    """
    Central Risk Engine: Coordinates multi-agent analysis pipeline,
    computes hybrid risk score (Rule-Based + ML Prediction),
    derives dynamic risk classification, and enforces adaptive security policies.
    """
    def __init__(self):
        self.ml_weight = settings.ML_WEIGHT
        self.rule_weight = settings.RULE_WEIGHT

    def process_security_event(self, event: SyntheticSecurityEvent) -> Dict[str, Any]:
        # 1. Independent analysis by specialized agents
        f_behavioral = behavioral_agent.analyze(event)
        f_integrity = file_integrity_agent.analyze(event)
        f_trust = trust_agent.analyze(event)
        
        findings = [f_behavioral, f_integrity, f_trust]
        
        # 2. Risk agent aggregates multi-agent telemetry
        aggregated_evidence = risk_agent.aggregate_evidence(event, findings)
        
        # 3. Rule-based risk scoring
        raw_rule, norm_rule, contributions = rule_scoring_engine.compute_rule_score(event, findings)
        
        # 4. Machine Learning Anomaly & Risk Prediction + SHAP
        ml_result = ml_predictor.predict(event)
        ml_prob = ml_result["ml_risk_probability"]
        ml_score = ml_result["ml_risk_score"]
        shap_explanations = ml_result["shap_explanations"]
        
        # 5. Hybrid Dynamic Risk Score Calculation
        # Final Risk = 0.6 * ML Risk + 0.4 * Rule-Based Risk (or configured weights)
        hybrid_risk = (self.ml_weight * ml_score) + (self.rule_weight * norm_rule)
        
        # Normalize and bound to [0, 100]
        final_risk_score = round(min(100.0, max(0.0, hybrid_risk)), 1)
        
        # 6. Adaptive Risk Classification
        risk_level = policy_manager.classify_risk_level(final_risk_score)
        
        # 7. Adaptive Security Policy Selection
        policy = policy_manager.get_policy(risk_level)
        
        # 8. Final Decision Agent synthesis
        decision = decision_agent.make_decision(
            event=event,
            risk_score=final_risk_score,
            risk_level=risk_level,
            policy=policy,
            findings=findings,
            contributions=contributions
        )
        
        # 9. Update Agent Telemetry in Database
        update_agent_stats("Behavioral Agent", detected_threat=(f_behavioral.severity > 0))
        update_agent_stats("File Integrity Agent", detected_threat=(f_integrity.severity > 0))
        update_agent_stats("Trust / Verification Agent", detected_threat=(f_trust.severity > 0))
        update_agent_stats("Risk Agent", detected_threat=(final_risk_score > 30.0))
        update_agent_stats("Final Decision Agent", detected_threat=(final_risk_score > 30.0))
        
        # 10. Persist Incident Record
        incident_id = decision.incident_id
        incident_payload = {
            "id": incident_id,
            "event_id": event.event_id,
            "timestamp": event.timestamp,
            "attack_type": event.attack_type.value if hasattr(event.attack_type, 'value') else str(event.attack_type),
            "risk_score": final_risk_score,
            "risk_level": risk_level.value,
            "source_agent": event.source_agent,
            "destination_agent": event.destination_agent,
            "triggered_agents": decision.triggered_agents,
            "evidence": [c.dict() for c in contributions],
            "security_controls": policy.dict(),
            "final_decision": decision.decision_rationale,
            "recommendation": decision.recommendation,
            "ml_prediction": ml_result,
            "raw_event": event.dict()
        }
        save_incident(incident_payload)
        
        return {
            "incident_id": incident_id,
            "event_id": event.event_id,
            "timestamp": event.timestamp,
            "attack_type": event.attack_type.value if hasattr(event.attack_type, 'value') else str(event.attack_type),
            "risk_score": final_risk_score,
            "risk_level": risk_level.value,
            "agent_findings": [f.dict() for f in findings],
            "aggregated_evidence": aggregated_evidence,
            "rule_scoring": {
                "raw_score": raw_rule,
                "normalized_score": norm_rule,
                "contributions": [c.dict() for c in contributions]
            },
            "ml_prediction": ml_result,
            "security_policy": policy.dict(),
            "final_decision": decision.dict()
        }

risk_engine = CentralRiskEngine()
