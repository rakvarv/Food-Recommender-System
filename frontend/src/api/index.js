export async function fetchKnowledgeRecommendations(cost, experience, minutes) {
  const response = await fetch("/api/recommend/knowledge", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      maxPrice: Number(cost),
      maxMinutes: Number(minutes),
      maxDifficulty: Number(experience),
    }),
  });

  if (!response.ok) throw new Error(response.statusText);

  const content = await response.json();

  console.log(content);
  return content;
}

export async function fetchContentRecommendations(recipeTitles) {
  const response = await fetch("/api/recommend/content", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      recipeTitles: recipeTitles,
    }),
  });

  if (!response.ok) throw new Error(response.statusText);

  const content = await response.json();

  console.log(content);
  return content;
}

export async function fetchAllRecipes() {
  const response = await fetch("/api/list", {
    method: "GET",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) throw new Error(response.statusText);

  const content: [{ label: String, id: Number }] = await response.json();

  console.log(content);
  return content;
}

export async function postAnswers(fromPage, answers, payload, recommendations) {
  const response = await fetch("/api/submit", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      fromPage: fromPage,
      answers: answers,
      payload: payload,
      recommendations: recommendations,
    }),
  });

  if (!response.ok) throw new Error(response.statusText);

  return response.ok;
}
