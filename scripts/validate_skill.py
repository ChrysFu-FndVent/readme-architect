#!/usr/bin/env python3
"""Run repository-local checks required before packaging the skill."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    skill = ROOT / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    issues = []
    if not text.startswith("---\nname: readme-architect\n"):
        issues.append("SKILL.md must start with the readme-architect frontmatter")
    for required in ("scripts/analyze_project.py", "scripts/validate_readme.py", "references/section-library.md"):
        if not (ROOT / required).is_file():
            issues.append(f"missing required skill resource: {required}")
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 1
    print("Skill structure is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
