import React, { useState } from 'react'
import './MachineInfo.css'
import ReactDOM from 'react-dom';
import Button from '@mui/material/Button';


function SubmitPlay() {
    console.log(SubmitPlay);
}

function MachineInfo() {
    const [userInfo, SetUserInfo] = useState([{ username: "Elie", time: 1.2, machineName: null, machinetype: "xbox" }]);

    return (
        <div className='machineinfo__container'>
            <div>
                {userInfo.map(user => (
                    <div key={user.username}>
                        <p>
                            {"UserName: "}
                            {user.username}
                        </p>
                        <p>
                            {"Machine Name: "}
                            {user.machineName}
                        </p>
                        <p >
                            {"Machine Type: "}
                            {user.machinetype}
                        </p>
                        <p>
                            {"Time left On account (hours): "}
                            {user.time}
                       </p>
                    </div>


                ))}
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