import pandas as pd
import joblib

def predict_output(model_path, test_data):
    model = joblib.load(model_path)
    df = pd.DataFrame(test_data)
    predictions = model.predict(df).tolist()
    return predictions
