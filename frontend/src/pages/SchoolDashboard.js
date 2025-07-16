import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FaUniversity, FaUsers, FaBuilding, FaBook } from 'react-icons/fa';

const SchoolDashboard = ({ schoolId, lang = 'en' }) => {
  const [data, setData] = useState(null);
  useEffect(() => {
    axios.get(`/analytics/school/${schoolId}/`).then(res => setData(res.data));
  }, [schoolId]);

  if (!data) return <div>Loading...</div>;

  return (
    <div className="dashboard-container">
      <h2>{lang === 'fr' ? 'Tableau de bord école' : 'School Dashboard'}</h2>
      <div className="dashboard-section">
        <FaBook />
        <h3>{lang === 'fr' ? 'Programmes' : 'Programs'}</h3>
        <p>{data.program_count}</p>
      </div>
      <div className="dashboard-section">
        <FaBuilding />
        <h3>{lang === 'fr' ? 'Départements' : 'Departments'}</h3>
        <p>{data.department_count}</p>
      </div>
      <div className="dashboard-section">
        <FaUsers />
        <h3>{lang === 'fr' ? 'Étudiants' : 'Students'}</h3>
        <p>{data.student_count}</p>
      </div>
    </div>
  );
};

export default SchoolDashboard;
