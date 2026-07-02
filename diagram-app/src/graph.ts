import dagre from "dagre";
import type { FieldEntry, SchemaDiagramData } from "./types";

/** Layout constants shared between graph building and node rendering. */
export const NODE_WIDTH = 280;
export const HEADER_H = 34;
export const ROW_H = 26;
export const PADDING_BOTTOM = 6;
// Base column gap when a node has no lanes at all — the per-node clearance below (based on
// how many lanes it actually needs) is added on top of this per rank transition.
const RANK_SEP = 50;
const NODE_SEP = 20;
const MIN_GAP = 16;
export const ROOT_COLOR = "#334155";
export const BASE_TURN = 24;
export const LANE_STEP = 16;
// Extra breathing room past the farthest lane's turn point, so a line's horizontal run ends
// clear of the next column's card instead of grazing (or running behind) its edge.
const CLEARANCE_BUFFER = 24;

export type Side = "l" | "r";

export interface Instance {
  id: string;
  modelKey: string;
  parentId: string | null;
  side: Side | null;
  color: string;
}

export interface BuiltEdge {
  id: string;
  source: string;
  sourceHandle: string;
  target: string;
  color: string;
  /** How far out this edge's turn point sits relative to its siblings (0 = closest in). Used
   * to stagger how far each line runs before it turns, so parallel lines leaving a large node
   * (like Metadata) don't overlap right as they exit. Assigned by assignLanes, not at
   * construction time — see there for why. */
  lane: number;
}

/** How far past a node's own edge its outgoing lines need to run before they turn — driven by
 * the farthest lane among edges leaving that node (optionally restricted to one side), plus a
 * fixed buffer. Zero if the node has no outgoing edges (on that side). */
function outwardClearance(instanceId: string, edges: BuiltEdge[], side?: Side, instancesById?: Map<string, Instance>) {
  let maxLane = -1;
  for (const e of edges) {
    if (e.source !== instanceId) continue;
    if (side && instancesById?.get(e.target)?.side !== side) continue;
    maxLane = Math.max(maxLane, e.lane);
  }
  return maxLane < 0 ? 0 : BASE_TURN + maxLane * LANE_STEP + CLEARANCE_BUFFER;
}

/** The model keys a field can resolve to that are drillable in-app (i.e. have a `key`). */
function fieldKeys(field: FieldEntry): string[] {
  return field.links.filter((l) => l.key).map((l) => l.key as string);
}

/** Any field with a drillable type is click-to-expand — whether it resolves to exactly one
 * type or is a discriminated union of several. Only Metadata's own core-file links start out
 * already expanded (see computeSeedExpansion); everything else starts collapsed. */
export function isExpandable(field: FieldEntry): boolean {
  return fieldKeys(field).length > 0;
}

export function branchColor(index: number, total: number): string {
  const hue = Math.round((360 * index) / total);
  return `hsl(${hue}, 60%, 40%)`;
}

/** Recover the instance id a field path belongs to (a field path is `${instanceId}::${fieldName}`). */
export function instanceOfFieldPath(fieldPath: string): string {
  return fieldPath.slice(0, fieldPath.lastIndexOf("::"));
}

/** The top-level core-file branch an instance/field path belongs to, or null for the root itself. */
export function branchOf(id: string): string | null {
  if (id === "root") return null;
  const parts = id.split("::");
  return parts[1];
}

export function estimateHeight(modelKey: string, schema: SchemaDiagramData): number {
  const model = schema.models[modelKey];
  const count = model ? model.fields.length : 0;
  return HEADER_H + count * ROW_H + PADDING_BOTTOM;
}

/** Map each of Metadata's own core-file fields to a side/color, so the initial fan-out out of
 * the root is balanced left/right instead of every instance needing its own side assignment. */
function coreFieldAssignments(schema: SchemaDiagramData): Map<string, { side: Side; color: string }> {
  const half = Math.ceil(schema.coreFiles.length / 2);
  const sideByKey = new Map<string, Side>();
  const colorByKey = new Map<string, string>();
  schema.coreFiles.forEach((key, i) => {
    sideByKey.set(key, i < half ? "l" : "r");
    colorByKey.set(key, branchColor(i, schema.coreFiles.length));
  });

  const assignments = new Map<string, { side: Side; color: string }>();
  const rootModel = schema.models[schema.root];
  for (const field of rootModel?.fields ?? []) {
    const keys = fieldKeys(field);
    if (keys.length === 1 && sideByKey.has(keys[0])) {
      assignments.set(field.name, { side: sideByKey.get(keys[0])!, color: colorByKey.get(keys[0])! });
    }
  }
  return assignments;
}

/** Every field path that starts out already expanded: just Metadata's own core-file links.
 * Everything past that — even a field with only one possible type — takes a click. */
