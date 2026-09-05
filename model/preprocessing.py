import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_data(file_path):
    """
    Load the customer churn dataset.
    """
    df = pd.read_csv(file_path)
    return df


def feature_engineering(df, monthly_charge_median=None):
    """
    Perform data cleaning and feature engineering.

    monthly_charge_median:
        Median MonthlyCharges calculated from training data.
        It is used to create HighMonthlyCharge consistently
        during both training and prediction.
    """

    df = df.copy()

    # -------------------------------------------------
    # 1. Convert TotalCharges to numeric
    # -------------------------------------------------

    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    # -------------------------------------------------
    # 2. Create AverageMonthlySpend
    # -------------------------------------------------

    df["AverageMonthlySpend"] = np.where(
        df["tenure"] > 0,
        df["TotalCharges"] / df["tenure"],
        df["MonthlyCharges"]
    )

    # -------------------------------------------------
    # 3. Create TenureGroup
    # -------------------------------------------------

    df["TenureGroup"] = pd.cut(
        df["tenure"],
        bins=[-1, 12, 24, 48, np.inf],
        labels=[
            "0-12 Months",
            "13-24 Months",
            "25-48 Months",
            "49+ Months"
        ]
    )

    # -------------------------------------------------
    # 4. Create TotalServices
    # -------------------------------------------------

    service_columns = [
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]

    df["TotalServices"] = (
        df[service_columns]
        .apply(
            lambda row: sum(
                1 for value in row
                if value == "Yes"
            ),
            axis=1
        )
    )

    # -------------------------------------------------
    # 5. Create HighMonthlyCharge
    # -------------------------------------------------

    if monthly_charge_median is None:

        # Used during training.
        monthly_charge_median = (
            df["MonthlyCharges"].median()
        )

    df["HighMonthlyCharge"] = (
        df["MonthlyCharges"] >= monthly_charge_median
    ).astype(int)

    # -------------------------------------------------
    # 6. Remove customerID
    # -------------------------------------------------

    if "customerID" in df.columns:
        df.drop(
            "customerID",
            axis=1,
            inplace=True
        )

    return df


def create_preprocessor(X):
    """
    Create numerical and categorical preprocessing pipelines.
    """

    numerical_features = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_features = X.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # -------------------------------------------------
    # Numerical pipeline
    # -------------------------------------------------

    numerical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median")
            ),
            (
                "scaler",
                StandardScaler()
            )
        ]
    )

    # -------------------------------------------------
    # Categorical pipeline
    # -------------------------------------------------

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent")
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                )
            )
        ]
    )

    # -------------------------------------------------
    # Combine pipelines
    # -------------------------------------------------

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                numerical_pipeline,
                numerical_features
            ),
            (
                "cat",
                categorical_pipeline,
                categorical_features
            )
        ]
    )

    return preprocessor