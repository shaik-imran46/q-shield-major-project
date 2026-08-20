import numpy as np
import time
import math
from typing import Dict, Any, List

class QuantumRandomNumberGenerator:
    """
    Educational Quantum Random Number Generator (QRNG) Simulator.
    Simulates single-qubit and multi-qubit Hadamard gate superposition and measurement.
    |0> --[ H ]-- (1/sqrt(2))(|0> + |1>) --[ M ]--> 0 or 1 with P=0.5
    """
    def __init__(self):
        self.simulation_name = "Q-Shield Hadamard-Superposition QRNG Simulator"
        
    def _simulate_qubit_measurement(self, bias: float = 0.0) -> int:
        """
        Simulates applying Hadamard gate H = 1/sqrt(2) * [[1, 1], [1, -1]] to state |0>,
        resulting in superposition (|0> + |1>)/sqrt(2), followed by measurement.
        """
        # State vector [alpha, beta]
        state = np.array([1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)], dtype=np.complex128)
        # Born rule probability of measuring |0> is |alpha|^2 = 0.5
        prob_0 = np.abs(state[0])**2 - bias
        prob_0 = max(0.0, min(1.0, prob_0))
        
        # Hardware-independent stochastic collapse
        random_roll = np.random.uniform(0.0, 1.0)
        return 0 if random_roll < prob_0 else 1

    def generate_random_bits(self, num_bits: int = 32, num_qubits: int = 4) -> Dict[str, Any]:
        start_time = time.perf_counter()
        
        bits = []
        for _ in range(num_bits):
            # In a multi-qubit register, each qubit undergoes Hadamard & measurement
            qubit_bits = [self._simulate_qubit_measurement() for _ in range(num_qubits)]
            # XOR parity reduction across register
            bit = 0
            for b in qubit_bits:
                bit ^= b
            bits.append(bit)
            
        bitstring = "".join(str(b) for b in bits)
        
        # Convert bitstring to bytes & hex
        padding_len = (8 - (len(bits) % 8)) % 8
        padded_bits = bits + [0] * padding_len
        byte_values = []
        for i in range(0, len(padded_bits), 8):
            chunk = padded_bits[i:i+8]
            val = 0
            for bit in chunk:
                val = (val << 1) | bit
            byte_values.append(val)
            
        hex_string = bytes(byte_values).hex()
        
        # Calculate Shannon entropy
        count_0 = bits.count(0)
        count_1 = bits.count(1)
        p0 = count_0 / len(bits) if len(bits) > 0 else 0.5
        p1 = count_1 / len(bits) if len(bits) > 0 else 0.5
        
        entropy = 0.0
        if p0 > 0:
            entropy -= p0 * math.log2(p0)
        if p1 > 0:
            entropy -= p1 * math.log2(p1)
            
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        
        return {
            "bitstring": bitstring,
            "hex_string": hex_string,
            "byte_values": byte_values,
            "entropy": round(entropy, 4),
            "num_bits": num_bits,
            "num_qubits": num_qubits,
            "execution_time_ms": round(elapsed_ms, 2),
            "simulation_type": "Quantum Randomness Simulation (Hadamard Superposition & Measurement)"
        }

qrng_service = QuantumRandomNumberGenerator()
