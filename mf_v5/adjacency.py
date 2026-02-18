"""Room adjacency graph and corridor-facing wall detection."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .config import EPSILON
from .datamodel import AdjacencyMap, Corridor, Rect, Room


SIDES = ("north", "south", "east", "west")


def _overlap_1d(a0: float, a1: float, b0: float, b1: float) -> float:
    return max(0.0, min(a1, b1) - max(a0, b0))


def _touches_north(a: Rect, b: Rect) -> bool:
    return abs(a.max_y - b.min_y) <= EPSILON and _overlap_1d(a.min_x, a.max_x, b.min_x, b.max_x) > EPSILON


def _touches_south(a: Rect, b: Rect) -> bool:
    return abs(a.min_y - b.max_y) <= EPSILON and _overlap_1d(a.min_x, a.max_x, b.min_x, b.max_x) > EPSILON


def _touches_east(a: Rect, b: Rect) -> bool:
    return abs(a.max_x - b.min_x) <= EPSILON and _overlap_1d(a.min_y, a.max_y, b.min_y, b.max_y) > EPSILON


def _touches_west(a: Rect, b: Rect) -> bool:
    return abs(a.min_x - b.max_x) <= EPSILON and _overlap_1d(a.min_y, a.max_y, b.min_y, b.max_y) > EPSILON


def build_adjacency(rooms: List[Room]) -> AdjacencyMap:
    adjacency: AdjacencyMap = {room.id: {side: None for side in SIDES} for room in rooms}

    for i, room_a in enumerate(rooms):
        for room_b in rooms[i + 1 :]:
            a, b = room_a.rect, room_b.rect

            if _touches_north(a, b):
                adjacency[room_a.id]["north"] = room_b.id
                adjacency[room_b.id]["south"] = room_a.id
            if _touches_south(a, b):
                adjacency[room_a.id]["south"] = room_b.id
                adjacency[room_b.id]["north"] = room_a.id
            if _touches_east(a, b):
                adjacency[room_a.id]["east"] = room_b.id
                adjacency[room_b.id]["west"] = room_a.id
            if _touches_west(a, b):
                adjacency[room_a.id]["west"] = room_b.id
                adjacency[room_b.id]["east"] = room_a.id

    return adjacency


def corridor_facing_walls(rooms: List[Room], corridor: Corridor) -> Dict[int, List[str]]:
    facing: Dict[int, List[str]] = {room.id: [] for room in rooms}
    c = corridor.rect

    for room in rooms:
        r = room.rect
        vertical_overlap = _overlap_1d(r.min_y, r.max_y, c.min_y, c.max_y) > EPSILON
        horizontal_overlap = _overlap_1d(r.min_x, r.max_x, c.min_x, c.max_x) > EPSILON

        if abs(r.max_x - c.min_x) <= EPSILON and vertical_overlap:
            facing[room.id].append("east")
        if abs(r.min_x - c.max_x) <= EPSILON and vertical_overlap:
            facing[room.id].append("west")
        if abs(r.max_y - c.min_y) <= EPSILON and horizontal_overlap:
            facing[room.id].append("north")
        if abs(r.min_y - c.max_y) <= EPSILON and horizontal_overlap:
            facing[room.id].append("south")

    return facing
