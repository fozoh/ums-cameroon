import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AuditLog = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get('http://localhost:8000/api/auditlog/', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => {
      setLogs(res.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div>Loading audit logs...</div>;

  return (
    <div className="max-w-2xl mx-auto p-8 bg-white rounded-xl shadow-lg mt-8">
      <h2 className="text-2xl font-bold mb-4">Audit Log</h2>
      {logs.length === 0 ? (
        <div>No audit log entries.</div>
      ) : (
        <table className="w-full text-left border">
          <thead>
            <tr>
              <th className="p-2 border">Timestamp</th>
              <th className="p-2 border">User</th>
              <th className="p-2 border">Action</th>
              <th className="p-2 border">Model</th>
              <th className="p-2 border">Object ID</th>
              <th className="p-2 border">Details</th>
            </tr>
          </thead>
          <tbody>
            {logs.map(log => (
              <tr key={log.id}>
                <td className="p-2 border">{log.timestamp}</td>
                <td className="p-2 border">{log.user ? log.user.email : '-'}</td>
                <td className="p-2 border">{log.action}</td>
                <td className="p-2 border">{log.model}</td>
                <td className="p-2 border">{log.object_id}</td>
                <td className="p-2 border">{log.details}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default AuditLog;
