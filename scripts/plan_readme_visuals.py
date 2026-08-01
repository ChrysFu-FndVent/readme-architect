#!/usr/bin/env python3
"""Create an evidence-bound visual plan for a generated README.

The plan proposes badge markup, separator treatments, and visual asset requests.
It never claims build, coverage, release, or deployment status without evidence.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.parse import quote


SIGNAL_GLYPHS = {
    "friendly-experience": "🌿",
    "product-showcase": "✦",
    "workflow-operations": "⚙️",
    "system-infrastructure": "◆",
    "data-research": "📊",
    "trust-governance": "🛡️",
    "learning-community": "📚",
    "creative-showcase": "✦",
    "ai-intelligence": "✨",
}


def badge_url(label, message, color, style):
    return "https://img.shields.io/badge/{}-{}-{}?style={}".format(
        quote(label, safe=""), quote(message, safe=""), color, style
    )


def badge(label, message, color, style, evidence, url=None, dynamic=False):
    url = url or badge_url(label, message, color, style)
    return {
        "label": label,
        "message": message,
        "color": color,
        "style": style,
        "url": url,
        "markdown": "![{}]({})".format(label, url),
        "dynamic": dynamic,
        "evidence": evidence,
    }


def has_diagram_evidence(profile):
    components = profile.get("presentation_profile", {}).get("recommended_components", [])
    keywords = ("diagram", "pipeline", "flow", "architecture", "map")
    return any(any(word in component.lower() for word in keywords) for component in components)


def plan(profile):
    archetype = profile.get("archetype", "minimal")
    signals = profile.get("presentation_profile", {}).get("signals", [])
    signal_keys = [item.get("key") for item in signals if item.get("key")]
    rich = archetype in {"web-app", "framework"} or bool(
        {"friendly-experience", "product-showcase", "creative-showcase"} & set(signal_keys)
    )
    style = "for-the-badge" if rich else "flat-square"
    budget = 7 if rich else (5 if archetype not in {"minimal", "library"} else 4)
    owner, repo = profile.get("owner"), profile.get("repo")
    badges = []

    ci_workflows = profile.get("ci_workflows", [])
    if owner and repo and ci_workflows:
        workflow = ci_workflows[0]
        url = "https://github.com/{}/{}/actions/workflows/{}/badge.svg?style={}".format(
            owner, repo, quote(workflow, safe=""), style
        )
        badges.append(badge("CI", "workflow", "22C55E", style, ".github/workflows/{}".format(workflow), url, True))
    license_id = profile.get("license")
    if license_id:
        if owner and repo:
            url = "https://img.shields.io/github/license/{}/{}?style={}".format(owner, repo, style)
            badges.append(badge("License", license_id, "16A34A", style, "license metadata", url, True))
        else:
            badges.append(badge("License", license_id, "16A34A", style, "license metadata"))
    version = profile.get("version")
    if version:
        badges.append(badge("Version", str(version), "F97316", style, "package manifest version"))
    languages = profile.get("languages", [])
    if languages:
        badges.append(badge("Built with", languages[0], "0EA5E9", style, "detected source files"))
    frameworks = profile.get("frameworks", [])
    if frameworks:
        badges.append(badge("Framework", frameworks[0], "7C3AED", style, "manifest dependency"))
    if profile.get("has_tests"):
        badges.append(badge("Tests", "included", "14B8A6", style, "test files or test directory"))
    if profile.get("has_docker"):
        badges.append(badge("Container", "Docker", "2496ED", style, "Dockerfile or compose file"))
    if profile.get("has_env_example"):
        badges.append(badge("Configuration", "example included", "EAB308", style, ".env.example or .env.sample"))

    glyphs = [SIGNAL_GLYPHS[key] for key in signal_keys if key in SIGNAL_GLYPHS][:3]
    if rich:
        separator = {
            "primary": "generated-gradient-strip",
            "fallback": "emoji-divider" if glyphs else "markdown-rule",
            "emoji": glyphs or ["✦"],
            "max_uses": 3,
            "output": "assets/readme/divider.png",
        }
    elif glyphs:
        separator = {"primary": "emoji-divider", "fallback": "markdown-rule", "emoji": glyphs, "max_uses": 2}
    else:
        separator = {"primary": "markdown-rule", "max_uses": 0}

    media = profile.get("media_candidates", [])
    has_banner = any(item.get("kind") == "banner" for item in media)
    has_screens = any(item.get("kind") == "screenshot" for item in media)
    requests = []
    if rich and not has_banner:
        requests.append({
            "kind": "banner",
            "output": "assets/readme/banner.png",
            "aspect_ratio": "16:9",
            "purpose": "project opening; leave clear space for title and badges",
            "requires": "imagegen or configured raster image route",
        })
    if not has_screens and {"friendly-experience", "creative-showcase"} & set(signal_keys):
        requests.append({
            "kind": "contextual-illustration",
            "output": "assets/readme/illustration.png",
            "aspect_ratio": "4:3",
            "purpose": "support one documented feature; never imitate a product screenshot",
            "requires": "imagegen or configured raster image route",
        })
    if has_diagram_evidence(profile):
        requests.extend([
            {"kind": "architecture-zh", "output": "assets/readme/architecture-zh.png", "purpose": "Chinese Architecture section", "requires": "drawio or Mermaid"},
            {"kind": "architecture-en", "output": "assets/readme/architecture-en.png", "purpose": "English Architecture section; identical topology", "requires": "drawio or Mermaid"},
        ])
    if separator["primary"] == "generated-gradient-strip":
        requests.append({
            "kind": "gradient-divider",
            "output": separator["output"],
            "aspect_ratio": "12:1",
            "purpose": "decorative separator, no text or logo",
            "requires": "imagegen or configured raster image route",
        })

    return {
        "archetype": archetype,
        "visual_density": "rich" if rich else "focused",
        "badge_budget": budget,
        "badge_candidates": badges[:budget],
        "separator": separator,
        "visual_requests": requests,
        "selection_rules": [
            "Use only candidates whose evidence is still verified in the project.",
            "Do not add coverage, release, deployment, security, or popularity badges without a real source.",
            "Generated raster assets need visual review before embedding; remove failed or irrelevant assets.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, help="JSON profile from analyze_project.py")
    parser.add_argument("--out", help="optional JSON output path")
    args = parser.parse_args(argv)
    try:
        with open(args.profile, "r", encoding="utf-8") as handle:
            profile = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        parser.error("cannot read profile: {}".format(exc))
    result = json.dumps(plan(profile), indent=2, ensure_ascii=False)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(result)
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
