import React from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { UDOC_PACKAGE } from "./packageMode";
import "./styles.css";

document.documentElement.dataset.udocPackage = UDOC_PACKAGE;
if (typeof document !== "undefined") {
  if (!/Client/i.test(document.title || "")) {
    document.title = "UDOC Client · Tenant SaaS · G.O.D.S";
  }
}

/** Client package: when plane picker appears, enter Software only (no hardware). */
function armClientPlaneGate() {
  if (UDOC_PACKAGE !== "client") return;
  let armed = false;
  const tryEnter = () => {
    const sw = document.querySelector(".plane.sw") as HTMLElement | null;
    if (!sw || armed) return;
    // Only auto-click once after login when select screen is visible
    if (!document.querySelector(".select-h")) return;
    armed = true;
    sw.click();
  };
  const obs = new MutationObserver(() => tryEnter());
  obs.observe(document.body, { childList: true, subtree: true });
  // Reset arm on sign-out style full reloads is fine; soft nav re-arms when select returns
  setInterval(() => {
    if (document.querySelector(".select-h") && !document.querySelector(".tabs")) {
      armed = false;
      tryEnter();
    }
  }, 1200);
}

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

armClientPlaneGate();
