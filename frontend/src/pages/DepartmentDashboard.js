import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FaBuilding, FaUsers, FaChalkboardTeacher, FaBook } from 'react-icons/fa';

const DepartmentDashboard = ({ departmentId, lang = 'en' }) => {
  const [data, setData] = useState(null);
  useEffect(() => {
    axios.get(`/analytics/department/${departmentId}/`).then(res => setData(res.data));
  }, [departmentId]);

  if (!data) return <div>Loading...</div>;

  return (
    <div className="dashboard-container">
      <h2>{lang === 'fr' ? 'Tableau de bord département' : 'Department Dashboard'}</h2>
      <div className="dashboard-section">
        <FaUsers />
        <h3>{lang === 'fr' ? 'Étudiants' : 'Students'}</h3>
        <p>{data.student_count}</p>
      </div>
      <div className="dashboard-section">
        <FaChalkboardTeacher />
        <h3>{lang === 'fr' ? 'Enseignants' : 'Lecturers'}</h3>
        <p>{data.lecturer_count}</p>
      </div>
      <div className="dashboard-section">
        <FaBook />
        <h3>{lang === 'fr' ? 'Cours' : 'Courses'}</h3>
        <p>{data.course_count}</p>
      </div>
    </div>
  );
};

export default DepartmentDashboard;
