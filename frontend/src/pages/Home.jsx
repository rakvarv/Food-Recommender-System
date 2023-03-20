import { Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import "./common.css";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="page_root">
      <Typography variant="h4">Student Food Recommender System</Typography>
      <br />
      <Typography variant="subtitle">Please select either A or B</Typography>
      <br />
      <Button
        className="home_button"
        variant="contained"
        onClick={() => navigate("/recA")}
      >
        A
      </Button>
      <br />
      <Button
        className="home_button"
        variant="contained"
        onClick={() => navigate("/recB")}
      >
        B
      </Button>
    </div>
  );
}
