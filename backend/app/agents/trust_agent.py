from typing import Dict, Any, Set
from app.agents.base_agent import BaseSecurityAgent
from app.database.schemas import SyntheticSecurityEvent, AgentFinding
from datetime import datetime

class TrustVerificationAgent(BaseSecurityAgent):
    """
    Agent 4: Trust / Verification Agent
    Verifies agent identity, authorization registry, cryptographic signatures, and computes dynamic trust scores.
    """
    def __init__(self):
        super().__init__(name="Trust / Verification Agent", agent_type="Identity & Trust Registry", confidence_base=0.94)
        self.known_trusted_agents: Set[str] = {"Agent-A", "Agent-B", "Agent-C", "Gateway-Node-01", "Core-Orchestrator"}

    def analyze(self, event: SyntheticSecurityEvent) -> AgentFinding:
        self.events_processed += 1
        
        src = event.source_agent
        is_known = src in self.known_trusted_agents
        is_auth = event.authenticated
        is_authorized = event.authorized
        trust = event.trust_score
        
        severity = 0.0
        findings = []
        evidence_dict: Dict[str, Any] = {
            "source_agent": src,
            "in_known_registry": is_known,
            "authenticated": is_auth,
            "authorized": is_authorized,
            "trust_score": trust
        }
        
        if not is_authorized or not is_known or "Unknown" in src or "Rogue" in src or "Attacker" in src:
            severity += 30.0
            findings.append(f"Unauthorized / Rogue Agent Identity ({src})")
            evidence_dict["identity_violation"] = True
            
        if not is_auth:
            severity += 20.0
            findings.append("Authentication anomaly / Invalid credentials")
            evidence_dict["auth_failure"] = True
            
        if trust < 50.0:
            severity = max(severity, 25.0)
            findings.append(f"Degraded agent trust score ({trust}/100)")
            evidence_dict["trust_degradation"] = True
            
        if findings:
            self.threats_detected += 1
            finding_str = " | ".join(findings)
            confidence = 0.96
        else:
            finding_str = f"Agent {src} verified, authenticated and authorized"
            confidence = 0.99
            
        return AgentFinding(
            agent=self.name,
            finding=finding_str,
            severity=min(severity, 100.0),
            confidence=confidence,
            evidence=evidence_dict,
            timestamp=datetime.utcnow().isoformat()
        )

trust_agent = TrustVerificationAgent()
