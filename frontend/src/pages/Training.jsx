import { useState, useEffect } from 'react';
import axios from 'axios';

function Training() {
  const [datasets, setDatasets] = useState([]);
  const [availableModels, setAvailableModels] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [parameters, setParameters] = useState({});
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');
  const [trainingResult, setTrainingResult] = useState(null);

  useEffect(() => {
    fetchDatasets();
    fetchModels();
  }, []);

  const fetchDatasets = async () => {
    try {
      const response = await axios.get('http://localhost:5000/datasets');
      setDatasets(response.data.datasets);
    } catch (error) {
      console.error('Error fetching datasets:', error);
    }
  };

  const fetchModels = async () => {
    try {
      const response = await axios.get('http://localhost:5000/models');
      setAvailableModels(response.data.available_models);
    } catch (error) {
      console.error('Error fetching models:', error);
    }
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setUploadError('');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadError('Please select a file first');
      return;
    }

    setUploading(true);
    setUploadError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:5000/upload', formData);
      await fetchDatasets();
      setFile(null);
      // Reset file input
      const fileInput = document.getElementById('file-upload');
      if (fileInput) fileInput.value = '';
    } catch (error) {
      setUploadError(error.response?.data?.error || 'Error uploading file');
      console.error('Error uploading file:', error);
    } finally {
      setUploading(false);
    }
  };

  const handleTrain = async () => {
    if (!selectedDataset || !selectedModel) {
      alert('Please select both dataset and model');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/train', {
        dataset: selectedDataset,
        model: selectedModel,
        parameters,
      });

      if (response.data.success) {
        setTrainingResult(response.data);
      } else {
        alert(response.data.error || 'Training failed');
      }
    } catch (error) {
      alert(error.response?.data?.error || 'Error during training');
      console.error('Error during training:', error);
    }
  };

  const formatMetricValue = (value) => {
    return typeof value === 'number' ? value.toFixed(4) : value;
  };

  return (
    <div className="space-y-8">
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-4 text-white">
          Upload Dataset
        </h2>
        <div className="space-y-4">
          <div className="flex items-center space-x-4">
            <label className="flex-1">
              <input
                type="file"
                id="file-upload"
                onChange={handleFileSelect}
                className="hidden"
                accept=".csv,.xlsx,.xls"
              />
              <div className="flex items-center space-x-2">
                <span className="flex-1 px-4 py-2 bg-gray-700 text-gray-200 rounded-l cursor-pointer hover:bg-gray-600 truncate">
                  {file ? file.name : 'Choose file'}
                </span>
                <button
                  onClick={handleUpload}
                  disabled={!file || uploading}
                  className={`px-4 py-2 rounded-r font-semibold ${
                    !file || uploading
                      ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                >
                  {uploading ? 'Uploading...' : 'Upload'}
                </button>
              </div>
            </label>
          </div>
          {uploadError && (
            <p className="text-red-500 text-sm">{uploadError}</p>
          )}
        </div>
      </div>

      <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-4 text-white">
          Train Model
        </h2>
        <div className="space-y-4">
          <select
            value={selectedDataset}
            onChange={(e) => setSelectedDataset(e.target.value)}
            className="w-full p-2 rounded bg-gray-700 text-white border-gray-600"
          >
            <option value="">Select Dataset</option>
            {datasets.map((dataset) => (
              <option key={dataset} value={dataset}>
                {dataset}
              </option>
            ))}
          </select>

          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="w-full p-2 rounded bg-gray-700 text-white border-gray-600"
          >
            <option value="">Select Model</option>
            {availableModels.map((model) => (
              <option key={model} value={model}>
                {model.replace(/_/g, ' ').toUpperCase()}
              </option>
            ))}
          </select>

          <button
            onClick={handleTrain}
            disabled={!selectedDataset || !selectedModel}
            className={`w-full py-2 px-4 rounded font-semibold ${
              !selectedDataset || !selectedModel
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            Train Model
          </button>
        </div>
      </div>

      {trainingResult && (
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold mb-4 text-white">
            Training Results
          </h2>
          <div className="space-y-4">
            <div className="bg-gray-700 p-4 rounded">
              <h3 className="text-lg font-semibold text-white mb-2">
                Model Information
              </h3>
              <p className="text-gray-200">
                Filename: {trainingResult.model_filename}
              </p>
              <p className="text-gray-200">
                Type: {trainingResult.metrics.model_type}
              </p>
            </div>

            <div className="bg-gray-700 p-4 rounded">
              <h3 className="text-lg font-semibold text-white mb-2">
                Performance Metrics
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-gray-200">
                    Training Score: {formatMetricValue(trainingResult.metrics.train_score)}
                  </p>
                  <p className="text-gray-200">
                    Test Score: {formatMetricValue(trainingResult.metrics.test_score)}
                  </p>
                </div>
                <div>
                  {trainingResult.metrics.accuracy && (
                    <p className="text-gray-200">
                      Accuracy: {formatMetricValue(trainingResult.metrics.accuracy)}
                    </p>
                  )}
                  {trainingResult.metrics.rmse && (
                    <p className="text-gray-200">
                      RMSE: {formatMetricValue(trainingResult.metrics.rmse)}
                    </p>
                  )}
                </div>
              </div>
            </div>

            <div className="bg-gray-700 p-4 rounded">
              <h3 className="text-lg font-semibold text-white mb-2">
                Model Parameters
              </h3>
              <pre className="text-sm text-gray-200 overflow-auto">
                {JSON.stringify(trainingResult.metrics.parameters, null, 2)}
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Training; 