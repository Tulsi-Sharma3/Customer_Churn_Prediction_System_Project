import joblib
import pandas as pd

from model.config import (
    CHURN_THRESHOLD,
    LOW_RISK_THRESHOLD,
    HIGH_RISK_THRESHOLD
)

from model.preprocessing import feature_engineering


# =========================================================
# LOAD MODEL
# =========================================================

MODEL_PATH = "model/churn_model.pkl"

model = joblib.load(MODEL_PATH)


# =========================================================
# RISK LEVEL
# =========================================================

def get_risk_level(probability):
    """
    Convert churn probability into a business risk level.
    """

    if probability < LOW_RISK_THRESHOLD:
        return "Low"

    elif probability < HIGH_RISK_THRESHOLD:
        return "Medium"

    else:
        return "High"


# =========================================================
# PREDICTION
# =========================================================

def predict_customer(customer_data):
    """
    Predict churn for a new customer.

    customer_data should contain only the original
    customer features.

    Engineered features are created automatically.
    """

    # -----------------------------------------------------
    # Convert dictionary to DataFrame
    # -----------------------------------------------------

    customer_df = pd.DataFrame(
        [customer_data]
    )

    # -----------------------------------------------------
    # Feature engineering
    # -----------------------------------------------------

    customer_df = feature_engineering(
        customer_df
    )

    # -----------------------------------------------------
    # Get churn probability
    # -----------------------------------------------------

    probability = model.predict_proba(
        customer_df
    )[0][1]

    # -----------------------------------------------------
    # Apply optimized threshold
    # -----------------------------------------------------

    prediction = int(
        probability >= CHURN_THRESHOLD
    )

    # -----------------------------------------------------
    # Convert prediction to text
    # -----------------------------------------------------

    if prediction == 1:
        churn_prediction = "Churn"
    else:
        churn_prediction = "No Churn"

    # -----------------------------------------------------
    # Risk level
    # -----------------------------------------------------

    risk_level = get_risk_level(
        probability
    )

    return {
        "prediction": churn_prediction,
        "probability": probability,
        "risk_level": risk_level
    }


# =========================================================
# BUSINESS RECOMMENDATION
# =========================================================

def get_recommendation(
    prediction,
    risk_level,
    customer_data
):
    """
    Generate a simple business recommendation.
    """

    if prediction == "Churn":

        if risk_level == "High":

            return (
                "Immediate retention action recommended. "
                "Consider contacting the customer with a "
                "personalized retention offer."
            )

        elif risk_level == "Medium":

            return (
                "Customer should be monitored and considered "
                "for a targeted retention campaign."
            )

        else:

            return (
                "Customer shows some churn signals. "
                "Continue monitoring customer engagement."
            )

    else:

        if risk_level == "High":

            return (
                "Prediction is currently No Churn, but the "
                "customer has elevated risk indicators. "
                "Continue monitoring."
            )

        elif risk_level == "Medium":

            return (
                "Customer appears relatively stable. "
                "Continue customer engagement."
            )

        else:

            return (
                "Customer appears low risk. "
                "Continue regular engagement."
            )


# =========================================================
# CUSTOMER-SPECIFIC EXPLANATION
# =========================================================

def explain_customer(customer_data):
    """
    Generate simple business-oriented explanations.

    These are model-informed risk signals, not causal
    explanations.
    """

    reasons = []

    # -----------------------------------------------------
    # Contract
    # -----------------------------------------------------

    if customer_data.get("Contract") == "Month-to-month":

        reasons.append(
            "Month-to-month contract is associated "
            "with higher churn risk."
        )

    elif customer_data.get("Contract") == "Two year":

        reasons.append(
            "Long-term contract is associated "
            "with lower churn risk."
        )

    # -----------------------------------------------------
    # Tenure
    # -----------------------------------------------------

    tenure = customer_data.get(
        "tenure",
        0
    )

    if tenure <= 12:

        reasons.append(
            "Customer has relatively short tenure."
        )

    elif tenure >= 48:

        reasons.append(
            "Customer has long tenure, which is "
            "generally associated with lower churn."
        )

    # -----------------------------------------------------
    # Monthly Charges
    # -----------------------------------------------------

    monthly_charges = customer_data.get(
        "MonthlyCharges",
        0
    )

    if monthly_charges >= 80:

        reasons.append(
            "Monthly charges are relatively high."
        )

    # -----------------------------------------------------
    # Internet Service
    # -----------------------------------------------------

    if customer_data.get(
        "InternetService"
    ) == "Fiber optic":

        reasons.append(
            "Fiber optic customers show higher "
            "observed churn in this dataset."
        )

    # -----------------------------------------------------
    # Payment Method
    # -----------------------------------------------------

    if customer_data.get(
        "PaymentMethod"
    ) == "Electronic check":

        reasons.append(
            "Electronic check customers show higher "
            "observed churn in this dataset."
        )

    # -----------------------------------------------------
    # Online Security
    # -----------------------------------------------------

    if customer_data.get(
        "OnlineSecurity"
    ) == "No":

        reasons.append(
            "Customer does not have online security."
        )

    # -----------------------------------------------------
    # Tech Support
    # -----------------------------------------------------

    if customer_data.get(
        "TechSupport"
    ) == "No":

        reasons.append(
            "Customer does not have technical support."
        )

    # -----------------------------------------------------
    # Default explanation
    # -----------------------------------------------------

    if not reasons:

        reasons.append(
            "No strong individual risk indicator "
            "was identified from the selected rules."
        )

    return reasons