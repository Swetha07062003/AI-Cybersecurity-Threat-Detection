import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# =========================
# LOAD DATASET
# =========================
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

# =========================
# PREPROCESSING
# =========================
data.drop("difficulty", axis=1, inplace=True)

data["label"] = data["label"].apply(lambda x: 0 if x == "normal" else 1)

data = pd.get_dummies(data, columns=["protocol_type","service","flag"])

# =========================
# SPLIT DATA
# =========================
X = data.drop("label", axis=1)
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# TRAIN MODEL
# =========================
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# =========================
# EVALUATION
# =========================
acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)

# =========================
# CREATE FOLDERS
# =========================
os.makedirs("outputs", exist_ok=True)
os.makedirs("models", exist_ok=True)

# =========================
# CONFUSION MATRIX
# =========================
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("outputs/confusion_matrix.png")
plt.close()

# =========================
# FEATURE IMPORTANCE
# =========================
importances = model.feature_importances_
features = X.columns

feat_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances
}).sort_values(by="Importance", ascending=False).head(10)

plt.figure(figsize=(8,5))
sns.barplot(x="Importance", y="Feature", data=feat_df)
plt.title("Top Important Features")
plt.savefig("outputs/feature_importance.png")
plt.close()

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, "models/cyber_model.pkl")

print("✅ Project Completed Successfully!")
print("📊 Outputs saved in 'outputs/' folder")
print("🤖 Model saved in 'models/' folder")