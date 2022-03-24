import React from 'react'
import './Login.css'
import Button from '@mui/material/Button';
import Avatar from '@mui/material/Avatar';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import { useState } from 'react'

const API_URL = "http://127.0.0.1:8000";


const theme = createTheme({
  palette: {
    mode: 'dark'
  },
});

export default function SignIn() {

  const [username, setName] = useState('');
  const [password, setPass] = useState('');
  let navigate = useNavigate();

  const handleLogin = () => {
    console.log("logged")
    axios.post(API_URL + "/login/", {
      uname: username,
      pword: password
    }).then(function (response) { // logged in
      alert(response.data.status);
      console.log(response.data.status);
      if (response.data.status === "Successful Login") {
        localStorage.setItem('authToken', response.data.authToken);
        localStorage.setItem('user', username);
        navigate("/");
      }
      window.location.reload();
    }).catch(function (error) { // invalid login
      console.log(error)
      alert(error.response.data);
    });
  }

  const handleNameChange = (e) => {
    setName(e.target.value)
    console.log("updated name");

  }

  const handlePassChange = (e) => {
    setPass(e.target.value);
    console.log("updated pass");
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    // eslint-disable-next-line no-console
    console.log({
      email: data.get('email'),
      password: data.get('password'),
    });
  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
              onChange={handleNameChange}

            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              onChange={handlePassChange}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              onClick={() => {
                handleLogin() 
              }}
            >
              Sign In
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}