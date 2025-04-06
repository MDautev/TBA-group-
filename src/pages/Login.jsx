// src/pages/Login.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export function Login({ setUser }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = () => {
    let role = null;

    if (username === 'client1' && password === 'pass123') {
      role = 'client';
    } else if (username === 'staff1' && password === 'pass123') {
      role = 'staff';
    } else if (username === 'del1' && password === 'pass123') {
      role = 'deliverer';
    } else {
      alert('Invalid credentials');
      return;
    }

    const newUser = { name: username, role };
    setUser(newUser);

    if (role === 'client') navigate('/dashboard/client');
    if (role === 'staff') navigate('/dashboard/staff');
    if (role === 'deliverer') navigate('/dashboard/deliverer');
  };

  return (
    <div className="login-container">
      <h2 className="login-title">Login</h2>

      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="input-field"
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="input-field"
      />

      <button onClick={handleLogin} className="login-btn">
        Login
      </button>
    </div>
  );
}

