import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

# Load your data
df = pd.read_csv("credit_card_transactions.csv")

# Drop non-numeric or unnecessary columns
df = df.select_dtypes(include=['int64', 'float64'])

# Split data
X = df.drop("IsFraud", axis=1)
y = df["IsFraud"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
with open("fraud_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as 'fraud_model.pkl'")
