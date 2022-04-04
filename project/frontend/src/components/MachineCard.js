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

import playstationLogo from "../image/Playstation_1280x_720.jpg";
import xboxLogo from "../image/Xbox_1280x_720.jpg"; // xbox version
import nintendoLogo from "../image/Nintendo_1280x_720.jpg";
import arcadeLogo from "../image/Arcade_1280x_720.jpg";
import error from "../image/Error_1280x_720.jpg";

import { useNavigate } from "react-router-dom";

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

function returnStatus (status) {
  switch(status) {
    case false: return "Available";
    case true: return "Unavailable"
  }
}


function MachineCard({machineId,name,status,machineType, screenWidth, screenHeight,...props}) {
 
  let navigate = useNavigate();

  function Machine_Card_Selected() {
    navigate(`/machines/${machineId}`);
  }

  var cardHeight;

  // considered a modest sized screen
  // cards will shrink a bit for if the dimension is quite small. Is done to prevent having too large of a card rendered on a mobile.
  if (screenWidth > 700 && screenHeight > 500 ) {
    cardHeight = "200";
  } else {
    cardHeight = "125";
  }

  

  return (

    // Part Division
    <div className="machinecard__container">
    
      <Card variant="outlined" sx={{ maxWidth: 500 }}>
        <CardMedia
          component="img"
          height={cardHeight}
          image={returnConsoleImage(machineType)}
          alt="logo"
        />

        <div className="machinecardName__container">
          <Typography variant="h5">
          {name}
          </Typography>

        </div>
      
        <div className="card__actions">
          <CardActions>
              {/* Does Certain Action When Button is Pressed! */}
              <Button
                variant="contained"
                fullWidth
                onClick={() => {
                  Machine_Card_Selected();
                }}
                disabled={status}
              >
                {/* Available */}
                {String(returnStatus(status))}
              </Button>
              
          </CardActions>
        </div>
      </Card>
    </div>
  );
}

export default MachineCard;