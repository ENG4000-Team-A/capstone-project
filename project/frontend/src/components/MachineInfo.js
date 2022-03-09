import React, { useState, useEffect } from 'react'
import './MachineInfo.css'
import { useParams } from 'react-router-dom'
import Button from '@mui/material/Button';
import axios from 'axios';
import { useAlert } from 'react-alert'

function MachineInfo() {
    const { id } = useParams()
    const [machine, setMachine] = useState({});
    const [userInfo, SetUserInfo] = useState({});
    const alert = useAlert()
useEffect(()=>{
    axios.get("http://localhost:8000/machines/?id="+id
    ).then(response => {
        setMachine(response.data.data)
        console.log(response.data.data)

    }).catch(error => {
        console.log(error)
    })

},[]);
useEffect(() => {
    const username = localStorage.getItem("user");
    console.log(username);
    axios.get(`http://localhost:8000/users/?uname=${username}`)
        .then(response => {
            console.log(response.data.data);
            SetUserInfo(response.data.data)
        })
        .catch(error => {
            console.log(error);
        });
}, []);

function SubmitPlay() {
    /**
     * This function simply redirects to the timer page.
     * No data needs to be passed as user data is stored in cache
     */
     if(userInfo.time==0){
        alert.show('you need to Purchase time to play')
    }
    else{
        axios.post("http://localhost:8000/start_timer/"+id, {
            uname: userInfo.username
        }).then(function (response) {
        console.log(response);
        var getUrl = window.location;
        var redirect = getUrl .protocol + "//" + getUrl.host + "/" + "timer";    
        window.location.assign(redirect);
      })
      .catch(function (error) {
        console.log(error);
      });
    }
    

}


    return (
        <div className='machineinfo__container'>
            <div>
                    <div key={userInfo.first_name}>
                        <p>
                            {"UserName: "}
                            {userInfo.first_name}
                        </p>
                        <p>
                            {"Time left On account (minutes): "}
                            {(userInfo.time/ 60).toFixed(1)}
                       </p>
                    </div>
                
                    <div key={machine.name}>
                       <p>
                            {"Machine Name: "}
                            {machine.machineName}
                        </p>
                        <p >
                            {"Machine Type: "}
                            {machine.machinetype}
                        </p>
                      
                       </div>
                
                 
            </div>
            <div>
                <Button variant="contained" color="success" onClick={SubmitPlay}>
                    Start Playing
                </Button>
            </div>
        </div>

    )
}

export default MachineInfo