import React from 'react';
import { Navigate } from 'react-router-dom';

const AdminProtected = ({ children }) => {
  const token = localStorage.getItem('token');
  const user = JSON.parse(localStorage.getItem('user'));

  const isAdmin = ['director', 'vc', 'hod', 'dean'].includes(user?.role);

  if (!token || !isAdmin) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

export default AdminProtected;