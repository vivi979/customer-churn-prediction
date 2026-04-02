# 🤖 Customer Churn Prediction Web App

## 📌 Objective

The goal of this project is to predict whether a customer is likely to churn using machine learning and provide an interactive web application where users can input customer details and get predictions.

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Flask
* HTML
* CSS
* Jupyter Notebook

## 📊 Project Overview

This is an end-to-end machine learning project that includes:

* Data preprocessing and cleaning
* Exploratory Data Analysis (EDA)
* Feature engineering
* Model training and evaluation
* Deployment using Flask web application

## 🧠 Model Details

* Model used: xgboost
* Model saved as: `churn_model.json`
* Preprocessing handled using: `columns.pkl`

## 🌐 Web Application Features

* User login interface
* Dashboard for entering customer details
* Real-time churn prediction
* Result display page

## 📁 Project Structure

```id="ps1"
CUST_CHURN/
│── app.py
│── churn_model.json
│── columns.pkl
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── result.html
│
├── static/
│   └── style.css
```

## ⚙️ How to Run the Project

1. Clone the repository
2. Install required libraries:

```bash id="ps2"
pip install -r requirements.txt
```

3. Run the application:

```bash id="ps3"
python app.py
```

4. Open in browser:

```id="ps4"
http://127.0.0.1:5000/
```

## 📈 Key Insights

* Customers with lower tenure are more likely to churn
* Monthly charges significantly impact churn
* Contract type plays a major role in customer retention

## 📁 Dataset

The dataset is not included due to size limitations.
You can use publicly available customer churn datasets from Kaggle.

## 🔗 Dataset Source

[( Kaggle dataset link here)](https://www.kaggle.com/competitions/playground-series-s6e3)

## 🚀 Future Improvements

* Integration with Power BI dashboards
* Deployment on cloud platforms
* Model optimization

## ✅ Conclusion

This project demonstrates an end-to-end machine learning workflow, from data analysis to deployment. It highlights the ability to build predictive models and deploy them in a real-world application.
