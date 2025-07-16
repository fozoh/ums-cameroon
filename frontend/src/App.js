import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import CourseRegistration from './pages/CourseRegistration';
import TranscriptRequest from './pages/TranscriptRequest';
import PaymentHistory from './pages/PaymentHistory';
import LecturerDashboard from './pages/lecturer/LecturerDashboard';
import UpdateMarks from './pages/lecturer/UpdateMarks';
import AdminDashboard from './pages/Admin/AdminDashboard';
import TermsOfService from './pages/TermsOfService';
import PrivacyPolicy from './pages/PrivacyPolicy';
import NotFound from './pages/NotFound';

// Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Layout Wrappers
const ProtectedLayout = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) return <Navigate to="/login" replace />;
  return (
    <>
      <Navbar />
      <main className="container mx-auto p-6">{children}</main>
      <Footer />
    </>
  );
};

const StudentProtected = ({ children }) => {
  const user = JSON.parse(localStorage.getItem('user'));
  if (user?.role !== 'student') {
    return <Navigate to="/login" replace />;
  }
  return children;
};

const LecturerProtected = ({ children }) => {
  const user = JSON.parse(localStorage.getItem('user'));
  if (user?.role !== 'lecturer') {
    return <Navigate to="/login" replace />;
  }
  return children;
};

const AdminProtected = ({ children }) => {
  const user = JSON.parse(localStorage.getItem('user'));
  const isAdmin = ['director', 'vc', 'hod', 'dean'].includes(user?.role);
  if (!isAdmin) {
    return <Navigate to="/dashboard" replace />;
  }
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Route */}
        <Route path="/login" element={<Login />} />

        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedLayout>
              <StudentProtected>
                <Dashboard />
              </StudentProtected>
            </ProtectedLayout>
          }
        />
        <Route
          path="/register-course"
          element={
            <ProtectedLayout>
              <StudentProtected>
                <CourseRegistration />
              </StudentProtected>
            </ProtectedLayout>
          }
        />
        <Route
          path="/transcript"
          element={
            <ProtectedLayout>
              <StudentProtected>
                <TranscriptRequest />
              </StudentProtected>
            </ProtectedLayout>
          }
        />
        <Route
          path="/payments"
          element={
            <ProtectedLayout>
              <StudentProtected>
                <PaymentHistory />
              </StudentProtected>
            </ProtectedLayout>
          }
        />

        {/* Lecturer Routes */}
        <Route
          path="/lecturer/dashboard"
          element={
            <ProtectedLayout>
              <LecturerProtected>
                <LecturerDashboard />
              </LecturerProtected>
            </ProtectedLayout>
          }
        />
        <Route
          path="/lecturer/update-marks"
          element={
            <ProtectedLayout>
              <LecturerProtected>
                <UpdateMarks />
              </LecturerProtected>
            </ProtectedLayout>
          }
        />

        {/* Admin Routes */}
        <Route
          path="/admin/dashboard"
          element={
            <ProtectedLayout>
              <AdminProtected>
                <AdminDashboard />
              </AdminProtected>
            </ProtectedLayout>
          }
        />

        {/* Static Pages */}
        <Route
          path="/terms"
          element={
            <ProtectedLayout>
              <TermsOfService />
            </ProtectedLayout>
          }
        />
        <Route
          path="/privacy"
          element={
            <ProtectedLayout>
              <PrivacyPolicy />
            </ProtectedLayout>
          }
        />

        {/* Fallback: 404 Not Found */}
        <Route
          path="*"
          element={
            <ProtectedLayout>
              <NotFound />
            </ProtectedLayout>
          }
        />

        {/* Default Redirect */}
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;