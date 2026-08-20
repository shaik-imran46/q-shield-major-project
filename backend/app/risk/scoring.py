from typing import Dict, Any, List, Tuple
from app.config import settings
from app.database.schemas import SyntheticSecurityEvent, AgentFinding, RiskContribution

class RuleBasedScoringEngine:
    """
    Transparent, modular rule-based risk scoring system for multi-agent evidence.
    Applies modular additive weights normalized strictly to [0, 100].
    """
    def __init__(self):
        self.weights = {
            "abnormal_frequency": settings.WEIGHT_ABNORMAL_FREQUENCY,           # +50
            "authentication_anomaly": settings.WEIGHT_AUTHENTICATION_ANOMALY,   # +20
            "message_integrity": settings.WEIGHT_MESSAGE_INTEGRITY_VIOLATION,   # +20
            "suspicious_communication": settings.WEIGHT_SUSPICIOUS_COMMUNICATION, # +10
            "file_integrity": settings.WEIGHT_FILE_INTEGRITY_VIOLATION,         # +30
            "unauthorized_agent": settings.WEIGHT_UNAUTHORIZED_AGENT,           # +30
            "replay_detection": settings.WEIGHT_REPLAY_DETECTION,               # +30
            "mitm_simulation": settings.WEIGHT_MITM_SIMULATION                  # +40
        }

    def compute_rule_score(self, event: SyntheticSecurityEvent, findings: List[AgentFinding]) -> Tuple[float, float, List[RiskContribution]]:
        raw_score = 0.0
        contributions: List[RiskContribution] = []
        
        # 1. Check abnormal communication frequency
        if event.message_frequency >= (event.normal_frequency * 2.5) or event.message_frequency >= 30.0:
            score_add = self.weights["abnormal_frequency"]
            raw_score += score_add
            contributions.append(RiskContribution(
                factor="Abnormal Communication Frequency",
                observed_value=f"{event.message_frequency} msgs/min (Normal: {event.normal_frequency})",
                score_addition=score_add,
                description="Sudden surge in request rate exceeding baseline profile"
            ))
            
        # 2. Check authentication anomaly
        if not event.authenticated:
            score_add = self.weights["authentication_anomaly"]
            raw_score += score_add
            contributions.append(RiskContribution(
                factor="Authentication Anomaly",
                observed_value="authenticated=False",
                score_addition=score_add,
                description="Invalid credentials or signature verification failure"
            ))
            
        # 3. Check message integrity
        if not event.integrity_valid:
            score_add = self.weights["message_integrity"]
            raw_score += score_add
            contributions.append(RiskContribution(
                factor="Message Integrity Violation",
                observed_value="integrity_valid=False",
                score_addition=score_add,
                description="In-transit payload modification or HMAC mismatch"
            ))
            
        # 4. Check suspicious communication interval/pattern
        if event.mitm_indicator or "Suspicious" in str(event.additional_metadata):
            score_add = self.weights["suspicious_communication"]
            raw_score += score_add
            contributions.append(RiskContribution(
                factor="Suspicious Communication",
                observed_value="Anomalous inter-agent routing pattern",
                score_addition=score_add,
                description="Unregistered intermediary hop detected"
            ))
            
        # 5. Check file integrity
        if event.file_tampering_detected or (event.original_file_hash and event.current_file_hash and event.original_file_hash != event.current_file_hash):
            score_add = self.weights["file_integrity"]
            raw_score += score_add
            contributions.append(RiskContribution(
                factor="File Integrity Violation",
                observed_value="SHA-256 Hash Mismatch",
                score_addition=score_add,
                description="Cryptographic checksum of synthetic file does not match pristine digest"
            ))
            
        # 6. Check unauthorized agent
        if not event.authorized or "Unknown" in event.source_agent or "Rogue" in event.source_agent:
            score_add = self.weights["unauthorized_agent"]
            raw_score += score_add
            contributions.append(RiskContribution(
                factor="Unauthorized Agent",
                observed_value=f"Agent ID: {event.source_agent} (authorized=False)",
                score_addition=score_add,
                description="Unregistered agent attempting privileged system interaction"
            ))
            
        # 7. Check replay detection
        if event.replay_detected:
            score_add = self.weights["replay_detection"]
            raw_score += score_add
            contributions.append(RiskContribution(
                factor="Replay Detection",
                observed_value=f"Message ID: {event.message_id} (Stale/Duplicate)",
                score_addition=score_add,
                description="Re-submission of previously authenticated token or payload"
            ))
            
        # 8. Check MITM simulation
        if event.mitm_indicator:
            score_add = self.weights["mitm_simulation"]
            raw_score += score_add
            contributions.append(RiskContribution(
                factor="MITM Simulation Interception",
                observed_value="Synthetic Interceptor Active",
                score_addition=score_add,
                description="Interception proxy detected modifying headers and payloads"
            ))
            
        # Normalized score capped at 100
        normalized_score = min(raw_score, 100.0)
        return raw_score, normalized_score, contributions

rule_scoring_engine = RuleBasedScoringEngine()
