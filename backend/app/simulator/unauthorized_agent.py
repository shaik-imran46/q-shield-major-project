import uuid
import hashlib
from datetime import datetime
from app.database.schemas import SyntheticSecurityEvent, AttackType

def create_unauthorized_agent_event() -> SyntheticSecurityEvent:
    event_id = f"EVT-{uuid.uuid4().hex[:6].upper()}"
    msg_id = f"MSG-{uuid.uuid4().hex[:4].upper()}"
    payload = "EXECUTE_COMMAND scope=cluster_admin cmd=export_encryption_keys"
    h = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    
    return SyntheticSecurityEvent(
        event_id=event_id,
        source_agent="Unknown-Agent-07",
        destination_agent="Core-Orchestrator",
        message_id=msg_id,
        timestamp=datetime.utcnow().isoformat(),
        payload=payload,
        message_frequency=6.0,
        normal_frequency=5.0,
        authenticated=False,
        authorized=False,
        integrity_valid=True,
        replay_detected=False,
        mitm_indicator=False,
        file_tampering_detected=False,
        original_file_hash=h,
        current_file_hash=h,
        attack_type=AttackType.UNAUTHORIZED_AGENT,
        trust_score=10.0,
        additional_metadata={
            "agent_identity": "Unknown-Agent-07",
            "registry_lookup": "NOT_FOUND",
            "authorization_status": "DENIED"
        }
    )
