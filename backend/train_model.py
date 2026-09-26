import pandas as pd
import joblib
import tldextract
import re
from sklearn.ensemble import RandomForestClassifier

def extract_features(url):
    features = []

    features.append(len(url))
    features.append(1 if url.startswith("https") else 0)
    features.append(1 if "@" in url else 0)

    domain = tldextract.extract(url).domain
    features.append(1 if "-" in domain else 0)

    features.append(url.count("."))

    features.append(
        1 if re.match(r"^\d+\.\d+\.\d+\.\d+", url) else 0
    )

    return features

data = pd.read_csv("url_dataset.csv")

X = data["url"].apply(extract_features)
X = pd.DataFrame(X.tolist())

y = data["label"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "phishing_model.pkl")

print("Model trained successfully!")