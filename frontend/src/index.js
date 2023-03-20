import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";
import Home from "./pages/Home";
import PageA from "./pages/PageA";
import ResultsPage from "./pages/ResultsPage";
import PageB from "./pages/PageB";
import QuestionPage from "./pages/QuestionPage";
import FinishPage from "./pages/FinishPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/recA",
    element: <PageA />,
  },
  {
    path: "/recA/results",
    element: <ResultsPage />,
  },
  {
    path: "/recB",
    element: <PageB />,
  },
  {
    path: "/recB/results",
    element: <ResultsPage />,
  },
  {
    path: "/questions",
    element: <QuestionPage />,
  },
  {
    path: "/finish",
    element: <FinishPage />,
  },
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
