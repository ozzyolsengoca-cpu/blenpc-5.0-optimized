"""Corridor-aware deterministic BSP floorplan generation."""

from __future__ import annotations

import random
from typing import List, Sequence, Tuple

from .config import CORRIDOR_WIDTH, EPSILON, MIN_ROOM_SIZE, snap
from .datamodel import Corridor, Rect, Room


def split_rect(rect: Rect, vertical: bool, split_pos: float) -> Tuple[Rect, Rect]:
    if vertical:
        return (
            Rect(rect.min_x, rect.min_y, split_pos, rect.max_y),
            Rect(split_pos, rect.min_y, rect.max_x, rect.max_y),
        )
    return (
        Rect(rect.min_x, rect.min_y, rect.max_x, split_pos),
        Rect(rect.min_x, split_pos, rect.max_x, rect.max_y),
    )


def intersects(a: Rect, b: Rect) -> bool:
    return not (
        a.max_x <= b.min_x + EPSILON
        or a.min_x >= b.max_x - EPSILON
        or a.max_y <= b.min_y + EPSILON
        or a.min_y >= b.max_y - EPSILON
    )


def _room_large_enough(rect: Rect) -> bool:
    return rect.width() >= MIN_ROOM_SIZE and rect.height() >= MIN_ROOM_SIZE


def generate_floorplan(width: float, depth: float, seed: int, floor_index: int) -> Tuple[List[Room], Corridor]:
    rng = random.Random(seed + floor_index)

    width = snap(width)
    depth = snap(depth)
    main_rect = Rect(0.0, 0.0, width, depth)

    cx = snap(width / 2 - CORRIDOR_WIDTH / 2)
    corridor = Corridor(Rect(cx, 0.0, cx + CORRIDOR_WIDTH, depth), floor_index)

    rooms: List[Room] = []
    queue = [main_rect]
    room_id = 0

    while queue:
        rect = queue.pop()

        if rect.width() < 2 * MIN_ROOM_SIZE and rect.height() < 2 * MIN_ROOM_SIZE:
            if not intersects(rect, corridor.rect) and _room_large_enough(rect):
                rooms.append(Room(rect, floor_index, room_id))
                room_id += 1
            continue

        vertical = rng.choice([True, False])
        split = snap(rect.min_x + rect.width() / 2) if vertical else snap(rect.min_y + rect.height() / 2)

        if vertical and (split <= rect.min_x + MIN_ROOM_SIZE or split >= rect.max_x - MIN_ROOM_SIZE):
            vertical = False
            split = snap(rect.min_y + rect.height() / 2)
        if (not vertical) and (split <= rect.min_y + MIN_ROOM_SIZE or split >= rect.max_y - MIN_ROOM_SIZE):
            vertical = True
            split = snap(rect.min_x + rect.width() / 2)

        r1, r2 = split_rect(rect, vertical, split)

        if not _room_large_enough(r1) or not _room_large_enough(r2):
            if not intersects(rect, corridor.rect) and _room_large_enough(rect):
                rooms.append(Room(rect, floor_index, room_id))
                room_id += 1
            continue

        if intersects(r1, corridor.rect) or intersects(r2, corridor.rect):
            if not intersects(rect, corridor.rect) and _room_large_enough(rect):
                rooms.append(Room(rect, floor_index, room_id))
                room_id += 1
            continue

        queue.append(r1)
        queue.append(r2)

    return sorted(rooms, key=lambda r: r.id), corridor
