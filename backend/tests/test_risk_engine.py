import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.risk.risk_engine import risk_engine
from app.simulator.normal import create_normal_event
from app.simulator.mitm import create_mitm_event
from app.database.schemas import RiskLevel

class TestRiskEngine(unittest.TestCase):
    def test_normal_risk_classification(self):
        event = create_normal_event()
        res = risk_engine.process_security_event(event)
        self.assertLessEqual(res["risk_score"], 30.0)
        self.assertEqual(res["risk_level"], "LOW")
        self.assertTrue(res["security_policy"]["pqc_enabled"])
        self.assertFalse(res["security_policy"]["qrng_enabled"])
        self.assertFalse(res["security_policy"]["qkd_enabled"])

    def test_mitm_high_risk_classification(self):
        event = create_mitm_event()
        res = risk_engine.process_security_event(event)
        self.assertGreaterEqual(res["risk_score"], 71.0)
        self.assertEqual(res["risk_level"], "HIGH")
        self.assertTrue(res["security_policy"]["pqc_enabled"])
        self.assertTrue(res["security_policy"]["qrng_enabled"])
        self.assertTrue(res["security_policy"]["qkd_enabled"])

if __name__ == "__main__":
    unittest.main()
