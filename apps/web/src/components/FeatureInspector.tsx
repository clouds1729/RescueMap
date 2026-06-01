import type { RescueFeature } from "../lib/geojson";

export default function FeatureInspector({ feature, onChange }: { feature: RescueFeature | null; onChange: (feature: RescueFeature) => void }) {
  if (!feature) {
    return (
      <section className="panel">
        <h2>Inspector</h2>
        <p className="muted">Select a feature to edit attributes.</p>
      </section>
    );
  }

  function updateProperty(key: string, value: string) {
    if (!feature) return;
    onChange({ ...feature, properties: { ...feature.properties, [key]: value } });
  }

  return (
    <section className="panel">
      <h2>Inspector</h2>
      <dl className="kv">
        <dt>ID</dt>
        <dd>{feature.properties.id}</dd>
        <dt>Type</dt>
        <dd>{feature.properties.feature_type}</dd>
      </dl>
      <label>
        Label
        <input value={String(feature.properties.label ?? "")} onChange={(event) => updateProperty("label", event.target.value)} />
      </label>
      <label>
        Floor
        <input value={String(feature.properties.floor ?? "1")} onChange={(event) => updateProperty("floor", event.target.value)} />
      </label>
    </section>
  );
}
