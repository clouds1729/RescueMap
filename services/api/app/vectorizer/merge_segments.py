from math import atan2, cos, degrees, hypot, radians, sin

from app.vectorizer.detect_lines import Segment


def angle(segment: Segment) -> float:
    x1, y1, x2, y2 = segment
    deg = degrees(atan2(y2 - y1, x2 - x1))
    return abs((deg + 180) % 180)


def length(segment: Segment) -> float:
    x1, y1, x2, y2 = segment
    return hypot(x2 - x1, y2 - y1)


def midpoint(segment: Segment) -> tuple[float, float]:
    x1, y1, x2, y2 = segment
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def _orientation_bucket(segment: Segment) -> str | None:
    a = angle(segment)
    if a <= 15 or a >= 165:
        return "horizontal"
    if 75 <= a <= 105:
        return "vertical"
    return None


def are_collinear(seg1: Segment, seg2: Segment, angle_tolerance: float = 10, distance_tolerance: float = 8) -> bool:
    b1 = _orientation_bucket(seg1)
    b2 = _orientation_bucket(seg2)
    if b1 is None or b1 != b2:
        return False
    if abs(angle(seg1) - angle(seg2)) > angle_tolerance:
        return False
    m1 = midpoint(seg1)
    m2 = midpoint(seg2)
    if b1 == "horizontal":
        return abs(m1[1] - m2[1]) <= distance_tolerance
    return abs(m1[0] - m2[0]) <= distance_tolerance


def _merge_pair(seg1: Segment, seg2: Segment) -> Segment:
    bucket = _orientation_bucket(seg1)
    points = [(seg1[0], seg1[1]), (seg1[2], seg1[3]), (seg2[0], seg2[1]), (seg2[2], seg2[3])]
    if bucket == "horizontal":
        y = sum(p[1] for p in points) / len(points)
        xs = [p[0] for p in points]
        return (min(xs), y, max(xs), y)
    if bucket == "vertical":
        x = sum(p[0] for p in points) / len(points)
        ys = [p[1] for p in points]
        return (x, min(ys), x, max(ys))
    longest = max((seg1, seg2), key=length)
    theta = radians(angle(longest))
    ux, uy = cos(theta), sin(theta)
    projections = [(p[0] * ux + p[1] * uy, p) for p in points]
    return (*min(projections)[1], *max(projections)[1])


def merge_collinear_segments(
    segments: list[Segment], angle_tolerance: float = 10, distance_tolerance: float = 8
) -> list[Segment]:
    remaining = list(segments)
    changed = True
    while changed:
        changed = False
        merged: list[Segment] = []
        used = [False] * len(remaining)
        for i, segment in enumerate(remaining):
            if used[i]:
                continue
            current = segment
            for j in range(i + 1, len(remaining)):
                if used[j]:
                    continue
                if are_collinear(current, remaining[j], angle_tolerance, distance_tolerance):
                    current = _merge_pair(current, remaining[j])
                    used[j] = True
                    changed = True
            used[i] = True
            merged.append(current)
        remaining = merged
    return remaining
