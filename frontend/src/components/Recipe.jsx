import {
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  CardMedia,
  Rating,
  Typography,
} from "@mui/material";
import PaidIcon from "@mui/icons-material/Paid";
import PaidOutlinedIcon from "@mui/icons-material/PaidOutlined";
import StarIcon from "@mui/icons-material/Star";
import StarBorderOutlinedIcon from "@mui/icons-material/StarBorderOutlined";

export default function Recipe(props) {
  /* eslint-disable */
  const {
    cost,
    category,
    difficulty,
    bestRating,
    ratingCount,
    ratingValue,
    totalMinutes,
    url,
    imageURL,
    title,
    description,
  } = props;
  /* eslint-enable */

  return (
    <>
      <Card sx={{ maxWidth: 345 }}>
        <CardMedia component="img" height="194" image={imageURL} alt={title} />
        <CardHeader title={title} subheader={category} />
        <CardContent>
          <Typography variant="body2">{description}</Typography>
        </CardContent>
        <CardContent>
          <Rating
            readOnly
            value={ratingValue}
            icon={<StarIcon />}
            emptyIcon={<StarBorderOutlinedIcon />}
            size="small"
            precision={0.1}
            sx={{ color: "gold" }}
          />
          <br />
          <Rating
            readOnly
            value={cost}
            icon={<PaidIcon />}
            emptyIcon={<PaidOutlinedIcon />}
            size="small"
            sx={{ color: "green" }}
          />
        </CardContent>
        <CardActions>
          <Button
            href={url}
            rel="noopener noreferrer"
            target="_blank"
            size="small"
          >
            Go To Recipe
          </Button>
        </CardActions>
      </Card>
      <br />
    </>
  );
}
