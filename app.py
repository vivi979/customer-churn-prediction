from flask import Flask, render_template, request, redirect
import pickle
import pandas as pd
import xgboost as xgb
import sqlite3

app = Flask(__name__)

model = xgb.XGBClassifier()
model.load_model("churn_model.json")

cols = pickle.load(open("columns.pkl", "rb"))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard_view')
def dashboard_view():
    return render_template('dashboard_view.html')
@app.route('/register')
def register_page():
    return render_template('register.html')
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('churn.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM employees 
    WHERE email=? AND password=?
    """, (email, password))

    user = cursor.fetchone()
    conn.close()

    if user:
        return redirect('/dashboard')
    else:
        return render_template('login.html', error="Invalid email or password ❌")

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    role = request.form['role']
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('churn.db')
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO employees (ename, email, password, role)
        VALUES (?, ?, ?, ?)
        """, (name, email, password, role))

        conn.commit()
        conn.close()

        return redirect('/login')

    except sqlite3.IntegrityError:
        conn.close()
        return "Email already exists ❌"
    except Exception as e:
        conn.close()
        return f"Registration failed: {str(e)}"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()

    df = pd.DataFrame([data])

    df['tenure'] = df['tenure'].astype(int)
    df['MonthlyCharges'] = df['MonthlyCharges'].astype(float)

    yes_no_cols = ['TechSupport', 'OnlineSecurity', 'HasInternet']
    for col in yes_no_cols:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0, '1':1, '0':0})

    df = pd.get_dummies(df)
    df = df.reindex(columns=cols, fill_value=0)

    prediction = model.predict_proba(df)[0][1]

    final_result = "Churn" if prediction > 0.5 else "No Churn"

    conn = sqlite3.connect('churn.db')
    cursor = conn.cursor()

    # Save customer data
    cursor.execute("""
    INSERT INTO customers 
    (cname, tenure, monthly_charges, contract, payment_method, internet_service, has_internet, tech_support, online_security)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('customerName'),
        int(data.get('tenure')),
        float(data.get('MonthlyCharges')),
        data.get('Contract'),
        data.get('PaymentMethod'),
        data.get('InternetService'),
        data.get('HasInternet'),
        data.get('TechSupport'),
        data.get('OnlineSecurity')
    ))

    customer_id = cursor.lastrowid

    # Save prediction
    cursor.execute("""
    INSERT INTO predictions (customer_id, prediction_result, churn_probability)
    VALUES (?, ?, ?)
    """, (customer_id, final_result, float(prediction)))

    # Save log
    cursor.execute("""
    INSERT INTO logs (employee_id, action)
    VALUES (?, ?)
    """, (1, "Predicted churn for customer: " + data.get('customerName')))

    conn.commit()
    conn.close()

    return render_template('result.html', prediction=round(prediction, 2), result=final_result)

if __name__ == '__main__':
    app.run(debug=True)