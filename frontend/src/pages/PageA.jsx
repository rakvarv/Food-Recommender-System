import { Button, Typography } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import SearchBox from "../components/SearchBox";
import "./common.css";

export default function PageA() {
  const [selectedRecipes, setSelectedRecipes] = useState([]);
  const navigate = useNavigate();

  const ready = selectedRecipes.length >= 3;

  const handleSubmit = () => {
    if (!ready) return;

    const recipeTitles = selectedRecipes.map((x) => x.label);

    navigate("./results", {
      state: { fromPage: "A", selectedRecipes: recipeTitles },
    });
  };

  return (
    <div className="page_root">
      <Typography variant="h5">Choose three recipes you would like</Typography>
      <br />
      <Typography variant="subtitle1">
        Click or type in the searchbox to look for recipes
      </Typography>
      <br />
      <SearchBox
        selectedRecipes={selectedRecipes}
        setSelectedRecipes={setSelectedRecipes}
      />
      <Button variant="contained" onClick={handleSubmit}>
        Get Recommendations
      </Button>
    </div>
  );
}
