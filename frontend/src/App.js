// ...existing code...
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
import SchoolDashboard from './pages/SchoolDashboard';
import Messaging from './pages/Messaging';
import DocumentUpload from './pages/DocumentUpload';
import EventBoard from './pages/EventBoard';
import FeedbackPage from './pages/FeedbackPage';
import DepartmentList from './pages/DepartmentList';

// Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Sidebar from './components/Sidebar';

// Layout Wrappers
const ProtectedLayout = ({ children }) => {
  const token = localStorage.getItem('token');
  const user = JSON.parse(localStorage.getItem('user'));
  const [lang] = React.useState(localStorage.getItem('lang') || 'en');
  if (!token) return <Navigate to="/login" replace />;
  return (
    <>
      <Navbar />
      <div style={{display:'flex'}}>
        <Sidebar role={user?.role} lang={lang} />
        <main style={{marginLeft:'220px',width:'100%',padding:'32px 24px'}}>{children}</main>
      </div>
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
  const [lang, setLang] = React.useState('en');
  const user = JSON.parse(localStorage.getItem('user'));
  return (
    <Router>
      <div className="lang-toggle" style={{textAlign:'right',padding:'10px'}}>
        <button onClick={() => setLang('en')} disabled={lang==='en'}>EN</button>
        <button onClick={() => setLang('fr')} disabled={lang==='fr'}>FR</button>
      </div>
      <Routes>
        {/* Public Route */}
        <Route path="/login" element={<Login />} />

        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedLayout>
              <StudentProtected>
                <Dashboard lang={lang} />
              </StudentProtected>
            </ProtectedLayout>
          }
        />
        {/* Department List (Admin/Staff) */}
        <Route
          path="/departments"
          element={
            <ProtectedLayout>
              <AdminProtected>
                <DepartmentList lang={lang} />
              </AdminProtected>
            </ProtectedLayout>
          }
        />
        <Route
          path="/register-course"
          element={
            <ProtectedLayout>
              <StudentProtected>
                <CourseRegistration lang={lang} />
              </StudentProtected>
            </ProtectedLayout>
          }
        />
        <Route
          path="/transcript"
          element={
            <ProtectedLayout>
              <StudentProtected>
                <TranscriptRequest lang={lang} />
              </StudentProtected>
            </ProtectedLayout>
          }
        />
        <Route
          path="/payments"
          element={
            <ProtectedLayout>
              <StudentProtected>
                <PaymentHistory lang={lang} />
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
                <LecturerDashboard lang={lang} />
              </LecturerProtected>
            </ProtectedLayout>
          }
        />
        <Route
          path="/lecturer/update-marks"
          element={
            <ProtectedLayout>
              <LecturerProtected>
                <UpdateMarks lang={lang} />
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
                <AdminDashboard lang={lang} />
              </AdminProtected>
            </ProtectedLayout>
          }
        />

        {/* School Dashboard */}
        <Route
          path="/school/dashboard/:schoolId"
          element={
            <ProtectedLayout>
              <SchoolDashboard schoolId={user?.school} lang={lang} />
            </ProtectedLayout>
          }
        />

        {/* Messaging */}
        <Route
          path="/messages"
          element={
            <ProtectedLayout>
              <Messaging userId={user?.id} lang={lang} />
            </ProtectedLayout>
          }
        />

        {/* Document Upload */}
        <Route
          path="/documents"
          element={
            <ProtectedLayout>
              <DocumentUpload userId={user?.id} lang={lang} />
            </ProtectedLayout>
          }
        />

        {/* Event Board */}
        <Route
          path="/events"
          element={
            <ProtectedLayout>
              <EventBoard lang={lang} />
            </ProtectedLayout>
          }
        />

        {/* Feedback/Survey */}
        <Route
          path="/feedback"
          element={
            <ProtectedLayout>
              <FeedbackPage userId={user?.id} lang={lang} />
            </ProtectedLayout>
          }
        />

        {/* Static Pages */}
        <Route
          path="/terms"
          element={
            <ProtectedLayout>
              <TermsOfService lang={lang} />
            </ProtectedLayout>
          }
        />
        <Route
          path="/privacy"
          element={
            <ProtectedLayout>
              <PrivacyPolicy lang={lang} />
            </ProtectedLayout>
          }
        />

        {/* Fallback: 404 Not Found */}
        <Route
          path="*"
          element={
            <ProtectedLayout>
              <NotFound lang={lang} />
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