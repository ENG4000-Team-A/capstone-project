import React, {useState, useEffect} from 'react'
import './Overview.css'
import MachineCard from './MachineCard.js';
import axios from 'axios';

function Overview() {

    const [machines, setMachine] = useState([]);

    useEffect(()=>{
        axios.get("http://localhost:8000/machines/"
        ).then(response => {
            setMachine(response.data.data)
            console.log(response.data)

        }).catch(error => {
            console.log(error)
        })
    
    },[]);

    return (
        <div className='overview__container'>
            { machines.map((machine) => (
                <MachineCard machineId={machine.id} name={machine.name} status={machine.active} machineType={machine.machine_type} ></MachineCard>
            )) }
        </div>
    )
}

export default Overview
