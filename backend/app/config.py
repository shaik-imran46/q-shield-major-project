import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Q-Shield: Adaptive Multi-Agent Cyber-Risk Detection and Post-Quantum Security Framework"
    PROJECT_SHORT_NAME: str = "Q-Shield"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Security & Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "qshield-quantum-secure-secret-key-2026-super-secure")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./qshield.db")
    
    # Risk Scoring Weights (Prompt Specified Modular Weights)
    WEIGHT_ABNORMAL_FREQUENCY: float = 50.0
    WEIGHT_AUTHENTICATION_ANOMALY: float = 20.0
    WEIGHT_MESSAGE_INTEGRITY_VIOLATION: float = 20.0
    WEIGHT_SUSPICIOUS_COMMUNICATION: float = 10.0
    WEIGHT_FILE_INTEGRITY_VIOLATION: float = 30.0
    WEIGHT_UNAUTHORIZED_AGENT: float = 30.0
    WEIGHT_REPLAY_DETECTION: float = 30.0
    WEIGHT_MITM_SIMULATION: float = 40.0
    
    # Hybrid Risk Calculation
    ML_WEIGHT: float = 0.60
    RULE_WEIGHT: float = 0.40
    
    # Risk Thresholds
    RISK_LOW_MAX: float = 30.0
    RISK_MEDIUM_MAX: float = 70.0

settings = Settings()
