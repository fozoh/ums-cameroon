import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FaBullhorn, FaCalendarAlt } from 'react-icons/fa';

const EventBoard = ({ lang = 'en' }) => {
  const [events, setEvents] = useState([]);
  useEffect(() => {
    axios.get('/events/').then(res => setEvents(res.data));
  }, []);

  return (
    <div className="event-board-container">
      <h2>{lang === 'fr' ? 'Événements et annonces' : 'Events & Announcements'}</h2>
      <div className="events-list">
        {events.map(ev => (
          <div key={ev.id} className="event-item">
            <FaBullhorn /> <b>{lang === 'fr' ? ev.title_fr : ev.title_en}</b>
            <span>{lang === 'fr' ? ev.description_fr : ev.description_en}</span>
            <span className="date"><FaCalendarAlt /> {ev.date}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventBoard;
