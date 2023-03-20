import {
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Slider,
  Typography,
} from "@mui/material";
import { PRICES, EXPERIENCE } from "../constants";

export default function Form(props) {
  const {
    cost,
    setCost,
    experience,
    setExperience,
    setMinutes,
    minutesDefault,
  } = props;

  return (
    <>
      <Typography variant="subtitle1">
        What is the highest amount of money you would like to spend?
      </Typography>
      <div style={{ width: "200px" }}>
        <FormControl fullWidth>
          <InputLabel>Cost</InputLabel>
          <Select
            label="Cost"
            value={cost ?? ""}
            onChange={(e) => setCost(e.target.value)}
          >
            {PRICES.map((price) => (
              <MenuItem key={price.value} value={price.value}>
                {price.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </div>
      <br />
      <Typography variant="subtitle1">
        What is your experience level in cooking?
      </Typography>
      <div style={{ width: "200px" }}>
        <FormControl fullWidth>
          <InputLabel>Experience</InputLabel>
          <Select
            label="Experience"
            value={experience ?? ""}
            onChange={(e) => setExperience(e.target.value)}
          >
            {EXPERIENCE.map((experience) => (
              <MenuItem key={experience.value} value={experience.value}>
                {experience.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </div>
      <br />
      <Typography variant="subtitle1">
        In minutes, how long from start to finish should the recipes take?
      </Typography>
      <div style={{ width: "200px" }}>
        <Slider
          defaultValue={minutesDefault}
          valueLabelDisplay="auto"
          step={5}
          marks
          min={10}
          max={120}
          onChange={(e) => setMinutes(e.target.value)}
        />
      </div>
      <br />
    </>
  );
}
