import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import React, { useEffect, useState } from 'react';

const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };
  const [notifications, setNotifications] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    if (user?.id) {
      fetch(`/api/notifications/?user=${user.id}&unread=true`)
        .then(res => res.json())
        .then(data => setNotifications(data));
    }
  }, [user?.id]);


  const user = JSON.parse(localStorage.getItem('user'));
  const role = user?.role;
  return (
    <nav className="navbar" style={{background:'#007bff',color:'#fff',padding:'12px 24px',display:'flex',justifyContent:'space-between',alignItems:'center'}}>
      <div className="navbar-brand">
        <div style={{position:'relative',marginRight:'18px'}}>
          <button onClick={() => setShowDropdown(!showDropdown)} style={{background:'none',border:'none',color:'#fff',cursor:'pointer',fontSize:'1.1em',position:'relative'}}>
            🔔
            {notifications.length > 0 && (
              <span style={{position:'absolute',top:'-6px',right:'-10px',background:'red',color:'#fff',borderRadius:'50%',padding:'2px 6px',fontSize:'0.8em'}}>{notifications.length}</span>
            )}
          </button>
          {showDropdown && (
            <div style={{position:'absolute',top:'32px',right:0,background:'#fff',color:'#333',boxShadow:'0 2px 8px rgba(0,0,0,0.15)',borderRadius:'6px',minWidth:'220px',zIndex:1000}}>
              <ul style={{listStyle:'none',margin:0,padding:'10px'}}>
                {notifications.length === 0 ? (
                  <li style={{padding:'8px'}}>No new notifications</li>
                ) : notifications.map(n => (
                  <li key={n.id} style={{padding:'8px',borderBottom:'1px solid #eee'}}>{n.message}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
        <Link to="/dashboard" style={{color:'#fff',fontWeight:'bold',fontSize:'1.2em',textDecoration:'none'}}>UMS Cameroon</Link>
      </div>
      <div className="navbar-links">
        {role === 'student' && <Link to="/register-course" style={{color:'#fff',marginRight:'18px',textDecoration:'none'}}>Register</Link>}
        {role === 'student' && <Link to="/payments" style={{color:'#fff',marginRight:'18px',textDecoration:'none'}}>Payments</Link>}
        {role === 'student' && <Link to="/transcript" style={{color:'#fff',marginRight:'18px',textDecoration:'none'}}>Transcript</Link>}
        {role === 'lecturer' && <Link to="/lecturer/dashboard" style={{color:'#fff',marginRight:'18px',textDecoration:'none'}}>Lecturer</Link>}
        {role === 'lecturer' && <Link to="/lecturer/update-marks" style={{color:'#fff',marginRight:'18px',textDecoration:'none'}}>Marks</Link>}
        {['director','vc','hod','dean'].includes(role) && <Link to="/admin/dashboard" style={{color:'#fff',marginRight:'18px',textDecoration:'none'}}>Admin</Link>}
        <Link to="/events" style={{color:'#fff',marginRight:'18px',textDecoration:'none'}}>Events</Link>
        <Link to="/messages" style={{color:'#fff',marginRight:'18px',textDecoration:'none'}}>Messages</Link>
        <Link to="/documents" style={{color:'#fff',marginRight:'18px',textDecoration:'none'}}>Documents</Link>
        <Link to="/feedback" style={{color:'#fff',marginRight:'18px',textDecoration:'none'}}>Feedback</Link>
        <Link to="/profile" style={{color:'#fff',textDecoration:'none'}}>Profile</Link>
      </div>
    </nav>
  );
};

export default Navbar;