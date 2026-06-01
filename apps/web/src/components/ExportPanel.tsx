import { Download } from "lucide-react";
import type { FeatureCollection } from "../lib/geojson";
import type { QAResult } from "../lib/api";

function downloadJson(name: string, data: unknown) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = name;
  link.click();
  URL.revokeObjectURL(url);
}

export default function ExportPanel({ collection, qaResult }: { collection: FeatureCollection; qaResult: QAResult | null }) {
  const report = qaResult
    ? { name: "RescueMap GIS QA Report", generated_at: new Date().toISOString(), ...qaResult }
    : { name: "RescueMap GIS QA Report", generated_at: new Date().toISOString(), message: "Run QA first." };

  return (
    <section className="panel">
      <h2>Export</h2>
      <button className="primary" onClick={() => downloadJson("rescuemap.geojson", collection)}>
        <Download size={16} /> Download GeoJSON
      </button>
      <button className="secondary" onClick={() => downloadJson("rescuemap-qa-report.json", report)}>
        <Download size={16} /> Download QA Report
      </button>
    </section>
  );
}
