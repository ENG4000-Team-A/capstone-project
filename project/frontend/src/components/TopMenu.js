import React, { useState, useEffect } from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import AccountCircle from '@mui/icons-material/AccountCircle';

import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';

import { useNavigate } from 'react-router-dom';

import { Link } from "react-router-dom";

// Import components for reactive font size
// https://mui.com/customization/typography/#responsive-font-sizes
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme();

// Controls the Console Tracker Font Size
theme.typography.h3 = {
  fontSize: '1.2rem',
  '@media (min-width:600px)': {
    fontSize: '1.5rem',
  },

  // If screen width -> 900px, then our fontSize will be 2rem
  [theme.breakpoints.up('min-width:900px')]: {
    fontSize: '2rem',
  },
};

// Controls the Drop down Menu Test Size
theme.typography.h6 = {
  fontSize: '1rem',
  '@media (min-width:600px)': {
    fontSize: '1rem',
  },
  [theme.breakpoints.up('md')]: {
    fontSize: '1.5rem',
  },
};


function TopMenu({ auth }) {

  const [anchorEl, setAnchorEl] = useState(true);
  const open = Boolean(anchorEl);

  const navigate = useNavigate();
  const pages = [
    { name: 'Home', to: '/' },
    { name: 'Game Stations', to: '/machines' },
    { name: 'My Timer', to: '/timer' }
  ];

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    localStorage.removeItem("loginCookie");
    navigate('/');
    window.location.reload();
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <IconButton
          size="large"
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>

        {/* Temporary Fix */}
        <ThemeProvider theme={theme}>
          <Typography variant="h3" component="div" sx={{ flexGrow: 1 }}>
            ConsoleTracker
          </Typography>
        </ThemeProvider>

        {!auth &&
          <Link to="/login" style={{ textDecoration: 'none' }}>
            <MenuItem key='login'>
              <Typography textAlign="center">Login</Typography>
            </MenuItem>
          </Link>
        }

        {auth && (
          <div>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleClick}
              color="inherit"
            >
              <AccountCircle />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={open}
              onClose={handleClose}
              onClick={handleClose}
            >

               {/* Temporary Measure */}
              <MenuItem onClick={handleClose}>

                <Typography textAlign="center" variant='h6'>
                  My account
                </Typography>

              </MenuItem>
             
              {auth && pages.map((page) => (
                <Link to={page.to} style={{ textDecoration: 'none' }}>
                  <MenuItem key={page.name} onClick={handleClose}>
                    <ThemeProvider theme={theme}>
                      <Typography textAlign="center" variant="h6">
                        {page.name}
                        </Typography>
                    </ThemeProvider>
                  </MenuItem>
                </Link>
              ))}

              <MenuItem onClick={handleLogout}>

                <Typography textAlign="center" variant='h6'>
                  Logout
                </Typography>

              </MenuItem>
            </Menu>
          </div>
        )}
      </Toolbar>
    </AppBar>
  )
}

export default TopMenu
