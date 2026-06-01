import cv2
import numpy as np

from app.vectorizer.detect_lines import detect_line_segments
from app.vectorizer.preprocess import preprocess_floorplan


def test_vectorizer_detects_synthetic_rectangle():
    image = np.full((160, 200, 3), 255, dtype=np.uint8)
    cv2.rectangle(image, (30, 30), (170, 120), (0, 0, 0), 3)
    binary = preprocess_floorplan(image)
    segments = detect_line_segments(binary, min_line_length=20, max_line_gap=5)
    assert len(segments) >= 2


def test_blank_image_has_no_crash():
    image = np.full((80, 80, 3), 255, dtype=np.uint8)
    binary = preprocess_floorplan(image)
    segments = detect_line_segments(binary)
    assert isinstance(segments, list)
