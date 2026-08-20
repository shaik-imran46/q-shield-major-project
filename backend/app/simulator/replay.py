import uuid
import hashlib
from datetime import datetime
from app.database.schemas import SyntheticSecurityEvent, AttackType

def create_replay_event() -> SyntheticSecurityEvent:
    event_id = f"EVT-{uuid.uuid4().hex[:6].upper()}"
    reused_msg_id = "MSG-REPLAY-883"
    payload = "AUTH_TOKEN_GRANT action=privileged_sync nonce=NONCE-OLD-994"
    h = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    
    return SyntheticSecurityEvent(
        event_id=event_id,
        source_agent="Agent-A",
        destination_agent="Agent-B",
        message_id=reused_msg_id,
        timestamp="2026-08-19T21:10:00.000000", # Stale timestamp
        payload=payload,
        message_frequency=12.0,
        normal_frequency=5.0,
        authenticated=True,
        authorized=True,
        integrity_valid=True,
        replay_detected=True,
        mitm_indicator=False,
        file_tampering_detected=False,
        original_file_hash=h,
        current_file_hash=h,
        attack_type=AttackType.REPLAY,
        trust_score=65.0,
        nonce="NONCE-OLD-994",
        additional_metadata={
            "stale_timestamp_delta_sec": 3600,
            "nonce_reuse": True,
            "duplicate_message_id": reused_msg_id
        }
    )
