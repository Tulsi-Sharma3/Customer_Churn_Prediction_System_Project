import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score
)

from preprocessing import (
    load_data,
    feature_engineering
)


# =========================================================
# 1. LOAD DATA
# =========================================================

df = load_data("data/dataset.csv")

df = feature_engineering(df)


# =========================================================
# 2. FEATURES AND TARGET
# =========================================================

X = df.drop("Churn", axis=1)

y = df["Churn"].map({
    "No": 0,
    "Yes": 1
})


# =========================================================
# 3. TRAIN TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# =========================================================
# 4. LOAD TRAINED MODEL
# =========================================================

model = joblib.load(
    "model/churn_model.pkl"
)


# =========================================================
# 5. GET CHURN PROBABILITY
# =========================================================

probabilities = model.predict_proba(X_test)[:, 1]


# =========================================================
# 6. TEST DIFFERENT THRESHOLDS
# =========================================================

thresholds = [
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60
]


results = []


for threshold in thresholds:

    predictions = (
        probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    results.append({
        "Threshold": threshold,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    })


# =========================================================
# 7. DISPLAY RESULTS
# =========================================================

results_df = pd.DataFrame(results)

print("=" * 60)
print("THRESHOLD ANALYSIS")
print("=" * 60)

print(
    results_df.to_string(
        index=False
    )
)