import { Button, Typography } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Form from "../components/Form";
import "./common.css";

export default function PageB() {
  const navigate = useNavigate();

  const minutesDefault = 30;

  const [cost, setCost] = useState(null);
  const [experience, setExperience] = useState(null);
  const [minutes, setMinutes] = useState(minutesDefault);

  const ready = cost && experience && minutes;

  const handleSubmit = () => {
    if (!ready) return;

    navigate("./results", {
      state: {
        fromPage: "B",
        cost: cost,
        experience: experience,
        minutes: minutes,
      },
    });
  };

  return (
    <div className="page_root">
      <Typography variant="h5">
        Enter your user preferences for recipes to recommend
      </Typography>
      <br />
      <Form
        cost={cost}
        setCost={setCost}
        experience={experience}
        setExperience={setExperience}
        minutes={minutes}
        setMinutes={setMinutes}
        minutesDefault={minutesDefault}
      />
      <Button variant="contained" onClick={handleSubmit}>
        Get Recommendations
      </Button>
    </div>
  );
}
