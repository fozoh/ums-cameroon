import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 p-6 mt-auto">
      <div className="container mx-auto flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
        <div className="text-gray-700">
          &copy; {new Date().getFullYear()} UMS Cameroon. All rights reserved.
        </div>
        <nav className="flex space-x-6">
          <Link to="/about" className="text-gray-600 hover:text-primary">About</Link>
          <Link to="/contact" className="text-gray-600 hover:text-primary">Contact</Link>
          <Link to="/privacy" className="text-gray-600 hover:text-primary">Privacy Policy</Link>
          <Link to="/support" className="text-gray-600 hover:text-primary">Support</Link>
        </nav>
      </div>
    </footer>
  );
};

export default Footer;