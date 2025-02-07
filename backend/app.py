from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from train import train_model
from predict import predict_output

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
MODEL_FOLDER = "models"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MODEL_FOLDER"] = MODEL_FOLDER
ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 200
    return jsonify({"error": "Invalid file type"}), 400

@app.route("/train", methods=["POST"])
def train():
    data = request.json
    filename = data.get("filename")
    model_type = data.get("model_type")
    parameters = data.get("parameters", {})

    if not filename or not model_type:
        return jsonify({"error": "Filename and model type required"}), 400

    dataset_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if not os.path.exists(dataset_path):
        return jsonify({"error": "Dataset not found"}), 404

    model_path, accuracy = train_model(dataset_path, model_type, parameters)
    
    return jsonify({"message": "Model trained successfully", "accuracy": accuracy, "model_path": model_path}), 200

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    model_name = data.get("model_name")
    test_data = data.get("test_data")

    if not model_name or not test_data:
        return jsonify({"error": "Model name and test data required"}), 400

    model_path = os.path.join(app.config["MODEL_FOLDER"], model_name)
    if not os.path.exists(model_path):
        return jsonify({"error": "Model not found"}), 404

    predictions = predict_output(model_path, test_data)
    return jsonify({"predictions": predictions}), 200

if __name__ == "__main__":
    app.run(debug=True)
