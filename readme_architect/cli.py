"""Safe offline command-line workflow for README Architect."""

from __future__ import annotations

import argparse
import contextlib
import difflib
import io
import json
import os
import re
import tempfile
from pathlib import Path

from readme_architect import __version__
from readme_architect.renderer import build_suggestions, render_readme
from scripts import analyze_project, plan_readme_visuals, validate_readme


def _atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=str(path.parent), delete=False
    )
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _validate_candidate(rendered):
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        reference = Path(rendered.banner_path)
        leading_parents = 0
        for part in reference.parts:
            if part != "..":
                break
            leading_parents += 1
        readme_dir = root.joinpath(*(["output"] * (leading_parents + 1)))
        readme = readme_dir / "README.md"
        banner = readme_dir / reference
        readme.parent.mkdir(parents=True, exist_ok=True)
        banner.parent.mkdir(parents=True, exist_ok=True)
        readme.write_text(rendered.text, encoding="utf-8")
        banner.write_text(rendered.banner, encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = validate_readme.main(["--bilingual", str(readme)])
        if result:
            raise RuntimeError("generated README failed validation:\n" + output.getvalue())


def _human_suggestions(payload):
    facts = payload["facts"]
    lines = [
        f"Project: {payload['project']}",
        f"Archetype: {payload['archetype']}",
        "Detected facts:",
        f"  Languages: {', '.join(facts['languages']) or 'none'}",
        f"  Frameworks: {', '.join(facts['frameworks']) or 'none'}",
        f"  Package managers: {', '.join(facts['package_managers']) or 'none'}",
        f"  Tests: {'yes' if facts['tests'] else 'no'}",
        f"  CI workflows: {', '.join(facts['ci_workflows']) or 'none'}",
        f"  License: {facts['license'] or 'none'}",
        "Recommendations:",
    ]
    lines.extend(f"  - {item}" for item in payload["recommendations"])
    return "\n".join(lines)


def _parser():
    parser = argparse.ArgumentParser(
        prog="readme-architect",
        description="Generate an evidence-bound bilingual README without network or model APIs.",
    )
    parser.add_argument("project", nargs="?", default=".", help="project directory (default: current directory)")
    parser.add_argument("--output", help="candidate README path (default: README.generated.md)")
    parser.add_argument("--write", action="store_true", help="write README.md directly without prompting")
    parser.add_argument("--dry-run", action="store_true", help="analyze and validate without writing files")
    parser.add_argument("--diff", action="store_true", help="print the README.md diff; does not write unless combined with --write")
    parser.add_argument("--suggest-only", action="store_true", help="print evidence-backed recommendations only")
    parser.add_argument("--json", action="store_true", help="emit JSON with --suggest-only")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def _project_slug(profile):
    slug = re.sub(r"[^a-z0-9]+", "-", str(profile.get("name") or "project").lower()).strip("-")
    return slug or "project"


def main(argv=None):
    parser = _parser()
    args = parser.parse_args(argv)
    if args.json and not args.suggest_only:
        parser.error("--json requires --suggest-only")
    if args.write and args.output:
        parser.error("--write and --output cannot be combined")
    if args.write and args.dry_run:
        parser.error("--write and --dry-run cannot be combined")

    root = Path(args.project).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"project directory not found: {root}")

    profile = analyze_project.analyze(str(root))
    visual_plan = plan_readme_visuals.plan(profile)
    suggestions = build_suggestions(profile, visual_plan)
    if args.suggest_only:
        print(json.dumps(suggestions, indent=2, ensure_ascii=False) if args.json else _human_suggestions(suggestions))
        return 0

    existing_path = root / "README.md"
    if args.write:
        readme_path = existing_path
    else:
        output_path = Path(args.output or "README.generated.md").expanduser()
        readme_path = output_path if output_path.is_absolute() else root / output_path
        readme_path = readme_path.resolve()

    slug = _project_slug(profile)
    banner_path = root / (
        f"assets/readme/{slug}-banner.svg"
        if args.write
        else f".readme-architect/generated/{slug}-banner.svg"
    )
    banner_reference = os.path.relpath(banner_path, start=readme_path.parent).replace(os.sep, "/")
    rendered = render_readme(profile, banner_reference)
    _validate_candidate(rendered)
    existing = existing_path.read_text(encoding="utf-8") if existing_path.is_file() else ""
    if args.diff:
        print("".join(difflib.unified_diff(
            existing.splitlines(keepends=True),
            rendered.text.splitlines(keepends=True),
            fromfile=str(existing_path),
            tofile=str(readme_path),
        )), end="")

    should_write = args.write or (not args.dry_run and not args.diff)
    if should_write:
        _atomic_write(banner_path, rendered.banner)
        _atomic_write(readme_path, rendered.text)
        print(f"README written: {readme_path}")
        print(f"Banner written: {banner_path}")
    else:
        print(f"No files written. Candidate: {readme_path}")
        print(f"No files written. Banner: {banner_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
