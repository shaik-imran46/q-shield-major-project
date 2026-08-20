import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.quantum.qrng import qrng_service
from app.quantum.qkd import qkd_service

class TestQuantumSimulations(unittest.TestCase):
    def test_qrng_generation(self):
        res = qrng_service.generate_random_bits(num_bits=64, num_qubits=4)
        self.assertEqual(len(res["bitstring"]), 64)
        self.assertGreater(res["entropy"], 0.8)
        self.assertIn("simulation_type", res)

    def test_bb84_clean_channel(self):
        res = qkd_service.simulate_key_exchange(num_qubits=32, eavesdropper_present=False)
        self.assertTrue(res["channel_secure"])
        self.assertFalse(res["eavesdropper_detected"])
        self.assertEqual(res["error_rate"], 0.0)
        self.assertNotEqual(res["final_key"], "ABORTED_INSECURE_CHANNEL")

    def test_bb84_eavesdropped_channel(self):
        res = qkd_service.simulate_key_exchange(num_qubits=48, eavesdropper_present=True)
        self.assertTrue(res["eavesdropper_present"])
        # Eve causes ~25% theoretical error rate
        self.assertGreater(res["error_rate"], 0.0)

if __name__ == "__main__":
    unittest.main()
