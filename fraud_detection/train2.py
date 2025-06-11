import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE
import pickle
import os

print("🔹 Loading data...")
df = pd.read_csv('data/application_data.csv')
print("✅ Data loaded:", df.shape)

# Drop columns with >40% missing values and fill remaining
df = df.dropna(axis=1, thresh=len(df)*0.6)
df = df.fillna(df.median(numeric_only=True))


# One-hot encode categoricals
df = pd.get_dummies(df, drop_first=True)
df = df.dropna()
print("✅ After preprocessing:", df.shape)

# Correlation matrix
corr_matrix = df.corr(numeric_only=True)
target_corr = corr_matrix['TARGET'].drop('TARGET')

# Features: high corr with target (>0.1), low pairwise corr (<0.5)
sorted_feats = target_corr[abs(target_corr) > 0.1].abs().sort_values(ascending=False).index.tolist()

selected_features = []
for feat in sorted_feats:
    if all(abs(corr_matrix.loc[feat, sel]) < 0.5 for sel in selected_features):
        selected_features.append(feat)
    if len(selected_features) >= 10:
        break

if not selected_features:
    print("❌ No features selected.")
    exit()

print("🔹 Selected features:", selected_features)

X = df[selected_features]
y = df['TARGET']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_res, y_train_res)

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("\n🔹 Classification Report:\n", classification_report(y_test, y_pred))
print("🔹 ROC AUC Score:", roc_auc_score(y_test, y_proba))

# Save model with feature metadata
os.makedirs('models', exist_ok=True)
with open('models/model.pkl', 'wb') as f:
    pickle.dump((model, selected_features), f)

print("✅ Model saved to models/model.pkl")
