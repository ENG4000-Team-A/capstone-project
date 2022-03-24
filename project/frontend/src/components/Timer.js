import React, {useEffect, useState} from 'react'
import Stack from '@mui/material/Stack'
import Button from '@mui/material/Button'
import axios from 'axios';
import './Timer.css'
import { modalClasses, modalUnstyledClasses } from '@mui/material';

const API_URL = "http://127.0.0.1:8000/timer/";
const BASE_URL = "http://127.0.01:8000/"
var timer
var remainingTime
var then

function StopTimer() {
  /**When STOP button is pressed:
   *  POST request with action: "stop" sent to stop timer
   *  Then redirects back to home
   */

  // POST request to change end time
  // NOTE: Stopping early does not reflect an accurate amount of time to the model
  

  axios.post(API_URL, {
                action: "stop"
            },
            {
                headers: {
                  Authorization: localStorage.getItem("authToken")
                }
            }
            ).then(function (response) {
              console.log(response);
              
          })
            .catch(function (error) {
                console.log(error);
            });
      
}

function startCountdown(id){
  // timer starts automatically. ISSUE: timer flicker
    timer = setInterval(function(){countdown(id)}, 1000); 
}

function countdown(id){

  var now = Math.floor(Date.now() / 1000);
	remainingTime = then - now;

	var hour = Math.floor(remainingTime / (60 * 60) );
	var min = Math.floor((remainingTime / 60) % 60 );
	var sec = Math.floor(remainingTime % 60);

	if (remainingTime < 0){
		hour = 0;
		min = 0;
		sec = 0;
    StopTimer();
	}

	var result = hour +':'+ min +':'+ sec;
	document.getElementById(id).innerHTML = result;
}

function Timer_Function() {

  const [userData, setUserData] = useState([]);

  useEffect(()=>{
      // User Uses Machine
      axios.get(API_URL,
        {
          headers: {
            Authorization: localStorage.getItem("authToken")
          }
      }
      ).then(response => {
          setUserData(response.data.data);
          console.log(response.data.data)
       }).catch(error => {
          console.log(error)
      })  
  },[]);

  then = Math.floor(  new Date(userData["end_time"]) / 1000);

    return (
      <div className='timer_container'>
          <div className='time' id="timer">
          {startCountdown("timer")}
          </div>           
          <div className='button'>
            <Button variant="contained" onClick={StopTimer}> STOP </Button>
          </div>
      </div>
    )
}

export default Timer_Function;