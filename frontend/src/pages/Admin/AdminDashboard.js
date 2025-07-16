import React from 'react';
import { UserGroupIcon } from '@heroicons/react/24/solid';

const AdminDashboard = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-6">
      <div className="bg-white p-8 rounded-xl shadow-lg max-w-2xl w-full flex flex-col items-center">
        <UserGroupIcon className="h-10 w-10 text-indigo-500 mb-2" />
        <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
        <p className="text-gray-700 text-center">
          Welcome to the admin dashboard. Here you can manage users, departments, and courses.
        </p>
      </div>
    </div>
  );
};

export default AdminDashboard;
