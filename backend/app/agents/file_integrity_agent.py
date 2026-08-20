import hashlib
from typing import Dict, Any
from app.agents.base_agent import BaseSecurityAgent
from app.database.schemas import SyntheticSecurityEvent, AgentFinding
from datetime import datetime

class FileIntegrityAgent(BaseSecurityAgent):
    """
    Agent 2: File Integrity Agent
    Verifies payload and simulated file integrity via cryptographic SHA-256 hashing.
    """
    def __init__(self):
        super().__init__(name="File Integrity Agent", agent_type="Cryptographic Integrity & SHA-256", confidence_base=0.97)

    def analyze(self, event: SyntheticSecurityEvent) -> AgentFinding:
        self.events_processed += 1
        
        # Check explicit file hashes or derive from payload
        orig_hash = event.original_file_hash
        curr_hash = event.current_file_hash
        
        if not orig_hash:
            orig_hash = hashlib.sha256(event.payload.encode('utf-8')).hexdigest()
            curr_hash = orig_hash if event.integrity_valid else hashlib.sha256((event.payload + "_TAMPERED").encode('utf-8')).hexdigest()
            
        hash_mismatch = (orig_hash != curr_hash)
        integrity_failed = (not event.integrity_valid) or hash_mismatch or event.file_tampering_detected
        
        severity = 0.0
        findings = []
        evidence_dict: Dict[str, Any] = {
            "original_hash": orig_hash,
            "current_hash": curr_hash,
            "hashes_match": not hash_mismatch,
            "algorithm": "SHA-256"
        }
        
        if integrity_failed:
            self.threats_detected += 1
            severity = 30.0 if not event.mitm_indicator else 35.0
            findings.append("File / Data integrity violation detected")
            if hash_mismatch:
                findings.append(f"SHA-256 mismatch ({orig_hash[:8]}... != {curr_hash[:8]}...)")
            finding_str = " | ".join(findings)
            confidence = 0.98
            evidence_dict["tampering_confirmed"] = True
        else:
            finding_str = "Cryptographic integrity verified"
            confidence = 0.99
            evidence_dict["tampering_confirmed"] = False
            
        return AgentFinding(
            agent=self.name,
            finding=finding_str,
            severity=severity,
            confidence=confidence,
            evidence=evidence_dict,
            timestamp=datetime.utcnow().isoformat()
        )

file_integrity_agent = FileIntegrityAgent()
