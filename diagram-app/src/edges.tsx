import { BaseEdge, type EdgeProps, type EdgeTypes } from "@xyflow/react";
import { BASE_TURN, LANE_STEP } from "./graph";

export interface CircuitEdgeData extends Record<string, unknown> {
  lane: number;
}

/** A strictly orthogonal trace: out of the source, one turn, one turn back into the target —
 * no curves. `lane` staggers how far it runs before the first turn, so several lines leaving
 * the same side of a large card (e.g. Metadata) don't all bend at the same X and overlap. */
export function CircuitEdge({ sourceX, sourceY, targetX, targetY, style, data }: EdgeProps) {
  const lane = (data as CircuitEdgeData | undefined)?.lane ?? 0;
  const dir = targetX >= sourceX ? 1 : -1;
  const turnX = sourceX + dir * (BASE_TURN + lane * LANE_STEP);
  const path = `M ${sourceX},${sourceY} H ${turnX} V ${targetY} H ${targetX}`;
  return <BaseEdge path={path} style={style} />;
}

export const edgeTypes: EdgeTypes = {
  circuit: CircuitEdge,
};
