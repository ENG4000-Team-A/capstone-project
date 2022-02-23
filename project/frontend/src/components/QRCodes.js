import React from "react";
import ReactDOM from "react-dom";
import QRCode from "react-qr-code";
import Button from '@mui/material/Button';
import { useState, useEffect } from 'react'
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import axios from 'axios';
import { Fragment } from "react";
import { Table } from "reactstrap";


function GenerateQRCode() {

    const theme = createTheme({
        palette: {
            mode: 'dark'
        },
    });

    const [value, setValue] = useState('');

    const downloadQRCode = () => {
        const svg = document.getElementById("QRCode");
        const svgData = new XMLSerializer().serializeToString(svg);
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        const img = new Image();
        img.onload = () => {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
            const pngFile = canvas.toDataURL("image/png");
            const downloadLink = document.createElement("a");
            downloadLink.download = "QRCode " + value + ".png";
            downloadLink.href = `${pngFile}`;
            downloadLink.click();
        };
        img.src = `data:image/svg+xml;base64,${btoa(svgData)}`;
    };

    const [machines, setMachine] = useState([]);

    useEffect(() => {
        axios.get("http://localhost:8000/machines/"
        ).then(response => {
            setMachine(response.data.data)
            console.log(response.data)
        }).catch(error => {
            console.log(error)
        })

    }, []);

    const editMachines = () => {
        for (var i = 0; i < machines.length; i++) {
            delete machines[i]["active"]
            delete machines[i]["ip"]
            machines[i]["downloadLink"] = "http://localhost:3000/machines/" + machines[i]["id"]
        }
    };
    editMachines()

    return (
        <ThemeProvider theme={theme}>
            <Container component="main" maxWidth="xl">
                <CssBaseline />
                <Fragment>
                    <Table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Type</th>
                                <th>Generate QR Code</th>
                                <th>Download</th>

                            </tr>
                        </thead>
                        {machines.map((machine) => {
                            return (
                                <tbody>
                                    <tr>
                                        <td>{machine.id}</td>
                                        <td>{machine.name}</td>
                                        <td>{machine.machine_type}</td>
                                        <td>{<Button
                                            type="submit"
                                            fullWidth
                                            variant="contained"
                                            sx={{ mt: 3, mb: 2 }}
                                            onClick={() => {
                                                ReactDOM.render(<QRCode id="QRCode" value={machine.downloadLink} />, document.getElementById("qrcode"))
                                                setValue('id_' + machine.id + ", name_" + machine.name)
                                            }}
                                        >
                                            Generate QR Code
                                        </Button>}</td>

                                        <td>{<Button
                                            type="submit"
                                            fullWidth
                                            variant="contained"
                                            sx={{ mt: 3, mb: 2 }}
                                            onClick={() => {
                                                downloadQRCode()
                                            }}
                                        >
                                            Download
                                        </Button>}</td>

                                    </tr>
                                </tbody>
                            )
                        })}
                    </Table>
                </Fragment>

                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Typography component="h1" variant="h5">
                        QR Code
                    </Typography>
                </Box>

                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }} id="qrcode">
                </div>
            </Container>
        </ThemeProvider>
    );
}

export default GenerateQRCode