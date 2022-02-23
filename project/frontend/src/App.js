import React, {useState, useEffect} from 'react';
import './App.css';
import Login from './components/Login.js';
import Overview from './components/Overview.js';
import MachineInfo from './components/MachineInfo.js';
import TopMenu from './components/TopMenu.js';
import Home from './components/Home.js';
import Timer from './components/Timer.js';
import Codes from './components/QRCodes';

import {
  BrowserRouter as Router,
  Routes,
  Route} from "react-router-dom";

function App() {

  const [auth, setAuth] = useState(false);

  useEffect(() => {
    const cookieKey = localStorage.getItem("loginCookie");
    if (cookieKey)
    {
      setAuth(true);
    }
    else
    {
      setAuth(false);
    }
}, []);


  return (
    <Router>
      <div>
        <TopMenu auth={auth}/>
        <Routes>
          <Route path="/" caseSensitive={false} element={<Home auth={auth} />} />
          <Route path="/login" caseSensitive={false} element={<Login />} />
          <Route path="/machines" caseSensitive={false} element={<Overview auth={auth}/>} />
          <Route path="/machines/:id" caseSensitive={false} element={<MachineInfo auth={auth}/>} />
          <Route path="/timer" caseSensitive={false} element={<Timer auth={auth}/>} />
          <Route path="/qrcodes" caseSensitive={false} element={<Codes auth={auth}/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
