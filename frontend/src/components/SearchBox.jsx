import { Autocomplete, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import { fetchAllRecipes } from "../api";

export default function SearchBox(props) {
  const { selectedRecipes, setSelectedRecipes } = props;

  const [searchList, setSearchList] = useState([]);
  const [value, setValue] = useState(null);
  const [loading, setLoading] = useState(false);

  // Hacky fix to fetch data if it has not already been fetched
  const [binaryState, setBinaryState] = useState(false);

  const selectionComplete = selectedRecipes.length >= 3;

  const handleSelectRecipe = (recipe) => {
    if (!recipe) return;
    if (selectionComplete) return;

    setSelectedRecipes([...selectedRecipes, recipe]);
    setValue(null);
  };

  useEffect(() => {
    async function fetchAndSetData() {
      if (loading) return;
      if (searchList.length !== 0) return;
      setLoading(true);

      const allRecipes = await fetchAllRecipes();
      setSearchList(allRecipes);
      setLoading(false);
    }

    return () => fetchAndSetData();
    // eslint-disable-next-line
  }, [binaryState]);

  return (
    <>
      {searchList && (
        <Autocomplete
          sx={{ width: 400 }}
          blurOnSelect
          disabled={selectionComplete}
          value={value}
          onChange={(event, val) => {
            handleSelectRecipe(val);
          }}
          onOpen={(event) => setBinaryState(!binaryState)}
          options={searchList}
          renderInput={(params) => (
            <TextField {...params} label="Search recipes" />
          )}
          renderOption={(props, option) => {
            return (
              <li {...props} key={option.id}>
                {option.label}
              </li>
            );
          }}
        />
      )}
      <ul>
        {selectedRecipes.map((recipe) => (
          <li key={recipe.id}>{recipe.label}</li>
        ))}
      </ul>
    </>
  );
}
