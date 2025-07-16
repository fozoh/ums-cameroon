import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FaPaperPlane, FaUser } from 'react-icons/fa';

const Messaging = ({ userId, lang = 'en' }) => {
  const [messages, setMessages] = useState([]);
  const [content, setContent] = useState('');
  const [recipient, setRecipient] = useState('');
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios.get('/users/').then(res => setUsers(res.data));
    axios.get(`/messages/?user=${userId}`).then(res => setMessages(res.data));
  }, [userId]);

  const sendMessage = () => {
    axios.post('/messages/', { sender: userId, recipient, content }).then(() => {
      setContent('');
      axios.get(`/messages/?user=${userId}`).then(res => setMessages(res.data));
    });
  };

  return (
    <div className="messaging-container">
      <h2>{lang === 'fr' ? 'Messagerie' : 'Messaging'}</h2>
      <div className="message-form">
        <select value={recipient} onChange={e => setRecipient(e.target.value)}>
          <option value="">{lang === 'fr' ? 'Choisir un destinataire' : 'Select recipient'}</option>
          {users.map(u => (
            <option key={u.id} value={u.id}>{u.email}</option>
          ))}
        </select>
        <input
          type="text"
          value={content}
          onChange={e => setContent(e.target.value)}
          placeholder={lang === 'fr' ? 'Votre message...' : 'Your message...'}
        />
        <button onClick={sendMessage}><FaPaperPlane /> {lang === 'fr' ? 'Envoyer' : 'Send'}</button>
      </div>
      <div className="messages-list">
        {messages.map(msg => (
          <div key={msg.id} className={msg.sender === userId ? 'sent' : 'received'}>
            <FaUser /> <b>{msg.sender_email}</b>: {msg.content}
            <span className="timestamp">{new Date(msg.timestamp).toLocaleString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Messaging;
