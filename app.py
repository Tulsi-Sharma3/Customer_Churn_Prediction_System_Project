
from flask import Flask, render_template, request

from model.prediction import (
    predict_customer,
    explain_customer,
    get_recommendation
)

from database.db import get_db_connection


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
            # Save prediction to MySQL
            # ---------------------------------------------

            # connection = get_db_connection()

            # cursor = connection.cursor()

            # insert_query = """
            #     INSERT INTO prediction_history (
            #         customer_id,
            #         prediction,
            #         churn_probability,
            #         risk_level
            #     )
            #     VALUES (%s, %s, %s, %s)
            # """

            # customer_id = request.form.get(
            #     "customer_id",
            #     "CUS-UNKNOWN"
            # )

            # cursor.execute(
            #     insert_query,
            #     (
            #         customer_id,
            #         result["prediction"],
            #         result["probability"],
            #         result["risk_level"]
            #     )
            # )

            # connection.commit()

            # cursor.close()
            # connection.close()

            # ---------------------------------------------
            # Customer Explanation
            # ---------------------------------------------

            reasons = explain_customer(
                customer
            )


            # ---------------------------------------------
            # Business Recommendation
            # ---------------------------------------------

            recommendation = get_recommendation(
                result["prediction"],
                result["risk_level"],
                customer
            )


            # ---------------------------------------------
            # SAVE PREDICTION TO MYSQL
            # ---------------------------------------------

            connection = get_db_connection()

            if connection:

                cursor = connection.cursor()

                insert_query = """
                    INSERT INTO prediction_history (

                        customer_id,

                        gender,
                        senior_citizen,
                        partner,
                        dependents,

                        tenure,

                        phone_service,
                        multiple_lines,
                        internet_service,

                        online_security,
                        online_backup,
                        device_protection,
                        tech_support,

                        streaming_tv,
                        streaming_movies,

                        contract,
                        paperless_billing,
                        payment_method,

                        monthly_charges,
                        total_charges,

                        prediction,
                        churn_probability,
                        risk_level

                    )

                    VALUES (

                        %s,
                        %s, %s, %s, %s,
                        %s,
                        %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s,
                        %s, %s, %s,
                        %s, %s,
                        %s, %s, %s

                    )
                """


                values = (

                    "WEB-" + str(
                        request.form.get(
                            "customer_id",
                            "UNKNOWN"
                        )
                    ),

                    customer["gender"],
                    customer["SeniorCitizen"],
                    customer["Partner"],
                    customer["Dependents"],

                    customer["tenure"],

                    customer["PhoneService"],
                    customer["MultipleLines"],
                    customer["InternetService"],

                    customer["OnlineSecurity"],
                    customer["OnlineBackup"],
                    customer["DeviceProtection"],
                    customer["TechSupport"],

                    customer["StreamingTV"],
                    customer["StreamingMovies"],

                    customer["Contract"],
                    customer["PaperlessBilling"],
                    customer["PaymentMethod"],

                    customer["MonthlyCharges"],
                    customer["TotalCharges"],

                    result["prediction"],
                    result["probability"],
                    result["risk_level"]
                )


                cursor.execute(
                    insert_query,
                    values
                )

                connection.commit()

                cursor.close()
                connection.close()

                print(
                    "Prediction saved successfully."
                )

            else:

                print(
                    "WARNING: Database connection failed."
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


        # ---------------------------------------------
        # Invalid input
        # ---------------------------------------------

        except ValueError:

            return (
                "Invalid input. "
                "Please check numeric values."
            )


        # ---------------------------------------------
        # Other errors
        # ---------------------------------------------

        except Exception as e:

            print(
                "ERROR:",
                e
            )

            return (
                "Something went wrong while "
                "processing the prediction."
            )


    # ---------------------------------------------
    # GET REQUEST
    # ---------------------------------------------

    return render_template(
        "predict.html"
    )

# =========================================================
# PREDICTION HISTORY
# =========================================================

@app.route("/history")
def history():

    connection = None
    cursor = None

    try:

        # Get filter values
        search = request.args.get("search", "").strip()
        prediction_filter = request.args.get(
            "prediction",
            ""
        )
        risk_filter = request.args.get(
            "risk",
            ""
        )

        # Connect to MySQL
        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        # Base query
        query = """
            SELECT
                id,
                customer_id,
                prediction,
                churn_probability,
                risk_level,
                prediction_time
            FROM prediction_history
            WHERE 1=1
        """

        parameters = []

        # ---------------------------------------------
        # Customer ID search
        # ---------------------------------------------

        if search:

            query += """
                AND customer_id LIKE %s
            """

            parameters.append(
                "%" + search + "%"
            )

        # ---------------------------------------------
        # Prediction filter
        # ---------------------------------------------

        if prediction_filter:

            query += """
                AND prediction = %s
            """

            parameters.append(
                prediction_filter
            )

        # ---------------------------------------------
        # Risk filter
        # ---------------------------------------------

        if risk_filter:

            query += """
                AND risk_level = %s
            """

            parameters.append(
                risk_filter
            )

        # ---------------------------------------------
        # Latest predictions first
        # ---------------------------------------------

        query += """
            ORDER BY prediction_time DESC
        """

        cursor.execute(
            query,
            tuple(parameters)
        )

        predictions = cursor.fetchall()

        return render_template(
            "history.html",
            predictions=predictions,
            search=search,
            prediction_filter=prediction_filter,
            risk_filter=risk_filter
        )

    except Exception as e:

        print("HISTORY ERROR:", e)

        return (
            "Unable to load prediction history."
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# =========================================================
# PREDICTION DETAILS
# =========================================================

@app.route("/history/<int:prediction_id>")
def history_detail(prediction_id):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT *
            FROM prediction_history
            WHERE id = %s
        """

        cursor.execute(
            query,
            (prediction_id,)
        )

        prediction = cursor.fetchone()

        # ---------------------------------------------
        # Prediction not found
        # ---------------------------------------------

        if not prediction:

            return "Prediction record not found.", 404

        # ---------------------------------------------
        # Generate customer information
        # ---------------------------------------------

        customer = {

            "gender":
                prediction["gender"],

            "SeniorCitizen":
                prediction["senior_citizen"],

            "Partner":
                prediction["partner"],

            "Dependents":
                prediction["dependents"],

            "tenure":
                prediction["tenure"],

            "PhoneService":
                prediction["phone_service"],

            "MultipleLines":
                prediction["multiple_lines"],

            "InternetService":
                prediction["internet_service"],

            "OnlineSecurity":
                prediction["online_security"],

            "OnlineBackup":
                prediction["online_backup"],

            "DeviceProtection":
                prediction["device_protection"],

            "TechSupport":
                prediction["tech_support"],

            "StreamingTV":
                prediction["streaming_tv"],

            "StreamingMovies":
                prediction["streaming_movies"],

            "Contract":
                prediction["contract"],

            "PaperlessBilling":
                prediction["paperless_billing"],

            "PaymentMethod":
                prediction["payment_method"],

            "MonthlyCharges":
                prediction["monthly_charges"],

            "TotalCharges":
                prediction["total_charges"]
        }

        # ---------------------------------------------
        # Explanation
        # ---------------------------------------------

        reasons = explain_customer(
            customer
        )

        # ---------------------------------------------
        # Recommendation
        # ---------------------------------------------

        recommendation = get_recommendation(
            prediction["prediction"],
            prediction["risk_level"],
            customer
        )

        return render_template(

            "history_detail.html",

            prediction=prediction,

            customer=customer,

            reasons=reasons,

            recommendation=recommendation
        )

    except Exception as e:

        print(
            "HISTORY DETAIL ERROR:",
            e
        )

        return (
            "Unable to load prediction details."
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        # -------------------------------------------------
        # Total predictions
        # -------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM prediction_history
        """)

        total_predictions = cursor.fetchone()["total"]


        # -------------------------------------------------
        # Churn predictions
        # -------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM prediction_history
            WHERE prediction = 'Churn'
        """)

        churn_predictions = cursor.fetchone()["total"]

        # -------------------------------------------------
        # Churn Distribution
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                prediction,
                COUNT(*) AS total
            FROM prediction_history
            GROUP BY prediction
        """)

        churn_distribution = cursor.fetchall()


        # -------------------------------------------------
        # Risk Distribution
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                risk_level,
                COUNT(*) AS total
            FROM prediction_history
            GROUP BY risk_level
        """)

        risk_distribution = cursor.fetchall()

        # -------------------------------------------------
        # No churn predictions
        # -------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM prediction_history
            WHERE prediction = 'No Churn'
        """)

        no_churn_predictions = cursor.fetchone()["total"]


        # -------------------------------------------------
        # High-risk customers
        # -------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM prediction_history
            WHERE risk_level = 'High'
        """)

        high_risk = cursor.fetchone()["total"]


        # -------------------------------------------------
        # Average churn probability
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                COALESCE(
                    AVG(churn_probability),
                    0
                ) AS average_probability
            FROM prediction_history
        """)

        average_probability = cursor.fetchone()[
            "average_probability"
        ]


        # -------------------------------------------------
        # Churn percentage
        # -------------------------------------------------

        if total_predictions > 0:

            churn_percentage = (
                churn_predictions /
                total_predictions
            ) * 100

        else:

            churn_percentage = 0


        # -------------------------------------------------
        # Recent predictions
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                customer_id,
                prediction,
                churn_probability,
                risk_level,
                prediction_time
            FROM prediction_history
            ORDER BY prediction_time DESC
            LIMIT 10
        """)

        recent_predictions = cursor.fetchall()

        # -------------------------------------------------
        # Prediction Trend
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                DATE(prediction_time) AS prediction_date,
                COUNT(*) AS total
            FROM prediction_history
            GROUP BY DATE(prediction_time)
            ORDER BY DATE(prediction_time)
        """)

        prediction_trend = cursor.fetchall()

        print("TREND DATA:", prediction_trend)

        # -------------------------------------------------
        # Model performance
        # -------------------------------------------------

        model_metrics = {
            "accuracy": 0.7977,
            "precision": 0.6488,
            "recall": 0.5187,
            "f1_score": 0.5765,
            "roc_auc": 0.8418
        }


        # -------------------------------------------------
        # Important churn factors
        # -------------------------------------------------

        churn_factors = [
            "Fiber optic internet service",
            "Month-to-month contract",
            "Electronic check payment",
            "Short customer tenure",
            "High monthly charges",
            "No online security",
            "No technical support"
        ]


        return render_template(
            "dashboard.html",

            total_predictions=total_predictions,

            churn_predictions=churn_predictions,

            # risk_distribution=risk_distribution,

            no_churn_predictions=no_churn_predictions,

            high_risk=high_risk,

            average_probability=(
                average_probability * 100
            ),

            churn_percentage=churn_percentage,

            recent_predictions=recent_predictions,

            model_metrics=model_metrics,

            churn_factors=churn_factors,

            churn_distribution=churn_distribution,

            risk_distribution=risk_distribution,
            prediction_trend=prediction_trend
        )


    except Exception as e:

        print(
            "DASHBOARD ERROR:",
            e
        )

        return (
            "Unable to load dashboard."
        )


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )