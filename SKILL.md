---
name: readme-architect
description: Automatically generate a personalized, style-matched bilingual README for a project by analyzing its code and files. The single README.md keeps its title and tagline in English, then presents Chinese content before its English equivalent. Detects the project's archetype (library, CLI, web/app, framework, ML/AI, monorepo, minimal) and adapts layout, sections, badges, and tone accordingly. Integrates the drawio skill (with a Mermaid fallback) for architecture/flow diagrams and the nano-banana-pro / nano-banana-flash / generate-gpt-image-2 skills for banners/logos/illustrations. Use when the user asks to create, generate, write, refresh, or beautify a README / project documentation from a codebase.
---

# README Architect

Generate a README that looks like it was hand-crafted for **this specific project** — right sections, right layout, right visuals — not a generic fill-in-the-blanks template.

## Operating mode

This skill runs **fully automatically** by default: analyze → classify → select components → generate visuals → assemble bilingual README → validate → report. Do not stop to ask questions unless a required input is missing (e.g. no readable project directory) or an outward-facing action needs consent (e.g. overwriting an existing hand-written README, or publishing).

Default output: one bilingual **`README.md`**. Render the document title and its short tagline in English once, then present the Chinese body first and the English body second. Use stable anchors and a language switch at the top. If the user specifies a single language, produce only that one.

## Workflow

### Step 1 — Analyze the project

Run the analyzer to build a structured profile (stdlib Python only, no install):

```bash
python3 "<skill-dir>/scripts/analyze_project.py" --root "<project-root>" --out "<project-root>/.readme-architect/profile.json"
```

The profile reports: project name, description, version, license, primary/secondary languages, package managers & manifests, detected frameworks, entrypoints/bin, scripts, test & CI presence, Docker, monorepo packages, existing docs/images, and the git remote (`owner/repo`) used for badges.

Read the JSON. Treat it as **evidence**, not gospel — confirm important facts against the actual files (open `package.json`, `pyproject.toml`, main entry, config) before writing claims. Never invent features, benchmarks, or usage that you cannot see in the code.

### Step 2 — Classify the archetype & pick a style

Map the profile to one archetype (see [references/style-archetypes.md](references/style-archetypes.md)):

| Signal | Archetype |
|---|---|
| Published package: `bin` field, entry CLI, argparse/click/cobra/commander | **cli-tool** |
| Importable package with public API, no app entry (lib on npm/PyPI/crates/go) | **library** |
| Web/app: React/Vue/Next/Django/Rails/Spring app, has UI, deployable service | **web-app** |
| Large framework/dev-tool with strong branding & ecosystem | **framework** |
| ML/AI/research: models, training/inference, datasets, notebooks, papers | **ml-ai** |
| Multiple workspace packages (pnpm/yarn/lerna/nx/cargo workspaces) | **monorepo** |
| Tiny/config/docs repo, few files | **minimal** |

Each archetype fixes a **layout** (centered-hero vs classic left-aligned vs lean), **tone** (emoji density, formality), a **badge palette**, and a **section set with ordering**. Pull the concrete preset from [references/style-archetypes.md](references/style-archetypes.md) and the corresponding file in `templates/`.

> The archetype is only the **baseline**. The final look must be tailored to *this* project (see Step 2b).

### Step 2b — Derive the project's design language

The archetype decides the skeleton; the project's own characteristics decide the skin. Extract a lightweight **design language** from real evidence and let it drive both layout decoration and every image-generation prompt:

- **Domain & purpose** — what the project actually does (from description, docs, module/dir names, dependencies). Drives illustration subject matter and metaphor.
- **Personality / tone** — playful vs enterprise vs research vs minimalist (infer from naming, existing README wording, emoji use, comments). Drives emoji density, layout richness, and art style.
- **Color palette** — reuse real brand colors when discoverable (existing logo, `theme`/`primary` in config, tailwind theme, CSS variables, `manifest.json` `theme_color`, docs site). Otherwise pick a palette that fits the domain, and reuse it consistently across banner, dividers, diagram accent color, and static badge colors.
- **Motifs & keywords** — recurring concepts/entities (e.g. “stream”, “graph”, “agent”, “wristband”) become visual motifs in the banner/illustration and node labels in diagrams.
- **Tech identity** — primary language/framework informs logo iconography and Built-With badges.

