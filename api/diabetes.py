from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

predict_api = Blueprint("predict_api", __name__,
                        url_prefix='/api/predict')
api = Api(predict_api)
# Load the dataset
data = pd.read_csv('diabetes_dataset.csv')

# Split the data into features and labels
X = data.drop('Diabetic', axis=1)
y = data['Diabetic']

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train a logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Function to predict the chance of being diabetic
def predict_diabetes(height, weekly_sugar_intake, weekly_activity, weight, age):
    input_data = scaler.transform([[height, weekly_sugar_intake, weekly_activity, weight, age]])
    chance_of_diabetes = model.predict_proba(input_data)[:,1][0]
    return chance_of_diabetes

# Take user input
class Predict(Resource):
    def post(self):
        body=request.get_json()
        height = float(body.get("height"))
        weekly_sugar_intake = float(body.get("sugar"))
        weekly_activity = float(body.get("activity"))
        weight = float(body.get("weight"))
        age = float(body.get("age"))
        chance_of_diabetes = predict_diabetes(height, weekly_sugar_intake, weekly_activity, weight, age) 
        return (jsonify(f"Based on the provided data, the chance of being diabetic is: {chance_of_diabetes * 100:.2f}%"))

api.add_resource(Predict, '/')