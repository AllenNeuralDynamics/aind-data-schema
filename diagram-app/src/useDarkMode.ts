import { useEffect, useState } from "react";

/** Furo (this site's Sphinx theme) sets `data-theme="light"|"dark"|"auto"` on <html>/<body>;
 * "auto" means "follow the OS", which prefers-color-scheme tells us directly. */
function resolveDarkMode(): boolean {
  const theme = document.documentElement.getAttribute("data-theme") || document.body.getAttribute("data-theme");
  if (theme === "dark") return true;
  if (theme === "light") return false;
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

export function useDarkMode(): boolean {
  const [isDark, setIsDark] = useState(resolveDarkMode);

  useEffect(() => {
    const update = () => setIsDark(resolveDarkMode());
    const media = window.matchMedia("(prefers-color-scheme: dark)");
    media.addEventListener("change", update);
    const observer = new MutationObserver(update);
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    observer.observe(document.body, { attributes: true, attributeFilter: ["data-theme"] });
    return () => {
      media.removeEventListener("change", update);
      observer.disconnect();
    };
  }, []);

  return isDark;
}
