import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FaStar } from 'react-icons/fa';

const FeedbackPage = ({ userId, lang = 'en' }) => {
  const [feedback, setFeedback] = useState('');
  const [rating, setRating] = useState(0);
  const [course, setCourse] = useState('');
  const [courses, setCourses] = useState([]);
  const [allFeedback, setAllFeedback] = useState([]);

  useEffect(() => {
    axios.get('/courses/').then(res => setCourses(res.data));
    axios.get('/feedback/').then(res => setAllFeedback(res.data));
  }, []);

  const submitFeedback = () => {
    axios.post('/feedback/', { user: userId, course, feedback_en: feedback, rating }).then(() => {
      setFeedback('');
      setRating(0);
      setCourse('');
      axios.get('/feedback/').then(res => setAllFeedback(res.data));
    });
  };

  return (
    <div className="feedback-container">
      <h2>{lang === 'fr' ? 'Retour et sondage' : 'Feedback & Survey'}</h2>
      <div className="feedback-form">
        <select value={course} onChange={e => setCourse(e.target.value)}>
          <option value="">{lang === 'fr' ? 'Choisir un cours' : 'Select course'}</option>
          {courses.map(c => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
        <textarea
          value={feedback}
          onChange={e => setFeedback(e.target.value)}
          placeholder={lang === 'fr' ? 'Votre retour...' : 'Your feedback...'}
        />
        <div className="rating">
          {[1,2,3,4,5].map(star => (
            <FaStar key={star} color={star <= rating ? 'gold' : 'gray'} onClick={() => setRating(star)} />
          ))}
        </div>
        <button onClick={submitFeedback}>{lang === 'fr' ? 'Soumettre' : 'Submit'}</button>
      </div>
      <div className="all-feedback">
        {allFeedback.map(fb => (
          <div key={fb.id} className="feedback-item">
            <b>{fb.user_email}</b>: {fb.feedback_en}
            <span className="rating">{[...Array(fb.rating)].map((_,i) => <FaStar key={i} color="gold" />)}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FeedbackPage;
