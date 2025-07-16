import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FaHome, FaBook, FaMoneyBill, FaUserGraduate, FaChalkboardTeacher, FaUniversity, FaEnvelope, FaUpload, FaBullhorn, FaCommentDots, FaCog } from 'react-icons/fa';

const Sidebar = ({ role, lang }) => {
  const location = useLocation();
  const [open, setOpen] = React.useState(window.innerWidth > 900);
  React.useEffect(() => {
    const handleResize = () => setOpen(window.innerWidth > 900);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  const links = [
    { to: '/dashboard', icon: <FaHome />, label: lang === 'fr' ? 'Accueil' : 'Home', roles: ['student'] },
    { to: '/register-course', icon: <FaBook />, label: lang === 'fr' ? 'Inscription' : 'Course Registration', roles: ['student'] },
    { to: '/payments', icon: <FaMoneyBill />, label: lang === 'fr' ? 'Paiements' : 'Payments', roles: ['student'] },
    { to: '/transcript', icon: <FaUserGraduate />, label: lang === 'fr' ? 'Relevé de notes' : 'Transcript', roles: ['student'] },
    { to: '/lecturer/dashboard', icon: <FaChalkboardTeacher />, label: lang === 'fr' ? 'Tableau Enseignant' : 'Lecturer Dashboard', roles: ['lecturer'] },
    { to: '/lecturer/update-marks', icon: <FaBook />, label: lang === 'fr' ? 'Notes' : 'Update Marks', roles: ['lecturer'] },
    { to: '/admin/dashboard', icon: <FaCog />, label: lang === 'fr' ? 'Admin' : 'Admin Dashboard', roles: ['director','vc','hod','dean'] },
    { to: `/school/dashboard/${JSON.parse(localStorage.getItem('user'))?.school || ''}`, icon: <FaUniversity />, label: lang === 'fr' ? 'École' : 'School Dashboard', roles: ['director','vc','hod','dean'] },
    { to: '/messages', icon: <FaEnvelope />, label: lang === 'fr' ? 'Messages' : 'Messages', roles: ['student','lecturer','director','vc','hod','dean'] },
    { to: '/documents', icon: <FaUpload />, label: lang === 'fr' ? 'Documents' : 'Documents', roles: ['student','lecturer','director','vc','hod','dean'] },
    { to: '/events', icon: <FaBullhorn />, label: lang === 'fr' ? 'Événements' : 'Events', roles: ['student','lecturer','director','vc','hod','dean'] },
    { to: '/feedback', icon: <FaCommentDots />, label: lang === 'fr' ? 'Retour' : 'Feedback', roles: ['student','lecturer','director','vc','hod','dean'] },
  ];
  return (
    <>
      <button
        className="sidebar-toggle"
        style={{position:'fixed',top:20,left:open?220:10,zIndex:1000,background:'#007bff',color:'#fff',border:'none',borderRadius:'4px',padding:'8px 12px',cursor:'pointer',display:window.innerWidth<=900?'block':'none'}}
        onClick={() => setOpen(!open)}
      >{open ? (lang==='fr'?'Fermer':'Close') : (lang==='fr'?'Menu':'Menu')}</button>
      <aside
        className="sidebar"
        style={{
          width: open ? '220px' : '0',
          background: '#f8f9fa',
          padding: open ? '20px' : '0',
          height: '100vh',
          position: 'fixed',
          top: 0,
          left: 0,
          overflow: 'hidden',
          transition: 'width 0.3s',
          boxShadow: open ? '2px 0 8px rgba(0,0,0,0.07)' : 'none',
          zIndex: 999
        }}
      >
        {open && (
          <ul style={{listStyle:'none',padding:0}}>
            {links.filter(l => l.roles.includes(role)).map(link => (
              <li key={link.to} style={{margin:'18px 0'}}>
                <Link to={link.to} style={{display:'flex',alignItems:'center',color:location.pathname===link.to?'#007bff':'#333',textDecoration:'none',fontWeight:location.pathname===link.to?'bold':'normal'}}>
                  <span style={{marginRight:'10px'}}>{link.icon}</span> {link.label}
                </Link>
              </li>
            ))}
          </ul>
        )}
      </aside>
    </>
  );
};

export default Sidebar;
