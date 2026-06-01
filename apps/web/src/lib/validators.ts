import type { FeatureCollection } from "./geojson";

export function isFeatureCollection(value: unknown): value is FeatureCollection {
  return Boolean(value && typeof value === "object" && (value as FeatureCollection).type === "FeatureCollection" && Array.isArray((value as FeatureCollection).features));
}
