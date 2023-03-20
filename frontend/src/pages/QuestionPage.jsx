import { Button, Slider, Typography } from "@mui/material";
import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { postAnswers } from "../api";
import { QUESTIONS } from "../constants";
import "./common.css";

export default function QuestionPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { state } = location;

  const minValue = 0;
  const maxValue = 10;
  const defaultValue = 5;

  const answersDefault = {
    satisfaction: null,
    easeOfUse: null,
    understanding: null,
  };

  const [answers, setAnswers] = useState(answersDefault);
  const ready =
    answers.satisfaction && answers.easeOfUse && answers.understanding;

  const handleChange = (e, label) => {
    const val = e.target.value;

    setAnswers({ ...answers, [label]: val });
  };

  const handleSubmit = async () => {
    if (!ready) return;
    const { fromPage, recommendations } = state;

    let payload;

    if (fromPage === "A") {
      payload = {
        recipe1: state.selectedRecipes[0],
        recipe2: state.selectedRecipes[1],
        recipe3: state.selectedRecipes[2],
      };
    } else {
      payload = {
        cost: state.cost,
        experience: state.experience,
        minutes: state.minutes,
      };
    }

    try {
      await postAnswers(fromPage, answers, payload, recommendations);
      navigate("/finish");
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="page_root">
      <Typography variant="h4">Please answers these three questions</Typography>
      <br />
      <br />
      {QUESTIONS.map((x) => {
        return (
          <>
            <Typography variant="h6">{x.display}</Typography>
            <Typography variant="subtitle1">{x.value}</Typography>
            <div style={{ width: "200px" }}>
              <Slider
                key={x.label}
                defaultValue={defaultValue}
                valueLabelDisplay="auto"
                step={1}
                marks
                min={minValue}
                max={maxValue}
                onChange={(e) => handleChange(e, x.label)}
              />
            </div>
            <br />
          </>
        );
      })}

      <Button variant="contained" disabled={!ready} onClick={handleSubmit}>
        Submit Answers
      </Button>
    </div>
  );
}
