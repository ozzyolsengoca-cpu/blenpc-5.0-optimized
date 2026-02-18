"""Wall segment generation without boolean operations."""

from __future__ import annotations

from typing import Dict, Iterable, List, Sequence

from .config import WALL_HEIGHT, WALL_THICKNESS
from .datamodel import Room, WallSegment


def build_room_wall_segments(rooms: Iterable[Room]) -> Dict[int, List[WallSegment]]:
    result: Dict[int, List[WallSegment]] = {}
    for room in rooms:
        r = room.rect
        result[room.id] = [
            WallSegment(room.id, "south", r.min_x, r.min_y, r.max_x, r.min_y, WALL_HEIGHT, WALL_THICKNESS),
            WallSegment(room.id, "north", r.min_x, r.max_y, r.max_x, r.max_y, WALL_HEIGHT, WALL_THICKNESS),
            WallSegment(room.id, "west", r.min_x, r.min_y, r.min_x, r.max_y, WALL_HEIGHT, WALL_THICKNESS),
            WallSegment(room.id, "east", r.max_x, r.min_y, r.max_x, r.max_y, WALL_HEIGHT, WALL_THICKNESS),
        ]
    return result
