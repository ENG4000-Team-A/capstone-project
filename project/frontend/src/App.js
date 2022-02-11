import './App.css';
import Login from './components/Login.js';
import Overview from './components/Overview.js';
import MachineInfo from './components/MachineInfo.js';
import TopMenu from './components/TopMenu.js';
import MachineCard from './components/MachineCard.js';
import {
  BrowserRouter as Router,
  Routes,
  Route} from "react-router-dom";

function App() {
  return (
    <Router>
      <div>
        <TopMenu/>
        <Routes>
          <Route path="/login" caseSensitive={false} element={<Login />} />
          <Route path="/" caseSensitive={false} element={<Overview />} />
          <Route path="/machine" caseSensitive={false} element={<MachineInfo />} />
          <Route path="/machine_card" caseSensitive={false} element={<MachineCard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
