from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
import tldextract
import re

app = Flask(__name__)
CORS(app)

# Load model
model = joblib.load("phishing_model.pkl")

print("===================================")
print("MODEL FEATURES =", model.n_features_in_)
print("===================================")


# -----------------------------
# FEATURE EXTRACTION
# -----------------------------
def extract_features(url):
    features = []

    # URL Length
    features.append(len(url))

    # HTTPS
    features.append(1 if url.startswith("https") else 0)

    # @ symbol
    features.append(1 if "@" in url else 0)

    # Hyphen in domain
    domain = tldextract.extract(url).domain
    features.append(1 if "-" in domain else 0)

    # Number of dots
    features.append(url.count("."))

    # IP Address
    features.append(
        1 if re.search(r"\d+\.\d+\.\d+\.\d+", url)
        else 0
    )

    return features


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# PREDICTION
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({
                "error": "URL not provided"
            })

        url = data["url"].strip().lower()

        # ----------------------------------
        # RULE-BASED CHECKS
        # ----------------------------------

        phishing_keywords = [
            "login",
            "verify",
            "secure",
            "update",
            "account",
            "bank",
            "paypal",
            "reward",
            "winner",
            "free",
            "bonus",
            "gift",
            "claim",
            "urgent"
        ]

        if any(word in url for word in phishing_keywords):
            return jsonify({
                "prediction": "PHISHING"
            })

        if "@" in url:
            return jsonify({
                "prediction": "PHISHING"
            })

        if re.search(r"\d+\.\d+\.\d+\.\d+", url):
            return jsonify({
                "prediction": "PHISHING"
            })

        # ----------------------------------
        # ML MODEL
        # ----------------------------------

        features = extract_features(url)

        features_df = pd.DataFrame([features])

        prediction = model.predict(features_df)[0]

        result = "PHISHING" if prediction == 1 else "SAFE"

        return jsonify({
            "prediction": result
        })

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        })


# -----------------------------
# START SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)