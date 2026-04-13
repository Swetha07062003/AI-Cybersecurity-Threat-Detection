import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# -----------------------------
# STEP 1: LOAD DATA
# -----------------------------
data = pd.read_csv("data/cyber_data.csv", header=None)

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

# -----------------------------
# STEP 2: CLEAN DATA
# -----------------------------
data = data.drop("difficulty", axis=1)

# Convert label
data["label"] = data["label"].apply(lambda x: 0 if x == "normal" else 1)

# Encode categorical
data = pd.get_dummies(data, columns=["protocol_type", "service", "flag"])

# -----------------------------
# STEP 3: SPLIT DATA
# -----------------------------
X = data.drop("label", axis=1)
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# STEP 4: TRAIN MODEL
# -----------------------------
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# -----------------------------
# STEP 5: EVALUATION
# -----------------------------
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# -----------------------------
# STEP 6: CONFUSION MATRIX
# -----------------------------
cm = confusion_matrix(y_test, y_pred)

plt.figure()
sns.heatmap(cm, annot=True, fmt="d")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.savefig("outputs/confusion_matrix.png")
plt.savefig("images/confusion_matrix.png")
plt.close()

# -----------------------------
# STEP 7: FEATURE IMPORTANCE
# -----------------------------
importances = model.feature_importances_
feature_names = X.columns

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values(by="Importance", ascending=False).head(10)

plt.figure()
sns.barplot(x="Importance", y="Feature", data=importance_df)
plt.title("Top 10 Important Features")

plt.savefig("outputs/feature_importance.png")
plt.savefig("images/feature_importance.png")
plt.close()

# -----------------------------
# STEP 8: SAVE MODEL
# -----------------------------
joblib.dump(model, "models/cyber_model.pkl")

# -----------------------------
# STEP 9: SIMULATION (VERY IMPORTANT)
# -----------------------------
print("\n--- Threat Detection Simulation ---")

sample = X_test.iloc[0:1]
prediction = model.predict(sample)

if prediction[0] == 1:
    print("🚨 ALERT: Cyber Threat Detected!")
else:
    print("✅ Normal Network Traffic")

print("\nProject Completed Successfully 🚀")