import { useState } from "react";
import { Navigation } from "lucide-react";
import { routeToExit } from "../lib/api";
import type { FeatureCollection, RescueFeature } from "../lib/geojson";
import { formatDistance } from "../lib/routing";

export default function RoutingPanel({
  collection,
  routeStart,
  onRoute
}: {
  collection: FeatureCollection;
  routeStart: [number, number] | null;
  onRoute: (feature: RescueFeature) => void;
}) {
  const routeFeature = collection.features.find((feature) => feature.properties.feature_type === "route");
  const hasExit = collection.features.some((feature) => feature.properties.feature_type === "exit");
  const [warnings, setWarnings] = useState<string[]>([]);

  async function handleRoute() {
    if (!routeStart) return;
    if (!hasExit) {
      setWarnings(["Add at least one exit before routing."]);
      return;
    }
    const result = await routeToExit(collection, routeStart);
    setWarnings(result.warnings);
    onRoute(result.route);
  }

  return (
    <section className="panel">
      <h2>Routing</h2>
      <p className="muted">{routeStart ? `Start: ${routeStart[0]}, ${routeStart[1]}` : "Choose Route Start, then click the map."}</p>
      <button className="primary" disabled={!routeStart} onClick={handleRoute}>
        <Navigation size={16} /> Route to nearest exit
      </button>
      {warnings.map((warning) => (
        <p className="route-warning" key={warning}>{warning}</p>
      ))}
      {routeFeature && (
        <p className="route-meta">
          Status: {routeFeature.properties.status} - {formatDistance(routeFeature.properties.distance_px as number)}
        </p>
      )}
    </section>
  );
}
