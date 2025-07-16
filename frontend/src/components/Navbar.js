import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-primary">UMS Cameroon</h1>
        <ul className="flex space-x-6">
          <li><Link to="/dashboard" className="text-gray-700 hover:text-primary">Dashboard</Link></li>
          <li><Link to="/register-course" className="text-gray-700 hover:text-primary">Register Course</Link></li>
          <li><Link to="/transcript" className="text-gray-700 hover:text-primary">Transcript</Link></li>
          <li><Link to="/payments" className="text-gray-700 hover:text-primary">Payments</Link></li>
          <li>
            <button onClick={handleLogout} className="text-red-500 hover:text-red-700">
              Logout
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;