# Section Library

Canonical README sections, their ordering, when to include them, and markup patterns.
Adapted from the standard-readme spec and widely-used templates (Best-README-Template,
make-a-readme). Include a section **only when there is real content for it** — an empty
or placeholder section is worse than no section.

## Canonical ordering

```
1.  Title
2.  Banner / Logo            (optional, directly after title)
3.  Badges                   (optional, newline-delimited, no heading)
4.  Tagline / Short desc     (required, < 120 chars, own line, no heading)
5.  Language switch          (optional, for multilingual READMEs)
6.  Table of Contents        (required if README > ~100 lines; immediately after the opening)
7.  About / Overview         (what & why)
8.  Key Features             (bulleted or feature grid)
9.  Demo / Screenshots       (real media only)
10. Architecture             (diagram + short explanation)
11. Built With / Tech Stack  (badge grid)
12. Getting Started
      - Prerequisites
      - Installation
13. Usage / Quick Start
14. API Reference            (or link to API.md)
15. Configuration            (env vars, config files, flags)
16. Examples
17. Roadmap
18. Testing
19. Deployment
20. Contributing             (link to CONTRIBUTING.md if present)
21. Security                 (if security-sensitive)
22. FAQ / Troubleshooting
23. Maintainers / Contributors
24. Acknowledgments / Credits
25. Citation                 (ML/research projects; BibTeX)
26. License                  (must be last)
```

Optional sections may be omitted; the relative order of those you keep must follow the list.

## Per-section rules

### Title
Required. Match the repo / package name. Optional descriptive title with the canonical name in
italic parens: `# Project Nice Name _(project-name)_`.

### Banner / Logo
Optional, no heading, directly after the title. Link to a **local** image in the repo
(`assets/readme/banner.png`). Use for centered project-opening layouts. Generate via nano-banana-pro /
gpt-image-2 when appropriate (see visual-assets.md).

### Badges
Optional, no heading, newline-delimited. Prefer shields.io. Order: build/CI → coverage →
version/package → downloads → license → community (stars/PRs welcome/chat). Only include badges
that resolve to a real resource. See badges.md.

### Tagline / Short description
Required. One line, < 120 chars, no `>` prefix. Should match the GitHub repo description and the
package manager `description` field when they exist. If neither exists, state only the verified
purpose, inputs, or outputs visible in the repository; do not infer a platform, audience, or promise.

### Table of Contents
Required for long READMEs. Place it immediately after the complete project opening (title, optional
banner/logo, badges, short tagline, and language switch) and before either language's About/Overview
body. Do not put a multi-paragraph project introduction, feature list, screenshot gallery, or other
long content before it. Two common styles:
- Collapsible: wrap in `<details><summary>Table of Contents</summary> … </details>`.
- Flat bullet list of `[Section](#anchor)` links.
Anchors are the lower-cased heading with spaces → `-` and punctuation removed.

### About / Overview
The "what and why". 1–3 short paragraphs. Cover the problem it solves and who it is for. Move long
motivation to a Background subsection if needed. Derive the wording from source, manifests, or
project-owned docs. Do not name an AI host, package registry, customer type, integration, or supported
environment unless a project file or the user explicitly establishes it.

### Key Features
Scannable. Bullets with a leading bold label, or a 2–3 column feature grid (HTML table). Only list
features that exist in the code.

### Demo / Screenshots
Real media only (screenshots, GIFs, asciinema, hosted video). Reference existing repo images; do
**not** synthesize fake product screenshots.

### Architecture
Short prose + a diagram (drawio). Use for multi-component systems, pipelines, services. Embed the
exported PNG with a relative path and alt text.

### Built With / Tech Stack
Badge grid of major frameworks/languages/tools actually used (from the analyzer's `frameworks` and
`languages`). Leave minor plugins to Acknowledgments.

### Getting Started → Prerequisites / Installation
Required for runnable projects (optional for pure-docs repos). Copy-paste-ready commands in fenced
blocks with the right language hint. Prefer the project's actual package manager & scripts. Never
invent a host-specific installation directory; when the host is unknown, state that the user must use
their host's configured skills or extension directory.

### Usage / Quick Start
The single most important section for adoption. A minimal runnable example: import + call, or the
first CLI command, or `npm run dev`. Derive from real entrypoints/scripts.

### API Reference
Describe exported functions/objects, signatures, return types. If large, link to `API.md` or a docs
site instead of inlining.

### Configuration
Env vars (table: name / required / default / description), config files, CLI flags. Populate from
`.env.example`, config schema, or flag definitions found in code.

### Roadmap
Checkbox list of done / planned items. Only include if you can infer real direction (issues,
TODOs, milestones); otherwise omit.

### Testing / Deployment
Include when tests / CI / Dockerfiles / deploy configs exist. Show the real commands.

### Contributing
Include only when the repository has a contribution policy, issue template, code of conduct, or an
explicit user instruction. State whether PRs are accepted only when that policy is documented; link to
`CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` when present.

### Maintainers / Contributors
Optional. Maintainer list with a contact link, and/or a `contrib.rocks` contributors image:
`https://contrib.rocks/image?repo=<owner>/<repo>`.

### Acknowledgments / Credits
Optional. Libraries, inspirations, sponsors.

### Citation
For research/ML projects. Provide a `bibtex` code block and mention `CITATION.cff` if present.

### License
Required, last section. State the SPDX identifier and link to the `LICENSE` file. Populate from the
detected license.

## Reusable markup snippets

Centered project opening (Hero section):
```html
<div align="center">
  <img src="assets/readme/logo.png" alt="Logo" width="120" />
  <h1>Project Name</h1>
  <p><em>One-line tagline.</em></p>
  <!-- badges -->
</div>
```

Back-to-top link (place after long sections):
```html
<p align="right">(<a href="#readme-top">back to top</a>)</p>
```
with `<a id="readme-top"></a>` at the very top of the file.

Reference-style links (keeps body readable; define at file end):
```markdown
[stars-shield]: https://img.shields.io/github/stars/OWNER/REPO?style=for-the-badge
[stars-url]: https://github.com/OWNER/REPO/stargazers
```

Feature grid:
```html
<table>
  <tr>
    <td width="33%"><b>⚡ Fast</b><br/>Short benefit sentence.</td>
    <td width="33%"><b>🔒 Secure</b><br/>Short benefit sentence.</td>
    <td width="33%"><b>🧩 Extensible</b><br/>Short benefit sentence.</td>
  </tr>
</table>
```
