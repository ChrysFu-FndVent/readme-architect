#!/usr/bin/env python3
"""Detect which companion skills/tools README Architect can integrate with.

Standard library only. Prints a human-readable capability report, or machine
JSON with --json. Never prints secret values (only whether a key is present).

Integrations probed:
  - image generation : nano-banana-pro, nano-banana-flash, generate-gpt-image-2
  - diagrams         : draw.io (CLI on PATH or the macOS app bundle) + Mermaid
  - credentials      : XIAOHULI_API_KEY (env), ~/.codex/auth.json OPENAI_API_KEY
  - runtimes         : python3, node

Usage:
  python3 check_integrations.py [--json]
"""
from __future__ import annotations

import json
import os
import shutil
import sys

# Default skill install roots, probed on any machine. Extend for other setups
# via env: README_ARCHITECT_SKILL_ROOTS="/path/one:/path/two" (os.pathsep-separated).
DEFAULT_SKILL_ROOTS = [
    "~/.qoder/skills",
    "~/.claude/skills",
    "~/.codex/skills",
    "~/.hermes/skills",
    "~/.workbuddy-ai/skills",
    "~/.config/skills",
    "~/skills",
    "~/.local/share/skills",
]


def skill_roots():
    """Roots to search for companion skills. Env override wins, then defaults,
    plus Windows %APPDATA% locations — so this works on machines other than the
    author's without code edits."""
    roots = []
    env = os.environ.get("README_ARCHITECT_SKILL_ROOTS")
    if env:
        roots += [p for p in env.split(os.pathsep) if p.strip()]
    roots += list(DEFAULT_SKILL_ROOTS)
    for var in ("APPDATA", "LOCALAPPDATA"):
        base = os.environ.get(var)
        if base:
            roots.append(os.path.join(base, "skills"))
    return roots


IMAGE_SKILLS = {
    "nano-banana-pro": ("scripts/generate_image.py", "python3"),
    "nano-banana-flash": ("scripts/generate_image.py", "python3"),
    "generate-gpt-image-2": ("scripts/gpt_image_2.mjs", "node"),
}


def _expand(p: str) -> str:
    return os.path.expanduser(p)


def find_skill(name: str, rel_script: str):
    """Return the first existing absolute script path for a skill, else None."""
    for root in skill_roots():
        cand = os.path.join(_expand(root), name, rel_script)
        if os.path.isfile(cand):
            return cand
    return None


def codex_auth_has_key() -> bool:
    home = os.environ.get("CODEX_HOME")
    paths = []
    if home:
        paths.append(os.path.join(_expand(home), "auth.json"))
    paths.append(_expand("~/.codex/auth.json"))
    for p in paths:
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data.get("OPENAI_API_KEY"), str) and data["OPENAI_API_KEY"].strip():
                    return True
            except Exception:
                continue
    return False


def detect_drawio():
    """Return (available: bool, invocation: str|None, note: str). Works on
    macOS / Linux / Windows without assuming one machine's layout."""
    on_path = shutil.which("drawio") or shutil.which("draw.io")
    if on_path:
        return True, on_path, "drawio on PATH"
    candidates = [
        "/Applications/draw.io.app/Contents/MacOS/draw.io",
        _expand("~/Applications/draw.io.app/Contents/MacOS/draw.io"),
    ]
    for var in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
        base = os.environ.get(var)
        if base:
            candidates.append(os.path.join(base, "draw.io", "draw.io.exe"))
    for c in candidates:
        if c and os.path.isfile(c):
            note = "macOS draw.io.app bundle" if c.endswith("draw.io") else "Windows draw.io install"
            return True, c, note + " (not on PATH)"
    if sys.platform.startswith("linux") and shutil.which("xvfb-run"):
        return False, None, "xvfb-run present but no drawio binary (install drawio-desktop)"
    return False, None, "no draw.io CLI/app found — will fall back to Mermaid"


