import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.behavioral_agent import behavioral_agent
from app.agents.file_integrity_agent import file_integrity_agent
from app.agents.trust_agent import trust_agent
from app.agents.risk_agent import risk_agent
from app.agents.decision_agent import decision_agent
from app.simulator.normal import create_normal_event
from app.simulator.repeated_message import create_repeated_message_event
from app.simulator.tampering import create_file_tampering_event
from app.simulator.unauthorized_agent import create_unauthorized_agent_event

class TestSecurityAgents(unittest.TestCase):
    def test_behavioral_agent_normal(self):
        event = create_normal_event()
        finding = behavioral_agent.analyze(event)
        self.assertEqual(finding.severity, 0.0)
        self.assertFalse(finding.evidence["anomaly_detected"])

    def test_behavioral_agent_burst(self):
        event = create_repeated_message_event()
        finding = behavioral_agent.analyze(event)
        self.assertGreaterEqual(finding.severity, 50.0)
        self.assertTrue(finding.evidence["anomaly_detected"])

    def test_file_integrity_agent_tamper(self):
        event = create_file_tampering_event()
        finding = file_integrity_agent.analyze(event)
        self.assertGreater(finding.severity, 0.0)
        self.assertTrue(finding.evidence["tampering_confirmed"])

    def test_trust_agent_unauthorized(self):
        event = create_unauthorized_agent_event()
        finding = trust_agent.analyze(event)
        self.assertGreaterEqual(finding.severity, 30.0)
        self.assertTrue(finding.evidence.get("identity_violation", False))

if __name__ == "__main__":
    unittest.main()
