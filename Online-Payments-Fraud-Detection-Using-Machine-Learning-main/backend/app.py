from flask import Flask, request, render_template
import joblib
import numpy as np
import os
import joblib

app = Flask(__name__)

base_dir = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(base_dir, "fraud_model.pkl")

# Safe convert function (🔥 empty value fix)
def get_val(x):
    return float(x) if x else 0


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict")
def predict_page():
    return render_template("predict.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        # ✅ FULL 8 FEATURES (PDF dataset)
        data = [
            get_val(request.form.get("step")),
            get_val(request.form.get("type")),
            get_val(request.form.get("amount")),
            get_val(request.form.get("oldbalanceOrg")),
            get_val(request.form.get("newbalanceOrig")),
            get_val(request.form.get("oldbalanceDest")),
            get_val(request.form.get("newbalanceDest")),
            0  # isFlaggedFraud default
        ]

        prediction = model = joblib.load(model_path)
        result = "Fraud" if prediction == 1 else "Not Fraud"

        return render_template("submit.html", result=result)

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)