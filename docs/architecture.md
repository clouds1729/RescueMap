# Architecture

RescueMap is a local full-stack prototype. The frontend manages the digitizing workflow and displays the floorplan image with SVG vector overlays. The backend handles upload conversion, vectorization, QA, routing, and GeoJSON export.

```text
User
  |
  v
React/Vite Web App
  | upload/vectorize/qa/route/export
  v
FastAPI Service
  |-- routes/upload.py     PDF/image intake
  |-- vectorizer/          OpenCV preprocessing, Hough lines, merging, GeoJSON
  |-- qa/                  Shapely GIS validation and report data
  |-- routing/             NetworkX indoor navigation graph
  |-- utils/               files, PDF conversion, geometry helpers
  v
Local runtime files + GeoJSON
```

The MVP stores uploaded images under `services/api/.runtime`. A production system would replace that with durable object storage and a database-backed project model.
