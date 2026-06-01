import { ShieldCheck } from "lucide-react";
import { runQa, type QAIssue, type QAResult } from "../lib/api";
import type { FeatureCollection } from "../lib/geojson";

const severityLabels = {
  error: "Errors",
  warning: "Warnings",
  info: "Info"
} as const;

export default function QAPanel({
  collection,
  result,
  onResult,
  onHighlight
}: {
  collection: FeatureCollection;
  result: QAResult | null;
  onResult: (result: QAResult) => void;
  onHighlight: (ids: string[]) => void;
}) {
  const grouped = {
    error: result?.checks.filter((issue) => issue.severity === "error") ?? [],
    warning: result?.checks.filter((issue) => issue.severity === "warning") ?? [],
    info: result?.checks.filter((issue) => issue.severity === "info") ?? []
  };

  async function handleQa() {
    onResult(await runQa(collection));
  }

  return (
    <section className="panel">
      <h2>GIS QA</h2>
      {collection.features.length === 0 && <p className="muted">Add or vectorize features before running QA.</p>}
      <button className="primary" onClick={handleQa}>
        <ShieldCheck size={16} /> Run QA
      </button>
      {result && (
        <>
          <div className="qa-summary">
            <span>{result.summary.total_features} features</span>
            <span>{result.summary.errors} errors</span>
            <span>{result.summary.warnings} warnings</span>
            <span>{result.summary.info} info</span>
          </div>
          <div className="issue-list">
            {(["error", "warning", "info"] as const).map(
              (severity) =>
                grouped[severity].length > 0 && (
                  <div className="issue-group" key={severity}>
                    <h3>{severityLabels[severity]}</h3>
                    {grouped[severity].map((issue: QAIssue, index: number) => (
                      <button
                        key={`${issue.id}-${index}`}
                        className={`issue ${issue.severity}`}
                        onClick={() => issue.feature_ids.length > 0 && onHighlight(issue.feature_ids)}
                      >
                        <strong>{issue.id}</strong>
                        <span>{issue.message}</span>
                      </button>
                    ))}
                  </div>
                )
            )}
            {result.checks.length === 0 && <p className="muted">No QA findings.</p>}
          </div>
        </>
      )}
    </section>
  );
}
