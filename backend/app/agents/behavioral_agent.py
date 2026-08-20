from typing import Dict, Any
from app.agents.base_agent import BaseSecurityAgent
from app.database.schemas import SyntheticSecurityEvent, AgentFinding
from datetime import datetime

class BehavioralAgent(BaseSecurityAgent):
    """
    Agent 1: Behavioral Agent
    Analyzes communication behavior, frequency spikes, repeated messages, and anomalous traffic patterns.
    """
    def __init__(self):
        super().__init__(name="Behavioral Agent", agent_type="Anomaly & Rate Analysis", confidence_base=0.91)

    def analyze(self, event: SyntheticSecurityEvent) -> AgentFinding:
        self.events_processed += 1
        
        freq = event.message_frequency
        norm = event.normal_frequency
        is_spike = freq > (norm * 2.5) or freq >= 30.0
        is_replay = event.replay_detected
        is_mitm = event.mitm_indicator
        
        severity = 0.0
        findings = []
        evidence_dict: Dict[str, Any] = {
            "observed_frequency": freq,
            "baseline_frequency": norm,
            "frequency_ratio": round(freq / norm, 2) if norm > 0 else 1.0,
            "anomaly_detected": False
        }
        
        if is_spike:
            severity += 50.0
            findings.append("Abnormal communication frequency")
            evidence_dict["frequency_spike"] = True
            evidence_dict["excess_messages_per_min"] = freq - norm
            
        if is_replay:
            severity = max(severity, 30.0)
            findings.append("Repeated message pattern / Replay burst")
            evidence_dict["replay_burst_detected"] = True
            
        if is_mitm:
            severity = max(severity, 20.0)
            findings.append("Suspicious communication interval variance")
            evidence_dict["interval_jitter_ms"] = 420.5
            
        if findings:
            self.threats_detected += 1
            finding_str = " | ".join(findings)
            evidence_dict["anomaly_detected"] = True
            confidence = min(0.98, 0.88 + (0.02 * (freq / max(norm, 1.0))))
        else:
            finding_str = "Normal communication behavior"
            confidence = 0.95
            
        return AgentFinding(
            agent=self.name,
            finding=finding_str,
            severity=min(severity, 100.0),
            confidence=round(confidence, 2),
            evidence=evidence_dict,
            timestamp=datetime.utcnow().isoformat()
        )

behavioral_agent = BehavioralAgent()
