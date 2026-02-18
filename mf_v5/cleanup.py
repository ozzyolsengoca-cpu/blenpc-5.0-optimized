"""Simple non-manifold prevention helpers for abstract geometry descriptors."""

from __future__ import annotations

from typing import Iterable, List, Tuple

from .config import EPSILON
from .datamodel import WallSegment


def remove_zero_length_segments(segments: Iterable[WallSegment]) -> List[WallSegment]:
    out = []
    for s in segments:
        if abs(s.x1 - s.x2) <= EPSILON and abs(s.y1 - s.y2) <= EPSILON:
            continue
        out.append(s)
    return out


def dedupe_segments(segments: Iterable[WallSegment]) -> List[WallSegment]:
    seen = set()
    out: List[WallSegment] = []
    for s in segments:
        key = (s.room_id, s.side, round(s.x1, 5), round(s.y1, 5), round(s.x2, 5), round(s.y2, 5))
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out