Record these as a short design brief and pass it into Step 4 (visuals) and the decoration choices in Step 5, so illustrations and typography feel designed *for this repo*, not generic. Never fabricate a brand color or motif that contradicts the code.

### Step 3 — Select components (sections)

Start from the archetype's section set, then **include only sections you have real content for** (from Step 1 evidence). Canonical ordering and per-section rules live in [references/section-library.md](references/section-library.md). Core ordering baseline (omit optional sections without content):

`Title → Banner/Logo → Badges → Tagline → TOC → About/Features → Architecture → Getting Started (Prerequisites/Install) → Usage/API → Configuration → Roadmap → Contributing → License → Acknowledgments/Citation`

Build badges from the git remote and detected facts using [references/badges.md](references/badges.md). Never emit a badge that points at a resource that does not exist (e.g. no coverage badge without coverage).

### Step 4 — Generate visual assets (conditional)

Decide per [references/visual-assets.md](references/visual-assets.md). Save all generated assets under `<project-root>/assets/readme/` and embed with **relative paths**.

**First, detect what's actually available** — never guess whether a companion skill or credential is present:

```bash
python3 "<skill-dir>/scripts/check_integrations.py"        # human-readable
python3 "<skill-dir>/scripts/check_integrations.py" --json  # machine-readable
```

This reports, per integration: image routes (`nano-banana-pro` / `nano-banana-flash` / `generate-gpt-image-2`) with `installed` + `usable_now` + what each `needs`, the drawio invocation (CLI on PATH **or** the macOS `draw.io.app` bundle), Mermaid (always available), which credentials are present (`XIAOHULI_API_KEY` env, `~/.codex/auth.json` `OPENAI_API_KEY`), and the **preferred banner route**. Let this report drive the choices below.

