# Visual Composition

Use the visual plan after project analysis to select refined README visuals without treating every
repository as a marketing page. The plan is a proposal; verify each evidence field before embedding.

## Run the Planner

```bash
python3 "<skill-dir>/scripts/plan_readme_visuals.py" \
  --profile "<project-root>/.readme-architect/profile.json" \
  --out "<project-root>/.readme-architect/visual-plan.json"
```

It emits evidence-bound badge candidates, a separator treatment, visual-density budget, and requested
assets. Keep only what helps a reader understand or trust the project.

## Badge Rules

- Use the planner's dynamic CI badge only when it found an actual workflow and GitHub remote.
- Use static badges to communicate facts such as language, framework, manifest version, included
  tests, Docker files, or example configuration. `Tests: included` is not `Tests: passing`.
- Do not add coverage, releases, package downloads, security, deployment, star, or maintained badges
  without a verified public endpoint or repository fact.
- Respect `badge_budget`. Center a rich set in a project opening; put focused badges beneath a concise
  title in information-dense READMEs.

## Divider Rules

Use dividers between major blocks only. A rich project may use no more than three generated gradient
strips, each a thin `12:1` raster asset in the project's palette with no text, logo, or fake UI. If
image generation is unavailable, use the proposed emoji line or a plain Markdown rule instead.

```html
<p align="center"><img src="assets/readme/divider.png" alt="" width="100%" /></p>
```

For an emoji fallback, use at most two occurrences and select glyphs from real project signals:

```markdown
<p align="center">🌿 &nbsp; ✦ &nbsp; 🌿</p>
```

Do not mix unrelated emoji, use a divider after every heading, or rely on color alone to convey a
state.

## Generated Image Briefs

For each `visual_request`, compose an `imagegen` prompt from the design brief plus the request. State
the actual project domain, named components/motifs, intended README placement, aspect ratio, palette,
and exclusions. Use a different composition for each asset:

| Request | Composition | Required exclusions |
|---|---|---|
| Banner | wide scene with clean title-safe space | no text, fake UI, watermark, or unrelated objects |
| Contextual illustration | one real feature or domain concept, editorial/diagrammatic rather than UI | no fabricated screenshot, metric, or product claim |
| Gradient divider | thin abstract color/material rhythm from the project palette | no text, logo, gradient background for the whole README, or recognisable UI |
| Architecture | evidence map rendered twice, Chinese and English labels | no invented node, edge, provider, or outcome |

Inspect each image at its rendered README width. Reject cropped subjects, illegible labels, generic
visual metaphors, broken contrast, accidental text, or outputs that duplicate existing project media.
Make at most one targeted revision; otherwise omit the asset.
