import React, { useEffect, useState } from 'react';
import axios from 'axios';

const DepartmentList = ({ lang = 'en' }) => {
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/api/departments/', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
      .then(res => {
        setDepartments(res.data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>{lang === 'fr' ? 'Chargement...' : 'Loading...'}</div>;
  if (error) return <div>{lang === 'fr' ? 'Erreur:' : 'Error:'} {error}</div>;

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow">
      <h2 className="text-2xl font-bold mb-4">
        {lang === 'fr' ? 'Liste des Départements' : 'Department List'}
      </h2>
      <ul className="divide-y divide-gray-200">
        {departments.map(dep => (
          <li key={dep.id} className="py-4">
            <div className="font-semibold text-lg">{dep.name}</div>
            {dep.hod && (
              <div className="text-gray-600 text-sm">
                {lang === 'fr' ? 'Chef de département:' : 'Head of Department:'} {dep.hod.user.first_name} {dep.hod.user.last_name}
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DepartmentList;
