import React, {useEffect, useState} from 'react'
import Stack from '@mui/material/Stack'
import Button from '@mui/material/Button'
import './Timer.css'

function StopTimer() {
    /* Functionality to be implemented */
    console.log(StopTimer);
}
function Timer() {
    /* Placeholder code from (https://www.w3schools.com/js/js_dates.asp) to confirm timer works. Replace to calculate time left when linked to model -Chandler*/
    const calculateTimeLeft = () => {
        let year = new Date().getFullYear();
        const difference = +new Date(`${year}-10-1`) - +new Date();
        let timeLeft = {};
    
        if (difference > 0) {
          timeLeft = {
            days: Math.floor(difference / (1000 * 60 * 60 * 24)),
            hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
            minutes: Math.floor((difference / 1000 / 60) % 60),
            seconds: Math.floor((difference / 1000) % 60),
          };
        }
    
        return timeLeft;
      };
    
      const [timeLeft, setTimeLeft] = useState(calculateTimeLeft());
      const [year] = useState(new Date().getFullYear());
    
      useEffect(() => {
        setTimeout(() => {
          setTimeLeft(calculateTimeLeft());
        }, 1000);
      });
    
      const timerComponents = [];
    
      Object.keys(timeLeft).forEach((interval) => {
        if (!timeLeft[interval]) {
          return;
        }
    
        timerComponents.push(
          <span>
            {timeLeft[interval]} {interval}{" "}
          </span>
        );
      });
    /* End of placeholder code */
    return (

        <div className='timer_container'>
                
            <div className='time'>
                {timerComponents[1]}: {timerComponents[2]} : {timerComponents[3]}
                <div className='button'>
                    <Button variant="contained" onClick={StopTimer}>
                       STOP PLAYING
                    </Button>
                </div>
            </div>
            
        </div>
    )
}

export default Timer;
