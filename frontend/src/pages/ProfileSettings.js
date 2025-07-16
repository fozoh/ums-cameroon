import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProfileSettings = ({ userId, lang = 'en' }) => {
  const [profile, setProfile] = useState({});
  const [avatar, setAvatar] = useState(null);
  const [password, setPassword] = useState('');
  const [notifPref, setNotifPref] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get(`/api/profile/${userId}/`).then(res => {
      setProfile(res.data);
      setNotifPref(res.data.notifications_enabled);
    });
  }, [userId]);

  const handleUpdate = () => {
    axios.put(`/api/profile/${userId}/`, { ...profile, notifications_enabled: notifPref }).then(() => {
      setMessage(lang === 'fr' ? 'Profil mis à jour' : 'Profile updated');
    });
  };

  const handleAvatarUpload = () => {
    if (!avatar) return;
    const formData = new FormData();
    formData.append('avatar', avatar);
    axios.post(`/api/profile/${userId}/avatar/`, formData).then(() => {
      setMessage(lang === 'fr' ? 'Avatar mis à jour' : 'Avatar updated');
    });
  };

  const handlePasswordChange = () => {
    axios.post(`/api/profile/${userId}/password/`, { password }).then(() => {
      setMessage(lang === 'fr' ? 'Mot de passe changé' : 'Password changed');
      setPassword('');
    });
  };

  return (
    <div className="profile-settings-container">
      <h2>{lang === 'fr' ? 'Profil & Paramètres' : 'Profile & Settings'}</h2>
      {message && <div className="message">{message}</div>}
      <div className="profile-form">
        <label>{lang === 'fr' ? 'Nom' : 'Name'}:</label>
        <input type="text" value={profile.name || ''} onChange={e => setProfile({...profile, name: e.target.value})} />
        <label>Email:</label>
        <input type="email" value={profile.email || ''} disabled />
        <label>{lang === 'fr' ? 'Téléphone' : 'Phone'}:</label>
        <input type="text" value={profile.phone || ''} onChange={e => setProfile({...profile, phone: e.target.value})} />
        <label>{lang === 'fr' ? 'Adresse' : 'Address'}:</label>
        <input type="text" value={profile.address || ''} onChange={e => setProfile({...profile, address: e.target.value})} />
        <button onClick={handleUpdate}>{lang === 'fr' ? 'Mettre à jour' : 'Update'}</button>
      </div>
      <div className="avatar-upload">
        <label>{lang === 'fr' ? 'Avatar' : 'Avatar'}:</label>
        <input type="file" onChange={e => setAvatar(e.target.files[0])} />
        <button onClick={handleAvatarUpload}>{lang === 'fr' ? 'Téléverser' : 'Upload'}</button>
      </div>
      <div className="password-change">
        <label>{lang === 'fr' ? 'Nouveau mot de passe' : 'New Password'}:</label>
        <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
        <button onClick={handlePasswordChange}>{lang === 'fr' ? 'Changer' : 'Change'}</button>
      </div>
      <div className="notification-settings">
        <label>{lang === 'fr' ? 'Notifications' : 'Notifications'}:</label>
        <input type="checkbox" checked={notifPref} onChange={e => setNotifPref(e.target.checked)} />
        <span>{lang === 'fr' ? 'Activer les notifications' : 'Enable notifications'}</span>
      </div>
    </div>
  );
};

export default ProfileSettings;
