import numpy as np
import pandas as pd
from typing import Tuple, List, Dict, Any

FEATURE_NAMES = [
    "message_frequency",
    "frequency_ratio",
    "auth_failure",
    "unauthorized_agent",
    "integrity_failure",
    "replay_detected",
    "mitm_indicator",
    "trust_score",
    "hash_mismatch",
    "interval_jitter",
    "payload_tampering"
]

def generate_synthetic_security_dataset(n_samples: int = 1200) -> Tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    """
    Generates a realistic synthetic training dataset representing multi-agent cyber-risk telemetry.
    Classes: 0 = Benign (Low Risk), 1 = Suspicious (Medium Risk), 2 = Malicious (High Risk)
    """
    np.random.seed(42)
    rows = []
    
    for _ in range(n_samples):
        scenario = np.random.choice(["normal", "flood", "mitm", "replay", "tampering", "unauthorized", "combined"],
                                    p=[0.40, 0.10, 0.12, 0.12, 0.10, 0.10, 0.06])
        
        if scenario == "normal":
            msg_freq = np.random.normal(5.0, 1.2)
            msg_freq = max(1.0, msg_freq)
            norm_freq = 5.0
            freq_ratio = msg_freq / norm_freq
            auth_fail = 0
            unauthorized = 0
            integ_fail = 0
            replay = 0
            mitm = 0
            trust = np.random.uniform(90.0, 99.0)
            hash_mismatch = 0
            jitter = np.random.exponential(15.0)
            payload_tamper = 0
            risk_label = 0 # Low Risk
            
        elif scenario == "flood":
            msg_freq = np.random.normal(52.0, 8.0)
            norm_freq = 5.0
            freq_ratio = msg_freq / norm_freq
            auth_fail = 0
            unauthorized = 0
            integ_fail = 0
            replay = 0
            mitm = 0
            trust = np.random.uniform(70.0, 85.0)
            hash_mismatch = 0
            jitter = np.random.exponential(30.0)
            payload_tamper = 0
            risk_label = 1 # Medium Risk
            
        elif scenario == "mitm":
            msg_freq = np.random.normal(8.0, 2.0)
            norm_freq = 5.0
            freq_ratio = msg_freq / norm_freq
            auth_fail = int(np.random.choice([0, 1], p=[0.2, 0.8]))
            unauthorized = 0
            integ_fail = 1
            replay = 0
            mitm = 1
            trust = np.random.uniform(30.0, 60.0)
            hash_mismatch = 1
            jitter = np.random.exponential(350.0)
            payload_tamper = 1
            risk_label = 2 # High Risk
            
        elif scenario == "replay":
            msg_freq = np.random.normal(12.0, 3.0)
            norm_freq = 5.0
            freq_ratio = msg_freq / norm_freq
            auth_fail = 0
            unauthorized = 0
            integ_fail = 0
            replay = 1
            mitm = 0
            trust = np.random.uniform(50.0, 75.0)
            hash_mismatch = 0
            jitter = np.random.exponential(50.0)
            payload_tamper = 0
            risk_label = 1 # Medium Risk
            
        elif scenario == "tampering":
            msg_freq = np.random.normal(5.5, 1.5)
            norm_freq = 5.0
            freq_ratio = msg_freq / norm_freq
            auth_fail = 0
            unauthorized = 0
            integ_fail = 1
            replay = 0
            mitm = 0
            trust = np.random.uniform(60.0, 80.0)
            hash_mismatch = 1
            jitter = np.random.exponential(25.0)
            payload_tamper = 1
            risk_label = 1 # Medium Risk
            
        elif scenario == "unauthorized":
            msg_freq = np.random.normal(6.0, 2.0)
            norm_freq = 5.0
            freq_ratio = msg_freq / norm_freq
            auth_fail = 1
            unauthorized = 1
            integ_fail = 0
            replay = 0
            mitm = 0
            trust = np.random.uniform(10.0, 30.0)
            hash_mismatch = 0
            jitter = np.random.exponential(40.0)
            payload_tamper = 0
            risk_label = 1 # Medium/High Risk
            
        else: # combined attack
            msg_freq = np.random.normal(48.0, 10.0)
            norm_freq = 5.0
            freq_ratio = msg_freq / norm_freq
            auth_fail = 1
            unauthorized = 1
            integ_fail = 1
            replay = 1
            mitm = 1
            trust = np.random.uniform(5.0, 25.0)
            hash_mismatch = 1
            jitter = np.random.exponential(450.0)
            payload_tamper = 1
            risk_label = 2 # High Risk
            
        rows.append([
            msg_freq, freq_ratio, auth_fail, unauthorized, integ_fail,
            replay, mitm, trust, hash_mismatch, jitter, payload_tamper, risk_label
        ])
        
    df = pd.DataFrame(rows, columns=FEATURE_NAMES + ["risk_label"])
    X = df[FEATURE_NAMES].values
    y = df["risk_label"].values
    return X, y, df