def detect():
    report = {"runtimes": {}, "image": {}, "diagram": {}, "credentials": {}, "web_widgets": {}}

    # runtimes
    report["runtimes"]["python3"] = bool(shutil.which("python3") or sys.executable)
    report["runtimes"]["node"] = bool(shutil.which("node"))

    # credentials (any of several sources may satisfy a route on a given machine)
    xkey = bool(os.environ.get("XIAOHULI_API_KEY"))
    openai_env = bool(os.environ.get("OPENAI_API_KEY"))
    codex = codex_auth_has_key()
    report["credentials"]["XIAOHULI_API_KEY_env"] = xkey
    report["credentials"]["OPENAI_API_KEY_env"] = openai_env
    report["credentials"]["codex_auth_OPENAI_API_KEY"] = codex

    # image skills
    for name, (rel, runtime) in IMAGE_SKILLS.items():
        path = find_skill(name, rel)
        installed = path is not None
        if name.startswith("nano-banana"):
            usable = installed and xkey
            need = None if usable else ("XIAOHULI_API_KEY (ask the user)" if installed else "install skill")
        else:  # gpt-image-2 uses the local Codex provider credential or OPENAI_API_KEY
            usable = installed and (codex or openai_env)
            need = None if usable else ("~/.codex/auth.json or OPENAI_API_KEY (ask the user)" if installed else "install skill")
        report["image"][name] = {
            "installed": installed, "path": path, "runtime": runtime,
            "usable_now": usable, "needs": need,
        }

    # diagram
    d_ok, d_inv, d_note = detect_drawio()
    report["diagram"]["drawio"] = {"available": d_ok, "invocation": d_inv, "note": d_note}
    report["diagram"]["mermaid"] = {"available": True, "note": "native GitHub render; no binary needed"}

    # web widgets (remote, only need a public repo + network at view time)
    report["web_widgets"]["shields_io_badges"] = True
    report["web_widgets"]["github_readme_stats"] = True
    report["web_widgets"]["star_history"] = True
    report["web_widgets"]["contrib_rocks"] = True

    return report


def preferred_banner_route(report):
    order = ["nano-banana-pro", "nano-banana-flash", "generate-gpt-image-2"]
    for name in order:
        info = report["image"].get(name, {})
        if info.get("usable_now"):
            return name
    # installed but blocked on a key?
    for name in order:
        info = report["image"].get(name, {})
        if info.get("installed"):
            return f"{name} (blocked: needs {info.get('needs')})"
    return None


def print_human(report):
    def mark(b):
        return "OK " if b else "-- "

    print("README Architect — integration check\n" + "=" * 40)
    print("\nRuntimes:")
    for k, v in report["runtimes"].items():
        print(f"  [{mark(v)}] {k}")

    print("\nImage generation (banner/logo/illustration):")
    for name, info in report["image"].items():
        status = "usable" if info["usable_now"] else (
            f"installed, needs {info['needs']}" if info["installed"] else "not installed")
        print(f"  [{mark(info['usable_now'])}] {name:22s} {status}")
    print(f"  -> preferred banner route: {preferred_banner_route(report)}")

    print("\nDiagrams:")
    d = report["diagram"]["drawio"]
    print(f"  [{mark(d['available'])}] draw.io   {d['note']}")
    if d["invocation"]:
        print(f"        invocation: {d['invocation']} -x -f png --scale 2 -o out.png in.drawio")
    print(f"  [{mark(True)}] mermaid   native GitHub fenced ```mermaid block (always available)")

    print("\nCredentials:")
    print(f"  [{mark(report['credentials']['XIAOHULI_API_KEY_env'])}] XIAOHULI_API_KEY (env) — nano-banana pro/flash")
    gpt_cred = report['credentials']['codex_auth_OPENAI_API_KEY'] or report['credentials']['OPENAI_API_KEY_env']
    src = "~/.codex/auth.json" if report['credentials']['codex_auth_OPENAI_API_KEY'] else ("OPENAI_API_KEY env" if report['credentials']['OPENAI_API_KEY_env'] else "none")
    print(f"  [{mark(gpt_cred)}] OpenAI credential for gpt-image-2 — source: {src}")

    print("\nWeb widgets (need only a public repo + viewer network):")
    for k, v in report["web_widgets"].items():
        print(f"  [{mark(v)}] {k}")

    if preferred_banner_route(report) is None:
        print("\nHint: no image route is usable on this machine. Either:")
        print("  • install one of: nano-banana-pro / nano-banana-flash / generate-gpt-image-2, or")
        print("  • provide a credential — export XIAOHULI_API_KEY=<key> (nano-banana) or OPENAI_API_KEY=<key> (gpt-image-2).")
        print("  The README still generates without a banner; ask the user before requesting any key, and never log it.")
    elif not report["credentials"]["XIAOHULI_API_KEY_env"]:
        print("\nHint: nano-banana needs XIAOHULI_API_KEY; falling back to gpt-image-2 where possible.")
        print("      To enable nano-banana: export XIAOHULI_API_KEY=<key>  # ask the user; never hard-code or log it")


def main():
    as_json = "--json" in sys.argv[1:]
    report = detect()
    if as_json:
        report["_preferred_banner_route"] = preferred_banner_route(report)
        print(json.dumps(report, indent=2))
    else:
        print_human(report)
    # exit 0 if at least one image route and one diagram route are usable
    img_ok = any(v["usable_now"] for v in report["image"].values())
    diag_ok = report["diagram"]["drawio"]["available"] or report["diagram"]["mermaid"]["available"]
    return 0 if (img_ok and diag_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
