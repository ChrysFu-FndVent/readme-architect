# Presentation Recipes

Use these recipes after choosing an archetype and reading the analyzer's `presentation_profile`.
They are domain overlays, not templates: retain only elements supported by the project files and the
Step 2b design brief. A recipe must never create unsupported product claims or replace practical
documentation with decoration.

## Selection Rules

1. Start with the archetype in `style-archetypes.md` for the document skeleton.
2. Confirm the profile's `matched_terms` in the repository's name, manifest description, or source
   paths before applying a recipe.
3. Use at most one banner, one diagram, one compact badge set, and one feature grid by default.
4. Run `check_integrations.py` before calling `drawio`, `nano-banana-*`, or `generate-gpt-image-2`.
   If a route is unavailable, omit the asset or use Mermaid for diagrams.
5. Existing screenshots always outrank generated images. Generated images illustrate concepts; they
   never impersonate a real product screen.

## Food, Recipe, and Health

**Signals:** `recipe`, `cookbook`, `meal`, `nutrition`, `diet`, `food`, `health`, `wellness`,
`fitness`, or `workout` in real project metadata or paths.

- **Tone:** warm, clear, and encouraging. Use a light, consistent palette drawn from the project; if
  none exists, choose a restrained food/health palette rather than a clinical or cartoonish default.
- **Components:** a friendly feature grid, rounded `for-the-badge` or `flat-square` badges, and an
  optional generated ingredient, meal-planning, activity, or wellbeing illustration that reflects
  the actual feature set.
- **Diagram:** add a flow only when the project has a real sequence, such as ingredients → planning →
  saved plan, or device data → analysis → recommendation. Use draw.io when available, Mermaid when
  not.
- **Safety:** do not state medical efficacy, diagnosis, nutritional guarantees, or health outcomes
  unless the repository provides substantiated evidence and appropriate wording.

## Operational Workbenches and Admin Tools

**Signals:** `workbench`, `dashboard`, `workspace`, `admin`, `operations`, `workflow`, `crm`, or
`backoffice` in real project metadata or paths.

- **Tone:** calm, information-dense, and operational. Prefer flat/flat-square badges, concise
  headings, tables, and a low emoji density.
- **Components:** a clear system architecture diagram when there are multiple modules or services; a
  workflow diagram when states, approvals, or handoffs are evidenced; configuration and deployment
  tables when those files exist.
- **Visuals:** use generated imagery sparingly. A diagram that explains data flow, permissions, or
  handoffs has priority over a decorative banner.
- **Safety:** show only real roles, integrations, data stores, and permissions. Do not invent scale,
  SLAs, audit controls, or compliance claims.

## AI, Agent, and Model Systems

**Signals:** `agent`, `llm`, `rag`, `model`, `inference`, `prompt`, `machine learning`, or
`artificial intelligence` in real project metadata or paths.

- **Tone:** technical and legible. Use an architecture or pipeline diagram before decorative media.
- **Components:** capability tables, evidence-based model/provider badges, a real agent or data-flow
  diagram, and a limitations section when the code or docs define bounds.
- **Visuals:** favor schematic or geometric illustrations derived from actual components, such as
  retriever, evaluator, queue, model, and human review. Avoid generic neural-network imagery.
- **Safety:** do not claim autonomy, benchmark results, provider support, accuracy, or safety controls
  that cannot be traced to the project.

## Neutral Fallback

When no recipe is supported by repository evidence, follow the archetype defaults. Prefer useful
sections, a compact badge set, and a diagram only when structure warrants it. The goal is a README
that is recognizably about the project, not a generic visual theme.
