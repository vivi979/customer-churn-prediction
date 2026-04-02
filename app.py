from flask import Flask, render_template, request, redirect
import pickle
import pandas as pd
import xgboost as xgb

app = Flask(__name__)

model = xgb.XGBClassifier()
model.load_model("churn_model.json")

cols = pickle.load(open("columns.pkl", "rb"))

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def login():
    return redirect('/dashboard')

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

    # encoding
    df = pd.get_dummies(df)

    # align columns
    df = df.reindex(columns=cols, fill_value=0)

    prediction = model.predict_proba(df)[0][1]

    return render_template('result.html', prediction=round(prediction, 2))

if __name__ == '__main__':
    app.run(debug=True)