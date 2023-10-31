import React, { useState } from 'react';
import { Button, TextField, Paper } from '@mui/material';
import './Login.css';

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [emailError, setEmailError] = useState(false);

  const validateEmail = (email) => {
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return emailPattern.test(email);
  };

  const handleEmailChange = (e) => {
    const newEmail = e.target.value;
    setEmail(newEmail);
    setEmailError(!validateEmail(newEmail));
  };

  return (
    <div className='login-container'>
      <Paper elevation={3} className='login-form'>
        <h1 className='login-title'>LOGIN</h1>
        <br />
        <p className='login-description'>
          To get access to the job data, log in here.
        </p>
        <br />
        <TextField
          label='Email'
          value={email}
          onChange={handleEmailChange}
          fullWidth
          error={emailError}
          helperText={emailError ? 'Invalid email format' : ''}
        />
        <br />
        <br />
        <TextField
          label='Password'
          type='password'
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          fullWidth
        />
        <br />
        <br />
        <br />
        <Button variant='contained' onClick={onLogin} fullWidth>
          Login
        </Button>
        <br />
        <p className='forgot-password'>
          Forgot your password?{' '}
          <a href='mailto:your-email@gmail.com'>Reset here</a>
        </p>
      </Paper>
    </div>
  );
}

export default Login;
