from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at document root: {path}")
    return data


def load_sources(root: Path | None = None) -> dict[str, dict[str, Any]]:
    root = root or repo_root()
    data = load_yaml(root / "data" / "sources" / "sources.yaml")
    sources = data.get("sources")
    if not isinstance(sources, list):
        raise ValueError("data/sources/sources.yaml must contain a 'sources' list")
    return {source["source_id"]: source for source in sources}


def load_programs(root: Path | None = None) -> dict[str, dict[str, Any]]:
    root = root or repo_root()
    programs: dict[str, dict[str, Any]] = {}
    for path in sorted((root / "data" / "programs").glob("*.yaml")):
        program = load_yaml(path)
        programs[program["program_id"]] = program
    return programs


def load_ruleset(root: Path | None = None) -> dict[str, Any]:
    root = root or repo_root()
    return load_yaml(root / "data" / "rules" / "2025-property-tax-relief.yaml")
