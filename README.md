# README Architect

> A Qoder/Claude **Agent Skill** that reads your codebase and generates a personalized,
> style-matched, bilingual README — with optional AI-generated banners and draw.io architecture
> diagrams.

Point it at any project and it will:

1. **Analyze** the repo (languages, package managers, frameworks, entrypoints, CI, license, git remote).
2. **Classify** the project archetype — `library`, `cli-tool`, `web-app`, `framework`, `ml-ai`, `monorepo`, or `minimal`.
3. **Derive a design language** from the project's real domain, palette, and personality.
4. **Assemble** an English `README.md` + Chinese `README.zh-CN.md`, choosing sections, badges, layout, and tone that fit *this* project.
5. **Generate visuals** when it helps — architecture/flow diagrams via the [`drawio`](https://github.com) skill, banners/logos via `nano-banana-pro` (fallback `generate-gpt-image-2`).
6. **Validate** the output (anchors resolve, local images exist, no leftover placeholders).

## Personalization capabilities

Badges (static & dynamic) · centered/aligned HTML blocks & dividers · tasteful per-section emoji ·
collapsible `<details>` · comparison/parameter tables · live data cards (star history, stats) ·
`> [!NOTE]` callouts & syntax-highlighted code · anchor-navigation TOC — all dialed to the
archetype's tone (lean for libraries, rich for web-apps/frameworks).

## Install

Copy the `readme-architect/` folder into your agent's skills directory (e.g. `~/.qoder/skills/`,
`~/.claude/skills/`), then ask your agent to *"generate a README for this project."*

## Layout

```text
readme-architect/
├── SKILL.md                    # orchestration & workflow
├── references/
│   ├── section-library.md      # sections, ordering, when to include
│   ├── style-archetypes.md     # archetype → layout/tone/badge/section presets
│   ├── badges.md               # shields.io badge catalog
│   ├── decoration-toolkit.md   # the 9 personalization techniques
│   └── visual-assets.md        # drawio / nano-banana-pro / gpt-image-2 integration
├── templates/                  # per-archetype README skeletons
└── scripts/
    ├── analyze_project.py      # repo → profile.json (stdlib only)
    └── validate_readme.py      # anchors / links / placeholders check
```

## Requirements

- Python 3.8+ (scripts use only the standard library).
- Optional: the `drawio`, `nano-banana-pro`, or `generate-gpt-image-2` skills for visuals — the
  README degrades gracefully if they are unavailable.

## License

MIT — see [`LICENSE`](LICENSE).
