import React, { useState, useEffect } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Toolbar from '@mui/material/Toolbar';
import Tooltip from '@mui/material/Tooltip';
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
  const navigate = useNavigate();

  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const [anchorElUser, setAnchorElUser] = React.useState(null);

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const handleLogout = () => {
    localStorage.removeItem("authToken");
    localStorage.removeItem("user");
    navigate('/');
    window.location.reload();
  };

  const pages = [
    { name: 'Home', to: '/' },
    { name: 'Game Stations', to: '/machines' },
    { name: 'My Timer', to: '/timer' }
  ];

  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>

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
              <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
                <IconButton
                  size="large"
                  aria-label="account of current user"
                  aria-controls="menu-appbar"
                  aria-haspopup="true"
                  onClick={handleOpenNavMenu}
                  color="inherit"
                >
                  <MenuIcon />
                </IconButton>
                <Menu
                  id="menu-appbar"
                  anchorEl={anchorElNav}
                  anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'left',
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'left',
                  }}
                  open={Boolean(anchorElNav)}
                  onClose={handleCloseNavMenu}
                  sx={{
                    display: { xs: 'block', md: 'none' },
                  }}
                >
                  {pages.map((page) => (
                    <Link to={page.to} style={{ textDecoration: 'none' }}>
                      <MenuItem key={page.name} onClick={handleCloseNavMenu}>
                        <ThemeProvider theme={theme}>
                          <Typography textAlign="center">{page.name}</Typography>
                        </ThemeProvider>
                      </MenuItem>
                    </Link>
                  ))}
                  <MenuItem onClick={handleLogout}>
                    <Typography textAlign="center">
                      Logout
                    </Typography>
                  </MenuItem>
                </Menu>
              </Box>
              <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
                {pages.map((page) => (
                  <Link to={page.to} style={{ textDecoration: 'none' }}>
                    <Button
                      key={page.name}
                      onClick={handleCloseNavMenu}
                      sx={{ my: 2, color: 'white', display: 'block' }}
                    >
                      {page.name}
                    </Button>
                  </Link>
                ))}
                <Button
                  onClick={handleLogout}
                  sx={{ my: 2, color: 'white', display: 'block' }}
                    >
                    Logout
                </Button>
              </Box>

              <Box sx={{ flexGrow: 0 }}>
                <Menu
                  sx={{ mt: '45px' }}
                  id="menu-appbar"
                  anchorEl={anchorElUser}
                  anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  open={Boolean(anchorElUser)}
                  onClose={handleCloseUserMenu}
                >
                </Menu>
              </Box>
            </div>
          )}
        </Toolbar>
      </Container>
    </AppBar>
  )
}

export default TopMenu