export function computeSeedExpansion(schema: SchemaDiagramData): Set<string> {
  const seed = new Set<string>();
  const rootModel = schema.models[schema.root];
  for (const field of rootModel?.fields ?? []) {
    if (isExpandable(field)) seed.add(`root::${field.name}`);
  }
  return seed;
}

/** Build the instances/edges currently visible: a field is only followed if its path is in
 * `expandedFields` (see computeSeedExpansion for what starts there by default). */
export function buildInstanceTree(
  schema: SchemaDiagramData,
  expandedFields: Set<string>,
): { instances: Instance[]; edges: BuiltEdge[] } {
  const instances: Instance[] = [];
  const edges: BuiltEdge[] = [];
  const coreAssignments = coreFieldAssignments(schema);

  const root: Instance = { id: "root", modelKey: schema.root, parentId: null, side: null, color: ROOT_COLOR };
  instances.push(root);

  function fieldSideColor(parent: Instance, fieldName: string): { side: Side; color: string } {
    const override = parent.id === "root" ? coreAssignments.get(fieldName) : undefined;
    return { side: override?.side ?? parent.side ?? "r", color: override?.color ?? parent.color };
  }

  // Lane is a placeholder here (assigned properly later, in assignLanes, once each instance's
  // vertical position — and so whether a given edge heads up or down — is actually known).
  function addChild(parent: Instance, field: FieldEntry, key: string, idx: number) {
    const id = `${parent.id}::${field.name}::${idx}`;
    const { side, color } = fieldSideColor(parent, field.name);
    const child: Instance = { id, modelKey: key, parentId: parent.id, side, color };
    instances.push(child);
    edges.push({ id, source: parent.id, sourceHandle: `out-${field.name}`, target: id, color, lane: 0 });
    walk(child);
  }

  function walk(instance: Instance) {
    const model = schema.models[instance.modelKey];
    if (!model) return;
    for (const field of model.fields) {
      const keys = fieldKeys(field);
      if (keys.length === 0) continue;
      const fieldPath = `${instance.id}::${field.name}`;
      if (!expandedFields.has(fieldPath)) continue;
      keys.forEach((key, idx) => addChild(instance, field, key, idx));
    }
  }

  walk(root);
  return { instances, edges };
}

/** Every expandable field path reachable from the root, expanded all the way down. Guards
 * against a model appearing in its own ancestor chain, defensively — the current schema is a
 * DAG, but this keeps a future cyclic reference from causing infinite recursion. */
export function computeFullExpansion(schema: SchemaDiagramData): Set<string> {
  const expanded = new Set<string>();

  function walk(instanceId: string, modelKey: string, ancestors: Set<string>) {
    const model = schema.models[modelKey];
    if (!model) return;
    for (const field of model.fields) {
      const keys = fieldKeys(field);
      if (keys.length === 0) continue;
      const fieldPath = `${instanceId}::${field.name}`;
      expanded.add(fieldPath);
      keys.forEach((key, idx) => {
        if (ancestors.has(key)) return;
        walk(`${fieldPath}::${idx}`, key, new Set(ancestors).add(key));
      });
    }
  }

  walk("root", schema.root, new Set([schema.root]));
  return expanded;
}

/**
 * Assign each edge's lane, given every instance's (already known) vertical center.
 *
 * A lane that only ever grows with row order overlaps once a card's lines head in both
 * directions: a line leaving near the top of a card but heading further *down* than lines
 * below it has to run past its own card's body to get there, and needs to be pushed out
 * *farther* than lines that leave lower down — the opposite of row order. So each source's
 * edges (per side) are split by direction and staggered outward from the direction switch:
 * lines heading up get farther out the closer their row is to the switchover, and lines
 * heading down start at their farthest right after the switchover and come back in below it.
 */
function assignLanes(
  instances: Instance[],
  edges: BuiltEdge[],
  schema: SchemaDiagramData,
  instancesById: Map<string, Instance>,
  centerY: Map<string, number>,
) {
  for (const side of ["l", "r"] as Side[]) {
    const bySource = new Map<string, BuiltEdge[]>();
    for (const e of edges) {
      if (instancesById.get(e.target)?.side !== side) continue;
      const group = bySource.get(e.source) ?? [];
      group.push(e);
      bySource.set(e.source, group);
    }

    for (const [sourceId, group] of bySource) {
      const source = instancesById.get(sourceId);
      const sourceModel = source ? schema.models[source.modelKey] : undefined;
      const sourceTop = (centerY.get(sourceId) ?? 0) - (source ? estimateHeight(source.modelKey, schema) : 0) / 2;

      const withDirection = group.map((edge) => {
        const fieldName = edge.sourceHandle.replace(/^out-/, "");
        const rowIndex = Math.max(0, sourceModel?.fields.findIndex((f) => f.name === fieldName) ?? 0);
        const rowY = sourceTop + HEADER_H + rowIndex * ROW_H + ROW_H / 2;
        const targetCenterY = centerY.get(edge.target) ?? 0;
        return { edge, isUp: targetCenterY < rowY };
      });

      const upGroup = withDirection.filter((w) => w.isUp);
      const downGroup = withDirection.filter((w) => !w.isUp);
      upGroup.forEach((w, i) => (w.edge.lane = i));
      downGroup.forEach((w, i) => (w.edge.lane = downGroup.length - 1 - i));
    }
  }
}

