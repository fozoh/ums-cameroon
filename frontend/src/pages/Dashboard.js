
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { AcademicCapIcon } from '@heroicons/react/24/solid';

const Dashboard = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCourses = async () => {
      const token = localStorage.getItem('token');
      try {
        const res = await axios.get('http://localhost:8000/api/my-courses/', {
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
        <AcademicCapIcon className="h-8 w-8 text-blue-600" />
        <h2 className="text-3xl font-bold text-primary">Your Courses</h2>
      </div>
      {loading ? (
        <div className="text-center text-gray-500 py-10">Loading courses...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.length === 0 ? (
            <p className="col-span-full text-center text-gray-500">No courses found.</p>
          ) : (
            courses.map((c, i) => (
              <div key={i} className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow border-l-4 border-primary">
                <h3 className="text-xl font-semibold flex items-center gap-2">
                  <AcademicCapIcon className="h-5 w-5 text-indigo-500" /> {c.course}
                </h3>
                <p className="mt-2">
                  CA: <span className="font-medium">{c.ca_marks || '-'}</span> | 
                  Exam: <span className="font-medium">{c.exam_marks || '-'}</span>
                </p>
                <div className="mt-4">
                  <span className={`inline-block px-3 py-1 rounded-full ${
                    c.final_grade === 'A' ? 'bg-green-100 text-green-700' :
                    c.final_grade === 'F' ? 'bg-red-100 text-red-700' :
                    'bg-yellow-100 text-yellow-700'
                  }`}>
                    Final Grade: {c.final_grade || 'N/A'}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default Dashboard;