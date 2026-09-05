import os


# ==========================================
# MODEL CONFIGURATION
# ==========================================

MODEL_PATH = "model/churn_model.pkl"

CHURN_THRESHOLD = 0.35


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DB_HOST = os.getenv(
    "DB_HOST",
    "localhost"
)

DB_USER = os.getenv(
    "DB_USER",
    "root"
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD",
    "4567"
)

DB_NAME = os.getenv(
    "DB_NAME",
    "customer_churn_db"
)