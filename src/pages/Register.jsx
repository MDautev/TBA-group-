// src/pages/Register.jsx
import React, { useState } from 'react';

export function Register({ setUser }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = () => {
    // Логика за регистрация
    if (username && password) {
      setUser({ name: username }); // Симулиран вход след регистрацията
      console.log('User registered:', username);
    } else {
      console.log('Please fill out all fields');
    }
  };

  return (
    <div className="register-container">
      <h2 className="register-title">Register</h2>
      <input
        type="text"
        placeholder="Username"
        className="input-field"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        className="input-field"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleRegister} className="register-btn">
        Register
      </button>
    </div>
  );
}
