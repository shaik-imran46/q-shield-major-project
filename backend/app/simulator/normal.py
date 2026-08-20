import uuid
import hashlib
from datetime import datetime
from app.database.schemas import SyntheticSecurityEvent, AttackType

def create_normal_event() -> SyntheticSecurityEvent:
    event_id = f"EVT-{uuid.uuid4().hex[:6].upper()}"
    msg_id = f"MSG-{uuid.uuid4().hex[:4].upper()}"
    payload = "GET /api/agent/v1/telemetry/heartbeat - Status: OK"
    h = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    
    return SyntheticSecurityEvent(
        event_id=event_id,
        source_agent="Agent-A",
        destination_agent="Agent-B",
        message_id=msg_id,
        timestamp=datetime.utcnow().isoformat(),
        payload=payload,
        message_frequency=5.0,
        normal_frequency=5.0,
        authenticated=True,
        authorized=True,
        integrity_valid=True,
        replay_detected=False,
        mitm_indicator=False,
        file_tampering_detected=False,
        original_file_hash=h,
        current_file_hash=h,
        attack_type=AttackType.NORMAL,
        trust_score=98.0,
        additional_metadata={"scenario": "Standard inter-agent heartbeat exchange"}
    )
