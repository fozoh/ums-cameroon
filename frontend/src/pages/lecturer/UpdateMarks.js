
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { PencilSquareIcon } from '@heroicons/react/24/solid';

const UpdateMarks = () => {
  const [enrollmentId, setEnrollmentId] = useState('');
  const [caMarks, setCaMarks] = useState('');
  const [examMarks, setExamMarks] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleUpdate = async () => {
    setLoading(true);
    const token = localStorage.getItem('token');
    try {
      await axios.post(
        'http://localhost:8000/api/lecturer/update-marks/',
        { enrollment_id: enrollmentId, ca_marks: caMarks, exam_marks: examMarks },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('✅ Marks updated successfully');
    } catch {
      alert('❌ Failed to update marks');
      navigate('/login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-md mx-auto bg-white p-8 rounded-xl shadow-lg flex flex-col items-center">
        <PencilSquareIcon className="h-10 w-10 text-indigo-500 mb-2" />
        <h2 className="text-2xl font-bold text-primary mb-4">Update Student Marks</h2>
        <div className="space-y-4 w-full">
          <div>
            <label className="block text-sm font-medium text-gray-700">Enrollment ID</label>
            <input
              type="text"
              value={enrollmentId}
              onChange={(e) => setEnrollmentId(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">CA Marks</label>
            <input
              type="number"
              value={caMarks}
              onChange={(e) => setCaMarks(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Exam Marks</label>
            <input
              type="number"
              value={examMarks}
              onChange={(e) => setExamMarks(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400"
            />
          </div>
          <button
            onClick={handleUpdate}
            className={`w-full flex items-center justify-center gap-2 bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors shadow ${loading ? 'opacity-60 cursor-not-allowed' : ''}`}
            disabled={loading}
          >
            <PencilSquareIcon className="h-5 w-5 text-white" />
            {loading ? 'Updating...' : 'Update Marks'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default UpdateMarks;