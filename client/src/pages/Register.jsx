import React, { useState, useRef } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    username: '',
    password: '',
    password2: '',
    address: '',
    dob: '',
    profilePicture: null,
    profilePictureFile: null,
  });

  const fileInputRef = useRef();

  const handleChange = (e) => {
    const { name, value, files } = e.target;

    if (name === 'profilePicture' && files.length > 0) {
      const file = files[0];
      setFormData(prev => ({
        ...prev,
        profilePicture: URL.createObjectURL(file),
        profilePictureFile: file,
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.password2) {
      alert('Passwords do not match.');
      return;
    }

    const data = new FormData();
    data.append('email', formData.email);
    data.append('password', formData.password);
    data.append('password2', formData.password2);
    data.append('first_name', formData.firstName);
    data.append('last_name', formData.lastName);
    data.append('address', formData.address);

    if (formData.username) data.append('username', formData.username);
    if (formData.dob) data.append('dob', formData.dob);
    if (formData.profilePictureFile) {
      data.append('image', formData.profilePictureFile);
    }

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/auth/register/", data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      alert('Registration successful!');
      console.log(res.data);
    } catch (error) {
      console.error(error.response?.data || error.message);
      alert('Registration failed! Check console for details.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-200 via-green-300 to-green-400 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-3xl font-semibold text-green-900 mb-6 text-center">Create an Account</h2>

        {/* Profile Picture Upload (Optional) */}
        <div className="flex justify-center mb-6">
          <div
            className="w-28 h-28 rounded-full border-4 border-green-500 overflow-hidden cursor-pointer shadow-md"
            onClick={() => fileInputRef.current.click()}
          >
            {formData.profilePicture ? (
              <img
                src={formData.profilePicture}
                alt="Profile Preview"
                className="object-cover w-full h-full"
              />
            ) : (
              <div className="flex items-center justify-center w-full h-full bg-green-100 text-green-500 text-5xl font-bold select-none">
                +
              </div>
            )}
          </div>
          <input
            type="file"
            name="profilePicture"
            accept="image/*"
            className="hidden"
            ref={fileInputRef}
            onChange={handleChange}
          />
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="flex space-x-4">
            <input
              type="text"
              name="firstName"
              placeholder="First Name"
              value={formData.firstName}
              onChange={handleChange}
              required
              className="w-1/2 px-4 py-3 border border-green-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            />
            <input
              type="text"
              name="lastName"
              placeholder="Last Name"
              value={formData.lastName}
              onChange={handleChange}
              required
              className="w-1/2 px-4 py-3 border border-green-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>

          <input
            type="text"
            name="username"
            placeholder="Username (optional)"
            value={formData.username}
            onChange={handleChange}
            className="w-full px-4 py-3 border border-green-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          />

          <input
            type="email"
            name="email"
            placeholder="Email address"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 border border-green-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          />

          <input
            type="text"
            name="address"
            placeholder="Address"
            value={formData.address}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 border border-green-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          />

          <input
            type="date"
            name="dob"
            placeholder="Date of Birth (optional)"
            value={formData.dob}
            onChange={handleChange}
            className="w-full px-4 py-3 border border-green-300 rounded-md text-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500"
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 border border-green-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          />

          <input
            type="password"
            name="password2"
            placeholder="Confirm Password"
            value={formData.password2}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 border border-green-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          />

          <button
            type="submit"
            className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-md shadow-md transition"
          >
            Register
          </button>
          <button
            type="button"
            className="w-full mt-2 bg-green-100 hover:bg-green-200 text-green-700 font-semibold py-3 rounded-md shadow-md transition"
            onClick={() => navigate('/login')}
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
}

export default Register;
