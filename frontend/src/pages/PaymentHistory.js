
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { BanknotesIcon } from '@heroicons/react/24/solid';

const PaymentHistory = () => {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPayments = async () => {
      const token = localStorage.getItem('token');
      try {
        const res = await axios.get('http://localhost:8000/api/payment-history/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setPayments(res.data);
      } catch {
        navigate('/login');
      } finally {
        setLoading(false);
      }
    };
    fetchPayments();
  }, [navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-3xl mx-auto">
        <div className="flex items-center gap-3 mb-6">
          <BanknotesIcon className="h-8 w-8 text-green-600" />
          <h2 className="text-2xl font-bold text-primary">Payment History</h2>
        </div>
        {loading ? (
          <div className="text-center text-gray-500 py-10">Loading payments...</div>
        ) : (
          <div className="space-y-4">
            {payments.length === 0 && <p>No payments found.</p>}
            {payments.map((p, i) => (
              <div key={i} className="bg-white p-4 rounded-lg shadow flex justify-between items-center border-l-4 border-green-400">
                <div>
                  <p className="font-semibold flex items-center gap-2">
                    <BanknotesIcon className="h-5 w-5 text-green-500" />
                    {p.amount} XAF
                  </p>
                  <small className="text-gray-500">{p.method} 2 {new Date(p.date).toLocaleDateString()}</small>
                </div>
                <span className="text-sm bg-green-100 text-green-700 px-3 py-1 rounded-full">Paid</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default PaymentHistory;