"""
predict.py
Loads the trained Random Forest bundle and exposes a single predict_risk()
function used by app.py.
"""

import os
import joblib
import numpy as np
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "flood_model.pkl")

_bundle = joblib.load(MODEL_PATH)
_model = _bundle["model"]
_label_encoder = _bundle["label_encoder"]
FEATURE_COLS = _bundle["feature_cols"]


def predict_risk(features: dict):
    """
    features: dict with keys matching FEATURE_COLS
    returns: (risk_label: str, confidence: float, probabilities: dict)
    """
    x = pd.DataFrame([[features[col] for col in FEATURE_COLS]], columns=FEATURE_COLS)
    pred_idx = _model.predict(x)[0]
    probs = _model.predict_proba(x)[0]

    label = _label_encoder.inverse_transform([pred_idx])[0]
    confidence = float(np.max(probs))
    prob_dict = {
        cls: round(float(p) * 100, 1)
        for cls, p in zip(_label_encoder.classes_, probs)
    }

    return label, round(confidence * 100, 1), prob_dict
