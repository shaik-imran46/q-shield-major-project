from typing import List, Dict, Any
from app.agents.base_agent import BaseSecurityAgent
from app.database.schemas import SyntheticSecurityEvent, AgentFinding
from datetime import datetime

class RiskAggregationAgent(BaseSecurityAgent):
    """
    Agent 3: Risk Agent
    Aggregates multi-dimensional evidence from Behavioral, File Integrity, and Trust agents
    without blindly trusting any single detection.
    """
    def __init__(self):
        super().__init__(name="Risk Agent", agent_type="Evidence Aggregation & Synthesis", confidence_base=0.96)

    def analyze(self, event: SyntheticSecurityEvent) -> AgentFinding:
        # Standalone analysis
        self.events_processed += 1
        return AgentFinding(
            agent=self.name,
            finding="Ready to synthesize multi-agent telemetry",
            severity=0.0,
            confidence=0.96,
            evidence={"status": "EVIDENCE_COLLECTOR_READY"},
            timestamp=datetime.utcnow().isoformat()
        )

    def aggregate_evidence(self, event: SyntheticSecurityEvent, findings: List[AgentFinding]) -> Dict[str, Any]:
        self.events_processed += 1
        
        aggregated_evidence = {
            "event_id": event.event_id,
            "timestamp": event.timestamp,
            "attack_type": event.attack_type.value if hasattr(event.attack_type, 'value') else str(event.attack_type),
            "findings_count": len(findings),
            "findings": [f.dict() for f in findings],
            "behavioral_evidence": {},
            "file_integrity_evidence": {},
            "trust_evidence": {},
            "detected_threat_types": []
        }
        
        has_threat = False
        for f in findings:
            if f.severity > 0:
                has_threat = True
                aggregated_evidence["detected_threat_types"].append(f.finding)
            if f.agent == "Behavioral Agent":
                aggregated_evidence["behavioral_evidence"] = f.evidence
            elif f.agent == "File Integrity Agent":
                aggregated_evidence["file_integrity_evidence"] = f.evidence
            elif f.agent == "Trust / Verification Agent":
                aggregated_evidence["trust_evidence"] = f.evidence
                
        if has_threat:
            self.threats_detected += 1
            
        return aggregated_evidence

risk_agent = RiskAggregationAgent()
