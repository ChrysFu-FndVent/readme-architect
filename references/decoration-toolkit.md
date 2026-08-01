# Decoration Toolkit

The concrete markup techniques used to make a README visually polished and easy to scan.
Apply them **in service of the content**, matched to the project's archetype/tone (see
style-archetypes.md) — decoration never invents facts and never fights readability.

These map to the 9 personalization capabilities this skill guarantees.

---

## 0. Tune decoration to the project's design language (mandatory)

The archetype (style-archetypes.md) sets the baseline richness; the project's own **design language**
(Step 2b: domain, personality, palette, motifs, tech identity) decides the concrete styling — exactly
as it drives image prompts in visual-assets.md. Layout must feel designed *for this repo*, not stamped
from a template. Translate the design brief into decisions:

- **Palette → color everything from the real brand.** Use the project's discovered brand/theme hex
  colors for static badge colors, `for-the-badge` label backgrounds, decorative divider/bar images,
  the diagram accent, and any custom section headers. Keep the *same* palette across banner, badges,
  dividers, and diagram so the page reads as one system. Never invent a brand color that contradicts
  the code; fall back to a domain-fitting palette only when none is discoverable.
- **Personality → emoji density, badge style, and richness.** Playful/consumer → generous emoji,
  rounded/vibrant accents, dynamic cards. Enterprise/fintech/health → few or no emoji, restrained
  `flat` badges, formal wording. Developer-tool/framework → geometric, high-contrast, iconographic.
  Research/ML → sober, table-forward, minimal ornament. Minimalist → single accent, lots of whitespace.
- **Motifs → emoji & symbol choices.** Pick section emoji and divider glyphs that echo the project's
  real motifs/domain (e.g. a data-stream tool leans 🌊/📊; a security tool leans 🔒/🛡️) instead of the
  generic default mapping below. The table in §4 is a fallback, not a mandate.
- **Tech identity → Built-With badges & code fences.** Use the real primary language/framework for
  static Built-With badge logos and for the language tag on every fenced code block.
- **Existing tone wins.** If a README/docs/site already exist, match their voice, heading style, and
  emoji habit rather than overriding them.

> Record these choices alongside the Step 2b design brief so badges, dividers, emoji, and diagrams all
> resolve to the same palette and personality.

---

## 1. Badge decoration (shields.io — static & dynamic)

Colorful labels for language, version, repo stats, CI, license. Put them at the top, under the
title/tagline, newline- or space-delimited. Full catalog in [badges.md](badges.md).

- **Dynamic** (auto-updates from GitHub/registries):
  ```markdown
  ![Stars](https://img.shields.io/github/stars/OWNER/REPO?style=flat)
  ![Build](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml)
  ![npm](https://img.shields.io/npm/v/PACKAGE)
  ```
- **Static** (fixed text/color, great for tech stack):
  ```markdown
  ![Made with](https://img.shields.io/badge/Made%20with-TypeScript-3178C6?logo=typescript&logoColor=white)
  ```
- Pick one `style=` (`flat`, `flat-square`, `for-the-badge`) and use it consistently. `for-the-badge`
  suits centered project-opening layouts; `flat` suits dense library READMEs.

## 2. Heading & divider beautification (centered titles + separators)

Use HTML for centering and visual section breaks between major blocks.

- Centered title block:
  ```html
  <div align="center"><h1>🚀 Project Name</h1></div>
  ```
- Dividers between big sections:
  - Simple rule: `---` (Markdown) or `<hr/>`.
  - Symbol divider: `<div align="center">· · ·</div>` or `<p align="center">✦ ✦ ✦</p>`.
  - Decorative image divider (gradient bar / wave):
    ```markdown
    ![divider](assets/readme/divider.png)
    ```
    A thin gradient bar or section illustration can be generated (see visual-assets.md).

## 3. Flexible alignment & multi-column layout

Center text/images and place images side by side using HTML.

- Center anything: wrap in `<div align="center"> … </div>` or `<p align="center"> … </p>`.
- Side-by-side images (columns):
  ```html
  <p align="center">
    <img src="assets/readme/shot1.png" width="45%" />
    &nbsp;&nbsp;
    <img src="assets/readme/shot2.png" width="45%" />
  </p>
  ```
- Two-column content via table (no borders needed): use `<table><tr><td>…</td><td>…</td></tr></table>`.

## 4. Emoji section markers (tasteful)

