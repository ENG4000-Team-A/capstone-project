import React, { useState } from 'react'
import './MachineInfo.css'
import ReactDOM from 'react-dom';
import Button from '@mui/material/Button';


function SubmitPlay() {
    console.log(SubmitPlay);
}

function MachineInfo() {
    const { id } = useParams()
    const [machine, setMachine] = useState([]);
    const [userInfo, SetUserInfo] = useState();
    
useEffect(()=>{
    axios.get("http://localhost:8000/getMachines/"+id
    ).then(response => {
        setMachine(response.data.data)
        console.log(response.data)

    }).catch(error => {
        console.log(error)
    })

},[]);
useEffect(() => {
    const username = localStorage.getItem("user");
    setName(username);
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
    return (
        <div className='machineinfo__container'>
            <div>
                {userInfo.map(user => (
                    <div key={user.first_name}>
                        <p>
                            {"UserName: "}
                            {user.first_name}
                        </p>
                        <p>
                            {"Time left On account (hours): "}
                            {user.time}
                       </p>
                    </div>
                ))}
                
                {machine.map(machine => (
                    <div key={machine.id}>
                       <p>
                            {"Machine Name: "}
                            {machine.name}
                        </p>
                        <p >
                            {"Machine Type: "}
                            {machine.machine_type}
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