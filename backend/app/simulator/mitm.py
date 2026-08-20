import uuid
import hashlib
from datetime import datetime
from app.database.schemas import SyntheticSecurityEvent, AttackType

def create_mitm_event() -> SyntheticSecurityEvent:
    event_id = f"EVT-{uuid.uuid4().hex[:6].upper()}"
    msg_id = f"MSG-{uuid.uuid4().hex[:4].upper()}"
    original_payload = "TRANSFER_FUNDS amount=500 recipient=Agent-B"
    tampered_payload = "TRANSFER_FUNDS amount=500000 recipient=Attacker-Proxy"
    
    orig_hash = hashlib.sha256(original_payload.encode('utf-8')).hexdigest()
    tampered_hash = hashlib.sha256(tampered_payload.encode('utf-8')).hexdigest()
    
    return SyntheticSecurityEvent(
        event_id=event_id,
        source_agent="Agent-A",
        destination_agent="Agent-B",
        message_id=msg_id,
        timestamp=datetime.utcnow().isoformat(),
        payload=tampered_payload,
        message_frequency=8.0,
        normal_frequency=5.0,
        authenticated=False, # Auth header invalid due to in-flight tampering
        authorized=True,
        integrity_valid=False,
        replay_detected=False,
        mitm_indicator=True,
        file_tampering_detected=True,
        original_file_hash=orig_hash,
        current_file_hash=tampered_hash,
        attack_type=AttackType.MITM,
        trust_score=40.0,
        additional_metadata={
            "interceptor_detected": "Synthetic-MITM-Proxy",
            "hop_variance_ms": 420.0,
            "original_payload": original_payload,
            "modified_payload": tampered_payload
        }
    )
