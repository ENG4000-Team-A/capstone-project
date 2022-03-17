import React, { useState, useEffect } from 'react'
import './MachineInfo.css'
import { useParams } from 'react-router-dom'
import Button from '@mui/material/Button';
import axios from 'axios';
import { Alert } from '@mui/material';
import { AlertTitle } from '@mui/material'
import ps5_logo from "../image/PS5_logo_placeholder.png";
import xboxSeriesXLogo from "../image/XBox_Series_placeholder.png"; // xbox version
import CardMedia from "@mui/material/CardMedia";
import { Card } from "@mui/material";
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Box from '@mui/material/Box';

function MachineInfo({ auth }) {
    const { id } = useParams()
    const [machine, setMachine] = useState({});
    const [userInfo, SetUserInfo] = useState({});
    const theme = createTheme({
        palette: {
            mode: 'dark'
        },
    });
    useEffect(() => {
        axios.get("http://localhost:8000/machines/?id=" + id
        ).then(response => {
            setMachine(response.data.data)
            console.log(response.data.data)

        }).catch(error => {
            console.log(error)
        })

    }, []);
    useEffect(() => {
        const username = localStorage.getItem("user");
        //setName(username);
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

    function Renderbutton() {
        /**
         * This function simply redirects to the timer page.
         * No data needs to be passed as user data is stored in cache
         */

        if (userInfo.time == 0.0) {
            console.log("cant start")

            return (
                <div body>
                    <Button variant="contained" button disabled={true} color="success" onClick={SubmitPlay}>
                        Start Playing
                    </Button>

                    <Alert text-align="center" severity="error">
                        <AlertTitle>Error</AlertTitle>
                        You must Purchase time on your account to play
                    </Alert>
                </div>
            )
        }
        else {
            return (
                <Button variant="contained" color="success" onClick={SubmitPlay}>
                    Start Playing
                </Button>
            )

        }
        function SubmitPlay() {
            axios.post("http://localhost:8000/start_timer/" + id, {
                uname: userInfo.username
            }).then(function (response) {
                console.log(response);
                var getUrl = window.location;
                var redirect = getUrl.protocol + "//" + getUrl.host + "/" + "timer";
                window.location.assign(redirect);
            })
                .catch(function (error) {
                    console.log(error);
                });
        }
    }
    function returnConsoleImage(console_name) {
        switch (console_name) {
            case "PS5": return ps5_logo;
            case "Xbox 1": return xboxSeriesXLogo;

        }
    }

    return (

        <div >

            {auth &&
                <Paper
                    sx={{
                        p: 0,
                        margin: 'auto',
                        maxWidth: 500,
                        flexGrow: 1,
                        backgroundColor: (theme) =>
                            theme.palette.mode === 'dark',
                    }}
                >
                    <Grid item xs container direction="column">
                        <Grid container spacing={4}>
                            <Grid item xs={12}>

                                <Card sx={{ maxWidth: 5000 }}>
                                    <CardMedia
                                        component="img"
                                        height="100"
                                        image={returnConsoleImage(machine.machine_type)}
                                        alt="logo"
                                    />
                                </Card>

                            </Grid>
                            <Grid item xs={12}>
                                {"UserName: "}
                                {userInfo.first_name}
                            </Grid>
                            <Grid item xs={12}>
                                {"Time left On account (minutes): "}
                                {(userInfo.time / 60).toFixed(1)}
                            </Grid>
                            <Grid item xs={12}>
                                {"Machine Name: "}
                                {machine.name}
                            </Grid>
                            <Grid item xs={12}>
                                {"Machine Type: "}
                                {machine.machine_type}
                            </Grid>
                            <Grid item xs={12}>
                                <Renderbutton />
                            </Grid>
                        </Grid>
                    </Grid>
                </Paper>

            }
            {!auth &&
                <div>Please login</div>
            }

        </div>

    )
}

export default MachineInfo