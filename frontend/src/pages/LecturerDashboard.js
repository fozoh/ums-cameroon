import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FaChalkboardTeacher, FaChartBar, FaUsers } from 'react-icons/fa';

const LecturerDashboard = ({ lecturerId, lang = 'en' }) => {
  const [data, setData] = useState(null);
  useEffect(() => {
    axios.get(`/analytics/lecturer/${lecturerId}/`).then(res => setData(res.data));
  }, [lecturerId]);

  if (!data) return <div>Loading...</div>;

  return (
    <div className="dashboard-container">
      <h2>{lang === 'fr' ? 'Tableau de bord enseignant' : 'Lecturer Dashboard'}</h2>
      {data.courses.map((course, i) => (
        <div className="dashboard-section" key={i}>
          <FaChalkboardTeacher />
          <h3>{course.course}</h3>
          <p>{lang === 'fr' ? 'Note moyenne' : 'Average Grade'}: {course.avg_grade || '-'}</p>
          <p>{lang === 'fr' ? 'Taux de présence' : 'Attendance Rate'}: {course.attendance_rate}%</p>
          <p>{lang === 'fr' ? 'Nombre d\'étudiants' : 'Student Count'}: {course.students}</p>
        </div>
      ))}
    </div>
  );
};

export default LecturerDashboard;
