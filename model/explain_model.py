import joblib
import pandas as pd

from preprocessing import (
    load_data,
    feature_engineering
)


# =========================================================
# 1. LOAD TRAINED MODEL
# =========================================================

model = joblib.load(
    "model/churn_model.pkl"
)


# =========================================================
# 2. LOAD DATA
# =========================================================

df = load_data("data/dataset.csv")

df = feature_engineering(df)

X = df.drop("Churn", axis=1)


# =========================================================
# 3. GET PREPROCESSOR AND MODEL
# =========================================================

preprocessor = model.named_steps["preprocessor"]

classifier = model.named_steps["model"]


# =========================================================
# 4. GET FEATURE NAMES
# =========================================================

feature_names = preprocessor.get_feature_names_out()


# =========================================================
# 5. GET LOGISTIC REGRESSION COEFFICIENTS
# =========================================================

coefficients = classifier.coef_[0]


# =========================================================
# 6. CREATE FEATURE IMPORTANCE TABLE
# =========================================================

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": coefficients
})


# Absolute coefficient = strength of influence
importance_df["AbsoluteCoefficient"] = (
    importance_df["Coefficient"].abs()
)


# =========================================================
# 7. SORT FEATURES
# =========================================================

importance_df = importance_df.sort_values(
    by="AbsoluteCoefficient",
    ascending=False
)


# =========================================================
# 8. DISPLAY TOP FEATURES
# =========================================================

print("=" * 60)
print("TOP FEATURES IN LOGISTIC REGRESSION")
print("=" * 60)

print(
    importance_df[
        [
            "Feature",
            "Coefficient",
            "AbsoluteCoefficient"
        ]
    ].head(20).to_string(index=False)
)


# =========================================================
# 9. POSITIVE CHURN FEATURES
# =========================================================

positive_features = (
    importance_df[
        importance_df["Coefficient"] > 0
    ]
    .sort_values(
        by="Coefficient",
        ascending=False
    )
)


print("\n" + "=" * 60)
print("FEATURES ASSOCIATED WITH HIGHER CHURN PREDICTION")
print("=" * 60)

print(
    positive_features[
        ["Feature", "Coefficient"]
    ].head(10).to_string(index=False)
)


# =========================================================
# 10. NEGATIVE CHURN FEATURES
# =========================================================

negative_features = (
    importance_df[
        importance_df["Coefficient"] < 0
    ]
    .sort_values(
        by="Coefficient"
    )
)


print("\n" + "=" * 60)
print("FEATURES ASSOCIATED WITH LOWER CHURN PREDICTION")
print("=" * 60)

print(
    negative_features[
        ["Feature", "Coefficient"]
    ].head(10).to_string(index=False)
)