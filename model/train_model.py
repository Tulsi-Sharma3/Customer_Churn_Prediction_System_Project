import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from preprocessing import (
    load_data,
    feature_engineering,
    create_preprocessor
)


# =========================================================
# 1. LOAD DATA
# =========================================================

DATA_PATH = "data/dataset.csv"

df = load_data(DATA_PATH)

print("=" * 60)
print("DATASET")
print("=" * 60)

print("Original shape:", df.shape)


# =========================================================
# 2. FEATURE ENGINEERING
# =========================================================

df = feature_engineering(df)

print("\nAfter feature engineering:", df.shape)


# =========================================================
# 3. SEPARATE FEATURES AND TARGET
# =========================================================

X = df.drop("Churn", axis=1)

y = df["Churn"].map({
    "No": 0,
    "Yes": 1
})


# =========================================================
# 4. TRAIN TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])


# =========================================================
# 5. CREATE PREPROCESSOR
# =========================================================

preprocessor = create_preprocessor(X_train)


# =========================================================
# 6. DEFINE MODELS
# =========================================================

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42
    ),

    "Decision Tree": DecisionTreeClassifier(
        max_depth=6,
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
}


# =========================================================
# 7. TRAIN AND EVALUATE MODELS
# =========================================================

results = {}

best_model = None
best_model_name = None
best_f1 = 0


for model_name, model in models.items():

    print("\n" + "=" * 60)
    print(model_name)
    print("=" * 60)

    # Create complete ML pipeline
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    # Train
    pipeline.fit(X_train, y_train)

    # Prediction
    y_pred = pipeline.predict(X_test)

    # Probability
    y_probability = pipeline.predict_proba(X_test)[:, 1]

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        y_probability
    )

    cm = confusion_matrix(
        y_test,
        y_pred
    )

    # Store results
    results[model_name] = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc
    }

    # Print results
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")

    print("\nConfusion Matrix:")
    print(cm)

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=["No Churn", "Churn"],
            zero_division=0
        )
    )

    # Select best model based on F1
    if f1 > best_f1:

        best_f1 = f1
        best_model = pipeline
        best_model_name = model_name


# =========================================================
# 8. MODEL COMPARISON
# =========================================================

print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

results_df = pd.DataFrame(results).T

print(results_df)


# =========================================================
# 9. BEST MODEL
# =========================================================

print("\n" + "=" * 60)
print("BEST MODEL")
print("=" * 60)

print("Best model:", best_model_name)
print("Best F1 Score:", round(best_f1, 4))


# =========================================================
# 10. SAVE BEST MODEL
# =========================================================

os.makedirs("model", exist_ok=True)

MODEL_PATH = "model/churn_model.pkl"

joblib.dump(
    best_model,
    MODEL_PATH
)

print("\nModel saved successfully!")
print("Location:", MODEL_PATH)