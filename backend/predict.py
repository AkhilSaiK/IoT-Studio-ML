import pandas as pd
import joblib
import numpy as np
import io
from storage import file_storage
import json

def predict_output(model_path, test_data):
    model = joblib.load(model_path)
    df = pd.DataFrame(test_data)
    predictions = model.predict(df).tolist()
    return predictions

def predict_values(data, model_name):
    """
    Make predictions using the specified model
    
    Args:
        data: pandas DataFrame or array-like for prediction
        model_name: name of the model to use for prediction
    
    Returns:
        numpy array of predictions
    """
    try:
        # Load the model
        model = file_storage.load_model(model_name)
        if model is None:
            raise ValueError(f"Model {model_name} not found")

        # Convert input to appropriate format
        if isinstance(data, str):
            # data = pd.read_csv(io.StringIO(data))
            data = json.loads(data)
            data = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            pass
        else:
            data = np.array(data)

        # Make predictions
        predictions = model.predict(data)
        return predictions

    except Exception as e:
        print(f"Error during prediction: {e}")
        raise