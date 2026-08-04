#!/usr/bin/env python3
"""Build a deterministic Codex skill archive without project-only files."""

from __future__ import annotations

import argparse
import os
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = ("SKILL.md", "LICENSE", "pyproject.toml")
RESOURCE_DIRS = ("agents", "readme_architect", "references", "scripts", "templates")
SKIP_PARTS = {"__pycache__", ".readme-architect"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def iter_skill_files(root=ROOT):
    paths = [root / name for name in ROOT_FILES if (root / name).is_file()]
    for directory in RESOURCE_DIRS:
        base = root / directory
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(root)
            if SKIP_PARTS.intersection(relative.parts) or path.suffix in SKIP_SUFFIXES:
                continue
            paths.append(path)
    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def build_archive(output, root=ROOT):
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in iter_skill_files(root):
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"readme-architect/{relative}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if os.access(path, os.X_OK) else 0o644) << 16
            archive.writestr(info, path.read_bytes())
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="destination .zip path")
    args = parser.parse_args(argv)
    output = build_archive(args.output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
