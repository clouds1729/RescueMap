# GIS Data Model

RescueMap uses GeoJSON FeatureCollections as the interchange format. For the MVP, coordinates are local floorplan pixel coordinates. That keeps digitizing and QA simple while still exercising GIS data modeling. Production export to municipal GIS or ArcGIS would require georeferencing: mapping image/local indoor coordinates to a known spatial reference, building control points, and storing floor-aware transforms.

## Feature Types

- `wall`: LineString with `id`, `feature_type`, `source`, `floor`, optional `confidence`
- `door`: Point or LineString with `id`, `feature_type`, `source`, `floor`, optional `connects`
- `room`: Polygon with `id`, `feature_type`, `label`, optional `room_type`, `floor`
- `exit`: Point with `id`, `feature_type`, `label`, `floor`
- `stairwell`: Point or Polygon with `id`, `feature_type`, `label`, `floor`
- `hazard`: Point or Polygon with `id`, `feature_type`, `label`, optional `severity`, `floor`
- `restricted_area`: Polygon with `id`, `feature_type`, `label`, `floor`
- `route`: LineString with `id`, `feature_type`, `distance_px`, `status`

This model is intentionally close to standard GeoJSON so the exported data can be inspected in common GIS tools after coordinate transformation.
