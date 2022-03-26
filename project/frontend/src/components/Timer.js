import React, {useEffect, useState} from 'react'
import Stack from '@mui/material/Stack'
import Button from '@mui/material/Button'
import axios from 'axios';
import './Timer.css'
import { modalClasses, modalUnstyledClasses } from '@mui/material';

const API_URL = "http://127.0.0.1:8000/timer/";
const BASE_URL = "http://127.0.01:8000/"
const COLOR_CODES = {
  info: {
    color: "green"
  }
};

let remainingPathColor = COLOR_CODES.info.color;

var timeLeftFormat = ""
var timer
var remainingTime
var then
var init = true


// vars for circle element
var TIME_LIMIT
var progressFraction = 0;

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

  var xhr = new XMLHttpRequest();
  xhr.open("POST", API_URL, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify({
      "action": "stop"
  }));
  window.location.replace(window.location.origin)
}

function updateTimeStringFormatted(h, m, s) {
    var hours = h < 10 ? "0" + h : h
    var minutes = m < 10 ? "0" + m : m
    var seconds = s < 10 ? "0" + s : s
    timeLeftFormat = hours + " : " + minutes + " : " + seconds
  }

function getTimeStringFormatted() {
  // NaN means session is over
  if (timeLeftFormat.includes('NaN')) {
    return "Start a session"
  } else {
    return timeLeftFormat
  } 
}

function setFraction(f) {
  progressFraction = f
}

function setCircleDashArray() {
  

    const circleDasharray = `${(
      progressFraction * 283
      ).toFixed(0)} 283`;

      if (progressFraction >= 0) {
        document
        .getElementById('base-timer-path-remaining')
        .setAttribute('stroke-dasharray', circleDasharray)
      }  
  }


function startCountdown(id){
  // timer starts automatically. ISSUE: timer flicker
    timer = setInterval(function(){countdown(id)}, 1000); 
}

function countdown(id){

  var now = Math.floor(Date.now() / 1000);

  remainingTime = then - now;

  if (init) {
    TIME_LIMIT = remainingTime;
    init = false
  }

  if (remainingTime/TIME_LIMIT >= 0) {
    progressFraction = remainingTime/TIME_LIMIT
  }
  

	var hour = Math.floor(remainingTime / (60 * 60) );
	var min = Math.floor((remainingTime / 60) % 60 );
	var sec = Math.floor(remainingTime % 60);

	if (remainingTime < 0){
		hour = 0;
		min = 0;
		sec = 0;
    StopTimer();
	}

  updateTimeStringFormatted(hour, min, sec);

	document.getElementById(id).innerHTML = getTimeStringFormatted();
  setCircleDashArray();
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
        <div class="base-timer">
          <svg class="base-timer__svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <g class="base-timer__circle">
              <circle class="base-timer__path-elapsed" cx="50" cy="50" r="45" />
              <path
                id="base-timer-path-remaining"
                stroke-dasharray="140 140"
                class="base-timer__path-remaining"
                d="
                  M 50, 50
                  m -45, 0
                  a 45,45 0 1,0 90,0
                  a 45,45 0 1,0 -90,0
                "
              ></path>
            </g>
          </svg>
        <span id='base-timer-label' class='base-timer__label'>
        <div className='time' id="timer">
          {startCountdown("timer")}
        </div> 
        </span>
      </div>
                    
          <div className='button'>
            <Button variant="contained" onClick={StopTimer}> STOP </Button>
          </div>
      </div>
    )
}

export default Timer_Function;