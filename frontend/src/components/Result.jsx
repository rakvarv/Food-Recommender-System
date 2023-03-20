import Recipe from "./Recipe";

export default function Result(props) {
  const { recommendations } = props;

  return (
    <>
      {recommendations.map((rec) => (
        <Recipe key={rec.url} {...rec} />
      ))}
    </>
  );
}
