import pandas as pd

data = pd.read_csv("phishing.csv")

print("Shape:", data.shape)
print("\nColumns:")
print(data.columns.tolist())