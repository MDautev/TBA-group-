import { Link } from "react-router-dom";

export function Navbar({ user, setUser }) {
  return (
    <nav className="bg-blue-600 text-white p-4 flex justify-between items-center shadow-md">
      <Link to="/" className="text-2xl font-bold text-white hover:text-yellow-300 transition duration-300">
        FoodApp
      </Link>
      <div className="flex items-center">
        {user ? (
          <button 
            onClick={() => setUser(null)} 
            className="ml-4 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition duration-300"
          >
            Logout
          </button>
        ) : (
          <>
            <Link 
              to="/login" 
              className="ml-4 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition duration-300"
            >
              Login
            </Link>
            <Link 
              to="/register" 
              className="ml-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition duration-300"
            >
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
