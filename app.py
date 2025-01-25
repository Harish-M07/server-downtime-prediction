from flask import Flask, request, jsonify
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = joblib.load("best_model.pkl")  # Replace with your model filename

# Define the prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from request
        data = request.get_json()
        
        # Convert input into a NumPy array for the model
        input_data = np.array([[
            data['CPU_Usage'],
            data['Memory_Usage'],
            data['Disk_IO'],
            data['Temperature'],
            data['Network_Traffic'],
            data['Power_Consumption'],
            data['Fan_Speed'],
            data['Day'],
            data['Month'],
            data['Year'],
            data['Hour'],
            data['Minute']
        ]])

        # Make prediction
        prediction = model.predict(input_data)

        # Respond with the prediction result
        result = "Downtime Likely" if prediction[0] == 1 else "No Downtime"
        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
