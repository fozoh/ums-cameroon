
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { ClipboardDocumentCheckIcon } from '@heroicons/react/24/solid';

const CourseRegistration = () => {

  const [courseId, setCourseId] = useState('');
  const [semester, setSemester] = useState('Semester 1');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async () => {
    setLoading(true);
    const token = localStorage.getItem('token');
    try {
      await axios.post(
        'http://localhost:8000/api/register-course/',
        { course_id: courseId, semester },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('✅ Course registered successfully!');
    } catch (error) {
      alert('❌ Failed to register course.');
      navigate('/login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-md mx-auto bg-white p-8 rounded-xl shadow-lg flex flex-col items-center">
        <ClipboardDocumentCheckIcon className="h-10 w-10 text-indigo-500 mb-2" />
        <h2 className="text-2xl font-bold text-primary mb-4">Register for a Course</h2>
        <div className="space-y-4 w-full">
          <div>
            <label className="block text-sm font-medium text-gray-700">Course ID</label>
            <input
              type="text"
              value={courseId}
              onChange={(e) => setCourseId(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
              placeholder="Enter course ID"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Semester</label>
            <select
              value={semester}
              onChange={(e) => setSemester(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            >
              <option>Semester 1</option>
              <option>Semester 2</option>
            </select>
          </div>

          <button
            onClick={handleRegister}
            className={`w-full flex items-center justify-center gap-2 bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors shadow ${loading ? 'opacity-60 cursor-not-allowed' : ''}`}
            disabled={loading}
          >
            <ClipboardDocumentCheckIcon className="h-5 w-5 text-white" />
            {loading ? 'Registering...' : 'Register Course'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default CourseRegistration;