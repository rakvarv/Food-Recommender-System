import { Typography } from "@mui/material";
import { useState } from "react";
import "./App.css";
import Form from "./components/Form";
import Result from "./components/Result";
import SearchBox from "./components/SearchBox";

function App() {
  const [recommendations, setRecommendations] = useState(null);
  const [selectedRecipes, setSelectedRecipes] = useState([]);

  return (
    <div className="app-container">
      <div>
        <Typography variant="h4">Student Recommender System</Typography>
        <br />
        <Typography variant="body1">
          Choose three recipes you would like
        </Typography>
        <br />
        <SearchBox
          selectedRecipes={selectedRecipes}
          setSelectedRecipes={setSelectedRecipes}
        />
        <br />
        <Form setRecommendations={setRecommendations} />
      </div>
      <div className="results">
        {recommendations && <Result recommendations={recommendations} />}
      </div>
    </div>
  );
}

export default App;
