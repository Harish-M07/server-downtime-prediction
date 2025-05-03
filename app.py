import numpy as np
import joblib
from flask import Flask, request, jsonify
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

# Load the trained model
model = joblib.load("Random_Forest_model.pkl")

# Initialize Flask app
app = Flask(__name__)

# Define the Prometheus metric
downtime_prediction_metric = Gauge("server_downtime_prediction", "Probability of server downtime")


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Server Downtime Predictor API!"})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Convert input data into numpy array
        features = np.array([[data["CPU_Usage"], data["Memory_Usage"], data["Disk_IO"],
                              data["Temperature"], data["Network_Traffic"],
                              data["Power_Consumption"], data["Fan_Speed"],
                              data["Day"], data["Month"], data["Year"],
                              data["Hour"], data["Minute"]]])

        # Get the probability of downtime
        prediction = model.predict_proba(features)[:, 1][0]  # Probability of failure

        # ✅ Update Prometheus metric
        downtime_prediction_metric.set(prediction)

        return jsonify({"downtime_probability": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Prometheus Metrics Endpoint
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
