/** Mirrors the JSON produced by aind_data_schema.utils.schema_tree.generate_schema_diagram_data */

export interface FieldLink {
  /** Model key to drill into in-app, or null if this type isn't a local model (e.g. an enum). */
  key: string | null;
  label: string;
  /** Docs page + anchor for this type, e.g. "components/devices.html#camera". */
  url: string;
}

export interface FieldEntry {
  name: string;
  title: string;
  typeStr: string;
  required: boolean;
  description: string;
  links: FieldLink[];
}

export interface ModelEntry {
  name: string;
  description: string;
  docUrl: string;
  fields: FieldEntry[];
}

export interface SchemaDiagramData {
  root: string;
  coreFiles: string[];
  models: Record<string, ModelEntry>;
}
