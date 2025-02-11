import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-gray-800 shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center h-16">
          <div className="flex space-x-4">
            <Link
              to="/"
              className="text-gray-200 hover:text-white hover:bg-gray-700 px-3 py-2 rounded-md"
            >
              Training
            </Link>
            <Link
              to="/predict"
              className="text-gray-200 hover:text-white hover:bg-gray-700 px-3 py-2 rounded-md"
            >
              Prediction
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar; 