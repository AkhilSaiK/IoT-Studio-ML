import os
import json
import joblib
from typing import Dict, List, BinaryIO

UPLOAD_FOLDER = 'uploads'
MODELS_FOLDER = 'models'
MODEL_PARAMS_FILE = os.path.join(MODELS_FOLDER, 'model_params.json')

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODELS_FOLDER, exist_ok=True)

def save_uploaded_file(file: BinaryIO, filename: str) -> bool:
    """Save an uploaded file to the uploads directory"""
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def get_uploaded_file(filename: str) -> str:
    """Get path to an uploaded file"""
    return os.path.join(UPLOAD_FOLDER, filename)

def get_all_uploads() -> List[str]:
    """Get list of all uploaded files"""
    return [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]

def save_model(model, model_filename: str, metrics: Dict) -> bool:
    """Save a trained model and its metrics"""
    try:
        # Save model file
        model_path = os.path.join(MODELS_FOLDER, f"{model_filename}.joblib")
        joblib.dump(model, model_path)

        # Save metrics
        metrics_path = os.path.join(MODELS_FOLDER, f"{model_filename}_metrics.json")
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=2)

        return True
    except Exception as e:
        print(f"Error saving model: {e}")
        return False

def load_model(model_name: str):
    """Load a trained model"""
    try:
        model_path = os.path.join(MODELS_FOLDER, f"{model_name}.joblib")
        return joblib.load(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def get_model_metrics(model_name: str) -> Dict:
    """Get metrics for a trained model"""
    try:
        metrics_path = os.path.join(MODELS_FOLDER, f"{model_name}_metrics.json")
        with open(metrics_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading model metrics: {e}")
        return {}

def get_all_models() -> List[str]:
    """Get list of all trained models"""
    return [f.replace('.joblib', '') for f in os.listdir(MODELS_FOLDER) 
            if f.endswith('.joblib')]

def save_model_params(model_name: str, parameters: Dict) -> None:
    """Save model parameters"""
    try:
        params = {}
        if os.path.exists(MODEL_PARAMS_FILE):
            with open(MODEL_PARAMS_FILE, 'r') as f:
                params = json.load(f)
        
        params[model_name] = parameters
        
        with open(MODEL_PARAMS_FILE, 'w') as f:
            json.dump(params, f, indent=2)
    except Exception as e:
        print(f"Error saving model parameters: {e}")

def get_model_params(model_name: str) -> Dict:
    """Get parameters for a model"""
    try:
        if os.path.exists(MODEL_PARAMS_FILE):
            with open(MODEL_PARAMS_FILE, 'r') as f:
                params = json.load(f)
                return params.get(model_name, {})
        return {}
    except Exception as e:
        print(f"Error reading model parameters: {e}")
        return {} 