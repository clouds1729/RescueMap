# RescueMap - Indoor GIS Vectorization and QA for Public Safety

RescueMap converts floor plan PDFs/images into editable indoor GIS layers for public-safety workflows. It combines OpenCV vectorization, manual digitization, GeoJSON export, spatial QA, and emergency routing.

## Why It Matters

- Public safety agencies need accurate indoor maps for incident response.
- Floor plans often exist only as PDFs or scanned images.
- GIS teams need repeatable digitization, validation, and export workflows.

## Features

- PDF/image upload with first-page PDF conversion
- OpenCV wall vectorization into GeoJSON LineString features
- Manual correction editor for walls, doors, rooms, exits, stairwells, hazards, and restricted areas
- GeoJSON export using local floorplan coordinates
- GIS QA report for malformed data, invalid geometry, missing labels, missing exits, isolated doors, overlapping rooms, and route gaps
- Indoor route to nearest exit with graph routing and straight-line fallback
- Backend pytest coverage, frontend build, Playwright smoke test, and GitHub Actions CI

## Tech Stack

- Frontend: React, TypeScript, Vite, TailwindCSS, SVG overlay editing
- Backend: Python, FastAPI, OpenCV, NumPy, Shapely, NetworkX, PyMuPDF, Pydantic
- Data: GeoJSON FeatureCollection
- Tests: pytest, Playwright, GitHub Actions

## Quickstart

Backend:

```bash
cd services/api
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd apps/web
npm install
npm run build
npm run dev -- --host 127.0.0.1 --port 5173
```

Open `http://localhost:5173`.

## Frontend Troubleshooting

If the project is checked out under a Windows-mounted WSL path such as `/mnt/c/...`, avoid mixing Windows and Linux installs in the same `node_modules` folder.

Clean WSL/Linux reinstall:

```bash
cd apps/web
rm -rf node_modules package-lock.json
npm install
npm run build
npm run dev -- --host 127.0.0.1 --port 5173
```

If `node_modules` cannot be deleted under `/mnt/c` because Windows is locking files, close Node/Vite/VS Code/browser processes and delete `node_modules` from Windows PowerShell, or copy the repo to the native WSL filesystem, for example `~/projects/rescuemap`, and run `npm install` there.

## Demo Workflow

1. Upload sample floorplan.
2. Run vectorization to detect walls.
3. Add rooms, doors, and exits manually.
4. Run QA to catch missing labels, missing exits, invalid geometry, and unreachable rooms.
5. Route from a selected room/start point to the nearest exit.
6. Export GeoJSON and QA report.

## Screenshots

- `docs/screenshots/upload.png`
- `docs/screenshots/vectorized.png`
- `docs/screenshots/qa.png`
- `docs/screenshots/routing.png`


## Future Work

- ArcGIS Online export
- Shapefile export
- Real georeferencing and indoor local coordinate mapping
- Multi-floor support
- AI-assisted feature detection
- Integration tests generated from natural language workflows
