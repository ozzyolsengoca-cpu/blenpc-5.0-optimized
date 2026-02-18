"""Merge descriptors and cleanup operations for downstream mesh stage."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .config import DISSOLVE_ANGLE, MERGE_DISTANCE


@dataclass(frozen=True)
class MergePlan:
    merge_distance: float = MERGE_DISTANCE
    dissolve_angle: float = DISSOLVE_ANGLE
    recalc_normals: bool = True
    remove_degenerate: bool = True
    delete_loose: bool = True
    mesh_validate: bool = True


def default_merge_plan() -> MergePlan:
    return MergePlan()


def summarize_cleanup(plan: MergePlan) -> Dict[str, object]:
    return {
        "remove_doubles": plan.merge_distance,
        "dissolve_limit": plan.dissolve_angle,
        "recalc_normals": plan.recalc_normals,
        "remove_degenerate": plan.remove_degenerate,
        "delete_loose": plan.delete_loose,
        "mesh_validate": plan.mesh_validate,
    }
