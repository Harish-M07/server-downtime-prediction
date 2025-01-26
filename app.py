from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained XGBoost model
MODEL_PATH = "XGBoost_model.pkl"  # Ensure this file is in the same directory as app.py
model = joblib.load(MODEL_PATH)

@app.route("/", methods=["GET"])
def home():
    """
    Default route to test if the API is running.
    """
    return jsonify({"message": "Welcome to the Server Downtime Predictor API!"})

@app.route("/predict", methods=["GET", "POST"])
def predict():
    """
    Predict downtime based on server metrics.
    - GET: Provide an instructional message.
    - POST: Accept JSON input and return a prediction.
    """
    if request.method == "GET":
        # Provide instructions for the /predict endpoint
        return jsonify({"message": "Send a POST request with server metrics to this endpoint."})
    
    if request.method == "POST":
        try:
            # Parse JSON input from the request
            data = request.get_json()
            
            # Validate input fields
            required_features = [
                "CPU_Usage", "Memory_Usage", "Disk_IO", "Temperature",
                "Network_Traffic", "Power_Consumption", "Fan_Speed",
                "Day", "Month", "Year", "Hour", "Minute"
            ]
            
            # Check if all required features are present in the input data
            for feature in required_features:
                if feature not in data:
                    return jsonify({"error": f"Missing required feature: {feature}"}), 400
            
            # Extract features from input data
            features = [
                data["CPU_Usage"],
                data["Memory_Usage"],
                data["Disk_IO"],
                data["Temperature"],
                data["Network_Traffic"],
                data["Power_Consumption"],
                data["Fan_Speed"],
                data["Day"],
                data["Month"],
                data["Year"],
                data["Hour"],
                data["Minute"]
            ]
            
            # Convert features to a NumPy array for prediction
            features_array = np.array(features).reshape(1, -1)
            
            # Predict downtime (output from the model)
            prediction = model.predict(features_array)
            
            # Return the prediction (assume the model returns a 0 or 1 indicating downtime)
            return jsonify({"prediction": "Downtime predicted" if prediction[0] == 1 else "No downtime predicted"})
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
