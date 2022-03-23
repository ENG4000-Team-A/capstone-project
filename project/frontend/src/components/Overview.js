import React, { useState, useEffect } from 'react'
import './Overview.css'
import MachineCard from './MachineCard.js';
import axios from 'axios';
import { Navigate } from "react-router-dom";

function Overview({ auth }) {

    const [machines, setMachine] = useState([]);

    const [dimensions, setDimensions] = React.useState({
        height: window.innerHeight,
        width: window.innerWidth
    })
    React.useEffect(() => {
        function handleResize() {
            setDimensions({
                height: window.innerHeight,
                width: window.innerWidth
            })

        }

        window.addEventListener('resize', handleResize)

        return _ => {
            window.removeEventListener('resize', handleResize)

        }
    })


    useEffect(() => {
        axios.get("http://localhost:8000/machines/"
        ).then(response => {
            setMachine(response.data.data)
            console.log(response.data)

        }).catch(error => {
            console.log(error)
        })

    }, []);

    return (
        <div className='overview__container'>
            {auth &&
                machines.map((machine) => (
                    <MachineCard machineId={machine.id} name={machine.name} status={machine.active} machineType={machine.machine_type} 
                    screenWidth={dimensions.width} screenHeight={dimensions.height} ></MachineCard>
                ))
            }
            {!auth &&
                // Enforce Login. Send back user to its original?
                // <Navigate to="/login"></Navigate> 
                <div>Please login</div>
            }
        </div>
    )
}

export default Overview
