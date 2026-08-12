"""
utils.py
Small helper functions used by app.py — input parsing/validation and
formatting so app.py stays readable.
"""

FIELDS = [
    ("rainfall_mm", "Rainfall (last 24h, mm)", 0, 500),
    ("water_level_m", "River Water Level (m)", 0, 15),
    ("river_discharge_cms", "River Discharge (cubic m/s)", 0, 2000),
    ("temperature_c", "Temperature (°C)", -10, 55),
    ("humidity_pct", "Humidity (%)", 0, 100),
    ("soil_moisture_pct", "Soil Moisture (%)", 0, 100),
    ("elevation_m", "Elevation (m)", 0, 3000),
    ("drainage_quality", "Drainage Quality (1=poor, 5=excellent)", 1, 5),
    ("historical_floods_5yr", "Floods in Last 5 Years", 0, 10),
    ("population_density", "Population Density (people/km²)", 0, 20000),
]


def parse_form(form) -> dict:
    """Convert raw form strings into a validated float/int dict."""
    features = {}
    for key, _, low, high in FIELDS:
        raw = form.get(key, "")
        value = float(raw)
        value = max(low, min(high, value))  # clamp into a sane range
        features[key] = value
    return features


def risk_badge_color(label: str) -> str:
    return {"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"}.get(label, "#64748b")
