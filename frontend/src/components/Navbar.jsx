import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-black shadow-lg">
      <div className="container mx-auto px-4 flex items-center h-16">
        <div className="flex items-center">
          <span className="text-white text-2xl font-bold mr-4">IoT-Studio</span> {/* Website Name */}
        </div>
        <div className="flex space-x-4 ml-auto">
          <Link
            to="/"
            className="text-white hover:text-white hover:bg-gray-700 px-3 py-2 rounded-md"
          >
            Training
          </Link>
          <Link
            to="/predict"
            className="text-white hover:text-white hover:bg-gray-700 px-3 py-2 rounded-md"
          >
            Prediction
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar; 