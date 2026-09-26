import re
from urllib.parse import urlparse

def extract_features(url):

    features = []

    # URL length
    features.append(len(url))

    # HTTPS
    features.append(1 if url.startswith("https") else 0)

    # Contains IP address
    features.append(
        1 if re.search(r"\d+\.\d+\.\d+\.\d+", url)
        else 0
    )

    # Number of dots
    features.append(url.count("."))

    # Number of hyphens
    features.append(url.count("-"))

    # Contains @
    features.append(1 if "@" in url else 0)

    # Contains suspicious words
    suspicious = [
        "login",
        "verify",
        "secure",
        "update",
        "bank",
        "paypal",
        "account"
    ]

    features.append(
        1 if any(word in url.lower() for word in suspicious)
        else 0
    )

    return features