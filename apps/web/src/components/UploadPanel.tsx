import { useState } from "react";
import { Upload, Wand2 } from "lucide-react";
import { uploadFloorplan, vectorize } from "../lib/api";
import { mergeCollections, type FeatureCollection } from "../lib/geojson";
import type { ProjectImage } from "../App";

export default function UploadPanel({
  project,
  collection,
  onProject,
  onCollection
}: {
  project: ProjectImage | null;
  collection: FeatureCollection;
  onProject: (project: ProjectImage) => void;
  onCollection: (collection: FeatureCollection) => void;
}) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleFile(file?: File) {
    if (!file) return;
    setBusy(true);
    setError(null);
    try {
      const result = await uploadFloorplan(file);
      onProject({ projectId: result.project_id, imageUrl: result.image_url, width: result.width, height: result.height });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setBusy(false);
    }
  }

  async function runVectorization() {
    if (!project) return;
    setBusy(true);
    setError(null);
    try {
      onCollection(mergeCollections(collection, await vectorize(project.projectId)));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Vectorization failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="panel">
      <h2>Upload</h2>
      <label className="drop-zone">
        <Upload size={22} />
        <span>{busy ? "Processing..." : "Drop or choose PDF/PNG/JPG"}</span>
        <input type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={(event) => handleFile(event.target.files?.[0])} />
      </label>
      {project && <img className="preview" src={project.imageUrl} alt="Uploaded floorplan preview" />}
      <button className="primary" disabled={!project || busy} onClick={runVectorization}>
        <Wand2 size={16} /> Run Vectorization
      </button>
      {error && <p className="error-text">{error}</p>}
    </section>
  );
}
