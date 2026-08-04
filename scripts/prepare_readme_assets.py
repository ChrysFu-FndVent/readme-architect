#!/usr/bin/env python3
"""Select, copy, and optionally center-crop project media for a README.

This script never edits source media. It creates derived assets under a chosen
destination and writes a manifest that records each source and transformation.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Set

try:
    from scripts.console import configure_utf8_stdio
except ModuleNotFoundError:
    from console import configure_utf8_stdio

from analyze_project import (
    IMAGE_EXTENSIONS,
    MEDIA_DEPRIORITY_TERMS,
    MEDIA_PRIORITY_TERMS,
    SKIP_DIRS,
    is_ignored,
    read_ignore_patterns,
)


def image_dimensions(path: Path):
    """Return raster dimensions for common formats without a third-party dependency."""
    try:
        data = path.read_bytes()[:65536]
    except OSError:
        return None
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if data[:6] in (b"GIF87a", b"GIF89a") and len(data) >= 10:
        return int.from_bytes(data[6:8], "little"), int.from_bytes(data[8:10], "little")
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        if data[12:16] == b"VP8X" and len(data) >= 30:
            return (int.from_bytes(data[24:27], "little") + 1,
                    int.from_bytes(data[27:30], "little") + 1)
    if data.startswith(b"\xff\xd8"):
        index = 2
        while index + 9 < len(data):
            if data[index] != 0xFF:
                index += 1
                continue
            marker = data[index + 1]
            index += 2
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                continue
            if index + 2 > len(data):
                break
            length = int.from_bytes(data[index:index + 2], "big")
            if length < 2 or index + length > len(data):
                break
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                return int.from_bytes(data[index + 5:index + 7], "big"), int.from_bytes(data[index + 3:index + 5], "big")
            index += length
    return None


def profile_keywords(profile_path: Optional[str]):
    if not profile_path or not os.path.isfile(profile_path):
        return set()
    try:
        profile = json.loads(Path(profile_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    presentation = profile.get("presentation_profile", {})
    corpus = " ".join([
        str(profile.get("name") or ""),
        str(profile.get("description") or ""),
        *presentation.get("matched_terms", []),
    ]).lower()
    return set(re.sub(r"[^a-z0-9]+", " ", corpus).split())


def discover(root: Path, destination: Path, keywords: Set[str]):
    ignored = read_ignore_patterns(str(root))
    destination_resolved = destination.resolve()
    candidates = []
    for directory, dirnames, filenames in os.walk(root):
        current = Path(directory)
        kept = []
        for dirname in dirnames:
            child = current / dirname
            rel = child.relative_to(root).as_posix()
            if dirname in SKIP_DIRS or dirname.startswith(".git") or is_ignored(rel, True, ignored):
                continue
            if child.resolve() == destination_resolved or destination_resolved in child.resolve().parents:
                continue
            kept.append(dirname)
        dirnames[:] = kept
        for filename in filenames:
            source = current / filename
            rel = source.relative_to(root).as_posix()
            if is_ignored(rel, False, ignored) or source.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            tokens = set(re.sub(r"[^a-z0-9]+", " ", rel.lower()).split())
            score = sum(weight for term, weight in MEDIA_PRIORITY_TERMS.items() if term in tokens)
            score += 20 * len(tokens & keywords)
            score -= 30 * len(tokens & MEDIA_DEPRIORITY_TERMS)
            if source.stat().st_size < 1024:
                score -= 20
            candidates.append((score, rel, source, sorted(tokens & keywords)))
    return sorted(candidates, key=lambda item: (-item[0], item[1]))


def parse_ratio(value: str):
    match = re.fullmatch(r"(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)", value)
    if not match or float(match.group(1)) <= 0 or float(match.group(2)) <= 0:
        raise ValueError("crop ratio must look like 16:9")
    return float(match.group(1)), float(match.group(2))


def crop_with_pillow(source: Path, target: Path, ratio, width: int):
    try:
        from PIL import Image
    except ImportError:
        return False
    try:
        with Image.open(source) as image:
            image = image.convert("RGB") if image.mode not in ("RGB", "RGBA") else image
            source_ratio = image.width / image.height
            target_ratio = ratio[0] / ratio[1]
            if source_ratio > target_ratio:
                crop_width = round(image.height * target_ratio)
                left = (image.width - crop_width) // 2
                box = (left, 0, left + crop_width, image.height)
            else:
                crop_height = round(image.width / target_ratio)
                top = (image.height - crop_height) // 2
                box = (0, top, image.width, top + crop_height)
            height = round(width / target_ratio)
            resampling = getattr(Image, "Resampling", Image)
            image.crop(box).resize((width, height), resampling.LANCZOS).save(target)
        return True
    except (OSError, ValueError):
        if target.exists():
            target.unlink()
        return False


def crop_with_external(source: Path, target: Path, ratio, width: int):
    dimensions = image_dimensions(source)
    if not dimensions:
        return False
    height = round(width * ratio[1] / ratio[0])
    if shutil.which("sips"):
        command = ["sips", "--cropToHeightWidth", str(height), str(width), str(source), "--out", str(target)]
    elif shutil.which("magick"):
        command = ["magick", str(source), "-gravity", "center", "-crop", f"{width}x{height}+0+0", "+repage", str(target)]
    else:
        return False
    return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False).returncode == 0


def unique_target(destination: Path, index: int, source: Path):
    stem = re.sub(r"[^a-z0-9]+", "-", source.stem.lower()).strip("-") or "image"
    candidate = destination / f"{index:02d}-{stem}{source.suffix.lower()}"
    suffix = 2
    while candidate.exists():
        candidate = destination / f"{index:02d}-{stem}-{suffix}{source.suffix.lower()}"
        suffix += 1
    return candidate


def main(argv=None):
    configure_utf8_stdio()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="project root")
    parser.add_argument("--dest", default="assets/readme/media", help="derived asset directory relative to root")
    parser.add_argument("--profile", help="analyzer profile JSON; adds project-specific ranking keywords")
    parser.add_argument("--limit", type=int, default=3, help="maximum selected assets")
    parser.add_argument("--include", action="append", default=[], help="explicit relative source path; repeatable")
    parser.add_argument("--crop-ratio", help="center crop selected raster media, e.g. 16:9")
    parser.add_argument("--crop-width", type=int, default=1600, help="width for cropped raster media")
    parser.add_argument("--dry-run", action="store_true", help="print the proposed manifest without writing files")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    destination = (root / args.dest).resolve()
    if not root.is_dir() or root not in destination.parents and root != destination:
        parser.error("--root must exist and --dest must remain inside it")
    if args.limit < 1 or args.crop_width < 64:
        parser.error("--limit must be positive and --crop-width must be at least 64")
    ratio = parse_ratio(args.crop_ratio) if args.crop_ratio else None
    profile = args.profile or str(root / ".readme-architect" / "profile.json")
    candidates = discover(root, destination, profile_keywords(profile))
    explicit = {path.replace("\\", "/") for path in args.include}
    if explicit:
        candidates = [item for item in candidates if item[1] in explicit]
        missing = explicit - {item[1] for item in candidates}
        if missing:
            parser.error("explicit media not found or excluded: " + ", ".join(sorted(missing)))
    selected = candidates[:args.limit]
    manifest = {"root": str(root), "destination": str(destination), "assets": [], "warnings": []}
    if not selected:
        manifest["warnings"].append("No supported project media found.")
    for index, (score, rel, source, keyword_hits) in enumerate(selected, 1):
        target = unique_target(destination, index, source)
        action = "would-copy" if args.dry_run else "copied"
        if not args.dry_run:
            destination.mkdir(parents=True, exist_ok=True)
            cropped = ratio and source.suffix.lower() not in {".svg", ".gif"} and (
                crop_with_pillow(source, target, ratio, args.crop_width)
                or crop_with_external(source, target, ratio, args.crop_width)
            )
            if not cropped:
                shutil.copy2(source, target)
            else:
                action = "center-cropped"
        manifest["assets"].append({
            "source": rel,
            "output": target.relative_to(root).as_posix(),
            "action": action,
            "score": score,
            "keyword_hits": keyword_hits,
            "dimensions": image_dimensions(source),
        })
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
