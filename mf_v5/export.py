"""Godot-oriented export settings and manifest generation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass(frozen=True)
class ExportSettings:
    format: str = "GLTF2"
    y_up: bool = True
    apply_modifiers: bool = True
    apply_scale: bool = True
    selected_only: bool = True
    collider_suffix: str = "-col"
    navmesh_collection: str = "MF_Navmesh"


def export_manifest(output_path: Path, building_name: str, settings: ExportSettings) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload: Dict[str, object] = {
        "building": f"{building_name}.glb",
        "collider": f"{building_name}{settings.collider_suffix}.glb",
        "navmesh": f"{building_name}_navmesh.glb",
        "settings": settings.__dict__,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path
