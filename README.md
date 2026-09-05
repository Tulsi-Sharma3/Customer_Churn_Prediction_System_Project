# Customer Churn Prediction System

A machine learning-based web application that predicts whether a customer is likely to churn and helps identify customers who may require retention efforts.

The system uses **Logistic Regression** for churn prediction and provides a **Flask-based web application** with MySQL integration, prediction history, risk analysis, and an interactive dashboard.

---

## 📌 Project Overview

Customer churn is a major challenge for businesses because losing existing customers can directly impact revenue.

This project analyzes customer information such as:

* Tenure
* Monthly charges
* Contract type
* Payment method
* Internet service
* Online security
* Technical support
* Other service-related attributes

The system predicts:

* **Churn / No Churn**
* **Churn Probability**
* **Risk Level**
* **Main Churn Risk Factors**
* **Recommended Retention Action**

Prediction results are stored in a **MySQL database**, allowing users to view, search, filter, and analyze previous predictions through the web application.

---

## 🚀 Key Features

* 🤖 Customer churn prediction using Machine Learning
* 📊 Churn probability estimation
* ⚠️ Low / Medium / High risk classification
* 🔍 Identification of important churn risk factors
* 💡 Customer retention recommendations
* 🗄️ MySQL database integration
* 📜 Prediction history
* 🔎 Search and filter prediction records
* 📋 Detailed prediction view
* 📈 Interactive dashboard
* 🍩 Churn distribution visualization
* 📊 Risk distribution visualization
* 📈 Prediction trend analysis
* 📌 Model performance metrics
* 🌐 Flask web application
* 🔐 Environment-based database configuration

---

## 🛠️ Technologies Used

### Programming Language

* Python

### Machine Learning & Data Analysis

* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn

### Machine Learning Model

* Logistic Regression

### Model Serialization

* Joblib
* Pickle

### Backend

* Flask

### Database

* MySQL
* MySQL Connector/Python

### Frontend

* HTML
* CSS
* JavaScript
* Chart.js

### Development Tools

* VS Code
* Jupyter Notebook
* Git
* GitHub

---

## 🔄 Machine Learning Workflow

```text
Customer Dataset
       ↓
Data Cleaning
       ↓
Data Preprocessing
       ↓
Feature Engineering
       ↓
Train-Test Split
       ↓
Feature Scaling & Encoding
       ↓
Logistic Regression
       ↓
Model Evaluation
       ↓
Model Serialization
       ↓
Flask Web Application
       ↓
Customer Churn Prediction
       ↓
MySQL Prediction Storage
       ↓
Dashboard & Analytics
```

---

## 📊 Dataset

The project uses the **IBM Telco Customer Churn Dataset**.

### Dataset Size

| Description                | Value |
| -------------------------- | ----: |
| Total Records              | 7,043 |
| Original Features          |    21 |
| Features After Engineering |    24 |
| Training Records           | 5,634 |
| Testing Records            | 1,409 |

### Important Dataset Columns

* gender
* SeniorCitizen
* Partner
* Dependents
* tenure
* PhoneService
* MultipleLines
* InternetService
* OnlineSecurity
* OnlineBackup
* DeviceProtection
* TechSupport
* StreamingTV
* StreamingMovies
* Contract
* PaperlessBilling
* PaymentMethod
* MonthlyCharges
* TotalCharges
* Churn

---

## ⚙️ Feature Engineering

Several additional features were created to improve customer-level analysis.

### AverageMonthlySpend

Calculates the customer's average spending based on total charges and tenure.

### TenureGroup

Groups customers according to their tenure to identify short-term and long-term customers.

### TotalServices

Represents the number of services used by a customer.

### HighMonthlyCharge

Identifies customers with relatively high monthly charges.

These engineered features help the model capture additional customer behavior patterns.

---

## 🎯 Target Variable

The target variable is:

```text
Churn
```

| Value   | Meaning                 |
| ------- | ----------------------- |
| Yes / 1 | Customer churn          |
| No / 0  | Customer does not churn |

The model performs binary classification to estimate the probability of customer churn.

---

## 🤖 Machine Learning Model

### Logistic Regression

Logistic Regression was selected as the primary classification algorithm because it is:

* Suitable for binary classification
* Efficient for structured/tabular data
* Relatively simple and interpretable
* Capable of producing probability estimates
* Useful for understanding feature impact

The trained model and preprocessing pipeline are serialized and used by the Flask application for real-time predictions.

---

## 📈 Model Performance

The Logistic Regression model was evaluated using multiple classification metrics.

| Metric    |      Score |
| --------- | ---------: |
| Accuracy  | **79.77%** |
| Precision | **64.88%** |
| Recall    | **51.87%** |
| F1 Score  | **57.65%** |
| ROC-AUC   | **84.18%** |

### Confusion Matrix

```text
[[930 105]
 [180 194]]
```

