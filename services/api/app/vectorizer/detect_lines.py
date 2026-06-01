import cv2
import numpy as np

Segment = tuple[float, float, float, float]


def detect_line_segments(binary: np.ndarray, min_line_length: int = 40, max_line_gap: int = 10) -> list[Segment]:
    if binary.size == 0 or np.count_nonzero(binary) == 0:
        return []
    edges = cv2.Canny(binary, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=30,
        minLineLength=min_line_length,
        maxLineGap=max_line_gap,
    )
    if lines is None:
        return []
    segments: list[Segment] = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 >= min_line_length:
            segments.append((float(x1), float(y1), float(x2), float(y2)))
    return segments
