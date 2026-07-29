# Style Archetypes

Each project maps to one archetype. The archetype fixes the **layout**, **tone**, **badge palette**,
**section set**, and **default visuals**. Detect the archetype from the analyzer profile, then apply
the matching preset and start from the matching file in `templates/`.

Detection uses the strongest signal; when several apply, prefer the more specific one
(cli-tool > library; monorepo overrides when multiple workspace packages exist).

---

## cli-tool

**Signals:** `bin` field in package.json, console_scripts/entry_points, argparse/click/typer/cobra/
commander/clap, a `man`/completions dir, name ends in `-cli`.

- **Layout:** classic left-aligned, compact. Optional small centered logo.
- **Tone:** practical, low emoji.
- **Badges:** package version, downloads, build, license, platform.
- **Sections:** Title → Badges → Tagline → TOC → About → Installation → Usage (command examples) →
  Commands (table) → Configuration → Examples → Contributing → License.
- **Visuals:** terminal recording/asciinema if present; a **flowchart** (drawio) for the command/
  data pipeline. Usually no banner.
- **Decoration:** command/flag tables, `<details>` for full flag list, `bash`-tagged code fences,
  `> [!TIP]` for shortcuts.

## library

**Signals:** importable package, public API, published to npm/PyPI/crates.io/pkg.go.dev, no app
entrypoint, has `exports`/`__init__.py`/`lib.rs`.

- **Layout:** classic left-aligned, dense, information-first.
- **Tone:** precise, minimal emoji.
- **Badges:** build, coverage, version, downloads, types, bundle size, license.
- **Sections:** Title → Badges → Tagline → TOC → About → Install → Usage (import + call) → API →
  Examples → Contributing → License.
- **Visuals:** rarely a banner; optional small logo. Diagram only if the lib has notable internal
  architecture.
- **Decoration:** API/parameter tables, `<details>` for advanced usage, precise code fences.

## web-app

**Signals:** React/Vue/Svelte/Angular/Next/Nuxt/Django/Rails/Laravel/Spring app, `public/` or
`src/pages`, Dockerfile + serve, `.env.example`, deploy config (vercel/netlify/fly/render).

- **Layout:** **centered-hero** (logo/banner + badges + tagline + demo links), then sections.
- **Tone:** friendly, moderate emoji.
- **Badges:** build/deploy, license, live-demo, tech-stack (static Built-With badges).
- **Sections:** Hero → TOC → About → Features (grid) → Demo/Screenshots → Architecture → Built With →
  Getting Started (Prereqs/Install) → Usage → Configuration → Deployment → Roadmap → Contributing →
  License → Acknowledgments.
- **Visuals:** **banner** (nano-banana-pro) + **architecture diagram** (drawio); real screenshots if
  present.
- **Decoration:** hero block, feature grid table, dividers, emoji headings, star-history card,
  callouts.

## framework

**Signals:** large dev-facing tool/framework, plugin/ecosystem dirs, docs site, many stars, strong
brand name, `packages/` with a core.

- **Layout:** **centered-hero** with strong branding, big logo, prominent CTAs (Docs / Quickstart /
  Discord).
- **Tone:** polished, confident, moderate emoji.
- **Badges:** version, downloads, build, coverage, chat/community, sponsors, license.
- **Sections:** Hero → TOC → About → Why/Features (grid) → Quick Start → Architecture → Ecosystem/
  Plugins → Docs links → Benchmarks (if real) → Roadmap → Contributing → Sponsors → License.
- **Visuals:** **banner + logo** (nano-banana-pro), **architecture diagram** (drawio), contributors
  montage.
- **Decoration:** all techniques used tastefully; dividers between major blocks, dynamic cards.

## ml-ai

**Signals:** notebooks, `train.py`/`inference.py`, `requirements.txt` with torch/tensorflow/
transformers/sklearn, `models/`, `data/`, `configs/`, a paper/arXiv link, `CITATION.cff`.

- **Layout:** classic, research-oriented; optional centered title with a results teaser image.
- **Tone:** rigorous, low-to-moderate emoji.
- **Badges:** paper/arXiv, license, framework, Python version, HF model/dataset if present.
- **Sections:** Title → Badges → Tagline → TOC → Overview → Architecture (model/pipeline diagram) →
  Results/Benchmarks (tables) → Installation (conda/pip) → Datasets → Usage (train/inference) →
  Pretrained models → Citation (BibTeX) → Acknowledgments → License.
- **Visuals:** **pipeline/architecture diagram** (drawio); result plots if present. Banner optional.
- **Decoration:** benchmark tables, `<details>` for full hyperparameters, `python`/`bash` fences,
  BibTeX block, callouts for reproducibility notes.

## monorepo

**Signals:** pnpm/yarn/npm workspaces, lerna/nx/turbo, cargo workspace, multiple `packages/*` with
their own manifests.

- **Layout:** classic; a packages table front-and-center.
- **Tone:** organized, low emoji.
- **Badges:** repo-level build, license; per-package version badges in the table.
- **Sections:** Title → Badges → Tagline → TOC → About → Packages (table with links) → Repo setup
  (install/build/test at root) → Development workflow → Contributing → License.
- **Visuals:** a **module/dependency diagram** (drawio) across packages.
- **Decoration:** packages table with per-package badges, `<details>` per package details.

## minimal

**Signals:** very few files, config/dotfiles/docs-only repo, no build system.

- **Layout:** lean, single-column, no hero.
- **Tone:** neutral.
- **Badges:** license only (and maybe stars).
- **Sections:** Title → Tagline → About → Usage → License.
- **Visuals:** none by default.
- **Decoration:** minimal — a couple of badges, clean tables, code fences.

---

## Style parameter cheat-sheet

| Archetype | Layout | Emoji | Badge style | Banner | Diagram |
|---|---|---|---|---|---|
| cli-tool | left | low | flat | no | flowchart |
| library | left | minimal | flat | no | optional |
| web-app | hero | moderate | for-the-badge | yes | architecture |
| framework | hero | moderate | for-the-badge | yes | architecture |
| ml-ai | left/teaser | low | flat | optional | pipeline |
| monorepo | left | low | flat | no | module map |
| minimal | left | none | flat | no | none |
