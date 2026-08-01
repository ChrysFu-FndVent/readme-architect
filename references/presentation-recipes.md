# Adaptive Presentation Signals

Use these signals after choosing an archetype and reading the analyzer's `presentation_profile`.
They are composable overlays, not domain templates: retain only elements supported by the project
files and the Step 2b design brief. A signal must never create unsupported product claims or
replace practical documentation with decoration.

## Selection Rules

1. Start with the archetype in `style-archetypes.md` for the document skeleton.
2. Confirm every signal's `matched_terms` in the repository's name, manifest description, or source
   paths before applying it. Signals can combine when they describe different real aspects of a
   project.
3. Set a component budget before composing signals: use at most one banner or illustration, one
   primary diagram, one compact badge set, one feature/gallery grid, and one evidence table by
   default. Add a second diagram only when it explains a distinct, documented concern.
4. Run `check_integrations.py` before calling `drawio`, `nano-banana-*`, or `generate-gpt-image-2`.
   If a route is unavailable, omit the asset or use Mermaid for diagrams.
5. Existing screenshots always outrank generated images. Generated images illustrate concepts; they
   never impersonate a real product screen.

## Signal Catalog

| Signal | Prefer | Avoid unless evidenced |
|---|---|---|
| **Friendly experience** | warm feature grid, rounded badges, contextual illustration | medical efficacy, guarantees, or outcomes |
| **Product showcase** | existing screenshots, demo links, concise feature gallery | generated UI screenshots or fictional interaction flows |
| **Workflow and operations** | state/workflow diagram, setup tables, real roles and handoffs | invented SLAs, scale, permissions, or integrations |
| **System and infrastructure** | architecture, deployment/integration map, configuration table | undocumented services, data stores, or cloud providers |
| **Data and research** | pipeline, genuine result table/chart, reproducibility notes | synthetic benchmarks, charts, or data claims |
| **Trust and governance** | trust boundary, permission flow, supported-controls table | security, compliance, or audit claims not documented in code |
| **Learning and community** | quick-start path, examples index, contribution/extension guide | unsupported support channels or certifications |
| **Creative showcase** | real asset gallery, intentionally visual feature grid, project-specific illustration | substituting generated media for the actual work |
| **AI and intelligence** | capability table, model/data-flow diagram, evidenced limitations | fabricated accuracy, providers, autonomy, or safeguards |

## Composition Examples

- A meal-planning mobile app can combine **friendly experience** with **product showcase**: use real
  screens first, a small feature grid, and one contextual illustration only if it adds meaning.
- A financial administration console can combine **workflow and operations**, **trust and
  governance**, and **system and infrastructure**: prioritize role-aware flow and integration maps;
  keep visual treatment restrained.
- A scientific visualizer can combine **data and research** with **creative showcase**: show genuine
  plots or assets, methodology, and a focused gallery rather than generic AI art.
- An AI developer platform can combine **AI and intelligence**, **system and infrastructure**, and
  **learning and community**: show the real pipeline, documented limitations, and extension path.

These examples demonstrate combinations, not an exhaustive taxonomy. For a project with no matching
signal, follow the archetype defaults and the project's existing voice.

## Neutral Fallback

When no recipe is supported by repository evidence, follow the archetype defaults. Prefer useful
sections, a compact badge set, and a diagram only when structure warrants it. The goal is a README
that is recognizably about the project, not a generic visual theme.
