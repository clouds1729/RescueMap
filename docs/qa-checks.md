# QA Checks

Severity levels:

- `error`: data is malformed or geometrically invalid.
- `warning`: data can be exported but may be unsafe or incomplete for emergency response.
- `info`: contextual guidance, such as the current local-coordinate reference system.

Implemented checks:

- `malformed_feature_collection`: verifies that the input root object is a GeoJSON FeatureCollection and that `features` is a list.
- `missing_feature_id`: every feature needs `properties.id` for editing, issue reporting, and stable exports.
- `missing_feature_type`: every feature needs semantic meaning for GIS QA.
- `unsupported_geometry_for_type`: prevents mismatches such as Point walls or Polygon exits.
- `invalid_polygon`: uses Shapely validity checks for room, restricted area, hazard, and stairwell polygons.
- `missing_room_label`: warns when rooms lack a `label` or `name`, because responders need readable room identifiers.
- `missing_exit`: warns when the map cannot support evacuation workflows.
- `overlapping_rooms`: warns when indoor polygons double-claim the same space.
- `isolated_door`: warns when a door is not near a wall or room boundary.
- `room_without_exit_route`: warns when a room cannot produce a graph route to any exit.
- `local_coordinates_notice`: records that coordinates are local floorplan pixels until georeferenced.

These checks are intentionally practical for a prototype: they catch common indoor mapping problems while making it clear when manual correction or georeferencing is still needed.
