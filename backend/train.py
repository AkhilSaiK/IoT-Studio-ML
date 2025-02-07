import pandas as pd
import os
import time
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, mean_squared_error
import numpy as np

MODEL_FOLDER = "models"
os.makedirs(MODEL_FOLDER, exist_ok=True)

MODELS = {
    "random_forest_classifier": RandomForestClassifier,
    "logistic_regression_classifier": LogisticRegression,
    "random_forest_regressor": RandomForestRegressor,
    "linear_regression": LinearRegression,
    "svm_classifier": SVC
}

def train_model(dataset_path, model_type, parameters):
    df = pd.read_csv(dataset_path) if dataset_path.endswith(".csv") else pd.read_excel(dataset_path)
    
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if model_type not in MODELS:
        return None, "Invalid model type"

    model = MODELS[model_type](**parameters) if parameters else MODELS[model_type]()
    model.fit(X_train, y_train)

    if "classifier" in model_type:
        y_pred = model.predict(X_test)
        metric = accuracy_score(y_test, y_pred)
        metric_name = "accuracy"
    else:
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        metric = rmse
        metric_name = "rmse"

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    model_filename = f"{model_type}_{os.path.basename(dataset_path)}_{timestamp}.pkl"
    model_path = os.path.join(MODEL_FOLDER, model_filename)
    joblib.dump(model, model_path)

    return model_filename, {
        "metric_name": metric_name,
        "metric_value": metric,
        "metric_description": "Root Mean Squared Error (in dollars)" if metric_name == "rmse" else "Accuracy Score (0-1)"
    }
