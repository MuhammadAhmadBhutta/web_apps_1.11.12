from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

# Load model & scaler
model_path = "dataset and models/kmeans_model.pkl"
scaler_path = "dataset and models/scaler.pkl"

kmeans = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Initialize Flask app
app = Flask(__name__)

# ---------------------------------------------
# ✅ Home route
# ---------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------------------------------------
# ✅ About route
# ---------------------------------------------
@app.route('/about')
def about():
    return render_template('about.html')

# ---------------------------------------------
# ✅ Predict route
# ---------------------------------------------
@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']

    if not file:
        return "No file uploaded!"

    df = pd.read_csv(file)

    # Columns you expect
    expected_columns = [
        'Total_Sales', 'Total_Profit', 'Total_Quantity',
        'Avg_Discount', 'Num_Orders', 'Num_Categories'
    ]

    if not all(col in df.columns for col in expected_columns):
        return f"Missing required columns: {expected_columns}"

    # Scale and predict
    X = df[expected_columns]
    X_scaled = scaler.transform(X)
    df['Cluster'] = kmeans.predict(X_scaled)

    # HTML table
    table_html = df.to_html(
        classes='table table-bordered table-striped',
        index=False
    )

    return render_template('results.html', table=table_html)

# ---------------------------------------------
# ✅ Run the app
# ---------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
