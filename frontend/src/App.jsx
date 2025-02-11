import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Training from './pages/Training';
import Prediction from './pages/Prediction';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-900">
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Training />} />
            <Route path="/predict" element={<Prediction />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App; 