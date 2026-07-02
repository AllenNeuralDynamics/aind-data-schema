import { useCallback, useEffect, useMemo, useRef, useState, type CSSProperties } from "react";
import {
  Background,
  Controls,
  Panel,
  ReactFlow,
  ReactFlowProvider,
  useReactFlow,
  type Edge,
  type Node,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { loadSchema } from "./loadSchema";
import { nodeTypes } from "./nodes";
import { edgeTypes } from "./edges";
import { useDarkMode } from "./useDarkMode";
import {
  branchOf,
  buildInstanceTree,
  computeFullExpansion,
  computePositions,
  estimateHeight,
  instanceOfFieldPath,
} from "./graph";
import type { SchemaDiagramData } from "./types";

/** Metadata's own core-file fields, each mapped to the side its branch was assigned
 * (needed because the root's fields fan out in both directions, unlike every other node). */
function rootFieldSides(schema: SchemaDiagramData): Record<string, "l" | "r"> {
  const sides: Record<string, "l" | "r"> = {};
  const half = Math.ceil(schema.coreFiles.length / 2);
  const sideByKey = new Map<string, "l" | "r">(schema.coreFiles.map((key, i) => [key, i < half ? "l" : "r"]));
  const rootModel = schema.models[schema.root];
  for (const field of rootModel?.fields ?? []) {
    const key = field.links.find((l) => l.key)?.key;
    if (key && sideByKey.has(key)) sides[field.name] = sideByKey.get(key)!;
  }
  return sides;
}

function Viewer() {
  const [schema, setSchema] = useState<SchemaDiagramData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expandedFields, setExpandedFields] = useState<Set<string>>(new Set());
  const [activeBranch, setActiveBranch] = useState<string | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);
  const { fitView } = useReactFlow();
  const isDark = useDarkMode();

  useEffect(() => {
    const onFullscreenChange = () => setIsFullscreen(document.fullscreenElement === wrapperRef.current);
    document.addEventListener("fullscreenchange", onFullscreenChange);
    return () => document.removeEventListener("fullscreenchange", onFullscreenChange);
  }, []);

  const toggleFullscreen = useCallback(() => {
    if (document.fullscreenElement) {
      document.exitFullscreen();
    } else {
      wrapperRef.current?.requestFullscreen();
    }
  }, []);

  useEffect(() => {
    let cancelled = false;
    loadSchema()
      .then((d) => !cancelled && setSchema(d))
      .catch((e) => !cancelled && setError(String(e)));
    return () => {
      cancelled = true;
    };
  }, []);

  const toggleField = useCallback((instanceId: string, fieldName: string) => {
    const fieldPath = `${instanceId}::${fieldName}`;
    setExpandedFields((prev) => {
      const next = new Set(prev);
      if (next.has(fieldPath)) next.delete(fieldPath);
      else next.add(fieldPath);
      return next;
    });
    setActiveBranch(branchOf(fieldPath));
  }, []);

  const onPaneClick = useCallback(() => {
    if (!activeBranch) return;
    setExpandedFields((prev) => {
      const next = new Set(prev);
      for (const fieldPath of prev) {
        if (branchOf(instanceOfFieldPath(fieldPath)) === activeBranch) next.delete(fieldPath);
      }
      return next;
    });
    setActiveBranch(null);
  }, [activeBranch]);

  const expandAll = useCallback(() => {
    if (!schema) return;
    setExpandedFields(computeFullExpansion(schema));
    setActiveBranch(null);
  }, [schema]);

  const collapseAll = useCallback(() => {
    setExpandedFields(new Set());
    setActiveBranch(null);
  }, []);

  const graph = useMemo(() => {
    if (!schema) return null;

    const { instances, edges: builtEdges } = buildInstanceTree(schema, expandedFields);
    const positions = computePositions(instances, builtEdges, schema);

    const rootSides = rootFieldSides(schema);
    const nodes: Node[] = instances.map((inst) => ({
      id: inst.id,
      type: "schema",
      position: positions.get(inst.id) ?? { x: 0, y: 0 },
      width: 280,
      height: estimateHeight(inst.modelKey, schema),
      data: {
        model: schema.models[inst.modelKey],
        color: inst.color,
        side: inst.side,
        fieldSide: inst.id === "root" ? rootSides : undefined,
        expandedFields,
        onToggleField: (fieldName: string) => toggleField(inst.id, fieldName),
      },
    }));

    const edges: Edge[] = builtEdges.map((e) => ({
      id: e.id,
      source: e.source,
      sourceHandle: e.sourceHandle,
      target: e.target,
      targetHandle: "in",
      type: "circuit",
      data: { lane: e.lane },
      style: { stroke: e.color, strokeWidth: 1.5 },
    }));

    return { nodes, edges };
  }, [schema, expandedFields, toggleField]);

  const hasFitOnce = useRef(false);

  useEffect(() => {
    // Only auto-frame once, right after the diagram first loads — expanding/collapsing fields
    // (including Expand/Collapse all) shouldn't yank the view away from wherever the user is.
    if (!graph || hasFitOnce.current) return;
    hasFitOnce.current = true;
    const raf = requestAnimationFrame(() => fitView({ padding: 0.15, maxZoom: 1 }));
    return () => cancelAnimationFrame(raf);
  }, [graph, fitView]);

  useEffect(() => {
    // Fullscreen toggling changes the actual viewport size, so it still warrants a re-frame.
    if (!hasFitOnce.current) return;
    const raf = requestAnimationFrame(() => fitView({ padding: 0.15, maxZoom: 1, duration: 300 }));
    return () => cancelAnimationFrame(raf);
  }, [isFullscreen, fitView]);

  if (error) {
    return (
      <div style={{ padding: 16, color: "#b91c1c", fontFamily: "sans-serif" }}>
        Failed to load schema diagram: {error}
      </div>
    );
  }
  if (!schema || !graph) {
    return <div style={{ padding: 16, fontFamily: "sans-serif", color: "#6b7280" }}>Loading schema diagram…</div>;
  }

  return (
    <div
      ref={wrapperRef}
      style={
        {
          width: "100%",
          height: isFullscreen ? "100vh" : "100%",
          background: "var(--schema-page-bg)",
          // Only the page/card backgrounds and body text invert — branch colors (headers,
          // borders, chevrons) are set directly per-node and are left alone.
          "--schema-page-bg": isDark ? "#000" : "#fff",
          "--schema-card-bg": isDark ? "#000" : "#fff",
          "--schema-card-text": isDark ? "#fff" : "#111827",
          "--schema-card-divider": isDark ? "#27272a" : "#f1f5f9",
          "--schema-card-highlight-bg": isDark ? "#1e1b4b" : "#eef2ff",
          "--schema-dot-color": isDark ? "#3f3f46" : "#91919a",
        } as CSSProperties
      }
    >
      <ReactFlow
        nodes={graph.nodes}
        edges={graph.edges}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        onPaneClick={onPaneClick}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
        // Low enough to fit the whole schema fully expanded (500+ nodes) in one fitView.
        minZoom={0.01}
        maxZoom={1.5}
        proOptions={{ hideAttribution: true }}
      >
        <Background color="var(--schema-dot-color)" />
        <Controls showInteractive={false} />
        <Panel position="top-right" style={{ display: "flex", gap: 8 }}>
          <button onClick={expandAll} style={panelButtonStyle}>
            Expand all
          </button>
          <button onClick={collapseAll} style={panelButtonStyle}>
            Collapse all
          </button>
          <button onClick={toggleFullscreen} style={panelButtonStyle}>
            {isFullscreen ? "Exit fullscreen" : "Fullscreen ⛶"}
          </button>
        </Panel>
      </ReactFlow>
    </div>
  );
}

const panelButtonStyle: CSSProperties = {
  fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  fontSize: 12,
  fontWeight: 600,
  padding: "6px 12px",
  borderRadius: 6,
  border: "1px solid #c7d2fe",
  background: "#fff",
  color: "#3730a3",
  cursor: "pointer",
  boxShadow: "0 1px 2px rgba(15,23,42,0.08)",
};

export default function App() {
  return (
    <ReactFlowProvider>
      <Viewer />
    </ReactFlowProvider>
  );
}
