import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get('http://localhost:8000/api/notifications/', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => {
      setNotifications(res.data);
      setLoading(false);
    });
  }, []);

  const markAsRead = async (id) => {
    const token = localStorage.getItem('token');
    await axios.put(`http://localhost:8000/api/notifications/${id}/read/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    setNotifications(notifications.map(n => n.id === id ? { ...n, read: true } : n));
  };

  if (loading) return <div>Loading notifications...</div>;

  return (
    <div className="max-w-xl mx-auto p-8 bg-white rounded-xl shadow-lg mt-8">
      <h2 className="text-2xl font-bold mb-4">Notifications</h2>
      {notifications.length === 0 ? (
        <div>No notifications.</div>
      ) : (
        <ul className="divide-y">
          {notifications.map(n => (
            <li key={n.id} className={`py-3 flex justify-between items-center ${n.read ? 'text-gray-400' : 'text-black'}`}>
              <span>{n.message}</span>
              {!n.read && (
                <button onClick={() => markAsRead(n.id)} className="bg-blue-600 text-white px-3 py-1 rounded">Mark as read</button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Notifications;
