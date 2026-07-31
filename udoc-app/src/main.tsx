import React from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { UDOC_PACKAGE } from "./packageMode";
import "./styles.css";

document.documentElement.dataset.udocPackage = UDOC_PACKAGE;
if (typeof document !== "undefined" && document.title && !/Client/i.test(document.title)) {
  document.title = "UDOC Client · Tenant SaaS · G.O.D.S";
}

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
