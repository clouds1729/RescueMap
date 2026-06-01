import { useRef, useState } from "react";
import type { ProjectImage } from "../App";
import type { FeatureCollection, RescueFeature } from "../lib/geojson";
import type { Tool } from "../lib/drawing";
import { buildLineFeature, buildPolygonFeature, colorForType, pointFeature } from "../lib/drawing";

export default function FloorplanCanvas({
  project,
  collection,
  selectedId,
  highlightedIds,
  tool,
  routeStart,
  onSelect,
  onFeature,
  onRouteStart
}: {
  project: ProjectImage | null;
  collection: FeatureCollection;
  selectedId: string | null;
  highlightedIds: string[];
  tool: Tool;
  routeStart: [number, number] | null;
  onSelect: (id: string | null) => void;
  onFeature: (feature: RescueFeature) => void;
  onRouteStart: (point: [number, number]) => void;
}) {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const [draft, setDraft] = useState<[number, number][]>([]);

  function localPoint(event: React.MouseEvent<SVGSVGElement>): [number, number] {
    const svg = svgRef.current!;
    const pt = svg.createSVGPoint();
    pt.x = event.clientX;
    pt.y = event.clientY;
    const transformed = pt.matrixTransform(svg.getScreenCTM()!.inverse());
    return [Math.round(transformed.x), Math.round(transformed.y)];
  }

  function handleClick(event: React.MouseEvent<SVGSVGElement>) {
    if (!project) return;
    const point = localPoint(event);
    if (tool === "select") return onSelect(null);
    if (tool === "route_start") return onRouteStart(point);
    if (tool === "wall") {
      const next = [...draft, point];
      if (next.length >= 2) {
        const feature = buildLineFeature("wall", next);
        if (feature) onFeature(feature);
        setDraft([]);
      } else {
        setDraft(next);
      }
      return;
    }
    if (tool === "room" || tool === "restricted_area") {
      setDraft((current) => [...current, point]);
      return;
    }
    const feature = pointFeature(tool, point);
    if (feature) onFeature(feature);
  }

  function finishPolygon() {
    if (tool !== "room" && tool !== "restricted_area") return;
    const feature = buildPolygonFeature(tool, draft);
    if (feature) onFeature(feature);
    setDraft([]);
  }

  return (
    <div className="canvas-shell">
      {!project && <div className="empty-state">Upload a floorplan to start digitizing indoor GIS layers.</div>}
      {project && (
        <>
          <svg ref={svgRef} className="floorplan-svg" viewBox={`0 0 ${project.width} ${project.height}`} onClick={handleClick} onDoubleClick={finishPolygon}>
            <image href={project.imageUrl} width={project.width} height={project.height} preserveAspectRatio="xMidYMid meet" />
            {collection.features.map((feature) => (
              <FeatureShape
                key={feature.properties.id}
                feature={feature}
                selected={feature.properties.id === selectedId}
                highlighted={highlightedIds.includes(feature.properties.id)}
                onSelect={onSelect}
              />
            ))}
            {draft.length > 0 && <polyline points={draft.map((p) => p.join(",")).join(" ")} className="draft-line" />}
            {routeStart && <circle cx={routeStart[0]} cy={routeStart[1]} r="7" className="route-start" />}
          </svg>
          {draft.length > 0 && <button className="finish" onClick={finishPolygon}>Finish Polygon</button>}
        </>
      )}
    </div>
  );
}

function FeatureShape({
  feature,
  selected,
  highlighted,
  onSelect
}: {
  feature: RescueFeature;
  selected: boolean;
  highlighted: boolean;
  onSelect: (id: string) => void;
}) {
  const color = colorForType(feature.properties.feature_type);
  const common = {
    className: selected ? "feature selected" : highlighted ? "feature highlighted" : "feature",
    stroke: color,
    fill: feature.geometry.type === "Polygon" ? color : "none",
    onClick: (event: React.MouseEvent) => {
      event.stopPropagation();
      onSelect(feature.properties.id);
    }
  };
  if (feature.geometry.type === "Point") {
    const [x, y] = feature.geometry.coordinates;
    return <circle {...common} cx={x} cy={y} r="7" fill={color} />;
  }
  if (feature.geometry.type === "LineString") {
    return <polyline {...common} points={feature.geometry.coordinates.map((p) => p.join(",")).join(" ")} />;
  }
  return <polygon {...common} points={feature.geometry.coordinates[0].map((p) => p.join(",")).join(" ")} />;
}
