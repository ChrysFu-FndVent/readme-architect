"""Deterministic, evidence-bound bilingual README rendering."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from urllib.parse import quote


@dataclass(frozen=True)
class RenderedReadme:
    text: str
    banner: str
    banner_path: str


ARCHETYPE_LABELS = {
    "cli-tool": ("命令行工具", "command-line tool"),
    "library": ("软件库", "software library"),
    "web-app": ("Web 应用", "web application"),
    "framework": ("开发框架", "development framework"),
    "ml-ai": ("机器学习 / AI 项目", "machine-learning / AI project"),
    "monorepo": ("多包仓库", "monorepo"),
    "minimal": ("轻量仓库", "minimal repository"),
}

PALETTES = {
    "friendly-experience": ("#0F766E", "#22C55E", "#F59E0B"),
    "product-showcase": ("#0369A1", "#06B6D4", "#F97316"),
    "workflow-operations": ("#334155", "#0EA5E9", "#F59E0B"),
    "system-infrastructure": ("#0F766E", "#0284C7", "#F97316"),
    "data-research": ("#1D4ED8", "#14B8A6", "#EAB308"),
    "trust-governance": ("#14532D", "#0F766E", "#DC2626"),
    "learning-community": ("#1D4ED8", "#F59E0B", "#DB2777"),
    "creative-showcase": ("#BE185D", "#F97316", "#0EA5E9"),
    "ai-intelligence": ("#4338CA", "#06B6D4", "#F59E0B"),
}
DEFAULT_PALETTE = ("#0F766E", "#0EA5E9", "#F97316")


def _one_line(value, fallback=""):
    text = str(value or fallback).replace("\r", " ").replace("\n", " ").strip()
    return re.sub(r"\s+", " ", text)


def _slug(value):
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "project"


def _palette(profile):
    signals = profile.get("presentation_profile", {}).get("signals", [])
    for signal in signals:
        key = signal.get("key")
        if key in PALETTES:
            return PALETTES[key]
    return DEFAULT_PALETTE


def _banner_svg(profile):
    first, second, third = _palette(profile)
    name = html.escape(_one_line(profile.get("name"), "Project"))
    language = html.escape(_one_line(profile.get("primary_language"), "Repository"))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="420" viewBox="0 0 1600 420" role="img" aria-labelledby="title desc">
  <title id="title">{name}</title>
  <desc id="desc">Evidence-bound project banner</desc>
  <rect width="1600" height="420" fill="#FCFCFB"/>
  <path d="M0 312C184 228 300 336 493 247C683 159 787 85 957 151C1146 225 1282 154 1600 39V420H0Z" fill="{first}" opacity=".95"/>
  <path d="M0 358C219 245 363 368 602 286C838 205 1034 327 1244 229C1390 161 1493 163 1600 137V420H0Z" fill="{second}" opacity=".88"/>
  <circle cx="1320" cy="106" r="122" fill="{third}" opacity=".9"/>
  <circle cx="1420" cy="187" r="44" fill="#FCFCFB" opacity=".84"/>
  <path d="M108 84H748" stroke="{first}" stroke-width="12" stroke-linecap="round"/>
  <text x="108" y="205" fill="#111827" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" font-size="60" font-weight="700">{name}</text>
  <text x="112" y="263" fill="#475569" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" font-size="26">{language}</text>
</svg>
'''


def _static_badge(label, message, color):
    return "https://img.shields.io/badge/{}-{}-{}?style=flat-square".format(
        quote(label, safe=""), quote(message, safe=""), color
    )


def _badges(profile):
    owner, repo = profile.get("owner"), profile.get("repo")
    language = profile.get("primary_language")
    license_id = profile.get("license")
    workflows = profile.get("ci_workflows") or []
    badges = []
    if owner and repo and workflows:
        workflow = quote(workflows[0], safe="")
        badges.append(
            ("CI", f"https://github.com/{owner}/{repo}/actions/workflows/{workflows[0]}",
             f"https://github.com/{owner}/{repo}/actions/workflows/{workflow}/badge.svg")
        )
    if language:
        badges.append(("Language", None, _static_badge("Language", language, "0EA5E9")))
    if license_id:
        if owner and repo:
            badges.append(
                ("License", f"https://github.com/{owner}/{repo}/blob/HEAD/LICENSE",
                 f"https://img.shields.io/github/license/{owner}/{repo}?style=flat-square")
            )
        else:
            badges.append(("License", None, _static_badge("License", license_id, "16A34A")))
    if profile.get("has_tests"):
        badges.append(("Tests included", None, _static_badge("Tests", "included", "14B8A6")))
    rendered = []
    for alt, target, image in badges[:5]:
        tag = f'<img alt="{html.escape(alt)}" src="{html.escape(image)}" />'
        rendered.append(f'<a href="{html.escape(target)}">{tag}</a>' if target else tag)
    return rendered


def _facts(profile, language):
    rows = []
    labels = {
        "zh": {"type": "项目类型", "language": "主要语言", "package": "包管理", "framework": "框架", "tests": "测试", "ci": "CI", "container": "容器", "yes": "已检测", "no": "未检测"},
        "en": {"type": "Project type", "language": "Primary language", "package": "Package management", "framework": "Frameworks", "tests": "Tests", "ci": "CI", "container": "Container", "yes": "Detected", "no": "Not detected"},
    }[language]
    archetype = ARCHETYPE_LABELS.get(profile.get("archetype"), ARCHETYPE_LABELS["minimal"])
    rows.append((labels["type"], archetype[0 if language == "zh" else 1]))
    if profile.get("primary_language"):
        rows.append((labels["language"], profile["primary_language"]))
    if profile.get("package_managers"):
        rows.append((labels["package"], ", ".join(profile["package_managers"])))
    if profile.get("frameworks"):
        rows.append((labels["framework"], ", ".join(profile["frameworks"])))
    rows.append((labels["tests"], labels["yes"] if profile.get("has_tests") else labels["no"]))
    if profile.get("ci_workflows"):
        rows.append((labels["ci"], ", ".join(profile["ci_workflows"])))
    if profile.get("has_docker"):
        rows.append((labels["container"], "Docker"))
    return rows


def _topology(profile):
    allowed = {"app", "apps", "assets", "cmd", "docs", "lib", "packages", "references", "scripts", "src", "templates", "tests"}
    return [item for item in profile.get("top_level", []) if item.lower() in allowed][:8]


def _mermaid(profile, language):
    nodes = _topology(profile)
    if len(nodes) < 2:
        return ""
    root_label = "项目根目录" if language == "zh" else "Project root"
    lines = ["```mermaid", "flowchart TD", f'    ROOT["{root_label}"]']
    for index, node in enumerate(nodes):
        safe = node.replace('"', "")
        lines.append(f'    ROOT --> N{index}["{safe}"]')
    lines.extend([
        "    classDef root fill:#0F766E,stroke:#134E4A,color:#FFFFFF,stroke-width:2px;",
        "    classDef module fill:#F8FAFC,stroke:#0EA5E9,color:#111827,stroke-width:1.2px;",
        "    class ROOT root;",
        "    class " + ",".join(f"N{i}" for i in range(len(nodes))) + " module;",
        "```",
    ])
    return "\n".join(lines)


def _installation(profile):
    entrypoints = profile.get("entrypoints") or []
    managers = set(profile.get("package_managers") or [])
    if "python" in managers and entrypoints:
        return "python -m pip install .", f"{entrypoints[0]} --help"
    scripts = profile.get("scripts") or {}
    if scripts:
        manager = "npm"
        if "pnpm" in managers:
            manager = "pnpm"
        elif "yarn" in managers:
            manager = "yarn"
        install = "npm install" if manager == "npm" else f"{manager} install"
        command_name = "start" if "start" in scripts else ("dev" if "dev" in scripts else next(iter(scripts)))
        command = f"npm run {command_name}" if manager == "npm" else f"{manager} {command_name}"
        return install, command
    return None


def _toc(has_map, has_start, has_license):
    zh = ["  - [项目概览](#zh-overview)", "  - [项目事实](#zh-facts)"]
    en = ["  - [Overview](#en-overview)", "  - [Project facts](#en-facts)"]
    if has_map:
        zh.append("  - [仓库结构](#zh-structure)")
        en.append("  - [Repository structure](#en-structure)")
    if has_start:
        zh.append("  - [快速开始](#zh-quick-start)")
        en.append("  - [Quick start](#en-quick-start)")
    if has_license:
        zh.append("  - [许可证](#zh-license)")
        en.append("  - [License](#en-license)")
    return "\n".join([
        "<details>",
        "<summary>Table of Contents</summary>",
        "",
        "- [简体中文](#简体中文)",
        *zh,
        "- [English](#english)",
        *en,
        "",
        "</details>",
    ])


def _fact_table(rows, language):
    headers = ("项目", "检测结果") if language == "zh" else ("Item", "Detected value")
    lines = [f"| {headers[0]} | {headers[1]} |", "|---|---|"]
    lines.extend(f"| {label} | {value} |" for label, value in rows)
    return "\n".join(lines)


def render_readme(profile, banner_path=None):
    """Render one Chinese-first bilingual README plus its local SVG banner."""
    name = _one_line(profile.get("name"), "Project")
    slug = _slug(name)
    banner_path = banner_path or f"assets/readme/{slug}-banner.svg"
    description = _one_line(profile.get("description"))
    archetype = ARCHETYPE_LABELS.get(profile.get("archetype"), ARCHETYPE_LABELS["minimal"])
    primary = profile.get("primary_language")
    if not description:
        description = f"A {archetype[1]}" + (f" built with {primary}." if primary else ".")
    badges = _badges(profile)
    topology = _topology(profile)
    installation = _installation(profile)
    has_license = bool(profile.get("license"))

    opening = [
        '<a id="readme-top"></a>',
        '<div align="right"><a href="#简体中文">简体中文</a> | <a href="#english">English</a></div>',
        "",
        '<div align="center">',
        f'  <img src="{html.escape(banner_path)}" alt="{html.escape(name)} project banner" width="100%" />',
        f"  <h1>{html.escape(name)}</h1>",
        f"  <p><em>{html.escape(description)}</em></p>",
    ]
    opening.extend(f"  {badge}" for badge in badges)
    opening.extend(["</div>", "", _toc(bool(topology), bool(installation), has_license)])

    zh_overview = f"仓库证据表明这是一个{archetype[0]}" + (f"，主要使用 {primary}。" if primary else "。")
    en_overview = description
    sections = [
        *opening,
        "",
        '<a id="简体中文"></a>',
        "## 简体中文",
        "",
        '<a id="zh-overview"></a>',
        "### 项目概览",
        "",
        zh_overview,
        "",
        '<a id="zh-facts"></a>',
        "### 项目事实",
        "",
        _fact_table(_facts(profile, "zh"), "zh"),
    ]
    if topology:
        sections.extend(["", '<a id="zh-structure"></a>', "### 仓库结构", "", _mermaid(profile, "zh")])
    if installation:
        sections.extend([
            "", '<a id="zh-quick-start"></a>', "### 快速开始", "",
            "```bash", installation[0], installation[1], "```",
        ])
    if has_license:
        sections.extend([
            "", '<a id="zh-license"></a>', "### 许可证", "",
            f"本项目包含 `{profile['license']}` 许可证文件。",
        ])
    sections.extend([
        "", '<a id="english"></a>', "## English", "",
        '<a id="en-overview"></a>', "### Overview", "", en_overview, "",
        '<a id="en-facts"></a>', "### Project facts", "",
        _fact_table(_facts(profile, "en"), "en"),
    ])
    if topology:
        sections.extend(["", '<a id="en-structure"></a>', "### Repository structure", "", _mermaid(profile, "en")])
    if installation:
        sections.extend([
            "", '<a id="en-quick-start"></a>', "### Quick start", "",
            "```bash", installation[0], installation[1], "```",
        ])
    if has_license:
        sections.extend([
            "", '<a id="en-license"></a>', "### License", "",
            f"This project includes a `{profile['license']}` license file.",
        ])
    sections.extend(["", '<p align="right">(<a href="#readme-top">back to top</a>)</p>', ""])
    return RenderedReadme("\n".join(sections), _banner_svg(profile), banner_path)


def build_suggestions(profile, visual_plan):
    """Return evidence and non-destructive next actions for terminal or JSON output."""
    recommendations = []
    if profile.get("existing_readmes"):
        recommendations.append("Preview a diff before replacing the existing README.")
    if not profile.get("ci_workflows"):
        recommendations.append("Add CI before displaying a build-status badge.")
    if not profile.get("license"):
        recommendations.append("Add or identify a license before publishing a license badge.")
    if profile.get("media_candidates"):
        recommendations.append("Inspect verified repository media before generating decorative imagery.")
    if not recommendations:
        recommendations.append("The detected repository facts are sufficient for a focused README.")
    return {
        "project": profile.get("name"),
        "archetype": profile.get("archetype"),
        "facts": {
            "languages": profile.get("languages") or [],
            "frameworks": profile.get("frameworks") or [],
            "package_managers": profile.get("package_managers") or [],
            "tests": bool(profile.get("has_tests")),
            "ci_workflows": profile.get("ci_workflows") or [],
            "license": profile.get("license"),
        },
        "badge_candidates": visual_plan.get("badge_candidates") or [],
        "recommendations": recommendations,
    }