The **ROC-AUC score of 84.18%** indicates that the model has good ability to distinguish between customers who are likely to churn and customers who are likely to stay.

---

## ⚠️ Churn Risk Analysis

The application converts the predicted churn probability into a customer risk level.

```text
Churn Probability
       ↓
Risk Assessment
       ↓
Low / Medium / High
```

The system also provides customer-specific risk factors and recommendations.

### Important Churn Factors

The project highlights factors associated with increased churn risk, including:

* Fiber optic internet service
* Month-to-month contract
* Electronic check payment
* Short customer tenure
* High monthly charges
* Lack of online security
* Lack of technical support

---

## 🌐 Web Application Modules

### 1. Prediction

Users enter customer information through the Flask web interface.

The application returns:

* Churn prediction
* Churn probability
* Risk level
* Main risk factors
* Recommended action

### 2. Prediction History

Prediction results are stored in MySQL and can be viewed later.

### 3. Search & Filter

Users can search and filter historical prediction records.

### 4. Prediction Details

Each prediction has a dedicated detail page containing customer and prediction information.

### 5. Dashboard

The dashboard provides an overview of prediction activity and model information.

Dashboard includes:

* Total predictions
* Predicted churn customers
* No-churn customers
* High-risk customers
* Churn percentage
* Average churn probability
* Churn distribution
* Risk distribution
* Prediction trends
* Model information
* Model performance
* Important churn factors
* Recent predictions

---

## 🗄️ Database

MySQL is used to store prediction history.

The application stores information such as:

* Customer ID
* Prediction
* Churn probability
* Risk level
* Prediction timestamp

This allows prediction results to be tracked and analyzed over time.

---

## 📁 Project Structure

```text
Customer-Churn-Prediction/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
├── check_database.py
├── eda.py
│
├── data/
│
├── model/
│
├── notebooks/
│
├── screenshots/
│
├── tests/
│
├── utils/
│
├── database/
│   ├── db.py
│   ├── schema.sql
│   └── seed.sql
│
├── templates/
│   ├── index.html
│   ├── predict.html
│   ├── result.html
│   ├── history.html
│   ├── history_detail.html
│   └── dashboard.html
│
└── static/
    ├── css/
    └── js/
```

> The exact files inside folders such as `model/`, `utils/`, `tests/`, and `notebooks/` may vary depending on the development stage.

---

## 💻 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

### 2. Navigate to the Project

```bash
cd Customer-Churn-Prediction
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```powershell
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ MySQL Configuration

Create the required MySQL database:

```sql
CREATE DATABASE customer_churn_db;
```

Configure your database credentials using a `.env` file in the project root.

### `.env`

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_NAME=customer_churn_db
```

Replace `YOUR_MYSQL_PASSWORD` with your local MySQL password.

### Important

Do **not** upload `.env` to GitHub because it contains database credentials.

The `.gitignore` file should contain:

```text
venv/
__pycache__/
*.pyc
.env
```

---

## ▶️ Run the Application

Activate the virtual environment and run:

```bash
python app.py
```

Then open the local Flask application in your browser.

Typical Flask development URL:

```text
http://127.0.0.1:5000/
```

---

## 🧪 Testing

The main application modules can be tested through:

```text
Home
  ↓
Prediction
  ↓
Prediction Result
  ↓
Prediction History
  ↓
Prediction Details
  ↓
Dashboard
```

The project also includes database and testing-related files for validating application functionality.

---

## 📸 Screenshots

Project screenshots can be added to the `screenshots/` folder.

Recommended screenshots:

1. Home Page
2. Prediction Form
3. Prediction Result
4. Prediction History
5. Prediction Details
6. Dashboard
7. Database Records

---

## 🔮 Future Improvements

Possible future improvements include:

* Random Forest and XGBoost model comparison
* Hyperparameter tuning
* Automated model retraining
* Model comparison dashboard
* Advanced customer retention recommendation engine
* Email alerts for high-risk customers
* Authentication and role-based access
* Cloud deployment
* Explainable AI using SHAP
* Model monitoring and performance tracking

---

## 🎓 Project Outcome

This project demonstrates an end-to-end machine learning application covering:

```text
Data Collection
      ↓
Data Cleaning
      ↓
Feature Engineering
      ↓
Machine Learning
      ↓
Model Evaluation
      ↓
Model Serialization
      ↓
Flask Integration
      ↓
MySQL Integration
      ↓
Prediction History
      ↓
Dashboard Analytics
```

The system provides a practical approach for identifying customers at risk of churn and can help businesses take proactive customer-retention actions.

---

## 👩‍💻 Author

**Tulsi Sharma**

MCA | Python | SQL | Machine Learning | Flask

---

## ⭐ Project Highlights

* End-to-end Machine Learning project
* Real-time prediction through Flask
* MySQL database integration
* Customer risk classification
* Prediction history management
* Interactive analytics dashboard
* Model performance reporting
* Feature engineering
* Production-style project structure
* Environment-based configuration
