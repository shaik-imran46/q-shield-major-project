from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class AttackType(str, Enum):
    NORMAL = "Normal Traffic"
    MITM = "MITM Attack Simulation"
    REPLAY = "Replay Attack Simulation"
    FILE_TAMPERING = "File Tampering Simulation"
    UNAUTHORIZED_AGENT = "Unauthorized Agent Simulation"
    REPEATED_MESSAGE = "Repeated Message Simulation"

# User Auth Schemas
class UserBase(BaseModel):
    username: str
    email: str
    role: UserRole = UserRole.ANALYST

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Security Event Schema
class SyntheticSecurityEvent(BaseModel):
    event_id: str
    source_agent: str
    destination_agent: str
    message_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    payload: str = "Standard agent communication payload"
    message_frequency: float = 5.0
    normal_frequency: float = 5.0
    authenticated: bool = True
    authorized: bool = True
    integrity_valid: bool = True
    replay_detected: bool = False
    mitm_indicator: bool = False
    file_tampering_detected: bool = False
    original_file_hash: Optional[str] = None
    current_file_hash: Optional[str] = None
    attack_type: AttackType = AttackType.NORMAL
    trust_score: float = 95.0
    nonce: Optional[str] = None
    additional_metadata: Dict[str, Any] = Field(default_factory=dict)

# Agent Finding Schema
class AgentFinding(BaseModel):
    agent: str
    finding: str
    severity: float  # 0 to 100
    confidence: float  # 0.0 to 1.0
    evidence: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

# Risk Contribution / SHAP Item
class RiskContribution(BaseModel):
    factor: str
    observed_value: Any
    score_addition: float
    description: str

# Risk Evaluation Schema
class RiskEvaluation(BaseModel):
    raw_rule_score: float
    normalized_rule_score: float
    ml_risk_probability: float
    ml_risk_score: float
    hybrid_risk_score: float
    risk_level: RiskLevel
    contributions: List[RiskContribution]
    shap_explanations: List[Dict[str, Any]]

# Security Policy Schema
class SecurityPolicy(BaseModel):
    risk_level: RiskLevel
    pqc_enabled: bool = True
    qrng_enabled: bool = False
    qkd_enabled: bool = False
    enhanced_authentication: bool = False
    communication_restrictions: bool = False
    description: str
    recommended_actions: List[str]

# Final Decision Schema
class FinalDecision(BaseModel):
    incident_id: str
    attack_type: str
    risk_score: float
    risk_level: RiskLevel
    triggered_agents: List[str]
    evidence_summary: List[str]
    security_policy: SecurityPolicy
    decision_rationale: str
    recommendation: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

# Incident Record
class IncidentRecord(BaseModel):
    id: str
    event_id: str
    timestamp: str
    attack_type: str
    risk_score: float
    risk_level: RiskLevel
    source_agent: str
    destination_agent: str
    triggered_agents: List[str]
    evidence: List[Dict[str, Any]]
    security_controls: Dict[str, Any]
    final_decision: str
    recommendation: str
    ml_prediction: Dict[str, Any]
    raw_event: Dict[str, Any]

# Quantum API Schemas
class QRNGRequest(BaseModel):
    num_bits: int = Field(default=32, ge=8, le=1024)
    num_qubits: int = Field(default=4, ge=1, le=16)

class QRNGResponse(BaseModel):
    bitstring: str
    hex_string: str
    byte_values: List[int]
    entropy: float
    num_bits: int
    execution_time_ms: float
    simulation_type: str = "Quantum Randomness Simulation (Hadamard Superposition & Measurement)"

class QKDRequest(BaseModel):
    num_qubits: int = Field(default=16, ge=8, le=128)
    eavesdropper_present: bool = False

class QKDResponse(BaseModel):
    num_qubits: int
    alice_bits: List[int]
    alice_bases: List[str]
    bob_bases: List[str]
    bob_measured_bits: List[int]
    matching_bases_indices: List[int]
    sifted_key: str
    error_rate: float
    final_key: str
    channel_secure: bool
    eavesdropper_detected: bool
    eavesdropper_present: bool
    eavesdropper_bases: Optional[List[str]] = None
    eavesdropper_measured_bits: Optional[List[int]] = None
    simulation_type: str = "BB84 Quantum Key Distribution Educational Simulation"

class PQCKeygenResponse(BaseModel):
    algorithm: str
    public_key: str
    private_key: str
    key_size_bytes: int
    security_level: str

class PQCEncapRequest(BaseModel):
    public_key: str
    algorithm: str = "ML-KEM-768 (Kyber)"

class PQCEncapResponse(BaseModel):
    algorithm: str
    ciphertext: str
    shared_secret: str

class PQCDecapRequest(BaseModel):
    private_key: str
    ciphertext: str
    algorithm: str = "ML-KEM-768 (Kyber)"

class PQCDecapResponse(BaseModel):
    shared_secret: str
    status: str

class PQCSignRequest(BaseModel):
    message: str
    private_key: str
    algorithm: str = "ML-DSA-65 (Dilithium)"

class PQCSignResponse(BaseModel):
    signature: str
    algorithm: str

class PQCVerifyRequest(BaseModel):
    message: str
    signature: str
    public_key: str
    algorithm: str = "ML-DSA-65 (Dilithium)"

class PQCVerifyResponse(BaseModel):
    valid: bool
    algorithm: str
