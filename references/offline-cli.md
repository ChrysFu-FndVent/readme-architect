# Offline CLI

Use the CLI for deterministic, network-free generation from repository evidence. It complements the
full Codex skill; it does not call a model, image API, or external documentation service.

## Install

Install from a release executable, the release skill archive, or the repository package:

```bash
python -m pip install .
readme-architect --version
```

## Safety Contract

| Command | README effect | Other output |
|---|---|---|
| `readme-architect PATH` | Write `README.generated.md`; keep `README.md` unchanged | Write the candidate SVG under `.readme-architect/generated/` |
| `readme-architect PATH --dry-run` | No write | Analyze and validate in memory |
| `readme-architect PATH --diff` | No write | Print a unified diff against `README.md` |
| `readme-architect PATH --write` | Atomically replace `README.md` without prompting | Write the SVG under `assets/readme/` |
| `readme-architect PATH --suggest-only` | No write | Print evidence and recommendations |
| `readme-architect PATH --suggest-only --json` | No write | Print machine-readable JSON |

`--write --diff` prints the diff and then writes. Reject `--write --dry-run`, `--write --output`, and
`--json` without `--suggest-only` instead of choosing an ambiguous behavior.

`--output FILE` accepts project-relative or absolute candidate paths. The generated banner remains
under `PATH/.readme-architect/generated/`, and its README reference is calculated relative to `FILE`
so nested and out-of-project previews remain valid.

## Offline Output

- Build the title, facts, badges, commands, and repository map only from analyzer fields backed by
  manifests, source paths, test directories, CI files, license files, and the Git remote.
- Put the shared project opening and complete table of contents before the Chinese body.
- Render the Chinese body before its English counterpart with identical facts and topology.
- Generate a local SVG banner from the project name, primary language, archetype, and detected
  presentation signals. Do not imitate a screenshot or add an unsupported claim.
- Render paired Mermaid repository maps only when at least two relevant top-level directories exist.
  Directory edges mean containment, not runtime data flow.
- Omit unsupported installation, usage, CI, release, license, framework, or architecture claims.

## Full Skill Boundary

Use the full skill workflow when the user wants inspected project screenshots, draw.io exports,
localized architecture prose, or AI-generated raster artwork. Treat CLI output as a safe candidate,
not as evidence that richer integrations are installed or usable.
