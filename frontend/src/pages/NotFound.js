import React from 'react';
import { ExclamationTriangleIcon } from '@heroicons/react/24/solid';

const NotFound = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-6">
      <div className="bg-white p-8 rounded-xl shadow-lg max-w-md w-full flex flex-col items-center">
        <ExclamationTriangleIcon className="h-12 w-12 text-red-500 mb-2" />
        <h1 className="text-3xl font-bold mb-4 text-center">404 - Page Not Found</h1>
        <p className="text-gray-700 text-center mb-4">
          Sorry, the page you are looking for does not exist.
        </p>
        <a href="/" className="bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow">Go Home</a>
      </div>
    </div>
  );
};

export default NotFound;
