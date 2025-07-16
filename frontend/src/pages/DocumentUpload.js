import React, { useState } from 'react';
import axios from 'axios';
import { FaUpload, FaDownload } from 'react-icons/fa';

const DocumentUpload = ({ userId, lang = 'en' }) => {
  const [title, setTitle] = useState('');
  const [file, setFile] = useState(null);
  const [documents, setDocuments] = useState([]);

  React.useEffect(() => {
    axios.get('/documents/').then(res => setDocuments(res.data));
  }, []);

  const handleUpload = () => {
    const formData = new FormData();
    formData.append('uploader', userId);
    formData.append('title', title);
    formData.append('file', file);
    axios.post('/documents/', formData).then(() => {
      setTitle('');
      setFile(null);
      axios.get('/documents/').then(res => setDocuments(res.data));
    });
  };

  return (
    <div className="document-upload-container">
      <h2>{lang === 'fr' ? 'Téléversement de documents' : 'Document Upload'}</h2>
      <div className="upload-form">
        <input
          type="text"
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder={lang === 'fr' ? 'Titre du document' : 'Document title'}
        />
        <input
          type="file"
          onChange={e => setFile(e.target.files[0])}
        />
        <button onClick={handleUpload}><FaUpload /> {lang === 'fr' ? 'Téléverser' : 'Upload'}</button>
      </div>
      <div className="documents-list">
        {documents.map(doc => (
          <div key={doc.id} className="document-item">
            <span>{doc.title}</span>
            <a href={doc.file} download><FaDownload /> {lang === 'fr' ? 'Télécharger' : 'Download'}</a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DocumentUpload;
