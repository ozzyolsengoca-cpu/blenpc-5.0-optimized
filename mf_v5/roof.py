"""Roof topology descriptors including true hip roof surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from .config import ROOF_HEIGHT
from .datamodel import Rect, RoofType


@dataclass(frozen=True)
class RoofFace:
    vertices: Tuple[Tuple[float, float, float], ...]


@dataclass(frozen=True)
class RoofGeometry:
    roof_type: RoofType
    faces: List[RoofFace]


def build_roof(footprint: Rect, base_z: float, roof_type: RoofType) -> RoofGeometry:
    if roof_type == RoofType.HIP:
        cx = (footprint.min_x + footprint.max_x) / 2
        cy = (footprint.min_y + footprint.max_y) / 2
        apex = (cx, cy, base_z + ROOF_HEIGHT)
        corners = [
            (footprint.min_x, footprint.min_y, base_z),
            (footprint.max_x, footprint.min_y, base_z),
            (footprint.max_x, footprint.max_y, base_z),
            (footprint.min_x, footprint.max_y, base_z),
        ]
        faces = [
            RoofFace((corners[0], corners[1], apex)),
            RoofFace((corners[1], corners[2], apex)),
            RoofFace((corners[2], corners[3], apex)),
            RoofFace((corners[3], corners[0], apex)),
        ]
        return RoofGeometry(roof_type, faces)

    if roof_type == RoofType.FLAT:
        faces = [
            RoofFace(
                (
                    (footprint.min_x, footprint.min_y, base_z),
                    (footprint.max_x, footprint.min_y, base_z),
                    (footprint.max_x, footprint.max_y, base_z),
                    (footprint.min_x, footprint.max_y, base_z),
                )
            )
        ]
        return RoofGeometry(roof_type, faces)

    # Basic placeholders for gabled/shed with deterministic slope direction.
    if roof_type == RoofType.GABLED:
        mid_x = (footprint.min_x + footprint.max_x) / 2
        ridge_a = (mid_x, footprint.min_y, base_z + ROOF_HEIGHT)
        ridge_b = (mid_x, footprint.max_y, base_z + ROOF_HEIGHT)
        faces = [
            RoofFace(((footprint.min_x, footprint.min_y, base_z), (footprint.min_x, footprint.max_y, base_z), ridge_b, ridge_a)),
            RoofFace(((footprint.max_x, footprint.min_y, base_z), (footprint.max_x, footprint.max_y, base_z), ridge_b, ridge_a)),
        ]
        return RoofGeometry(roof_type, faces)

    # SHED
    faces = [
        RoofFace(
            (
                (footprint.min_x, footprint.min_y, base_z),
                (footprint.max_x, footprint.min_y, base_z + ROOF_HEIGHT),
                (footprint.max_x, footprint.max_y, base_z + ROOF_HEIGHT),
                (footprint.min_x, footprint.max_y, base_z),
            )
        )
    ]
    return RoofGeometry(roof_type, faces)
