#!/usr/bin/env python3
"""Validate a generated README: TOC anchors, local asset links, leftover placeholders.

Standard library only. Exit code 0 = clean, 1 = issues found.
Usage: python3 validate_readme.py [--bilingual] path/to/README.md
"""
from __future__ import annotations

import os
import re
import sys
import argparse

try:
    from scripts.console import configure_utf8_stdio
except ModuleNotFoundError:
    from console import configure_utf8_stdio

PLACEHOLDER_PATTERNS = [
    (re.compile(r"\bTODO\b"), "leftover TODO"),
    (re.compile(r"\bFIXME\b"), "leftover FIXME"),
    (re.compile(r"example\.com"), "placeholder domain example.com"),
    (re.compile(r"\bOWNER/REPO\b"), "unresolved OWNER/REPO placeholder"),
    (re.compile(r"\byour_username\b|\bgithub_username\b|\brepo_name\b"), "template username/repo placeholder"),
    (re.compile(r"lorem ipsum", re.I), "lorem ipsum filler"),
    (re.compile(r"<PACKAGE>|<project-root>|<skill-dir>|<owner>|<repo>"), "unfilled angle-bracket placeholder"),
]

FENCE_RE = re.compile(r"^```")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$")
EXPLICIT_ANCHOR_RE = re.compile(r'<a\s+(?:id|name)=["\']([^"\']+)["\']', re.I)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
MD_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
HTML_SRC_RE = re.compile(r'<img[^>]*\ssrc=["\']([^"\']+)["\']', re.I)


def slugify(text):
    # GitHub-style anchor slug
    text = re.sub(r"<[^>]+>", "", text)  # strip html
    text = text.strip().lower()
    # remove emoji / symbols, keep word chars, spaces, hyphens
    text = re.sub(r"[^\w\s\-]", "", text, flags=re.UNICODE)
    text = text.replace(" ", "-")
    text = re.sub(r"-+", "-", text)
    return text


def strip_code_blocks(lines):
    out = []
    in_fence = False
    for ln in lines:
        if FENCE_RE.match(ln.strip()):
            in_fence = not in_fence
            out.append("")  # keep line numbers aligned
            continue
        out.append("" if in_fence else ln)
    return out


def main(argv=None):
    configure_utf8_stdio()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bilingual", action="store_true",
                        help="enforce the default Chinese-first, English-second layout")
    parser.add_argument("path", help="README file to validate")
    args = parser.parse_args(argv)
    path = os.path.abspath(args.path)
    if not os.path.isfile(path):
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2
    base = os.path.dirname(path)

    with open(path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()
    content = "".join(raw_lines)
    code_stripped = strip_code_blocks(raw_lines)
    prose = "".join(code_stripped)

    issues, warnings = [], []

    # 1. collect heading anchors
    anchors = set()
    slug_counts = {}
    for ln in code_stripped:
        m = HEADING_RE.match(ln.strip())
        if m:
            slug = slugify(m.group(2))
            if slug in slug_counts:
                slug_counts[slug] += 1
                anchors.add(f"{slug}-{slug_counts[slug]}")
            else:
                slug_counts[slug] = 0
                anchors.add(slug)
    for m in EXPLICIT_ANCHOR_RE.finditer(content):
        anchors.add(m.group(1).lower())

    # 2. check internal anchor links + local file links
    for m in MD_LINK_RE.finditer(prose):
        target = m.group(1).split(" ")[0].strip()
        if target.startswith("#"):
            anchor = target[1:].lower()
            if anchor and anchor not in anchors:
                issues.append(f"broken TOC/anchor link: {target}")
        elif re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
            continue  # external, not checked here
        else:
            local = target.split("#")[0]
            if local and not os.path.exists(os.path.join(base, local)):
                issues.append(f"local link target missing on disk: {local}")

    # 3. check local images exist (md + html)
    for regex in (MD_IMG_RE, HTML_SRC_RE):
        for m in regex.finditer(content):
            src = m.group(1).strip()
            if re.match(r"^[a-z]+://", src) or src.startswith("data:"):
                continue  # remote/embedded (badges, dynamic cards)
            if not os.path.exists(os.path.join(base, src)):
                issues.append(f"local image missing on disk: {src}")

    # 4. placeholders (only in prose, not code samples)
    for regex, label in PLACEHOLDER_PATTERNS:
        if regex.search(prose):
            issues.append(f"{label}")

    # 5. structural warnings
    if not re.search(r"^#\s+", content, re.M) and not re.search(r"<h1\b", content, re.I):
        issues.append("no top-level H1 title found")
    if len(raw_lines) > 100 and "table of contents" not in content.lower() \
            and not re.search(r"<summary>[^<]*contents", content, re.I):
        warnings.append("README > 100 lines but no Table of Contents detected")
    if "license" not in content.lower():
        warnings.append("no License section detected")

    # 6. default bilingual output contract
    if args.bilingual:
        zh_matches = list(re.finditer(r'<a\s+(?:id|name)=["\']简体中文["\']', content, re.I))
        en_matches = list(re.finditer(r'<a\s+(?:id|name)=["\']english["\']', content, re.I))
        if len(zh_matches) != 1:
            issues.append("bilingual layout requires exactly one 简体中文 anchor")
        if len(en_matches) != 1:
            issues.append("bilingual layout requires exactly one english anchor")
        if zh_matches and en_matches and zh_matches[0].start() > en_matches[0].start():
            issues.append("bilingual layout must place the Chinese body before the English body")
        switch = re.search(r'href=["\']#简体中文["\'].*href=["\']#english["\']', content, re.I | re.S)
        if not switch:
            issues.append("bilingual layout requires a Chinese/English anchor switch")
        markdown_h1s = [ln for ln in code_stripped if re.match(r"^#\s+", ln)]
        html_h1s = re.findall(r"<h1\b", content, re.I)
        if len(markdown_h1s) + len(html_h1s) != 1:
            issues.append("bilingual layout requires exactly one shared H1 title")
        if zh_matches and re.search(r"<h1\b|^#\s+", content[:zh_matches[0].start()], re.I | re.M) is None:
            issues.append("the shared H1 title must appear before the Chinese body")
        if "README.zh-CN.md" in prose:
            issues.append("default bilingual output must not link to README.zh-CN.md")

    # report
    print(f"Validating: {path}")
    print(f"  headings/anchors: {len(anchors)} | lines: {len(raw_lines)}")
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  ! {w}")
    if issues:
        print("\nISSUES (fix these):")
        for i in issues:
            print(f"  ✗ {i}")
        print(f"\n{len(issues)} issue(s) found.")
        return 1
    print("\n✓ No blocking issues found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
