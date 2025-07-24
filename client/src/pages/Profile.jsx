import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Profile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
  if (user) {
    console.log('User object:', user);
  }
}, [user]);


  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('No access token found. Please login.');
        setLoading(false);
        return;
      }

      try {
        const res = await axios.get('http://127.0.0.1:8000/api/auth/profile/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUser(res.data);
      } catch (err) {
        setError('Failed to fetch profile. Please login again.');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) return <div className="text-center text-green-900">Loading profile...</div>;
  if (error) return <div className="text-center text-red-600">{error}</div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-200 via-green-300 to-green-400 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-slate-200 rounded-lg shadow-lg p-8">
        <h2 className="text-3xl font-semibold text-green-900 mb-6 text-center">Your Profile</h2>

        <div className="flex flex-col items-center space-y-4">
          <div className="w-28 h-28 rounded-full border-4 border-green-500 overflow-hidden shadow-md">
            {user.image ? (
              <img
              src={user.image}
              alt="Profile"
              className="object-cover w-full h-full"
            />

            ) : (
              <div className="flex items-center justify-center w-full h-full bg-green-100 text-green-500 text-5xl font-bold select-none">
                {user.first_name?.[0] || user.email[0]}
              </div>
            )}
          </div>

          <div className="w-full space-y-2">
            <p><strong>First Name:</strong> {user.first_name}</p>
            <p><strong>Last Name:</strong> {user.last_name}</p>
            <p><strong>Username:</strong> {user.username}</p>
            <p><strong>Email:</strong> {user.email}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
