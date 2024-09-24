// src/pages/LoginPage.js
import React, { useState } from 'react';
import { useMutation, gql } from '@apollo/client';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

const LOGIN_USER = gql`
  mutation LoginUser($username: String!, $password: String!) {
    tokenAuth(username: $username, password: $password) {
      token
    }
  }
`;

function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginUser, { data, loading, error }] = useMutation(LOGIN_USER);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const result = await loginUser({ variables: { username, password } });
      const token = result.data.tokenAuth.token;
      localStorage.setItem('token', token); // Save token
      navigate('/upload'); // Redirect to upload page
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h2 className="login-heading">Login</h2>
        <form className="login-form" onSubmit={handleLogin}>
          <input className="login-input" type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
          <input className="login-input" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button className="login-button" type="submit">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