Give each section heading a leading emoji so modules are instantly distinguishable. Keep it
**one emoji per heading**, consistent, and skip entirely for strictly formal/enterprise projects.
Suggested mapping:

| Section | Emoji | Section | Emoji |
|---|---|---|---|
| About / Overview | ✨ / 📖 | Features | 🎯 / ⚡ |
| Architecture | 🏗️ | Tech Stack | 🧰 |
| Getting Started | 🚀 | Installation | 📦 |
| Usage | 💡 / 🔧 | Configuration | ⚙️ |
| API | 📚 | Roadmap | 🗺️ |
| Testing | 🧪 | Deployment | ☁️ |
| Contributing | 🤝 | Security | 🔒 |
| FAQ | ❓ | License | 📄 |
| Acknowledgments | 🙏 | Citation | 📝 |

## 5. Collapsible detail blocks (`<details>`)

Fold long code, verbose tutorials, big option tables, or logs to keep the top of the page clean.

```html
<details>
<summary>📂 Full project structure</summary>

```text
src/
  index.ts
  ...
```

</details>
```
Note the blank lines around the inner content so Markdown renders inside the block. Good uses: full
directory tree, exhaustive config/flags, advanced examples, changelog, troubleshooting.

## 6. Table layout

Use Markdown tables for feature comparisons and parameter lists; use HTML tables when you need
column widths, centering, or embedded images/badges.

```markdown
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--port` | number | `3000` | Server port |
```

## 7. Dynamic data cards (live third-party widgets)

Real-time repo/stats visuals that update themselves. Include only for public GitHub repos and only
when they add signal; keep to 1–2 so the page stays fast.

- Repo stats card:
  ```markdown
  ![Repo stats](https://github-readme-stats.vercel.app/api/pin/?username=OWNER&repo=REPO)
  ```
- Language breakdown:
  ```markdown
  ![Top langs](https://github-readme-stats.vercel.app/api/top-langs/?username=OWNER&layout=compact)
  ```
- Star history:
  ```markdown
  [![Star History](https://api.star-history.com/svg?repos=OWNER/REPO&type=Date)](https://star-history.com/#OWNER/REPO&Date)
  ```
- Contributors montage:
  ```markdown
  ![Contributors](https://contrib.rocks/image?repo=OWNER/REPO)
  ```

## 8. Highlight / callout blocks & code highlighting

- GitHub alert callouts for notes, tips, warnings:
  ```markdown
  > [!NOTE]
  > Useful context the reader should know.

  > [!TIP]
  > A shortcut or best-practice.

  > [!WARNING]
  > Something that can cause data loss or breakage.
  ```
  (Also `[!IMPORTANT]`, `[!CAUTION]`.) Fall back to `> **Note:**` on renderers without alert support.
- Always tag fenced code blocks with the correct language for syntax highlighting
  (```` ```ts ````, ```` ```python ````, ```` ```bash ````, ```` ```jsonc ````). Use the language
  detected in the analyzer profile.

## 9. Anchor navigation / table of contents

For long READMEs, add a jump menu at the top and back-to-top links.

- Anchors are auto-generated from headings: lower-case, spaces → `-`, punctuation dropped, emoji
  stripped. `## 🚀 Getting Started` → `#-getting-started` (leading emoji leaves a leading `-`), so
  prefer verifying anchors with the validator, or add explicit anchors:
  ```html
  <a id="getting-started"></a>
  ## 🚀 Getting Started
  ```
- Collapsible TOC keeps the header compact:
  ```html
  <details><summary>📑 Table of Contents</summary>

  - [About](#about)
  - [Getting Started](#getting-started)
  - [Usage](#usage)

  </details>
  ```
- Place `<a id="readme-top"></a>` at the very top and a back-to-top link after long sections
  (see section-library.md).

---

## Restraint rules

- Decoration follows the project's design language (§0), not just the archetype: the archetype sets
  the baseline richness, the design brief (palette/personality/motifs) sets the actual colors, emoji,
  and glyphs. When they conflict, honor the project's real tone.
- Don't stack every technique on one README. Choose per archetype: libraries stay lean (badges +
  TOC + tables + code highlight); web-apps/frameworks go rich (project opening, emoji, feature grid, dynamic
  cards, dividers).
- Every dynamic widget and badge must point at a **real** owner/repo/package. If the repo isn't on
  GitHub yet, prefer static badges and skip live cards.
- Keep total remote-image requests modest; the README must render fast and degrade gracefully if a
  third-party widget service is down.
