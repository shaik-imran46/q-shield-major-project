import uuid
import hashlib
from datetime import datetime
from app.database.schemas import SyntheticSecurityEvent, AttackType

def create_repeated_message_event() -> SyntheticSecurityEvent:
    event_id = f"EVT-{uuid.uuid4().hex[:6].upper()}"
    msg_id = f"MSG-{uuid.uuid4().hex[:4].upper()}"
    payload = "HEARTBEAT_POLL burst_index=48 req_interval=20ms"
    h = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    
    return SyntheticSecurityEvent(
        event_id=event_id,
        source_agent="Agent-A",
        destination_agent="Agent-B",
        message_id=msg_id,
        timestamp=datetime.utcnow().isoformat(),
        payload=payload,
        message_frequency=50.0, # High burst rate: 50 msgs/min vs 5 normal
        normal_frequency=5.0,
        authenticated=True,
        authorized=True,
        integrity_valid=True,
        replay_detected=False,
        mitm_indicator=False,
        file_tampering_detected=False,
        original_file_hash=h,
        current_file_hash=h,
        attack_type=AttackType.REPEATED_MESSAGE,
        trust_score=75.0,
        additional_metadata={
            "observed_rate": "50 msgs/min",
            "baseline_rate": "5 msgs/min",
            "rate_multiplier": "10.0x",
            "burst_spike_detected": True
        }
    )
