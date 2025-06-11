import pandas as pd
import pickle

# Load model and selected features
with open("models/model.pkl", "rb") as f:
    model, selected_features = pickle.load(f)

# Load and preprocess data
print("🔹 Loading and preprocessing data...")
df = pd.read_csv("data/application_data.csv")
df = df.dropna(axis=1, thresh=len(df)*0.6)
df = df.fillna(df.median(numeric_only=True))
df = pd.get_dummies(df, drop_first=True)
df = df.dropna()

# Predict for specific SK_ID_CURR
sk_id = 100047
 # Replace as needed

if sk_id not in df['SK_ID_CURR'].values:
    print(f"❌ SK_ID_CURR {sk_id} not found.")
else:
    row = df[df['SK_ID_CURR'] == sk_id]
    missing = [col for col in selected_features if col not in row.columns]
    if missing:
        print(f"❌ Required columns missing in row: {missing}")
    else:
        x = row[selected_features]  # KEEP as DataFrame to retain column names
        prediction = model.predict(x)[0]
        print(f"🔍 Prediction for SK_ID_CURR {sk_id}: {prediction}")
        print(f"✅ Return to Tool: {bool(prediction)}")




# import pandas as pd
# import pickle

# # Load model and selected features
# with open("models/model.pkl", "rb") as f:
#     model, selected_features = pickle.load(f)

# # Load and preprocess data
# print("🔹 Loading and preprocessing data...")
# df = pd.read_csv("data/application_data.csv")
# df = df.dropna(axis=1, thresh=len(df)*0.6)
# df = df.fillna(df.median(numeric_only=True))
# df = pd.get_dummies(df, drop_first=True)
# df = df.dropna()

# # Predict for specific SK_ID_CURR
# sk_id = 100493  # Replace as needed

# if sk_id not in df['SK_ID_CURR'].values:
#     print(f"❌ SK_ID_CURR {sk_id} not found.")
# else:
#     row = df[df['SK_ID_CURR'] == sk_id]
#     missing = [col for col in selected_features if col not in row.columns]
#     if missing:
#         print(f"❌ Required columns missing in row: {missing}")
#     else:
#         x = row[selected_features]
#         prediction = model.predict(x)[0]
#         print(f"🔍 Prediction for SK_ID_CURR {sk_id}: {prediction}")
#         print(f"✅ Return to Tool: {bool(prediction)}")

# # Suggest SK_ID_CURR values with prediction = 1
# print("\n🔍 Suggesting SK_ID_CURR values with predicted value 1 (True):")
# suggested = []
# for _, row in df.iterrows():
#     if all(col in row for col in selected_features):
#         x_test = pd.DataFrame([row[selected_features]])
#         if model.predict(x_test)[0] == 1:
#             suggested.append(int(row['SK_ID_CURR']))
#         if len(suggested) >= 5:  # limit to 5 examples
#             break

# if suggested:
#     print("✅ Suggested SK_ID_CURR values:", suggested)
# else:
#     print("⚠️ No SK_ID_CURR values found with prediction 1.")
