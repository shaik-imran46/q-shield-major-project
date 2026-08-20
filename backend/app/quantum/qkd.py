import numpy as np
import hashlib
from typing import Dict, Any, List

class BB84Simulator:
    """
    Educational BB84 Quantum Key Distribution (QKD) Simulator.
    Demonstrates quantum state preparation, basis reconciliation,
    eavesdropping detection via QBER (Quantum Bit Error Rate), and key distillation.
    """
    def __init__(self):
        self.bases_symbols = ["+", "x"] # + = Rectilinear, x = Diagonal
        
    def simulate_key_exchange(self, num_qubits: int = 16, eavesdropper_present: bool = False) -> Dict[str, Any]:
        np.random.seed(None)
        
        # 1. Alice generates random bits and random bases
        alice_bits = [int(np.random.choice([0, 1])) for _ in range(num_qubits)]
        alice_bases = [str(np.random.choice(self.bases_symbols)) for _ in range(num_qubits)]
        
        # Qubits in transit (represented by (bit, basis))
        qubit_states = list(zip(alice_bits, alice_bases))
        
        eve_bases = []
        eve_measured_bits = []
        
        # 2. Interception / Eavesdropping stage (Eve)
        if eavesdropper_present:
            modified_states = []
            for bit, basis in qubit_states:
                e_basis = str(np.random.choice(self.bases_symbols))
                eve_bases.append(e_basis)
                if e_basis == basis:
                    e_bit = bit
                else:
                    # Basis mismatch causes quantum state collapse
                    e_bit = int(np.random.choice([0, 1]))
                eve_measured_bits.append(e_bit)
                # Eve re-transmits qubit in her measured basis state
                modified_states.append((e_bit, e_basis))
            qubits_received_by_bob = modified_states
        else:
            qubits_received_by_bob = qubit_states
            
        # 3. Bob chooses random measurement bases
        bob_bases = [str(np.random.choice(self.bases_symbols)) for _ in range(num_qubits)]
        bob_measured_bits = []
        
        for i, (bit, basis) in enumerate(qubits_received_by_bob):
            b_basis = bob_bases[i]
            if b_basis == basis:
                b_bit = bit
            else:
                # 50% probability of projection onto orthogonal state
                b_bit = int(np.random.choice([0, 1]))
            bob_measured_bits.append(b_bit)
            
        # 4. Sifting phase: compare bases over public channel
        matching_bases_indices = [i for i in range(num_qubits) if alice_bases[i] == bob_bases[i]]
        
        alice_sifted = [alice_bits[i] for i in matching_bases_indices]
        bob_sifted = [bob_measured_bits[i] for i in matching_bases_indices]
        
        # 5. Calculate Quantum Bit Error Rate (QBER)
        errors = 0
        total_sifted = len(matching_bases_indices)
        for i in range(total_sifted):
            if alice_sifted[i] != bob_sifted[i]:
                errors += 1
                
        error_rate = (errors / total_sifted) if total_sifted > 0 else 0.0
        
        # Standard QKD security threshold is ~11% (Shor-Preskill / BB84 limit)
        is_secure = error_rate < 0.11 and total_sifted > 0
        eavesdropper_detected = error_rate >= 0.11
        
        sifted_key_str = "".join(str(b) for b in bob_sifted)
        
        # Privacy amplification / key distillation using cryptographic hash
        if is_secure and sifted_key_str:
            final_key = hashlib.sha256(sifted_key_str.encode('utf-8')).hexdigest()[:32].upper()
        else:
            final_key = "ABORTED_INSECURE_CHANNEL" if eavesdropper_detected else "INSUFFICIENT_KEY_LENGTH"
            
        return {
            "num_qubits": num_qubits,
            "alice_bits": alice_bits,
            "alice_bases": alice_bases,
            "bob_bases": bob_bases,
            "bob_measured_bits": bob_measured_bits,
            "matching_bases_indices": matching_bases_indices,
            "sifted_key": sifted_key_str,
            "error_rate": round(error_rate * 100, 2),
            "final_key": final_key,
            "channel_secure": is_secure,
            "eavesdropper_detected": eavesdropper_detected,
            "eavesdropper_present": eavesdropper_present,
            "eavesdropper_bases": eve_bases if eavesdropper_present else None,
            "eavesdropper_measured_bits": eve_measured_bits if eavesdropper_present else None,
            "simulation_type": "BB84 Quantum Key Distribution Educational Simulation"
        }

qkd_service = BB84Simulator()
