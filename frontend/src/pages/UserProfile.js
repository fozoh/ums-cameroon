import React, { useEffect, useState } from 'react';
import axios from 'axios';

const UserProfile = () => {
  const [profile, setProfile] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [form, setForm] = useState({ phone: '', address: '', avatar: null });

  useEffect(() => {
    // Fetch user profile from backend
    const token = localStorage.getItem('token');
    axios.get('http://localhost:8000/api/profile/', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => {
      setProfile(res.data);
      setForm({ phone: res.data.phone || '', address: res.data.address || '', avatar: null });
    });
  }, []);

  const handleChange = e => {
    const { name, value, files } = e.target;
    setForm(prev => ({ ...prev, [name]: files ? files[0] : value }));
  };

  const handleSave = async () => {
    const token = localStorage.getItem('token');
    const formData = new FormData();
    formData.append('phone', form.phone);
    formData.append('address', form.address);
    if (form.avatar) formData.append('avatar', form.avatar);
    await axios.put('http://localhost:8000/api/profile/', formData, {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' }
    });
    setEditMode(false);
    window.location.reload();
  };

  if (!profile) return <div>Loading...</div>;

  return (
    <div className="max-w-xl mx-auto p-8 bg-white rounded-xl shadow-lg mt-8">
      <h2 className="text-2xl font-bold mb-4">User Profile</h2>
      <div className="flex flex-col items-center mb-4">
        <img src={profile.avatar || '/default-avatar.png'} alt="Avatar" className="w-24 h-24 rounded-full mb-2" />
        <div className="font-semibold">{profile.user.email}</div>
      </div>
      {editMode ? (
        <div className="flex flex-col gap-4">
          <input name="phone" value={form.phone} onChange={handleChange} placeholder="Phone" className="p-2 border rounded" />
          <input name="address" value={form.address} onChange={handleChange} placeholder="Address" className="p-2 border rounded" />
          <input name="avatar" type="file" onChange={handleChange} className="p-2 border rounded" />
          <button onClick={handleSave} className="bg-blue-600 text-white px-4 py-2 rounded">Save</button>
        </div>
      ) : (
        <div className="flex flex-col gap-2">
          <div><strong>Phone:</strong> {profile.phone || '-'}</div>
          <div><strong>Address:</strong> {profile.address || '-'}</div>
          <button onClick={() => setEditMode(true)} className="bg-blue-600 text-white px-4 py-2 rounded mt-4">Edit Profile</button>
        </div>
      )}
    </div>
  );
};

export default UserProfile;
