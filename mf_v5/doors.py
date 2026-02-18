"""Door carving by splitting wall segments into manifold-safe pieces."""

from __future__ import annotations

from typing import Dict, Iterable, List

from .config import DOOR_HEIGHT, DOOR_WIDTH, EPSILON
from .datamodel import DoorOpening, WallSegment


def _split_horizontal(seg: WallSegment, cx: float, door_width: float) -> List[WallSegment]:
    left_end = cx - door_width / 2
    right_start = cx + door_width / 2
    x_min, x_max = sorted((seg.x1, seg.x2))

    pieces: List[WallSegment] = []
    if left_end - x_min > EPSILON:
        pieces.append(WallSegment(seg.room_id, seg.side, x_min, seg.y1, left_end, seg.y2, seg.height, seg.thickness))
    if x_max - right_start > EPSILON:
        pieces.append(WallSegment(seg.room_id, seg.side, right_start, seg.y1, x_max, seg.y2, seg.height, seg.thickness))
    return pieces


def _split_vertical(seg: WallSegment, cy: float, door_width: float) -> List[WallSegment]:
    bottom_end = cy - door_width / 2
    top_start = cy + door_width / 2
    y_min, y_max = sorted((seg.y1, seg.y2))

    pieces: List[WallSegment] = []
    if bottom_end - y_min > EPSILON:
        pieces.append(WallSegment(seg.room_id, seg.side, seg.x1, y_min, seg.x2, bottom_end, seg.height, seg.thickness))
    if y_max - top_start > EPSILON:
        pieces.append(WallSegment(seg.room_id, seg.side, seg.x1, top_start, seg.x2, y_max, seg.height, seg.thickness))
    return pieces


def carve_doors(
    wall_segments: Dict[int, List[WallSegment]],
    openings: Iterable[DoorOpening],
) -> Dict[int, List[WallSegment]]:
    openings_by_room_side = {(d.room_id, d.side): d for d in openings}
    carved: Dict[int, List[WallSegment]] = {}

    for room_id, segments in wall_segments.items():
        out: List[WallSegment] = []
        for seg in segments:
            opening = openings_by_room_side.get((room_id, seg.side))
            if not opening:
                out.append(seg)
                continue

            if seg.side in ("north", "south"):
                out.extend(_split_horizontal(seg, opening.center[0], opening.width))
            else:
                out.extend(_split_vertical(seg, opening.center[1], opening.width))
        carved[room_id] = out

    return carved


def corridor_door_openings(corridor_facing: Dict[int, List[str]], room_rect_lookup: Dict[int, tuple]) -> List[DoorOpening]:
    openings: List[DoorOpening] = []
    for room_id, sides in corridor_facing.items():
        if not sides:
            continue
        side = sides[0]
        min_x, min_y, max_x, max_y = room_rect_lookup[room_id]
        if side in ("north", "south"):
            center = ((min_x + max_x) / 2, max_y if side == "north" else min_y)
        else:
            center = (max_x if side == "east" else min_x, (min_y + max_y) / 2)
        openings.append(DoorOpening(room_id, side, center, DOOR_WIDTH, DOOR_HEIGHT))
    return openings
