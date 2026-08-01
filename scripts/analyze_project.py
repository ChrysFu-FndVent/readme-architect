#!/usr/bin/env python3
"""Analyze a project directory and emit a structured profile for README generation.

Standard library only. Produces JSON describing languages, package managers,
frameworks, entrypoints, docs/images, git remote, and an archetype hint.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
from collections import Counter

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "env", "__pycache__", "dist",
    "build", "out", ".next", ".nuxt", "target", ".idea", ".vscode", "vendor",
    "coverage", ".pytest_cache", ".mypy_cache", ".turbo", ".cache", "site-packages",
    ".gradle", "Pods", "DerivedData", ".terraform", ".svelte-kit",
}

LANG_BY_EXT = {
    ".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript", ".js": "JavaScript",
    ".jsx": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript", ".go": "Go",
    ".rs": "Rust", ".java": "Java", ".kt": "Kotlin", ".rb": "Ruby", ".php": "PHP",
    ".c": "C", ".h": "C", ".cpp": "C++", ".cc": "C++", ".hpp": "C++", ".cs": "C#",
    ".swift": "Swift", ".m": "Objective-C", ".scala": "Scala", ".dart": "Dart",
    ".vue": "Vue", ".svelte": "Svelte", ".sh": "Shell", ".sql": "SQL",
    ".ipynb": "Jupyter Notebook", ".r": "R", ".ex": "Elixir", ".exs": "Elixir",
    ".lua": "Lua", ".zig": "Zig", ".hs": "Haskell", ".clj": "Clojure",
}

MANIFESTS = {
    "package.json": "npm", "pnpm-workspace.yaml": "pnpm", "yarn.lock": "yarn",
    "pyproject.toml": "python", "setup.py": "python", "setup.cfg": "python",
    "requirements.txt": "pip", "Pipfile": "pipenv", "Cargo.toml": "cargo",
    "go.mod": "go", "pom.xml": "maven", "build.gradle": "gradle",
    "build.gradle.kts": "gradle", "composer.json": "composer", "Gemfile": "bundler",
    "pubspec.yaml": "pub", "mix.exs": "hex",
}

FRAMEWORK_SIGNS = {
    # dependency-name substring -> framework label
    "react": "React", "react-dom": "React", "next": "Next.js", "nuxt": "Nuxt",
    "vue": "Vue.js", "@angular/core": "Angular", "svelte": "Svelte",
    "@sveltejs/kit": "SvelteKit", "express": "Express", "koa": "Koa",
    "fastify": "Fastify", "nestjs": "NestJS", "@nestjs/core": "NestJS",
    "django": "Django", "flask": "Flask", "fastapi": "FastAPI",
    "starlette": "Starlette", "torch": "PyTorch", "tensorflow": "TensorFlow",
    "transformers": "Transformers", "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn", "pandas": "pandas", "numpy": "NumPy",
    "langchain": "LangChain", "streamlit": "Streamlit", "gradio": "Gradio",
    "rails": "Ruby on Rails", "laravel": "Laravel", "spring-boot": "Spring Boot",
    "gin-gonic/gin": "Gin", "actix-web": "Actix", "axum": "Axum", "tokio": "Tokio",
    "electron": "Electron", "tauri": "Tauri", "vite": "Vite", "webpack": "Webpack",
    "tailwindcss": "Tailwind CSS", "prisma": "Prisma", "graphql": "GraphQL",
    "click": "Click", "typer": "Typer", "argparse": "argparse", "cobra": "Cobra",
    "commander": "Commander", "clap": "clap", "yargs": "yargs",
}

CLI_SIGNS = {"click", "typer", "argparse", "cobra", "commander", "clap", "yargs", "oclif"}
ML_SIGNS = {"torch", "tensorflow", "transformers", "scikit-learn", "sklearn", "keras", "jax"}
WEBAPP_SIGNS = {"react", "vue", "svelte", "@angular/core", "next", "nuxt", "django",
                "flask", "fastapi", "rails", "laravel", "spring-boot"}

SPDX_HINTS = [
    ("MIT License", "MIT"), ("Apache License", "Apache-2.0"), ("GNU GENERAL PUBLIC LICENSE", "GPL-3.0"),
    ("BSD 3-Clause", "BSD-3-Clause"), ("BSD 2-Clause", "BSD-2-Clause"),
    ("Mozilla Public License", "MPL-2.0"), ("The Unlicense", "Unlicense"),
    ("ISC License", "ISC"), ("GNU LESSER", "LGPL-3.0"),
]


def read_text(path, limit=200_000):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(limit)
    except OSError:
        return ""


def read_ignore_patterns(root):
    """Read optional repository-local filters without inheriting .gitignore."""
    path = os.path.join(root, ".readme-architectignore")
    if not os.path.isfile(path):
        return []
    patterns = []
    for line in read_text(path).splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)
    return patterns


def is_ignored(rel_path, is_dir, patterns):
    """Apply a small, documented subset of gitignore-style matching rules."""
    rel_path = rel_path.replace(os.sep, "/").strip("/")
    ignored = False
    for raw_pattern in patterns:
        negated = raw_pattern.startswith("!")
        pattern = raw_pattern[1:] if negated else raw_pattern
        root_only = pattern.startswith("/")
        pattern = pattern.lstrip("/")
        directory_only = pattern.endswith("/")
        pattern = pattern.rstrip("/")
        if not pattern:
            continue
        candidates = [pattern]
        if pattern.startswith("**/"):
            candidates.append(pattern[3:])
        matched = False
        for candidate in candidates:
            if directory_only:
                if root_only or "/" in candidate:
                    matched = rel_path == candidate or rel_path.startswith(candidate + "/")
                else:
                    matched = candidate in rel_path.split("/")
            elif root_only or "/" in candidate:
                matched = fnmatch.fnmatchcase(rel_path, candidate)
            else:
                matched = fnmatch.fnmatchcase(os.path.basename(rel_path), candidate)
            if matched:
                break
        if matched and (not directory_only or is_dir or "/" in rel_path):
            ignored = not negated
    return ignored


def detect_license(root, manifest_data):
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "license"):
        p = os.path.join(root, name)
        if os.path.isfile(p):
            text = read_text(p, 4000)
            for needle, spdx in SPDX_HINTS:
                if needle.lower() in text.lower():
                    return spdx
            return "SEE LICENSE FILE"
    for m in manifest_data.values():
        lic = m.get("license")
        if isinstance(lic, str) and lic:
            return lic
        if isinstance(lic, dict) and lic.get("type"):
            return lic["type"]
    return None


def parse_package_json(path):
    try:
        data = json.loads(read_text(path))
    except (json.JSONDecodeError, ValueError):
        return {}
    deps = {}
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        deps.update(data.get(key, {}) or {})
    return {
        "name": data.get("name"),
        "description": data.get("description"),
        "version": data.get("version"),
        "license": data.get("license"),
        "bin": data.get("bin"),
        "scripts": data.get("scripts", {}) or {},
        "workspaces": data.get("workspaces"),
        "deps": list(deps.keys()),
        "type": data.get("type"),
    }


def parse_pyproject(path):
    text = read_text(path)
    out = {"deps": []}
    m = re.search(r'(?m)^\s*name\s*=\s*["\']([^"\']+)["\']', text)
    if m:
        out["name"] = m.group(1)
    m = re.search(r'(?m)^\s*description\s*=\s*["\']([^"\']+)["\']', text)
    if m:
        out["description"] = m.group(1)
    m = re.search(r'(?m)^\s*version\s*=\s*["\']([^"\']+)["\']', text)
    if m:
        out["version"] = m.group(1)
    for dep in re.findall(r'["\']([A-Za-z0-9_.\-]+)\s*(?:[><=~!\[].*?)?["\']', text):
        low = dep.lower()
        if low in FRAMEWORK_SIGNS or low in ML_SIGNS:
            out["deps"].append(low)
    if re.search(r'\[project\.scripts\]|console_scripts', text):
        out["has_scripts"] = True
    return out


def get_git_remote(root):
    try:
        url = subprocess.check_output(
            ["git", "-C", root, "config", "--get", "remote.origin.url"],
            stderr=subprocess.DEVNULL, text=True,
        ).strip()
    except (subprocess.CalledProcessError, OSError):
        return None, None, None
    m = re.search(r'github\.com[:/]+([^/]+)/(.+?)(?:\.git)?$', url)
    if m:
        return url, m.group(1), m.group(2)
    return url, None, None


def walk_project(root, ignore_patterns):
    langs = Counter()
    total_files = 0
    top_entries = set()
    all_rel = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        kept_dirs = []
        for d in dirnames:
            rel = os.path.normpath(os.path.join(rel_dir, d)) if rel_dir != "." else d
            if d in SKIP_DIRS or d.startswith(".git") or is_ignored(rel, True, ignore_patterns):
                continue
            kept_dirs.append(d)
        dirnames[:] = kept_dirs
        depth = os.path.relpath(dirpath, root).count(os.sep)
        if os.path.relpath(dirpath, root) == ".":
            top_entries.update(dirnames)
            top_entries.update(filenames)
        for fn in filenames:
            rel = os.path.normpath(os.path.join(rel_dir, fn)) if rel_dir != "." else fn
            if is_ignored(rel, False, ignore_patterns):
                continue
            total_files += 1
            ext = os.path.splitext(fn)[1].lower()
            if ext in LANG_BY_EXT:
                langs[LANG_BY_EXT[ext]] += 1
            if depth < 3:
                all_rel.append(rel)
    return langs, total_files, top_entries, all_rel


def find_images(all_rel):
    exts = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")
    return [p for p in all_rel if p.lower().endswith(exts)
            and ("asset" in p.lower() or "image" in p.lower() or "screenshot" in p.lower()
                 or "doc" in p.lower() or "logo" in p.lower() or "banner" in p.lower())][:20]


def choose_archetype(profile):
    deps = set(profile["frameworks_raw"])
    top = {e.lower() for e in profile["_top"]}
    langs = profile["languages"]

    if profile["monorepo_packages"]:
        return "monorepo"
    if deps & ML_SIGNS or any(p.endswith(".ipynb") or "train" in p.lower() or "model" in p.lower()
                              for p in profile["_rel"]) and (deps & ML_SIGNS):
        if deps & ML_SIGNS:
            return "ml-ai"
    if profile["has_bin"] or (deps & CLI_SIGNS) or (profile["name"] or "").endswith("-cli"):
        return "cli-tool"
    if deps & WEBAPP_SIGNS or {"public", "src", "index.html"} & top:
        if deps & WEBAPP_SIGNS:
            return "web-app"
    if profile["total_files"] < 12 and not profile["package_managers"]:
        return "minimal"
    if profile["is_publishable_lib"]:
        return "library"
    if deps & WEBAPP_SIGNS:
        return "web-app"
    return "library" if profile["package_managers"] else "minimal"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    ignore_patterns = read_ignore_patterns(root)
    langs, total_files, top_entries, all_rel = walk_project(root, ignore_patterns)

    manifest_data = {}
    package_managers = []
    for fn, pm in MANIFESTS.items():
        if os.path.isfile(os.path.join(root, fn)):
            package_managers.append(pm)
            if fn == "package.json":
                manifest_data["package.json"] = parse_package_json(os.path.join(root, fn))
            elif fn == "pyproject.toml":
                manifest_data["pyproject.toml"] = parse_pyproject(os.path.join(root, fn))

    # aggregate deps / frameworks
    raw_deps = []
    for m in manifest_data.values():
        raw_deps.extend(d.lower() for d in m.get("deps", []))
    if os.path.isfile(os.path.join(root, "requirements.txt")):
        for line in read_text(os.path.join(root, "requirements.txt")).splitlines():
            name = re.split(r"[><=~!\[ ]", line.strip(), 1)[0].lower()
            if name:
                raw_deps.append(name)
    frameworks = []
    for sign, label in FRAMEWORK_SIGNS.items():
        if any(sign in d for d in raw_deps):
            if label not in frameworks:
                frameworks.append(label)

    # monorepo packages
    monorepo_packages = []
    for base in ("packages", "apps", "crates", "libs"):
        bp = os.path.join(root, base)
        if os.path.isdir(bp):
            for entry in sorted(os.listdir(bp)):
                ep = os.path.join(bp, entry)
                if os.path.isdir(ep) and any(
                    os.path.isfile(os.path.join(ep, mf))
                    for mf in ("package.json", "Cargo.toml", "pyproject.toml")
                ):
                    monorepo_packages.append(f"{base}/{entry}")

    pkg = manifest_data.get("package.json", {})
    pyp = manifest_data.get("pyproject.toml", {})
    name = pkg.get("name") or pyp.get("name") or os.path.basename(root)
    description = pkg.get("description") or pyp.get("description")
    version = pkg.get("version") or pyp.get("version")

    has_bin = bool(pkg.get("bin")) or bool(pyp.get("has_scripts"))
    scripts = pkg.get("scripts", {})

    remote_url, owner, repo = get_git_remote(root)
    license_id = detect_license(root, manifest_data)

    ci_files = []
    wf_dir = os.path.join(root, ".github", "workflows")
    if os.path.isdir(wf_dir):
        ci_files = [f for f in os.listdir(wf_dir) if f.endswith((".yml", ".yaml"))]

    has_tests = any(
        os.path.isdir(os.path.join(root, d)) for d in ("test", "tests", "__tests__", "spec")
    ) or any("test" in p.lower() or "spec" in p.lower() for p in all_rel[:500])

    existing_readmes = [f for f in top_entries if f.lower().startswith("readme")]
    is_publishable_lib = bool(
        (pkg and not has_bin and (pkg.get("name") and not pkg.get("scripts", {}).get("start")))
        or ("__init__.py" in {os.path.basename(p) for p in all_rel})
        or os.path.isfile(os.path.join(root, "src", "lib.rs"))
    )

    profile = {
        "name": name,
        "description": description,
        "version": version,
        "license": license_id,
        "languages": [l for l, _ in langs.most_common()],
        "language_counts": dict(langs.most_common(12)),
        "package_managers": sorted(set(package_managers)),
        "frameworks": frameworks,
        "frameworks_raw": [d for d in raw_deps if d in FRAMEWORK_SIGNS or d in ML_SIGNS or d in CLI_SIGNS],
        "has_bin": has_bin,
        "scripts": scripts,
        "monorepo_packages": monorepo_packages,
        "total_files": total_files,
        "ci_workflows": ci_files,
        "has_ci": bool(ci_files),
        "has_tests": has_tests,
        "has_docker": any(f.lower() in ("dockerfile", "docker-compose.yml", "compose.yaml")
                          for f in top_entries),
        "has_env_example": ".env.example" in top_entries or ".env.sample" in top_entries,
        "existing_readmes": existing_readmes,
        "has_contributing": "CONTRIBUTING.md" in top_entries,
        "has_code_of_conduct": "CODE_OF_CONDUCT.md" in top_entries,
        "has_citation": "CITATION.cff" in top_entries,
        "ignore_patterns": ignore_patterns,
        "images": find_images(all_rel),
        "git_remote": remote_url,
        "owner": owner,
        "repo": repo,
        "is_publishable_lib": is_publishable_lib,
        "_top": sorted(top_entries),
        "_rel": all_rel[:1000],
    }
    profile["archetype"] = choose_archetype(profile)

    # drop internal keys from output for cleanliness but keep a trimmed top listing
    profile["top_level"] = profile.pop("_top")
    profile.pop("_rel", None)

    text = json.dumps(profile, indent=2, ensure_ascii=False)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"profile written to {args.out}")
        print(f"archetype={profile['archetype']} name={profile['name']} "
              f"languages={profile['languages'][:3]} frameworks={profile['frameworks'][:5]}")
    else:
        print(text)


if __name__ == "__main__":
    sys.exit(main())
