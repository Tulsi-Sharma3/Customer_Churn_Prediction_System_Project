import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/dataset.csv")

print("=" * 50)
print("DATASET INFORMATION")
print("=" * 50)

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nDataset Info:")
df.info()

print("\n" + "=" * 50)
print("MISSING VALUES")
print("=" * 50)

print(df.isnull().sum())

print("\n" + "=" * 50)
print("DUPLICATES")
print("=" * 50)

print("Duplicate rows:", df.duplicated().sum())
print("Duplicate customer IDs:", df["customerID"].duplicated().sum())

print("\n" + "=" * 50)
print("TARGET DISTRIBUTION")
print("=" * 50)

print(df["Churn"].value_counts())

print("\nTarget Percentage:")
print(df["Churn"].value_counts(normalize=True) * 100)

print("\n" + "=" * 50)
print("STATISTICAL SUMMARY")
print("=" * 50)

print(df.describe())

print("\n" + "=" * 50)
print("CATEGORICAL COLUMNS")
print("=" * 50)

categorical_columns = df.select_dtypes(include="object").columns

print(categorical_columns.tolist())

print("\n" + "=" * 50)
print("TOTAL CHARGES CHECK")
print("=" * 50)

print("Original datatype:", df["TotalCharges"].dtype)

total_charges_numeric = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

print(
    "Invalid/blank TotalCharges:",
    total_charges_numeric.isna().sum()
)

# -----------------------------
# CHURN DISTRIBUTION
# -----------------------------

churn_counts = df["Churn"].value_counts()

plt.figure(figsize=(6, 4))

plt.bar(
    churn_counts.index,
    churn_counts.values
)

plt.title("Customer Churn Distribution")
plt.xlabel("Churn")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.show()


# -----------------------------
# CONTRACT VS CHURN
# -----------------------------

contract_churn = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
) * 100

print("\nChurn Rate by Contract:")
print(contract_churn)

contract_churn.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Churn Rate by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Percentage")

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()


# -----------------------------
# INTERNET SERVICE VS CHURN
# -----------------------------

internet_churn = pd.crosstab(
    df["InternetService"],
    df["Churn"],
    normalize="index"
) * 100

print("\nChurn Rate by Internet Service:")
print(internet_churn)

internet_churn.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Churn Rate by Internet Service")
plt.xlabel("Internet Service")
plt.ylabel("Percentage")

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()


# -----------------------------
# PAYMENT METHOD VS CHURN
# -----------------------------

payment_churn = pd.crosstab(
    df["PaymentMethod"],
    df["Churn"],
    normalize="index"
) * 100

print("\nChurn Rate by Payment Method:")
print(payment_churn)

payment_churn.plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("Churn Rate by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Percentage")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.show()


print("\nEDA completed successfully!")