- **Architecture / flow / sequence diagram.** Generate when the project has meaningful structure (backend+frontend, services, ML pipeline, multi-module data flow). Feed it the real components you found.
  - If the report shows **drawio available**, build the `.drawio` XML for the detected diagram type (color nodes/edges with the Step 2b palette), export PNG via the reported invocation, and embed the PNG.
  - If drawio is **not** available, fall back to a native ` ```mermaid ` block (GitHub renders it inline, no binary needed) styled with the same palette via a `classDef`.
- **Banner / logo / illustration.** Generate for `web-app` / `framework` archetypes, or when the project has strong branding and no existing logo. Derive the prompt from the project's real domain, name, and palette (Step 2b). Use the **preferred banner route** from the report, following this fallback chain:
  1. `nano-banana-pro` (model `gemini-3-pro-image`) — best quality; needs `XIAOHULI_API_KEY`.
  2. `nano-banana-flash` (model `gemini-3.1-flash-image`) — faster; also needs `XIAOHULI_API_KEY`.
  3. `generate-gpt-image-2` — reuses the local `~/.codex/auth.json` `OPENAI_API_KEY`, so it works with no extra key.
  Move down the chain on a failed/`503`/model-unavailable response or a missing credential.
- **Never fabricate product screenshots.** Use real screenshots only if they already exist in the repo. Image-gen is for banners/logos/abstract illustrations, not fake UI.

**API-key handling.** nano-banana pro/flash require `XIAOHULI_API_KEY` in the environment. If the report shows both nano-banana skills installed but blocked on that key, and `generate-gpt-image-2` is usable, silently use the gpt-image-2 fallback. If **no** image route is usable and the user asked for a banner/logo, ask the user once to `export XIAOHULI_API_KEY=<key>` (or confirm skipping the image) — never hard-code, echo, or log the key value.

If a tool/skill or its credentials are unavailable, **degrade gracefully**: skip that asset, proceed, and note the omission in the final report. Do not block the README on missing visuals.

Invocation contracts (verify a skill's own SKILL.md before calling — do not guess flags):
- drawio (PATH): `drawio -x -f png --scale 2 -o out.png in.drawio`; macOS app bundle: `/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png --scale 2 -o out.png in.drawio`; Linux headless: prefix with `xvfb-run -a`.
- nano-banana-pro / nano-banana-flash: `python3 <skill-dir>/scripts/generate_image.py --prompt "<prompt>" --output "<assets/readme/banner.png>"` (needs `XIAOHULI_API_KEY`).
- generate-gpt-image-2: `node <skill-dir>/scripts/gpt_image_2.mjs generate --prompt "<prompt>" --out "<assets/readme/banner.png>"` (uses `~/.codex/auth.json`).

### Step 5 — Assemble the README

Write one `README.md`. Render the title and short tagline in English only, once at the top. Under that shared header, add a language switch and two anchored body sections: **Simplified Chinese first**, followed by a faithful English equivalent. The two body sections must have the same facts, structure, assets, and navigation targets, with distinct anchors. Do not create `README.zh-CN.md` for the default bilingual mode.

```markdown
<div align="right"><a href="#简体中文">简体中文</a> | <a href="#english">English</a></div>
```

Follow the chosen template in `templates/` for markup patterns (centered hero blocks, `<details>` TOC, reference-style link definitions, Built-With badge grid, back-to-top links). Apply the visual polish techniques in [references/decoration-toolkit.md](references/decoration-toolkit.md) — badges, centered/aligned HTML blocks, decorative dividers, tasteful per-section emoji, collapsible `<details>`, comparison/parameter tables, live data cards (star history / stats), `> [!NOTE]` callouts, language-tagged code fences, and anchor navigation. Drive every styling choice from the **Step 2b design brief** (real palette → badge/divider/diagram colors; personality → emoji density & richness; motifs → emoji/glyph choices) on top of the archetype baseline (lean for libraries, rich for web-app/framework), so the layout looks designed for *this* project. Match the project's existing tone if a README or docs already exist.

**Safety on overwrite:** if a substantive hand-written `README.md` already exists, do not silently overwrite it — write the complete bilingual document to `README.generated.md` and tell the user, unless they explicitly asked to replace it.

### Step 6 — Validate

```bash
python3 "<skill-dir>/scripts/validate_readme.py" "<project-root>/README.md"
```

This checks: required sections present, TOC anchors resolve, local image/link paths exist on disk, and no leftover template placeholders (`<...>`, `TODO`, `example.com`). Fix every reported issue before finishing.

### Step 7 — Report

Summarize: detected archetype & style, sections included (and notable ones skipped + why), assets generated (with tool used) or skipped, validation result, and the output file paths.

## Guardrails

- Evidence over invention: every feature/command/badge must trace to a real file or fact.
- Keep generated files inside the project workspace; never leak API keys into prompts, files, or logs.
- Retry a failing external skill at most once, then degrade gracefully and report.
- Respect existing hand-written docs; prefer additive/side-file output when unsure.
- **Portable, not machine-specific.** Never assume the author's setup. Always run `check_integrations.py` on the current machine and act on *its* results — different OS (macOS/Linux/Windows), different skill install roots (override with `README_ARCHITECT_SKILL_ROOTS`), and different credentials (`XIAOHULI_API_KEY` or an OpenAI credential via `~/.codex/auth.json` / `OPENAI_API_KEY`) are all expected. If a companion skill is missing, use the next route in the chain; if a needed key is absent, ask the user for that exact variable once, else skip the asset. The README must still generate end-to-end with whatever is available.

## Reference files

- [references/section-library.md](references/section-library.md) — every section, ordering, when to include, markup.
- [references/style-archetypes.md](references/style-archetypes.md) — archetype → layout/tone/badge/section presets.
- [references/badges.md](references/badges.md) — shields.io badge catalog by category.
- [references/decoration-toolkit.md](references/decoration-toolkit.md) — the 9 personalization techniques (badges, dividers, alignment, emoji, `<details>`, tables, dynamic cards, callouts, anchors) with copy-ready markup.
- [references/visual-assets.md](references/visual-assets.md) — when & how to call drawio / nano-banana-pro / gpt-image-2.
- `templates/*.md` — ready-to-adapt README skeletons per archetype.

## Scripts

- `scripts/analyze_project.py` — build the structured project profile (Step 1).
- `scripts/check_integrations.py` — detect available image routes, drawio (PATH/app bundle), Mermaid, and credentials **on the current machine**; prints the preferred banner route (Step 4). `--json` for machine output. Portable across macOS/Linux/Windows; extend skill search paths with `README_ARCHITECT_SKILL_ROOTS`.
- `scripts/validate_readme.py` — validate sections, TOC anchors, local paths, placeholders (Step 6).
