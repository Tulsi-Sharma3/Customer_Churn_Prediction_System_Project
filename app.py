# import pandas as pd
# import numpy as np

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import StandardScaler

# from sklearn.linear_model import LogisticRegression

# from sklearn.metrics import accuracy_score
# from sklearn.metrics import confusion_matrix
# from sklearn.metrics import classification_report

# import pickle

# # Load Dataset
# df = pd.read_csv("customer_churn.csv")

# '''
# Data Cleaning :-
# Remove duplicates
# Handle missing values
# Convert TotalCharges into numeric
# Drop CustomerID
# '''

# df.drop("customerID",axis=1,inplace=True)

# df["TotalCharges"]=pd.to_numeric(df["TotalCharges"],errors="coerce")

# df.dropna(inplace=True)

# # Encode categorial feature :
# encoder=LabelEncoder()

# for col in df.columns:
#     if df[col].dtype=="object":
#         df[col]=encoder.fit_transform(df[col])

# # Split Data :
# X=df.drop("Churn",axis=1)
# y=df["Churn"]

# X_train,X_test,y_train,y_test=train_test_split(
# X,y,
# test_size=0.2,
# random_state=42
# )

# # Feature Scaling :
# scaler=StandardScaler()

# X_train=scaler.fit_transform(X_train)

# X_test=scaler.transform(X_test)

# # Train Model:
# model=LogisticRegression()

# model.fit(X_train,y_train)

# # Prediction :
# y_pred=model.predict(X_test)

# # Evaluation :
# print(accuracy_score(y_test,y_pred))

# print(confusion_matrix(y_test,y_pred))

# print(classification_report(y_test,y_pred))

# # Save Model :
# pickle.dump(model,open("churn_model.pkl","wb"))

# pickle.dump(scaler,open("scaler.pkl","wb"))

# # 

from flask import Flask, render_template, request

from model.prediction import (
    predict_customer,
    explain_customer,
    get_recommendation
)


# =========================================================
# CREATE FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# PREDICTION PAGE
# =========================================================

@app.route(
    "/predict",
    methods=["GET", "POST"]
)
def predict():

    if request.method == "POST":

        try:

            # ---------------------------------------------
            # Collect customer information
            # ---------------------------------------------

            customer = {

                "gender":
                    request.form["gender"],

                "SeniorCitizen":
                    int(
                        request.form["SeniorCitizen"]
                    ),

                "Partner":
                    request.form["Partner"],

                "Dependents":
                    request.form["Dependents"],

                "tenure":
                    int(
                        request.form["tenure"]
                    ),

                "PhoneService":
                    request.form["PhoneService"],

                "MultipleLines":
                    request.form["MultipleLines"],

                "InternetService":
                    request.form["InternetService"],

                "OnlineSecurity":
                    request.form["OnlineSecurity"],

                "OnlineBackup":
                    request.form["OnlineBackup"],

                "DeviceProtection":
                    request.form["DeviceProtection"],

                "TechSupport":
                    request.form["TechSupport"],

                "StreamingTV":
                    request.form["StreamingTV"],

                "StreamingMovies":
                    request.form["StreamingMovies"],

                "Contract":
                    request.form["Contract"],

                "PaperlessBilling":
                    request.form["PaperlessBilling"],

                "PaymentMethod":
                    request.form["PaymentMethod"],

                "MonthlyCharges":
                    float(
                        request.form["MonthlyCharges"]
                    ),

                "TotalCharges":
                    float(
                        request.form["TotalCharges"]
                    )
            }


            # ---------------------------------------------
            # ML Prediction
            # ---------------------------------------------

            result = predict_customer(
                customer
            )


            # ---------------------------------------------
            # Customer explanation
            # ---------------------------------------------

            reasons = explain_customer(
                customer
            )


            # ---------------------------------------------
            # Business recommendation
            # ---------------------------------------------

            recommendation = get_recommendation(
                result["prediction"],
                result["risk_level"],
                customer
            )


            # ---------------------------------------------
            # Send result to template
            # ---------------------------------------------

            return render_template(
                "result.html",
                customer=customer,
                prediction=result["prediction"],
                probability=result["probability"],
                risk_level=result["risk_level"],
                reasons=reasons,
                recommendation=recommendation
            )


        except ValueError:

            return (
                "Invalid input. "
                "Please check numeric values."
            )


        except Exception as e:

            print("ERROR:", e)

            return (
                "Something went wrong while "
                "processing the prediction."
            )


    return render_template(
        "predict.html"
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )