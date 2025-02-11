import pandas as pd
import os
import time
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.metrics import accuracy_score, mean_squared_error
import numpy as np
from storage import file_storage
import datetime

MODEL_FOLDER = "models"
os.makedirs(MODEL_FOLDER, exist_ok=True)

# Define available models with their configurations
AVAILABLE_MODELS = {
    'linear_regression': {
        'class': LinearRegression,
        'type': 'regression',
        'parameters': {}
    },
    'logistic_regression': {
        'class': LogisticRegression,
        'type': 'classification',
        'parameters': {
            'C': 1.0,
            'max_iter': 1000
        }
    },
    'random_forest_regressor': {
        'class': RandomForestRegressor,
        'type': 'regression',
        'parameters': {
            'n_estimators': 100,
            'max_depth': None
        }
    },
    'random_forest_classifier': {
        'class': RandomForestClassifier,
        'type': 'classification',
        'parameters': {
            'n_estimators': 100,
            'max_depth': None
        }
    },
    'svr': {
        'class': SVR,
        'type': 'regression',
        'parameters': {
            'kernel': 'rbf',
            'C': 1.0
        }
    },
    'svc': {
        'class': SVC,
        'type': 'classification',
        'parameters': {
            'kernel': 'rbf',
            'C': 1.0
        }
    }
}

def get_available_model_names():
    """Return list of available models that can be trained"""
    return list(AVAILABLE_MODELS.keys())

def train_model(dataset_name, model_name, parameters=None):
    """
    Train a model using the specified dataset and parameters
    """
    try:
        if model_name not in AVAILABLE_MODELS:
            raise ValueError(f"Model {model_name} not available")
        
        # Get the dataset
        dataset_path = file_storage.get_uploaded_file(dataset_name)
        if not os.path.exists(dataset_path):
            raise ValueError(f"Dataset {dataset_name} not found")

        # Read the dataset
        df = pd.read_csv(dataset_path) if dataset_path.endswith(".csv") else pd.read_excel(dataset_path)
        
        # Assume last column is target variable
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        # Get model class and default parameters
        model_info = AVAILABLE_MODELS[model_name]
        model_class = model_info['class']
        model_params = model_info['parameters'].copy()

        # Update parameters if provided
        if parameters:
            model_params.update(parameters)

        # Split data for training and validation
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize and train the model
        model = model_class(**model_params)
        model.fit(X_train, y_train)

        # Calculate metrics
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        # Calculate additional metrics based on model type
        additional_metrics = {}
        if model_info['type'] == 'classification':
            y_pred = model.predict(X_test)
            additional_metrics['accuracy'] = accuracy_score(y_test, y_pred)
        else:  # regression
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            additional_metrics['rmse'] = np.sqrt(mse)

        # Create model filename and save
        model_filename = f"{model_name}_{dataset_name}_{datetime.datetime.now().strftime('%d%m%Y_%H%M%S')}"
        metrics = {
            'train_score': float(train_score),
            'test_score': float(test_score),
            'parameters': model_params,
            'model_type': model_info['type'],
            **additional_metrics
        }
        
        file_storage.save_model(model, model_filename, metrics)

        return True, {
            'model_filename': model_filename,
            'metrics': metrics
        }

    except Exception as e:
        print(f"Error during training: {e}")
        return False, str(e)
