import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FaChartBar, FaUserGraduate, FaMoneyBill, FaComments } from 'react-icons/fa';

const StudentDashboard = ({ studentId, lang = 'en' }) => {
  const [data, setData] = useState(null);
  useEffect(() => {
    axios.get(`/analytics/student/${studentId}/`).then(res => setData(res.data));
  }, [studentId]);

  if (!data) return <div>Loading...</div>;

  return (
    <div className="dashboard-container">
      <h2>{lang === 'fr' ? 'Tableau de bord étudiant' : 'Student Dashboard'}</h2>
      <div className="dashboard-section">
        <FaChartBar />
        <h3>{lang === 'fr' ? 'Notes' : 'Grades'}</h3>
        <ul>
          {data.grades.map((g, i) => (
            <li key={i}>{g.course}: {g.final_grade}</li>
          ))}
        </ul>
      </div>
      <div className="dashboard-section">
        <FaUserGraduate />
        <h3>{lang === 'fr' ? 'Présence' : 'Attendance'}</h3>
        <p>{lang === 'fr' ? 'Taux de présence' : 'Attendance Rate'}: {data.attendance_rate}%</p>
      </div>
      <div className="dashboard-section">
        <FaMoneyBill />
        <h3>{lang === 'fr' ? 'Paiements' : 'Payments'}</h3>
        <ul>
          {data.payment_history.map((p, i) => (
            <li key={i}>{p.amount} - {p.method} ({new Date(p.timestamp).toLocaleDateString()})</li>
          ))}
        </ul>
      </div>
      <div className="dashboard-section">
        <FaComments />
        <h3>{lang === 'fr' ? 'Avis' : 'Feedback'}</h3>
        <ul>
          {data.feedback_summary.map((f, i) => (
            <li key={i}>{f.course}: {lang === 'fr' ? f.feedback_fr : f.feedback_en} (⭐{f.rating})</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default StudentDashboard;
