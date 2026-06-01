# Two-Minute Demo Script

“RescueMap is a public-safety indoor GIS prototype. The problem is that emergency response teams need reliable indoor maps, but many building floor plans are still trapped in PDFs, scans, or image files. That makes them hard to validate, edit, route across, or export into GIS workflows.

The first step in RescueMap is uploading a PDF or image floor plan. The backend converts the first PDF page into an image if needed, then runs an OpenCV vectorization pipeline: grayscale preprocessing, adaptive thresholding, morphology, Hough line detection, and segment merging. The output becomes GeoJSON wall features in local floorplan pixel coordinates.

From there, the analyst can manually digitize and correct the indoor GIS layers. I can add rooms, doors, exits, stairwells, hazards, and restricted areas directly over the original plan. The app keeps those features in a GeoJSON data model, which is the interchange format used by the editor, QA tools, routing, and export.

Next I’ll run GIS QA. The backend checks for malformed FeatureCollections, missing IDs and feature types, unsupported geometry, invalid polygons, missing room labels, missing exits, overlapping rooms, isolated doors, and rooms without graph routes to exits. That QA layer helps agencies trust indoor maps before they are used in public-safety workflows.

Finally, I’ll choose a route start point and route to the nearest exit. RescueMap builds a simple NetworkX navigation graph from rooms, doors, exits, and the route start. If the graph is incomplete, it returns a clear fallback straight-line route and warning instead of failing silently.

The current limitation is that coordinates are local floorplan pixels. A production version would add georeferencing, multi-floor transforms, ArcGIS Online export, and deeper integration with emergency response GIS systems.”
