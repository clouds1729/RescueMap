export type FeatureType =
  | "wall"
  | "door"
  | "room"
  | "exit"
  | "stairwell"
  | "hazard"
  | "restricted_area"
  | "route";

export type Geometry =
  | { type: "Point"; coordinates: [number, number] }
  | { type: "LineString"; coordinates: [number, number][] }
  | { type: "Polygon"; coordinates: [number, number][][] };

export interface RescueFeature {
  type: "Feature";
  geometry: Geometry;
  properties: {
    id: string;
    feature_type: FeatureType;
    source?: "auto" | "manual";
    floor?: string;
    label?: string;
    confidence?: number;
    distance?: number;
    distance_px?: number;
    status?: string;
    [key: string]: unknown;
  };
}

export interface FeatureCollection {
  type: "FeatureCollection";
  features: RescueFeature[];
}

export const emptyCollection = (): FeatureCollection => ({ type: "FeatureCollection", features: [] });

export function makeFeature(featureType: FeatureType, geometry: Geometry, props: Record<string, unknown> = {}): RescueFeature {
  return {
    type: "Feature",
    geometry,
    properties: {
      id: `${featureType}_${crypto.randomUUID().slice(0, 8)}`,
      feature_type: featureType,
      source: "manual",
      floor: "1",
      ...props
    }
  };
}

export function mergeCollections(base: FeatureCollection, incoming: FeatureCollection): FeatureCollection {
  const manual = base.features.filter((feature) => feature.properties.source !== "auto");
  return { type: "FeatureCollection", features: [...manual, ...incoming.features] };
}
