import numpy as np
from typing import Dict, Any, List
from app.database.schemas import SyntheticSecurityEvent
from app.ml.model import ml_model
from app.ml.explainability import SHAPExplainabilityEngine

class MLRiskPredictor:
    def __init__(self):
        self.model = ml_model
        self.explainer = SHAPExplainabilityEngine(self.model)

    def extract_features(self, event: SyntheticSecurityEvent) -> np.ndarray:
        msg_freq = float(event.message_frequency)
        norm_freq = float(max(event.normal_frequency, 1.0))
        freq_ratio = msg_freq / norm_freq
        auth_fail = 1.0 if not event.authenticated else 0.0
        unauthorized = 1.0 if (not event.authorized or "Unknown" in event.source_agent or "Rogue" in event.source_agent) else 0.0
        integ_fail = 1.0 if (not event.integrity_valid or event.file_tampering_detected) else 0.0
        replay = 1.0 if event.replay_detected else 0.0
        mitm = 1.0 if event.mitm_indicator else 0.0
        trust = float(event.trust_score)
        
        orig_h = event.original_file_hash
        curr_h = event.current_file_hash
        hash_mismatch = 1.0 if (orig_h and curr_h and orig_h != curr_h) or event.file_tampering_detected else 0.0
        
        jitter = 400.0 if mitm else (35.0 if replay else 12.0)
        payload_tamper = 1.0 if (integ_fail or mitm or hash_mismatch) else 0.0
        
        return np.array([
            msg_freq, freq_ratio, auth_fail, unauthorized, integ_fail,
            replay, mitm, trust, hash_mismatch, jitter, payload_tamper
        ], dtype=float)

    def predict(self, event: SyntheticSecurityEvent) -> Dict[str, Any]:
        x = self.extract_features(event)
        prob = self.model.predict_risk_probability(x)
        ml_risk_score = round(prob * 100.0, 2)
        explanations = self.explainer.explain_instance(x)
        
        return {
            "ml_risk_probability": round(prob, 4),
            "ml_risk_score": ml_risk_score,
            "feature_importances": self.model.get_feature_importances(),
            "shap_explanations": explanations
        }

ml_predictor = MLRiskPredictor()
