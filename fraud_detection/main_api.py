# from fastapi import FastAPI, HTTPException, Query
# import pandas as pd
# import pickle

# # Load model and selected features
# with open("models/model.pkl", "rb") as f:
#     model, selected_features = pickle.load(f)

# # Load and preprocess the full dataset once at startup
# print("🔹 Loading and preprocessing data...")
# df = pd.read_csv("data/application_data.csv")
# df = df.dropna(axis=1, thresh=len(df)*0.6)
# df = df.fillna(df.median(numeric_only=True))
# df = pd.get_dummies(df, drop_first=True)
# df = df.dropna()

# # Create FastAPI app
# app = FastAPI()

# @app.get("/fraud_detection/predict")
# def predict(customer_id: int = Query(..., description="Customer ID to check for fraud")):
#     if customer_id not in df['SK_ID_CURR'].values:
#         raise HTTPException(status_code=404, detail=f"Customer ID {customer_id} not found.")

#     row = df[df['SK_ID_CURR'] == customer_id]

#     # Ensure all selected features are in the row
#     missing_cols = [col for col in selected_features if col not in row.columns]
#     if missing_cols:
#         raise HTTPException(status_code=422, detail=f"Missing required features: {missing_cols}")

#     x = row[selected_features]
#     prediction = model.predict(x)[0]
#     result = "fraud" if prediction == 1 else "not fraud"

#     return {
#         "prediction": int(prediction),
#         "result": result
#     }

from fastapi import FastAPI, HTTPException
import pandas as pd
import pickle

# Load model and selected features
with open("models/model.pkl", "rb") as f:
    model, selected_features = pickle.load(f)

# Load and preprocess the full dataset once at startup
print("🔹 Loading and preprocessing data...")
df = pd.read_csv("data/application_data.csv")
df = df.dropna(axis=1, thresh=len(df)*0.6)
df = df.fillna(df.median(numeric_only=True))
df = pd.get_dummies(df, drop_first=True)
df = df.dropna()

# Create FastAPI app
app = FastAPI()

@app.get("/fraud_detection/predict/{customer_id}")
def predict(customer_id: int):
    if customer_id not in df['SK_ID_CURR'].values:
        raise HTTPException(status_code=404, detail=f"Customer ID {customer_id} not found.")

    row = df[df['SK_ID_CURR'] == customer_id]

    # Ensure all selected features are in the row
    missing_cols = [col for col in selected_features if col not in row.columns]
    if missing_cols:
        raise HTTPException(status_code=422, detail=f"Missing required features: {missing_cols}")

    x = row[selected_features]
    prediction = model.predict(x)[0]
    isFraud = True if prediction == 1 else False

    return {
        "customerId": customer_id,
        "isFraud": isFraud
    }
