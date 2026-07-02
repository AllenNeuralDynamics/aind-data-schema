import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

/**
 * Viewer entry point. Mounts a read-only React Flow diagram into every
 * element with the `rf-schema-diagram` class. In the docs, such a <div> is
 * injected via a raw-HTML block on the front page.
 */
function mountAll() {
  const targets = document.querySelectorAll<HTMLElement>(".rf-schema-diagram");
  targets.forEach((el) => {
    if (el.dataset.mounted) return;
    el.dataset.mounted = "true";
    if (!el.style.height) el.style.height = "calc(620px + 20vh)";
    createRoot(el).render(
      <StrictMode>
        <App />
      </StrictMode>,
    );
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", mountAll);
} else {
  mountAll();
}
