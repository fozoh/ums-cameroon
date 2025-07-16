
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { BookOpenIcon } from '@heroicons/react/24/solid';

const LecturerDashboard = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCourses = async () => {
      const token = localStorage.getItem('token');
      try {
        const res = await axios.get('http://localhost:8000/api/lecturer/courses/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setCourses(res.data);
      } catch {
        navigate('/login');
      } finally {
        setLoading(false);
      }
    };
    fetchCourses();
  }, [navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="flex items-center gap-3 mb-6">
        <BookOpenIcon className="h-8 w-8 text-indigo-600" />
        <h2 className="text-2xl font-bold text-primary">Your Courses</h2>
      </div>
      {loading ? (
        <div className="text-center text-gray-500 py-10">Loading courses...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {courses.length === 0 ? (
            <p className="text-gray-500">You have no courses assigned yet.</p>
          ) : (
            courses.map((c, i) => (
              <div key={i} className="bg-white p-5 rounded-xl shadow hover:shadow-md transition-shadow border-l-4 border-indigo-400">
                <h3 className="text-lg font-semibold flex items-center gap-2">
                  <BookOpenIcon className="h-5 w-5 text-indigo-500" /> {c.name}
                </h3>
                <p className="text-sm text-gray-500">Code: {c.code} 2 Department: {c.department?.name}</p>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default LecturerDashboard;