import React, {useState, useEffect} from 'react';
import axios from 'axios';
import './Home.css'
import './rows.css'

function Home({auth}) {

    const [name, setName] = useState(null);
    const [userInfo, setInfo] = useState({
        machine: "",
        first_name: "",
        id: 0,
        last_name: "",
        phone_number: "",
        time: 0,
        username: ""
    });

  useEffect(() => {
    const username = localStorage.getItem("user");
    setName(username);
    console.log(username);
    axios.get('http://localhost:8000/users/',
        {
          headers: {
            Authorization: localStorage.getItem("authToken")
          }
        }
    )
        .then(response => {
            console.log(response.data.data);
            setInfo(response.data.data);
        })
        .catch(error => {
            console.log(error);
        });

}, []);


  return <div>
      {auth &&
        <div class="main-content-container">
          <div class='section-container profile'>
            <div class="wrap">
              <div class="content">
                <div class="row-12">
                  <div class="col-sm-12 col-4 profile-pic">
                    <img src="https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg" width="100%"/>
                  </div>
                  <div class="col-sm-12 col-8">
                    <h4>{userInfo.first_name} {userInfo.last_name}</h4>
                    <h5 class="sub">{userInfo.username} | {userInfo.phone_number} </h5>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class='section-container profile-time'>
            <div class="wrap">
              <div class="content">
                <div class="row-12">
                  <div class="col-sm-12 col-6">
                    <div class="card dark">
                      <h3 class="light-header"> Time Remaining </h3>
                      <h3> {(userInfo.time/ 60).toFixed(1)} minutes </h3>
                    </div>
                  </div>
                  <div class="col-sm-12 col-6">
                    <div class="card dark">
                      <h3 class="light-header"> Current Console </h3>
                      <h3> {userInfo.machine} </h3>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      }

  </div>;
}

export default Home;
