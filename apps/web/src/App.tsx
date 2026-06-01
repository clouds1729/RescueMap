import { useMemo, useState } from "react";
import UploadPanel from "./components/UploadPanel";
import ToolPalette from "./components/ToolPalette";
import FloorplanCanvas from "./components/FloorplanCanvas";
import FeatureInspector from "./components/FeatureInspector";
import QAPanel from "./components/QAPanel";
import ExportPanel from "./components/ExportPanel";
import RoutingPanel from "./components/RoutingPanel";
import type { FeatureCollection, RescueFeature } from "./lib/geojson";
import { emptyCollection } from "./lib/geojson";
import type { Tool } from "./lib/drawing";
import type { QAResult } from "./lib/api";

export interface ProjectImage {
  projectId: string;
  imageUrl: string;
  width: number;
  height: number;
}

export default function App() {
  const [project, setProject] = useState<ProjectImage | null>(null);
  const [collection, setCollection] = useState<FeatureCollection>(emptyCollection());
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [highlightedIds, setHighlightedIds] = useState<string[]>([]);
  const [tool, setTool] = useState<Tool>("select");
  const [qaResult, setQaResult] = useState<QAResult | null>(null);
  const [routeStart, setRouteStart] = useState<[number, number] | null>(null);
  const selectedFeature = useMemo(
    () => collection.features.find((feature) => feature.properties.id === selectedId) ?? null,
    [collection, selectedId]
  );

  function upsertFeature(feature: RescueFeature) {
    setCollection((current) => ({
      type: "FeatureCollection",
      features: [...current.features.filter((item) => item.properties.id !== feature.properties.id), feature]
    }));
  }

  function replaceRouteFeature(feature: RescueFeature) {
    setCollection((current) => ({
      type: "FeatureCollection",
      features: [...current.features.filter((item) => item.properties.feature_type !== "route"), feature]
    }));
  }

  function highlightFeatures(ids: string[]) {
    setHighlightedIds(ids);
    setSelectedId(ids[0] ?? null);
  }

  function deleteSelected() {
    if (!selectedId) return;
    setCollection((current) => ({ ...current, features: current.features.filter((feature) => feature.properties.id !== selectedId) }));
    setSelectedId(null);
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div>
          <p className="eyebrow">Public Safety Indoor GIS</p>
          <h1>RescueMap</h1>
        </div>
        <UploadPanel project={project} onProject={setProject} collection={collection} onCollection={setCollection} />
        <ToolPalette activeTool={tool} onTool={setTool} onDelete={deleteSelected} />
      </aside>
      <section className="map-stage">
        <div className="stage-header">
          <div>
            <h2>Floorplan Editor</h2>
            <p>{collection.features.length} mapped features · local pixel coordinates</p>
          </div>
          <span className="status-pill">{project ? "Project loaded" : "Awaiting upload"}</span>
        </div>
        <FloorplanCanvas
          project={project}
          collection={collection}
          selectedId={selectedId}
          highlightedIds={highlightedIds}
          tool={tool}
          routeStart={routeStart}
          onSelect={(id) => {
            setSelectedId(id);
            setHighlightedIds(id ? [id] : []);
          }}
          onFeature={upsertFeature}
          onRouteStart={setRouteStart}
        />
      </section>
      <aside className="sidebar rightbar">
        <FeatureInspector feature={selectedFeature} onChange={upsertFeature} />
        <QAPanel collection={collection} result={qaResult} onResult={setQaResult} onHighlight={highlightFeatures} />
        <RoutingPanel collection={collection} routeStart={routeStart} onRoute={replaceRouteFeature} />
        <ExportPanel collection={collection} qaResult={qaResult} />
      </aside>
    </main>
  );
}
