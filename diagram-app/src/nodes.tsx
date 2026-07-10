import { Handle, Position, type NodeProps, type NodeTypes } from "@xyflow/react";
import { HEADER_H, ROW_H, isExpandable, type Side } from "./graph";
import type { ModelEntry } from "./types";

const FONT = '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
const MONO = '"SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace';
const CARD_SHADOW = "0 1px 2px rgba(15,23,42,0.08), 0 2px 6px rgba(15,23,42,0.10)";

export interface SchemaNodeData {
  model: ModelEntry;
  color: string;
  /** Fixed side for every field on this node, or null on the root (whose fields fan both ways). */
  side: Side | null;
  /** Only used when side is null (the root): per-field side, from Metadata's own core-file fields. */
  fieldSide?: Record<string, Side>;
  expandedFields: Set<string>;
  onToggleField: (fieldName: string) => void;
  [key: string]: unknown;
}

const HANDLE_STYLE = { opacity: 0, width: 1, height: 1, border: 0, minWidth: 0, minHeight: 0 };

export function SchemaNode({ id, data }: NodeProps) {
  const d = data as SchemaNodeData;
  const { model, color } = d;

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        boxSizing: "border-box",
        background: "var(--schema-card-bg, #fff)",
        border: `2px solid ${color}`,
        borderRadius: 8,
        boxShadow: CARD_SHADOW,
        fontFamily: FONT,
        overflow: "visible",
        position: "relative",
        // React Flow sets `pointer-events: none` on .react-flow__viewport (and everything
        // inside it) once nodesDraggable/nodesConnectable/elementsSelectable are all false —
        // it assumes nothing inside a node needs to be clickable. Our chevrons and doc links
        // do, so re-enable pointer events from here down.
        pointerEvents: "auto",
      }}
    >
      {d.side ? (
        <Handle
          type="target"
          id="in"
          position={d.side === "l" ? Position.Right : Position.Left}
          style={HANDLE_STYLE}
          isConnectable={false}
        />
      ) : null}

      <div
        style={{
          height: HEADER_H,
          boxSizing: "border-box",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 6,
          padding: "0 10px",
          background: color,
          color: "#fff",
          borderRadius: "5px 5px 0 0",
        }}
      >
        <strong style={{ fontSize: 13.5, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {model.name}
        </strong>
        {model.docUrl ? (
          <a
            href={model.docUrl}
            target="_blank"
            rel="noopener noreferrer"
            title="View in docs"
            className="nodrag nopan"
            style={{ color: "#fff", fontSize: 12, fontWeight: 700, flex: "0 0 auto", textDecoration: "none" }}
          >
            docs ↗
          </a>
        ) : null}
      </div>

      {model.fields.map((field, idx) => {
        const expandable = isExpandable(field);
        const fieldPath = `${id}::${field.name}`;
        const expanded = expandable && d.expandedFields.has(fieldPath);
        const outSide: Side = d.side ?? d.fieldSide?.[field.name] ?? "r";
        // Only show a row-level doc link when there's exactly one candidate type — for a
        // discriminated field, picking one of several options' docs would be misleading;
        // expanding it gives each option its own node with its own "docs" link instead.
        const docLink = field.links.length === 1 && field.links[0].url ? field.links[0] : undefined;

        return (
          <div
            key={field.name}
            onClick={expandable ? () => d.onToggleField(field.name) : undefined}
            title={`${field.typeStr}${field.description ? " — " + field.description : ""}`}
            className={expandable ? "nodrag nopan" : undefined}
            style={{
              position: "relative",
              height: ROW_H,
              boxSizing: "border-box",
              display: "flex",
              alignItems: "center",
              gap: 4,
              padding: "0 8px",
              fontSize: 12,
              borderTop: idx === 0 ? "none" : "1px solid var(--schema-card-divider, #f1f5f9)",
              cursor: expandable ? "pointer" : "default",
              background: expanded ? "var(--schema-card-highlight-bg, #eef2ff)" : "var(--schema-card-bg, #fff)",
            }}
          >
            {expandable ? (
              <span style={{ color, fontWeight: 700, fontSize: 18, width: 14, flex: "0 0 auto", lineHeight: 1 }}>
                {expanded ? "−" : "+"}
              </span>
            ) : (
              <span style={{ width: 14, flex: "0 0 auto" }} />
            )}
            <code style={{ fontFamily: MONO, fontSize: 11.5, color: "var(--schema-card-text, #111827)" }}>
              {field.name}
            </code>
            {field.required ? <span style={{ color: "#dc2626", fontWeight: 700 }}>*</span> : null}
            <span
              style={{
                marginLeft: "auto",
                fontSize: 10.5,
                color: "#6b7280",
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
                maxWidth: 110,
              }}
            >
              {field.typeStr}
            </span>
            {docLink ? (
              <a
                href={docLink.url}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => e.stopPropagation()}
                title={`Open ${docLink.label} in the docs`}
                className="nodrag nopan"
                style={{ color: "#4f46e5", fontSize: 11, fontWeight: 700, flex: "0 0 auto", textDecoration: "none" }}
              >
                ↗
              </a>
            ) : (
              <span style={{ width: 10, flex: "0 0 auto" }} />
            )}
            {expandable ? (
              <Handle
                type="source"
                id={`out-${field.name}`}
                position={outSide === "l" ? Position.Left : Position.Right}
                style={HANDLE_STYLE}
                isConnectable={false}
              />
            ) : null}
          </div>
        );
      })}
    </div>
  );
}

export const nodeTypes: NodeTypes = {
  schema: SchemaNode,
};
