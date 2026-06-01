import type { FeatureCollection, RescueFeature } from "./geojson";

export interface QAIssue {
  id: string;
  severity: "error" | "warning" | "info";
  message: string;
  feature_ids: string[];
}

export interface QAResult {
  summary: {
    total_features: number;
    errors: number;
    warnings: number;
    info: number;
  };
  checks: QAIssue[];
}

export interface RouteResponse {
  route: RescueFeature;
  warnings: string[];
}

export interface UploadResponse {
  project_id: string;
  image_url: string;
  width: number;
  height: number;
}

export async function uploadFloorplan(file: File): Promise<UploadResponse> {
  const body = new FormData();
  body.append("file", file);
  const response = await fetch("/api/upload", { method: "POST", body });
  if (!response.ok) throw new Error((await response.json()).detail ?? "Upload failed");
  return response.json();
}

export async function vectorize(projectId: string): Promise<FeatureCollection> {
  const response = await fetch("/api/vectorize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ project_id: projectId, options: {} })
  });
  if (!response.ok) throw new Error((await response.json()).detail ?? "Vectorization failed");
  return response.json();
}

export async function runQa(featureCollection: FeatureCollection): Promise<QAResult> {
  const response = await fetch("/api/qa", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ feature_collection: featureCollection })
  });
  if (!response.ok) throw new Error("QA failed");
  return response.json();
}

export async function routeToExit(featureCollection: FeatureCollection, start: [number, number]): Promise<RouteResponse> {
  const response = await fetch("/api/route", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ feature_collection: featureCollection, start })
  });
  if (!response.ok) throw new Error("Routing failed");
  return response.json();
}
