# Vectorization Pipeline

The vectorizer converts floorplan imagery into wall-like GeoJSON features.

1. Load the uploaded or PDF-converted image with OpenCV.
2. Convert to grayscale and apply light Gaussian denoising.
3. Apply adaptive thresholding so scanned plans with uneven lighting still produce a binary image.
4. Invert when needed so dark plan ink becomes foreground.
5. Run morphological close/open operations to connect small gaps and reduce speckle.
6. Run Canny edge detection and HoughLinesP to detect line segments.
7. Merge horizontal-ish and vertical-ish collinear segments using angle and distance tolerances.
8. Export each merged segment as a GeoJSON wall LineString.

## Limitations

The MVP detects linework, not semantic building elements. Dense text, furniture, dimensions, and scan artifacts may become false wall segments. That is why manual correction is a core workflow: GIS teams need a human-in-the-loop editor before public-safety export.
