import { Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import "./common.css";

export default function FinishPage() {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/");
  };

  return (
    <div className="page_root">
      <Typography variant="h4">Thank you for participating!</Typography>
      <br />
      <br />
      <Typography variant="h6">Your answers have been recorded.</Typography>
      <br />
      <br />
      <br />
      <br />
      <Button variant="contained" onClick={handleClick}>
        Back To Start
      </Button>
    </div>
  );
}
