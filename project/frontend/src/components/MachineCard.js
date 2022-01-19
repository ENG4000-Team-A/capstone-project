import { Card } from "@mui/material";
import React from "react";
import "./MachineCard.css";

// Reference https://mui.com/components/cards/#basic-card
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

/*
Image Source
Side note: calling an image from ../../public/ folder will not work because it falls outside of the project src/ directory.
Relative imports outside of src/ are not supported. You can either move the image into src/, or add a symlink to it from project's node_modules/

Images currently does not fit in to the card. Will resize it when dummy information are replaced.
*/

import ps5_logo from "../image/PS5_logo_placeholder.png";
import xboxSeriesXLogo from "../image/XBox_Series_placeholder.png"; // xbox version
import error from "../image/Error.png";

function Machine_Card_Selected() {
  alert("Clicked!");
}

function returnConsoleImage (console_name) {
  switch(console_name) {
    case "PS5": return ps5_logo;
    case "Xbox": return xboxSeriesXLogo;
    default: return error;
  }
}

function MachineCard() {

  // Dummy JSON object
  var consoleInformation = {
    "name": "PS5",
    "status": "Available",
    "image": returnConsoleImage("PS5"),
    "alt_text": "PS5 logo",
    "button_prompt": "Available"
  };


  return (
    // Part Division
    <div className="machinecard__container">
      Machine Machine Card for {consoleInformation.name}
      <Card sx={{ maxWidth: 250 }}>
        <CardMedia
          component="img"
          height="100"
          image={consoleInformation.image}
          alt={consoleInformation.alt_text}
        />

        {/* Show Text Content Here */}
        {/* <CardContent>
          <Typography variant="body2" color="text.secondary" align="center">
            {consoleInformation.status}
          </Typography>
        </CardContent> */}

        <div className="card__actions">
          <CardActions>
              {/* Does Certain Action When Button is Pressed! */}
              <Button
                variant="contained"
                onClick={() => {
                  Machine_Card_Selected();
                }}
              >
                {consoleInformation.button_prompt}
              </Button>
              
          </CardActions>
        </div>
      </Card>
    </div>
  );
}

export default MachineCard;