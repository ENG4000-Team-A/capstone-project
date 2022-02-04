import React, {useState, useEffect} from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import AccountCircle from '@mui/icons-material/AccountCircle';

import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';

import { useNavigate } from 'react-router-dom';
 
import {Link} from "react-router-dom";


function TopMenu({auth}) {

    const [anchorEl, setAnchorEl] = useState(true);
    const open = Boolean(anchorEl);

    const navigate = useNavigate();
    const pages = [
      {name:'Home', to:'/'}, 
      {name:'Game Stations', to:'/machines'}, 
      {name:'My Timer', to:'/timer'}
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
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            ConsoleTracker
          </Typography>
          { auth && pages.map((page) => (
            <Link to={page.to} style={{ textDecoration: 'none' }}>
              <MenuItem key={page.name} onClick={handleClose}>
                  <Typography textAlign="center">{page.name}</Typography>
              </MenuItem>
            </Link>
              ))}
          { !auth && 
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
                <MenuItem onClick={handleClose}>My account</MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </div>
          )}
        </Toolbar>
      </AppBar>
    )
}

export default TopMenu
