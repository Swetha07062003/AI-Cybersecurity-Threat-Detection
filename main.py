# =========================================
# AI CYBERSECURITY THREAT DETECTION SYSTEM
# FINAL COMPLETE VERSION (ALL 3 GRAPHS)
# =========================================

import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# =========================================
# CREATE REQUIRED FOLDERS
# =========================================
os.makedirs("models", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("images", exist_ok=True)

# =========================================
# LOAD DATASET
# =========================================
print("Loading dataset...")
data = pd.read_csv("data/cyber_data.csv", header=None)

# =========================================
# COLUMN NAMES
# =========================================
columns = [
"duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment",
"urgent","hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted",
"num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds",
"is_host_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
"rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate",
"dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate",
"dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
"dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate",
"label","difficulty"
]

data.columns = columns

# =========================================
# DATA CLEANING
# =========================================
print("Cleaning data...")
data = data.drop("difficulty", axis=1)

# Convert label to binary
data["label"] = data["label"].apply(lambda x: 0 if x == "normal" else 1)

# One-hot encoding
data = pd.get_dummies(data, columns=["protocol_type", "service", "flag"])

# =========================================
# SPLIT DATA
# =========================================
print("Splitting dataset...")
X = data.drop("label", axis=1)
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================================
# TRAIN MODEL
# =========================================
print("Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# =========================================
# MODEL EVALUATION
# =========================================
print("Evaluating model...")
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# =========================================
# 1️⃣ CONFUSION MATRIX HEATMAP
# =========================================
print("Saving Confusion Matrix...")

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.tight_layout()
plt.savefig("outputs/confusion_matrix.png", dpi=300)
plt.savefig("images/confusion_matrix.png", dpi=300)
plt.close()

print("✅ Confusion Matrix saved!")

# =========================================
# 2️⃣ FEATURE IMPORTANCE GRAPH
# =========================================
print("Saving Feature Importance Graph...")

feature_importance = pd.Series(model.feature_importances_, index=X.columns)

top_features = feature_importance.nlargest(10)
top_features = top_features.sort_values()

plt.figure(figsize=(10, 7))
top_features.plot(kind='barh')

plt.title("Top 10 Important Features")
plt.xlabel("Importance Score")

# Fix label visibility
plt.yticks(fontsize=8)
plt.subplots_adjust(left=0.35)

plt.tight_layout()
plt.savefig("outputs/feature_importance.png", dpi=300)
plt.savefig("images/feature_importance.png", dpi=300)
plt.close()

print("✅ Feature Importance graph saved!")

# =========================================
# 3️⃣ CORRELATION HEATMAP (SECOND HEATMAP)
# =========================================
print("Saving Correlation Heatmap...")

# Reduce features for readability
corr_data = X.iloc[:, :15]

corr_matrix = corr_data.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, cmap="coolwarm")

plt.title("Feature Correlation Heatmap")

plt.tight_layout()
plt.savefig("outputs/correlation_heatmap.png", dpi=300)
plt.savefig("images/correlation_heatmap.png", dpi=300)
plt.close()

print("✅ Correlation Heatmap saved!")

# =========================================
# SAVE MODEL
# =========================================
print("Saving model...")
joblib.dump(model, "models/cyber_model.pkl")

# =========================================
# THREAT SIMULATION
# =========================================
print("\n--- Threat Detection Simulation ---")

sample = X_test.iloc[0:1]
prediction = model.predict(sample)

if prediction[0] == 1:
    print("🚨 ALERT: Cyber Threat Detected!")
else:
    print("✅ Normal Network Traffic")

# =========================================
# FINAL MESSAGE
# =========================================
print("\n✅ PROJECT COMPLETED SUCCESSFULLY 🚀")
print("📊 3 Graphs saved in 'outputs/' and 'images/' folders")
print("🤖 Model saved in 'models/'")