from typing import List, Dict, Any
from app.agents.base_agent import BaseSecurityAgent
from app.database.schemas import SyntheticSecurityEvent, AgentFinding, RiskLevel, SecurityPolicy, FinalDecision
from datetime import datetime

class FinalDecisionAgent(BaseSecurityAgent):
    """
    Agent 5: Final Decision Agent
    Synthesizes multi-agent telemetry and risk engine calculations into an actionable,
    explainable security decision and adaptive control activation plan.
    """
    def __init__(self):
        super().__init__(name="Final Decision Agent", agent_type="Adaptive Policy & Control Orchestrator", confidence_base=0.98)

    def analyze(self, event: SyntheticSecurityEvent) -> AgentFinding:
        self.events_processed += 1
        return AgentFinding(
            agent=self.name,
            finding="Ready to orchestrate final adaptive policy decision",
            severity=0.0,
            confidence=0.98,
            evidence={"status": "DECISION_ORCHESTRATOR_ACTIVE"},
            timestamp=datetime.utcnow().isoformat()
        )

    def make_decision(
        self,
        event: SyntheticSecurityEvent,
        risk_score: float,
        risk_level: RiskLevel,
        policy: SecurityPolicy,
        findings: List[AgentFinding],
        contributions: List[Any]
    ) -> FinalDecision:
        self.events_processed += 1
        
        triggered_agents = [f.agent for f in findings if f.severity > 0]
        if self.name not in triggered_agents:
            triggered_agents.append(self.name)
        if "Risk Agent" not in triggered_agents:
            triggered_agents.append("Risk Agent")
            
        evidence_summaries = []
        for c in contributions:
            evidence_summaries.append(f"{c.factor} (+{c.score_addition:.0f} pts): {c.observed_value}")
            
        if not evidence_summaries:
            evidence_summaries.append("All security metrics within benign operating baseline thresholds.")
            
        # Formulate rationale
        if risk_level == RiskLevel.LOW:
            rationale = f"Evaluated event {event.event_id} with low composite risk score ({risk_score}/100). Baseline agent behavior verified. Standard Post-Quantum Cryptographic (PQC) encryption maintained."
            recommendation = "Continue standard telemetry monitoring with ML-KEM/ML-DSA encryption."
        elif risk_level == RiskLevel.MEDIUM:
            rationale = f"Evaluated event {event.event_id} with moderate composite risk ({risk_score}/100) triggering {len(triggered_agents)} agents. Adaptive escalation to Level 2 defense: PQC + Quantum Random Number Generator (QRNG) simulated entropy re-seeding."
            recommendation = "Enforce QRNG nonce refreshment, re-negotiate session keys, and alert SOC analysts."
        else: # HIGH
            self.threats_detected += 1
            rationale = f"CRITICAL SECURITY ALERT: Evaluated event {event.event_id} with HIGH risk ({risk_score}/100). Detected severe multi-factor anomalies across {len(triggered_agents)} agents. Full Adaptive Security Spectrum activated: PQC + QRNG + BB84 QKD Simulation + Enhanced Auth + Channel Quarantine."
            recommendation = "Quarantine untrusted agent channels, mandate out-of-band BB84 QKD key distillation, and require immediate zero-trust re-authentication."
            
        return FinalDecision(
            incident_id=f"INC-{event.event_id.replace('EVT-', '')}",
            attack_type=event.attack_type.value if hasattr(event.attack_type, 'value') else str(event.attack_type),
            risk_score=risk_score,
            risk_level=risk_level,
            triggered_agents=triggered_agents,
            evidence_summary=evidence_summaries,
            security_policy=policy,
            decision_rationale=rationale,
            recommendation=recommendation,
            timestamp=datetime.utcnow().isoformat()
        )

decision_agent = FinalDecisionAgent()
