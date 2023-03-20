import { Button, CircularProgress, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  fetchContentRecommendations,
  fetchKnowledgeRecommendations,
} from "../api";
import Result from "../components/Result";
import "./common.css";

export default function ResultsPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { state } = location;

  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState(null);

  const contentRecommendation = async () => {
    const { selectedRecipes } = state;

    try {
      const rec = await fetchContentRecommendations(selectedRecipes);
      setRecommendations(rec);
    } catch (error) {
      console.log(error);
    }
    setLoading(false);
  };

  const knowledgeRecommendation = async () => {
    const { cost, minutes, experience } = state;

    try {
      const rec = await fetchKnowledgeRecommendations(
        cost,
        experience,
        minutes
      );
      setRecommendations(rec);
    } catch (error) {
      console.log(error);
    }
    setLoading(false);
  };

  const handleSubmit = () => {
    const recommendedTitles = recommendations.map((x) => x.title);
    navigate("/questions", {
      state: { ...location.state, recommendations: recommendedTitles },
    });
  };

  useEffect(() => {
    if (recommendations || loading) return () => {};
    setLoading(true);
    const { fromPage } = state;

    if (fromPage === "A") {
      console.log("A");
      return () => contentRecommendation();
    }
    if (fromPage === "B") {
      console.log("B");
      return () => knowledgeRecommendation();
    }
    // eslint-disable-next-line
  }, [state]);

  return (
    <div className="page_root">
      <Typography variant="h4">Recipes Recommended for You</Typography>
      <br />
      <Typography variant="subtitle">
        Take a second to view your recommendations.
      </Typography>
      <br />
      <Typography variant="subtitle">
        Please scroll to the bottom for your last step.
      </Typography>
      <br />
      <br />
      {recommendations ? (
        <Result recommendations={recommendations} />
      ) : (
        <CircularProgress size="5em" />
      )}
      {recommendations && (
        <Button variant="contained" onClick={handleSubmit}>
          Go To Questionnaire
        </Button>
      )}
    </div>
  );
}
