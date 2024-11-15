import React from "react";
import ReactDOM from "react-dom/client"; // Make sure to use 'react-dom/client' for React 18
import App from "./components/App";
import "./index.css";


const container = document.getElementById("root");
const root = ReactDOM.createRoot(container);
root.render(<App />);