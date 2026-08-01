# Badges Catalog

shields.io badge patterns by category. Replace `OWNER`, `REPO`, `PACKAGE` with real values from the
analyzer profile (git remote → `owner/repo`; package name from the manifest). Keep one consistent
`style` across the whole README. Only emit a badge that resolves to a **real** resource.

`style` options: `flat` (default, dense/library), `flat-square`, `for-the-badge` (bold, project-opening
layouts), `plastic`, `social`.

## Repo / community (dynamic, GitHub)

```markdown
![Stars](https://img.shields.io/github/stars/OWNER/REPO?style=flat)
![Forks](https://img.shields.io/github/forks/OWNER/REPO?style=flat)
![Issues](https://img.shields.io/github/issues/OWNER/REPO)
![Pull Requests](https://img.shields.io/github/issues-pr/OWNER/REPO)
![Contributors](https://img.shields.io/github/contributors/OWNER/REPO)
![Last commit](https://img.shields.io/github/last-commit/OWNER/REPO)
![Commit activity](https://img.shields.io/github/commit-activity/m/OWNER/REPO)
![Repo size](https://img.shields.io/github/repo-size/OWNER/REPO)
```

## CI / build / coverage (only if CI/coverage exists)

```markdown
![CI](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/CI_FILE.yml?branch=main)
![Coverage](https://img.shields.io/codecov/c/github/OWNER/REPO)
```
`CI_FILE.yml` is the actual workflow file name in `.github/workflows/`.

## Version / downloads (per ecosystem — only if published)

```markdown
<!-- npm -->
![npm version](https://img.shields.io/npm/v/PACKAGE)
![npm downloads](https://img.shields.io/npm/dm/PACKAGE)
![bundle size](https://img.shields.io/bundlephobia/minzip/PACKAGE)
![types](https://img.shields.io/npm/types/PACKAGE)

<!-- PyPI -->
![PyPI](https://img.shields.io/pypi/v/PACKAGE)
![Python versions](https://img.shields.io/pypi/pyversions/PACKAGE)
![PyPI downloads](https://img.shields.io/pypi/dm/PACKAGE)

<!-- crates.io -->
![Crates.io](https://img.shields.io/crates/v/PACKAGE)
![Crates downloads](https://img.shields.io/crates/d/PACKAGE)

<!-- Go -->
![Go Reference](https://pkg.go.dev/badge/github.com/OWNER/REPO.svg)
![Go Report](https://goreportcard.com/badge/github.com/OWNER/REPO)

<!-- Docker -->
![Docker pulls](https://img.shields.io/docker/pulls/OWNER/REPO)
![Image size](https://img.shields.io/docker/image-size/OWNER/REPO)

<!-- Maven -->
![Maven Central](https://img.shields.io/maven-central/v/GROUP/ARTIFACT)
```

## License / release (dynamic)

```markdown
![License](https://img.shields.io/github/license/OWNER/REPO)
![Release](https://img.shields.io/github/v/release/OWNER/REPO)
![Tag](https://img.shields.io/github/v/tag/OWNER/REPO)
```

## Static tech-stack badges (Built With grid)

`https://img.shields.io/badge/<label>-<message>-<color>?logo=<logo>&logoColor=white`

```markdown
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?logo=rust&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?logo=go&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)
![Next.js](https://img.shields.io/badge/Next.js-000000?logo=nextdotjs&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?logo=vuedotjs&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?logo=nodedotjs&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)
```
Brand-color hexes above match each tool's identity; you may override the `<color>` to match the
project's own palette for a cohesive look. Look up the correct `logo=` slug from simpleicons.org.

## Custom / project-specific static badges

```markdown
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)
![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green)
![Made with love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)
![Status](https://img.shields.io/badge/status-beta-orange)
![arXiv](https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b)
```
Use `%20` for spaces and URL-encode symbols. Set `<color>` to the project's accent color for badges
you author, to reinforce the design language.

## Recommended ordering

`build/CI → coverage → version → downloads → license → community → chat/social`. In project-opening layouts,
use `for-the-badge` and center them; in library layouts, use `flat` on their own line under the
tagline.
