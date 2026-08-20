from abc import ABC, abstractmethod
from typing import Dict, Any
from app.database.schemas import SyntheticSecurityEvent, AgentFinding

class BaseSecurityAgent(ABC):
    def __init__(self, name: str, agent_type: str, confidence_base: float = 0.95):
        self.name = name
        self.agent_type = agent_type
        self.confidence_base = confidence_base
        self.events_processed = 0
        self.threats_detected = 0

    @abstractmethod
    def analyze(self, event: SyntheticSecurityEvent) -> AgentFinding:
        """Analyzes a synthetic security event and returns structured findings and evidence."""
        pass

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.agent_type,
            "status": "ACTIVE",
            "events_processed": self.events_processed,
            "threats_detected": self.threats_detected,
            "confidence": self.confidence_base
        }
