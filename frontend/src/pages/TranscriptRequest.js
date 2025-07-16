
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { DocumentTextIcon } from '@heroicons/react/24/solid';

const TranscriptRequest = () => {

  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const requestTranscript = async () => {
    setLoading(true);
    const token = localStorage.getItem('token');
    try {
      await axios.post('http://localhost:8000/api/transcript-request/', {}, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert('✅ Transcript request submitted!');
    } catch {
      alert('❌ Login required');
      navigate('/login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-md mx-auto bg-white p-8 rounded-xl shadow-lg flex flex-col items-center">
        <DocumentTextIcon className="h-10 w-10 text-green-500 mb-2" />
        <h2 className="text-2xl font-bold text-primary mb-4">Request Official Transcript</h2>
        <p className="mb-6">Apply for an official transcript below.</p>

        <button
          onClick={requestTranscript}
          className={`w-full flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-semibold transition-colors shadow ${loading ? 'opacity-60 cursor-not-allowed' : ''}`}
          disabled={loading}
        >
          <DocumentTextIcon className="h-5 w-5 text-white" />
          {loading ? 'Submitting...' : 'Apply for Transcript'}
        </button>
      </div>
    </div>
  );
};

export default TranscriptRequest;