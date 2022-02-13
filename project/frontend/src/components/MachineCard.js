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

import { useNavigate } from "react-router-dom";




function returnConsoleImage (console_name) {
  switch(console_name) {
    case "PS4": return ps5_logo;
    case "Xbox 1": return xboxSeriesXLogo;
    default: return error;
  }
}

function MachineCard({machineId,name,status,machineType,...props}) {
 
  let navigate = useNavigate();

  function Machine_Card_Selected() {
    navigate(`/machines/${machineId}`);
  }

  return (

    // Part Division
    <div className="machinecard__container">
       {name}
      <Card sx={{ maxWidth: 500 }}>
        <CardMedia
          component="img"
          height="100"
          image={returnConsoleImage(machineType)}
          alt="logo"
        />
        Status: {String(status)}

        <div className="card__actions">
          <CardActions>
              {/* Does Certain Action When Button is Pressed! */}
              <Button
                variant="contained"
                onClick={() => {
                  Machine_Card_Selected();
                }}
                disabled={status}
              >
                Available
              </Button>
              
          </CardActions>
        </div>
      </Card>
    </div>
  );
}

export default MachineCard;