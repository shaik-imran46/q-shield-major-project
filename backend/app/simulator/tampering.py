import uuid
import hashlib
from datetime import datetime
from app.database.schemas import SyntheticSecurityEvent, AttackType

def create_file_tampering_event() -> SyntheticSecurityEvent:
    event_id = f"EVT-{uuid.uuid4().hex[:6].upper()}"
    msg_id = f"MSG-{uuid.uuid4().hex[:4].upper()}"
    
    pristine_file_content = "SECURITY_POLICY_CONFIG version=2.4 allowed_ports=[443, 8443] enc=PQC_ONLY"
    tampered_file_content = "SECURITY_POLICY_CONFIG version=2.4 allowed_ports=[*] enc=NONE allow_insecure=TRUE"
    
    orig_h = hashlib.sha256(pristine_file_content.encode('utf-8')).hexdigest()
    curr_h = hashlib.sha256(tampered_file_content.encode('utf-8')).hexdigest()
    
    return SyntheticSecurityEvent(
        event_id=event_id,
        source_agent="Agent-A",
        destination_agent="Agent-B",
        message_id=msg_id,
        timestamp=datetime.utcnow().isoformat(),
        payload=f"FILE_SYNC filename=policy_manifest.json sha256={curr_h}",
        message_frequency=5.5,
        normal_frequency=5.0,
        authenticated=True,
        authorized=True,
        integrity_valid=False,
        replay_detected=False,
        mitm_indicator=False,
        file_tampering_detected=True,
        original_file_hash=orig_h,
        current_file_hash=curr_h,
        attack_type=AttackType.FILE_TAMPERING,
        trust_score=60.0,
        additional_metadata={
            "filename": "policy_manifest.json",
            "original_sha256": orig_h,
            "tampered_sha256": curr_h,
            "checksum_mismatch": True
        }
    )