/** Lay out one side's subtree with dagre (rankdir LR), then mirror/offset it so rank 0 sits at
 * ±colX and deeper ranks extend further outward — and recenter it so its top-level nodes
 * straddle y=0, keeping the root vertically centered regardless of how lopsided the two sides are.
 *
 * Each node's dagre width is inflated by its own outward clearance (how far its busiest lane
 * needs to run before turning), so dagre's normal rank-spacing pushes the *entire* next column
 * out far enough — not just the one busy card, since every node sharing that rank sits at the
 * same rank position anyway. `applyClearance` is off for the preliminary pass (see
 * computePositions) since lanes aren't known yet at that point. */
function layoutSide(
  instances: Instance[],
  edges: BuiltEdge[],
  schema: SchemaDiagramData,
  side: Side,
  instancesById: Map<string, Instance>,
  colX: number,
  applyClearance: boolean,
) {
  const group = instances.filter((i) => i.side === side);
  const positions = new Map<string, { x: number; y: number }>();
  if (group.length === 0) return positions;

  const g = new dagre.graphlib.Graph();
  g.setGraph({ rankdir: "LR", nodesep: NODE_SEP, ranksep: RANK_SEP });
  g.setDefaultEdgeLabel(() => ({}));
  const idSet = new Set(group.map((i) => i.id));
  group.forEach((i) => {
    const clearance = applyClearance ? outwardClearance(i.id, edges, side, instancesById) : 0;
    g.setNode(i.id, { width: NODE_WIDTH + 2 * clearance, height: estimateHeight(i.modelKey, schema) });
  });
  edges.forEach((e) => {
    if (idSet.has(e.source) && idSet.has(e.target)) g.setEdge(e.source, e.target);
  });
  dagre.layout(g);

  const topLevel = group.filter((i) => i.parentId === "root");
  const refX = topLevel.length ? g.node(topLevel[0].id).x : 0;
  const avgY = topLevel.length ? topLevel.reduce((sum, i) => sum + g.node(i.id).y, 0) / topLevel.length : 0;

  group.forEach((i) => {
    const n = g.node(i.id);
    const dx = n.x - refX;
    const x = side === "l" ? -colX - dx : colX + dx;
    positions.set(i.id, { x, y: n.y - avgY });
  });
  return positions;
}

/** Top-left position (React Flow convention) for every instance, keyed by instance id. */
export function computePositions(
  instances: Instance[],
  edges: BuiltEdge[],
  schema: SchemaDiagramData,
): Map<string, { x: number; y: number }> {
  const instancesById = new Map(instances.map((i) => [i.id, i]));

  // Pass 1: plain layout, no lane clearance. Width doesn't affect dagre's cross-axis (Y)
  // placement in LR mode, so this pass already gives every instance its final vertical
  // position — which is exactly what assignLanes needs to tell up-heading edges from
  // down-heading ones before real lanes (and therefore real clearance) can be computed.
  const placeholderColX = NODE_WIDTH + MIN_GAP;
  const prelimLeft = layoutSide(instances, edges, schema, "l", instancesById, placeholderColX, false);
  const prelimRight = layoutSide(instances, edges, schema, "r", instancesById, placeholderColX, false);
  const centerY = new Map<string, number>([["root", 0]]);
  for (const inst of instances) {
    const p = (inst.side === "l" ? prelimLeft : prelimRight).get(inst.id);
    if (p) centerY.set(inst.id, p.y);
  }

  assignLanes(instances, edges, schema, instancesById, centerY);

  // Pass 2: final layout, now with lane-aware clearance. Root isn't part of either dagre
  // subgraph (it's placed manually at the origin), so its own clearance toward each side has
  // to be folded into that side's starting column position here.
  const colXFor = (side: Side) => NODE_WIDTH + outwardClearance("root", edges, side, instancesById) + MIN_GAP;
  const left = layoutSide(instances, edges, schema, "l", instancesById, colXFor("l"), true);
  const right = layoutSide(instances, edges, schema, "r", instancesById, colXFor("r"), true);

  const result = new Map<string, { x: number; y: number }>();
  for (const inst of instances) {
    const h = estimateHeight(inst.modelKey, schema);
    const center = inst.id === "root" ? { x: 0, y: 0 } : (inst.side === "l" ? left : right).get(inst.id) ?? { x: 0, y: 0 };
    result.set(inst.id, { x: center.x - NODE_WIDTH / 2, y: center.y - h / 2 });
  }
  return result;
}
