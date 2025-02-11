import { useState, useEffect } from 'react';
import axios from 'axios';

function Prediction() {
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [predictionType, setPredictionType] = useState('direct');
  const [file, setFile] = useState(null);
  const [directInput, setDirectInput] = useState('');
  const [predictions, setPredictions] = useState(null);
  const [trainedModels, setTrainedModels] = useState([]);

  const supportedFormats = '.csv, .xlsx, .xls';

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      const response = await axios.get('http://localhost:5000/models');
      setTrainedModels(response.data.trained_models);
    } catch (error) {
      console.error('Error fetching models:', error);
    }
  };

  const handlePredict = async () => {
    try {
      if (predictionType === 'file' && file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('model', selectedModel);

        const response = await axios.post('http://localhost:5000/predict/file', formData, {
          responseType: 'blob',
        });

        // Create download link for the file
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'predictions.csv');
        document.body.appendChild(link);
        link.click();
        link.remove();
      } else {
        const response = await axios.post('http://localhost:5000/predict', {
          type: 'direct',
          data: directInput,
          model: selectedModel,
        });
        setPredictions(response.data.predictions);
      }
    } catch (error) {
      console.error('Error during prediction:', error);
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4 text-white">
        Make Predictions
      </h2>
      
      <div className="space-y-4">
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white border-gray-600"
        >
          <option value="">Select Model</option>
          {trainedModels.map((model) => (
            <option key={model} value={model}>
              {model}
            </option>
          ))}
        </select>

        <div className="flex space-x-4">
          <button
            onClick={() => setPredictionType('direct')}
            className={`flex-1 py-2 px-4 rounded ${
              predictionType === 'direct'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-200'
            }`}
          >
            Direct Input
          </button>
          <button
            onClick={() => setPredictionType('file')}
            className={`flex-1 py-2 px-4 rounded ${
              predictionType === 'file'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-200'
            }`}
          >
            File Upload
          </button>
        </div>

        {predictionType === 'direct' ? (
          <textarea
            value={directInput}
            onChange={(e) => setDirectInput(e.target.value)}
            className="w-full p-2 rounded bg-gray-700 text-white border-gray-600"
            rows="4"
            placeholder="Enter your input data. Eg: [[1, 2, 3], [4, 5, 6]]"
          />
        ) : (
          <div className="space-y-2">
            <input
              type="file"
              accept={supportedFormats}
              onChange={(e) => setFile(e.target.files[0])}
              className="block w-full text-gray-400
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-gray-700 file:text-white
                hover:file:bg-gray-600"
            />
            <p className="text-sm text-gray-400">
              Supported formats: {supportedFormats}
            </p>
          </div>
        )}

        <button
          onClick={handlePredict}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
        >
          Make Prediction
        </button>

        {predictions && (
          <div className="mt-4 p-4 bg-gray-700 rounded">
            <h3 className="text-lg font-semibold mb-2 text-white">
              Predictions:
            </h3>
            <pre className="text-sm text-gray-300">
              {JSON.stringify(predictions, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default Prediction; 