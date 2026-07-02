import type { SchemaDiagramData } from "./types";

// Capture this module's own URL so Vite does NOT rewrite the `new URL(...,
// import.meta.url)` call below into build-time static-asset resolution
// (which would break the runtime-resolved, sibling-file path in production).
const MODULE_URL = import.meta.url;

function schemaUrl(): string {
  if (import.meta.env.DEV) return "/schema_diagram.json";
  return new URL("./schema_diagram.json", MODULE_URL).href;
}

let cached: Promise<SchemaDiagramData> | null = null;

export function loadSchema(): Promise<SchemaDiagramData> {
  if (!cached) {
    cached = fetch(schemaUrl()).then((res) => {
      if (!res.ok) throw new Error(`Failed to load schema_diagram.json: ${res.status}`);
      return res.json() as Promise<SchemaDiagramData>;
    });
  }
  return cached;
}
