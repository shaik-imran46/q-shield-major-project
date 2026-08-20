import numpy as np
from typing import List, Dict, Any
from app.ml.dataset import FEATURE_NAMES
from app.ml.model import SecurityRiskClassifier

class SHAPExplainabilityEngine:
    """
    Explainable AI (XAI) Engine providing Shapley Additive Explanations (SHAP)
    for model transparency and regulatory accountability.
    """
    def __init__(self, model: SecurityRiskClassifier):
        self.model = model
        self.feature_labels = {
            "message_frequency": "Message Frequency (msgs/min)",
            "frequency_ratio": "Frequency Surge Ratio",
            "auth_failure": "Authentication Failure",
            "unauthorized_agent": "Unauthorized Agent Indicator",
            "integrity_failure": "Message Integrity Failure",
            "replay_detected": "Replay Attack Indicator",
            "mitm_indicator": "MITM Interception Indicator",
            "trust_score": "Agent Trust Score",
            "hash_mismatch": "SHA-256 Checksum Mismatch",
            "interval_jitter": "Communication Interval Jitter",
            "payload_tampering": "Payload Tampering Flag"
        }

    def explain_instance(self, x: np.ndarray) -> List[Dict[str, Any]]:
        """
        Computes exact additive feature contributions (SHAP values) for input sample x.
        phi_i = w_i * (x_i - mean_i) / std_i
        """
        x_scaled = (x - self.model.mean_) / self.model.scale_
        linear_contribs = self.model.weights_ * x_scaled
        
        # Scale linear contributions to 0-100 risk score point domain
        scaling_factor = 10.0
        shap_scores = linear_contribs * scaling_factor
        
        explanations = []
        for i, name in enumerate(FEATURE_NAMES):
            raw_val = x[i]
            contrib = float(round(shap_scores[i], 2))
            
            # Format observed value for human presentation
            if name in ["auth_failure", "unauthorized_agent", "integrity_failure", "replay_detected", "mitm_indicator", "hash_mismatch", "payload_tampering"]:
                val_str = "True (Detected)" if raw_val == 1 else "False (Clean)"
            elif name == "trust_score":
                val_str = f"{raw_val:.1f} / 100"
            elif name == "message_frequency":
                val_str = f"{raw_val:.1f} msgs/min"
            elif name == "frequency_ratio":
                val_str = f"{raw_val:.2f}x Baseline"
            elif name == "interval_jitter":
                val_str = f"{raw_val:.1f} ms"
            else:
                val_str = str(raw_val)
                
            direction = "INCREASES_RISK" if contrib > 0.5 else ("DECREASES_RISK" if contrib < -0.5 else "NEUTRAL")
            
            explanations.append({
                "feature_id": name,
                "feature_name": self.feature_labels.get(name, name),
                "observed_value": val_str,
                "contribution": contrib,
                "direction": direction,
                "abs_importance": abs(contrib)
            })
            
        # Sort descending by absolute impact
        explanations.sort(key=lambda item: item["abs_importance"], reverse=True)
        return explanations
