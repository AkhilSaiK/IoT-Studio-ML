from flask import jsonify, send_file
import pandas as pd
import os
from storage import file_storage
from predict import predict_values
from train import train_model, get_available_model_names

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_file_upload(file):
    if file and allowed_file(file.filename):
        success = file_storage.save_uploaded_file(file, file.filename)
        if success:
            return jsonify({'success': True, 'filename': file.filename})
    return jsonify({'success': False, 'error': 'Invalid file format'})

def read_input_file(file_path):
    """Read different file formats into pandas DataFrame"""
    file_extension = file_path.rsplit('.', 1)[1].lower()
    if file_extension == 'csv':
        return pd.read_csv(file_path)
    elif file_extension in ['xlsx', 'xls']:
        return pd.read_excel(file_path)
    raise ValueError(f"Unsupported file format: {file_extension}")

def handle_prediction(data_type, input_data, model_name):
    try:
        if data_type == 'file':
            # Save the uploaded file temporarily
            temp_input_path = os.path.join(UPLOAD_FOLDER, 'temp_input' + os.path.splitext(input_data.filename)[1])
            input_data.save(temp_input_path)
            
            # Read the input file
            df = read_input_file(temp_input_path)
            predictions = predict_values(df, model_name)
            
            # Add predictions to the dataframe
            df['predicted_output'] = predictions
            
            # Save to output file in the same format as input
            file_extension = os.path.splitext(input_data.filename)[1]
            output_path = os.path.join(UPLOAD_FOLDER, 'predicted_' + input_data.filename)
            
            if file_extension.lower() == '.csv':
                df.to_csv(output_path, index=False)
            else:  # Excel formats
                df.to_excel(output_path, index=False)
            
            # Clean up temporary input file
            os.remove(temp_input_path)
            
            return send_file(output_path, as_attachment=True)
        else:
            # Handle direct input data
            predictions = predict_values(input_data, model_name)
            return jsonify({'predictions': predictions.tolist()})
            
    except Exception as e:
        return jsonify({'error': str(e)})

def handle_training(dataset, model_name, parameters):
    try:
        success, result = train_model(dataset, model_name, parameters)
        if success:
            file_storage.save_model_params(model_name, parameters)
            return jsonify({
                'success': True,
                'model_filename': result['model_filename'],
                'metrics': result['metrics']
            })
        return jsonify({'success': False, 'error': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def get_datasets():
    datasets = file_storage.get_all_uploads()
    return jsonify({'datasets': datasets})

def get_models():
    """Get both available models for training and trained models"""
    available_models = get_available_model_names()
    trained_models = file_storage.get_all_models()
    return jsonify({
        'available_models': available_models,
        'trained_models': trained_models
    }) 