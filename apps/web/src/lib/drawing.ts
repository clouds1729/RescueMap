import type { FeatureType, Geometry, RescueFeature } from "./geojson";
import { makeFeature } from "./geojson";

export type Tool = "select" | "wall" | "room" | "door" | "exit" | "stairwell" | "hazard" | "restricted_area" | "route_start" | "delete";

export function colorForType(type: FeatureType): string {
  return {
    wall: "#d7e3f4",
    door: "#5eead4",
    room: "#38bdf8",
    exit: "#22c55e",
    stairwell: "#a78bfa",
    hazard: "#f97316",
    restricted_area: "#ef4444",
    route: "#facc15"
  }[type];
}

export function pointFeature(tool: Tool, point: [number, number]): RescueFeature | null {
  if (!["door", "exit", "stairwell", "hazard"].includes(tool)) return null;
  return makeFeature(tool as FeatureType, { type: "Point", coordinates: point }, { label: tool === "exit" ? "Exit" : "" });
}

export function buildLineFeature(type: "wall" | "door", points: [number, number][]): RescueFeature | null {
  if (points.length < 2) return null;
  const geometry: Geometry = { type: "LineString", coordinates: [points[0], points[points.length - 1]] };
  return makeFeature(type, geometry);
}

export function buildPolygonFeature(type: "room" | "restricted_area", points: [number, number][]): RescueFeature | null {
  if (points.length < 3) return null;
  const closed = [...points, points[0]];
  return makeFeature(type, { type: "Polygon", coordinates: [closed] }, { label: type === "room" ? "Unlabeled room" : "Restricted" });
}
