import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Paths
DATA_PATH = "data/triage_data.csv"
MODEL_PATH = "models/triage_model.pkl"

# 1) Load data
df = pd.read_csv(DATA_PATH)

# 2) Features & target
X = df.drop(columns=["urgency_label"])
y = df["urgency_label"]

# 3) Encode target labels (Low/Medium/High/Critical -> 0/1/2/3)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 4) Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# 5) Train model (Decision Tree: simple + explainable)
model = DecisionTreeClassifier(max_depth=6, random_state=42)
model.fit(X_train, y_train)

# 6) Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# 7) Save model + encoder
os.makedirs("models", exist_ok=True)
joblib.dump({"model": model, "label_encoder": label_encoder}, MODEL_PATH)
print(f"\nModel saved to: {MODEL_PATH}")
