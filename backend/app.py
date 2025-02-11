from flask import Flask, request, jsonify
from flask_cors import CORS
from api_operations import (
    handle_file_upload, 
    handle_prediction, 
    handle_training,
    get_datasets,
    get_models
)

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    return handle_file_upload(request.files['file'])

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    data_type = data.get('type')  # 'file' or 'direct'
    input_data = data.get('data')
    model_name = data.get('model')
    return handle_prediction(data_type, input_data, model_name)

@app.route('/predict/file', methods=['POST'])
def predict_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    model_name = request.form.get('model')
    return handle_prediction('file', file, model_name)

@app.route('/train', methods=['POST'])
def train():
    data = request.get_json()
    dataset = data.get('dataset')
    model_name = data.get('model')
    parameters = data.get('parameters')
    return handle_training(dataset, model_name, parameters)

@app.route('/datasets', methods=['GET'])
def datasets():
    return get_datasets()

@app.route('/models', methods=['GET'])
def models():
    return get_models()

if __name__ == '__main__':
    app.run(debug=True)
