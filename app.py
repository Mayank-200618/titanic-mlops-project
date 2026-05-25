import pandas as pd
import numpy as np
import pickle
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

print("Loading serialized Titanic prediction artifacts into API execution memory...")
with open('titanic_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('columns.json', 'r') as f:
    model_columns = json.load(f)


@app.route('/health', methods=['GET'])
def health_check():
    # Diagnostic endpoint used by active infrastructure monitoring tools.
    return jsonify({
        "status": "healthy",
        "service": "titanic-survival-prediction-engine",
        "engine_state": "active_listening"
    }), 200


@app.route('/predict', methods=['POST'])
def run_inference():
    # Receives JSON payload describing passenger features, aligns format,
    # and calculates survival metrics.
    try:
        payload = request.get_json()

        # Parse individual input characteristics from request body
        pclass   = int(payload['Pclass'])
        age      = float(payload['Age'])
        sibsp    = int(payload['SibSp'])
        parch    = int(payload['Parch'])
        fare     = float(payload['Fare'])
        sex      = payload['Sex'].lower()
        embarked = payload['Embarked'].upper()

        # Apply data transformation rules exactly matching original model parameters
        sex_male    = 1 if sex == 'male' else 0
        embarked_Q  = 1 if embarked == 'Q' else 0
        embarked_S  = 1 if embarked == 'S' else 0
        family_size = sibsp + parch + 1

        # Reconstruct into target dictionary structure
        passenger_profile = {
            'Pclass':      pclass,
            'Age':         age,
            'SibSp':       sibsp,
            'Parch':       parch,
            'Fare':        fare,
            'FamilySize':  family_size,
            'Sex_male':    sex_male,
            'Embarked_Q':  embarked_Q,
            'Embarked_S':  embarked_S
        }

        # Convert dictionary to DataFrame and align column order with model schema
        input_df = pd.DataFrame([passenger_profile])
        input_df = input_df[model_columns]

        # Extract classification probability matrices
        probabilities        = model.predict_proba(input_df)[0]
        survival_probability = probabilities[1]
        classification_verdict = 1 if survival_probability >= 0.5 else 0

        return jsonify({
            "model_classification_status": "success",
            "survival_probability":        round(float(survival_probability), 4),
            "prediction_verdict":          classification_verdict,
            "verdict_string":              "SURVIVED" if classification_verdict == 1 else "PERISHED"
        }), 200

    except Exception as error_msg:
        return jsonify({
            "model_classification_status": "failure",
            "error_log": str(error_msg)
        }), 400


if __name__ == '__main__':
    # Listen globally across port 5000 inside container instances
    app.run(host='0.0.0.0', port=5000)