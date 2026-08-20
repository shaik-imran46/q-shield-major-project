from app.database.schemas import RiskLevel, SecurityPolicy
from app.config import settings

class AdaptiveSecurityPolicyManager:
    """
    Adaptive Security Policy Manager.
    Maps dynamic risk levels to proportional, multi-layered post-quantum and cryptographic controls.
    """
    @staticmethod
    def get_policy(risk_level: RiskLevel) -> SecurityPolicy:
        if risk_level == RiskLevel.LOW:
            return SecurityPolicy(
                risk_level=RiskLevel.LOW,
                pqc_enabled=True,
                qrng_enabled=False,
                qkd_enabled=False,
                enhanced_authentication=False,
                communication_restrictions=False,
                description="Low Risk Level (0-30): Standard Post-Quantum Cryptographic protection active (ML-KEM-768 & ML-DSA-65 lattice key encapsulation & signatures).",
                recommended_actions=[
                    "Maintain continuous telemetry monitoring across agents",
                    "Ensure ML-KEM post-quantum key exchange is active for all inter-agent traffic",
                    "Log benign communication patterns to baseline behavior profile"
                ]
            )
        elif risk_level == RiskLevel.MEDIUM:
            return SecurityPolicy(
                risk_level=RiskLevel.MEDIUM,
                pqc_enabled=True,
                qrng_enabled=True,
                qkd_enabled=False,
                enhanced_authentication=True,
                communication_restrictions=False,
                description="Medium Risk Level (31-70): PQC + QRNG Simulation Active. Quantum randomness entropy used for nonces, salts, and session re-keying to prevent replay and forgery.",
                recommended_actions=[
                    "Activate Quantum Random Number Generator (QRNG) for cryptographic nonces",
                    "Re-negotiate ML-KEM session keys with quantum entropy",
                    "Enforce strict message timestamp expiration windows (< 1000ms)",
                    "Alert SOC analysts of suspicious behavior patterns"
                ]
            )
        else: # HIGH
            return SecurityPolicy(
                risk_level=RiskLevel.HIGH,
                pqc_enabled=True,
                qrng_enabled=True,
                qkd_enabled=True,
                enhanced_authentication=True,
                communication_restrictions=True,
                description="High Risk Level (71-100): Maximum Defense Mode Active. PQC + QRNG + BB84 QKD Simulation + Enhanced Cryptographic Authentication + Communication Isolation.",
                recommended_actions=[
                    "Execute BB84 Quantum Key Distribution simulation to establish out-of-band quantum-secure key material",
                    "Enforce strict agent channel throttling and quarantine untrusted/unauthorized agents",
                    "Mandate full ML-DSA-65 zero-trust signature verification on every message",
                    "Trigger automated SOC incident alert with multi-agent evidence breakdown",
                    "Invalidate all prior nonces and perform mandatory cryptographic re-handshake"
                ]
            )

    @staticmethod
    def classify_risk_level(risk_score: float) -> RiskLevel:
        if risk_score <= settings.RISK_LOW_MAX:
            return RiskLevel.LOW
        elif risk_score <= settings.RISK_MEDIUM_MAX:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.HIGH

policy_manager = AdaptiveSecurityPolicyManager()
