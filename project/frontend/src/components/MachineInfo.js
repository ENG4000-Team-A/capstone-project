import React, { useState, useEffect } from 'react'
import './MachineInfo.css'
import { useParams } from 'react-router-dom'
import Button from '@mui/material/Button';
import axios from 'axios';
import { Alert } from '@mui/material';
import { AlertTitle } from '@mui/material'
import CardMedia from "@mui/material/CardMedia";
import { Card } from "@mui/material";
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Box from '@mui/material/Box';


// Image Exportation
import playstationLogo from "../image/Playstation_1280x_720.jpg";
import xboxLogo from "../image/Xbox_1280x_720.jpg"; // xbox version
import nintendoLogo from "../image/Nintendo_1280x_720.jpg";
import arcadeLogo from "../image/Arcade_1280x_720.jpg";
import error from "../image/Error_1280x_720.jpg";

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
        axios.get('http://localhost:8000/users/',
            {
                headers: {
                    Authorization: localStorage.getItem("authToken")
                }
            }
        )
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

                    <div className="errorMessage__container">
                    <Alert severity="error" >
                        <AlertTitle>Error</AlertTitle>
                        You must Purchase time on your account to play
                    </Alert>
                        </div>

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
            },
                {
                    headers: {
                        Authorization: localStorage.getItem("authToken")
                    }
                }
            ).then(function (response) {
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
            case "PS3": return playstationLogo;
            case "PS4": return playstationLogo;
            case "PS5": return playstationLogo;
            case "Xbox One": return xboxLogo;
            case "Xbox One S": return xboxLogo;
            case "Xbox One X": return xboxLogo;
            case "Xbox Series X": return xboxLogo;
            case "Nintendo Switch": return nintendoLogo;
            case "Wii U": return nintendoLogo;
            case "Arcade": return arcadeLogo;
            default: return error;
        }
      }

    return (

        <div id="infoBox">

            {auth &&
                <Paper
                    sx={{
                        p: 0,
                        margin: 'auto',
                        padding: '30px',
                        maxWidth: 500,
                        flexGrow: 1,
                        backgroundColor: (theme) =>
                            theme.palette.mode === 'dark',
                    }}
                >
                    <Grid item xs container direction="column">
                        <Grid container spacing={4}>
                            <Grid item xs={12}>

                                <Card variant="outlined" sx={{ maxWidth: 500 }}>
                                    <CardMedia
                                        component="img"
                                        height="200"
                                        image={returnConsoleImage(machine.machine_type)}
                                        alt="logo"
                                    />
                                </Card>

                            </Grid>
                            <Grid item xs={12}>
                                {"Username : "}
                                {userInfo.first_name}
                            </Grid>
                            <Grid item xs={12}>
                                {"Time Left On Account : "}
                                {(userInfo.time / 60).toFixed(1)}
                                {" Minutes"}
                            </Grid>
                            <Grid item xs={12}>
                                {"Machine Name : "}
                                {machine.name}
                            </Grid>
                            <Grid item xs={12}>
                                {"Machine Type : "}
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