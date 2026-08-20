from fastapi import APIRouter
from typing import Dict, Any
from app.risk.risk_engine import risk_engine
from app.simulator.normal import create_normal_event
from app.simulator.mitm import create_mitm_event
from app.simulator.replay import create_replay_event
from app.simulator.tampering import create_file_tampering_event
from app.simulator.unauthorized_agent import create_unauthorized_agent_event
from app.simulator.repeated_message import create_repeated_message_event

router = APIRouter(prefix="/simulator", tags=["Incident Simulator"])

@router.post("/normal")
def simulate_normal() -> Dict[str, Any]:
    event = create_normal_event()
    return risk_engine.process_security_event(event)

@router.post("/mitm")
def simulate_mitm() -> Dict[str, Any]:
    event = create_mitm_event()
    return risk_engine.process_security_event(event)

@router.post("/replay")
def simulate_replay() -> Dict[str, Any]:
    event = create_replay_event()
    return risk_engine.process_security_event(event)

@router.post("/tampering")
def simulate_tampering() -> Dict[str, Any]:
    event = create_file_tampering_event()
    return risk_engine.process_security_event(event)

@router.post("/unauthorized-agent")
def simulate_unauthorized_agent() -> Dict[str, Any]:
    event = create_unauthorized_agent_event()
    return risk_engine.process_security_event(event)

@router.post("/repeated-message")
def simulate_repeated_message() -> Dict[str, Any]:
    event = create_repeated_message_event()
    return risk_engine.process_security_event(event)
