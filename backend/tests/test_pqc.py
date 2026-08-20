import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.quantum.pqc import pqc_service

class TestPostQuantumCryptography(unittest.TestCase):
    def test_kem_encapsulation_decapsulation(self):
        keypair = pqc_service.kem_generate_keypair()
        self.assertIn("public_key", keypair)
        self.assertIn("private_key", keypair)
        
        encap = pqc_service.kem_encapsulate(keypair["public_key"])
        self.assertIn("ciphertext", encap)
        self.assertIn("shared_secret", encap)
        
        decap = pqc_service.kem_decapsulate(keypair["private_key"], encap["ciphertext"])
        self.assertEqual(decap["status"], "DECAPSULATION_SUCCESSFUL")

    def test_dsa_signature_verification(self):
        keypair = pqc_service.dsa_generate_keypair()
        message = "CONFIDENTIAL_SECURITY_COMMAND_1024"
        
        sig = pqc_service.dsa_sign(message, keypair["private_key"])
        self.assertIn("signature", sig)
        
        verify_res = pqc_service.dsa_verify(message, sig["signature"], keypair["public_key"])
        self.assertTrue(verify_res["valid"])
        self.assertEqual(verify_res["status"], "SIGNATURE_VERIFIED_VALID")

if __name__ == "__main__":
    unittest.main()
