"""
app.py
Flask entry point for the Flood Risk Prediction web app.

Run with:
    python app/app.py
Then open http://127.0.0.1:5000/
"""

import os
import sys

# Make imports work whether this file is run directly, imported by gunicorn
# as "app:app" from inside app/, or imported from the project root.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request
from predict import predict_risk, FEATURE_COLS
from utils import parse_form, risk_badge_color, FIELDS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, "templates"),
    static_folder=os.path.join(PROJECT_ROOT, "static"),
)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", fields=FIELDS)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        features = parse_form(request.form)
    except (TypeError, ValueError):
        return render_template(
            "index.html",
            fields=FIELDS,
            error="Please fill in every field with a valid number.",
        )

    label, confidence, probabilities = predict_risk(features)

    return render_template(
        "result.html",
        risk_level=label,
        confidence=confidence,
        probabilities=probabilities,
        color=risk_badge_color(label),
        inputs=features,
        fields=FIELDS,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
